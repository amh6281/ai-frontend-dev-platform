#!/usr/bin/env python3

import json
import re
import sys
from pathlib import Path


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


def record_text(record: dict) -> str:
    """Pull assistant text out of a transcript record, tolerating shape differences."""
    if record.get("role") != "assistant" and record.get("type") != "assistant":
        return ""
    content = record.get("content")
    if content is None:
        content = (record.get("message") or {}).get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(part.get("text", "") for part in content if isinstance(part, dict))
    return ""


def last_assistant_message(transcript_path: str) -> str:
    """Best-effort read of the last assistant turn.

    Cursor documents `transcript_path` but not the file format, so every parse
    failure degrades to an empty string and the gate stays silent.
    """
    try:
        raw = Path(transcript_path).read_text(encoding="utf-8")
    except OSError:
        return ""

    records = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            records = []
            break
        if isinstance(parsed, dict):
            records.append(parsed)

    if not records:
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            return ""
        if isinstance(parsed, dict):
            parsed = parsed.get("messages") or []
        if isinstance(parsed, list):
            records = [item for item in parsed if isinstance(item, dict)]

    for record in reversed(records):
        text = record_text(record)
        if text:
            return text
    return ""


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    if payload.get("status") != "completed" or payload.get("loop_count", 0) > 0:
        json.dump({}, sys.stdout)
        return 0

    message = last_assistant_message(payload.get("transcript_path") or "")
    if not message:
        json.dump({}, sys.stdout)
        return 0

    follow_up_parts = []
    if not mentions_changed_files(message):
        follow_up_parts.append("Mention the key changed file or path in the final response.")
    if not has_verification_summary(message):
        follow_up_parts.append("State what you verified, or explicitly say verification was not run.")

    if not follow_up_parts:
        json.dump({}, sys.stdout)
        return 0

    json.dump({"followup_message": " ".join(follow_up_parts)}, sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
