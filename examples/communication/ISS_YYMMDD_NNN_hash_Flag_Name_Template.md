# ISS_YYMMDD_NNN_hash_Flag_Name_Template (이슈 생성 체크 템플릿)

## 1. 해시 생성
- `YYMMDD + HHMMSS + random 2자리`의 SHA-256 앞 6자리를 해시로 사용
- 예시: `a3f2b1`

## 2. 플래그 결정
- `L` (Linked): WRK 작업 도중 발생한 이슈 → 부모 WRK 해시 필수 기재
- `S` (Standalone): WRK 없이 독립적으로 발생한 이슈

## 3. 이슈 폴더 생성
- `001_INDEX.md`에서 오늘 날짜의 마지막 ISS 순서를 확인
- 폴더명: `issues/ISS_YYMMDD_NNN_hash_Flag_Name`
- 예시: `issues/ISS_260209_001_a3f2b1_L_CameraFix`

## 4. 마스터 리포트 생성
- `000_Master_Report_Template.md`를 복사
- 파일명: `000_{IssueName}_Master_Report.md`
- **L 플래그인 경우**: `부모 작업` 필드에 WRK 해시를 반드시 기재
- 부모 WRK의 마스터 리포트 `관련 이슈` 테이블에도 이 ISS를 등록

## 5. 상세 시도 문서 생성
- `assets/001_Attempt_Log_Template.md`를 복사
- 파일명: `001_{AttemptName}.md`, `002_{AttemptName}.md` ...

## 6. 완료 처리
- `999_Issue_Completed_Template.md`를 복사해 `999_Issue_Completed.md` 생성
- 폴더를 `END/`로 이동
- `001_INDEX.md` 갱신
- **L 플래그인 경우**: 부모 WRK 마스터 리포트의 `관련 이슈` 상태를 갱신
