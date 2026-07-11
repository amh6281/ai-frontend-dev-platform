# Writing Style Rules

Use these rules for any prose you produce: code comments, documentation, commit messages, PR descriptions, UI copy, and responses. The goal is text that reads like a person wrote it, without the usual AI tells. The Korean patterns below are adapted from the im-not-ai AI-tell taxonomy (https://github.com/epoko77-ai/im-not-ai).

## Principles

- Preserve meaning: never change facts, numbers, proper nouns, or direct quotes to fix style.
- Edit only spans that read as an AI tell; leave clean text alone.
- Keep the genre and register; do not turn a commit message into an essay.
- Do not over-edit: a rewrite that changes far more than the tell it targets has gone too far.

## Severity

- Must remove: a single instance already reads as AI (em dash as punctuation, "결론적으로", hype words).
- Remove on repeat: fine once or twice, a tell when it stacks (hedging, front-loaded conjunctions, identical sentence endings).
- Context only: a problem only when it piles onto other tells (mild intensifiers, formal nouns).

## English tells

- Do not use em dashes (—) or en dashes (–) as sentence punctuation; use commas, parentheses, colons, or separate sentences.
- Cut hype words: seamless, robust, powerful, leverage, delve, dive in, elevate, unlock, supercharge, game-changer, cutting-edge, best-in-class.
- Drop filler openers ("It's worth noting", "It's important to note") and empty closers ("In conclusion", "Overall", "In summary").
- Prefer plain verbs: "use" over "leverage" or "utilize", "explore" over "delve into".
- Avoid the "not just X, but Y" and "it's not only ... it's ..." constructions.
- Do not lean on bold, headings, bullet lists, or emoji where plain sentences read better.

## Korean tells (한글 출력 시)

- 번역투를 걷어냅니다: "~를 통해" → "~로", "~에 대해" → "~을", "~에 있어서" → "~에서 / ~할 때", "~에서의 / ~로의" 이중 조사 → 단순 조사.
- 이중 피동과 군더더기 술어를 줄입니다: "~되어진다" → "~된다", "가지고 있다" → "있다".
- 영어 대명사를 직역해 "그 / 그녀 / 그것 / 그들"을 반복하지 않습니다.
- 기계적 병렬을 피합니다: "첫째 / 둘째 / 셋째", 과도한 불릿·헤딩.
- AI 관용구를 삭제합니다: "결론적으로", "시사하는 바가 크다", "주목할 만하다", "혁신적인".
- 완곡 표현을 다듬습니다: "~할 수 있을 것으로 보인다" → "~한다 / ~할 수 있다".
- 문두 접속사("또한 / 따라서 / 즉 / 나아가")를 연달아 쓰지 않습니다.
- 형식명사를 줄입니다: "~하는 것이다" → "~한다", "~할 필요가 있다" → "~해야 한다", 불필요한 "점 / 수 / 바".
- 시각 장식을 자제합니다: 과도한 볼드, "따옴표" 강조, 대시(—) 남발.
- 연결어미 뒤에 불필요한 쉼표를 넣지 않습니다.

## Keep as-is (윤문 대상 제외)

- 수치, 단위, 날짜.
- 고유명사, 인명, 제품명, 모델명.
- 큰따옴표 안의 직접 인용.
- 법률·규정 조문, 불가피한 학술 개념어.

## Comments and Docs

- Keep comments about why, not a narration of the obvious (see code-quality.md Comments).
- Never add meta references to being an AI or a language model.
