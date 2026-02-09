# WRK_YYMMDD_NNN_hash_Name_Template (작업 생성 체크 템플릿)

## 1. 해시 생성
- `YYMMDD + HHMMSS + random 2자리`의 SHA-256 앞 6자리를 해시로 사용
- 예시: `e1b8a0`

## 2. 작업 폴더 생성
- `001_INDEX.md`에서 오늘 날짜의 마지막 WRK 순서를 확인
- 폴더명: `works/WRK_YYMMDD_NNN_hash_Name`
  - `YYMMDD`: 생성 날짜
  - `NNN`: 해당 날짜 내 WRK 순서 (001, 002...)
  - `hash`: 6자리 고유 해시
  - `Name`: 작업명 (PascalCase 권장)
- 예시: `works/WRK_260209_001_e1b8a0_LoginImpl`

## 3. 마스터 리포트 생성
- `000_Work_Master_Report_Template.md`를 복사
- 파일명: `000_{WorkName}_Master_Report.md`

## 4. 진행 기록
- `001_{StepName}.md`, `002_{StepName}.md` 순서로 기록
- 문제 발생 시 ISS 이슈를 생성하고 마스터 리포트의 `관련 이슈` 테이블에 등록

## 5. 완료 처리
- `999_Work_Completed_Template.md`를 복사해 `999_Work_Completed.md` 생성
- 관련 ISS의 완료 상태 확인
- 폴더를 `END/`로 이동
- `001_INDEX.md` 갱신
