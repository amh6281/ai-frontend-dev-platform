# Codex Workspace

이 디렉터리는 Codex용 작업 루트입니다.
Codex 관련 규칙, 서브에이전트 설정, 참고 문서는 이 폴더 안에서 관리합니다.

## 구조

```txt
codex/
├── README.md
├── AGENTS.md
├── AGENTS.kr.md
└── .codex/
    ├── config.toml
    ├── coding-rules.md
    ├── rules/
    │   └── default.rules
    └── agents/
        ├── designer.toml
        ├── frontend-engineer.toml
        ├── planner.toml
        └── reviewer.toml
```

## 역할

- `AGENTS.md`: Codex가 실제로 참조하는 기본 작업 규칙
- `AGENTS.kr.md`: 사람이 읽기 위한 한국어 참고 문서
- `.codex/config.toml`: Codex 공통 설정
- `.codex/agents/*.toml`: 역할별 서브에이전트 정의
- `.codex/rules/default.rules`: 기본 규칙
- `.codex/coding-rules.md`: 레거시 참고 문서

## 사용 기준

- Codex는 이 폴더를 하나의 작업 루트처럼 사용합니다.
- 공통 작업 원칙은 `AGENTS.md`를 기준으로 읽습니다.
- 추가 설정이 필요하면 `.codex/` 안에서 찾습니다.
- 역할별 에이전트 동작은 `.codex/agents/` 아래 파일로 관리합니다.

## 관리 원칙

- Codex 전용 문서는 이 폴더 안에서만 관리합니다.
- 저장소 전체 개요는 상위 루트 `README.md`에서 설명합니다.
- Cursor 전용 설정은 `../cursor/`에서 별도로 관리합니다.
