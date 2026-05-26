# Claude Workspace

Claude Code용 작업 루트입니다. Claude 전용 지침은 이 폴더 안에서 관리합니다.

---

## 폴더 구조

```
claude/
├── .claude/
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
│   │   ├── karpathy-guidelines.md
│   │   ├── react.md
│   │   ├── testing.md
│   │   └── typescript.md
├── CLAUDE.md
└── README.md
```

---

## 빠른 시작

Claude를 사용할 때는 `claude/`를 작업 루트로 열고 시작합니다.

1. 기본 작업 규칙은 `CLAUDE.md`에서 확인합니다.
2. 세부 rule은 `.claude/rules/*.md`에서 확인합니다.
3. 반복 작업 command는 `.claude/commands/*.md`에서 확인합니다.
4. Claude 전용 규칙이나 command를 바꾸면 이 문서를 함께 갱신합니다.
5. 저장소 전체 구조를 바꾸면 루트 `../README.md`도 함께 갱신합니다.

---

## 적용된 규칙

`CLAUDE.md`에는 Claude 워크플로우용 기본 작업 규칙과 rule 파일 목록이 포함되어 있습니다.
세부 규칙은 Cursor 쪽 rules를 참고해 Claude용 Markdown 파일로 옮겼습니다.

| 파일 | 내용 |
| ---- | ---- |
| `.claude/rules/accessibility.md` | 시맨틱, 키보드, 포커스, 이름, contrast, responsive |
| `.claude/rules/code-quality.md` | 작업 범위, 검증, 명명, 책임 분리, 중복 제거, 성능 |
| `.claude/rules/karpathy-guidelines.md` | 단순성, surgical change, 가정 명시, 검증 목표 |
| `.claude/rules/react.md` | 컴포넌트, 상태, effect, 렌더링, 폼, async UI |
| `.claude/rules/testing.md` | 테스트 의도, 위치, UI 테스트, async 검증, 보고 |
| `.claude/rules/typescript.md` | 타입 안정성, union, guard, import type, `satisfies` |

---

## Commands

Cursor command를 Claude용 slash command 문서로 옮겼습니다. Claude에서 사용할 때는 `claude/`를 작업 루트로 열고 `.claude/commands/`의 문서를 기준으로 실행합니다.

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

## 운영 원칙

- Claude 전용 설정은 이 `claude/` 폴더에서만 관리합니다.
- 저장소 전체 개요는 루트 `README.md`를 참조하세요.
- Codex 설정은 `../codex/`, Cursor 설정은 `../cursor/`에서 별도 관리합니다.
