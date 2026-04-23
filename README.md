# ai-frontend-dev-platform

![Codex](https://img.shields.io/badge/Codex-supported-black) ![Cursor](https://img.shields.io/badge/Cursor-supported-black)

AI 에이전트별 작업 규칙과 실행 문서를 한 저장소에서 관리하는 플랫폼입니다.  
각 도구는 자신의 작업 루트 안에서만 설정을 찾으며, 서로의 규칙에 영향을 주지 않습니다.

> Codex를 쓴다면 `codex/`만 보면 됩니다. Cursor를 쓴다면 `cursor/`만 보면 됩니다.

---

## 왜 이런 구조인가

Codex와 Cursor는 각각 저장소 루트에서 설정 파일을 탐색합니다. 두 도구를 같은 저장소에서 함께 쓰면 서로의 설정이 충돌하거나 의도치 않게 읽힐 수 있습니다. 이 저장소는 각 도구의 작업 루트를 분리해 이 문제를 해결합니다.

- 저장소 루트는 전체 개요 전용 — 도구별 설정을 두지 않습니다
- 각 도구는 자신의 하위 디렉터리를 프로젝트 루트처럼 사용합니다
- 도구를 추가할 때 다른 디렉터리를 건드리지 않아도 됩니다

---

## 저장소 구조

```
.
├── README.md
├── codex/          ← Codex 작업 루트
│   ├── AGENTS.md
│   ├── AGENTS.kr.md
│   ├── .agents/
│   │   └── skills/
│   └── .codex/
│       ├── config.toml
│       ├── hooks.json
│       ├── hooks/
│       ├── coding-rules.md
│       ├── rules/
│       └── agents/
│           ├── designer.toml
│           ├── frontend-engineer.toml
│           ├── performance_reviewer.toml
│           ├── planner.toml
│           └── reviewer.toml
└── cursor/         ← Cursor 작업 루트
    └── .cursor/
        ├── commands/
        └── rules/
```

---

## 각 도구 안내

### Codex

| 경로 | 역할 |
|------|------|
| `codex/AGENTS.md` | Codex 작업 기본 규칙 (영문, 에이전트가 읽음) |
| `codex/AGENTS.kr.md` | 사람이 읽는 한국어 참고본 |
| `codex/.agents/skills/` | 저장소 로컬 Codex skill |
| `codex/.codex/config.toml` | 공통 설정 및 fallback 파일명 지정 |
| `codex/.codex/hooks.json` | hook 연결 설정 |
| `codex/.codex/agents/*.toml` | 역할별 custom agent 정의 |
| `codex/.codex/rules/default.rules` | 기본 규칙 |

같은 디렉터리에 `AGENTS.override.md`가 있으면 `AGENTS.md`보다 우선합니다.  
대체 파일명(`TEAM_GUIDE.md` 등)은 `config.toml`의 fallback 설정이 있을 때만 동작합니다.

### Cursor

| 경로 | 역할 |
|------|------|
| `cursor/.cursor/commands/*.md` | commit, review, refactor 등 command 문서 |
| `cursor/.cursor/rules/code-quality.mdc` | 코드 품질 규칙 |
| `cursor/.cursor/rules/typescript.mdc` | TypeScript 규칙 |

---

## 운영 원칙

- 저장소 루트에는 도구별 설정 파일을 두지 않습니다
- 새 도구를 추가할 때는 동일한 패턴으로 최상위에 디렉터리를 만들고 그 안에서 독립적으로 구성합니다
- Codex 규칙과 Cursor 규칙은 서로를 참조하지 않습니다

---

## 기여

규칙이나 설정을 수정할 때는 해당 도구의 작업 루트 안에서만 변경하세요.  
저장소 루트나 다른 도구의 디렉터리는 건드리지 않아도 됩니다.
