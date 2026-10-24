# 로드맵

앞으로 추가할 항목을 우선순위별로 정리한 문서입니다. 항목을 처리하면 체크하고, 새 항목은 해당 우선순위 아래에 추가합니다.

우선순위 기준은 "드리프트를 막는 장치 > 저장소를 실제로 쓰는 경로 > 룰·커맨드 확장" 순입니다. 룰을 늘릴수록 손으로 맞춰야 할 파일이 함께 늘어나므로 자동화가 먼저입니다.

---

## P1. 드리프트 차단

- [ ] **스캐폴딩 스크립트** : `scripts/new-rule.py`, `scripts/new-command.py`, `scripts/new-agent.py`. `CONTRIBUTING.md` 체크리스트의 파일을 한 번에 생성한다. 현재는 검사(check-parity)만 있고 생성이 없어서 드리프트를 사후에만 잡는다.
- [ ] **hook 테스트** : `scripts/test-hooks.py`. 샘플 stdin JSON을 12개 훅 스크립트에 넣고 deny/allow/warn 판정을 검증한다. 가장 깨지기 쉬운 코드인데 지금은 검증이 전혀 없다.
- [ ] **CI 확장** : `.github/workflows/parity.yml`에 hook 테스트와 python lint(ruff) 추가. 현재는 parity 하나만 돈다.
- [ ] **pre-commit 훅 설치 스크립트** : `scripts/install-git-hooks.sh`. `check-parity.py`를 커밋 전에 돌린다. `scripts/check-parity.py` docstring이 pre-commit 연결을 언급하지만 실제 장치가 없다.

## P2. 실제 프로젝트 적용

- [ ] **배포 스크립트** : `scripts/install.sh --tool claude --target ../my-app`. 심볼릭 링크 또는 복사로 워크스페이스 설정을 실제 프로젝트에 넣는다. 지금은 설정을 모아두기만 하고 소비하는 경로가 없다.
- [ ] **업데이트 경로** : 이미 적용한 프로젝트에서 저장소 변경분을 다시 받아오는 방법(링크 방식이면 자동, 복사 방식이면 diff 확인).

## P3. 룰 확장

- [ ] **data-fetching** : 서버 상태와 클라이언트 상태 분리, 캐시 키 설계, 낙관적 업데이트, 재시도·에러 경계. 현재 react.md와 performance.md에 흩어져 있다.
- [ ] **error-handling** : 에러 바운더리, 폴백 UI, 사용자에게 노출할 메시지와 감출 내부 정보의 경계.
- [ ] **framework (Next.js)** : 서버·클라이언트 컴포넌트 경계, `use client` 오염, 서버 전용 값 유출. FSD 룰과 맞물리는 지점이라 효과가 크다.
- [ ] **git-convention** : 브랜치·커밋 규칙. 지금은 commit·create-pr 커맨드 본문에만 있어서 커맨드를 쓰지 않으면 적용되지 않는다.
- [ ] **i18n** : 문자열 외부화, 복수형·날짜·통화, RTL. 제품에 다국어 요구가 생기면 추가한다.

## P4. 커맨드·에이전트 확장

- [ ] **plan** : `planner` 에이전트를 부르는 진입 커맨드가 없다.
- [ ] **debug** : 재현 → 원인 특정 → 수정 → 회귀 테스트 고정 흐름.
- [ ] **a11y-audit / perf-audit** : `accessibility-reviewer`, `performance-reviewer`를 단독 실행하는 진입점.
- [ ] **onboard** : `code-mapper`로 낯선 코드베이스 구조를 파악하는 커맨드.

## P5. parity 스크립트 보강

- [ ] **hook 배선 검사** : 스크립트 파일 존재만 확인하고, `claude/.claude/settings.json`·`cursor/.cursor/hooks.json`·`codex/.codex/hooks.json`에서 실제로 참조되는지는 보지 않는다. 파일만 있고 미배선이어도 통과한다.
- [ ] **본문 드리프트 검사** : 파일명만 비교하므로 같은 이름의 룰 내용이 갈라져도 통과한다. 정규화 후 섹션 헤딩 집합을 비교하는 수준까지는 가능하다.
- [ ] **README 표 검사** : 세 README의 파일 목록 표가 수작업이라 반드시 어긋난다. 실제 파일 목록과 대조한다.

## P6. 저장소 위생

- [ ] **Claude permission 설정** : `claude/.claude/settings.json`에 `hooks`만 있고 `permissions.allow/deny`가 없다. Codex는 `codex/.codex/rules/default.rules`로 shell 정책을 선언하는데 Claude·Cursor에는 대응물이 없다.
- [ ] **MCP 설정** : 세 도구 모두 MCP 서버 목록이 없다. 공용 MCP 세트를 parity 축으로 관리할지 결정한다.
- [ ] **LICENSE**
- [ ] **PR 템플릿, CODEOWNERS** : `.github/`에 워크플로만 있다.

---

## 완료

- [x] **Claude 룰 경로 스코프** (2026-10-24) : `.claude/rules/*.md`에 `paths` frontmatter를 추가해 Cursor `globs`와 적용 범위를 맞췄다. 그전에는 11개 룰이 매 세션 전부 로드됐다.
- [x] **CONTRIBUTING.md** (2026-08-06) : 룰·커맨드·에이전트·훅 추가 시 함께 고칠 파일 체크리스트. parity가 보지 못하는 문서 표·frontmatter·훅 배선까지 포함한다.
- [x] **performance 룰** (2026-08-05) : `performance-reviewer` 에이전트의 근거 룰이 없던 비대칭을 해소했다.
- [x] **styling 룰** (2026-08-05) : `designer` 에이전트의 근거 룰이 없던 비대칭을 해소했다.
