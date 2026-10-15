# Day 16 — Durable state: three sessions, zero déjà vu

> One big task, three sessions, three Copilot surfaces (VS Code agent → Copilot CLI → cloud agent). The only thing they share is a markdown file. Can session 3 pick up **without repeating a step or undoing a decision**?

**Deliverable:** Progress file history (`plans/<issue>-progress.md`) showing no repeated steps

## Bets

- **Bet A** — How many steps/decisions from S1–S2 will S3 repeat or reverse, even with the progress file? **My guess: 1**
  - Result: _scored in Mission 7_
- **Bet B** — At roughly what % of the token limit does Copilot CLI auto-compress history? **My guess: 50%**
  - Result: _scored in Mission 4_

## Lessons (Mission 1 — Progress and decisions as artifacts)

Source: [Researching, planning, and iterating before opening a pull request](https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results#researching-planning-and-iterating-before-opening-a-pull-request)

- The cloud agent can **research the repo, create an implementation plan, and iterate on a branch** *before* any PR exists
- Why: understand the codebase first, agree on an approach before code is written, review the diff before opening a PR

Source: [Review session logs](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/manage-and-track-agents#review-session-logs)

- *"Session logs show Copilot's internal reasoning and the tools it used to understand your repository, make changes, and validate its work."*
- Copilot runs in its own ephemeral dev environment, so it can run tests and linters there

Source: [Trace commits to session logs](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/manage-and-track-agents#trace-commits-to-session-logs)

- Cloud agent commits are **authored by Copilot**, with the person who started the task as **co-author**
- Each commit message **links to the session logs**, so a reviewer can trace *why* a change was made

**Key idea: logs are evidence, not state.** A new session never reads yesterday's log. The durable state it *does* read is the repo, so the progress file lives in the repo.

| What | Where it lives | Read by the next session? |
|---|---|---|
| Progress (Done / Decided / Next) | `plans/<issue>-progress.md` in the repo | ✅ yes, if told to (`AGENTS.md`) |
| Reasoning + tool calls | Session logs | ❌ no, humans read these for review/audit |
| Who changed what | Commits (Copilot author + you co-author, link to log) | Only the code, not the reasoning |

- ⚠️ Check-question slip: I first picked *"yesterday's session log"* as what a new session reads. Wrong: logs are for humans (review/audit); the next session reads **repo files**. Analogy: log = audit trail, progress file = case file.
- A decision that must survive (e.g. disposition enum `CLEARED / ESCALATED / SAR_FILED`) goes in **Decided**, committed to the branch

## Setup (Mission 2 — One big task, three slices)

- Issue [#81](https://github.com/mosherif-labs/github-labs/issues/81): **Disposition override**, a QA reviewer changes a closed alert's disposition, audited
  - Changed from the plan's "disposition model + endpoint" because `app/` already had `Disposition`, `POST /alerts/{id}/close` and `/history`
- Branch `feat/81-disposition`, draft PR [#82](https://github.com/mosherif-labs/github-labs/pull/82)
- Progress file: `plans/81-progress.md` (Done / Decided / Next)
- `AGENTS.md` rule: read the progress file before working on an issue; update Done / Decided / Next at the end
- Slices: **S1** model (VS Code agent) · **S2** `PATCH /alerts/{id}/disposition` + validation (Copilot CLI) · **S3** audit trail + tests (cloud agent via `@copilot` on PR #82)

## Session 1 — VS Code agent (Mission 3)

- Prompt: *"Work on S1 of `plans/81-progress.md` only."* (deliberately no "update the file": the `AGENTS.md` rule had to do that)
- Read `plans/81-progress.md` **first**, before touching code ✅
- Stayed in scope: only `app/models.py` + `tests/test_alerts.py` (no endpoint) ✅; tests green
- Added `DispositionChangeIn` (disposition, reviewer, reason), `AlertEventType.DISPOSITION_CHANGED`, optional `from_disposition` / `to_disposition` on `AlertHistoryEvent`
- File updated: Done = S1 · Decided = *from/to optional because `AlertHistoryEvent` serves many event types* · Next starts at S2
- 🔍 Gap to watch: issue wants the audit event to carry **reason**, but `AlertHistoryEvent` has no `reason` field yet. A later session must add it (not a reversal, but Done doesn't flag it)
- Done entry has no commit sha (the template asked for one): the agent can't know a sha before the commit exists

## Lessons (Mission 4 — How the CLI resumes)

Source: [Resume an interactive session](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/overview#resume-an-interactive-session)

- `--resume` (launch option) or `/resume` (slash command): **pick** a past interactive session and continue with its saved context
- `copilot --continue`: no picker, reopens the **most recently closed local** session
- The CLI can also pull a cloud agent session started on GitHub into your local environment

## Session 2 — Copilot CLI (Mission 5)

## Session 3 — Cloud agent (Mission 6)

## Audit (Mission 7)

## Reflection
