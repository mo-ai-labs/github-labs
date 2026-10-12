# Day 12 — Nobody pressed the button

> At 03:17 a test fails, an issue appears, Copilot picks it up and a PR shows up, all with **no human trigger**. Can you prove, link by link, which workflow run started it?

**Deliverable:** A PR opened with no human trigger, traceable to its workflow run

## Bets

- **Bet A** — Can your scheduled workflow assign an issue to Copilot using the built-in `GITHUB_TOKEN`? **My guess: No**
  - Result: **Win**: actual **No**. The issues API needs a **user token**: *"Make sure you're authenticating with the API using a user token, for example a personal access token or a GitHub App user-to-server token."* ([Creating and assigning a new issue](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-via-the-api#creating-and-assigning-a-new-issue)), and *"The `GITHUB_TOKEN` secret is a GitHub App installation access token."* ([About the GITHUB_TOKEN](https://docs.github.com/en/actions/concepts/security/github_token#about-the-github_token))
- **Bet B** — In an agentic workflow with `safe-outputs`, what write permissions does the **agent** itself hold? **My guess: Whatever the workflow grants**
  - Result: **Miss**: actual **Read-only**. Safe outputs let the workflow create issues, comments and PRs *"all without giving the agentic portion of the workflow any write permissions"* ([Safe outputs](https://github.github.com/gh-aw/reference/safe-outputs/)); the writes run in separate jobs because *"GitHub Actions permissions are per-job and immutable for the duration of a job"* ([Compilation Process](https://github.github.com/gh-aw/reference/compilation-process/#why-detection-safe-outputs-and-conclusion-are-separate-jobs)). Nuance: workflows are *"read-only by default … unless you explicitly grant more"*, so granting write in the frontmatter is possible but defeats the design

## Lessons (Mission 1 — Hand work to Copilot from a script)

Source: [Using the issues API](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-via-the-api#using-the-issues-api)

- Assign an issue to Copilot via **GraphQL** or **REST**; public preview, subject to change
- Optional `agent_assignment` = *how* to do it (assignee = *who*):

| REST | GraphQL | Controls |
|---|---|---|
| `target_repo` | `targetRepositoryId` | Repo Copilot works in |
| `base_branch` | `baseRef` | Branch Copilot starts from |
| `custom_instructions` | `customInstructions` | Extra instructions |
| `custom_agent` | `customAgent` | Custom agent to use |
| `model` | `model` | Model to use |

Source: [Adding assignees to an existing issue](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-via-the-api#adding-assignees-to-an-existing-issue)

- `POST /repos/OWNER/REPO/issues/ISSUE_NUMBER/assignees` with `"assignees": ["copilot-swe-agent[bot]"]` + optional `agent_assignment`
- Assigning **is** the start signal; no separate "start agent" call
- `POST /repos/OWNER/REPO/issues` takes the same `assignees` + `agent_assignment` → create and hand off in **one call**

Source: [Creating and assigning a new issue](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-via-the-api#creating-and-assigning-a-new-issue)

- Needs a **user token** (PAT or GitHub App user-to-server); a person is accountable and their Copilot seat pays
- Fine-grained PAT: read **metadata**; read + write **actions, contents, issues, pull requests**. Classic PAT: `repo`
- `GITHUB_TOKEN` = GitHub App **installation** token (`github-actions[bot]`), not a user → can't hand work to Copilot → store a PAT as an Actions secret (Mission 4)

Source: [Starting a session](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-from-cli#starting-a-session)

- `gh agent-task create "prompt"` starts Copilot with **no issue**; opens a PR in the current repo. Flags: `--base`, `--repo`, `--follow`
- Needs gh **v2.80.0+**; public preview
- Track: `gh agent-task list`, `gh agent-task view --log --follow`

**Which handoff for an unattended job?** The issue path. My first pick was "either, same traceability", and that's wrong: with `gh agent-task create` there's no issue, so the run link lives only in prompt text. With the issue path, every link (run → issue → PR) is a stored GitHub object you can click through.

![Two handoff paths](img/d12-handoff-paths.svg)

*Editable source: [d12-handoff-paths.excalidraw](img/d12-handoff-paths.excalidraw)*

## Lessons (Mission 2 — Agentic workflows and safe outputs)

Source: [How agentic workflows work](https://docs.github.com/en/copilot/concepts/agents/about-github-agentic-workflows#how-agentic-workflows-work)

- One `.md` file = YAML **frontmatter** (when it runs, permissions, allowed writes) + natural-language **body** (the agent's instructions)
- `gh aw compile` → hardened `.lock.yml` Actions workflow; commit **both** to the default branch; runs on its trigger, from the UI or the CLI
- **What needs a recompile?** Frontmatter: *"compiled into the lock file and requires recompilation when changed"* (security-sensitive). Body: *"loaded at runtime and takes effect on the next run"*, so you can edit it on GitHub.com without recompiling ([Editing Workflows](https://github.github.com/gh-aw/guides/editing-workflows/#editing-without-recompilation))

Source: [Security guardrails](https://docs.github.com/en/copilot/concepts/agents/about-github-agentic-workflows#security-guardrails)

- **Read-only by default**; writes (issues, comments, PRs) only through validated `safe-outputs` in the frontmatter
- **Secrets stay outside the agent runtime** (isolated downstream jobs) → a prompt-injected "print the secrets" fails first because the agent never had them
- **Threat detection** scans proposed outputs before writes; **firewalled execution**; **role-based access** on who triggers/edits
- Engines: Copilot (default, needs a Copilot plan), Claude, Codex, Gemini, each with its own auth secret. Public preview

Source: [Safe outputs: Comment Creation (add-comment:)](https://github.github.com/gh-aw/reference/safe-outputs/#comment-creation-add-comment)

- Core idea: create issues, comments and PRs *"all without giving the agentic portion of the workflow any write permissions"*
- Agent writes a **request** into its output artifact → separate `add_comment` job validates it against the frontmatter and posts with its own scoped token
- `max` (default 1); `target`: `"triggering"` (default), `"*"` or a number; `required-labels`; AI-generated footer on by default (traceability)
- Injected "post 5 comments, one on #99" with `max: 1` + default target → at most 1 comment, on the triggering issue only

Source: [Safe outputs: Add Labels (add-labels:)](https://github.github.com/gh-aw/reference/safe-outputs/#add-labels-add-labels)

- `allowed`: labels or glob patterns; `blocked`: denied *"regardless of the allow list"* (blocked wins); `max` (default 3)
- *"infrastructure-level protection against prompt injection attacks in repositories with many labels"*; labels can trigger deploys or skip reviews, so an injected label = privilege escalation
- `allowed: ["*"]`, `blocked: ["deploy-*"]`, `max: 2` + request {bug, deploy-prod, question, enhancement} → deploy-prod dropped, at most 2 of the rest

### What `gh aw compile` does

Source: [Compilation Process](https://github.github.com/gh-aw/reference/compilation-process/)

1. **Parse + validate**: extract frontmatter, check it against the schema, allow only allow-listed `${{ }}` expressions, resolve imports
2. **Build jobs**: pre_activation → activation → **agent** → detection → **safe output jobs** → conclusion
3. **Resolve dependencies**: topological order, no cycles
4. **Pin actions to SHAs** (*"tags can be moved, SHAs cannot"*); cache in `.github/aw/actions-lock.json` (commit it)
5. **Write `.lock.yml`**: frontmatter baked in, body loaded at runtime
- Why separate jobs: *"GitHub Actions permissions are per-job and immutable for the duration of a job"*, so the agent job stays read-only and only the safe-output jobs get scoped write permission. The agent hands off only an artifact
- Useful flags: `--strict`, `--actionlint`, `--zizmor`, `--poutine`, `--no-emit`; `gh aw validate` = compile + linters, no output

![Jobs in the lock file](img/d12-lock-jobs.svg)

*Editable source: [d12-lock-jobs.excalidraw](img/d12-lock-jobs.excalidraw)*

### What the compiled `issue-triage.lock.yml` actually contains (Mission 6)

`gh aw` v0.89.21 installed and compiled on **native Windows** (the docs only list Linux, macOS, Windows+WSL as supported). Output: `issue-triage.lock.yml` (~125 KB, `strict: true`, frontmatter + body hashes in its header), `.github/aw/actions-lock.json` (SHA pin cache).

| Job | Needs | Permissions |
|---|---|---|
| pre_activation | — | none |
| activation | pre_activation | actions: read, contents: read, issues: write |
| **agent** | activation | **contents: read, issues: read** |
| detection | activation, agent | contents: read |
| **safe_outputs** | activation, agent, detection | **issues: write, pull-requests: write** |
| conclusion | all | actions: read, issues: write, pull-requests: write |

Bet B, proven from the generated file: the agent job is read-only; writes live in `safe_outputs`, after `detection`. The agent's safe-output MCP server only exposes `add_comment`, `add_labels`, `missing_data`, `missing_tool`, `noop`.

**First run (Mission 6b):** test issue [#72](https://github.com/mosherif-labs/github-labs/issues/72) *"GET /alerts returns 500 when status filter is empty"* → agent (read-only) → `safe_outputs` applied **1 label (`bug`)** + **1 comment**, nothing else. `max: 2` is a ceiling, not a target.
- Comment author: `github-actions` (the `safe_outputs` job's token), **not** Copilot
- Built-in traceability: the comment footer says *"Generated by [Issue triage](…/actions/runs/38299822562) for #72 · copilot · auto"* plus usage figures, so the run link comes for free (the AI footer that `add-comment` adds by default)
- Read-only research paid off: the agent read the README and flagged that the filter is documented as `alert_status`, not `status` Token: `COPILOT_GITHUB_TOKEN` = fine-grained PAT on my **user account**, *Copilot Requests: Read* only ([auth reference](https://github.github.com/gh-aw/reference/auth/#copilot_github_token)); Learn unit 4's `secrets.GITHUB_TOKEN` is wrong, the docs win.

## Lessons (Mission 3 — Traceability, by design)

**What GitHub records for you** ([Administrators can lose sight of agents' work](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations#administrators-can-lose-sight-of-agents-work))

- Agent commits are co-authored and signed; session logs and audit-log events exist; commit messages link back to the agent session

**Automations with no person per task** ([Automations run without a person initiating each task](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations#automations-run-without-a-person-initiating-each-task))

- Work is attributed to **whoever created the automation**, and **they can't approve it** (no self-approval)
- Events from non-authorized users are ignored by default; Actions still need human approval to run on agent PRs

**Loops** ([Trigger behavior and workflow limits](https://learn.microsoft.com/en-us/training/modules/agent-tooling-mcp-execution-environments/5-agent-execution-limits-protections#trigger-behavior-and-workflow-limits))

- Most actions done with `GITHUB_TOKEN` don't trigger further workflow runs (loop protection); **PATs and App tokens can**, so design against recursion

**What I must add myself:** the link from the *triggering workflow run* to the issue (run URL + log tail in the issue body). GitHub links issue → session → PR → commits, but nothing records *which run* opened the issue unless the workflow writes it.

## Trace (Mission 7): PR #70 back to the run, with no human trigger

| # | Link | Evidence | Who GitHub says did it |
|---|---|---|---|
| 1 | **Run** [38296857335](https://github.com/mosherif-labs/github-labs/actions/runs/38296857335) | `nightly-tests`, `simulate_failure=true`; canary failed → `if: failure()` step ran | workflow run (dispatch) |
| 2 | **Issue** [#69](https://github.com/mosherif-labs/github-labs/issues/69) "Nightly tests failed (run 38296857335)" | body = run URL + pytest log tail (link 1, written by *our* workflow); Copilot reacted 👀 | author `sheriffMoose`; timeline: `sheriffMoose` assigned `Copilot` **and** `sheriffMoose` (API call only asked for Copilot) |
| 3 | **PR** [#70](https://github.com/mosherif-labs/github-labs/pull/70) + [session log](https://github.com/mosherif-labs/github-labs/pull/70/agent-sessions/327c8b6e-ac4d-4215-97e3-643d38c58fd9) | PR body links the run and says `Fixes #69`; session "Resolving nightly tests failure issue", **started on behalf of sheriffMoose**, 3m6s | Copilot, on behalf of `sheriffMoose` |
| 4 | **Commits** `24540ec` "Initial plan", `602cea4` "Treat deliberate nightly canary simulation as expected failure" | `602cea4` author `Copilot`, body `Co-authored-by: sheriffMoose`; **message has no session link** (the docs say commits link the session; here the link lives on the PR, not in the commit message) | Copilot + co-author `sheriffMoose` |

**What GitHub recorded for me:** issue → session → PR → commits, all attributed to the PAT owner (me).
**What only exists because I wrote it:** link 1 → 2 (run URL in the issue body) and the run link in the PR body (because `custom_instructions` asked for it). Nothing GitHub records names the workflow run as the trigger; every event says `sheriffMoose`.

**If someone deletes issue #69, where does the chain break?** My first answer: "it doesn't, GitHub records the run as the PR's trigger". Wrong: none of the records above name the run. Deleting the issue removes its body (the run URL + log), its timeline, and the target of `Fixes #69`. PR → run then survives **only** through the link in the PR body, which exists because `custom_instructions` asked for it. Fix: put the run link in more than one durable place (PR body via instructions, a workflow log line that prints the created issue URL) and restrict who can delete issues.

### Review of PR #70 (the agent "fixed" the alarm)

- Change: `@pytest.mark.xfail(SIMULATE_FAILURE == "true", raises=AssertionError, strict=True)` on `test_canary`, plus 2 tests of the canary itself
- Effect: with `simulate_failure=true` the canary now counts as an *expected* failure → suite green → `if: failure()` never fires → **no issue, no agent**. The drill silently stops working
- Root cause is **my instruction**, not the agent: `custom_instructions: "Fix the failing test"`. It did exactly that. An agent handed a red test will make it green unless told the failure might be intentional
- Lesson: hand-offs from automation must state intent and limits ("if the failure is intentional or environmental, explain in the PR and don't change tests"), and every agent PR still needs a human review. Green CI ≠ correct

## Reflection

1. **Who is accountable for the PR?** Me, the PAT owner: issue, assignment and agent session all record `sheriffMoose`. So I can't approve it myself; a second reviewer must.
2. **What stops the loop?** My first answer, GITHUB_TOKEN loop protection, was wrong: the issue is created with a **PAT**, which *can* trigger workflows. What actually stops it: `nightly-tests` only runs on `schedule` / `workflow_dispatch`; agent PRs run `ci.yml`, which never opens issues; Actions on agent PRs need human approval to run.
3. **Auditor: who approved the change after the 03:17 failure?** Run → issue (run URL in body) → agent session log → PR approved by a second person → merge commit, plus audit-log events. PR #70 is the reason the review is the real control.
