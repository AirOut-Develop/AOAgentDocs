# AOAgentDocs 로드맵

현재 버전: **1.4.0** (VERSION 정본).

## 1.3 범위
- PRD/설계/계획/검증/배포의 별도 상태와 연결
- 선택적 namespaced 설치와 hash 충돌 보호
- 복수 플랫폼과 iOS 지침
- 명시적 ZIP payload 및 문서 검사 CLI
- 첫 소비자 프로젝트 도입 검증

## 후속 후보 (미구현)
- registry에서 탐색 페이지 생성
- 대규모 문서의 선택적 변경 영향 분석
- 안전한 3-way kit upgrade 및 제거된 파일의 명시적 이관
- 아키텍처 의존성 자동 검사

v2는 구조 호환성이 실제로 깨지는 변경일 때 결정한다. 이번에 기존 WRK/ISS를 재명명하지 않는다.

## 1.3.1
첫 소비자 Git 등록에서 발견된 CRLF/hash 불일치를 .gitattributes와 실제 Git roundtrip 회귀로 수정.

## 1.4.0
장기 작업의 `docs/STATUS.md` 대시보드와 세션 시작·종료·현황보고 규칙을 추가한다.
registry/원문이 상태 정본이고 STATUS는 다음 행동을 찾는 파생 인덱스다.
