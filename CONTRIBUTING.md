# 스킬 작성 가이드

각 스킬은 하나의 작업을 수행하는 독립된 폴더로 작성합니다.
에이전트가 설명만 읽고 사용 시점을 판단할 수 있고,
해당 스킬만 설치해도 작업에 필요한 파일을 읽을 수 있어야 합니다.

## 새 스킬 만들기

가장 가까운 분류를 선택하고, 저장소 전체에서 고유한 이름을 정합니다.
이름은 영문 소문자, 숫자, 하이픈으로 구성하며 1~64자여야 합니다.
하이픈은 처음과 끝에 넣거나 연속으로 사용하지 않습니다.

아래 예시는 `workflow`에 `my-skill`을 만드는 명령입니다.
이름과 분류를 실제 스킬에 맞게 바꿉니다.

```bash
mkdir -p skills/workflow/my-skill
cp templates/skill.md.tmpl skills/workflow/my-skill/SKILL.md
```

복사한 파일에서 `name`을 폴더명과 같게 바꾸고,
`metadata.category`를 분류 폴더명으로 수정합니다.
템플릿의 안내 문장은 실제 지침으로 교체합니다.

## 파일 구성

```text
skills/<category>/<skill-name>/
├── SKILL.md
├── scripts/       # 실행 코드가 필요한 경우
├── references/    # 필요한 순간에 읽는 상세 자료
└── assets/        # 서식, 예제 데이터, 이미지
```

`SKILL.md`는 실제 스킬 폴더에만 배치합니다.
루트나 분류 폴더에 배치하면 CLI가 하위 스킬을 발견하는 데 영향을 줍니다.
템플릿은 `skill.md.tmpl`처럼 별도 확장자로 보관합니다.

스킬 내부의 파일은 스킬 루트 기준 상대경로로 참조합니다.
개별 설치 시 함께 제공되도록 필요한 파일을 해당 스킬 안에 포함합니다.
로컬 절대경로, 저장소 루트의 `AGENTS.md`, 다른 스킬 폴더는 실행에 필요한 의존성으로
사용하지 않습니다.

## 메타데이터와 지침

`SKILL.md`는 YAML frontmatter와 Markdown 본문으로 구성합니다.

- `name`: 스킬 폴더명과 같은 이름입니다.
- `description`: 무엇을 하는지와 언제 사용하는지를 1~1024자로 설명합니다.
- `metadata.author`: 작성자를 문자열로 기록합니다.
- `metadata.category`: 분류 폴더명을 문자열로 기록합니다.
- `compatibility`: 필요한 실행 환경이 있을 때만 기록합니다. 최대 500자입니다.
- `license`: 스킬의 라이선스를 기록합니다. 저장소의 기본 라이선스는 MIT입니다.

분류와 영문 이름 제약은 이 저장소의 작성 규칙입니다.
그 외 형식은 [Agent Skills 규격](https://agentskills.io/specification)을 따릅니다.
추가 관리 정보는 `metadata` 안에 문자열로 넣습니다.

본문에는 적용 범위, 필요한 입력, 실행 절차, 기대 결과, 검증 방법을 적습니다.
사용하면 안 되는 인접 작업도 구체적으로 설명하면 불필요한 실행을 줄일 수 있습니다.
본문은 500줄 미만으로 유지하고, 긴 설명은 직접 연결한 `references/` 파일로 옮깁니다.
외부 도구가 필요하면 사전 조건과 실패 시 처리 방법을 함께 적습니다.

## 추가 전 확인

유지보수 도구에는 Python 3.11 이상과 [uv](https://docs.astral.sh/uv/)가 필요합니다.
저장소 루트에서 개발 의존성을 설치하고 검증을 실행합니다.

```bash
uv sync --locked
uv run --locked python scripts/validate_skills.py
uv run --locked python -m unittest discover -s tests -v
```

저장소 검증은 공식 `skills-ref` 검증기를 사용하고, 분류별 배치, 영문 이름,
저장소 전체 이름 중복, `metadata.category` 일치도 확인합니다.
스킬이 없는 초기 상태는 정상으로 처리하고, 스킬 폴더를 만들었다면 `SKILL.md`를 요구합니다.
개별 스킬만 검사할 때는 다음 명령을 사용합니다.

```bash
uv run --locked skills-ref validate skills/<category>/<skill-name>
```

`skills-ref`는 공식 저장소의 특정 커밋에 고정한 개발용 참조 도구입니다.
설치되는 스킬의 실행 의존성에는 포함되지 않습니다.
파일 참조가 실제로 존재하는지는 작성자가 별도로 확인합니다.
실제 실행은 [평가 가이드](evals/README.md)에 따라 별도로 확인합니다.
형식 검증은 지침의 실행 품질이나 모든 에이전트에서의 호환성을 보장하지 않습니다.

스킬을 추가한 뒤 루트 README와 분류 README에 이름, 설명, 설치 명령을 갱신합니다.
외부 자료를 포함하면 원본 라이선스와 저작권 고지도 함께 보관합니다.

## 변경과 커밋

하나의 스킬 변경에 필요한 지침, 자료, 검증, 목록 갱신은 같은 커밋에 포함합니다.
서로 독립된 스킬이나 도구 변경은 별도 커밋으로 나눕니다.
커밋 제목은 `feat(workflow): add my-skill`과 같은 Conventional Commits 형식을 사용합니다.
