# AOAgentDocs 1.3.1

첫 소비자 AOCortexAPI의 실제 Git 등록에서 발견한 줄바꿈/hash 문제를 수정했습니다.

- `.aodocs/.gitattributes`가 관리 킷과 속성 파일 자체의 Git 줄바꿈 변환을 방지합니다.
- 기존 속성 파일이 다르면 덮어쓰지 않고 충돌로 중단합니다.
- 1.3.1 validator가 보호 속성 파일까지 검사합니다.
- 실제 `core.autocrlf=true` Git add/commit/clone 후 설치 파일 hash와 validate를 검증했습니다.
- 이미 변환된 1.3.0 checkout도 원래 hash와 대조해 줄바꿈만 복구합니다. 실제 내용 수정은 거부합니다.
- 전체 킷 테스트 85개 통과. 기존 1.3.0 태그/ZIP은 보존합니다.

태그 `aodocs/v1.3.1` 또는 첨부 ZIP에서 기존 install dry-run/apply 명령을 실행하세요.
PRD·계획·프로젝트 지침·WRK/ISS 이력은 덮어쓰지 않습니다.
문서 검사 성공은 제품 기능 테스트 성공과 다릅니다. native Windows/macOS 실행은 별도 검증 대상입니다.
