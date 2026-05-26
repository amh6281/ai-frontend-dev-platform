---
description: Run project quality checks (lint, type, build) before commit or PR.
allowed-tools: Bash(git *), Bash(npm *), Bash(pnpm *), Bash(yarn *), Bash(node *), Bash(rg *), Bash(sed *), Bash(awk *)
---

# Verify Project

> 현재 프로젝트 상태에서 **품질 검증(정적 검사, 타입 검사, 빌드 등)** 을 실행하고 결과를 요약하는 용도다.

---

## 작업 원칙

- 검증 대상은 **현재 작업 디렉토리 기준 프로젝트 전체**다
- 커밋 여부와 관계없이 실행 가능하다
- 실패한 검증이 하나라도 있으면 **명확한 실패 원인과 위치를 요약**한다
- 단순 로그 나열이 아니라 **핵심 문제만 추려서 요약**한다
- 가능한 경우 **수정 방향을 한 줄로 제안**한다
- 모든 검증이 통과되면 성공 상태를 명확히 출력한다

---

## 실행 전 중단 조건

아래 상태 중 하나라도 해당하면 이유를 설명하고 즉시 멈춘다.

| 상태              | 판단 기준                         | 안내 메시지                            |
| ----------------- | --------------------------------- | -------------------------------------- |
| package.json 없음 | 프로젝트 루트에 package.json 없음 | Node 프로젝트가 아니므로 실행 불가     |
| 의존성 미설치     | node_modules 없음                 | `npm install` 또는 `pnpm install` 필요 |

---

## 1. 컨텍스트 파악

아래 항목을 모두 확인한다.

| 항목              | 파악 방법                                          |
| ----------------- | -------------------------------------------------- |
| package.json 존재 | 프로젝트 루트에서 확인                             |
| 패키지 매니저     | lock 파일(package-lock.json / pnpm-lock.yaml) 확인 |
| eslint 설정 존재  | `.eslintrc.*` 또는 `eslint.config.*` 확인          |
| tsconfig 존재     | `tsconfig.json` 또는 `tsconfig.*.json` 확인        |
| build script 존재 | `package.json`의 `scripts.build` 확인              |

확인 커맨드 예시:

```bash
ls package.json tsconfig.json 2>/dev/null
cat package.json | jq '.scripts'
ls .eslintrc.* eslint.config.* 2>/dev/null
```

---

## 2. 검증 실행

아래 순서대로 실행한다. 각 항목은 설정이 존재하는 경우에만 실행하고, 없으면 skip 처리한다.

### Step 1 — Lint 검사

eslint 설정이 있는 경우 실행한다.

```bash
eslint . --quiet
```

### Step 2 — Type 검사

TypeScript 프로젝트(`tsconfig.json` 존재)인 경우 실행한다.

```bash
tsc -b
```

### Step 3 — Build 검사

`package.json`에 `build` script가 있는 경우 실행한다.

```bash
# npm
npm run build

# pnpm
pnpm build
```

---

## 3. 결과 해석 기준

### 실패 판단

- 하나라도 exit code ≠ 0 이면 해당 항목 **실패**로 간주
- 경고(warning)는 실패로 간주하지 않음 (단, 필요 시 별도 표시)

### 출력 규칙

- 에러 로그 전체를 그대로 출력하지 않는다
- 아래 항목만 요약한다

| 항목 | 내용                            |
| ---- | ------------------------------- |
| 파일 | 에러 발생 파일 경로             |
| 라인 | 가능하면 라인 번호              |
| 원인 | 핵심 에러 메시지                |
| 영향 | 어떤 문제를 유발하는지 (간단히) |

---

## 4. 출력 형식

### 실패한 경우

```
Verify result : failed

1. [Lint] src/components/xxx.tsx:12
   - Unexpected any usage
   - 타입 안정성 저하 가능

2. [Type] src/api/user.ts:34
   - Type 'undefined' is not assignable to type 'string'
   - 런타임 에러 발생 가능

3. [Build]
   - Failed to resolve import '@/utils/xxx'
   - 빌드 실패
```

### 성공한 경우

```
Verify result : success

- Lint  : passed
- Type  : passed
- Build : passed
```

### 실행 가능한 검증이 없는 경우

```
Verify result : skipped
Reason        : No verification scripts found
```

---

## 5. 추가 규칙

- lint / type / build 중 일부만 존재해도 가능한 항목만 실행한다
- 실행 순서는 Lint → Type → Build 순서를 유지한다
- 하나의 항목이 실패해도 나머지 항목은 계속 실행한다 (전체 결과 파악을 위해)
- 동일 파일에서 같은 종류의 에러가 여러 개일 경우, 대표 케이스 1~2개만 요약하고 나머지는 개수로 표시한다

---

## 실패 처리

| 시점           | 처리 방법                                           |
| -------------- | --------------------------------------------------- |
| lint 실행 실패 | eslint 설정 문제 또는 코드 오류로 판단 후 요약 출력 |
| type 검사 실패 | 타입 오류 파일·라인·원인 요약                       |
| build 실패     | 빌드 에러 핵심 메시지 요약                          |
| 명령어 없음    | 해당 항목 skip 처리 후 계속 진행                    |
