# github-labs

A toy transaction-screening service (FastAPI, in-memory storage). It's the proving ground for the GH-600 study plan: an AI agent will push code here, so the service stays small on purpose.

> **Synthetic data only.** Every name, country code, amount and rule in this repo is invented. Nothing comes from a real bank, customer or rulebook.

## Run it

```powershell
uv sync
uv run uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000/docs.

## Test it

```powershell
uv run pytest
```

CI (`.github/workflows/ci.yml`, job `test`) runs the same suite on every pull request and on pushes to `main`.

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Liveness check |
| POST | `/transactions/screen` | Screen a transaction; raises an alert when the score is 50 or more |
| GET | `/transactions/{id}` | Get a screening result |
| GET | `/alerts` | List alerts (filters: `alert_status`, `assignee`) |
| GET | `/alerts/{id}` | Get an alert |
| POST | `/alerts/{id}/assign` | Assign an open alert to an analyst |
| POST | `/alerts/{id}/notes` | Add a note to an alert |
| POST | `/alerts/{id}/close` | Close an alert with a disposition |
| PATCH | `/alerts/{id}/disposition` | Change the disposition of a closed alert |
| GET | `/watchlist` | List watchlist entries |
| POST | `/watchlist` | Add a watchlist entry |
| DELETE | `/watchlist/{id}` | Remove a watchlist entry |
| GET | `/rules` | List the screening rules and their scores |

## Screening rules (all synthetic)

| Rule | Score |
|---|---|
| `WATCHLIST_NAME`: party name fuzzy-matches a watchlist entry (≥ 0.85) | 70 |
| `HIGH_RISK_COUNTRY`: party country is `XQ`, `XR` or `ZZ` (ISO user-assigned codes) | 40 |
| `LARGE_AMOUNT`: amount ≥ 7,500 | 20 |
| `ROUND_AMOUNT`: amount is an exact multiple of 1,000 | 10 |

A total score of 50 or more (capped at 100) means the decision is `review` and an alert opens.

## Layout

- `app/`: the service
- `tests/`: unit tests (pytest + FastAPI `TestClient`)
- `.github/workflows/`: CI
- `infra/`: reserved for humans; agents must not touch it

<!-- d17 drift test -->
