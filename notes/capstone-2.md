# Day 13 — Capstone 2: fail safely, then roll back

> Make the agent fail **on purpose**: a blocked edit under `infra/`, three retries that run out, a bad PR that gets merged. The win is not a green run. It's a failed run that ends with the right human notified and a clean rollback, every step linked.

**Deliverable:** this file: a failed run that ends with the right human notified and a clean rollback, with links · Learn module 3 finished

## Bets

- **Bet A**: Your `preToolUse` hook script **crashes** (non-zero exit, no JSON). Does the tool call go ahead? (Yes, fail-open · No, fail-closed · The agent asks the user) **My guess: No, fail-closed**
  - Result: **Win**: command `preToolUse` hooks are fail-closed: a crash or non-zero exit (including exit `2`) **denies** the call. Two catches: command-hook **timeouts are always fail-open** (even admin policy hooks), and **HTTP** `preToolUse` hooks are fail-open. ([Hooks reference: preToolUse](https://docs.github.com/en/copilot/reference/hooks-reference#pretooluse--pretooluse))
- **Bet B**: In a **cloud agent** session, your `postToolUse` hook appends to `logs/tool-calls.jsonl`. Where is that file after the session? (Committed in the PR · An Actions artifact · In the session log · Gone) **My guess: An Actions artifact**
  - Result: _pending (Mission 2)_

## Mission 1: hooks, the only gate that says no mid-session

- Hook files live in `.github/hooks/NAME.json` with `"version": 1` and a `hooks` object; they must be on the **default branch** to run in cloud agent sessions ([how-to](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/use-hooks#creating-a-hook-in-a-repository-on-github))
- `preToolUse` can return `permissionDecision`: `allow` / `deny` / `ask` + `permissionDecisionReason`. An explicit decision short-circuits normal permission checks; **no output** = normal flow ([decision control](https://docs.github.com/en/copilot/reference/hooks-reference#pretooluse-decision-control))
- Failure modes: crash / non-zero exit → **deny** · timeout → fail-open: **normal permission flow**, the guard gets no say · HTTP hook error → fail-open
![Hook failures: only gates can say no](img/d13-hook-failures.svg)
*Editable source: [d13-hook-failures.excalidraw](img/d13-hook-failures.excalidraw)*

- Exit codes ([reference](https://docs.github.com/en/copilot/reference/hooks-reference#exit-codes-for-command-hooks)), checked live 2026-10-12, newer than the plan:
  - `0`: success; stdout parsed as the hook's JSON output
  - `2`: a **warning** by default (stderr shown, run continues), **but** for `preToolUse` / `permissionRequest` it's a **deny even if stdout says `allow`**; for `postToolUseFailure`, stdout is appended to the failure the agent sees (recovery guidance)
  - other non-zero: logged, run continues (fail-open), **except `preToolUse`: deny**
  - timeout: killed after `timeoutSec`, execution continues (fail-open for every event)
- Tool names ([table](https://docs.github.com/en/copilot/reference/hooks-reference#tool-names-for-hook-matching)): `ask_user`, `bash`, `create`, `edit`, `glob`, `grep`, `powershell` (not in cloud agent), `task`, `view`, `web_fetch`. Writes under `infra/` can come from **`create|edit|bash`**
- `matcher` is a filter **in front of** the script: an unmatched tool never reaches the guard
- Multiple hooks of the same type run in order; for `preToolUse` **any `deny` wins**
- **Don't print `allow`** when you have no opinion: it short-circuits the CLI's normal permission checks. Print nothing, exit 0
