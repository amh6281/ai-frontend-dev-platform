# Verify 참고본

이 문서는 사람이 읽기 쉽게 정리한 한국어 참고본입니다.
Codex의 실제 skill trigger와 instruction 로딩에는 사용되지 않습니다.
실제 적용되는 skill 본문은 같은 위치의 `SKILL.md`를 기준으로 합니다.

## 용도

- 현재 프로젝트에서 품질 검증(lint, type, build)을 실행하고 결과를 요약하는 skill입니다.
- 검증 대상은 현재 작업 디렉토리 기준 프로젝트 전체이며, 커밋 여부와 관계없이 실행 가능합니다.
- 단순 로그 나열이 아니라 핵심 실패 원인과 위치만 추려서 요약합니다.

## 관련 파일

- `SKILL.md`: Codex가 실제로 읽는 skill 본문입니다.
- `agents/openai.yaml`: skill 목록 UI에서 보이는 이름, 짧은 설명, 기본 프롬프트 같은 메타데이터를 정의합니다.

즉, 실제 검증 workflow는 `SKILL.md`가 담당하고,
`openai.yaml`은 사람이 skill을 고르거나 호출할 때 보조하는 표시용 설정에 가깝습니다.

## 언제 쓰나

- 커밋이나 PR 전에 프로젝트 품질 검증을 돌려야 할 때
- lint / type / build 상태를 한 번에 확인하고 싶을 때
- 실패 원인을 파일·라인·원인 중심으로 요약받고 싶을 때

## 작업 흐름

1. `package.json`이 없으면(Node 프로젝트 아님) 또는 `node_modules`가 없으면(의존성 미설치) 이유를 설명하고 멈춥니다.
2. package.json, 패키지 매니저(lock 파일), eslint 설정, tsconfig, build script 존재 여부를 확인합니다.
3. Lint(`eslint . --quiet`) → Type(`tsc -b`) → Build(`npm run build` / `pnpm build`) 순서로 실행합니다.
4. 각 항목은 설정이 있을 때만 실행하고, 없으면 skip 처리합니다.
5. exit code ≠ 0 인 항목을 실패로 보고, 파일·라인·원인·영향만 요약합니다.
6. 결과를 failed / success / skipped 형식 중 하나로 출력합니다.

## 핵심 기준

- 가능한 항목만 실행하되 Lint → Type → Build 순서를 유지합니다.
- 하나가 실패해도 나머지 검증은 계속 실행해 전체 결과를 파악합니다.
- 경고(warning)는 실패로 간주하지 않습니다.
- 동일 파일에서 같은 종류의 에러가 많으면 대표 1~2개만 요약하고 나머지는 개수로 표시합니다.
- 에러 로그 전체를 그대로 출력하지 않습니다.
