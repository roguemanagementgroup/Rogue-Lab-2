# Change-Control and Rollback Record Template

> Complete one record per proposed change. Store completed records in the engagement's approved system, never in this repository. Use opaque asset references only.

## 1. Change identification

| Field | Entry |
|---|---|
| Change record ID | |
| Date drafted | |
| Author role | |
| Engagement / authorization reference | |
| Asset reference (opaque) | |
| Related posture observation | |
| Priority band (P1 / P2 / P3) | |

## 2. Proposed change

| Field | Entry |
|---|---|
| Current observed state (as documented in the approved posture summary) | |
| Proposed end state | |
| Method category (for example: standard OS security setting via client-approved management path) | |
| Expected duration and window | |
| Blast radius (what could be affected if it goes wrong) | |
| Dependencies | |

## 3. Risk and approval

| Field | Entry |
|---|---|
| Risk of making the change | |
| Risk of not making the change | |
| Business approver (role) | |
| Technical approver (role) | |
| Approval date(s) | |
| Scheduled window | |

## 4. Rollback plan

| Field | Entry |
|---|---|
| Rollback trigger criteria (objective conditions that stop or reverse the change) | |
| Documented prior state to restore | |
| Rollback owner (role) | |
| Maximum time to complete rollback | |
| Data or evidence to preserve before rollback | |
| Post-rollback verification step | |

## 5. Execution record (filled in only by the client-authorized operator)

| Field | Entry |
|---|---|
| Executed by (role) and date/time with timezone | |
| Deviation from plan (if any) | |
| Outcome | Completed / Rolled back / Stopped and escalated |
| Verification result reference | |

## Rules of use

- This template authorizes nothing by itself. Execution requires the engagement's written authorization plus the approvals recorded above.
- If reality deviates from the plan, stop and record the deviation; do not improvise.
- A rolled-back change is a normal outcome, not a failure. Record it factually.
