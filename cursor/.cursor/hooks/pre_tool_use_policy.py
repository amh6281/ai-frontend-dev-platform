#!/usr/bin/env python3

import json
import re
import sys


DENY_PATTERNS = [
    (r"\brm\s+-rf\s+/", "Refusing recursive deletion against root-like paths."),
    (r"\bsudo\s+rm\b", "Refusing privileged file deletion."),
    (r"\bgit\s+reset\s+--hard\b", "Refusing destructive git reset."),
    (r"\bgit\s+checkout\s+--\b", "Refusing destructive checkout of tracked files."),
    (r"\bmkfs\b", "Refusing disk-formatting command."),
    (r"\bdd\s+if=.*of=/dev/", "Refusing raw device write command."),
]

# Cursor has no warn-only channel, so publish commands escalate to a user prompt.
ASK_PATTERNS = [
    (r"\bnpm\s+publish\b", "Publishing from Cursor should require an explicit human decision."),
    (r"\bpnpm\s+publish\b", "Publishing from Cursor should require an explicit human decision."),
]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    command = payload.get("command") or ""

    for pattern, reason in DENY_PATTERNS:
        if re.search(pattern, command):
            json.dump(
                {
                    "permission": "deny",
                    "user_message": f"Blocked by repo hook: {reason}",
                    "agent_message": reason,
                },
                sys.stdout,
            )
            return 0

    for pattern, reason in ASK_PATTERNS:
        if re.search(pattern, command):
            json.dump(
                {
                    "permission": "ask",
                    "user_message": reason,
                    "agent_message": reason,
                },
                sys.stdout,
            )
            return 0

    # No opinion. Returning "allow" here would override Cursor's own approval
    # settings for every command the hook does not care about.
    json.dump({}, sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
