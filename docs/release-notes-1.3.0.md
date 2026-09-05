# AOAgentDocs 1.3.0

기존 WRK/ISS를 유지하며 PRD → 설계 → 개발 계획 → 검증 → 릴리스를 연결합니다.

- 프로젝트별 server/iOS/Android/Web 범위와 활성/계획 플랫폼 구분
- 기존 지침·이력을 덮어쓰지 않는 `.aodocs/kit` 설치
- 기본 dry-run, 수정 충돌/경로 탈출/심볼릭 링크/다운그레이드 방지
- 문서 ID/참조/상태/완료 근거/관리 파일 무결성 검사
- 명시적 파일 목록으로 재현 가능한 ZIP 배포
- AOCortexAPI 첫 소비자에서 실제 ZIP 설치·기존 파일 보존·회귀 검증

Python 3.10+만 필요합니다. README의 태그 고정 clone 또는 첨부 ZIP에서
`python3 scripts/aodocs.py install TARGET`으로 시작하세요. 변경 적용은 `--apply`가 필요합니다.

기존 root `.aodocs_version`/RULES/CONTRIBUTING과 WRK/ISS/END는 자동 변환하지 않습니다.
문서 검사 통과와 실제 제품 테스트 통과는 다릅니다. native Windows/macOS 실행은 별도 검증 대상입니다.
