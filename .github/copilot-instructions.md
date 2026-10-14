# Copilot instructions: github-labs

A toy transaction-screening service: FastAPI, in-memory storage (`app/store.py`), Python 3.12+, managed with `uv`.

## Build and test

- Install: `uv sync --locked`
- Test: `uv run pytest -v` (the same command CI runs in `.github/workflows/ci.yml`, job `test`)
- Run locally: `uv run uvicorn app.main:app --reload`
- Run the full test suite before finishing any change, and only finish when it passes.

## Coding standards

- Put routes in `app/routers/`, request/response models in `app/models.py`, screening logic in `app/screening.py`.
- Validate input with Pydantic `Field` constraints on the models in `app/models.py` (as `TransactionIn` does), not with hand-written checks in the route.
- Get the store through the `StoreDep` dependency, and hold `store.lock` while reading or writing it.
- Use type hints on all functions. Keep changes small and focused on the issue.
- Every behaviour change comes with tests in `tests/`.
- Add a dependency only if the issue asks for it, and update `uv.lock` with `uv` (never by hand).

## Boundaries

- **Never create, modify or delete anything in `infra/`.** It is human-only.
- Don't change `.github/workflows/` unless the issue explicitly asks for it.
- Don't change `RULES` scores, `RISK_SCORE_REVIEW_THRESHOLD`, `NAME_MATCH_THRESHOLD` or `LARGE_AMOUNT` in `app/screening.py` unless the issue explicitly asks for it. Those are compliance decisions.
- **Synthetic data only.** Never add real names, account numbers or customer data.
