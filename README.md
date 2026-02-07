# 🌌 AOAgentDocs

에이전트 기반 개발 과정에서 **설계 의도와 의사결정의 타당성**을 장기적으로 보존하기 위한 표준 문서 킷입니다.

## 시작 의도
- 개발 진행 중 확정된 설계/아키텍처를 **클린 아키텍처 관점**으로 기록합니다.
- 특정 프레임워크/라이브러리 중심이 아니라, **기술 스택 비종속의 순수 로직**과 구조적 합리성을 문서화합니다.
- 개발 중 시행착오, 실패 원인, 우회 전략, 최종 해결 과정을 `communication` 체계로 리포팅하여 **재발 방지용 장기 백업 지식**으로 축적합니다.

## 문서 역할
- `RULES/`: 에이전트 협업 규칙, 검증 기준, 운영 원칙
- `examples/`: 프로젝트 이식 시 바로 사용할 템플릿
- `MIGRATION_PROMPT.txt`: 새 프로젝트로 이관하는 절차
- `CONTRIBUTING.md`: 진입점 및 작업 시작 파이프라인
- `VERSION`: 현재 배포 버전
- `CHANGELOG.md`: 버전별 변경 이력
- `RELEASE_POLICY.md`: 릴리즈/태그/배포 운영 기준
- `ROADMAP.md`: 다음 버전 계획 (`v2.0` 포함)

## communication 운영 핵심
- 루트에는 인덱스/가이드/템플릿과 `issues/`만 유지
- 실제 이슈는 `issues/ISS_YYMMDD_NNN_Name` 폴더로 분리
- 문서 네이밍은 `000_...`, `001_...`, `999_Issue_Completed.md` 3자리 체계 사용
- 완료 이슈는 인덱스의 완료 표 + 이슈 폴더의 완료 문서로 확정

## 릴리즈 운영
- 버전 정책: [RELEASE_POLICY.md](./RELEASE_POLICY.md)
- 변경 이력: [CHANGELOG.md](./CHANGELOG.md)
- 로드맵: [ROADMAP.md](./ROADMAP.md)
- 현재 버전: [VERSION](./VERSION)
- 패키징 스크립트: `scripts/release_package.sh`
- 릴리즈 전 보안 감사 필수: 시크릿/민감정보/산출물 오염 점검 후 배포
