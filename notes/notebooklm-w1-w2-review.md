# GH-600 — Weeks 1–2 review pack for NotebookLM

> Covers plan Days 1–14 (Sep 28 → Oct 11): **Domain 1** (agent architecture & SDLC, 15–20%) and **Domain 2** (tools, MCP, execution environments, 20–25%). Exam: **Sun Oct 25**.
> Built from `study-plans/docs/GH600_DAILY_PLAN.md`, the Mission Guides in `study-plans/assets/plans/GH-600/week01–02`, and my notes in `github-labs/notes/`.
> Status (updated Oct 13): Days 1–13 done. **Day 14 (Week 2 review) isn't done yet**; its topics are included anyway.

---

## 0. How to load this into NotebookLM

1. **Upload this file** as the first source. It tells NotebookLM what matters; the doc pages below are the evidence.
2. **Add the web sources** in section 1 (*Add source → Website*, one URL each). NotebookLM imports the **whole page** and ignores `#anchors`, so the page URLs below have no anchors. The exact sections to focus on are in sections 2–3.
   - Tier A = 36 pages, Tier A + B = 42. Tier C is extra (12 more).
3. **Upload my notes bundle** `notebooklm-w1-w2-notes-bundle.md` (all 15 notes files from section 4 in one file, gap log first). That keeps the total at **44 sources**, under the free plan's 50 limit.
4. Skip the `github.com/mosherif-labs/...` links (PRs, runs, sessions). The repo is private, so NotebookLM can't fetch them.
5. Use the prompts in section 6.

---

## 1. Web sources to add (deduplicated, no anchors)

### Tier A — core (must add; most-cited in my plans)

**Exam**
- https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-600

**Copilot cloud agent**
- https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent
- https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations
- https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results
- https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/manage-and-track-agents
- https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/review-copilot-output

**Instructions, custom agents, skills**
- https://docs.github.com/en/copilot/concepts/prompting/response-customization
- https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions
- https://docs.github.com/en/copilot/reference/custom-agents-configuration
- https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/create-custom-agents
- https://docs.github.com/en/copilot/concepts/agents/about-agent-skills

**Tools & permissions**
- https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/allowing-tools
- https://code.visualstudio.com/docs/copilot/chat/chat-tools

**MCP**
- https://docs.github.com/en/copilot/concepts/agents/cloud-agent/mcp-and-cloud-agent
- https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/extend-cloud-agent-with-mcp
- https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/configure-secrets-and-variables
- https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-mcp-usage/configure-mcp-server-access
- https://docs.github.com/en/copilot/reference/enterprise-administrators/mcp-private-registry-enforcement
- https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-mcp-usage/configure-enterprise-allowlist

**Execution environment, CI, hooks**
- https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/customize-the-agent-environment
- https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-the-firewall
- https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-via-the-api
- https://docs.github.com/en/copilot/concepts/agents/about-github-agentic-workflows
- https://docs.github.com/en/copilot/reference/hooks-reference
- https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/use-hooks

**Microsoft Learn units (the exam's own course material)**
- https://learn.microsoft.com/en-us/training/modules/foundations-agentic-ai/4-describe-github-system-record-control-plane
- https://learn.microsoft.com/en-us/training/modules/foundations-agentic-ai/5-identify-risks-traceability
- https://learn.microsoft.com/en-us/training/modules/foundations-agentic-ai/6-apply-contributor-model-agent-generated-work
- https://learn.microsoft.com/en-us/training/modules/design-agent-architecture-integration/2-agent-responsibilities
- https://learn.microsoft.com/en-us/training/modules/design-agent-architecture-integration/3-inputs-outputs-success-criteria
- https://learn.microsoft.com/en-us/training/modules/design-agent-architecture-integration/4-plan-reason-execution
- https://learn.microsoft.com/en-us/training/modules/design-agent-architecture-integration/5-pull-request-governance-controls
- https://learn.microsoft.com/en-us/training/modules/design-agent-architecture-integration/6-reliable-workflows
- https://learn.microsoft.com/en-us/training/modules/design-agent-architecture-integration/7-agent-operations-controls
- https://learn.microsoft.com/en-us/training/modules/agent-tooling-mcp-execution-environments/4-execution-context-boundaries
- https://learn.microsoft.com/en-us/training/modules/agent-tooling-mcp-execution-environments/5-agent-execution-limits-protections

### Tier B — supporting (add if room)
- https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-mcp-usage/configure-mcp-registry
- https://docs.github.com/en/copilot/how-tos/copilot-in-your-ide/customize-copilot/extend-copilot-with-tools-and-context/configure-toolsets
- https://github.com/github/github-mcp-server/blob/main/docs/remote-server.md
- https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-from-cli
- https://github.github.com/gh-aw/reference/safe-outputs/
- https://docs.github.com/en/copilot/how-tos/copilot-cli/automate-copilot-cli/run-cli-programmatically

### Tier C — GitHub platform basics (only if a separate notebook or Pro)
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms
- https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema
- https://docs.github.com/en/actions/tutorials/manage-your-work/add-comments-with-labels
- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
- https://docs.github.com/en/actions/reference/workflows-and-actions/expressions
- https://docs.github.com/en/actions/concepts/security/github_token
- https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/reverting-a-pull-request
- https://github.github.com/gh-aw/setup/quick-start/
- https://github.github.com/gh-aw/reference/auth/
- https://docs.github.com/en/copilot/reference/supported-surfaces-for-policies

---

## 2. Week 1 — Domain 1: Agent architecture & SDLC (Days 1–7)

**Study-guide bullets (Skills measured):**
- *Integrate agents into the SDLC* — steps for agents, anti-patterns, inputs/outputs/success criteria
- *Define boundaries between planning, reasoning, and action* — planning distinct from execution, structured plan, validate plans, prevent action until approved
- *Configure observability and control* — degree of autonomy incl. guardrails, inspectable artifacts, human intervention without slowing delivery

### Day 1 — How Copilot cloud agent works in the SDLC
**Focus sections**
- [About cloud agent — Overview](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent#overview-of-copilot-cloud-agent) · [Limitations (workflow)](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent#limitations-in-copilot-cloud-agents-software-development-workflow) · [Customizing](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent#customizing-copilot-cloud-agent)
- [Repository instructions — Creating](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions#creating-custom-instructions) · [Path-specific](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions#creating-path-specific-custom-instructions)
- [Precedence of custom instructions](https://docs.github.com/en/copilot/concepts/prompting/response-customization#precedence-of-custom-instructions)
- [Choosing the right type of tasks](https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results#choosing-the-right-type-of-tasks-to-give-to-copilot)
- [Learn — Mapping SDLC stages to GitHub artifacts](https://learn.microsoft.com/en-us/training/modules/design-agent-architecture-integration/2-agent-responsibilities#mapping-sdlc-stages-to-github-artifacts)

**Key facts**
- Entry points: agents panel/tab, assigning an issue, `@copilot` on a PR, IDE, CLI/API, automations (schedule/events). Runs in an ephemeral GitHub Actions environment.
- Limits: **one repo, one branch, one PR per task; 59-minute hard session cap**.
- Five customization levers: custom instructions, MCP servers, custom agents, hooks, skills.
- Files: `.github/copilot-instructions.md` (repo-wide), `.github/instructions/NAME.instructions.md` with `applyTo` globs (+ `excludeAgent`), `AGENTS.md` anywhere.
- Precedence: **Personal → Repository (path-specific → repo-wide → `AGENTS.md`) → Organization**; nothing is dropped, all relevant sets are sent.
- Good agent tasks: bugs, UI tweaks, test coverage, docs, accessibility, tech debt. Keep for humans: cross-repo refactors, production-critical, security/PII/auth, ambiguous work. Deployment is usually restricted.
- My lesson: merge the rulebook to `main` **before** assigning, or the run won't see it.

### Day 2 — Task contracts & anti-patterns
**Focus sections**
- [Learn — Task structure makes outcomes predictable](https://learn.microsoft.com/en-us/training/modules/design-agent-architecture-integration/3-inputs-outputs-success-criteria#task-structure-makes-outcomes-predictable) · [Example task contract](https://learn.microsoft.com/en-us/training/modules/design-agent-architecture-integration/3-inputs-outputs-success-criteria#example-task-contract-vulnerability-remediation)
- [Learn — Common risks and anti-patterns](https://learn.microsoft.com/en-us/training/modules/foundations-agentic-ai/5-identify-risks-traceability#common-risks-and-anti-patterns)
- [Well-scoped issues](https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results#making-sure-your-issues-are-well-scoped)
- [Issue forms — top-level syntax](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms#top-level-syntax)

**Key facts**
- Inputs = issue context, constraints, boundaries. Outputs = plan + PR + evidence. Success criteria = checks, scans, review outcomes.
- Anti-patterns → mitigations: planless execution → plan section in PR template; over-permissioned agent → least-privilege token + environments; hidden reasoning → plan + linked runs; blind trust ("CI passed") → CODEOWNERS + required reviews; vague scope; oversized tasks; too many tools; agent grading its own work.
- Success criteria must be **enforced by the system** (required status checks), not just written in instructions.
- Issue form required keys: `name`, `description`, `body`.

### Day 3 — Planner vs implementer agents
**Focus sections**
- [Custom agents — YAML frontmatter](https://docs.github.com/en/copilot/reference/custom-agents-configuration#yaml-frontmatter-properties) · [Tools](https://docs.github.com/en/copilot/reference/custom-agents-configuration#tools) · [Tool aliases](https://docs.github.com/en/copilot/reference/custom-agents-configuration#tool-aliases)
- [Learn — Why separation improves reliability](https://learn.microsoft.com/en-us/training/modules/design-agent-architecture-integration/4-plan-reason-execution#why-separation-improves-reliability) · [Enforcing planning boundaries](https://learn.microsoft.com/en-us/training/modules/design-agent-architecture-integration/4-plan-reason-execution#enforcing-planning-boundaries-using-capability-limits-and-tool-gating)
- [Using custom agents](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/create-custom-agents#using-custom-agents)

**Key facts**
- Only `description` is required. Optional: `name`, `target` (`vscode`/`github-copilot`, default both), `tools`, `model`, `disable-model-invocation`, `user-invocable`, `mcp-servers`, `metadata`. `infer` is retired.
- `tools` omitted or `["*"]` = all; a list = only those; `[]` = **none**.
- Aliases: `read`, `edit`, `search`, `execute` (shell/Bash/powershell), `agent`, `web`, `todo` — **`web` and `todo` don't apply to the cloud agent**.
- Four planning-boundary mechanisms: read-only planning agent, explicit handoff after approval, tool gating, plan mode.
- Profiles must be merged to the default branch; org-level agents live in the org's `.github`/`.github-private` repo; repo-level overrides by name.

### Day 4 — Plan validation & approval gate
**Focus sections**
- [Learn — Option A: plan-first PR](https://learn.microsoft.com/en-us/training/modules/design-agent-architecture-integration/4-plan-reason-execution#option-a-plan-first-pull-request)
- [Learn — PRs are architectural control points](https://learn.microsoft.com/en-us/training/modules/design-agent-architecture-integration/5-pull-request-governance-controls#pull-requests-are-architectural-control-points) · [PR template requiring a plan](https://learn.microsoft.com/en-us/training/modules/design-agent-architecture-integration/5-pull-request-governance-controls#implementation-pr-template-that-requires-a-structured-plan) · [CODEOWNERS](https://learn.microsoft.com/en-us/training/modules/design-agent-architecture-integration/5-pull-request-governance-controls#using-codeowners-to-ensure-safety)
- [Events — issues](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#issues) · [Expressions — contains](https://docs.github.com/en/actions/reference/workflows-and-actions/expressions#contains)

**Key facts**
- Option A (plan-first PR, approved before code) for high-risk / hard-to-reverse changes; Option B (plan + code in one PR) still validated before merge.
- A plan-gate workflow as a **required status check** turns "please include a plan" into a guarantee.
- An agent that can bypass checks or merge without review = workflow design failure, not a model problem.
- Validate the plan against the **request** ("every file justified by the issue"), not just a deny-list.
- A workflow on `issues: assigned` can comment, but it **doesn't stop** Copilot from starting.

### Day 5 — Autonomy, inspectable artifacts, human intervention
**Focus sections**
- [Learn — Autonomy must be designed](https://learn.microsoft.com/en-us/training/modules/design-agent-architecture-integration/6-reliable-workflows#autonomy-must-be-designed-not-assumed)
- [Learn — Traceability and observability](https://learn.microsoft.com/en-us/training/modules/foundations-agentic-ai/5-identify-risks-traceability#traceability-and-observability)
- [Trace commits to session logs](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/manage-and-track-agents#trace-commits-to-session-logs) · [Steer an agent session](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/manage-and-track-agents#steer-an-agent-session)
- [Manage Actions workflow runs](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/review-copilot-output#manage-github-actions-workflow-runs)
- [Risks — agent can push code](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations#copilot-cloud-agent-can-push-code-changes-to-your-repository)
- [Limitations — compatibility with other features](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent#limitations-in-copilot-cloud-agents-compatibility-with-other-features)
- [Learn — GitHub as the control plane](https://learn.microsoft.com/en-us/training/modules/foundations-agentic-ai/4-describe-github-system-record-control-plane#github-as-the-control-plane) · [The contributor model](https://learn.microsoft.com/en-us/training/modules/foundations-agentic-ai/6-apply-contributor-model-agent-generated-work#the-contributor-model)

**Key facts**
- Autonomy by risk: **Low** (`docs/`) automerge after checks · **Medium** (`src/`, deps) PR + checks + ≥1 review · **High** (`infra/`, workflows) CODEOWNERS + multiple reviews · **Critical** (prod, secrets) environment approvals; agent prepares, can't execute.
- Copilot pushes to a `copilot/` branch (or the PR's branch when `@copilot` on a PR); subject to branch protections.
- Workflows **don't run automatically** on Copilot's pushes → *Approve and run workflows*.
- The person who asked for the PR **can't approve it**. Only users with write access can trigger the agent.
- Commits authored by Copilot, requester as **co-author**; commit message links to session logs.
- Steering a running session costs AI credits; *Stop session* keeps pushed commits.
- Incompatible rulesets block the agent → add **Copilot as a bypass actor** (rulesets only).
- Minimum audit trail: goal · plan · bounded changeset · automated evidence · human judgment · outcome.
- Contributor model rubric: intent · scope · evidence · ownership · policy · fallback. Avoid both excessive suspicion and excessive trust.

### Day 6 — Capstone 1: plan → approve → execute
**Focus sections**
- [Learn — Outputs are workflow contracts](https://learn.microsoft.com/en-us/training/modules/design-agent-architecture-integration/6-reliable-workflows#outputs-are-workflow-contracts-step-outputs-vs-job-outputs-vs-env)
- [Learn — Minimum observability set](https://learn.microsoft.com/en-us/training/modules/design-agent-architecture-integration/7-agent-operations-controls#minimum-observability-set) · [Control tools, MCP, secrets](https://learn.microsoft.com/en-us/training/modules/design-agent-architecture-integration/7-agent-operations-controls#how-to-control-tools-mcp-integrations-and-secrets-safely)

**Key facts**
- Same required check fails **twice → escalate** to a human (what failed, what was tried, evidence, next step).
- Agent profiles give three boundaries: **capability** (tools), **visibility** (user-selectable), **delegation** (subagents/handoffs).
- Step outputs (`$GITHUB_OUTPUT`) stay in a job; job outputs cross jobs via `needs.<job>.outputs`.
- My finding: every plan needed a **test** fix, never a scope fix.

### Day 7 — Week 1 review: know cold
- Instruction-file precedence (see Day 1).
- Custom instructions vs custom agents vs **skills** ([About agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills#about-agent-skills)): skills are folders of instructions/scripts/resources loaded *when relevant*; project skills in `.github/skills`, `.claude/skills` or `.agents/skills`.
- Human checkpoints without approving every step: required checks, risk-tiered autonomy, plan-first only for high risk, steering via PR comments.

---

## 3. Week 2 — Domain 2: Tools, MCP, execution environments (Days 8–14)

**Week goal:** an agent runs from CI with least-privilege tools, a restricted network, hooks that block dangerous edits, and a clear escalation path.

### Day 8 — Tool selection & permissions
**Focus sections**
- [Custom agents — Tools](https://docs.github.com/en/copilot/reference/custom-agents-configuration#tools) · [Tools processing](https://docs.github.com/en/copilot/reference/custom-agents-configuration#tools-processing)
- [CLI — Allowing or denying specific tools](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/allowing-tools#allowing-or-denying-permission-for-specific-tools) · [Restricting tool choice](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/allowing-tools#restricting-the-choice-of-tools-available-to-the-ai-model) · [Persisted permissions](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/allowing-tools#persisted-permissions)
- [VS Code — Tool approval](https://code.visualstudio.com/docs/copilot/chat/chat-tools#tool-approval)
- [Creating a custom agent profile](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/create-custom-agents#creating-a-custom-agent-profile-in-a-repository-on-github)

**Key facts**
- `tools:` **filters** built-in and MCP tools alike; unknown names are ignored. MCP tools: `server/tool` or `server/*`.
- CLI has two layers: **availability** (`--available-tools` / `--excluded-tools`; if both given, **available wins**) and **permission** (`--allow-tool` / `--deny-tool`; **deny wins**). Patterns: `shell(git push)`, `shell(git:*)`, `write(path)`, `MyMCP(tool)`.
- Interactive CLI approvals persist in `permissions-config.json`; command-line flags are session-only; `/reset-allowed-tools` clears.
- Per surface: **CLI** = flags + `permissions-config.json` · **VS Code** = Allow dropdown + `chat.tools.terminal.autoApprove` + *Reset Tool Confirmations* · **cloud agent** = no prompt, the profile's `tools:` is the gate.
- Profile filenames allow `.`, `-`, `_`, letters, digits (no spaces).
- My surprise: docs-writer (`read`, `edit`) still ran pytest via a *Task* sub-step → verify the session log; back up with hooks/checks.

### Day 9 — MCP servers
**Focus sections**
- [MCP and cloud agent — Overview](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/mcp-and-cloud-agent#overview) · [Default MCP servers](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/mcp-and-cloud-agent#default-mcp-servers) · [Setting up in a repo](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/mcp-and-cloud-agent#setting-up-mcp-servers-in-a-repository) · [For custom agents](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/mcp-and-cloud-agent#mcp-servers-for-custom-agents)
- [Extend with MCP — JSON config](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/extend-cloud-agent-with-mcp#writing-a-json-configuration-for-mcp-servers) · [Adding config to repo](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/extend-cloud-agent-with-mcp#adding-an-mcp-configuration-to-your-repository) · [Reusing VS Code config](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/extend-cloud-agent-with-mcp#reusing-your-mcp-configuration-from-visual-studio-code) · [Customizing built-in GitHub MCP](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/extend-cloud-agent-with-mcp#customizing-the-built-in-github-mcp-server)
- [Secrets — naming](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/configure-secrets-and-variables#naming-requirements-for-secrets-and-variables) · [About](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/configure-secrets-and-variables#about-secrets-and-variables-for-copilot-cloud-agent)
- [Toolsets](https://docs.github.com/en/copilot/how-tos/copilot-in-your-ide/customize-copilot/extend-copilot-with-tools-and-context/configure-toolsets#configuring-toolsets-for-the-github-mcp-server) · [Remote server: toolsets + read-only](https://github.com/github/github-mcp-server/blob/main/docs/remote-server.md)
- [Custom agents — MCP env vars & secrets](https://docs.github.com/en/copilot/reference/custom-agents-configuration#mcp-server-environment-variables-and-secrets) · [MCP server configurations](https://docs.github.com/en/copilot/reference/custom-agents-configuration#mcp-server-configurations) · [MCP server type](https://docs.github.com/en/copilot/reference/custom-agents-configuration#mcp-server-type)

**Key facts**
- Cloud agent supports MCP **tools only** (no resources/prompts); **no OAuth** remote servers; **no approval prompt** — it calls tools autonomously, so allowlist specific read-only tools.
- Defaults: GitHub MCP (read-only, current repo) + Playwright (localhost only).
- Repo config: **Settings → Copilot → MCP servers**, set by **repo admins**; applies to cloud agent **and** code review (code review keeps only `readOnlyHint` tools).
- JSON: `mcpServers`, each needs `tools` + `type` (`local`/`stdio`/`http`/`sse`); `stdio` maps to `local`.
- Secrets: **Agents** secrets/variables (separate from Actions) named **`COPILOT_MCP_*`**; not exposed as normal env vars. `${{ secrets.X }}` works only in profile YAML.
- Processing order: out-of-the-box → custom agent `mcp-servers` → **repository settings (last, wins)**. Profile MCP servers are visible only to that agent.
- GitHub MCP read-only: `/readonly` URL path or `X-MCP-Readonly` header; toolsets via `X-MCP-Toolsets` header (several) or `/x/{toolset}` (one). Widen with `COPILOT_MCP_GITHUB_PERSONAL_ACCESS_TOKEN`.
- Where MCP config lives: VS Code `.vscode/mcp.json` · cloud agent = repo settings JSON · agent profile = `mcp-servers:` frontmatter.

### Day 10 — MCP registries & allowlists
**Focus sections**
- [Rulesets — bypass permissions](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository#granting-bypass-permissions-for-your-branch-or-tag-ruleset)
- [Configure MCP server access — org policy](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-mcp-usage/configure-mcp-server-access#configuring-the-mcp-allowlist-policy-for-an-organization) · [enterprise policy](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-mcp-usage/configure-mcp-server-access#configuring-the-mcp-allowlist-policy-for-an-enterprise)
- [Registry endpoint requirements](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-mcp-usage/configure-mcp-registry#endpoint-and-specification-requirements)
- [Enforcement — Supported surfaces](https://docs.github.com/en/copilot/reference/enterprise-administrators/mcp-private-registry-enforcement#supported-surfaces) · [Limitations](https://docs.github.com/en/copilot/reference/enterprise-administrators/mcp-private-registry-enforcement#current-enforcement-limitations) · [Local servers](https://docs.github.com/en/copilot/reference/enterprise-administrators/mcp-private-registry-enforcement#enforcement-for-local-servers) · [Multiple seats](https://docs.github.com/en/copilot/reference/enterprise-administrators/mcp-private-registry-enforcement#policy-resolution-for-users-with-multiple-seats)
- [Enterprise allowlist (`managed-settings.json`)](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-mcp-usage/configure-enterprise-allowlist)

**Key facts**
- Three knobs: *MCP servers in Copilot* enabled · *MCP Registry URL* · *Restrict MCP access to registry servers* = **Allow all** or **Registry only**. Org: Settings → Copilot → Policies. Enterprise: AI controls → MCP. Business/Enterprise seats only.
- Registry = v0.1 spec: `GET /v0.1/servers`, `/{name}/versions/latest`, `/{name}/versions/{version}` + CORS headers. Azure API Center: base URL only.
- Enforced on **IDEs + Copilot CLI** (min versions: CLI 1.0.11, VS Code 1.109.3, VS 18.4.0, JetBrains, Eclipse, Xcode). **Not the cloud agent.**
- Matching is by **name/ID only**; can't yet block *installing*. Local servers need an exactly matching server ID.
- Seat policy follows whoever **assigns the seat**; tie-break = **scope → strictness → recency** (enterprise over org first).
- `managed-settings.json`: once an allow list exists, anything not on it is blocked; deny still wins; `serverCommand` must match exactly.
- Two lanes: developer laptop → registry policy / managed settings · **cloud agent → repo MCP JSON + agent profiles** (pick the lane by where the server runs).
- Solo practice: ruleset bypass for *Repository admin* in **For pull requests only** mode.

### Day 11 — Execution environment, scope & firewall
**Focus sections**
- [Setup steps](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/customize-the-agent-environment#customizing-copilots-development-environment-with-copilot-setup-steps) · [Preinstalling deps](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/customize-the-agent-environment#preinstalling-tools-or-dependencies-in-copilots-environment) · [Larger runners](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/customize-the-agent-environment#upgrading-to-larger-github-hosted-github-actions-runners) · [Self-hosted runners](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/customize-the-agent-environment#using-self-hosted-github-actions-runners)
- [Firewall — Overview](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-the-firewall#overview) · [Limitations](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-the-firewall#limitations) · [Recommended allowlist](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-the-firewall#understanding-the-recommended-firewall-allowlist) · [Custom allowlist](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-the-firewall#managing-the-custom-allowlist)
- [Learn — Branch-based scope](https://learn.microsoft.com/en-us/training/modules/agent-tooling-mcp-execution-environments/4-execution-context-boundaries#configure-an-agent-to-use-branch-based-scope)

**Key facts**
- `.github/workflows/copilot-setup-steps.yml`, single job named **`copilot-setup-steps`**, on the **default branch**. Keys: `steps`, `permissions`, `runs-on`, `services`, `snapshot`, `timeout-minutes` (max 59).
- A failing setup step → Copilot **skips the remaining setup steps** and starts anyway (no abort). Check the setup-steps run is green.
- Runners: only **Ubuntu x64** and **Windows 64-bit**. Self-hosted (ARC) / Windows → firewall must be **disabled**.
- Firewall is on by default; blocks show as a **warning in the PR body / a comment**. Applies **only to processes the agent starts via its Bash tool** — **not** MCP servers, **not** setup steps.
- Custom allowlist: Settings → Copilot → Internet access. **Domain** entry = itself + subdomains (not siblings/parent); **URL** entry = scheme + host + path prefix.
- Branch scope is enforced by the **execution context** (base branch picked when delegating), not the profile.
- My lesson: a blocked fetch can lead the agent to **fabricate** data and still open a green PR → say "if it fails, stop".

### Day 12 — Agents invoked from CI
**Focus sections**
- [Via the API — issues API](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-via-the-api#using-the-issues-api) · [Adding assignees](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-via-the-api#adding-assignees-to-an-existing-issue) · [Creating and assigning](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-via-the-api#creating-and-assigning-a-new-issue)
- [From the GitHub CLI — starting a session](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-from-cli#starting-a-session)
- [Agentic workflows — how they work](https://docs.github.com/en/copilot/concepts/agents/about-github-agentic-workflows#how-agentic-workflows-work) · [Security guardrails](https://docs.github.com/en/copilot/concepts/agents/about-github-agentic-workflows#security-guardrails)
- [Safe outputs — add-comment](https://github.github.com/gh-aw/reference/safe-outputs/#comment-creation-add-comment) · [add-labels](https://github.github.com/gh-aw/reference/safe-outputs/#add-labels-add-labels)
- [Risks — admins lose sight](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations#administrators-can-lose-sight-of-agents-work) · [Automations run without a person](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations#automations-run-without-a-person-initiating-each-task)
- [Learn — Trigger behavior and workflow limits](https://learn.microsoft.com/en-us/training/modules/agent-tooling-mcp-execution-environments/5-agent-execution-limits-protections#trigger-behavior-and-workflow-limits)

**Key facts**
- Assign via REST/GraphQL: `assignees: ["copilot-swe-agent[bot]"]` + `agent_assignment` (`target_repo`, `base_branch`, `custom_instructions`, `custom_agent`, `model`). Needs a **user token** (PAT), not `GITHUB_TOKEN`.
- `gh agent-task create` (CLI 2.80.0+) starts a session without an issue — weaker traceability than the issue path.
- Agentic workflows: Markdown (frontmatter + natural-language body) compiled with `gh aw compile` to `.lock.yml`; commit both. **Read-only by default**; writes only via validated **safe outputs** run by separate jobs. Engine token `COPILOT_GITHUB_TOKEN` (PAT with Copilot Requests).
- Automation work is attributed to whoever created the automation, and **they can't approve it**.
- `GITHUB_TOKEN` actions don't trigger new workflow runs (loop protection); PATs/App tokens can → design against recursion.
- My lesson: put the run link in more than one durable place; deleting the issue breaks the chain otherwise.

### Day 13 — Capstone 2: safe execution
**Focus sections**
- [Hooks — creating in a repo](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/use-hooks#creating-a-hook-in-a-repository-on-github) · [Troubleshooting](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/use-hooks#troubleshooting)
- [Hooks reference — preToolUse decision control](https://docs.github.com/en/copilot/reference/hooks-reference#pretooluse-decision-control) · [Exit codes](https://docs.github.com/en/copilot/reference/hooks-reference#exit-codes-for-command-hooks) · [Tool names](https://docs.github.com/en/copilot/reference/hooks-reference#tool-names-for-hook-matching) · [Cloud agent environment](https://docs.github.com/en/copilot/reference/hooks-reference#cloud-agent-execution-environment) · [Hooks locations](https://docs.github.com/en/copilot/reference/hooks-reference#hooks-locations)
- [Learn — Retries](https://learn.microsoft.com/en-us/training/modules/agent-tooling-mcp-execution-environments/5-agent-execution-limits-protections#retries) · [Rollbacks](https://learn.microsoft.com/en-us/training/modules/agent-tooling-mcp-execution-environments/5-agent-execution-limits-protections#rollbacks) · [Escalation paths](https://learn.microsoft.com/en-us/training/modules/agent-tooling-mcp-execution-environments/5-agent-execution-limits-protections#escalation-paths) · [Traceability](https://learn.microsoft.com/en-us/training/modules/agent-tooling-mcp-execution-environments/5-agent-execution-limits-protections#traceability-and-accountability)
- [Run CLI programmatically — CI/CD](https://docs.github.com/en/copilot/how-tos/copilot-cli/automate-copilot-cli/run-cli-programmatically#cicd-integration) · [Reverting a PR](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/reverting-a-pull-request#reverting-a-pull-request)

**Key facts**
- `.github/hooks/NAME.json`, `"version": 1`, on the default branch. Events include `sessionStart`, `sessionEnd`, `userPromptSubmitted`, `preToolUse`, `postToolUse`, `errorOccurred`, `postToolUseFailure`, `agentStop`, `subagentStart/Stop`.
- `preToolUse` returns `permissionDecision` `allow`/`deny`/`ask`. **Crash / non-zero exit = deny (fail-closed); timeout = fail-open; HTTP hooks = fail-open.** Any `deny` among several hooks wins. Don't print `allow` if you have no opinion.
- Exit `2`: deny on `preToolUse`/`permissionRequest` (even if stdout says allow); recovery guidance on `postToolUseFailure`; a warning elsewhere. Only **gate** events can block.
- Guard for writes under `infra/` must match **`create|edit|bash`**; `matcher` filters before the script runs. Back it with a ruleset/CODEOWNERS.
- Cloud agent: only the `bash` field runs; workdir `/workspace`; filesystem **ephemeral** (hook-written files are gone after the job — not committed, not an artifact; the **session log** is the record); permissions pre-granted, so a hook's `ask` = **deny**. `notification` doesn't fire, `permissionRequest` has no effect, `preCompact` only `auto`. Default hook timeout 30 s; single-line JSON output.
- Copilot CLI loads hooks from policy files, repo `.github/hooks/`, `~/.copilot/hooks/`, settings and plugins (all run); the cloud agent loads **only** repo `.github/hooks/*.json`.
- To keep a tool-call log, run the CLI in your own workflow and upload it with `actions/upload-artifact` (`if: always()`), or use an `http` hook.
- Safe-execution patterns (Learn unit 5): error handling (fail fast) · retries (transient only, backoff) · rollbacks (branch isolation + PR review, revert after merge) · escalation (notify from workflow steps) · traceability. Summary: *resilient, controlled, auditable, human-governed*.
- `errorOccurred` is an observer (fields `error`, `errorContext`, `recoverable`): it can report, never block.
- Rollback = branch isolation + PR review; after merge, **Revert** opens a new PR.
- Copilot CLI in CI: `copilot -p "..." -s --allow-tool=... --no-ask-user` (`--share=./audit.md` saves the transcript), auth `COPILOT_GITHUB_TOKEN` (PAT).
- Where Learn module 3 disagrees with the docs, **the docs win**: install `npm install -g @github/copilot` and run `copilot -p` (not `npx @github/copilot-cli`); `COPILOT_GITHUB_TOKEN` comes from a PAT, not `GITHUB_TOKEN`; `applyTo` belongs to instructions files, not agent profiles.

### Day 14 — Week 2 review: know cold *(not done yet)*
- Agent frontmatter + tool aliases
- MCP config locations (VS Code / cloud agent / profile) and their precedence
- Cloud agent limits (one repo, one branch, one PR, 59 min)
- Firewall defaults and scope
- Where registry/allowlist policies are set, and which surfaces enforce them

---

## 4. My own notes (already combined in `notebooklm-w1-w2-notes-bundle.md`)

From `github-labs/notes/` (my bets, evidence and corrections). Regenerate the bundle if these change:

| File | Day |
|---|---|
| `d01-artifacts.md` | 1 — artifacts of a cloud agent run |
| `d02-antipatterns.md` | 2 — vague vs templated task |
| `d03-agents.md` | 3 — planner / implementer |
| `d04-plan-gate.md`, `plan-checklist.md` | 4 — plan gate |
| `d05-controls.md` | 5 — built-in controls with evidence |
| `w01-capstone.md` | 6 — capstone timings and interventions |
| `w01-quiz.md` | 7 — 20 Domain 1 questions + answer key |
| `d08-tools.md` | 8 — tool belts |
| `d09-mcp.md` | 9 — MCP |
| `d10-mcp-governance.md` | 10 — registries & allowlists |
| `d11-env.md` | 11 — environment failures |
| `d12-ci.md` | 12 — CI-triggered agents |
| `w02-capstone.md` | 13 — hooks, retries, escalation, rollback |
| **`gap-log.md`** | **all misses — most valuable source** |

Optional: diagrams in `notes/img/*.svg` (convert to PNG/PDF first if NotebookLM rejects SVG).

---

## 5. Weak spots (from my gap log) — ask NotebookLM to drill these

1. **Instruction precedence**: personal > repository (path-specific > repo-wide > `AGENTS.md`) > organization; all are still sent.
2. **Success criteria** are enforced by required checks, not by instruction files.
3. **Plan validation** checks against the request ("every file justified"), not just a deny-list.
4. **Commit traceability**: Copilot is author, requester is co-author, commit message links to the session log.
5. **CLI tool layers**: availability (`--available-tools` beats `--excluded-tools`) vs permission (`--deny-tool` beats `--allow-tool`); approvals persist in `permissions-config.json`.
6. **Tool approval differs per surface** (CLI / VS Code / cloud agent has no prompt).
7. **Org agent profiles** are files in `.github`/`.github-private`, not a settings page.
8. **`web` isn't available** to the cloud agent.
9. **Cloud-agent MCP secrets** = Agents secrets prefixed `COPILOT_MCP_`, not Actions secrets.
10. **MCP config precedence**: repository settings are processed last and win.
11. **Registry only is not enforced on the cloud agent** — the cloud agent's MCP gate is repo admins + agent profiles.
12. **`managed-settings.json`**: an allow list blocks everything not on it; deny still wins; exact `serverCommand` match.
13. **Policy tie-breakers**: scope → strictness → recency.
14. **Setup-step failure** skips the remaining steps; it does not abort.
15. **Runners**: Ubuntu x64 / Windows 64-bit only; self-hosted needs the firewall disabled.
16. **Firewall scope**: only the Bash tool's processes, not MCP servers or setup steps.
17. **Domain allowlist entry**: itself + subdomains only.
18. **Hook failure modes**: timeout = fail-open; exit 2 on `preToolUse` = deny; only gate events can block; guard matcher `create|edit|bash`.
19. **Cloud agent hook output**: a file a hook writes is **gone** after the session (not committed, not an artifact); the session log is the record.

---

## 6. Prompts to use in NotebookLM

- *"Using only the GitHub Docs and Microsoft Learn sources, quiz me with 15 scenario-style multiple-choice questions on Domain 2 (tools, MCP, execution environment). Cite the source for each answer."*
- *"Quiz me on the 19 weak spots in section 5 of the review pack. Make the wrong options the mistakes I actually made in gap-log.md."*
- *"Explain the difference between where MCP servers are governed for developer IDEs/CLI versus the Copilot cloud agent. Build a table: surface, where configured, who can set it, what enforces it."*
- *"Compare every way to limit what an agent can do: profile `tools:`, CLI flags, MCP tool allowlists, firewall, hooks, rulesets, CODEOWNERS, required checks. For each: what it blocks, where it's set, and how it fails."*
- *"List every fail-open vs fail-closed behavior across hooks, setup steps and the firewall."*
- **Audio Overview** customization: *"Focus on the cloud agent's limits, custom agent frontmatter, MCP configuration and secrets, registry enforcement surfaces, the firewall and hooks. Skip basic GitHub Actions syntax."*
- **Study guide / flashcards** feature: generate from Tier A sources + `gap-log.md`.
