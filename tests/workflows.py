"""Print what is wrong with the shared workflows; exit 1 if anything is.

Every file in .github/workflows except self.yml must be callable
(`workflow_call`), and self.yml must call each one, so none of them
ships untested. Standard library only, so it reads the YAML as text.

Usage: python3 tests/workflows.py [ROOT]
"""
import os
import re
import sys

SELF = "self.yml"


def problems(root):
    workflows = os.path.join(root, ".github", "workflows")
    names = sorted(n for n in os.listdir(workflows) if n.endswith((".yml", ".yaml")))
    if SELF not in names:
        yield f"{SELF} is missing"
        return
    with open(os.path.join(workflows, SELF)) as f:
        called = set(re.findall(r"^\s*uses:\s*\./\.github/workflows/(\S+)\s*$", f.read(), re.M))
    for name in names:
        if name == SELF:
            continue
        with open(os.path.join(workflows, name)) as f:
            text = f.read()
        if not re.search(r"^  workflow_call:", text, re.M):
            yield f"{name}: not callable (no workflow_call trigger)"
        if name not in called:
            yield f"{name}: not called by {SELF}, so nothing tests it"
    for name in sorted(called - set(names)):
        yield f"{SELF} calls {name}, which doesn't exist"


if __name__ == "__main__":
    found = list(problems(sys.argv[1] if len(sys.argv) > 1 else "."))
    print("\n".join(found))
    sys.exit(1 if found else 0)
