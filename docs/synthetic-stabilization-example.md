# Synthetic Stabilization Example

> Every value on this page is fabricated for demonstration. `SYNTH-ASSET-002` does not exist. This example shows the shape of the documentation, not a real client engagement.

## Scenario

A synthetic posture summary for `SYNTH-ASSET-002` shows:

- OS: Windows 10.0 (build 22631)
- Defender: antivirus enabled, real-time protection enabled, service enabled
- BitLocker: system volume protection enabled, 1 protected volume
- Firewall: domain enabled, private enabled, **public disabled**
- Updates: latest install date recorded; currentness not determined

## Assessment of the observation

The public firewall profile being disabled raises the exposure of the endpoint on untrusted networks. This is a posture observation, not an incident finding: the data says nothing about why the profile is disabled or whether any abuse occurred.

## Prioritization

| Axis | Rating | Rationale |
|---|---|---|
| Exposure | High | Public profile applies on untrusted networks such as hotspots. |
| Consequence | High | Unfiltered inbound traffic on an untrusted network increases attack surface. |
| Reversibility | Trivial | Re-enabling or re-disabling a firewall profile is a standard, fast, reversible configuration state. |

Result: **P1** - plan first, with full change control.

## Proposed change record (synthetic)

| Field | Entry |
|---|---|
| Change record ID | SYNTH-CC-001 |
| Asset reference | SYNTH-ASSET-002 |
| Current observed state | Public firewall profile disabled |
| Proposed end state | Public firewall profile enabled using the client's approved management path |
| Blast radius | Legitimate inbound services on public networks could be blocked; most client endpoints have none |
| Priority | P1 |

## Rollback plan (synthetic)

- Trigger: an approved business application loses required connectivity during the change window.
- Restore: return the public firewall profile to its documented prior state (disabled) via the same approved management path.
- Maximum rollback time: 15 minutes.
- Post-rollback verification: re-run the approved read-only posture collection and confirm the documented prior state.

## Verification plan (synthetic)

| # | Criterion | Method | Expected result |
|---|---|---|---|
| 1 | Public firewall profile state | Approved read-only posture collection | `enabled` |
| 2 | Domain and private profiles unchanged | Same collection | Both still `enabled` |

## Decision log entry (synthetic)

| Date | Decision | By (role) |
|---|---|---|
| (synthetic) | Approved SYNTH-CC-001 for the next maintenance window | Business approver, technical approver |

## What this example deliberately does not show

No hostnames, usernames, IP addresses, serial numbers, or raw logs appear above, and none would appear in a real record stored in this repository. A real engagement keeps its completed records in the client's approved system.
