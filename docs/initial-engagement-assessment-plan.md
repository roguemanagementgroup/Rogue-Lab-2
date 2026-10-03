# Initial Engagement Assessment Plan and Runbook

## Purpose and intended use

This runbook supports a narrowly scoped first-visit endpoint posture assessment. It is a planning artifact for an authorized engagement, not an instruction to access a system without permission. It uses synthetic examples only and does not establish that a client has been compromised or that any actor is responsible for a condition.

## Assessment objective

Produce a bounded, point-in-time summary of approved Windows endpoint posture metadata so stakeholders can decide whether to schedule controlled stabilization work. The approved observation set is limited to operating-system version/build, Microsoft Defender feature state, BitLocker protection state, firewall profile state, and the latest installed-update date when available.

## Authorization gate

Do not begin until the engagement owner has confirmed all of the following in writing:

| Check | Required confirmation |
|---|---|
| Authority | The requester is authorized to approve the listed systems and collection activity. |
| Purpose | The assessment objective and intended audience are documented. |
| Scope | Approved asset references, maintenance window, and locations are identified without placing client identifiers in this repository. |
| Method | The Windows posture specification and output destination are approved. |
| Data handling | Approved storage, access roles, retention, and disposal are recorded. |
| Change boundary | Read-only collection is authorized; no remediation or configuration change is included. |
| Escalation | A client contact and a stop/escalation path are available. |

The operator must use the script's `-IHaveWrittenAuthorization` switch only after this gate is complete. The switch is an operator attestation, not evidence of authorization.

## Preflight checklist

1. Confirm the approved asset reference is an internal, non-public reference and will not be written to the repository.
2. Confirm the operator has a client-approved local session and that running PowerShell is permitted.
3. Review the exact output fields against the approved data classes.
4. Set an approved, access-controlled destination for the JSON output; do not use this repository as an evidence store.
5. Confirm that Defender, BitLocker, firewall, or update-query cmdlets unavailable on the endpoint will be represented as `unavailable`, not worked around.
6. Confirm a stop condition: unexpected sensitive output, material performance concern, scope disagreement, or loss of authorization.

## Execution flow

1. Reconfirm scope and consent with the engagement owner.
2. Run the approved collection script once per approved endpoint, using an approved output location.
3. Validate field shape and required values before analysis. The repository validator is for synthetic fixtures; apply an approved validation process to live artifacts outside the repository.
4. Transfer only approved artifacts through the documented evidence-handling process.
5. Summarize observations with limits, unavailable fields, and data-quality notes.
6. Propose any stabilization change separately through change control. Do not use this assessment step to remediate systems.

## Stop and escalation conditions

Stop immediately and notify the engagement owner if collection returns credentials, personal data, host/device identifiers, serial numbers, IP addresses, event logs, unexpected inventory detail, or anything outside the authorization. Do not modify the script to obtain unavailable information. Restrict access to the output and follow the approved handling process.

## Deliverable boundaries

The deliverable is a posture summary, not an incident determination. It may identify a configuration state that warrants review, but it cannot prove exploitation, persistence, compromise, attribution, or absence of risk.
