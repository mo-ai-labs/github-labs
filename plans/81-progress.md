# #81 progress — Disposition override (QA reviewer, audited)

Issue: https://github.com/mosherif-labs/github-labs/issues/81

## Done
- S1: added `DispositionChangeIn`, `DISPOSITION_CHANGED`, and optional from/to disposition fields to alert history events; added focused model tests (2026-10-15)

## Decided
- History event from/to values are optional because `AlertHistoryEvent` represents multiple event types; the disposition-change event uses `from_disposition` and `to_disposition` (2026-10-15)

## Next
- S2: endpoint + validation: PATCH /alerts/{id}/disposition
- S3: audit trail + tests
