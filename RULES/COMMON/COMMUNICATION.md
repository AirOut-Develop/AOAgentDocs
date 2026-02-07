# 📢 소통 및 문서화 지침 (Communication & Documentation)

## 1. 기본 원칙
- 문서는 한국어로 작성합니다.
- 프로젝트 적용 시 기록 위치는 `docs/communication/`입니다.

## 2. 절차 및 템플릿
- 가이드: [000_README_Communication_Guide.md](../../examples/communication/000_README_Communication_Guide.md)
- 인덱스 템플릿: [001_ISSUE_INDEX.md](../../examples/communication/001_ISSUE_INDEX.md)
- 마스터 템플릿: [000_Master_Report_Template.md](../../examples/communication/000_Master_Report_Template.md)
- 완료 템플릿: [999_Issue_Completed_Template.md](../../examples/communication/999_Issue_Completed_Template.md)
- 시도 템플릿: [001_Attempt_Log_Template.md](../../examples/communication/assets/001_Attempt_Log_Template.md)

## 3. 네이밍 규칙
- 이슈 폴더: `issues/ISS_YYMMDD_NNN_Name`
- 마스터 리포트: `000_{IssueName}_Master_Report.md`
- 상세 리포트: `001_...`, `002_...`, `003_...`
- 완료 문서: `999_Issue_Completed.md` (완료 이슈 필수)
- 루트(`docs/communication/`)에는 인덱스/가이드/템플릿과 `issues/`만 둡니다.

## 4. 중간 기록 규칙
- 작업 중 중요한 발견(핵심 원인 후보, 재현 조건 변화, 우회 전략, 차단 해제)은 즉시 같은 이슈 폴더의 `00x_...` 문서로 중간 기록합니다.
- 중간 기록 직후 `000_{IssueName}_Master_Report.md`의 실행 요약/시도 내역을 함께 갱신해 흐름 단절을 방지합니다.

## 5. 이슈 문서 보안 규칙
- 이슈/리포트/로그 문서에 토큰, 비밀번호, 키 파일, 개인식별정보를 원문으로 기록하지 않습니다.
- 재현에 필요한 값은 마스킹(`****`) 처리 후 공유합니다.
- 외부 공유(이슈 등록/PR 첨부) 전 보안 점검을 완료했는지 확인합니다.
