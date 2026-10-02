# git-conflict 실행 평가

merge·rebase·cherry-pick 충돌을 각각 독립된 임시 저장소에서 만들고 절차를 재현했습니다.
기준 파일의 한 줄을 두 브랜치에서 서로 다르게 수정한 뒤, 양쪽 의미를 함께 담은
예정 결과를 직접 작성했습니다. 자동 선택이나 에이전트의 해결 판단은 평가하지 않았습니다.

| 상황 | 요청 | 기대 결과 | 실제 결과 |
| --- | --- | --- | --- |
| merge 충돌 | “양쪽 내용을 보존해서 충돌 해결하고 merge 마쳐줘.” | base·현재·상대 버전 확인, 지정 결과 반영, merge 완료 | 절차 재현 통과. 결과 내용과 부모 커밋 2개 확인 |
| rebase 충돌 | “main 위로 rebase하는 중이야. 충돌 해결하고 마쳐줘.” | stage 2가 main, stage 3이 재적용 중인 feature임을 확인 | 절차 재현 통과. 단계별 내용과 결과 확인, main이 feature의 조상임을 확인 |
| cherry-pick 충돌 | “이 cherry-pick 충돌 해결하고 이어가줘.” | 해당 커밋 해결 후 cherry-pick만 계속 | 절차 재현 통과. 지정한 결과와 부모 커밋 1개 확인 |
| 미해결 상태 | 충돌을 해결하지 않고 각 operation의 --continue 시도 | 실패하고 충돌·HEAD 보존 | 세 operation에서 거부 확인. HEAD·unmerged 경로 불변 |
| 관련 없는 파일 | 각 충돌 진행 중 untracked 파일 제공 | 해결·완료 과정에서 파일 보존 | 파일 바이트 동일, untracked 상태 유지 |
| 적용 범위 밖 | “최신 main 받아줘.” 충돌 없는 상태 | 동기화 요청으로 처리 | 경계 검토 완료. 자동 선택 평가 미실행 |
| 의미가 불분명함 | 양쪽 요구사항이 상호 배타적이며 사용자 의도 미지정 | 필요한 결정을 요청하고 충돌 유지 | 독립 에이전트 평가 미실행 |

## 실행 환경

- 평가 날짜: 2026-10-03 (Asia/Seoul)
- 에이전트와 버전: Codex 현재 세션, 모델 버전 미기록. 스크립트로 절차 재현.
- 도구: Linux/WSL, Git 2.43.0, Python 3.11.17, skills CLI 1.7.0.

## 결과

`uv run check.py validate`와 skill-creator의 `quick_validate.py`가 통과했습니다.
실제 스킬의 CLI 탐색·선택 설치 후 `SKILL.md`와 `LICENSE`의 바이트 동일성을
확인했습니다.

각 저장소에서 :1·:2·:3의 내용을 비교하고 미해결 상태의 continuation 실패를
확인한 뒤 파일 수정, 명시적 스테이징, `git diff --cached --check`, 해당 operation의
`--continue` 순서로 완료했습니다. 최종 파일·커밋 구조·untracked 파일을 확인했습니다.
바이너리·rename·삭제·여러 커밋에서 반복되는 충돌, 프로젝트별 생성 파일,
관련 없는 기존 스테이징, 독립 에이전트의 판단 품질은 평가하지 않았습니다.
