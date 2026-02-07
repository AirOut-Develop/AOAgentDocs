# 🐙 버전 관리 지침 (Version Control Convention)

## 1. 커밋 메시지 (Commit Message)
- **언어:** 한국어 (제목/본문)
- **형식:** `type: 작업 요약` (예: `feat: 로그인 기능 구현`)
- **타입(Type):**
  - `feat`: 새로운 기능 추가
  - `fix`: 버그 수정
  - `docs`: 문서 수정
  - `style`: 코드 포맷팅 (로직 변경 없음)
  - `refactor`: 코드 리팩토링
  - `test`: 테스트 코드 추가
  - `chore`: 빌드 설정, 의존성/도구 설정 등

## 2. 브랜치 전략 (Branch Strategy)
- **main/master:** 배포 가능한 안정 버전
- **develop:** 개발 통합 브랜치 (선택)
- **feature/*:** 기능 개발 브랜치

## 3. 버전 태그 규칙 (Release Tag)
- 버전 체계는 `SemVer`(`MAJOR.MINOR.PATCH`)를 사용합니다.
- 태그 형식은 `aodocs/vX.Y.Z`를 사용합니다. (예: `aodocs/v1.1.0`)
- 태그 전 `VERSION`, `CHANGELOG.md`, `RELEASE_POLICY.md`를 반드시 동기화합니다.

## 4. 릴리즈 브랜치 운영 (선택)
- 대규모 변경 전에는 `release/vX.Y.Z` 브랜치를 생성해 검증합니다.
- 검증 완료 후 `main` 병합 + 태그 생성 + 배포 산출물(zip) 업로드 순서로 완료합니다.

## 5. 이슈/PR 제출 전 보안 점검
- 이슈 본문, PR 본문, 첨부 파일, 커밋 diff에 시크릿/민감정보가 없는지 확인합니다.
- 필요 시 민감 문자열은 마스킹(`****`) 또는 샘플 값으로 치환합니다.
- 보안 점검이 완료되지 않으면 원격 push 및 PR 생성을 진행하지 않습니다.
