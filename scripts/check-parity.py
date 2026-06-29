#!/usr/bin/env python3
"""Check that rules / commands / agents / hooks stay in sync across the
claude, cursor, and codex workspaces.

Run after editing any platform's config (or wire into pre-commit / CI):

    python3 scripts/check-parity.py

Exits non-zero if a hard-parity dimension drifts. Soft checks (codex embedded
rules, Korean variants) only print warnings and never fail the run.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Naming differs across platforms; fold variants onto one canonical slug.
#   - claude/cursor use "commit"; codex skill dir is "git-commit"
#   - claude agents use hyphens; codex agents use underscores (handled by normalize)
ALIASES = {"git-commit": "commit"}


def normalize(name: str) -> str:
    """Strip extension, lowercase, unify separators, apply aliases."""
    stem = name.rsplit(".", 1)[0] if "." in name else name
    slug = stem.lower().replace("_", "-")
    return ALIASES.get(slug, slug)


def slugs_from_files(dir_path: Path, suffix: str) -> set[str]:
    if not dir_path.is_dir():
        return set()
    return {normalize(p.name) for p in dir_path.glob(f"*{suffix}")}


def slugs_from_dirs(dir_path: Path) -> set[str]:
    if not dir_path.is_dir():
        return set()
    return {normalize(p.name) for p in dir_path.iterdir() if p.is_dir()}


# --- result tracking -------------------------------------------------------

failures = 0


def report(dimension: str, sets: dict[str, set[str]]) -> None:
    """Hard check: every platform must expose the same canonical slug set."""
    global failures
    union = set().union(*sets.values())
    drift = False
    for slug in sorted(union):
        missing = [plat for plat, s in sets.items() if slug not in s]
        if missing:
            drift = True
            print(f"  [DRIFT] {dimension}: '{slug}' missing in {', '.join(missing)}")
    if drift:
        failures += 1
    else:
        present = ", ".join(f"{p}={len(s)}" for p, s in sets.items())
        print(f"  [OK]    {dimension}: {len(union)} in sync ({present})")


def warn(message: str) -> None:
    print(f"  [WARN]  {message}")


# --- dimensions ------------------------------------------------------------

print("== Parity check ==\n")

# 1) Rules — claude & cursor are file-based and must match exactly.
print("rules (claude <-> cursor):")
claude_rules = slugs_from_files(ROOT / "claude/.claude/rules", ".md")
cursor_rules = slugs_from_files(ROOT / "cursor/.cursor/rules", ".mdc")
report("rules", {"claude": claude_rules, "cursor": cursor_rules})

# codex folds rules into AGENTS.md; verify each canonical rule has coverage.
agents_md = (ROOT / "codex/AGENTS.md").read_text(encoding="utf-8")
CODEX_RULE_PATTERNS = {
    "accessibility": r"## Accessibility",
    "code-quality": r"## Implementation Standards",
    "fsd-architecture": r"## Feature-Sliced Design",
    "karpathy-guidelines": r"smallest defensible change",
    "react": r"## React",
    "security": r"## Security",
    "testing": r"## Verification",
    "typescript": r"## TypeScript",
}
for slug in sorted(claude_rules):
    pattern = CODEX_RULE_PATTERNS.get(slug)
    if pattern is None:
        warn(f"rules: '{slug}' has no codex AGENTS.md coverage mapping")
    elif not re.search(pattern, agents_md):
        warn(f"rules: '{slug}' not found in codex AGENTS.md (pattern /{pattern}/)")

# 2) Commands / skills — must exist in all three.
print("\ncommands (claude <-> cursor <-> codex):")
report(
    "commands",
    {
        "claude": slugs_from_files(ROOT / "claude/.claude/commands", ".md"),
        "cursor": slugs_from_files(ROOT / "cursor/.cursor/commands", ".md"),
        "codex": slugs_from_dirs(ROOT / "codex/.agents/skills"),
    },
)

# 3) Agents — claude & codex (cursor has no agents by design).
print("\nagents (claude <-> codex):")
report(
    "agents",
    {
        "claude": slugs_from_files(ROOT / "claude/.claude/agents", ".md"),
        "codex": slugs_from_files(ROOT / "codex/.codex/agents", ".toml"),
    },
)

# 4) Hooks — claude & codex.
print("\nhooks (claude <-> codex):")
report(
    "hooks",
    {
        "claude": slugs_from_files(ROOT / "claude/.claude/hooks", ".py"),
        "codex": slugs_from_files(ROOT / "codex/.codex/hooks", ".py"),
    },
)

# 5) Korean variants — codex completeness (soft).
print("\nkorean variants (codex, soft):")
if not (ROOT / "codex/AGENTS.kr.md").is_file():
    warn("codex/AGENTS.kr.md is missing")
for skill_dir in sorted((ROOT / "codex/.agents/skills").glob("*/")):
    if (skill_dir / "SKILL.md").is_file() and not (skill_dir / "SKILL.kr.md").is_file():
        warn(f"codex skill '{skill_dir.name}' has SKILL.md but no SKILL.kr.md")
print("  [OK]    korean variant scan complete")

# --- verdict ---------------------------------------------------------------

print()
if failures:
    print(f"FAILED: {failures} dimension(s) drifted.")
    sys.exit(1)
print("PASS: all hard-parity dimensions in sync.")
