# 📢 소통 및 문서화 지침 (Communication & Documentation)

## 1. 기본 원칙
- 문서는 한국어로 작성합니다.
- 프로젝트 적용 시 기록 위치는 `docs/communication/`입니다.

## 2. 절차 및 템플릿
- 가이드: [000_README_Communication_Guide.md](../../examples/communication/000_README_Communication_Guide.md)
- 통합 인덱스: [001_INDEX.md](../../examples/communication/001_INDEX.md)
- ISS 마스터 템플릿: [000_Master_Report_Template.md](../../examples/communication/000_Master_Report_Template.md)
- WRK 마스터 템플릿: [000_Work_Master_Report_Template.md](../../examples/communication/000_Work_Master_Report_Template.md)
- ISS 완료 템플릿: [999_Issue_Completed_Template.md](../../examples/communication/999_Issue_Completed_Template.md)
- WRK 완료 템플릿: [999_Work_Completed_Template.md](../../examples/communication/999_Work_Completed_Template.md)
- 시도 템플릿: [001_Attempt_Log_Template.md](../../examples/communication/assets/001_Attempt_Log_Template.md)

## 3. 네이밍 규칙
- 작업 폴더: `works/WRK_YYMMDD_NNN_hash_Name`
- 이슈 폴더: `issues/ISS_YYMMDD_NNN_hash_Flag_Name`
  - `YYMMDD`: 생성 날짜 (1차 정렬 기준)
  - `NNN`: 해당 날짜 내 순서 (2차 정렬, WRK/ISS 독립 카운트)
  - `hash`: 6자리 hex 고유 ID (생성 시 1회 확정, 평생 불변)
  - `Flag`: `L`(WRK 연계) / `S`(독립) — ISS에만 적용
  - `Name`: 이슈/작업 이름 (PascalCase 권장)
- 마스터 리포트: `000_{Name}_Master_Report.md`
- 상세 리포트: `001_...`, `002_...`, `003_...`
- 완료 문서: `999_Completed.md`
- 루트(`docs/communication/`)에는 인덱스/가이드/템플릿과 `works/`, `issues/`, `END/`만 둡니다.

## 4. 해시 생성 규칙
- `YYMMDD + HHMMSS + random 2자리`의 SHA-256 앞 **6자리**를 사용합니다.
- 해시는 **Primary Key**이며, 인덱스 조회 없이 즉시 채번 가능합니다.
- NNN(날짜 내 순서)은 `001_INDEX.md`에서 해당 날짜의 마지막 번호를 확인합니다.

## 5. WRK ↔ ISS 연결 규칙
- ISS(`L` 플래그)의 마스터 리포트에 **부모 WRK 해시를 필수** 기재합니다.
- WRK의 마스터 리포트의 `관련 이슈` 테이블에 ISS 해시를 등록합니다.
- ISS 완료 시 부모 WRK의 `관련 이슈` 상태를 함께 갱신합니다.
- ISS(`S` 플래그)는 독립 이슈로, 부모 WRK 참조가 없습니다.

## 6. 중간 기록 규칙
- 작업 중 중요한 발견(핵심 원인 후보, 재현 조건 변화, 우회 전략, 차단 해제)은 즉시 같은 폴더의 `00x_...` 문서로 중간 기록합니다.
- 중간 기록 직후 마스터 리포트의 실행 요약/진행 내역을 함께 갱신해 흐름 단절을 방지합니다.

## 7. 완료 처리 규칙
- `999_Completed.md` 작성 후 **즉시 `END/`로 폴더 이동**합니다.
- `works/`와 `issues/`에는 항상 **진행중인 항목만** 남습니다.
- 인덱스의 완료 섹션에 `END/` 경로를 반영합니다.
- `END/` 폴더는 읽기 전용 아카이브로 취급합니다.

## 8. 이슈 문서 보안 규칙
- 이슈/리포트/로그 문서에 토큰, 비밀번호, 키 파일, 개인식별정보를 원문으로 기록하지 않습니다.
- 재현에 필요한 값은 마스킹(`****`) 처리 후 공유합니다.
- 외부 공유(이슈 등록/PR 첨부) 전 보안 점검을 완료했는지 확인합니다.
