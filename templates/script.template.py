#!/usr/bin/env python3
"""
[Script name] - one line on what deterministic job this does.

Why this is a script and not prose: this work is exact and repetitive, so
encoding it once here is more reliable and cheaper than having the AI redo
the reasoning on every run.

Contract:
  Input:  [what it takes - args, stdin, a file path. Be specific.]
  Output: [what it produces - stdout, a file, an exit code. Be specific.]

Dependencies:
  [list anything beyond the standard library, or "none"]

Fallback for AIs that cannot run code:
  [In one line, point back to where the equivalent logic is described in
  prose in SKILL.md or a reference, so a chat-only AI is not blocked.]
"""

import sys


def main(argv):
    # [Do the one job. Keep inputs and outputs clear and boring.]
    # Read input:
    # ...
    # Transform:
    # ...
    # Emit output:
    # ...
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
