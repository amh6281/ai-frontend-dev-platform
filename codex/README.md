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
    ├── hooks.json
    ├── hooks/
    │   ├── pre_tool_use_policy.py
    │   ├── session_start_context.py
    │   ├── stop_quality_gate.py
    │   └── user_prompt_submit_guard.py
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
- `.codex/hooks.json`: Codex lifecycle hook 설정
- `.codex/hooks/*.py`: hook event에 연결된 실행 스크립트
- `.codex/agents/*.toml`: 역할별 서브에이전트 정의
- `.codex/rules/default.rules`: 기본 규칙
- `.codex/coding-rules.md`: 레거시 참고 문서

## 사용 기준

- Codex는 이 폴더를 하나의 작업 루트처럼 사용합니다.
- 공통 작업 원칙은 이 폴더의 `AGENTS.md`를 기준으로 읽습니다.
- 추가 설정이 필요하면 `.codex/` 안에서 찾습니다.
- 역할별 에이전트 동작은 `.codex/agents/` 아래 파일로 관리합니다.

## AGENTS.md Discovery

Codex는 작업을 시작하기 전에 `AGENTS.md` 체인을 구성합니다.
이 작업 공간에서는 공식 discovery 규칙에 따라 상위 디렉터리에서 현재 디렉터리까지 순서대로 문서를 읽습니다.

### 현재 프로젝트에서의 로드 순서

1. `codex/AGENTS.md`

Codex를 `codex/` 작업 공간 기준으로 시작하면 이 파일이 기본 instruction chain이 됩니다.
즉, 이 프로젝트에서는 저장소 최상단이 아니라 `codex/` 디렉터리 자체를 Codex 루트처럼 운영합니다.

### 우선순위 규칙

- 현재 작업 루트인 `codex/`에서는 `AGENTS.override.md`를 먼저 찾습니다.
- override가 없으면 `AGENTS.md`를 찾습니다.
- 둘 다 없을 때만 `project_doc_fallback_filenames`에 있는 대체 파일명을 확인합니다.
- 같은 디렉터리에서는 최대 한 개의 instruction 파일만 사용됩니다.

### 현재 설정과의 연결

- `.codex/config.toml`의 `project_doc_fallback_filenames = ["TEAM_GUIDE.md", ".agents.md"]`가 fallback 이름을 정의합니다.
- `.codex/config.toml`의 `project_doc_max_bytes = 65536`가 instruction chain 최대 크기를 늘립니다.
- 현재 `codex/` 작업 공간에서는 `AGENTS.md`가 존재하므로 fallback 파일명은 기본적으로 사용되지 않습니다.

### 운영 팁

- Codex 공통 규칙은 `codex/AGENTS.md`에 둡니다.
- Codex 전용 상세 설정은 `.codex/` 아래에 둡니다.
- 더 세분화된 팀 규칙이 필요하면 `codex/` 하위 디렉터리에 `AGENTS.md` 또는 `AGENTS.override.md`를 추가해 레이어를 늘릴 수 있습니다.

## Hooks

Codex hooks는 공식 문서 기준으로 `config.toml`의 feature flag와 `hooks.json`을 함께 사용합니다.

### 현재 기준

- hooks 기능 활성화: `.codex/config.toml`
- repo-local hooks 파일: `.codex/hooks.json`
- 이 저장소에서는 `codex/`가 작업 루트이므로, Codex 관점의 repo-local hooks 경로는 `codex/.codex/hooks.json`입니다.

### 현재 설정

- `.codex/config.toml`에 `[features]` 와 `codex_hooks = true`를 설정했습니다.
- `.codex/hooks.json`에 실제 hook handler를 연결했습니다.
- hook command는 모두 git root 기준으로 `codex/.codex/hooks/*.py`를 실행합니다.

### 지원 이벤트

- `SessionStart`
- `PreToolUse`
- `PostToolUse`
- `UserPromptSubmit`
- `Stop`

### 운영 메모

- 여러 config layer에 있는 `hooks.json`은 함께 로드됩니다.
- repo-local hook 경로는 상대경로보다 git root 기준으로 해석하는 방식이 안전합니다.
- 현재 `PreToolUse`와 `PostToolUse`는 주로 Bash 계열 interception 중심입니다.
- `Stop` hook은 turn 종료를 막는 개념이 아니라 다음 continuation prompt를 만들며 계속 진행시키는 방식입니다.
- Windows에서는 hooks가 비활성화됩니다.

### 현재 포함된 hook

- `session_start_context.py`: 세션 시작 시 `codex/` 작업 루트와 응답 규칙을 추가 컨텍스트로 주입합니다.
- `pre_tool_use_policy.py`: `rm -rf /`, `git reset --hard` 같은 파괴적 Bash 명령을 차단합니다.
- `user_prompt_submit_guard.py`: 프롬프트에 API 키나 private key가 들어오면 차단합니다.
- `stop_quality_gate.py`: 최종 응답에 변경 파일 언급과 검증 상태가 빠지면 한 번 더 보완하도록 continuation을 요청합니다.

### 사용법

Codex hooks는 슬래시 커맨드처럼 직접 실행하는 방식이 아닙니다.
`/hook`, `/run-hook` 같은 별도 명령을 입력할 필요 없이, Codex 세션 흐름 안에서 자동으로 실행됩니다.

#### 어떻게 동작하나

- Codex가 이 작업 루트에서 시작되거나 resume되면 `SessionStart` hook이 자동 실행됩니다.
- 사용자가 프롬프트를 제출하면 `UserPromptSubmit` hook이 자동 실행됩니다.
- Codex가 Bash 계열 명령을 실행하려고 하면 `PreToolUse` hook이 자동 실행됩니다.
- Codex turn이 끝나려 할 때 `Stop` hook이 자동 실행됩니다.

즉, 사용자가 따로 "훅 실행해줘"라고 말해야 하는 구조가 아니라,
해당 이벤트가 발생하면 Codex가 `hooks.json`에 연결된 스크립트를 자동으로 호출합니다.

#### 사용자가 체감하는 방식

- 그냥 평소처럼 Codex에게 작업을 요청하면 됩니다.
- 예를 들어 "이 파일 수정해줘", "테스트 돌려줘", "빌드 에러 확인해줘"처럼 일반 요청을 하면 됩니다.
- 그 과정에서 hook이 백그라운드에서 자동으로 동작합니다.
- 어떤 경우에는 hook이 위험한 명령을 막거나, 응답 보완을 한 번 더 요구할 수 있습니다.

#### 현재 프로젝트 기준 예시

- 세션을 새로 열면 `session_start_context.py`가 작업 루트와 응답 규칙을 추가 컨텍스트로 넣습니다.
- 프롬프트에 API 키가 포함되면 `user_prompt_submit_guard.py`가 요청을 차단할 수 있습니다.
- Codex가 `git reset --hard` 같은 명령을 실행하려 하면 `pre_tool_use_policy.py`가 막습니다.
- 최종 응답에 변경 파일이나 검증 상태가 빠지면 `stop_quality_gate.py`가 한 번 더 보완하도록 유도합니다.

#### 전제 조건

- Codex가 이 저장소의 `codex/` 작업 루트를 기준으로 실행되어야 합니다.
- `.codex/config.toml`에서 `codex_hooks = true`가 켜져 있어야 합니다.
- `.codex/hooks.json`에 이벤트와 스크립트 연결이 정의되어 있어야 합니다.
- 연결된 Python 스크립트를 실행할 수 있는 환경이어야 합니다.

#### 한계

- 현재 hook은 모든 도구를 완전히 가로채는 구조는 아닙니다.
- 공식 문서 기준으로 `PreToolUse`와 `PostToolUse`는 현재 Bash 중심 interception입니다.
- `UserPromptSubmit`과 `Stop`은 matcher를 사실상 사용하지 않습니다.
- Windows에서는 현재 hooks가 비활성화됩니다.

### 예시 형태

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/env python3 \"$(git rev-parse --show-toplevel)/codex/.codex/hooks/pre_tool_use_policy.py\"",
            "statusMessage": "Checking shell safety policy",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

## 관리 원칙

- Codex 전용 문서는 이 폴더 안에서만 관리합니다.
- 저장소 전체 개요는 상위 루트 `README.md`에서 설명합니다.
- Cursor 전용 설정은 `../cursor/`에서 별도로 관리합니다.
