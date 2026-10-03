# Evidence Handling and Chain-of-Custody Template

> Use this template only for authorized assessment artifacts. Do not paste sensitive content into this repository. Record references to approved storage locations rather than raw data.

## Authorization and scope

| Field | Record |
|---|---|
| Engagement or change reference | |
| Written authorization reference | |
| Approved purpose | |
| In-scope systems or asset group | |
| Approved data classes | |
| Excluded data classes | Credentials, personal data, raw endpoint logs, forensic images, and any unapproved data |
| Retention period and disposal authority | |

## Artifact record

| Field | Record |
|---|---|
| Artifact ID | |
| Sanitized description | |
| Collection method and version | |
| Collection start and end time (with timezone) | |
| Collector role or identifier | |
| Source asset reference | Use an approved pseudonym or internal reference; do not use a hostname, username, serial, or IP here |
| Approved storage location reference | |
| Integrity value and algorithm, if applicable | |
| Sensitivity classification | |
| Known limitations or transformation | |

## Custody transfer log

| Date and time (with timezone) | From role | To role | Purpose | Approved location or transfer method | Integrity check result | Acknowledgment |
|---|---|---|---|---|---|---|
| | | | | | | |

## Review and disposition

| Field | Record |
|---|---|
| Reviewer role | |
| Review date | |
| Access restrictions confirmed | |
| Retention end date | |
| Disposition action | |
| Disposition date and approver | |
| Exceptions or escalation reference | |

## Handling notes

Keep the original approved artifact separate from any sanitized derivative. Any transformation must be reproducible and documented. If an artifact contains data beyond the approved scope, stop handling it, restrict access, and escalate through the engagement's approved process.
