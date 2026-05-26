---
description: Keep workspace documentation aligned with the real tool-root structure, command files, rules, and configuration.
allowed-tools: Bash(find *), Bash(rg *), Bash(sed *), Bash(git *)
---

# Workspace Doc Sync

> 이 커맨드는 폴더 구조, 도구별 작업 루트, command/rule/config 설명이 실제 파일 구조와 어긋났을 때 문서를 동기화한다.

---

## 작업 원칙

- 실제 파일 구조를 먼저 확인한 뒤 문서를 수정한다.
- 존재하지 않는 경로, 설정, discovery 동작을 문서에 쓰지 않는다.
- 도구별 작업 루트 경계를 명확히 유지한다.
- 변경 범위는 문서 정합성을 회복하는 데 필요한 파일로 제한한다.
- hooks, skills, commands, rules처럼 서로 다른 메커니즘을 같은 것으로 설명하지 않는다.

---

## 1. 실제 구조 확인

아래 항목을 확인한다.

| 항목 | 확인 내용 |
| ---- | --------- |
| 루트 README | 저장소 전체 구조와 빠른 시작 표 |
| Claude 루트 | `claude/CLAUDE.md`, `.claude/commands/`, `.claude/rules/` |
| Codex 루트 | `codex/AGENTS.md`, `.codex/`, `.agents/skills/` |
| Cursor 루트 | `cursor/.cursor/commands/`, `cursor/.cursor/rules/` |

확인 커맨드 예시:

```bash
find . -maxdepth 4 -type f | sort
rg -n "commands|rules|skills|hooks|AGENTS|CLAUDE" README.md claude codex cursor
```

---

## 2. 루트 경계 정리

- 저장소 루트가 전체 개요인지, 특정 도구의 실제 작업 루트인지 명확히 쓴다.
- Claude 관련 설명은 `claude/` 안에서 닫히도록 정리한다.
- Codex 관련 설명은 `codex/` 안에서 닫히도록 정리한다.
- Cursor 관련 설명은 `cursor/` 안에서 닫히도록 정리한다.
- 비교가 필요한 경우에만 여러 도구의 path semantics를 같은 문단에 둔다.

---

## 3. 문서 동기화

구조 변경에 따라 아래 문서를 함께 확인하고 필요한 파일만 수정한다.

| 변경 유형 | 주요 확인 문서 |
| --------- | -------------- |
| 저장소 전체 구조 변경 | `README.md` |
| Claude command/rule 변경 | `claude/README.md`, `claude/CLAUDE.md` |
| Codex AGENTS/hooks/skills 변경 | `codex/README.md`, `codex/AGENTS.md`, `codex/AGENTS.kr.md` |
| Cursor commands/rules 변경 | `cursor/README.md` |

---

## 4. 작성 기준

- 자동 실행되는 기능과 사용자가 명시적으로 호출하는 기능을 구분한다.
- command는 command로, rule은 rule로, hook은 lifecycle hook으로, skill은 Codex skill로 설명한다.
- 문서 간 표현이 서로 충돌하지 않게 같은 용어와 경로를 사용한다.
- 기능 사용법은 추상 설명보다 실제 경로와 호출 단위 중심으로 쓴다.

---

## 5. 최종 응답

작업 후 아래를 요약한다.

```text
Workspace doc sync result : updated | clean

Changed:
- <파일 경로> — <무엇을 맞췄는지>

Verification:
- <확인한 명령 또는 확인하지 못한 이유>
```

---

## 실패 처리

| 상황 | 처리 |
| ---- | ---- |
| 문서가 실제 구조와 충돌 | 실제 구조 기준으로 최소 수정 |
| 특정 도구 discovery 동작이 불확실 | 확정 표현을 피하고 확인 필요 사항으로 표시 |
| 관련 파일이 없음 | 없는 경로를 만들지 말고 현재 구조 기준으로 문서 정리 |
