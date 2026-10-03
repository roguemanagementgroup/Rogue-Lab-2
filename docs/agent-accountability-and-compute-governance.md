# Agent Accountability and Compute Governance

## Purpose

This document describes how this project keeps AI-assisted work observable, bounded, and reviewable by a human who does not write code. It pairs naturally with the engagement gates elsewhere in the repository: the [authorization gate](initial-engagement-assessment-plan.md) controls what the agent may do, and the accountability reporter records what the agent actually spent doing it.

The reporter is [tools/agent_accountability.py](../tools/agent_accountability.py). It is ordinary, inspectable Python (standard library only), tested by [tests/test_agent_accountability.py](../tests/test_agent_accountability.py), and demonstrated on the synthetic fixture [fixtures/accountability-events.synthetic.json](../fixtures/accountability-events.synthetic.json).

## What it measures

The reporter consumes recorded usage events - the same telemetry the Copilot runtime already writes locally - and reports, per model and per work phase:

- API request count
- Fresh input tokens vs. cache-reused input tokens (the main conservation lever)
- Output and reasoning tokens
- Billing-weighted usage in relative AIU units
- Model execution time
- Anomaly flags for any single request that exceeds declared cost or duration thresholds
- Optional budget enforcement: the tool exits nonzero if a declared budget is exceeded, so it can gate automation

## What it does not do, stated plainly

- It is **not** secret or invisible. Transparency is the point: the code, its inputs, and its outputs are reviewable by anyone with access to the workspace.
- It **cannot** report a percentage of a subscription quota, because quota data lives in the account provider's systems, not in session telemetry. It reports absolute measured usage instead.
- It **cannot** see other agents, other sessions' private data, or anything that was not recorded in its input file.
- AIU is a relative billing-weighted unit, **not a dollar amount**. Currency conversion requires the provider's pricing, which this tool does not have.
- It does not run silently in the background or monitor people. It generates a report on demand from a data file.

## Human-in-the-loop governance loop

The pattern this repository demonstrates, end to end:

1. **Preflight ("builder's permit"):** written authorization gates before any action, as in the [engagement runbook](initial-engagement-assessment-plan.md).
2. **Bounded execution:** narrowly scoped, read-only-by-default work, staged in reviewable per-phase commits.
3. **Measured spend:** recorded telemetry aggregated by the accountability reporter, with anomaly flags and optional budget gates.
4. **Plain-language transcript:** the report explains what happened in terms a non-technical owner can verify, and the git history provides the auditable "what changed, when, and why."

## Using the reporter

```powershell
python tools\agent_accountability.py fixtures\accountability-events.synthetic.json
python tools\agent_accountability.py usage.json --format html --output report.html --budget-aiu 200
```

Exit codes: `0` within budget, `1` budget exceeded, `2` invalid input. This makes the tool safe to place in front of automated work as a spending gate.

## Defensible portfolio language

Statements below are accurate for this repository and may be quoted in a portfolio context:

- "The project records and reports measured AI usage per phase, including cache-reuse ratios and anomaly flags, using a small standard-library tool with tests."
- "All agent work is gated by written-authorization preflight checks and staged in reviewable per-phase commits."
- "Reports distinguish measured data from derived figures and state their own limits."

Claims of uniqueness, superiority, or market position are intentionally absent: they cannot be evidenced from inside this repository, and the project's own conventions prohibit unsupported claims.
