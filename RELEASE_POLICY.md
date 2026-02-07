# 📦 AOAgentDocs 릴리즈 정책

## 1. 목적
- AOAgentDocs를 팀/외부에 배포 가능한 형태로 안정적으로 관리합니다.
- 변경 이력을 추적 가능하게 유지하고, 회귀/혼입 리스크를 낮춥니다.

## 2. 버전 정책 (SemVer)
- `MAJOR`: 호환 불가 구조 변경 (예: 폴더 규칙 대폭 변경)
- `MINOR`: 하위 호환 기능/가이드 추가
- `PATCH`: 오탈자/링크/문구 수정 등 경미한 보정

예시:
- `1.1.0` → 릴리즈 관리 체계 도입
- `2.0.0` → 클린 아키텍처 가이드 정식 포함(예정)

## 3. 태그/산출물 규칙
- Git 태그: `aodocs/vX.Y.Z`
- 배포 파일: `AOAgentDocs_vX.Y.Z.zip`
- 릴리즈 노트: `CHANGELOG.md`의 해당 버전 섹션을 기준으로 작성

## 4. 릴리즈 체크리스트
1. `VERSION`을 목표 버전으로 갱신
2. `CHANGELOG.md`에 변경 사항 기록 (`Unreleased` 정리)
3. 링크 무결성 검사 (깨진 상대 링크 0건)
4. 핵심 문서 일관성 점검 (`README`, `CONTRIBUTING`, `MIGRATION_PROMPT`, `RULES/COMMON/*`)
5. 보안 감사 수행 (아래 `보안 감사 게이트` 항목 충족 필수)
6. 릴리즈 커밋 생성
7. Git 태그 생성 (`aodocs/vX.Y.Z`)
8. `scripts/release_package.sh`로 `AOAgentDocs_vX.Y.Z.zip` 생성 및 배포 채널 업로드

## 5. 보안 감사 게이트 (필수)
- 하드코딩된 시크릿(API Key, Token, Password, Private Key) 유출이 0건이어야 합니다.
- 개인식별정보(PII) 또는 내부 민감 정보가 샘플/템플릿에 포함되지 않아야 합니다.
- 배포 산출물(zip)에 불필요한 로컬/런타임 파일(`.omc`, `.codex`, `.idea`, 개인 로그)이 포함되지 않아야 합니다.
- 보안 이슈가 발견되면 `CHANGELOG.md`의 `Unreleased`에 기록하고, 해결 완료 전 릴리즈를 금지합니다.

## 6. 핫픽스 정책
- 배포 후 치명 오탈자/링크 오류 발견 시 `PATCH` 릴리즈를 즉시 발행합니다.
- 핫픽스도 동일하게 `VERSION`, `CHANGELOG`, 태그를 동기화합니다.
- 보안 취약점 핫픽스는 최우선 처리하고 일반 패치보다 먼저 배포합니다.

## 7. v2.0 준비 조건
- 클린 아키텍처 문서 초안 100% 작성
- 아키텍처 용어집/검증 체크리스트/ADR 템플릿 포함
- 기존 communication 규칙과 충돌 없음 검증
