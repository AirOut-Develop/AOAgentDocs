# 제품 문서 생명주기 — AOAgentDocs 1.3

## 역할과 정본

PRD는 무엇을/왜, 설계는 어떻게, 계획은 실행 순서와 검증, WRK/ISS는 실제 진행/실패를 기록한다.
킷은 프로젝트 지침을 대체하지 않는다. 플랫폼 규칙은 선택한 범위에만 적용한다.

- .aodocs/kit: 관리되는 규칙·템플릿·도구. 직접 편집하지 않는다.
- .aodocs/project.json: project_id, platforms(활성), planned_platforms(계획). 사용자 소유.
- .aodocs/documents.json: 문서 ID·상태·참조 정본. 본문은 기존 docs 경로 유지.
- INDEX/history/MEMORY는 요약과 링크이며, 다른 상태 정본을 만들지 않는다.

작은 버그는 ISS/짧은 계획+회귀 증거면 충분하다. 모든 수정마다 PRD를 만들지 않는다.
새 기능/API/인증 정책 변경은 PRD revision과 설계·계획을 연결한다.

## Registry schema 1

루트는 `{"schema_version":1,"documents":[]}`다. 각 문서 필수 필드는
id/kind/path/status/revision/owner/platforms다. ID는 대문자 영숫자·하이픈,
revision은 양의 정수다. project_id는 프로젝트를 식별하는 비어 있지 않은 문자열이다.

- path: 프로젝트 root 기준 기존 Markdown 상대 경로. 상위 탈출/symlink 거부.
- refs: 관련 문서 ID 배열.
- requirements: PRD가 정의하는 요구사항 ID 배열.
- covers: 작업/검증이 다루는 요구사항 ID 배열.
- evidence: 검증 문서 ID 배열.

문서/요구사항 ID는 프로젝트 범위에서 중복 불가. 기존 6자리 해시도 유한하므로 중복 검사한다.
서로 다른 프로젝트 ID의 관계는 본문에 저장소/문서 링크로 명시한다.

| kind | 허용 status |
|---|---|
| prd/design/adr | draft, in_review, approved, superseded, withdrawn |
| plan/work/issue | planned, in_progress, blocked, done, cancelled |
| verification | not_run, passed, failed, waived |
| release | not_deployed, canary, released, rolled_back |

**문서 승인 ≠ 구현 완료 ≠ 테스트 통과 ≠ 배포 완료**다.
approved 문서는 approval={by,at,revision}이 필요하고 문서 revision과 일치해야 한다.
실제 승인 없이 approval을 만들어 넣지 않는다. 범위 변경 시 in_review로 돌아가 영향을 검토한다.

passed 검증에는 command/environment/source_revision이 필요하다. 출력/시각/한계는 본문에 남긴다.
waived는 reason/owner/expires_at이 필요하며 passed를 대신하지 못한다.
done plan/work/issue와 released release는 passed evidence 최소 1개가 필요하고,
해당 covers가 evidence covers의 합집합으로 충족돼야 한다.
planned_platforms에만 있는 플랫폼은 passed 검증/done 작업/released 배포에 넣을 수 없다.
승인된 PRD/설계가 미래 플랫폼을 설명하는 것은 허용한다. 실제 지원 전환은 project.json에서
planned에서 active로 명시적으로 옮기고 해당 플랫폼의 실제 검증 기록을 남긴다.

## 이관과 호환

- PRD는 상태 때문에 이동하지 않는다. 대체/폐기는 metadata와 후속 문서 링크를 사용한다.
- 기존 WRK/ISS END 규약은 유지한다. 이동 시 registry 경로와 관련 링크를 갱신한다.
- 새 킷을 설치해도 조직 포크와 root 규칙은 자동 병합하지 않는다.
- 미래 플랫폼 요구사항을 구현/검증 완료로 표시하지 않는다.
- 일회성 세션 체크는 작업 문서에 두며 AGENTS/CLAUDE 같은 지침 파일을 상태판으로 쓰지 않는다.

## 검증 범위

validate는 metadata/ID/참조/기록된 근거/관리 hash와 payload 목록 일치, 등록 문서 상대 링크를 검사한다.
inline 이미지와 명시적/축약형 이름 참조(`[text][ref]`, `[ref][]`)도 검사한다.
완전한 CommonMark parser는 아니며 정의 없는 단축 참조(`[ref]`)는 진단하지 않는다.
코드 block의 예시 링크, 외부 URL, anchor, 승인 진위, 실제 기능/보안은 판정하지 않는다.
테스트 command를 실행하지 않는다. 빈 registry도 설치 검사는 통과하지만 제품 검증은 0건이다.

[양식/JSON 예시](../../examples/lifecycle/README.md)를 참고한다.

## Git 바이트 보존 (1.3.1)

설치기가 `.aodocs/.gitattributes`를 관리한다. `.gitattributes -text`로 속성 파일 자체를,
`kit/** -text whitespace=cr-at-eol`로 관리 킷의 원본 바이트를 보존한다.
1.3.1 이상에서는 이 파일이 없거나 바뀌어도 validate가 실패한다. 같은 버전 재설치 역시 충돌을 확인한다.
root의 프로젝트 Git 속성이나 사용자 문서를 자동으로 변경하지 않는다.
