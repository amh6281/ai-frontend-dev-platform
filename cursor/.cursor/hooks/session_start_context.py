#!/usr/bin/env python3

import json
import sys


# Cursor's beforeSubmitPrompt hook cannot inject context, so the per-prompt
# guidance the Claude and Codex hooks add there is folded in here instead.
PROMPT_GUIDANCE = (
    "When a request asks for code changes, work from concrete file paths, expected behavior, "
    "and verification goals."
)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    roots = payload.get("workspace_roots") or []
    workspace_hint = roots[0] if roots else "."
    composer_mode = payload.get("composer_mode") or "agent"

    context = (
        "This repository uses a split workspace layout. Treat `cursor/` as the Cursor "
        "working root, load rules from `cursor/.cursor/rules/`, and load commands from "
        "`cursor/.cursor/commands/`. When reporting completion, include changed files and the "
        "verification status or explicitly say it was not run."
    )

    if composer_mode != "agent":
        context += f" This session runs in {composer_mode} mode, so do not assume edits are applied."

    result = {
        "additional_context": f"{context} {PROMPT_GUIDANCE} Workspace root: {workspace_hint}."
    }
    json.dump(result, sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
