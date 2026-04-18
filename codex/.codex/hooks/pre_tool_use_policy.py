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

WARN_PATTERNS = [
    (r"\bnpm\s+publish\b", "Publishing from Codex should require an explicit human decision."),
    (r"\bpnpm\s+publish\b", "Publishing from Codex should require an explicit human decision."),
]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    command = ((payload.get("tool_input") or {}).get("command")) or ""

    for pattern, reason in DENY_PATTERNS:
        if re.search(pattern, command):
            json.dump(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": reason,
                    },
                    "systemMessage": f"Blocked by repo hook: {reason}",
                },
                sys.stdout,
            )
            return 0

    warnings = [reason for pattern, reason in WARN_PATTERNS if re.search(pattern, command)]
    if warnings:
        json.dump(
            {
                "systemMessage": " ".join(warnings),
            },
            sys.stdout,
        )
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
