#!/usr/bin/env python3

import json
import re
import sys


SECRET_PATTERNS = [
    (r"sk-[A-Za-z0-9]{20,}", "Possible OpenAI-style API key detected."),
    (r"ghp_[A-Za-z0-9]{20,}", "Possible GitHub personal access token detected."),
    (r"AIza[0-9A-Za-z\-_]{20,}", "Possible Google API key detected."),
    (r"-----BEGIN (RSA|EC|OPENSSH|DSA|PGP) PRIVATE KEY-----", "Private key material detected."),
]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    prompt = payload.get("prompt") or ""

    for pattern, reason in SECRET_PATTERNS:
        if re.search(pattern, prompt):
            json.dump(
                {
                    "decision": "block",
                    "reason": f"{reason} Remove secrets from the prompt before continuing.",
                },
                sys.stdout,
            )
            return 0

    guidance = (
        "Prefer concrete file paths, expected behavior, and verification goals when the request "
        "asks for code changes."
    )
    json.dump(
        {
            "continue": True,
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": guidance,
            },
        },
        sys.stdout,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
