#!/usr/bin/env python3

import json
import os
import sys


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    cwd = payload.get("cwd") or ""
    source = payload.get("source") or "startup"
    workspace_hint = os.path.relpath(cwd, os.getcwd()) if cwd else "."

    context = (
        "This repository uses a split workspace layout. Treat `codex/` as the Codex "
        "working root, load instructions from `codex/AGENTS.md`, and load extra settings "
        "from `codex/.codex/`. When reporting completion, include changed files and the "
        "verification status or explicitly say it was not run."
    )

    if source == "resume":
        context += " This is a resumed session, so re-check the current files before editing."

    result = {
        "continue": True,
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": f"{context} Session cwd: {workspace_hint}."
        }
    }
    json.dump(result, sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
