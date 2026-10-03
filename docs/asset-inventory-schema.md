# Asset Inventory Schema

## Purpose

This schema defines the minimum asset register needed to plan an authorized endpoint posture review. It deliberately avoids personal data and endpoint identifiers. Keep the real register in an approved client system; this repository may contain only synthetic examples.

## Record schema

| Field | Type | Requirement | Handling rule |
|---|---|---|---|
| `asset_reference` | String | Required | Use an approved opaque reference. Do not use a hostname, username, IP address, serial number, or hardware identifier. |
| `asset_group` | Enum | Required | One of `workstation`, `laptop`, `shared-kiosk`, or `other-approved`. |
| `operating_system_family` | Enum | Required | `Windows` for the Phase 2 collection design. |
| `assessment_scope` | Enum | Required | `approved`, `deferred`, or `excluded`. |
| `authorization_reference` | String | Required outside this repository | Store only in the approved engagement system; omit from synthetic fixtures. |
| `data_handling_class` | Enum | Required | `internal-assessment` or stricter, as determined by the engagement. |
| `approved_collection_window` | String | Required outside this repository | Store in the approved engagement system; do not commit dates or schedules. |
| `collection_status` | Enum | Required | `not-started`, `collected`, `unavailable`, or `stopped-and-escalated`. |
| `notes` | String | Optional | Do not include personal data, endpoint identifiers, raw findings, or client details. |

## Validation rules

- An asset cannot be collected unless `assessment_scope` is `approved`.
- `authorization_reference` and `approved_collection_window` must exist in the approved engagement system before collection, but are intentionally excluded from this repository and fixture format.
- `collection_status` must be `stopped-and-escalated` when a stop condition occurs; do not add sensitive details to `notes`.
- Use the opaque `asset_reference` to correlate an approved artifact with the approved register outside this repository.

## Synthetic example

```json
{
  "asset_reference": "SYNTH-ASSET-001",
  "asset_group": "workstation",
  "operating_system_family": "Windows",
  "assessment_scope": "approved",
  "data_handling_class": "internal-assessment",
  "collection_status": "not-started"
}
```
