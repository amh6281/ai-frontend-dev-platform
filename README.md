# ai-frontend-dev-platform

AI 에이전트 기반 프론트엔드 개발 표준화 플랫폼입니다.  
Claude, Codex, Cursor 같은 다양한 에이전트/에디터 환경에서 공통으로 사용할 수 있는 규칙과 작업 가이드를 `.cursor`와 `.codex` 폴더에 모아둡니다.

---

## 소개

- `.cursor`: Cursor용 commands와 rules
- `.codex`: Codex용 멀티 에이전트 설정과 workflow
- 특정 도구에 종속되지 않고, 에이전트가 읽어서 따를 수 있는 문서 중심 구조

저장 위치가 `.cursor`여도 사용 주체는 Cursor로 한정하지 않습니다.  
Claude, Codex, Cursor 등 어떤 에이전트든 같은 기준으로 작업하도록 만드는 것이 목적입니다.

---

## Cursor

Cursor에서는 `.cursor/commands`, `.cursor/rules` 중심으로 작업합니다.

### 구조

```txt
.cursor/
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

### Commands

**commit**  
git diff를 분석해 팀 커밋 컨벤션(`Type(IssueNumber): 한글 요약`)에 맞는 커밋 메시지를 자동으로 생성하고 커밋합니다.

**create-pr / create-pr-kr**  
커밋 + push + PR 생성 또는 업데이트를 한 번에 처리합니다. PR 템플릿(`.github/pull_request_template.md`)을 기반으로 본문을 자동 작성합니다. `create-pr-kr`은 한국어 버전입니다.

**refactor**  
`code-quality.mdc`와 `typescript.mdc` 룰을 기준으로 대상 파일을 분석하고 리팩토링 포인트를 제안합니다. 승인한 항목만 코드에 반영합니다.

**review**  
열려 있는 PR의 diff를 분석해 bug, regression, 누락된 검증, 위험한 설계 중심으로 GitHub 인라인 리뷰 코멘트를 남깁니다. 제안 목록을 먼저 보여주고 승인 후 제출합니다.

**sync-pr**  
현재 브랜치를 base 브랜치와 동기화하고 PR 상태를 갱신합니다.

**verify**  
lint → type check → build 순서로 프로젝트 품질 검증을 실행하고 결과를 요약합니다. 에러 로그 전체 대신 파일·라인·원인만 추려서 출력합니다.

---

### Rules

코드 작성 단계부터 팀 컨벤션이 자동으로 적용됩니다.

**code-quality.mdc**  
매직 넘버·스트링 상수화, 단일 책임 원칙, early return, DRY, 시맨틱 HTML 및 접근성 속성 적용 기준을 정의합니다.

**typescript.mdc**  
`any` 금지, `React.FC` 미사용, `enum` → `as const` + union type, `import type` 강제, 인라인 타입 분리, 도메인 타입 위치(`src/modules/types/`) 등 TypeScript 컨벤션을 정의합니다.

---

## Codex

Codex에서는 `.codex/config.toml`과 `.codex/agents/*.toml`을 통해 역할별 커스텀 에이전트를 정의하고, 멀티 에이전트 흐름으로 작업할 수 있습니다.

### 구조

```txt
.codex/
├── config.toml
├── agents/
│   ├── designer.toml
│   ├── frontend-engineer.toml
│   ├── planner.toml
│   └── reviewer.toml
└── workflows/
    └── multi-agent-product-delivery.md
```

### 설정 파일

- `.codex/config.toml`: 서브에이전트 공통 설정
- `.codex/agents/*.toml`: 역할별 커스텀 에이전트
- `.codex/workflows/multi-agent-product-delivery.md`: 운영 예시와 프롬프트 템플릿

### Agents

**planner**  
요구사항, 범위, 사용자 흐름, 오픈 질문을 정리합니다.

**designer**  
레이아웃, 컴포넌트, 상태별 UI, 시각 방향을 정의합니다.

**frontend_engineer**  
구현 계획, 컴포넌트 구조, 상태 흐름, 검증 포인트를 정리하고 실제 작업에 연결합니다.

**reviewer**  
버그, 회귀, 테스트 누락, 접근성/반응형 리스크를 우선 점검합니다.

### TOML 메모

- TOML은 `#` 주석을 지원합니다.
- 에이전트 파일에는 필드 의미와 수정 포인트를 짧게 주석으로 남길 수 있습니다.
- 긴 운영 설명은 TOML보다 README나 workflow 문서에 두는 편이 좋습니다.

### 사용 예시

```txt
이 기능을 멀티 에이전트로 진행해줘.
planner로 요구사항을 정리하고, designer로 UI 명세를 만든 다음, frontend_engineer로 구현 계획과 코드 변경을 진행해.
마지막에는 reviewer로 회귀 위험과 테스트 누락을 점검하고 전체 결과를 통합해줘.
```

전체 흐름은 `.codex/workflows/multi-agent-product-delivery.md`를 기준으로 사용하면 됩니다.
