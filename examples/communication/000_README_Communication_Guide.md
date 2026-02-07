# 📘 커뮤니케이션 폴더 운영 가이드

## 1. 구조
```text
docs/communication/
├── 000_README_Communication_Guide.md
├── 001_ISSUE_INDEX.md
├── 000_Master_Report_Template.md
├── ISS_YYMMDD_NNN_Name_Template.md
├── 999_Issue_Completed_Template.md
├── assets/
└── issues/
    └── ISS_YYMMDD_NNN_Name/
        ├── 000_{IssueName}_Master_Report.md
        ├── 001_...
        ├── ...
        └── 999_Issue_Completed.md
```

## 2. 시작 절차
1. `001_ISSUE_INDEX.md` 확인
2. 신규 이슈 폴더(`issues/ISS_YYMMDD_NNN_Name`) 생성
3. `000_Master_Report_Template.md`로 마스터 리포트 생성
4. `001_...`, `002_...` 순서로 상세 기록
5. 중요한 발견이 나오면 종료까지 기다리지 말고 즉시 `00x_...` 문서와 마스터 리포트를 중간 갱신
6. 이슈 완료 시 `999_Issue_Completed_Template.md`로 완료 문서 생성
7. 인덱스(활성/완료 표) 갱신

## 3. 인덱스 생성 규칙
- 템플릿 `001_ISSUE_INDEX.md`를 프로젝트의 `docs/communication/001_ISSUE_INDEX.md`로 복사
- 활성 이슈/완료 이슈를 항상 최신으로 유지
