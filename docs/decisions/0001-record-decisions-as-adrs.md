# 0001 - Record agent-relevant decisions as ADRs

Status: Accepted
Date: 2026-10-14

## Context
Copilot Memory expires unused facts after 28 days and is not reviewed in PRs.

## Decision
Durable decisions live in docs/decisions/NNNN-title.md, reviewed via PR.

## Consequences
Agents are told (AGENTS.md) to read docs/decisions/ before changing behaviour.
