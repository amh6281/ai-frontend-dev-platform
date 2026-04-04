---
description: Analyze target files based on code-quality and typescript rules, propose refactoring points, and apply changes after approval.
allowed-tools: Bash(git *), Bash(rg *), Bash(sed *), Bash(awk *), Bash(find *), Bash(cat *)
---

# Refactor

> 이 커맨드는 `.cursor/rules/code-quality.mdc` 와 `.cursor/rules/typescript.mdc` 룰을 기준으로
> 대상 파일을 분석하고, 리팩토링 포인트를 제안한 뒤 승인 시 코드를 직접 수정한다.

---

## 작업 원칙

- 리팩토링 기준은 반드시 **프로젝트 룰(code-quality.mdc, typescript.mdc)** 에 근거한다
- 룰에 명시되지 않은 취향 차이나 스타일 선호는 제안하지 않는다
- 기능 동작을 변경하지 않는다 — **구조·타입·가독성 개선에 한정**한다
- 제안 목록을 먼저 보여주고, **사용자 승인 후에만 코드를 수정**한다
- 승인 없이 파일을 수정하지 않는다

---

## 실행 전 중단 조건

아래 상태 중 하나라도 해당하면 이유를 설명하고 즉시 멈춘다.

| 상태             | 판단 기준                                        | 안내 메시지                          |
| ---------------- | ------------------------------------------------ | ------------------------------------ |
| 룰 파일 없음     | `code-quality.mdc` 와 `typescript.mdc` 모두 없음 | 리팩토링 기준 룰 파일을 찾을 수 없음 |
| 대상 파일 없음   | 사용자가 지정한 파일이 존재하지 않음             | 대상 파일을 확인 후 재실행           |
| 대상 파일 미지정 | 사용자가 파일도 범위도 지정하지 않음             | 대상 파일 또는 범위를 지정 후 재실행 |

---

## 1. 룰 파일 로드

아래 경로에서 룰 파일을 읽어 리팩토링 기준으로 사용한다.

```bash
cat .cursor/rules/code-quality.mdc
cat .cursor/rules/typescript.mdc
```

두 파일 중 하나만 존재하면 존재하는 파일 기준으로 진행하고, 없는 파일은 skip 처리한다.

---

## 2. 대상 파일 파악

사용자 입력에 따라 아래 중 하나로 대상을 결정한다.

| 입력 유형               | 동작                                      |
| ----------------------- | ----------------------------------------- |
| 파일 경로 1개 이상 명시 | 해당 파일만 분석                          |
| 디렉토리 명시           | 해당 디렉토리 하위 `.ts` `.tsx` 파일 전체 |
| "전체" 또는 범위 미지정 | `src/` 하위 `.ts` `.tsx` 파일 전체        |

확인 커맨드 예시:

```bash
# 디렉토리 내 대상 파일 목록 확인
find src -name "*.ts" -o -name "*.tsx" | sort
```

---

## 3. 분석 기준

룰 파일을 기반으로 아래 항목을 순서대로 검토한다.

### code-quality.mdc 기준 (§2 Code Writing Principles / §3 Performance / §7 Accessibility)

- **매직 넘버·매직 스트링** (§2 Constants Over Magic Numbers) → 상수로 분리 여부
- **중복 로직** (§2 DRY) → 공통 함수·훅으로 추출 가능 여부
- **단일 책임 초과** (§2 Single Responsibility) → 함수·컴포넌트 분리 필요 여부
- **중첩 조건문** (§2 Encapsulation) → early return 또는 별도 함수로 단순화 가능 여부
- **렌더 내 무거운 연산** (§3 Avoid Heavy Computation in Render) → memoization 적용 가능 여부
- **O(n²) 반복** (§3 Avoid Nested Loops) → Map / Set 교체 가능 여부
- **시맨틱 HTML 미사용** (§7 Use Semantic HTML Elements) → `<div>` 대신 적절한 시맨틱 태그 교체 여부
- **접근성 속성 누락** (§7 Accessibility Attributes) → `aria-label` / `alt` / `role` 등 추가 여부

### typescript.mdc 기준

- **`any` 사용** (§1) → `unknown`, 제네릭, 구체적 타입으로 교체 가능 여부 (콜백 파라미터 포함)
- **`React.FC` 사용** (§2) → 화살표 함수 + 명시적 props 타입으로 교체 여부
- **`enum` 사용** (§3) → `as const` 객체 + `(typeof CONST)[keyof typeof CONST]` union type으로 교체 여부
- **interface vs type 혼용** (§4) → 객체 구조는 `interface`, union·intersection은 `type`으로 정리 여부
- **인라인 타입** (§5) → 별도 named `interface` / `type`으로 분리 가능 여부
- **exported 함수 반환 타입 미명시** (§6) → 명시적 반환 타입 추가 여부
- **`import type` 미사용** (§16) → 타입 전용 import에 `import type` 적용 여부
- **unsafe `as` 타입 단언** (§19) → 타입 가드 또는 안전한 narrowing으로 교체 가능 여부
- **`satisfies` 미사용** (§21) → 객체 shape 검증 시 `satisfies` 적용 가능 여부
- **넓은 타입 사용** (§13) → `string` / `number` 대신 리터럴 union으로 좁힐 수 있는 경우
- **boolean prop 과다** (§14) → `variant` 등 union 타입으로 통합 가능 여부
- **도메인 타입 위치** (§18) → `src/modules/types/` 하위로 분리되지 않은 타입 존재 여부

---

## 4. 제안 계획 (수정 전 승인)

분석이 끝나면 **코드를 수정하기 전에** 아래 형식으로 제안 목록을 보여주고 승인을 기다린다.

```
Refactor plan — <대상 파일 또는 범위>

  1. [code-quality] <파일명>:<라인번호> — <제안 한 줄 요약>
  2. [typescript]   <파일명>:<라인번호> — <제안 한 줄 요약>
  3. [code-quality] <파일명>:<라인번호> — <제안 한 줄 요약>
  ...

Apply? y / n / 번호 지정 (예: "1, 3만")
```

사용자 응답에 따라 동작한다.

| 응답                     | 동작                                     |
| ------------------------ | ---------------------------------------- |
| `y` 또는 "전부 적용"     | 전체 항목 수정                           |
| 번호 지정 ("1, 3만" 등)  | 해당 항목만 수정, 나머지 생략            |
| `n` 또는 "취소"          | 수정 없이 종료                           |
| 특정 항목 내용 수정 요청 | 수정 후 계획을 다시 보여주고 재승인 대기 |

- 승인 없이 파일을 수정하지 않는다
- 리팩토링 포인트가 없으면 계획 단계 없이 바로 "리팩토링 대상 없음"을 출력하고 종료한다

---

## 5. 코드 수정

승인된 항목에 한해 파일을 직접 수정한다.

수정 원칙:

- 한 번에 하나의 파일씩 수정하고, 수정 후 다음 파일로 넘어간다
- 기능 동작에 영향을 주는 변경은 하지 않는다
- 수정 범위는 승인된 항목에 한정한다 — 연관 코드라도 승인되지 않은 부분은 건드리지 않는다
- 수정 완료 후 변경된 파일 목록과 항목을 요약해서 출력한다

---

## 6. 최종 응답 형식

### 수정이 있는 경우

```
Refactor result : applied

수정 파일 : <개수>개
적용 항목 : <개수>개

1. [typescript]   src/components/UserCard.tsx:12 — any → User 타입으로 교체
2. [code-quality] src/components/UserCard.tsx:34 — 매직 스트링 → ERROR_MESSAGE 상수로 분리
3. [typescript]   src/hooks/useAuth.ts:8        — export default → named export로 변경
```

### 리팩토링 대상이 없는 경우

```
Refactor result : clean

룰 기준으로 리팩토링이 필요한 항목을 찾지 못했습니다.
```

### 취소한 경우

```
Refactor result : cancelled

수정 없이 종료했습니다.
```

---

## 실패 처리

| 시점              | 처리 방법                                             |
| ----------------- | ----------------------------------------------------- |
| 룰 파일 읽기 실패 | 파일 경로 확인 후 재실행 안내                         |
| 파일 분석 실패    | 해당 파일 skip 후 나머지 계속 진행                    |
| 수정 실패         | 실패한 항목과 원인을 출력하고 나머지 항목은 계속 진행 |
