# Cursor Workspace

Cursor용 작업 루트입니다. Command, rule, subagent, hook 문서는 이 폴더 안에서 관리합니다.

---

## 폴더 구조

```
cursor/
├── README.md
└── .cursor/
    ├── agents/
    │   ├── accessibility-reviewer.md
    │   ├── code-mapper.md
    │   ├── designer.md
    │   ├── docs-researcher.md
    │   ├── frontend-engineer.md
    │   ├── performance-reviewer.md
    │   ├── planner.md
    │   ├── reviewer.md
    │   ├── security-reviewer.md
    │   └── test-engineer.md
    ├── commands/
    │   ├── commit.md
    │   ├── create-pr.md
    │   ├── create-pr-kr.md
    │   ├── refactor.md
    │   ├── review.md
    │   ├── sync-pr.md
    │   ├── verify.md
    │   └── workspace-doc-sync.md
    ├── hooks/
    │   ├── session_start_context.py
    │   ├── pre_tool_use_policy.py
    │   ├── user_prompt_submit_guard.py
    │   └── stop_quality_gate.py
    ├── hooks.json
    └── rules/
        ├── accessibility.mdc
        ├── code-quality.mdc
        ├── fsd-architecture.mdc
        ├── karpathy-guidelines.mdc
        ├── performance.mdc
        ├── react.mdc
        ├── security.mdc
        ├── styling.mdc
        ├── testing.mdc
        ├── typescript.mdc
        └── writing-style.mdc
```

---

## 빠른 시작

Cursor를 사용할 때는 `cursor/`를 작업 루트로 열고 시작합니다.

1. 반복 작업 명령은 `.cursor/commands/*.md`에서 확인합니다.
2. 코드 작성 규칙은 `.cursor/rules/*.mdc`에서 확인합니다.
3. 역할별 subagent는 `.cursor/agents/*.md`에서 확인합니다.
4. hook 연결은 `.cursor/hooks.json`에서 확인하고, 실제 동작은 `.cursor/hooks/*.py`에서 수정합니다.
5. command나 rule, subagent, hook을 추가하면 이 문서의 해당 표를 함께 갱신합니다.

Codex 설정과 Cursor 설정은 서로 참조하지 않고, 각자 폴더 안에서 독립적으로 관리합니다.

---

## Commands

`.cursor/commands/` 안의 각 파일은 Cursor에서 실행 가능한 command를 정의합니다.

| 파일              | 역할                  |
| ----------------- | --------------------- |
| `commit.md`       | 커밋 메시지 작성 규칙 |
| `create-pr.md`    | PR 생성 (영문)        |
| `create-pr-kr.md` | PR 생성 (한국어)      |
| `refactor.md`     | 리팩터링 가이드       |
| `review.md`       | 코드 리뷰             |
| `sync-pr.md`      | PR 동기화             |
| `verify.md`       | 변경 사항 검증        |
| `workspace-doc-sync.md` | 작업 루트 구조와 문서 설명 동기화 |

---

## Rules

`.cursor/rules/` 안의 파일은 Cursor가 작업 중 참조하는 코드 작성 규칙입니다.

| 파일                       | 역할                            |
| -------------------------- | ------------------------------- |
| `accessibility.mdc`        | 접근성 작성 및 검증 규칙        |
| `code-quality.mdc`         | 코드 품질 기준                  |
| `fsd-architecture.mdc`     | FSD 레이어 계층·import 방향·public API·슬라이스 구조 |
| `karpathy-guidelines.mdc`  | LLM 코딩 실수 방지 행동 가이드 |
| `performance.mdc`          | 측정 우선·렌더링 비용·데이터 로딩·번들·체감 성능 |
| `react.mdc`                | React 컴포넌트·훅 작성 규칙     |
| `security.mdc`             | secret·입력 검증·인증·storage·의존성 보안 규칙 |
| `styling.mdc`              | 디자인 토큰·스타일 경계·레이아웃·반응형·모션·시각 상태 |
| `testing.mdc`              | 테스트 작성 및 검증 규칙        |
| `typescript.mdc`           | TypeScript 작성 규칙            |
| `writing-style.mdc`        | AI 티 문체 제거(영어·한글)·번역투·관용구·대시 배제 |

---

## Subagents

역할별로 작업을 나눠 위임하는 Cursor subagent입니다. `.cursor/agents/*.md`로 정의하며, `/이름`으로 직접 부르거나 description 매칭 시 Cursor가 자동 위임합니다.

| 호출 이름                | 역할                                                                     |
| ------------------------ | ------------------------------------------------------------------------ |
| `accessibility-reviewer` | 키보드 흐름, 포커스 관리, 시맨틱, 스크린 리더, 대비 접근성 리뷰          |
| `code-mapper`            | 실제 코드 경로·수정 표면 탐색                                            |
| `designer`               | 레이아웃·상태·인터랙션·접근성 설계                                       |
| `docs-researcher`        | 공식 문서 기준 API·동작 검증                                             |
| `frontend-engineer`      | 구현 계획 및 코드 변경                                                   |
| `performance-reviewer`   | 렌더링, 데이터 패칭, 번들 크기, 캐시, 고빈도 상호작용의 성능 리스크 리뷰 |
| `planner`                | 요구사항·범위·수용 기준 정리                                             |
| `reviewer`               | 정확성·접근성·회귀·검증 공백 중심의 종합 리뷰                            |
| `security-reviewer`      | secret 노출, 인증·권한, XSS, 민감정보 경계 등 보안 리뷰                  |
| `test-engineer`          | 버그 재현, 테스트 전략 수립, 회귀 테스트 작성, 검증 명령 실행            |

`../claude/.claude/agents/`의 Claude subagent와 이름·본문이 같고, frontmatter만 Cursor 스키마에 맞췄습니다.

- **`readonly: true`** : 읽기 전용 8종에 지정. Claude의 `tools: Read, Grep, Glob` 제한을 대신합니다
- **`model` 생략** : Cursor의 모델 ID 체계가 Claude의 `opus`/`sonnet` alias와 달라 상위 세션 모델을 상속합니다

---

## Hooks

Cursor lifecycle 이벤트에 스크립트를 자동 연결합니다. `.cursor/hooks.json`에 정의하며 동작하는 `python3`가 필요합니다.

| 이벤트                 | Hook 파일                     | 동작                                               |
| ---------------------- | ----------------------------- | -------------------------------------------------- |
| `sessionStart`         | `session_start_context.py`    | 분리된 workspace 구조·최종 응답 기준 컨텍스트 주입 |
| `beforeShellExecution` | `pre_tool_use_policy.py`      | `rm -rf /`, `git reset --hard` 등 파괴적 명령 deny, publish 계열은 ask |
| `beforeSubmitPrompt`   | `user_prompt_submit_guard.py` | 프롬프트 내 API 키·private key 패턴 감지 시 차단    |
| `stop`                 | `stop_quality_gate.py`        | 변경 파일·검증 상태 누락 시 후속 메시지 요청       |

Claude·Codex의 hook 4종과 같은 정책을 쓰지만 이벤트 이름과 입출력 스키마가 다릅니다. 스크립트 파일명은 셋 다 동일하게 맞춰 parity 검사가 대응 관계를 인식합니다.

**Claude와 다른 점**

- **차단 방식** : Claude는 `hookSpecificOutput.permissionDecision`, Cursor는 `permission: deny` 또는 exit code 2를 씁니다
- **경고 채널 없음** : Cursor에는 warn 전용 출력이 없어 `npm publish` 같은 명령을 `ask`로 올립니다
- **컨텍스트 주입 위치** : `beforeSubmitPrompt`는 컨텍스트를 주입할 수 없어, 프롬프트 작성 가이드를 `sessionStart`로 옮겼습니다
- **stop 페이로드** : Cursor의 `stop`은 마지막 응답 본문을 주지 않고 `transcript_path`만 줍니다. 트랜스크립트 파일 포맷은 공식 문서에 없어서 JSONL과 단일 JSON을 모두 시도하고, 파싱에 실패하면 아무 요청도 하지 않고 넘어갑니다

---

## 운영 원칙

- Cursor 설정은 이 `cursor/` 폴더 안에서만 관리합니다.
- 저장소 전체 개요는 루트 `README.md`를 참조하세요.
- Codex 설정은 `../codex/`에서 별도 관리합니다.
