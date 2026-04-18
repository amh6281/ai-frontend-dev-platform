# Cursor Workspace

이 디렉터리는 Cursor용 작업 루트입니다.
Cursor command와 rule 문서는 이 폴더 안에서 관리합니다.

## 구조

```txt
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
    │   └── verify.md
    └── rules/
        ├── code-quality.mdc
        └── typescript.mdc
```

## 역할

- `.cursor/commands/*.md`: Cursor에서 실행하는 command 문서
- `.cursor/rules/*.mdc`: Cursor가 작업 중 참조하는 rule 문서

## 사용 기준

- Cursor는 이 폴더를 하나의 작업 루트처럼 사용합니다.
- Cursor 관련 instruction과 설정은 저장소 최상단이 아니라 `cursor/` 작업 루트 안에서 닫히도록 구성합니다.
- 실행 가능한 명령 정의는 `.cursor/commands/`에서 찾습니다.
- 코드 작성 규칙은 `.cursor/rules/`에서 찾습니다.
- 명령과 규칙은 섞지 않고 용도별로 분리해서 관리합니다.

## 관리 원칙

- Cursor 전용 문서는 이 폴더 안에서만 관리합니다.
- 저장소 전체 개요는 상위 루트 `README.md`에서 설명합니다.
- Codex 전용 설정은 `../codex/`에서 별도로 관리합니다.
