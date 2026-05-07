# Codex Workspace

Codex 작업 루트입니다. 규칙·에이전트·훅·스킬 설정을 이 폴더에서 관리합니다.

---

## 폴더 구조

```
codex/
├── AGENTS.md              # Codex 기본 작업 규칙
├── AGENTS.kr.md           # 한국어 참고 문서 (사람용)
├── .agents/skills/        # Repo-local Codex skills
└── .codex/
    ├── config.toml        # 공통 설정
    ├── hooks.json         # Lifecycle hook 설정
    ├── hooks/             # Hook 실행 스크립트 (*.py)
    ├── coding-rules.md    # 레거시 참고 문서
    ├── rules/
    │   └── default.rules
    └── agents/
        ├── code-mapper.toml
        ├── designer.toml
        ├── docs-researcher.toml
        ├── frontend-engineer.toml
        ├── performance_reviewer.toml
        ├── planner.toml
        ├── reviewer.toml
        └── test_engineer.toml
```

---

## AGENTS.md 로드 규칙

- Codex는 작업 시작 전 `AGENTS.md` 체인을 구성합니다.
- 우선순위: `AGENTS.override.md` → `AGENTS.md` → `config.toml`의 `project_doc_fallback_filenames`
- 이 프로젝트에서는 `codex/AGENTS.md`가 기본 instruction입니다.

---

## Subagents

복잡한 작업을 역할별로 나눠 병렬 실행할 수 있습니다.
`.codex/agents/*.toml`로 정의하며, **명시적 요청 시에만** spawn됩니다.

| Agent                  | 역할                                                                    |
| ---------------------- | ----------------------------------------------------------------------- |
| `planner`              | 요구사항·범위·수용 기준 정리                                            |
| `designer`             | 레이아웃·상태·인터랙션·접근성 설계                                      |
| `code_mapper`          | 실제 코드 경로·수정 표면 탐색                                           |
| `frontend_engineer`    | 구현 계획 및 코드 변경                                                  |
| `docs_researcher`      | 공식 문서 기준 API·동작 검증                                            |
| `reviewer`             | 정확성·보안·접근성·회귀 리뷰                                            |
| `performance_reviewer` | 렌더링, 데이터 패칭, 번들 크기, 캐시, 고빈도 상호작용의 성능 리스크 리뷰 |
| `test_engineer`        | 버그 재현, 테스트 전략 수립, 회귀 테스트 작성, 검증 명령 실행           |

**예시 요청**

```
planner로 요구사항 정리 → designer로 UI 방향 설계 → frontend_engineer로 구현
code_mapper로 저장 흐름 파악 후 frontend_engineer로 최소 수정만 적용
docs_researcher로 API 제약 확인 후 reviewer로 위험 점검
performance_reviewer로 렌더링, 번들, 캐시 병목 점검
test_engineer로 버그 재현 후 회귀 테스트 추가 및 검증
```

**관련 설정** (`config.toml`)

- `agents.max_threads = 6` — 동시 agent thread 수 상한
- `agents.max_depth = 1` — 직속 child까지만 허용, 과도한 중첩 방지

**Custom agent 파일 기준**

- `name`
- `description`
- `developer_instructions`
- `nickname_candidates`
- `model`
- `model_reasoning_effort`
- `sandbox_mode`

---

## Skills

재사용 가능한 작업 단위입니다. `SKILL.md` 중심으로 instructions·scripts·assets를 묶습니다.

**위치:** `codex/.agents/skills/<skill-name>/`

**호출 방법**

- 명시: 프롬프트에 `$skill-name` 직접 입력
- 암시: description 매칭 시 Codex가 자동 선택

**SKILL.md 최소 형태**

```md
---
name: my-skill
description: 언제 이 skill을 써야 하는지 명확히 기술
---

Skill instructions...
```

**포함된 샘플 skill**

- `workspace-doc-sync` — 폴더 구조 변경 후 README·AGENTS·hooks·skills 문서를 실제 구조에 맞게 동기화

---

## Hooks

Codex lifecycle 이벤트에 스크립트를 자동 연결합니다.
별도 명령 없이 해당 이벤트 발생 시 자동 실행됩니다.

**활성화 조건**

- `config.toml`에 `codex_hooks = true` 설정
- `hooks.json`에 이벤트·스크립트 연결 정의

**지원 이벤트 및 현재 hook**

| 이벤트             | Hook 파일                     | 동작                                               |
| ------------------ | ----------------------------- | -------------------------------------------------- |
| `SessionStart`     | `session_start_context.py`    | 작업 루트·응답 규칙 컨텍스트 주입                  |
| `PreToolUse`       | `pre_tool_use_policy.py`      | `rm -rf /`, `git reset --hard` 등 파괴적 명령 차단 |
| `UserPromptSubmit` | `user_prompt_submit_guard.py` | 프롬프트 내 API 키·private key 포함 시 차단        |
| `Stop`             | `stop_quality_gate.py`        | 변경 파일·검증 상태 누락 시 보완 요청              |

> Windows에서는 hooks가 비활성화됩니다.

---

## 관리 원칙

- Codex 전용 설정은 이 `codex/` 폴더에서만 관리합니다.
- 저장소 전체 개요는 루트 `README.md`를 참조하세요.
- Cursor 전용 설정은 `../cursor/`에서 별도 관리합니다.
