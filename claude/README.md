# Claude Workspace

Claude Code용 작업 루트입니다. Claude 전용 지침은 이 폴더 안에서 관리합니다.

---

## 폴더 구조

```
claude/
├── .claude/
│   └── rules/
│       ├── accessibility.md
│       ├── code-quality.md
│       ├── karpathy-guidelines.md
│       ├── react.md
│       ├── testing.md
│       └── typescript.md
├── CLAUDE.md
└── README.md
```

---

## 빠른 시작

Claude를 사용할 때는 `claude/`를 작업 루트로 열고 시작합니다.

1. 기본 작업 규칙은 `CLAUDE.md`에서 확인합니다.
2. 세부 rule은 `.claude/rules/*.md`에서 확인합니다.
3. Claude 전용 규칙을 바꾸면 이 문서를 함께 갱신합니다.
4. 저장소 전체 구조를 바꾸면 루트 `../README.md`도 함께 갱신합니다.

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

## 운영 원칙

- Claude 전용 설정은 이 `claude/` 폴더에서만 관리합니다.
- 저장소 전체 개요는 루트 `README.md`를 참조하세요.
- Codex 설정은 `../codex/`, Cursor 설정은 `../cursor/`에서 별도 관리합니다.
