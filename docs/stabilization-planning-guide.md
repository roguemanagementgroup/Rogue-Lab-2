# Stabilization Planning Guide

## Purpose

This guide turns an approved endpoint posture summary into a prioritized, reversible stabilization plan. It is a planning artifact only: nothing in this phase executes changes on any endpoint. Every proposed change requires its own change-control record, rollback plan, and verification plan before anyone touches a system.

## Boundaries

- Planning uses approved or synthetic posture summaries; this repository never holds live endpoint data.
- A posture observation is not proof of compromise, negligence, or misconfiguration intent. It is a state that warrants review.
- No persistence review, credential handling, network discovery, or remediation commands are produced here.
- Recommendations describe standard, documented Windows security configuration states (for example, an enabled firewall profile). They are not novel techniques and must be reviewed against the client's own policies.

## Inputs

1. An approved posture summary conforming to the [collection specification](windows-posture-collection-specification.md) (or the synthetic fixture for demonstrations).
2. The completed [authorization gate](initial-engagement-assessment-plan.md) and asset register entry.
3. Client constraints: maintenance windows, business criticality, existing baselines, and named approvers.

## Prioritization model

Each candidate change is scored on three qualitative axes. The model is deliberately simple so a non-technical stakeholder can follow it.

| Axis | Question | Scale |
|---|---|---|
| Exposure | How reachable is the affected surface if left as-is? | High / Medium / Low |
| Consequence | What is the plausible harm if the weakness is abused? | High / Medium / Low |
| Reversibility | How quickly and safely can the change be undone? | Trivial / Moderate / Difficult |

### Priority bands

| Band | Meaning | Rule |
|---|---|---|
| P1 | High exposure or high consequence, trivially reversible | Plan first; still requires full change control. |
| P2 | Meaningful risk reduction with moderate effort or coordination | Schedule in a normal maintenance window. |
| P3 | Hygiene improvement, low urgency | Bundle or defer; record the decision either way. |

A change that is difficult to reverse is never P1, regardless of risk, because an irreversible first action violates the stabilization principle of this lab.

## Decision rules

1. One proposed change per change-control record. Bundled changes defeat rollback.
2. Record the current observed state before proposing anything; that record is the rollback target.
3. Prefer the smallest change that addresses the observation.
4. If a fix requires software installation, policy redesign, or vendor engagement, it leaves this lab's scope and is handed to the client's normal IT process.
5. When evidence is unavailable or ambiguous, the plan says so; it does not guess.

## Outputs

For each approved change:

- A completed [change-control and rollback record](change-control-and-rollback-template.md).
- A completed [verification plan](stabilization-verification-plan-template.md).
- An updated decision log entry in the engagement's approved system (not this repository).

See the [synthetic worked example](synthetic-stabilization-example.md) for a complete demonstration using fabricated data.
