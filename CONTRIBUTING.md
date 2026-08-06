# 기여 가이드

이 저장소는 같은 규칙을 Claude, Cursor, Codex 세 워크스페이스에 중복해서 둡니다. 항목 하나를 추가하면 여러 파일을 동시에 고쳐야 하고, 하나라도 빠지면 도구마다 다르게 동작합니다. 아래 체크리스트는 무엇을 같이 고쳐야 하는지 정리한 문서입니다.

`python3 scripts/check-parity.py`는 파일 존재 여부만 봅니다. 문서 표, frontmatter, 훅 배선, 본문 내용은 검사하지 않으므로 체크리스트로 직접 확인해야 합니다.

---

## 공통 원칙

- **parity 축 네 개** : rules, commands(codex는 skills), agents, hooks. 세 워크스페이스에서 같은 이름으로 유지한다.
- **스키마 차이는 워크스페이스 안에서 흡수** : 이름과 본문은 같게 두고, frontmatter나 이벤트 이름 같은 플랫폼 차이만 각 폴더에서 맞춘다.
- **slug는 kebab-case** : 예외는 `codex/.codex/agents/*.toml` 파일명(snake_case)과 `git-commit` 스킬 디렉터리다.
- **한 PR에 한 항목** : 룰 하나, 커맨드 하나. 여러 개를 묶으면 빠진 파일을 찾기 어렵다.
- **작업 후 parity 실행** : `python3 scripts/check-parity.py`가 통과해야 한다.

---

## 룰 추가

`<slug>`는 예를 들어 `data-fetching`.

| # | 파일 | 무엇을 |
| - | ---- | ------ |
| 1 | `claude/.claude/rules/<slug>.md` | 룰 본문 |
| 2 | `cursor/.cursor/rules/<slug>.mdc` | 같은 본문 + frontmatter |
| 3 | `claude/CLAUDE.md` | Rule Files 목록 한 줄 + 본문 임베드 섹션 |
| 4 | `codex/AGENTS.md` | 본문 임베드 섹션 (CLAUDE.md와 같은 헤딩) |
| 5 | `codex/AGENTS.kr.md` | 한국어 섹션 |
| 6 | `scripts/check-parity.py` | `EMBEDDED_RULE_PATTERNS`에 `<slug>` → 헤딩 정규식 |
| 7 | `claude/README.md` | 폴더 트리 + 적용된 규칙 표 |
| 8 | `cursor/README.md` | 폴더 트리 + Rules 표 |

`codex/README.md`에는 룰 표가 없다. Codex는 룰을 `AGENTS.md` 본문에 임베드하므로 3~5번이 그 역할을 한다.

**cursor frontmatter**

```yaml
---
description: 언제 이 룰을 적용하는지. 파일 유형과 상황을 함께 쓴다.
globs: ['**/*.{ts,tsx,js,jsx}']
---
```

`globs` 대신 `alwaysApply: true`를 쓸 수 있다. 파일 유형과 무관하게 항상 적용할 때만 쓴다(`karpathy-guidelines`, `writing-style`).

**6번을 빠뜨리면** parity가 `has no coverage mapping`으로 실패한다. 패턴은 3·4번 임베드 섹션에 실제로 존재하는 헤딩이어야 한다.

---

## 커맨드 추가

Claude·Cursor의 command와 Codex의 skill이 같은 축이다.

| # | 파일 | 무엇을 |
| - | ---- | ------ |
| 1 | `claude/.claude/commands/<slug>.md` | command 본문 |
| 2 | `cursor/.cursor/commands/<slug>.md` | 같은 본문 |
| 3 | `codex/.agents/skills/<slug>/SKILL.md` | frontmatter(`name`, `description`) + 본문 |
| 4 | `codex/.agents/skills/<slug>/SKILL.kr.md` | 한국어 참고본. 없으면 parity가 `[WARN]` |
| 5 | `codex/.agents/skills/<slug>/agents/openai.yaml` | `display_name`, `short_description`, `default_prompt` |
| 6 | `claude/CLAUDE.md` | Commands 목록 한 줄 |
| 7 | `claude/README.md` | 폴더 트리 + Commands 표 |
| 8 | `cursor/README.md` | Commands 표 |
| 9 | `codex/README.md` | 폴더 트리 + Skills 표 |
| 10 | `README.md` | Codex 항목의 skill 이름 나열 |
| 11 | `scripts/check-parity.py` | 스킬 디렉터리명이 command명과 다를 때만 `ALIASES` 등록 |

11번은 예외 처리다. `commit` 커맨드의 스킬 디렉터리가 `git-commit`이라 `ALIASES = {"git-commit": "commit"}`이 있다. 이름을 맞출 수 있으면 맞추고 11번을 건너뛴다.

---

## 에이전트 추가

| # | 파일 | 무엇을 |
| - | ---- | ------ |
| 1 | `claude/.claude/agents/<slug>.md` | `name`, `description`, `tools`, `model` + 본문 |
| 2 | `cursor/.cursor/agents/<slug>.md` | 같은 `name`·`description`·본문, `readonly` |
| 3 | `codex/.codex/agents/<snake_slug>.toml` | `name`, `description`, `model`, `sandbox_mode`, `developer_instructions` |
| 4 | `claude/CLAUDE.md` | Subagents 목록 한 줄 |
| 5 | `claude/README.md` | 폴더 트리 + Subagents 표 |
| 6 | `cursor/README.md` | Subagents 표 |
| 7 | `codex/README.md` | 폴더 트리 + Subagents 표 |

**권한 표기 대응**

| 성격 | Claude | Cursor | Codex |
| ---- | ------ | ------ | ----- |
| 읽기 전용 | `tools: Read, Grep, Glob` | `readonly: true` | `sandbox_mode = "read-only"` |
| 쓰기 가능 | `tools` 생략 또는 확장 | `readonly` 생략 | `sandbox_mode = "workspace-write"` |

`name` 필드는 세 플랫폼 모두 kebab-case로 같게 쓴다. Codex는 파일명만 snake_case이고 `name`은 kebab-case다. Cursor는 모델 ID 체계가 달라 `model`을 생략하고 상위 세션 모델을 상속한다.

---

## 훅 추가

스크립트 파일명이 parity 축이다. 세 워크스페이스에서 같은 파일명을 쓴다.

| # | 파일 | 무엇을 |
| - | ---- | ------ |
| 1 | `claude/.claude/hooks/<name>.py` | Claude 스키마 구현 |
| 2 | `cursor/.cursor/hooks/<name>.py` | Cursor 스키마 구현 |
| 3 | `codex/.codex/hooks/<name>.py` | Codex 스키마 구현 |
| 4 | `claude/.claude/settings.json` | 이벤트 배선 |
| 5 | `cursor/.cursor/hooks.json` | 이벤트 배선 |
| 6 | `codex/.codex/hooks.json` | 이벤트 배선 |
| 7 | `claude/CLAUDE.md` | Hooks 표 |
| 8 | `claude/README.md`, `cursor/README.md`, `codex/README.md` | 각 Hooks 표 |

**이벤트 이름 대응**

| 시점 | Claude | Cursor | Codex |
| ---- | ------ | ------ | ----- |
| 세션 시작 | `SessionStart` | `sessionStart` | `SessionStart` |
| 셸 실행 전 | `PreToolUse` (matcher `Bash`) | `beforeShellExecution` | `PreToolUse` (matcher `Bash`) |
| 프롬프트 제출 | `UserPromptSubmit` | `beforeSubmitPrompt` | `UserPromptSubmit` |
| 응답 종료 | `Stop` | `stop` | `Stop` |

**차단 방식 차이**

- **Claude** : `hookSpecificOutput.permissionDecision`으로 `deny`/`ask`를 반환한다.
- **Cursor** : `permission: deny` 또는 exit code 2. warn 채널이 없어 경고 대상은 `ask`로 올린다.
- **Codex** : Claude와 같은 스키마를 쓰되 경로를 `git rev-parse --show-toplevel` 기준으로 잡는다.

경로 규칙도 다르다. Claude는 `$CLAUDE_PROJECT_DIR`, Cursor와 Codex는 `$(git rev-parse --show-toplevel)`을 쓴다. 복사할 때 그대로 두면 경로가 어긋난다.

---

## 검증

```bash
python3 scripts/check-parity.py
```

- **`[DRIFT]`** : 축 하나라도 어긋나면 exit 1. CI(`.github/workflows/parity.yml`)에서도 같은 명령이 돈다.
- **`[WARN]`** : `SKILL.kr.md`, `AGENTS.kr.md` 누락. 실패시키지 않는다.

**parity가 잡지 못하는 것**

- 같은 이름 파일의 본문이 갈라진 경우
- frontmatter 키 누락이나 오타
- 훅 스크립트가 배선 파일에서 참조되지 않는 경우
- README 표와 실제 파일 목록의 불일치

이 네 가지는 [docs/ROADMAP.md](docs/ROADMAP.md) P5에 개선 항목으로 잡혀 있다. 그때까지는 위 체크리스트로 직접 확인한다.

---

## PR 전 확인

1. `python3 scripts/check-parity.py` 통과
2. 체크리스트의 문서 표를 모두 갱신했는지 확인
3. 로드맵 항목을 처리했다면 [docs/ROADMAP.md](docs/ROADMAP.md)에서 체크하고 완료 섹션으로 옮긴다
4. 커밋 메시지와 PR 본문은 `claude/.claude/rules/writing-style.md` 기준을 따른다
