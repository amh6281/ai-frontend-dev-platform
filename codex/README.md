# Codex Workspace

이 디렉터리는 Codex용 작업 루트입니다.
Codex 관련 규칙, 서브에이전트 설정, 참고 문서는 이 폴더 안에서 관리합니다.

## 구조

```txt
codex/
├── README.md
├── AGENTS.md
├── AGENTS.kr.md
├── .agents/
│   └── skills/
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
- `.agents/skills/`: repo-local Codex skill 위치
- `.codex/config.toml`: Codex 공통 설정
- `.codex/hooks.json`: Codex lifecycle hook 설정
- `.codex/hooks/*.py`: hook event에 연결된 실행 스크립트
- `.codex/agents/*.toml`: 역할별 custom agent 정의
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

## Subagents

Codex는 subagent workflow를 통해 여러 작업을 병렬로 나눠 실행할 수 있습니다.
이 작업 공간에서는 `.codex/agents/*.toml` 파일을 사용해 custom agent를 정의하고, 필요할 때 명시적으로 spawn해서 사용합니다.

### 현재 기준

- global subagent 설정: `.codex/config.toml`의 `[agents]`
- project-scoped custom agents: `.codex/agents/*.toml`
- 현재 정의된 custom agents: `planner`, `designer`, `frontend_engineer`, `reviewer`

### 어떻게 동작하나

- Codex는 사용자가 명시적으로 요청할 때만 subagent를 spawn합니다.
- 즉, 일반 요청만으로 항상 자동 분기되는 구조는 아니고, "agent를 나눠서 진행해줘" 같은 요청이 있어야 병렬 orchestration이 일어납니다.
- parent agent가 subagent를 띄우고, 후속 지시를 보내고, 결과를 수집해 최종 응답으로 통합합니다.

### 사용법

- 여러 관점을 병렬로 보고 싶을 때 역할별 agent를 명시해서 요청합니다.
- 예를 들어 기획, 디자인, 구현, 리뷰를 나눠서 진행하고 싶을 때 각 agent를 순서대로 또는 병렬로 지정할 수 있습니다.

예시:

- `planner로 요구사항을 정리하고 designer로 UI 방향을 만든 뒤 frontend_engineer로 구현해줘`
- `reviewer를 따로 spawn해서 현재 변경점의 회귀 위험만 점검해줘`
- `planner, designer, reviewer를 각각 병렬로 돌리고 결과를 통합해줘`

### 현재 설정과의 연결

- `.codex/config.toml`의 `agents.max_threads = 6`은 동시에 열 수 있는 agent thread 수 상한입니다.
- `.codex/config.toml`의 `agents.max_depth = 1`은 direct child까지 허용하고 더 깊은 재귀 fan-out은 막는 설정입니다.
- 현재 설정은 병렬 작업은 허용하되, 과도한 중첩 delegation은 제한하는 보수적인 기본값입니다.

### Custom agent 파일 기준

현재 `.codex/agents/*.toml` 파일은 공식 문서 기준의 핵심 필드를 사용합니다.

- `name`
- `description`
- `developer_instructions`

필요하면 아래 같은 추가 필드도 함께 둘 수 있습니다.

- `nickname_candidates`
- `model`
- `model_reasoning_effort`
- `sandbox_mode`

### 현재 agent 역할

- `planner`: 요구사항, 범위, 사용자 흐름, 열린 질문 정리
- `designer`: 레이아웃, 상태, 인터랙션, 시각 방향 정리
- `frontend_engineer`: 구현 계획과 실제 코드 변경 담당
- `reviewer`: 정확성, 회귀, 검증 누락 중심 리뷰

### 운영 메모

- subagent는 token과 tool 사용량이 추가되므로 항상 필요한 경우에만 쓰는 편이 좋습니다.
- child agent는 parent의 sandbox와 approval 성격을 이어받습니다.
- `max_depth`를 크게 올리면 fan-out이 과해질 수 있어 현재처럼 `1`을 유지하는 편이 안정적입니다.
- 같은 이름의 built-in agent보다 같은 이름의 custom agent가 우선할 수 있습니다.

## Skills

Codex skills는 재사용 가능한 작업 단위를 패키징하는 방식입니다.
하나의 skill은 `SKILL.md`를 중심으로 instructions, references, scripts, assets를 묶어서 특정 작업을 더 안정적으로 수행하게 합니다.

### 현재 기준

- repo-local skill 위치: `.agents/skills/`
- 이 저장소에서는 `codex/`가 Codex 작업 루트이므로, skill discovery도 `codex/.agents/skills` 기준으로 설명합니다.
- 현재 샘플 custom skill로 `workspace-doc-sync`를 추가해 두었습니다.

### 어떻게 호출되나

Codex skill은 두 가지 방식으로 활성화될 수 있습니다.

- 명시 호출: 프롬프트에서 `$skill-name` 형태로 직접 언급합니다.
- 암시 호출: 사용자의 요청이 skill description과 잘 맞으면 Codex가 자동으로 선택할 수 있습니다.

즉, hooks처럼 lifecycle 이벤트에 자동 연결되는 구조와는 다르고,
skill은 필요할 때 직접 `$skill-name`으로 부르거나 설명 매칭을 통해 선택되는 방식입니다.

### 사용법

- 특정 skill을 확실히 쓰고 싶으면 프롬프트에 `$skill-name`을 직접 넣습니다.
- CLI나 IDE에서는 `/skills`로 사용 가능한 skill 목록을 확인한 뒤 선택할 수 있습니다.
- 단순히 일반 요청을 보내도, description이 충분히 명확하면 Codex가 skill을 암시적으로 선택할 수 있습니다.

예시:

- `$skill-name 이 작업을 처리해줘`
- `$skill-name 을 사용해서 이 API 문서를 정리해줘`
- `/skills`로 목록 확인 후 원하는 skill 선택

### 폴더 구조

공식 권장 구조는 아래와 같습니다.

```txt
.agents/
└── skills/
    └── my-skill/
        ├── SKILL.md
        ├── SKILL.kr.md
        ├── agents/
        │   └── openai.yaml
        ├── scripts/
        ├── references/
        └── assets/
```

`agents/openai.yaml`은 skill UI 메타데이터를 담는 파일입니다.
예를 들어 skill 목록에 보이는 이름, 짧은 설명, 기본 프롬프트, implicit invocation 정책 같은 값을 정의할 수 있습니다.
반면 실제 skill trigger와 instruction 본문은 `SKILL.md`가 담당합니다.

### SKILL.md 최소 형태

`SKILL.md`에는 YAML frontmatter로 `name`과 `description`이 반드시 있어야 합니다.
Codex는 이 metadata를 먼저 읽고, 실제 사용이 필요할 때만 본문을 로드합니다.

예시:

```md
---
name: my-skill
description: Explain exactly when this skill should and should not trigger.
---

Skill instructions for Codex to follow.
```

`SKILL.kr.md` 같은 한국어 참고 문서는 사람이 읽기 위한 보조 문서로 둘 수 있습니다.
다만 skill trigger와 실제 instruction 로딩은 `SKILL.md`를 기준으로 동작합니다.

### 어디에 두면 되나

- 현재 작업 루트 기준 repo-local skill: `codex/.agents/skills/`
- 사용자 전역 skill: `$HOME/.agents/skills`
- 시스템 기본 skill: Codex 내장 skill

이 프로젝트에서는 이력서용 또는 포트폴리오용으로 repo-local skill을 함께 체크인하는 방식이 가장 설명하기 좋습니다.

### 만들 때 기준

- 한 skill은 한 가지 작업에 집중합니다.
- 설명은 trigger 조건이 분명해야 합니다.
- 반복 구현이 많을 때만 `scripts/`를 넣고, 그렇지 않으면 instruction-only skill이 기본입니다.
- 상세 레퍼런스는 `references/`로 분리해 SKILL 본문을 가볍게 유지합니다.

### 운영 메모

- skill metadata는 항상 먼저 노출되고, 본문은 실제로 사용할 때만 로드됩니다.
- 같은 이름의 skill이 여러 위치에 있으면 merge되지 않고 각각 별도로 보일 수 있습니다.
- skill 변경 사항이 바로 안 보이면 Codex를 재시작하는 편이 안전합니다.
- 특정 skill을 끄고 싶으면 `~/.codex/config.toml`의 `[[skills.config]]`로 비활성화할 수 있습니다.

### 샘플 skill

- `workspace-doc-sync`: 작업 루트 구조 변경 후 `README`, `AGENTS`, hooks, skills 관련 문서를 실제 폴더 구조와 맞추는 instruction-only skill입니다.
- `workspace-doc-sync/SKILL.kr.md`: 사람이 읽기 쉬운 한국어 참고본입니다.
- `workspace-doc-sync/agents/openai.yaml`: UI에서 보이는 skill 이름, 설명, 기본 프롬프트를 정의합니다.
- 명시 호출 예시: `$workspace-doc-sync 문서 구조를 현재 폴더 기준으로 다시 맞춰줘`

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
