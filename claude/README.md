# Claude Workspace

Claude Code용 작업 루트입니다. Claude 전용 지침은 이 폴더 안에서 관리합니다.

---

## 폴더 구조

```
claude/
├── .claude/
│   ├── agents/
│   │   ├── accessibility-reviewer.md
│   │   ├── code-mapper.md
│   │   ├── designer.md
│   │   ├── docs-researcher.md
│   │   ├── frontend-engineer.md
│   │   ├── performance-reviewer.md
│   │   ├── planner.md
│   │   ├── reviewer.md
│   │   ├── security-reviewer.md
│   │   └── test-engineer.md
│   ├── commands/
│   │   ├── commit.md
│   │   ├── create-pr.md
│   │   ├── create-pr-kr.md
│   │   ├── refactor.md
│   │   ├── review.md
│   │   ├── sync-pr.md
│   │   ├── verify.md
│   │   └── workspace-doc-sync.md
│   ├── rules/
│   │   ├── accessibility.md
│   │   ├── code-quality.md
│   │   ├── fsd-architecture.md
│   │   ├── karpathy-guidelines.md
│   │   ├── react.md
│   │   ├── testing.md
│   │   └── typescript.md
│   ├── hooks/
│   │   ├── session_start_context.py
│   │   ├── pre_tool_use_policy.py
│   │   ├── user_prompt_submit_guard.py
│   │   └── stop_quality_gate.py
│   └── settings.json
├── CLAUDE.md
└── README.md
```

---

## 빠른 시작

Claude를 사용할 때는 `claude/`를 작업 루트로 열고 시작합니다.

1. 기본 작업 규칙은 `CLAUDE.md`에서 확인합니다.
2. 세부 rule은 `.claude/rules/*.md`에서 확인합니다.
3. 반복 작업 command는 `.claude/commands/*.md`에서 확인합니다.
4. 역할별 subagent는 `.claude/agents/*.md`에서 확인합니다.
5. lifecycle hook 연결은 `.claude/settings.json`에서 확인하고, 실제 동작은 `.claude/hooks/*.py`에서 수정합니다.
6. Claude 전용 규칙이나 command, subagent, hook을 바꾸면 이 문서를 함께 갱신합니다.
7. 저장소 전체 구조를 바꾸면 루트 `../README.md`도 함께 갱신합니다.

---

## 적용된 규칙

`CLAUDE.md`에는 Claude 워크플로우용 기본 작업 규칙과 rule 파일 목록이 포함되어 있습니다.
세부 규칙은 Claude용 Markdown 파일로 `.claude/rules/`에서 관리합니다.

| 파일 | 내용 |
| ---- | ---- |
| `.claude/rules/accessibility.md` | 시맨틱, 키보드, 포커스, 이름, contrast, responsive |
| `.claude/rules/code-quality.md` | 작업 범위, 검증, 명명, 책임 분리, 중복 제거, 성능 |
| `.claude/rules/fsd-architecture.md` | FSD 레이어 계층, import 방향, public API, 슬라이스 구조, shared 추출 |
| `.claude/rules/karpathy-guidelines.md` | 단순성, surgical change, 가정 명시, 검증 목표 |
| `.claude/rules/react.md` | 컴포넌트, 상태, effect, 렌더링, 폼, async UI |
| `.claude/rules/testing.md` | 테스트 의도, 위치, UI 테스트, async 검증, 보고 |
| `.claude/rules/typescript.md` | 타입 안정성, union, guard, import type, `satisfies` |

---

## Commands

반복 workflow는 Claude용 slash command 문서로 관리합니다. Claude에서 사용할 때는 `claude/`를 작업 루트로 열고 `.claude/commands/`의 문서를 기준으로 실행합니다.

| 파일 | 역할 |
| ---- | ---- |
| `.claude/commands/commit.md` | staged changes 기준 커밋 메시지 작성, 커밋, push 전 확인 |
| `.claude/commands/create-pr.md` | git 변경사항 분석 후 커밋과 PR 생성 (영문 설명) |
| `.claude/commands/create-pr-kr.md` | git 변경사항 분석 후 커밋과 PR 생성 (한국어 설명) |
| `.claude/commands/refactor.md` | Claude rule 기준 리팩터링 제안 및 승인 후 적용 |
| `.claude/commands/review.md` | PR diff 기반 코드 리뷰 코멘트 작성 |
| `.claude/commands/sync-pr.md` | 현재 브랜치 PR 생성 또는 기존 PR 본문 갱신 |
| `.claude/commands/verify.md` | lint, type, build 품질 검증 실행 및 요약 |
| `.claude/commands/workspace-doc-sync.md` | 작업 루트 구조와 문서 설명을 실제 파일 구조에 맞춰 동기화 |

---

## Subagents

복잡한 작업을 역할별로 나눠 위임할 수 있는 Claude Code subagent입니다.
`.claude/agents/*.md`로 정의하며, 명시적으로 호출하거나 description 매칭 시 Claude가 자동 위임합니다.

| 호출 이름                | 파일                              | 역할                                                                     |
| ------------------------ | --------------------------------- | ------------------------------------------------------------------------ |
| `accessibility-reviewer` | `accessibility-reviewer.md`       | 키보드 흐름, 포커스 관리, 시맨틱, 스크린 리더, 대비 접근성 리뷰          |
| `code-mapper`            | `code-mapper.md`                  | 실제 코드 경로·수정 표면 탐색                                            |
| `designer`               | `designer.md`                     | 레이아웃·상태·인터랙션·접근성 설계                                       |
| `docs-researcher`        | `docs-researcher.md`              | 공식 문서 기준 API·동작 검증                                             |
| `frontend-engineer`      | `frontend-engineer.md`            | 구현 계획 및 코드 변경                                                   |
| `performance-reviewer`   | `performance-reviewer.md`         | 렌더링, 데이터 패칭, 번들 크기, 캐시, 고빈도 상호작용의 성능 리스크 리뷰 |
| `planner`                | `planner.md`                      | 요구사항·범위·수용 기준 정리                                             |
| `reviewer`               | `reviewer.md`                     | 정확성·접근성·회귀·검증 공백 중심의 종합 리뷰                            |
| `security-reviewer`      | `security-reviewer.md`            | secret 노출, 인증·권한, XSS, 민감정보 경계 등 보안 리뷰                  |
| `test-engineer`          | `test-engineer.md`                | 버그 재현, 테스트 전략 수립, 회귀 테스트 작성, 검증 명령 실행            |

**명명 규칙**: Claude subagent는 `name` 필드와 파일명에 kebab-case를 사용합니다. (Codex agent는 snake_case)

**Frontmatter 필수 키**

- `name` — kebab-case 식별자
- `description` — 언제 이 agent를 써야 하는지

**Frontmatter 선택 키**

- `tools` — 허용 도구 목록 (생략 시 상위 agent의 도구를 상속). 읽기 전용 agent는 `Read, Grep, Glob`로 제한.
- `model` — `opus`, `sonnet`, `haiku`, `inherit` 중 하나.

**예시 요청**

```
accessibility-reviewer로 키보드, 포커스, 스크린 리더 흐름 점검
code-mapper로 저장 흐름 파악 후 frontend-engineer로 최소 수정만 적용
designer로 UI 방향 설계 후 frontend-engineer로 구현
docs-researcher로 API 제약 확인 후 reviewer로 위험 점검
performance-reviewer로 렌더링, 번들, 캐시 병목 점검
security-reviewer로 secret 노출, 인증 경계, XSS 위험 점검
planner로 요구사항 정리 → designer로 UI 방향 설계 → frontend-engineer로 구현
test-engineer로 버그 재현 후 회귀 테스트 추가 및 검증
```

---

## Hooks

Claude Code lifecycle 이벤트에 스크립트를 자동 연결합니다. 별도 명령 없이 해당 이벤트 발생 시 자동 실행됩니다.

**활성화 조건**

- `.claude/settings.json`의 `hooks`에 이벤트·스크립트 연결 정의
- 경로는 `$CLAUDE_PROJECT_DIR`를 사용해 `claude/` 작업 루트 기준으로 해석
- 동작하는 `python3` 필요

**지원 이벤트 및 현재 hook**

| 이벤트             | Hook 파일                     | 동작                                               |
| ------------------ | ----------------------------- | -------------------------------------------------- |
| `SessionStart`     | `session_start_context.py`    | 분리된 workspace 구조·최종 응답 기준 컨텍스트 주입 |
| `PreToolUse` (Bash) | `pre_tool_use_policy.py`     | `rm -rf /`, `git reset --hard` 등 파괴적 명령 차단, publish 계열 경고 |
| `UserPromptSubmit` | `user_prompt_submit_guard.py` | 프롬프트 내 API 키·private key 패턴 감지 시 차단    |
| `Stop`             | `stop_quality_gate.py`        | 변경 파일·검증 상태 누락 시 보완 요청              |

`../codex/.codex/hooks/`의 Codex 훅과 동일한 이벤트 스키마를 사용하며, 경로·문구만 Claude 작업 루트에 맞췄습니다. 훅 동작을 바꾸면 스크립트와 이 표를 함께 갱신합니다.

---

## 변경 위치 가이드

| 바꾸려는 것              | 수정 위치                       | 같이 확인할 문서                |
| ------------------------ | ------------------------------- | ------------------------------- |
| 기본 Claude 작업 규칙    | `CLAUDE.md`                     | 이 문서의 적용된 규칙 섹션      |
| 세부 코드 작성 rule      | `.claude/rules/*.md`            | `CLAUDE.md`의 Rule Files        |
| 반복 작업 command        | `.claude/commands/*.md`         | 이 문서의 Commands 섹션         |
| 역할별 subagent          | `.claude/agents/*.md`           | 이 문서의 Subagents 섹션        |
| lifecycle hook 연결      | `.claude/settings.json`         | 이 문서의 Hooks 섹션            |
| hook 실제 정책           | `.claude/hooks/*.py`            | `.claude/settings.json`         |

---

## 운영 원칙

- Claude 전용 설정은 이 `claude/` 폴더에서만 관리합니다.
- 저장소 전체 개요는 루트 `README.md`를 참조하세요.
- Codex 설정은 `../codex/`, Cursor 설정은 `../cursor/`에서 별도 관리합니다.
