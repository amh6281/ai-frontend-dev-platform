# ai-frontend-dev-platform

![Codex](https://img.shields.io/badge/Codex-supported-black) ![Claude](https://img.shields.io/badge/Claude-supported-black) ![Cursor](https://img.shields.io/badge/Cursor-supported-black)

AI 에이전트별 작업 규칙과 실행 문서를 한 저장소에서 관리하는 플랫폼입니다.  
각 도구는 자신의 작업 루트 안에서 설정이 독립적으로 닫히도록 구성합니다.

> Codex를 쓴다면 `codex/`만 보면 됩니다. Claude를 쓴다면 `claude/`만 보면 됩니다. Cursor를 쓴다면 `cursor/`만 보면 됩니다.

---

## 왜 이런 구조인가

Codex, Claude, Cursor는 각각 설정 파일을 탐색하는 방식이 다릅니다. 여러 도구를 같은 저장소에서 함께 쓰면 서로의 설정이 섞이거나 의도치 않게 읽힐 수 있습니다.
이 저장소는 각 도구의 작업 루트를 분리해 그 문제를 줄입니다.

- 저장소 루트는 전체 개요만 설명합니다.
- 각 도구는 자신의 하위 디렉터리를 프로젝트 루트처럼 사용합니다.
- Codex 설정은 `codex/`, Claude 설정은 `claude/`, Cursor 설정은 `cursor/` 안에서만 관리합니다.

---

## 저장소 구조

```
.
├── README.md
├── codex/          # Codex 작업 루트
│   ├── AGENTS.md
│   ├── AGENTS.kr.md
│   ├── .agents/
│   │   └── skills/
│   └── .codex/
│       ├── config.toml
│       ├── hooks.json
│       ├── hooks/
│       ├── rules/
│       └── agents/
├── claude/         # Claude 작업 루트
│   ├── .claude/
│   │   ├── agents/
│   │   ├── commands/
│   │   ├── rules/
│   │   ├── hooks/
│   │   └── settings.json
│   ├── CLAUDE.md
│   └── README.md
└── cursor/         # Cursor 작업 루트
    └── .cursor/
        ├── commands/
        └── rules/
```

---

## 빠른 시작

사용할 AI 도구의 폴더로 이동한 뒤, 그 폴더를 작업 루트처럼 열어 사용합니다.

| 도구   | 시작 위치 | 먼저 볼 문서           | 수정이 필요한 경우                    |
| ------ | --------- | ---------------------- | ------------------------------------- |
| Codex  | `codex/`  | `codex/README.md`      | `codex/AGENTS.md`, `codex/.codex/`    |
| Claude | `claude/` | `claude/README.md`     | `claude/CLAUDE.md`, `claude/.claude/commands/`, `claude/.claude/rules/`, `claude/.claude/agents/`, `claude/.claude/hooks/`, `claude/.claude/settings.json` |
| Cursor | `cursor/` | `cursor/README.md`     | `cursor/.cursor/commands/`, `cursor/.cursor/rules/` |

예를 들어 Codex 규칙을 바꿀 때는 `codex/` 안의 문서와 설정만 수정하고, Claude rule을 바꿀 때는 `claude/` 안의 문서와 설정만 수정합니다. Cursor command를 바꿀 때는 `cursor/` 안의 문서와 설정만 수정합니다.

---

## Codex

| 경로                               | 역할                         |
| ---------------------------------- | ---------------------------- |
| `codex/AGENTS.md`                  | 기본 작업 규칙               |
| `codex/AGENTS.kr.md`               | 한국어 참고본 (사람용)       |
| `codex/.agents/skills/`            | Repo-local skills (`git-commit`, `create-pr`, `create-pr-kr`, `sync-pr`, `review`, `refactor`, `verify`, `workspace-doc-sync`) |
| `codex/.codex/config.toml`         | 공통 설정 및 fallback 파일명 |
| `codex/.codex/hooks.json`          | Hook 연결 설정               |
| `codex/.codex/agents/*.toml`       | 역할별 custom agent 정의     |
| `codex/.codex/rules/default.rules` | 기본 규칙                    |

**AGENTS.md 로딩 우선순위:** `AGENTS.override.md` → `AGENTS.md` → `config.toml`의 fallback 파일명

**Custom agent 표기:** agent 호출 이름과 TOML 파일명은 snake_case로 맞춥니다.

---

## Claude

| 경로                         | 역할                 |
| ---------------------------- | -------------------- |
| `claude/CLAUDE.md`           | 기본 작업 규칙       |
| `claude/.claude/commands/*.md` | Claude command 문서 |
| `claude/.claude/rules/*.md`  | Claude 세부 rule 문서 |
| `claude/.claude/agents/*.md` | 역할별 Claude subagent 정의 |
| `claude/.claude/settings.json` | Claude 설정 및 lifecycle hook 연결 |
| `claude/.claude/hooks/*.py`  | lifecycle hook 실행 스크립트 |
| `claude/README.md`           | Claude 작업 루트 안내 |

**CLAUDE.md 로딩:** Claude Code는 프로젝트 지침으로 `CLAUDE.md`를 사용합니다. 이 저장소에서는 Claude 작업 루트를 `claude/`로 분리합니다.

**Hooks:** Codex의 lifecycle hook 4종(SessionStart, PreToolUse, UserPromptSubmit, Stop)을 동일한 이벤트 스키마로 `claude/.claude/hooks/`에 옮기고 `claude/.claude/settings.json`에 연결합니다. 동작하는 `python3`가 필요합니다.

---

## Cursor

| 경로                           | 역할                |
| ------------------------------ | ------------------- |
| `cursor/.cursor/commands/*.md` | Cursor command 문서 |
| `cursor/.cursor/rules/*.mdc`   | Cursor rule 문서    |

---

## 운영 원칙

- 저장소 루트에는 도구별 설정 파일을 두지 않습니다.
- 새 도구를 추가할 때는 동일한 패턴으로 최상위에 디렉터리를 만들고 그 안에서 독립적으로 구성합니다.
- Codex 규칙과 Cursor 규칙은 서로를 참조하지 않습니다.

---

## 동기화 검증

세 워크스페이스(claude/cursor/codex)의 rules·commands·agents·hooks 가 어긋나지 않았는지 검사합니다.
규칙·커맨드·에이전트를 추가하거나 수정한 뒤 실행하세요.

```bash
python3 scripts/check-parity.py
```

- 어느 한 플랫폼에서 항목이 빠지면 `[DRIFT]` 를 출력하고 비정상 종료(exit 1)합니다.
- codex의 임베드된 규칙(`AGENTS.md`)과 한국어판(`*.kr.md`) 누락은 `[WARN]` 으로만 알립니다.
