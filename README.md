# 🌌 AOAgentDocs

에이전트 기반 개발 과정에서 **설계 의도와 의사결정의 타당성**을 장기적으로 보존하기 위한 표준 문서 킷입니다.

## 설계 목적
- 개발 진행 중 확정된 설계/아키텍처를 **클린 아키텍처 관점**으로 기록합니다.
- 특정 프레임워크/라이브러리 중심이 아니라, **기술 스택 비종속의 순수 로직**과 구조적 합리성을 문서화합니다.
- 개발 중 시행착오, 실패 원인, 우회 전략, 최종 해결 과정을 `communication` 체계로 리포팅하여 **재발 방지용 장기 백업 지식**으로 축적합니다.

## 설치 방법
1. 릴리즈에서 `AOAgentDocs_vX.Y.Z.zip`를 다운로드하거나 저장소를 clone 합니다.
2. 대상 프로젝트 루트에 아래 항목을 복사합니다.
   - `CONTRIBUTING.md`
   - `RULES/`
   - `examples/`
3. `MIGRATION_PROMPT.txt`를 먼저 읽고, 프로젝트에 맞게 이식 절차를 수행합니다.
4. 이식 완료 후 `CONTRIBUTING.md`의 작업 시작 파이프라인을 따라 진입합니다.

## 권장 사용 순서
1. `MIGRATION_PROMPT.txt`로 초기 세팅
2. `CONTRIBUTING.md`로 작업 파이프라인 시작
3. `RULES/COMMON/*` + `RULES/PLATFORM/*` 규칙 확인
4. `examples/communication/*` 템플릿 기반으로 이슈 기록 운영

## 문서 구성
| 항목 | 역할 |
|------|------|
| `RULES/` | 에이전트 협업 규칙, 검증 기준, 운영 원칙 |
| `examples/` | 프로젝트 이식 시 바로 사용할 템플릿 |
| `MIGRATION_PROMPT.txt` | 새 프로젝트로 이관하는 절차 |
| `CONTRIBUTING.md` | 진입점 및 작업 시작 파이프라인 |
| `VERSION` | 현재 배포 버전 |
| `CHANGELOG.md` | 버전별 변경 이력 |
| `RELEASE_POLICY.md` | 릴리즈/태그/배포 운영 기준 |
| `ROADMAP.md` | 다음 버전 계획 (`v2.0` 포함) |

## communication 운영 핵심
- 운영 루트(`docs/communication/`)에는 인덱스/가이드/템플릿과 `issues/`만 유지합니다.
- 실제 이슈는 `issues/ISS_YYMMDD_NNN_Name` 폴더 단위로 생성합니다.
- 이슈 시작 시 `000_{IssueName}_Master_Report.md`를 먼저 만들고 목표/상태를 기록합니다.
- 세부 시도/검증은 `001_...`, `002_...`, `003_...` 순서의 3자리 번호 체계로 누적합니다.
- 중요한 발견(원인 후보, 재현 조건 변화, 차단 해제)은 즉시 `00x_...`로 중간 기록하고, 같은 시점에 마스터 리포트를 갱신합니다.
- 완료 시 `999_Issue_Completed.md`를 생성하고 완료 기준 충족 여부를 명시합니다.
- 인덱스 `001_ISSUE_INDEX.md`는 활성/완료 표를 항상 최신 상태로 유지합니다.
- 문서 작성/공유 전 시크릿/민감정보 마스킹을 확인하고, 보안 점검이 끝난 내용만 이슈/PR에 반영합니다.
- 운영 템플릿 기준 문서: `examples/communication/000_README_Communication_Guide.md`, `examples/communication/001_ISSUE_INDEX.md`

## 릴리즈 운영
- 버전 정책: [RELEASE_POLICY.md](./RELEASE_POLICY.md)
- 변경 이력: [CHANGELOG.md](./CHANGELOG.md)
- 로드맵: [ROADMAP.md](./ROADMAP.md)
- 현재 버전: [VERSION](./VERSION)
- 패키징 스크립트: `scripts/release_package.sh`
- 릴리즈 전 보안 감사 필수: 시크릿/민감정보/산출물 오염 점검 후 배포

## 배포 전 체크
- 이슈/PR/릴리즈 모두 보안 점검 완료 후 진행
- `RELEASE_POLICY.md`의 보안 감사 게이트 충족 여부 확인
- 배포 태그 규칙: `aodocs/vX.Y.Z`
