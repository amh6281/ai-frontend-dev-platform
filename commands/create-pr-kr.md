```markdown
---
description: git 변경사항을 분석하고, 팀 커밋 컨벤션에 맞는 커밋과 풀 리퀘스트를 생성한 뒤 PR을 자동으로 만듭니다.
---

# 자동 Pull Request 생성

## 중요 안내 (Cursor 보안)

Cursor는 저장소를 수정하거나 네트워크에 접근하는 명령(예: `git push`, `gh pr create`)에 대해 수동 **실행 승인**을 요구할 수 있습니다. 이 커맨드는 다음과 같이 동작합니다.

- 커밋 제목 + PR 본문 생성
- git/gh 명령 자동 실행 (승인 요청이 발생할 수 있음)

보안 모델을 유지하면서 수동 작업을 최소화하는 것을 목표로 합니다.

## Step 1 — 변경사항 분석

현재 git diff를 분석해 다음을 파악합니다.

- 변경된 파일
- 변경된 기능
- 변경 성격 (기능 추가, 버그 수정, 리팩토링, 스타일 등)

---

## Step 2 — 이슈 번호 추출

현재 브랜치명에서 이슈 번호를 추출합니다.

예시:

feature/TK-1325-card-delete  
fix/TK-210-login-error

→ 이슈 번호 = TK-1325

규칙:

- 이슈 번호는 **반드시 존재해야 함**
- 찾을 수 없는 경우 중단하고 다음을 출력:

브랜치명에 이슈 번호가 포함되어야 합니다 (예: TK-1325)

---

## Step 3 — 커밋 타입 결정

아래 커밋 타입 중 하나를 선택합니다.

Feat: 새로운 기능 추가  
Fix: 버그 수정 또는 typo  
Refactor: 리팩토링 코드 구조 개선 기능 변경 없음  
Style: CSS 등 UI 디자인 변경  
Comment: 주석 추가 또는 변경  
Test: 테스트 코드 추가 수정 삭제  
Chore: 빌드 설정 패키지 assets 변경  
Init: 프로젝트 초기 생성  
Rename: 파일 또는 폴더 이름 변경  
Remove: 파일 삭제 작업

변경사항을 **가장 잘 나타내는 타입** 하나를 선택합니다.

---

## Step 4 — 커밋 제목 생성

형식:

<Type>(<IssueNumber>): <한글 요약>

규칙:

- 최대 **50자**
- **마침표 사용 금지**
- **특수문자 사용 금지**
- **개조식 구문**
- **한글 작성**

예시:

Feat(TK-1325): 카드 삭제 버튼 추가  
Fix(TK-210): 로그인 토큰 갱신 오류 수정  
Refactor(TK-98): Zustand store 구조 정리  
Chore(TK-450): Cursor rules skills 구조 추가

---

## Step 5 — PR 본문 생성

`.github/pull_request_template.md`를 원본 템플릿으로 사용합니다.

- `.github/pull_request_template.md`를 불러와 동일한 섹션 구조(`Related Issue`, `Summary`, `Checklist`)를 유지합니다.
- diff 분석 결과와 추출한 이슈 번호로 플레이스홀더를 채웁니다.
- Checklist에서 선택된 커밋 타입에 해당하는 항목 하나만 체크합니다.
- 이 커맨드 정의 안에 템플릿 전체 내용을 포함하지 않습니다.

커밋 타입 → 체크리스트 항목 매핑:

- Feat → 새로운 기능 추가
- Fix → 버그 수정
- Style → CSS 등 사용자 UI 디자인 변경
- Refactor → 코드 리팩토링
- Comment → 주석 추가 및 수정
- Test → 테스트 추가, 테스트 리팩토링
- Chore → 빌드 부분 혹은 패키지 매니저 수정
- Rename → 파일 혹은 폴더명 수정
- Remove → 파일 혹은 폴더 삭제

---

## Step 6 — 명령 자동 실행

PR 제목과 본문 생성 후 아래 명령을 순서대로 실행합니다.

1. `git add -A`
2. `git commit -m "<PR title>"`
3. `git push -u origin HEAD`
4. `BRANCH=$(git branch --show-current)`
5. `EXISTING_PR_NUMBER=$(gh pr list --state open --head "$BRANCH" --json number --jq '.[0].number // empty')`
6. `if [ -n "$EXISTING_PR_NUMBER" ]; then\`  
   `gh pr edit "$EXISTING_PR_NUMBER" --title "<PR title>" --body "<PR body>";`  
   `gh pr view "$EXISTING_PR_NUMBER" --json url --jq .url;`  
   `else`  
   `gh pr create --title "<PR title>" --body "<PR body>";`  
   `fi`

규칙:

- 순서대로 실행하며 실패 시 중단합니다.
- 인터랙티브 git 플래그를 사용하지 않습니다.
- 강제 푸시를 하지 않습니다.
- PR이 생성되거나 수정된 경우 URL을 출력합니다.
```
