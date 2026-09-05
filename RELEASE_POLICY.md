# AOAgentDocs 릴리스 정책

## 버전
- MAJOR: 기존 계약/구조의 비호환 변경.
- MINOR: 기존 기록을 유지하는 선택적 기능/가이드 추가 (이번 1.3.0).
- PATCH: 버그·문구·링크 수정.
- VERSION이 정본이며 README/CHANGELOG/ROADMAP을 함께 갱신한다.

## 태그와 산출물
- 태그: `aodocs/vX.Y.Z`
- ZIP: `dist/AOAgentDocs_vX.Y.Z.zip`, 내부 root `AOAgentDocs/`.
- `python3 scripts/release_package.py`가 kit-files.json의 명시 목록만 포함한다.
- POSIX: `bash scripts/release_package.sh`, Windows: `pwsh -File scripts/release_package.ps1`.
- Windows wrapper에는 Python 3.10+가 필요하다. 확인하지 않은 OS 실행 결과는 미검증으로 남긴다.

## 릴리스 게이트
1. 테스트를 먼저 작성하고 실패→수정→통과 기록을 남긴다.
2. `python3 -m unittest discover -s tests -v`와 Python 문법/shell syntax 검사를 수행한다.
3. 배포 문서 상대 링크와 버전 일관성을 점검한다.
4. ZIP을 풀어 신규 설치/dry-run/멱등성/관리 파일 충돌/legacy 파일 보존/validate를 시험한다.
5. 비밀/PII/실제 제품 로그가 payload에 없음을 검토한다. hash는 시크릿 감사를 대체하지 않는다.
6. 실제 소비자 도입에서 기존 코드·문서 보존과 등록 문서 검증을 확인한다.
7. source commit과 검증 기록을 커밋하고 태그를 만든다. 공개 상태는 push/업로드 후 따로 확인한다.

## 제외와 한계

킷 배포에 `.git`, `.omc`, `.omx`, `.codex`, `.superpowers`, 로컬 환경·노트,
제품 docs 이력·tests·서버 데이터는 포함하지 않는다. 명시 목록의 추가도 보안 검토 대상이다.
validate는 기록된 evidence와 링크를 검사할 뿐 실제 제품 테스트/승인 진위를 확인하지 않는다.
기존 root 설치/조직 포크를 자동으로 병합하지 않는다. 동시 설치/원자적 rollback은 지원하지 않는다.
실패 시 변경 목록과 Git diff를 확인한 뒤 정확한 범위에서 복구한다.
