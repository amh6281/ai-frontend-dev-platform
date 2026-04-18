#!/usr/bin/env python3

import json
import re
import sys


VERIFICATION_HINTS = [
    "verify",
    "verification",
    "verified",
    "test",
    "tests",
    "lint",
    "build",
    "검증",
    "테스트",
    "실행하지 못",
    "실행 못",
    "run tests",
    "not run",
]


def has_verification_summary(message: str) -> bool:
    lowered = message.lower()
    return any(hint in lowered for hint in VERIFICATION_HINTS)


def mentions_changed_files(message: str) -> bool:
    return bool(re.search(r"`[^`]+`", message) or re.search(r"\[[^\]]+\]\(/", message))


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    if payload.get("stop_hook_active"):
        json.dump({"continue": True}, sys.stdout)
        return 0

    last_message = payload.get("last_assistant_message") or ""
    missing_verification = not has_verification_summary(last_message)
    missing_file_refs = not mentions_changed_files(last_message)

    if not missing_verification and not missing_file_refs:
        json.dump({"continue": True}, sys.stdout)
        return 0

    follow_up_parts = []
    if missing_file_refs:
        follow_up_parts.append("Mention the key changed file or path in the final response.")
    if missing_verification:
        follow_up_parts.append("State what you verified, or explicitly say verification was not run.")

    json.dump(
        {
            "decision": "block",
            "reason": " ".join(follow_up_parts),
        },
        sys.stdout,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
