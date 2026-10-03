# Stabilization Verification Plan Template

> Verification proves a specific change reached its intended state. It does not prove the endpoint is secure, uncompromised, or compliant. Complete one plan per change-control record.

## Change under verification

| Field | Entry |
|---|---|
| Change record ID | |
| Asset reference (opaque) | |
| Proposed end state (copied from the change record) | |

## Success criteria

| # | Criterion | Measurement method | Expected result |
|---|---|---|---|
| 1 | | | |
| 2 | | | |

Criteria must be objective and checkable with an approved read-only method, such as re-running the approved posture collection described in the [collection specification](windows-posture-collection-specification.md).

## Verification procedure

1. Confirm the change record shows execution completed.
2. Wait the agreed settling period, if any.
3. Re-run the approved read-only collection for the changed area only.
4. Compare each success criterion against the new observation.
5. Record pass/fail per criterion with timestamp and operator role.

## Failure handling

| Scenario | Action |
|---|---|
| Any criterion fails | Do not retry the change ad hoc. Escalate to the technical approver and consider the documented rollback plan. |
| Collection unavailable | Record `unavailable`; schedule a retry within the approved window. |
| New out-of-scope observation | Stop. Route through the engagement's escalation path; do not expand scope silently. |

## Evidence and closeout

| Field | Entry |
|---|---|
| Verification artifact reference (approved storage) | |
| Verifier role and date | |
| Approver sign-off | |
| Residual risk accepted (if any) | |
| Retention and disposal note | |
