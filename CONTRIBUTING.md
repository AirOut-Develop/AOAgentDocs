# 📘 프로젝트 기여 지침 (Project Contribution Guidelines)

> 이 저장소는 안티그래비티 표준 문서 킷(AOAgentDocs)입니다.
> 클린 아키텍처 관점에서 설계 의도와 의사결정 타당성을 기록합니다.
> 기술 스택 비종속의 순수 로직 검증 문서를 유지합니다.
> 시행착오는 `communication` 리포트로 축적해 장기 백업 지식으로 관리합니다.

## 🛑 [필수] 작업 시작 전 파이프라인 (MIGRATION 완료 후)
> 이 파이프라인은 `MIGRATION_PROMPT.txt`로 문서 킷 이식/초기화가 끝난 프로젝트에서 실행합니다.

1. [000_CHECKLIST_TEMPLATE.md](RULES/000_CHECKLIST_TEMPLATE.md)를 읽고 현재 세션용 체크리스트를 준비합니다.
2. 프로젝트 루트에 `ONBOARDING.md`가 없으면 생성합니다. (또는 팀 표준 메모리 파일 사용)
3. 체크리스트를 복사해 세션 정보와 함께 `ONBOARDING.md`(또는 팀 표준 파일)에 기록합니다.
4. 체크박스를 완료한 뒤 작업을 시작합니다.

## 🌐 공통 규칙
- [COMMUNICATION.md](RULES/COMMON/COMMUNICATION.md)
- [VERSION_CONTROL_CONVENTION.md](RULES/COMMON/VERSION_CONTROL_CONVENTION.md)
- [CODE_ETHICS.md](RULES/COMMON/CODE_ETHICS.md)

## 📱 플랫폼 규칙
<!-- [PLATFORM_RULES_START] -->
### Android
- [ARCHITECTURE.md](RULES/PLATFORM/ANDROID/ARCHITECTURE.md)
<!-- [PLATFORM_RULES_END] -->

## 🚀 시작하기
`AOAgentDocs` 적용/작업 시작은 `MIGRATION_PROMPT.txt`를 먼저 읽고 진입합니다.

- 이식 절차(진입점): `MIGRATION_PROMPT.txt`
- 소통 템플릿: `examples/communication/`
- 환경 템플릿: `examples/PROJECT_ENV_Template.md`

## 📦 릴리즈 관리
- 버전 기준: `VERSION`
- 변경 이력: `CHANGELOG.md`
- 릴리즈 절차: `RELEASE_POLICY.md`
- 중장기 계획: `ROADMAP.md`
- 패키지 생성: `scripts/release_package.sh`
- 릴리즈 게이트: 보안 감사 완료 후에만 태그/배포 진행

## 🔐 이슈/PR 보안 게이트
- 이슈 등록 전: 본문/첨부 로그에 토큰, 비밀번호, API Key, 개인식별정보가 없는지 점검합니다.
- PR 생성 전: 변경 파일과 커밋 메시지에 민감정보가 없는지 점검합니다.
- 보안 점검 미완료 상태에서는 이슈 등록/PR 제출을 금지합니다.
