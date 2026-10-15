# AGENTS.md

Guidance for AI coding agents working in this repository.

## Setup

```bash
uv sync --locked
```

## Test

```bash
uv run pytest -v
```

This is the same command CI runs. The suite must pass before you open or update a pull request.

## Run

```bash
uv run uvicorn app.main:app --reload
```

## Rules

- Never touch `infra/`. It is human-only.
- Synthetic data only.
- Risk scores are floats from 0.0 to 1.0.
- Return HTTP 422 for validation errors.
- Before working on an issue, read `plans/<issue>-progress.md` if it exists. At the end, update its Done / Decided / Next. Never redo Done or reverse Decided without a new Decided entry.
- Read `docs/decisions/` before changing behaviour; never contradict an Accepted ADR without a new ADR.
- See `.github/copilot-instructions.md` for coding standards and `.github/instructions/` for path-specific rules.
