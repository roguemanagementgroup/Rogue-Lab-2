[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidateNotNullOrEmpty()]
    [string] $OutputPath,

    [Parameter(Mandatory)]
    [switch] $IHaveWrittenAuthorization
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (-not $IHaveWrittenAuthorization) {
    throw 'Written authorization is required. This script collects no data without explicit operator attestation.'
}

if ($env:OS -ne 'Windows_NT') {
    throw 'This collection specification applies only to Windows endpoints.'
}

function Get-SafeValue {
    param(
        [scriptblock] $Query
    )

    try {
        return & $Query
    }
    catch {
        return 'unavailable'
    }
}

$os = Get-SafeValue { Get-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion' -ErrorAction Stop }
$defender = Get-SafeValue { Get-MpComputerStatus -ErrorAction Stop }
$bitlockerVolumes = Get-SafeValue { @(Get-BitLockerVolume -ErrorAction Stop) }
$firewallProfiles = Get-SafeValue { @(Get-NetFirewallProfile -ErrorAction Stop) }
$hotfixes = Get-SafeValue { @(Get-CimInstance -ClassName Win32_QuickFixEngineering -ErrorAction Stop) }

$defenderSummary = if ($defender -eq 'unavailable') {
    @{ antivirus = 'unavailable'; real_time_protection = 'unavailable'; service = 'unavailable' }
}
else {
    @{
        antivirus = if ($defender.AntivirusEnabled) { 'enabled' } else { 'disabled' }
        real_time_protection = if ($defender.RealTimeProtectionEnabled) { 'enabled' } else { 'disabled' }
        service = if ($defender.AMServiceEnabled) { 'enabled' } else { 'disabled' }
    }
}

$bitlockerSummary = if ($bitlockerVolumes -eq 'unavailable') {
    @{ system_volume_protection = 'unavailable'; protected_volume_count = 0 }
}
else {
    $systemVolume = $bitlockerVolumes | Where-Object { $_.VolumeType -eq 'OperatingSystem' } | Select-Object -First 1
    @{
        system_volume_protection = if ($null -eq $systemVolume) { 'unavailable' } elseif ($systemVolume.ProtectionStatus -eq 'On') { 'enabled' } else { 'disabled' }
        protected_volume_count = @($bitlockerVolumes | Where-Object { $_.ProtectionStatus -eq 'On' }).Count
    }
}

$firewallSummary = @{}
foreach ($profileName in @('Domain', 'Private', 'Public')) {
    if ($firewallProfiles -eq 'unavailable') {
        $firewallSummary[$profileName.ToLowerInvariant()] = 'unavailable'
    }
    else {
        $profile = $firewallProfiles | Where-Object { $_.Name -eq $profileName } | Select-Object -First 1
        $firewallSummary[$profileName.ToLowerInvariant()] = if ($null -eq $profile) { 'unavailable' } elseif ($profile.Enabled) { 'enabled' } else { 'disabled' }
    }
}

$latestUpdate = if ($hotfixes -eq 'unavailable') {
    'unavailable'
}
else {
    $updateDates = foreach ($hotfix in $hotfixes) {
        $parsed = [datetime]::MinValue
        if ([datetime]::TryParse([string] $hotfix.InstalledOn, [ref] $parsed)) {
            $parsed
        }
    }
    $date = $updateDates |
        Sort-Object -Descending |
        Select-Object -First 1
    if ($null -eq $date) { 'unavailable' } else { $date.ToString('yyyy-MM-dd') }
}

$summary = [ordered]@{
    format_version = '1.0'
    collection_mode = 'authorized-local-read-only'
    os = if ($os -eq 'unavailable') {
        [ordered]@{ product_family = 'Windows'; version = 'unavailable'; build = 'unavailable' }
    } else {
        [ordered]@{ product_family = 'Windows'; version = [string] $os.CurrentVersion; build = [string] $os.CurrentBuildNumber }
    }
    defender = $defenderSummary
    bitlocker = $bitlockerSummary
    firewall = $firewallSummary
    updates = [ordered]@{
        latest_install_date = $latestUpdate
        currentness = 'not-determined'
    }
}

$summary | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $OutputPath -Encoding utf8NoBOM
Write-Output "Wrote approved posture fields to $OutputPath."
