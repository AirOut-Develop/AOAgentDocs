# Changelog

이 문서는 AOAgentDocs의 릴리즈 이력을 관리합니다.

## [1.2.0] - 2026-02-09
### Added
- WRK(작업 보고서) 체계 신설: `WRK_YYMMDD_NNN_hash_Name` 형식
- 해시 기반 고유 ID 도입 (SHA-256 앞 6자리, 충돌 방지)
- L/S 플래그 도입: ISS ↔ WRK 연계 여부 명시
- `UPGRADE_PROMPT.txt` 추가: 자동 업그레이드 리팩토링 프롬프트
- `.aodocs_version` 버전 마커 메커니즘
- `END/` 완료 아카이브 즉시 이동 규칙
- `works/` 폴더 구조 추가
- WRK 템플릿 3종: 마스터 리포트, 완료, 생성 체크
- 플랫폼 placeholder: `PLATFORM/WEB/`, `PLATFORM/SERVER/`
- Windows 패키징: `scripts/release_package.ps1`

### Changed
- ISS 네이밍: `ISS_YYMMDD_NNN_Name` → `ISS_YYMMDD_NNN_hash_Flag_Name`
- 인덱스: `001_ISSUE_INDEX.md` → `001_INDEX.md` (WRK+ISS 통합)
- `COMMUNICATION.md` 전면 개편 (WRK+ISS 해시 체계)
- `README.md` 전면 개편 (구조도, Mermaid, 배지)
- `MIGRATION_PROMPT.txt` WRK 체계 및 해시 규칙 반영
- `CONTRIBUTING.md` 설치/업그레이드 분기 반영

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
- communication 최신 규칙 반영: WRK+ISS 해시 기반 체계 (`ISS_YYMMDD_NNN_hash_Flag_Name`, `WRK_YYMMDD_NNN_hash_Name`)
- 기여 지침에 이슈/PR 보안 게이트 반영
