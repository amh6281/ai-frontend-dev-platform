# ai-frontend-dev-platform

AI 에이전트별 작업 규칙과 실행 문서를 한 저장소에서 관리하는 플랫폼입니다.
이제 숨김 설정 폴더를 저장소 루트에 두지 않고, 각 도구 전용 작업 루트 안으로 옮겼습니다.

## 현재 구조

```txt
.
├── README.md
├── codex/
│   ├── AGENTS.md
│   ├── AGENTS.kr.md
│   └── .codex/
└── cursor/
    └── .cursor/
```

- `codex/`는 Codex가 작업할 때 기준이 되는 루트입니다.
- `cursor/`는 Cursor가 작업할 때 기준이 되는 루트입니다.
- 각 도구는 자신의 작업 루트 안에 있는 숨김 설정 폴더를 기준으로 필요한 문서를 찾습니다.
- Codex와 Cursor 모두 저장소 최상단이 아니라 각자의 작업 루트 안에서 instruction과 설정이 닫히도록 구성합니다.

## Codex

Codex 관련 문서는 `codex/` 아래에 모여 있습니다.

### Codex가 보는 기준 경로

- 작업 루트: `codex/`
- 기본 instruction 문서: `codex/AGENTS.md`
- 한국어 참고 문서: `codex/AGENTS.kr.md`
- 추가 설정 및 에이전트 정의: `codex/.codex/`

### AGENTS.md 로딩 방식

- 이 프로젝트에서는 `codex/` 디렉터리 자체를 Codex 루트처럼 운영합니다.
- 따라서 Codex 관련 instruction discovery도 `codex/` 작업 루트 기준으로 설명합니다.
- 같은 디렉터리에 `AGENTS.override.md`가 있으면 일반 `AGENTS.md`보다 우선합니다.
- `TEAM_GUIDE.md`, `.agents.md` 같은 대체 파일명은 `codex/.codex/config.toml`의 fallback 설정이 있을 때만 사용됩니다.

### 구조

```txt
codex/
├── AGENTS.md
├── AGENTS.kr.md
└── .codex/
    ├── config.toml
    ├── hooks.json
    ├── hooks/
    ├── coding-rules.md
    ├── rules/
    │   └── default.rules
    └── agents/
        ├── designer.toml
        ├── frontend-engineer.toml
        ├── planner.toml
        └── reviewer.toml
```

### 역할

- `codex/AGENTS.md`: Codex 작업 공간 기본 규칙
- `codex/AGENTS.kr.md`: 사람이 읽기 위한 한국어 참고본
- `codex/.codex/config.toml`: Codex 공통 설정과 fallback filename 설정
- `codex/.codex/hooks.json`: Codex hook 연결 설정
- `codex/.codex/agents/*.toml`: 역할별 서브에이전트 정의
- `codex/.codex/rules/default.rules`: 기본 규칙

즉, Codex 관점에서는 저장소 루트가 아니라 `codex/`가 실질적인 프로젝트 루트처럼 동작합니다.
세부적인 hooks, agents, rules 설정은 `codex/.codex` 안에서 찾도록 구성되어 있습니다.

## Cursor

Cursor 관련 문서는 `cursor/` 아래에 모여 있습니다.

### Cursor가 보는 기준 경로

- 작업 루트: `cursor/`
- commands: `cursor/.cursor/commands/`
- rules: `cursor/.cursor/rules/`

### 구조

```txt
cursor/
└── .cursor/
    ├── commands/
    │   ├── commit.md
    │   ├── create-pr.md
    │   ├── create-pr-kr.md
    │   ├── refactor.md
    │   ├── review.md
    │   ├── sync-pr.md
    │   └── verify.md
    └── rules/
        ├── code-quality.mdc
        └── typescript.mdc
```

### 역할

- `.cursor/commands/*.md`: Cursor command 문서
- `.cursor/rules/*.mdc`: Cursor rule 문서

Cursor도 동일하게 저장소 루트가 아니라 `cursor/`를 자기 작업 루트처럼 사용하고,
필요한 설정은 `cursor/.cursor` 안에서 찾는 구조입니다.

## 운영 원칙

- 저장소 루트는 전체 개요를 설명하는 공간입니다.
- Codex 전용 규칙은 `codex/` 아래에서 관리합니다.
- Cursor 전용 규칙은 `cursor/` 아래에서 관리합니다.
- 도구별 설정을 섞지 않고, 각 작업 루트 안에서 독립적으로 유지합니다.
