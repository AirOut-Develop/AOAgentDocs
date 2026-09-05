# Lifecycle 양식 사용법

양식은 복사 전용이다. 설치기는 제품 문서를 만들거나 완료 상태를 채우지 않는다.
[PRD](PRD.md), [설계](DESIGN.md), [ADR](ADR.md), [계획](PLAN.md),
[검증](VERIFICATION.md), [릴리스](RELEASE.md), [현재 작업](STATUS.md) 중 필요한 것만 사용한다.

1. PRD.md를 제품의 `docs/prd/example.md`로, PLAN.md를 `docs/plans/example.md`로,
   VERIFICATION.md를 `docs/verification/example.md`로 복사한다. 실제 내용을 작성한다.
2. [documents.example.json](documents.example.json)의 documents 배열 항목을
   `.aodocs/documents.json`에 병합한다. 기존 항목을 덮어쓰지 않는다.
3. ID/경로/owner/platforms를 프로젝트에 맞춰 수정한다. requirement와 covers를 연결한다.
4. validate를 실행한다. 예시는 draft/planned/not_run이므로 구현 완료의 증거가 아니다.
5. 실제 테스트 실행 후 verification을 passed/failed로 바꾸고 command/environment/source_revision,
   결과 본문을 남긴다. 완료 작업의 evidence에 검증 ID를 넣는다.

JSON metadata가 상태 정본이다. Markdown 제목에 상태를 복사해 두 곳에서 갱신하지 않는다.
범위가 바뀌면 revision을 올리고 승인 영향과 테스트 재실행 범위를 본문에 기록한다.
