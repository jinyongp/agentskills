# Agent Skills

작업 목적과 기술별로 관리하는 jinyongp의 Agent Skills 모음입니다.
[Agent Skills 규격](https://agentskills.io/specification)을 따르며,
[skills CLI](https://github.com/vercel-labs/skills)로 설치합니다.

현재는 저장소 구조와 작성 템플릿을 준비한 상태이며, 설치 가능한 스킬은 아직 없습니다.
스킬이 추가되고 GitHub에 반영되면 아래 명령으로 목록을 확인하고 설치할 수 있습니다.

```bash
# 스킬 목록 확인
npx skills add jinyongp/agentskills --list

# 대화형으로 스킬 선택
npx skills add jinyongp/agentskills

# 특정 스킬 설치: <skill-name>을 목록에 있는 이름으로 바꿉니다.
npx skills add jinyongp/agentskills --skill <skill-name>

# Codex에 전역 설치
npx skills add jinyongp/agentskills --skill <skill-name> --agent codex --global
```

## 분류

| 분류 | 범위 | 스킬 |
| --- | --- | --- |
| [workflow](skills/workflow/README.md) | 저장소 조사, 계획, 검증, 작업 마감 | 아직 없음 |
| [frontend](skills/frontend/README.md) | 프레임워크, UI, 접근성 | 아직 없음 |
| [git](skills/git/README.md) | 커밋, 브랜치, PR | 아직 없음 |
| [writing](skills/writing/README.md) | 개발 문서, 문장 편집 | 아직 없음 |
| [tooling](skills/tooling/README.md) | 개발 도구 설정과 운영 | 아직 없음 |

스킬은 `skills/<category>/<skill-name>/SKILL.md`에 배치합니다.
분류는 저장소에서 목록을 관리하기 위한 구분이며, 설치할 때는 스킬 이름을 선택합니다.

## 스킬 추가

[작성 가이드](CONTRIBUTING.md)에 따라 [템플릿](templates/skill.md.tmpl)을 복사하고
사용 시점, 실행 절차, 결과 확인 방법을 작성합니다.
스킬 폴더 안의 `scripts/`, `references/`, `assets/`에 필요한 파일을 함께 넣으면
개별 설치 후에도 사용할 수 있습니다.

전체 검증은 저장소 루트에서 한 명령으로 실행합니다.
Python 3.11 이상, uv, Node.js 22.20 이상과 npm이 필요합니다.

```bash
uv run check.py
```

개발 의존성을 자동으로 준비하고 형식 검증, 테스트, 임시 프로젝트 설치 시험을 실행합니다.
빠르게 형식과 배치만 확인하려면 `uv run check.py validate`를 사용합니다.
GitHub Actions도 같은 스크립트를 실행하며, `--locked` 옵션으로 커밋된 의존성 버전을 확인합니다.
세부 실행 방법은 [작성 가이드](CONTRIBUTING.md#추가-전-확인)에 있습니다.
스킬을 설치하는 사용자는 이 유지보수 도구를 설치할 필요가 없습니다.

## 라이선스

이 저장소는 [MIT License](LICENSE)를 사용합니다.
외부 자료를 포함하는 스킬은 원본의 라이선스와 저작권 고지를 함께 유지해야 합니다.
