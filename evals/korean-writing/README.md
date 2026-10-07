# Korean writing evaluation

## Decision clarity review — 2026-10-07

Parent instruction review; model version not recorded.
Paired case: An ambiguous modifier moves beside its referent or becomes a clause; a
recoverable omitted subject stays omitted.
The revised rule states the evidence and resulting decision while preserving the
contrasting valid case. This is rule review, not independent task execution or a
measured quality improvement. Earlier verification results below are historical.

## Instruction review

Parent review on 2026-10-06 in the current Codex session; model version not recorded.
The examples below are manual fidelity checks, not independent agent execution.

| Source or request | Candidate or decision | Review result |
| --- | --- | --- |
| "설정 변경에 대한 검토를 진행합니다." | "설정 변경을 검토합니다." | Same action and polite ending; removes a needless nominal predicate |
| "일부 사용자는 오류를 줄일 수 있다." | Keep some and possibility | "사용자의 오류를 줄인다" would overstate scope and certainty |
| "결과는 아직 확인되지 않았다." | Keep as written | Unknown actor need not be invented to force active voice |
| "내일 다시 볼까요?" | Keep as written | A proposal must not become an obligation |
| "좋아요. 이대로 진행해요." | Keep consistent polite voice | Formalization or ending variety alone adds no value |
| Request a public notice in plain formal style | Follow that genre | Natural writing does not require casual speech |
| Review without editing, with rewrite also loaded | Return passage-specific findings | One workflow preserves read-only scope |
| Korean conversation requesting an English deliverable | Apply Korean advice only to requested Korean spans | No whole-deliverable language switch |
| Edit one section of a long chapter | Retrieve necessary adjacent context and disclose scope | Unread sections are not covered by review |

## Verification and limits

No runtime scripts, morphology scores, or AI detector. Mechanical output ceilings
do not establish writing quality. Inspect relevant source sections and disclose
omissions. Automatic selection, independent native-reader judgments, and large-source
recovery remain unmeasured. No wording-pinning tests were added.

Research informed contextual judgment: [KatFishNet](https://aclanthology.org/2025.acl-long.1030/)
studies Korean detection signals, not a general quality score. The
[certainty distortion preprint](https://arxiv.org/abs/2606.07951) concerns English
rewrites; it motivates a fidelity check without establishing Korean error rates.
Guidance and examples are original; source corpora and third-party manuals are not bundled.

Full verification passed: 43 skills, 76 existing tests, and CLI fixtures. Creator
validation and selective installation with skills@1.7.0 passed; two files copied
byte-for-byte. MIT notice and local links passed. Body: 3,687 characters.
