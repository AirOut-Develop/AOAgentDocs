# 📘 커뮤니케이션 폴더 운영 가이드

## 1. 구조
```text
docs/communication/
├── 000_README_Communication_Guide.md
├── 001_INDEX.md                         ← WRK+ISS 통합 인덱스
├── 000_Master_Report_Template.md        ← ISS 마스터 리포트
├── 000_Work_Master_Report_Template.md   ← WRK 마스터 리포트
├── ISS_YYMMDD_NNN_hash_Flag_Name_Template.md
├── WRK_YYMMDD_NNN_hash_Name_Template.md
├── 999_Issue_Completed_Template.md
├── 999_Work_Completed_Template.md
├── assets/
├── works/                ← 진행중 작업만
│   └── WRK_YYMMDD_NNN_hash_Name/
│       ├── 000_{WorkName}_Master_Report.md
│       ├── 001_...
│       └── 999_Work_Completed.md
├── issues/               ← 진행중 이슈만
│   └── ISS_YYMMDD_NNN_hash_Flag_Name/
│       ├── 000_{IssueName}_Master_Report.md
│       ├── 001_...
│       └── 999_Issue_Completed.md
└── END/                  ← 완료된 WRK+ISS 아카이브
    ├── WRK_YYMMDD_NNN_hash_Name/
    └── ISS_YYMMDD_NNN_hash_Flag_Name/
```

## 2. 해시 생성 규칙
- `YYMMDD + HHMMSS + random 2자리`의 SHA-256 앞 **6자리**를 사용합니다.
- 해시는 생성 시 **1회 확정**, 문서 평생 **불변**입니다.
- 인덱스 조회 없이 즉시 채번 가능 (충돌 확률 사실상 0).

## 3. 네이밍 규칙
- WRK: `WRK_YYMMDD_NNN_hash_Name`
- ISS: `ISS_YYMMDD_NNN_hash_Flag_Name`
  - `Flag`: `L`(WRK 연계) / `S`(독립)
- `NNN`: 해당 날짜 내 순서 (WRK/ISS 독립 카운트)

## 4. 작업(WRK) 시작 절차
1. 해시 생성
2. `001_INDEX.md`에서 오늘 WRK 마지막 순서 확인 → 다음 NNN 채번
3. `works/WRK_YYMMDD_NNN_hash_Name` 폴더 생성
4. 마스터 리포트 생성, 진행 기록 누적
5. 문제 발생 시 ISS 생성 (아래 §5 참조)
6. 완료 시 `999_Work_Completed.md` 작성 → `END/`로 이동 → 인덱스 갱신

## 5. 이슈(ISS) 시작 절차
1. 해시 생성
2. 플래그 결정: WRK 도중 발생 → `L` / 독립 → `S`
3. `001_INDEX.md`에서 오늘 ISS 마지막 순서 확인 → 다음 NNN 채번
4. `issues/ISS_YYMMDD_NNN_hash_Flag_Name` 폴더 생성
5. 마스터 리포트 생성 (`L`이면 부모 WRK 해시 필수 기재)
6. 부모 WRK 마스터 리포트의 `관련 이슈` 테이블에 등록
7. 시도 기록 누적, 중간 발견 시 즉시 중간 기록
8. 완료 시 `999_Issue_Completed.md` 작성 → `END/`로 이동 → 인덱스 갱신

## 6. 완료 처리
- `999_Completed.md` 작성 후 **즉시 `END/`로 이동**합니다.
- `works/`와 `issues/`에는 항상 **진행중인 항목만** 남습니다.
- 인덱스의 완료 섹션에 `END/` 경로로 갱신합니다.

## 7. 인덱스 규칙
- `001_INDEX.md`에서 WRK와 ISS를 통합 관리합니다.
- 해시가 Primary Key이며, 폴더명의 해시와 1:1 매칭합니다.
