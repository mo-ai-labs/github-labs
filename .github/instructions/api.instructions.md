---
applyTo: "app/routers/**,app/models.py"
---
Validation errors return HTTP 422 (FastAPI's default for request-model validation). Put field rules in the Pydantic models in `app/models.py`; don't add custom 400 handlers.
Risk scores are integers: see `risk_score` in `app/models.py` and the rule scores in `app/rules.py`. Don't restate ranges here.
