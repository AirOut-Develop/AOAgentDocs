# 기여 및 프로젝트 도입 지침

## 도입 사용자

1. [README](README.md)의 dry-run/apply 순서로 설치한다.
2. [생명주기 규칙](RULES/COMMON/DOCUMENT_LIFECYCLE.md)과 프로젝트 자체 지침을 함께 읽는다.
3. `.aodocs/project.json`에 활성/계획 플랫폼을 구분한다.
4. 작업 기록은 제품 저장소의 기존 docs에 남기고 registry에 연결한다.
5. 일회성 온보딩 체크는 작업 문서에 기록한다. AGENTS/CLAUDE를 상태 파일로 바꾸지 않는다.

## 공통 규칙

- [COMMUNICATION](RULES/COMMON/COMMUNICATION.md)
- [DOCUMENT_LIFECYCLE](RULES/COMMON/DOCUMENT_LIFECYCLE.md)
- [VERSION_CONTROL_CONVENTION](RULES/COMMON/VERSION_CONTROL_CONVENTION.md)
- [CODE_ETHICS](RULES/COMMON/CODE_ETHICS.md)

## 플랫폼 — 복수 선택 가능

<!-- [PLATFORM_RULES_START] -->
- [iOS](RULES/PLATFORM/IOS/ARCHITECTURE.md)
- [Android](RULES/PLATFORM/ANDROID/ARCHITECTURE.md)
- [Web](RULES/PLATFORM/WEB/ARCHITECTURE.md)
- [Server](RULES/PLATFORM/SERVER/ARCHITECTURE.md)
<!-- [PLATFORM_RULES_END] -->

공통 킷보다 프로젝트의 검증된 범위/기술 결정과 상위 지침이 우선한다.
미구현 플랫폼을 현재 지원한다고 기록하지 않는다.

## 킷 기여자

- 기존 기록을 이동하거나 무조건 덮어쓰는 업그레이드는 금지한다.
- 도구 변경은 임시 프로젝트에서 실패 테스트 → 구현 → 회귀 검증한다.
- VERSION/README/CHANGELOG/ROADMAP/설치 안내를 함께 점검한다.
- payload 추가는 kit-files.json에 명시하고 개인정보/시크릿/로컬 산출물 혼입을 검토한다.
- 소비자 프로젝트에 설치한 상태에서도 수정 충돌·멱등성·기존 문서 보존을 확인한다.
- 운영 규약이나 승인 기록을 에이전트가 만들어 권한을 주장하지 않는다.

[릴리스 정책](RELEASE_POLICY.md), [감사 안내](AGENT_AUDIT_PROMPT.md)를 따른다.
