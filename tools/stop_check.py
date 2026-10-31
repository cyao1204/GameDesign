"""Claude Code Stop hook: warn (never block) when the working tree has uncommitted changes.

CLAUDE.md asks for GDD changes to be committed as we go; this makes a forgotten commit visible
at the end of every turn. Silent when the tree is clean.
"""

from __future__ import annotations

import json
import subprocess
import sys


def dirty_paths() -> list[str]:
    """Paths git reports as changed or untracked. Empty if git can't be run."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True, check=True, timeout=20
        )
    except (OSError, subprocess.SubprocessError) as error:
        print(json.dumps({"systemMessage": f"stop_check: could not run git status ({error})"}))
        return []
    return [line[3:] for line in result.stdout.splitlines() if line.strip()]


def main() -> int:
    paths = dirty_paths()
    if paths:
        listed = ", ".join(paths[:10]) + (" …" if len(paths) > 10 else "")
        message = f"WARNING: {len(paths)} uncommitted path(s): {listed}. Commit before ending the session."
        print(json.dumps({"systemMessage": message}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
