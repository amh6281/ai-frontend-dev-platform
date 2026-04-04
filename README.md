# ai-frontend-dev-platform

Cursor 기반 프론트엔드 개발 표준화 플랫폼입니다.  
Rules로 컨벤션을 강제하고, Commands로 반복 작업을 자동화합니다.

---

## 구성

```
.cursor/
├── commands/
│   ├── commit.md
│   ├── create-pr.md
│   ├── create-pr-kr.md
│   ├── refactor.md
│   ├── review.md
│   ├── sync-pr.md
│   └── verify.md
│
└── rules/
    ├── code-quality.mdc
    └── typescript.mdc
```

---

## Commands

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

## Rules

코드 작성 단계부터 팀 컨벤션이 자동으로 적용됩니다.

**code-quality.mdc**  
매직 넘버·스트링 상수화, 단일 책임 원칙, early return, DRY, 시맨틱 HTML 및 접근성 속성 적용 기준을 정의합니다.

**typescript.mdc**  
`any` 금지, `React.FC` 미사용, `enum` → `as const` + union type, `import type` 강제, 인라인 타입 분리, 도메인 타입 위치(`src/modules/types/`) 등 TypeScript 컨벤션을 정의합니다.
