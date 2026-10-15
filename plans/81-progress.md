# #81 progress — Disposition override (QA reviewer, audited)

Issue: https://github.com/mosherif-labs/github-labs/issues/81

## Done
- S1: added `DispositionChangeIn`, `DISPOSITION_CHANGED`, and optional from/to disposition fields to alert history events; added focused model tests (2026-10-15)
- S2: added `PATCH /alerts/{id}/disposition` (404 unknown, 409 if alert not closed or disposition unchanged, 422 via `DispositionChangeIn`) with endpoint tests; no history event yet; `/context` midway: under 25% of the token limit (2026-10-15)
- S3: append `DISPOSITION_CHANGED` history events with reviewer and from/to dispositions on successful updates; added endpoint audit-trail test (2026-10-15)

## Decided
- History event from/to values are optional because `AlertHistoryEvent` represents multiple event types; the disposition-change event uses `from_disposition` and `to_disposition` (2026-10-15)
- S3 uses the existing `actor` field for the reviewer; no additional history fields are needed (2026-10-15)

## Next
- None; S1–S3 are complete.

## Audit
- Repeats: 0. Reversals: 0 (S3 `7a01a20` kept S1's model, S2's endpoint and the unrecorded 409 for a no-op change).
- Drift: the issue's `reason` never reached the history event; S2's Next line dropped it and S3 locked it in ("no additional history fields are needed").
- Format fix: add an **Acceptance** section copied from the issue; every session ticks items there and never edits them.
