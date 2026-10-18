import fnmatch
import os
import re
import sys
from pathlib import Path

# Runs only on agent PRs (the workflow skips human PRs), from a checkout of main.
# Approved plans live in notes/plans/<issue>.md (moved there from plans/ in 804f5f2);
# progress files stay in plans/<issue>-progress.md.
changed = [c.strip() for c in Path(sys.argv[1]).read_text().splitlines() if c.strip()]
m = re.search(r"Plan:\s*((?:notes/)?plans/\S+\.md)", os.environ.get("PR_BODY") or "")
issue = os.environ.get("ISSUE")  # the issue this PR closes, if any
plan = m.group(1) if m else (f"notes/plans/{issue}.md" if issue else None)
if not plan or not os.path.exists(plan):
    print(f"::error::Agent PR has no approved plan on main (looked for {plan})")
    sys.exit(1)

allowed, in_files = [], False
for line in Path(plan).read_text(encoding="utf-8").splitlines():
    if line.startswith("## "):
        in_files = line.strip().lower() == "## files to change"
        continue
    f = re.match(r"\s*-\s*`([^`]+)`", line) if in_files else None
    if f:
        allowed.append(f.group(1))
allowed.append("plans/*-progress.md")  # progress updates are always fine

# The plan is read from main, so an agent editing it in its PR changes nothing here,
# and the edit itself is out of scope unless the plan lists it.
out = [c for c in changed if not any(fnmatch.fnmatch(c, a) for a in allowed)]
for c in out:
    print(f"::error file={c}::{c} is not in the approved plan {plan}")
print(f"{len(changed) - len(out)}/{len(changed)} changed files are inside {plan}")
sys.exit(1 if out else 0)
