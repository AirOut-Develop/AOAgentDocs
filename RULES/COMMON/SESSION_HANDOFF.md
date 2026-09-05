# 세션 인수인계와 현재 작업 대기열

## 목적

긴 프로젝트에서 에이전트·터미널·모델이 바뀌어도 **검증된 현재 상태와 다음 행동을
한 번에 복구**한다. 프로젝트에는 `docs/STATUS.md` 하나를 권장한다.

STATUS는 대시보드이지 새로운 상태 정본이 아니다. 문서 ID·상태·revision은
`.aodocs/documents.json`, 요구사항과 실행 내용은 연결된 PRD/PLAN/WRK/ISS/verification/
release 원문이 정본이다. 충돌하면 정본을 우선하고 STATUS를 갱신한다.

## 필수 구성

`docs/STATUS.md`에는 다음 항목을 간결하게 둔다.

1. 최종 갱신 시각, branch/기준 source revision, 활성·계획 플랫폼.
2. 새 세션 시작 순서와 가장 먼저 읽을 문서 링크.
3. **지금 바로 할 일 한 개**: 목표, 필요한 입력, 다음 에이전트 행동, 금지사항.
4. 활성 PRD/PLAN/WRK/ISS/verification/release 전체 목록. **0건인 유형도 0건으로 표시**.
5. 완료되어 반복하지 않을 일과 그 verification/release 링크.
6. 우선순위가 있는 후속 작업 대기열과 보류/범위 밖 항목.
7. 마지막 검증 결과와 미검증 항목, 현재 차단점.

표시된 상태는 registry에서 읽어 옮긴 파생 정보다. STATUS에만 완료를 기록하지 않는다.
문서가 없는 아이디어를 확정 계획처럼 쓰지 않는다. 장기 구상과 다음 실행 항목을 구분한다.

## 새 세션 시작

1. 프로젝트의 상위 지침과 `docs/STATUS.md`를 읽는다.
2. Git root/branch/HEAD/dirty 상태를 확인한다.
3. `.aodocs/project.json`과 `.aodocs/documents.json`을 읽는다.
4. `python3 .aodocs/kit/scripts/aodocs.py validate .`를 실행한다.
5. STATUS의 지금 바로 할 일에 연결된 WRK → PLAN → ISS → 최신 verification 순으로 읽는다.
6. 최신 문서와 실제 소스·운영 상태가 다르면 자동으로 오래된 결론을 재사용하지 않는다.

## 작업 중과 세션 종료

- 중요한 범위 변경·원인·차단 해제·검증 결과는 해당 정본 문서에 먼저 기록한다.
- registry 상태/revision/refs/evidence를 실제 결과에 맞게 갱신한다.
- STATUS에는 중복 상세를 쓰지 않고 결과 링크와 다음 행동을 갱신한다.
- 다음 행동은 **입력과 성공 조건이 있는 한 문장**으로 남긴다.
- 새 파일이 있으면 프로젝트 문서 지도·inventory 규약을 갱신한다.
- validate와 필요한 제품 테스트를 실행하고 실제 실행하지 않은 항목은 미검증으로 남긴다.
- commit/push 여부, 배포 여부, rollback 위치는 서로 구분한다.

세션이 예기치 않게 끝나 STATUS를 갱신하지 못했으면 Git·registry·원문·검증 결과를 다시
읽어 복구한다. 대화 요약이나 tmux 화면만을 상태 근거로 삼지 않는다.

## 현황보고

사용자가 현황을 요청하면 다음을 함께 보고한다.

- 현재 목표와 가장 가까운 다음 행동.
- 등록된 PRD/PLAN/WRK/ISS/verification/release의 **전체 ID·상태·링크**.
- 완료/진행/차단/보류/미검증의 구분과 0건인 유형.
- 실제 적용된 구조와 아직 제안뿐인 구조.
- 마지막 확인 시각, Git commit/push, 테스트·실기·배포 상태.

보고 시 registry를 새로 읽는다. STATUS의 오래된 표를 그대로 복사하지 않는다.

## 보안과 범위

토큰·비밀번호·nonce·세션 원문·PII·개인 기기 식별자를 STATUS에 기록하지 않는다.
개인 에이전트 세션 ID나 로컬 복구 절차는 제품 STATUS와 분리한다.
설치기는 프로젝트별 내용을 알 수 없으므로 STATUS를 자동 생성하거나 덮어쓰지 않는다.
[STATUS 양식](../../examples/lifecycle/STATUS.md)을 필요한 프로젝트가 명시적으로 복사한다.
