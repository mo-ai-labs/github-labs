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

## Session 1 — VS Code agent (Mission 3)

## Lessons (Mission 4 — How the CLI resumes)

## Session 2 — Copilot CLI (Mission 5)

## Session 3 — Cloud agent (Mission 6)

## Audit (Mission 7)

## Reflection
