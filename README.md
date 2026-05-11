# ai-frontend-dev-platform

![Codex](https://img.shields.io/badge/Codex-supported-black) ![Cursor](https://img.shields.io/badge/Cursor-supported-black)

AI 에이전트별 작업 규칙과 실행 문서를 한 저장소에서 관리하는 플랫폼입니다.  
각 도구는 자신의 작업 루트 안에서 설정이 독립적으로 닫히도록 구성합니다.

> Codex를 쓴다면 `codex/`만 보면 됩니다. Cursor를 쓴다면 `cursor/`만 보면 됩니다.

---

## 왜 이런 구조인가

Codex와 Cursor는 각각 설정 파일을 탐색하는 방식이 다릅니다. 두 도구를 같은 저장소에서 함께 쓰면 서로의 설정이 섞이거나 의도치 않게 읽힐 수 있습니다.
이 저장소는 각 도구의 작업 루트를 분리해 그 문제를 줄입니다.

- 저장소 루트는 전체 개요만 설명합니다.
- 각 도구는 자신의 하위 디렉터리를 프로젝트 루트처럼 사용합니다.
- Codex 설정은 `codex/`, Cursor 설정은 `cursor/` 안에서만 관리합니다.

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
└── cursor/         # Cursor 작업 루트
    └── .cursor/
        ├── commands/
        └── rules/
```

---

## Codex

| 경로                               | 역할                         |
| ---------------------------------- | ---------------------------- |
| `codex/AGENTS.md`                  | 기본 작업 규칙               |
| `codex/AGENTS.kr.md`               | 한국어 참고본 (사람용)       |
| `codex/.agents/skills/`            | Repo-local skills            |
| `codex/.agents/skills/workspace-doc-sync/` | 문서 구조 동기화 skill |
| `codex/.codex/config.toml`         | 공통 설정 및 fallback 파일명 |
| `codex/.codex/hooks.json`          | Hook 연결 설정               |
| `codex/.codex/agents/*.toml`       | 역할별 custom agent 정의     |
| `codex/.codex/rules/default.rules` | 기본 규칙                    |

**AGENTS.md 로딩 우선순위:** `AGENTS.override.md` → `AGENTS.md` → `config.toml`의 fallback 파일명

**Custom agent 표기:** agent 호출 이름은 TOML의 `name` 값을 기준으로 하며, 파일명은 kebab-case 또는 snake_case일 수 있습니다.

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
