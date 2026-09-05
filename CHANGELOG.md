# Changelog

이 문서는 AOAgentDocs의 릴리즈 이력을 관리합니다.

## [1.4.0] - 2026-09-05
### Added
- `RULES/COMMON/SESSION_HANDOFF.md`: 새 세션 시작·종료·현황보고 규칙
- `examples/lifecycle/STATUS.md`: 현재 작업·다음 행동·전체 문서 상태 대시보드 양식
- 활성 문서가 0건인 유형과 미검증·보류·실제/제안 구조를 명시하는 보고 규약
### Changed
- CONTRIBUTING/체크리스트/문서 생명주기/설치 안내에서 STATUS를 선택적으로 연결
- 설치기는 프로젝트 상태를 추측하지 않고 STATUS를 자동 생성·덮어쓰지 않음
### Compatibility
- 기존 registry, PRD/PLAN/WRK/ISS, root 규칙과 프로젝트 문서는 변경하지 않음.
- 기존 프로젝트는 킷 업데이트 후 필요한 경우 양식을 복사해 명시적으로 도입.

## [1.3.1] - 2026-09-05
### Fixed
- 첫 소비자에서 확인된 Git CRLF 정규화에 의한 관리 파일 hash 불일치
- `.aodocs/.gitattributes`로 킷과 속성 파일 자체의 줄바꿈 변환 방지
- 신규 속성 파일의 dry-run/충돌/symlink 보호와 1.3.1 무결성 검사
- `core.autocrlf=true` 환경의 실제 git add/commit/clone/validate 회귀
- 이미 줄바꿈 변환된 정확히 1.3.0 checkout을 기존 hash와 대조해 제한적으로 복구
### Compatibility
- 1.3.0 태그·산출물은 그대로 보존. 최신 install로 namespaced kit만 갱신.

## [1.3.0] - 2026-09-05
### Added
- PRD/설계/ADR/계획/검증/릴리스 연결 규약과 선택적 registry
- iOS 규칙, 복수 활성/계획 플랫폼
- 비파괴 namespaced 설치·upgrade 및 문서 검사 CLI (Python 표준 라이브러리)
- installer/validator/ZIP 소비자 roundtrip 회귀 테스트
- 계획 플랫폼의 허위 완료 방지, 관리 목록 일치/심볼릭 링크 경계 검사
### Changed
- root 복사/덮어쓰기 대신 `.aodocs/kit` 설치를 기본 경로로 제공 (legacy 파일 보존)
- 동일 Python packager와 명시 payload 목록으로 ZIP 생성, 로컬 산출물 혼입 방지
- 현재 버전/로드맵/감사 안내 동기화, 해시 무충돌 가정 제거
### Compatibility
- 기존 WRK/ISS/END와 root `.aodocs_version` 보존. 자동 재명명/이관 없음.
- 새 설치 버전은 `.aodocs/manifest.json`에서 관리. 문서 검사와 실제 기능 검증은 별개.

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
