# Changelog

이 문서는 AOAgentDocs의 릴리즈 이력을 관리합니다.

## [Unreleased]
- 예정 변경 사항은 릴리즈 전까지 이 섹션에 기록합니다.

## [1.1.1] - 2026-02-07
### Changed
- `README.md` 보강 내용(설치 방법, 운영 핵심 상세화, 문서 구성 표)을 퍼블릭 릴리즈와 정합화
- `.gitignore`에 `dist/` 추가하여 릴리즈 산출물/부가 파일 혼입 방지

## [1.1.0] - 2026-02-07
### Added
- 릴리즈 운영 문서 추가: `VERSION`, `RELEASE_POLICY.md`, `ROADMAP.md`
- 버전/태그 규칙 추가: `RULES/COMMON/VERSION_CONTROL_CONVENTION.md`
- 릴리즈 패키징 스크립트 추가: `scripts/release_package.sh`
- 보안 감사 게이트 추가: 릴리즈/이슈/PR 전 민감정보 점검 필수

### Changed
- 문서 킷 명칭을 `AOAgentDocs`로 통일
- communication 최신 규칙 반영: `issues/ISS_YYMMDD_NNN_Name` 구조
- 기여 지침에 이슈/PR 보안 게이트 반영
