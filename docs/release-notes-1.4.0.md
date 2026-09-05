# AOAgentDocs 1.4.0

긴 프로젝트를 새 세션에서 바로 이어갈 수 있도록 현재 작업 대시보드와 인수인계 규칙을 추가했습니다.

- `RULES/COMMON/SESSION_HANDOFF.md`: 새 세션 시작·종료·현황보고 규칙
- `examples/lifecycle/STATUS.md`: 지금 할 일, 전체 등록 문서, 완료 범위, 후속 대기열 양식
- PRD/PLAN/WRK/ISS/verification/release 전체와 0건인 유형까지 보고
- 완료·진행·차단·보류·미검증 및 실제 적용/제안 구조 구분
- 기존 STATUS와 프로젝트 문서는 installer가 생성하거나 덮어쓰지 않음

상태 정본은 `.aodocs/documents.json`과 연결 문서입니다. STATUS는 다음 행동을 빠르게 찾는
대시보드이며 독립적인 승인·완료 상태를 만들지 않습니다.

전체 테스트 86개 통과. 1.3.1의 비파괴 설치·Git 바이트 보존·legacy upgrade 호환을 유지합니다.
