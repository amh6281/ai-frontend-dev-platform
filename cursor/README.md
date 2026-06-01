# Cursor Workspace

Cursor용 작업 루트입니다. Command와 rule 문서는 이 폴더 안에서 관리합니다.

---

## 폴더 구조

```
cursor/
├── README.md
└── .cursor/
    ├── commands/
    │   ├── commit.md
    │   ├── create-pr.md
    │   ├── create-pr-kr.md
    │   ├── refactor.md
    │   ├── review.md
    │   ├── sync-pr.md
    │   ├── verify.md
    │   └── workspace-doc-sync.md
    └── rules/
        ├── accessibility.mdc
        ├── code-quality.mdc
        ├── karpathy-guidelines.mdc
        ├── react.mdc
        ├── testing.mdc
        └── typescript.mdc
```

---

## 빠른 시작

Cursor를 사용할 때는 `cursor/`를 작업 루트로 열고 시작합니다.

1. 반복 작업 명령은 `.cursor/commands/*.md`에서 확인합니다.
2. 코드 작성 규칙은 `.cursor/rules/*.mdc`에서 확인합니다.
3. command를 추가하면 이 문서의 Commands 표를 함께 갱신합니다.
4. rule을 추가하면 이 문서의 Rules 표를 함께 갱신합니다.

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
| `karpathy-guidelines.mdc`  | LLM 코딩 실수 방지 행동 가이드 |
| `react.mdc`                | React 컴포넌트·훅 작성 규칙     |
| `testing.mdc`              | 테스트 작성 및 검증 규칙        |
| `typescript.mdc`           | TypeScript 작성 규칙            |

---

## 운영 원칙

- Cursor 설정은 이 `cursor/` 폴더 안에서만 관리합니다.
- 저장소 전체 개요는 루트 `README.md`를 참조하세요.
- Codex 설정은 `../codex/`에서 별도 관리합니다.
