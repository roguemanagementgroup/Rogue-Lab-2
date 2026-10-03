# Windows Posture Collection Specification

## Safety boundary

This specification is for explicitly authorized Windows endpoints only. It describes a read-only, local posture summary and excludes device names, usernames, serial numbers, IP addresses, event logs, credentials, installed-software inventories, running-process data, persistence review, network discovery, remediation, and configuration changes.

The optional script in `scripts/Collect-SafeWindowsPosture.ps1` must not run without written authorization. It requires an explicit attestation switch, writes only to an operator-supplied approved destination, and does not change endpoint configuration.

## Approved data elements

| Category | Fields | Source | Behavior when unavailable |
|---|---|---|---|
| OS posture | Product family, version, build | Windows registry product metadata | Record `unavailable`; do not add a substitute query. |
| Defender posture | Antivirus, real-time protection, and service state | `Get-MpComputerStatus` | Record `unavailable`; do not install features or change Defender settings. |
| BitLocker posture | OS-volume protection state and protected-volume count | `Get-BitLockerVolume` | Record `unavailable`; do not unlock, encrypt, decrypt, or query recovery material. |
| Firewall posture | Enabled state for Domain, Private, and Public profiles | `Get-NetFirewallProfile` | Record `unavailable`; do not modify rules or profiles. |
| Update posture | Latest installed-update date | `Get-CimInstance Win32_QuickFixEngineering` | Record `unavailable`; do not initiate scanning or installation. |

## Normalized output rules

- The synthetic fixture is defined by `schemas/windows-posture.schema.json`. Live output mirrors the posture sections but intentionally omits the fixture-only fields and every endpoint identifier.
- Use an approved opaque asset reference only outside this repository. The included fixture uses a clearly synthetic reference.
- Boolean-like states use `enabled`, `disabled`, or `unavailable`.
- Absence of data is not a pass, failure, compromise indicator, or attribution signal.
- The update field reports only the newest available installation date; it does not determine whether an endpoint is fully patched.

The repository validator accepts only the synthetic fixture format. It must not be used to import, normalize, or retain live endpoint output.

## Repeatability checks

Run these commands against repository content only. They validate the synthetic fixture and do not access an endpoint:

```powershell
python scripts\validate_posture_fixture.py fixtures\windows-posture.synthetic.json
python -m unittest discover -s tests -v
```

## Operator procedure

1. Complete the [authorization gate and preflight checklist](initial-engagement-assessment-plan.md).
2. Review the script with the engagement owner and set an approved output path outside the repository.
3. Run the script locally with `-IHaveWrittenAuthorization` and the approved output path.
4. Confirm the output contains only the approved normalized fields before transferring it through approved evidence handling.
5. If output is unavailable or out of scope, stop and escalate rather than expanding collection.

## Synthetic fixture

`fixtures/windows-posture.synthetic.json` is a fabricated example designed for documentation and test validation. It must not be replaced with a live endpoint artifact.
