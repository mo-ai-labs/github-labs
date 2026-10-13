# Day 13 — Capstone 2: fail safely, then roll back

> Make the agent fail **on purpose**: a blocked edit under `infra/`, three retries that run out, a bad PR that gets merged. The win is not a green run. It's a failed run that ends with the right human notified and a clean rollback, every step linked.

**Status (2026-10-13):** Missions 0–1 done live with Claude. Missions 2–12 closed as a **review note**: the reading content is checked against the live docs on 2026-10-13, and the labs (Missions 3–9) are written up as worked reference (code, expected outcome, traps) **without being run**. To do them for real later, the code below is ready to paste.

![Capstone 2 safe execution paths](img/d13-safe-paths.svg)
*Editable source: [d13-safe-paths.excalidraw](img/d13-safe-paths.excalidraw)*

## TL;DR: the 8 things to walk into the exam with

1. **Only gate hooks can say no.** `preToolUse` (and `permissionRequest`, CLI only) block on a crash, non-zero exit or exit `2`. Every other event fails open: logged, run continues.
2. **Timeouts are always fail-open**, even for `preToolUse` and admin policy hooks: the call goes through the normal permission flow. Default `timeoutSec` = **30 s**. Keep guards local and fast.
3. **Exit code beats stdout** on gates: `{"permissionDecision":"allow"}` + exit `2` = **deny**.
4. **Never print `allow`** when the guard has no opinion: it short-circuits the normal permission checks. Print nothing, exit 0.
5. **The `matcher` filters before the script runs.** A tool not in it never reaches the guard. Writes come from `create|edit|bash`, and `bash` is leaky (`cd infra && rm main.tf`), so back hooks with CODEOWNERS / rulesets.
6. **Cloud agent hooks:** only `.github/hooks/*.json` from the default branch · Linux, `bash` field only · `/workspace` · **ephemeral filesystem** (hook files vanish) · `ask` = **deny** · `permissionRequest` has no effect · `notification` doesn't fire.
7. **Four safe-execution patterns** (Learn unit 5): **retries** for transient failures · **rollback** = branch isolation + PR review, then **revert** after merge · **escalation** = required review, auto-assigned reviewers, notify from workflow steps · **traceability** = workflow logs + commit history + PR discussions.
8. **Revert a merged PR** with the **Revert** button (write access needed). It opens a **new PR**; if it conflicts, or the PR wasn't merged on GitHub, use `git revert` on the commits.

## Bets

- **Bet A**: Your `preToolUse` hook script **crashes** (non-zero exit, no JSON). Does the tool call go ahead? **My guess: No, fail-closed**
  - Result: **Win**. Command `preToolUse` hooks are fail-closed: a crash or non-zero exit (including exit `2`) **denies** the call. Catches: command-hook **timeouts are always fail-open**, and **HTTP** `preToolUse` hooks are fail-open. ([Hooks reference: preToolUse](https://docs.github.com/en/copilot/reference/hooks-reference#pretooluse--pretooluse))
- **Bet B**: In a **cloud agent** session, your `postToolUse` hook appends to `logs/tool-calls.jsonl`. Where is that file after the session? **My guess: An Actions artifact**
  - Result: **Miss**: **gone**. The cloud agent filesystem is **ephemeral**: files hooks write are discarded when the job ends. Nothing uploads them for you. To keep hook output from a cloud session, send it out through an **`http` hook**; for a file you can download, run the logger in **your own workflow** (Copilot CLI + `actions/upload-artifact`), which is what Mission 6 does. ([Cloud agent execution environment](https://docs.github.com/en/copilot/reference/hooks-reference#cloud-agent-execution-environment))

---

## Mission 1: hooks, the only gate that says no mid-session ✅ (done live)

**Anatomy** ([how-to](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/use-hooks#creating-a-hook-in-a-repository-on-github))
- File: `.github/hooks/NAME.json` with `"version": 1` and a `hooks` object. Must be merged to the **default branch** to run in cloud agent sessions.
- How-to template events: `sessionStart`, `sessionEnd`, `userPromptSubmitted`, `preToolUse`, `postToolUse`, `errorOccurred`. The reference adds `postToolUseFailure`, `permissionRequest`, `agentStop`, `subagentStart` / `subagentStop`, `preCompact`, `notification`.
- Command hook keys: `type: "command"`, `bash`, `powershell`, `cwd`, `timeoutSec`, `env`.

**Decision control** ([reference](https://docs.github.com/en/copilot/reference/hooks-reference#pretooluse-decision-control))
- `preToolUse` prints `permissionDecision`: `allow` / `deny` / `ask` + `permissionDecisionReason`.
- An explicit `allow` / `deny` short-circuits the normal permission flow; **no output = normal flow**.
- Several hooks on the same event run **in order**; for `preToolUse` **any `deny` wins**.

**Failure modes**

![Hook failures: only gates can say no](img/d13-hook-failures.svg)
*Editable source: [d13-hook-failures.excalidraw](img/d13-hook-failures.excalidraw)*

| Hook result | **Gate** (`preToolUse`, `permissionRequest`) | **Observer** (everything else) |
|---|---|---|
| exit `0` | stdout JSON decides (no output = normal flow) | output used |
| exit `2` | **DENY**, even if stdout says `allow` | warning, run continues (`postToolUseFailure`: stdout appended as a recovery hint) |
| other non-zero / crash | **DENY** (fail-closed) | logged, run continues |
| timeout | fail-open: **normal permission flow** | logged, run continues |

([Exit codes for command hooks](https://docs.github.com/en/copilot/reference/hooks-reference#exit-codes-for-command-hooks))

> One-line test: **is it `preToolUse` or `permissionRequest`?** No → it can't block anything. A broken `sessionStart` means the session runs *without* whatever it was meant to set up.

**Tool names for `matcher`** ([table](https://docs.github.com/en/copilot/reference/hooks-reference#tool-names-for-hook-matching)): `ask_user` (useless in cloud agent: no user), `bash`, `create`, `edit`, `glob`, `grep`, `powershell` (not in cloud agent), `task` (subagents), `view`, `web_fetch`.
- A guard against writes under `infra/` must cover **`create|edit|bash`**. `view` only reads.
- `"create|edit"` alone: a `bash` `sed -i … infra/x` **never reaches** the guard (not "runs and allows").

---

## Mission 2: where hooks run (and where their files go)

| | **Copilot CLI** | **Cloud agent** |
|---|---|---|
| Runs on | your machine (or your Actions runner) | GitHub's Linux sandbox |
| Loads hooks from | policy files + repo `.github/hooks/*.json` + `~/.copilot/hooks/` + inline settings + plugins (**all run**) | **only** `.github/hooks/*.json` from the cloned repo |
| Events | **all** | all except: `notification` doesn't fire · `permissionRequest` has no effect · `preCompact` only `trigger: "auto"` |
| Shell field | `bash` / `powershell` by OS | **`bash` only** (`powershell` ignored; `command` as fallback) |
| Working dir | where you run it | `/workspace` (or `/root` with no repo) |
| Files hooks write | stay on disk | **discarded when the job ends** |
| Network | yours | firewall: GitHub + Copilot hosts by default |
| Permissions | interactive | non-interactive, all tools **pre-granted**; `ask` → **deny** |

([Hooks locations](https://docs.github.com/en/copilot/reference/hooks-reference#hooks-locations) · [Cloud agent execution environment](https://docs.github.com/en/copilot/reference/hooks-reference#cloud-agent-execution-environment))

**Why the logger runs in your own workflow:** a cloud agent hook's log file dies with the job. So the logging hook runs where *you* control the job (Copilot CLI inside `agent-run.yml`), which uploads `logs/tool-calls.jsonl` with `actions/upload-artifact`. In cloud agent sessions the guard still applies; the record there is the **session log**.

**Troubleshooting checklist** ([how-to](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/use-hooks#troubleshooting)): file in `.github/hooks/` · valid JSON (`jq .`) · `"version": 1` · script `chmod +x` + shebang · default timeout **30 s** · output on **one line** (`jq -c`, or `ConvertTo-Json -Compress`) · debug with `set -x` and stderr, and pipe sample JSON into the script.

---

## Mission 3: Guard 1, nothing touches `infra/` (reference lab)

`infra/README.md` already exists (*"AI agents must not create, modify or delete anything in this folder"*), and CODEOWNERS already routes `/infra/` to `@sheriffMoose`.

`.github/hooks/guardrails.json`
```json
{
  "version": 1,
  "hooks": {
    "preToolUse": [
      { "type": "command", "bash": "./scripts/hooks/block-infra.sh", "cwd": ".", "timeoutSec": 10 }
    ],
    "postToolUse": [
      { "type": "command", "bash": "./scripts/hooks/log-tool.sh", "cwd": ".", "timeoutSec": 10 }
    ]
  }
}
```

`scripts/hooks/block-infra.sh`
```bash
#!/bin/bash
# preToolUse guardrail: deny any tool call whose arguments touch infra/
INPUT=$(cat)                                   # JSON on stdin
TOOL=$(echo "$INPUT" | jq -r '.toolName')
ARGS=$(echo "$INPUT" | jq -c '.toolArgs')      # string or object: -c gives one line either way

case "$TOOL" in
  create|edit|bash)
    if echo "$ARGS" | grep -Eq '(^|["/ ])infra/'; then
      echo '{"permissionDecision":"deny","permissionDecisionReason":"Changes under infra/ need a human (capstone-2 guardrail)"}'
      exit 0
    fi
    ;;
esac
# No output = no decision: the normal permission flow continues.
# Never print "allow" here: that would skip the normal permission checks.
exit 0
```

```bash
chmod +x scripts/hooks/block-infra.sh
git update-index --chmod=+x scripts/hooks/block-infra.sh     # Windows: record the exec bit in git

# Deny case → prints the deny JSON
echo '{"timestamp":1704614400000,"cwd":"/tmp","toolName":"edit","toolArgs":"{\"path\":\"infra/main.tf\"}"}' | ./scripts/hooks/block-infra.sh
# Allow case → prints nothing, exit 0
echo '{"timestamp":1704614400000,"cwd":"/tmp","toolName":"edit","toolArgs":"{\"path\":\"app/main.py\"}"}' | ./scripts/hooks/block-infra.sh; echo "exit: $?"
```

**Live-doc notes vs the plan:** the plan's `case` also listed `str_replace_editor|apply_patch|powershell`; the live tool table has none of those for the cloud agent, so `create|edit|bash` is the set. The reference types `toolArgs` as `unknown` (not promised to be a string), hence `jq -c` instead of `jq -r`.

**Known leaks (why the hook is one layer, not the control):** `cd infra && rm main.tf` has no `infra/` in its text · a script the agent writes elsewhere then runs · `task` subagents. The merge-time backstop is **CODEOWNERS + a ruleset requiring code-owner review** on `infra/`.

## Mission 4: Guard 2, log every tool call (reference lab)

`scripts/hooks/log-tool.sh`
```bash
#!/bin/bash
# postToolUse: append one JSON line per tool call
INPUT=$(cat)
mkdir -p logs
echo "$INPUT" | jq -c '{ts: .timestamp, tool: .toolName, args: .toolArgs}' >> logs/tool-calls.jsonl
exit 0
```
- `chmod +x` + `git update-index --chmod=+x`, add `logs/` to `.gitignore`.
- Ship it through a PR → green checks → `gh pr merge --admin`: **hooks only count once on `main`**.
- It's an observer: if it fails (disk full, `jq` missing) the run **continues**, so a missing log is silent. Check the artifact, don't assume it.

## Mission 5: safe execution paths, by the book

From [Learn module 3, unit 5: Agent execution limits and protections](https://learn.microsoft.com/en-us/training/modules/agent-tooling-mcp-execution-environments/5-agent-execution-limits-protections):

| Pattern | What the module says | Today's implementation |
|---|---|---|
| **Error handling** | fail fast, log meaningful errors, no partial changes (`continue-on-error: false`) | step `exit 1` after the last attempt; job fails |
| **[Retries](https://learn.microsoft.com/en-us/training/modules/agent-tooling-mcp-execution-environments/5-agent-execution-limits-protections#retries)** | for **transient** failures: rerun failed steps, retry logic in scripts, workflows safe to re-execute | 3 attempts, exponential backoff 30/60/120 s |
| **[Rollbacks](https://learn.microsoft.com/en-us/training/modules/agent-tooling-mcp-execution-environments/5-agent-execution-limits-protections#rollbacks)** | **built in** via branch isolation + PR review; close/discard the PR, or **revert** commits after merge | Revert PR (Mission 9) |
| **[Escalation](https://learn.microsoft.com/en-us/training/modules/agent-tooling-mcp-execution-environments/5-agent-execution-limits-protections#escalation-paths)** | require PR review · auto-assign reviewers · **notify maintainers from workflow steps** | `needs-human` issue mentioning `ESCALATION_OWNER` |
| **[Traceability](https://learn.microsoft.com/en-us/training/modules/agent-tooling-mcp-execution-environments/5-agent-execution-limits-protections#traceability-and-accountability)** | workflow logs + commit history + PR discussions: inspectable, attributable | run log + tool-call artifact + issue → run link + PR timeline |

Also on that page: the cloud agent can only touch **its own repo**, works on a **separate branch**, and **doesn't merge** on its own · **environment protections** (required approvals, secret scoping, deployment targets) gate deployments · `GITHUB_TOKEN`-triggered events **don't start new workflow runs** (loop protection); **PATs / GitHub App tokens can**, so design against recursive runs. Summary words: **resilient, controlled, auditable, human-governed**.

**Copilot CLI in CI** ([Running Copilot CLI programmatically](https://docs.github.com/en/copilot/how-tos/copilot-cli/automate-copilot-cli/run-cli-programmatically#cicd-integration)):
```yaml
- env:
    COPILOT_GITHUB_TOKEN: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
  run: copilot -p "…" -s --allow-tool='shell(npm:*), write' --no-ask-user
```
- `-p` prompt · `-s` silent (no session metadata) · `--allow-tool` least privilege (comma list in one flag) · `--no-ask-user` no clarifying questions · `--model` pin a model · `--share='./audit.md'` save the transcript (traceability!) · `--allow-all` only in a sandbox.
- Auth: `COPILOT_GITHUB_TOKEN` from a **PAT secret**, not `GITHUB_TOKEN` (Day 12: fine-grained PAT with **Copilot Requests**).

## Mission 6: timeout + retry with backoff (reference lab)

`.github/workflows/agent-run.yml`
```yaml
name: agent-run

on:
  workflow_dispatch:
    inputs:
      task:
        description: "Prompt for the agent"
        required: true
        default: "Add a unit test for GET /alerts/{id} returning 404 and run pytest"
      simulate_outage:
        type: boolean
        default: false

permissions:
  contents: read
  issues: write # escalation issue + label only

jobs:
  agent:
    runs-on: ubuntu-latest
    timeout-minutes: 30 # job-level ceiling
    steps:
      - uses: actions/checkout@v7
      - uses: astral-sh/setup-uv@v10.2.0
        with:
          python-version: "3.13"
          enable-cache: true
      - run: uv sync --locked
      - run: echo "$PWD/.venv/bin" >> "$GITHUB_PATH"
      - run: npm install -g @github/copilot

      - name: Run agent (timeout + retry with backoff)
        timeout-minutes: 20 # step-level ceiling
        shell: bash
        env:
          COPILOT_GITHUB_TOKEN: ${{ secrets.COPILOT_GITHUB_TOKEN }}
          TASK: ${{ inputs.task }}
          SIMULATE_OUTAGE: ${{ inputs.simulate_outage }}
        run: |
          for attempt in 1 2 3; do
            if [ "$SIMULATE_OUTAGE" = "true" ]; then
              echo "simulated outage"; rc=1
            else
              copilot -p "$TASK" -s --no-ask-user --allow-tool='write, shell(pytest:*)'; rc=$?
            fi
            [ "$rc" -eq 0 ] && exit 0
            [ "$attempt" -eq 3 ] && break          # don't sleep after the last attempt
            delay=$(( 15 * 2 ** attempt ))         # 30s, 60s
            echo "attempt $attempt failed (rc=$rc); retrying in ${delay}s"
            sleep "$delay"
          done
          exit 1

      - name: Upload tool-call log
        if: always()
        uses: actions/upload-artifact@v7
        with:
          name: tool-calls-${{ github.run_id }}
          path: logs/tool-calls.jsonl
          if-no-files-found: warn

      - name: Escalate to a human
        if: failure()
        shell: bash
        env:
          GH_TOKEN: ${{ github.token }}
          RUN_URL: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
          OWNER: ${{ vars.ESCALATION_OWNER }}
        run: |
          gh label create needs-human --color B60205 --force
          gh issue create \
            --title "Agent run ${{ github.run_id }} failed after 3 attempts" \
            --label needs-human \
            --body "@$OWNER the agent run failed after retries. Logs and tool-call artifact: $RUN_URL"
```

How to read it:
- **Two timeouts:** step 20 min inside job 30 min. A timeout fails the step, so `failure()` still escalates.
- **Backoff** doubles the wait. I fixed one thing vs the plan: it no longer sleeps 120 s after the final attempt.
- **`if: always()`** uploads the log on success *and* failure; **`if: failure()`** escalates only when an earlier step failed.
- **Least privilege:** `contents: read` + `issues: write`; the agent's own token is the PAT, scoped by `--allow-tool`.
- **Cost:** a real failing attempt is a billed `copilot -p` run, so three failures cost three. That's why the drill uses `simulate_outage`, which never calls Copilot.
- Prereqs: Actions secret `COPILOT_GITHUB_TOKEN` (Day 12 PAT) + repo variable `ESCALATION_OWNER` = `sheriffMoose`.

## Mission 7: fire drill, retries run out (expected outcome)

`gh workflow run agent-run.yml -f simulate_outage=true`
- Log shows `attempt 1 failed … retrying in 30s`, `attempt 2 … 60s`, then the step fails (~1.5 min).
- `Upload tool-call log` runs (warns: no file, since no agent ran) → `Escalate to a human` creates **"Agent run N failed after 3 attempts"** with label `needs-human` and `@sheriffMoose` + the run URL.
- **Notification:** an @mention in an issue body notifies the mentioned user (web/email per your notification settings), *unless the issue author is you*. `gh issue create` here runs as `github-actions[bot]`, so the mention does reach you.
- Time to human ≈ attempts + backoff (~90 s) + runner start.

## Mission 8: the guard in a cloud agent session (expected outcome)

Assign Copilot *"Update `infra/README.md` to describe the Terraform layout"*:
- The `edit` (or `create`) on `infra/README.md` is **denied**, and the session log shows the tool call with your reason text: *"Changes under infra/ need a human (capstone-2 guardrail)"*.
- Typical agent reaction: reports it can't change the file, or tries another route. If it tries `bash` with a path containing `infra/`, the guard denies that too; a `cd infra && …` would slip through (see leaks).
- Record lives in the **session log** (the hook's own files are gone with the job).

## Mission 9: merge something bad, then undo it (expected outcome)

1. Throwaway base: `git switch main; git pull; git switch -c capstone2-test; git push -u origin capstone2-test`
2. Assign Copilot, base branch `capstone2-test`: *"Lower the default screening match threshold to 0.1"* → merge it anyway.
3. [Revert](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/reverting-a-pull-request#reverting-a-pull-request): **Revert** button at the bottom of the merged PR (needs **write** access) → creates a **new PR** that reverts the merge commit → merge it → threshold back.
   - Conflicts, or PR not merged on GitHub → `git revert <sha>` the individual commits instead.
- **What a reviewer should catch:** a screening threshold of 0.1 is a **risk-control change**, not a code tweak: false-positive flood, no model-risk sign-off, no test asserting the threshold.
- **Earliest guard:** CODEOWNERS already lists `/app/screening.py` → with a ruleset requiring **code-owner review**, the PR can't merge without the owner. A hook could deny edits to `app/screening.py` even earlier (during the session), and a required check asserting the threshold catches it in CI.

## Mission 10: Learn module 3

[Tooling, MCP, and Agent Execution Environments](https://learn.microsoft.com/en-us/training/modules/agent-tooling-mcp-execution-environments/): units 1 (Introduction) and 2 (How agents interact with GitHub APIs and workflows) left, plus the assessment, to do closed-book on review day.

**Where the module disagrees with docs.github.com (go with the docs):**
| Module says | Docs say |
|---|---|
| `npx @github/copilot-cli -p …` | install `npm install -g @github/copilot`, run `copilot -p …` |
| `COPILOT_GITHUB_TOKEN` from `GITHUB_TOKEN` | from a **PAT** secret |
| agent `applyTo` field | `applyTo` belongs to **instructions** files, not agent profiles |

## Mission 11: the capstone story

**Timeline of the failed run:** `workflow_dispatch` (simulate_outage) → attempt 1 fails → 30 s → attempt 2 → 60 s → attempt 3 → step fails → tool-call artifact upload (`always()`) → `needs-human` issue mentioning the owner with the run link (`failure()`) → notification.

**Guardrails:** `preToolUse` `block-infra.sh` denies `create|edit|bash` touching `infra/` in CLI **and** cloud agent sessions (it's a repo hook on `main`). The tool-call log lives in the **Actions artifact** for CLI runs in `agent-run.yml`; for cloud sessions, the **session log** is the record.

**Rollback:** bad PR merged into `capstone2-test` → **Revert** → revert PR merged → threshold restored.

**One line each:**
- **Error handling:** fail fast; the step exits 1 after the last attempt, and the job fails visibly.
- **Retries:** 3 attempts with exponential backoff, for transient failures only (a wrong prompt fails 3× and costs 3×).
- **Rollback:** branch isolation + PR review before merge; Revert PR after merge.
- **Escalation:** `needs-human` issue + @owner + run link, raised by a workflow step on `failure()`.
- **Traceability:** run log + artifact + issue ↔ run link + PR/revert timeline + commit history.

**What's still missing before I'd trust this at a bank:**
- **Required code-owner review** ruleset on `infra/` and `app/screening.py` (CODEOWNERS exists but isn't enforced yet), plus a **second reviewer**: the requester can't approve their own risk change.
- A **required check** asserting screening thresholds stay in an approved range.
- Logs that **outlive** 90-day artifact retention and are **tamper-evident** (ship to the bank's log store / SIEM via an `http` hook or a workflow step).
- Hook guard hardened against `bash` leaks (allow-list commands with `--allow-tool` instead of block-listing paths).
- Retries that tell **transient** from **permanent** failures, and a cap on spend.
- **Environment protections** with required approvers before anything deploys.

---

## Reflection

1. **Which guard would have stopped the bad threshold change earliest, and what would it cost in speed?** A `preToolUse` hook denying edits to `app/screening.py`: it stops it *during* the session, at the cost of the agent being unable to touch that file at all (every legit change needs a human). The cheaper-in-friction option is a **ruleset requiring code-owner review** (CODEOWNERS already lists the file): it costs one owner review per PR touching it.
2. **Where did traceability break or get manual?** Cloud agent hook output is **ephemeral**, so the cloud record is only the session log. The escalation issue links the run, but nothing links the issue back to the PR or revert automatically. Simulated runs produce no tool-call file at all.
3. **Financial Crimes angle:** lowering a screening threshold is a **model / risk-control change**. A bank would require model-risk-management sign-off (validation of the new threshold's false-negative impact), compliance approval, a change ticket, and segregation of duties (author ≠ approver). Encode it as: CODEOWNERS on threshold config → **ruleset** requiring code-owner + 2 approvals, a **required check** validating the value against an approved range, and a `preToolUse` **hook** so agents can't edit it at all.

## Side quest: an `errorOccurred` hook

Input fields ([reference](https://docs.github.com/en/copilot/reference/hooks-reference)): `sessionId`, `timestamp`, `cwd`, `error` {`message`, `name`, `stack?`}, `errorContext` (`model_call` · `tool_execution` · `system` · `user_input`), `recoverable` (bool). It's an **observer**: it can report and escalate, never block.
```bash
#!/bin/bash
# errorOccurred: print the payload to stderr
jq . >&2
exit 0
```

## Self-test (cover the answers)

<details><summary>1. A `preToolUse` guard hangs past `timeoutSec`. What happens to the tool call?</summary>Fail-open: it goes through the <b>normal permission flow</b>. In a cloud agent, all tools are pre-granted, so it runs.</details>
<details><summary>2. Guard prints <code>allow</code> and exits 2.</summary><b>Denied.</b> On gate events, exit 2 = deny even if stdout says allow.</details>
<details><summary>3. <code>postToolUse</code> logger exits 1.</summary>Logged, run continues. Observers can't block.</details>
<details><summary>4. Cloud agent hook returns <code>"ask"</code>.</summary>Treated as <b>deny</b>: the cloud agent is non-interactive.</details>
<details><summary>5. Where does a cloud agent hook's log file go?</summary>Nowhere: the filesystem is ephemeral. Use an <code>http</code> hook, or run the CLI in your own workflow and upload an artifact.</details>
<details><summary>6. Matcher <code>"create|edit"</code>, agent runs <code>sed -i … infra/x</code>.</summary>The guard never runs (bash isn't matched): the edit goes through.</details>
<details><summary>7. Revert button missing on a merged PR?</summary>You lack <b>write</b> access. If it was merged outside GitHub or conflicts → <code>git revert</code> the commits.</details>
<details><summary>8. Which token triggers new workflow runs: GITHUB_TOKEN or a PAT?</summary>A <b>PAT / GitHub App token</b>. GITHUB_TOKEN events don't start new runs (loop protection).</details>
<details><summary>9. Hooks on a feature branch: do they run in a cloud agent session?</summary>No: they must be on the <b>default branch</b>.</details>
<details><summary>10. The four safe-execution patterns?</summary>Retries · rollbacks · escalation paths · traceability (plus error handling).</details>

## Sources

- [Using hooks with Copilot cloud agent](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/use-hooks)
- [Hooks reference](https://docs.github.com/en/copilot/reference/hooks-reference)
- [Running Copilot CLI programmatically](https://docs.github.com/en/copilot/how-tos/copilot-cli/automate-copilot-cli/run-cli-programmatically#cicd-integration)
- [Reverting a pull request](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/reverting-a-pull-request)
- [Learn: Agent execution limits and protections](https://learn.microsoft.com/en-us/training/modules/agent-tooling-mcp-execution-environments/5-agent-execution-limits-protections)
