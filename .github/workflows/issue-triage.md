---
description: "Triage new issues in github-labs"
on:
  issues:
    types: [opened]
permissions:
  contents: read
  issues: read
engine: copilot
tools:
  github:
    toolsets: [default]
safe-outputs:
  add-comment:
    max: 1
  add-labels:
    allowed: [bug, enhancement, question, needs-human]
    max: 2
---

# Issue triage

Read the newly opened issue and the repository README.
Pick at most two labels from the allowed list and post one short comment
that restates the problem and names the endpoint it most likely touches.
If the issue mentions real customer or bank data, label it `needs-human`
and say only that a maintainer will follow up.
