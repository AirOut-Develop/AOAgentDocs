# AOAgentDocs

**1.3.0 · PRD부터 개발·검증·배포까지 연결하는 재사용 문서 킷**

WRK(작업)·ISS(이슈)의 기록 체계를 유지하며, 요구사항과 실제 검증 근거를 연결합니다.
서버/iOS/Android/Web을 함께 선택할 수 있습니다. UI 프레임워크나 에이전트 실행 도구를 강제하지 않습니다.

## 빠른 시작 — 기존 프로젝트를 덮어쓰지 않습니다

Python **3.10 이상**이 필요하며 추가 패키지는 없습니다. 먼저 신뢰할 수 있는 소스를 확인하세요.

```bash
git clone https://github.com/AirOut-Develop/AOAgentDocs.git
cd AOAgentDocs
# 정확한 버전은 태그 aodocs/v1.3.0 또는 검토한 커밋으로 고정하세요.
python3 scripts/aodocs.py install /path/to/project --profile server --profile ios
# 위 명령은 dry-run: 변경 목록만 확인합니다.
python3 scripts/aodocs.py install /path/to/project --profile server --profile ios --apply
python3 scripts/aodocs.py validate /path/to/project
```

Windows에서는 `python3` 대신 `py -3`를 사용할 수 있습니다.
ZIP을 받은 경우 `AOAgentDocs/`를 프로젝트 **바깥**에 풀고 같은 명령을 실행합니다.
원본 킷과 대상 프로젝트 경로가 겹치면 설치를 거부합니다.

### 설치 결과와 소유권

```text
<project>/
  .aodocs/
    kit/                  # 배포 규칙·템플릿·도구 (관리 파일; 직접 편집 금지)
    manifest.json         # 설치 버전·파일 hash (설치기 소유)
    project.json          # 현재/계획 플랫폼 (프로젝트 소유)
    documents.json        # 문서 ID·상태·연결 (프로젝트 소유)
  docs/                   # 실제 PRD·계획·이력은 기존 위치 그대로
```

기존 `README.md`, `AGENTS.md`, `CLAUDE.md`, `RULES/`, `.aodocs_version`, 이력은 보존합니다.
자동으로 프로젝트의 규칙 우선순위를 바꾸지 않습니다. 프로젝트 문서 지도에
`.aodocs/kit/RULES/COMMON/DOCUMENT_LIFECYCLE.md`와 `.aodocs/documents.json` 링크를 추가하세요.
`.aodocs/`는 공유할 문서/도구이므로 Git에 추적합니다. 민감정보를 넣지 마세요.

## 설치 후 첫 PRD 등록

1. [생명주기 규칙](RULES/COMMON/DOCUMENT_LIFECYCLE.md)을 읽습니다.
2. [양식 안내](examples/lifecycle/README.md)의 PRD/계획/검증 양식을 필요한 것만 복사합니다.
3. `.aodocs/documents.json`에 문서 경로, 요구사항 ID, 참조를 등록합니다.
4. `python3 .aodocs/kit/scripts/aodocs.py validate .`로 확인합니다.
5. 실제 구현/테스트 뒤에만 검증 결과를 갱신합니다.

**문서 검사 성공은 로그인이나 앱 기능 성공이 아닙니다.** 빈 registry도 설치 검사는 통과합니다.
오탈자·작은 수정마다 PRD를 만들 필요는 없습니다.

## 에이전트에게 요청하기

```text
AOAgentDocs 1.3을 이 프로젝트에 비파괴 설치해주세요.
원본 킷은 프로젝트 외부에 두고 install dry-run부터 실행하세요.
기존 지침/이력은 덮어쓰지 말고 활성 플랫폼과 계획 플랫폼을 분리하세요.
제품 PRD 한 건을 실제 계획·이슈·검증 기록과 연결하고 validate를 실행하세요.
검증된 내용과 미검증 기능을 구분해 보고하세요.
```

## 안전한 업그레이드

같은 install 명령으로 최신 킷을 적용합니다. 같은 버전이어도 파일 hash를 확인합니다.
관리 파일이 수정됐거나 새 payload에서 사라지면 변경 전에 중단합니다. 강제 덮어쓰기는 없습니다.
사용자 소유 project/documents metadata는 자동으로 바꾸지 않습니다.
과거 root 복사 설치(1.2)는 그대로 두고 `.aodocs/kit`을 추가하며, 실제 참조 이관은 사람이 검토합니다.
자세한 절차: [신규 설치](MIGRATION_PROMPT.txt), [업그레이드](UPGRADE_PROMPT.txt).

## 무엇이 연결되나요?

`PRD 요구사항 → 설계/ADR → PLAN·WRK·ISS → 소스 커밋 → 검증 증거 → 릴리스`

- 승인 문서: 누가 어느 revision을 검토했는지.
- 완료 작업: 어떤 요구사항을 어떤 passed 검증으로 확인했는지.
- 배포: iOS/Android/서버 각각 실제 배포 여부.
- 과거 WRK/ISS ID와 END 이력은 자동 이동/재명명하지 않습니다.
- 짧은 해시도 중복 검사가 필요합니다. 무충돌을 가정하지 않습니다.

## 킷 개발·배포

```bash
python3 -m unittest discover -s tests -v
python3 scripts/release_package.py
# dist/AOAgentDocs_v1.3.0.zip
```

[배포 정책](RELEASE_POLICY.md) · [변경 이력](CHANGELOG.md) · [로드맵](ROADMAP.md)

ZIP은 [명시적 payload 목록](kit-files.json)만 포함합니다. 원본 저장소의 제품 이력·tests·로컬
노트·에이전트 런타임은 배포하지 않습니다. POSIX/PowerShell wrapper도 동일한 Python packager를 씁니다.

첫 도입 검증: AOCortexAPI의 server+iOS, 향후 Android를 대상으로 검증합니다.
자세한 개발/검증 기록은 원본 저장소 docs에 남기며 킷 사용자에게 강제로 설치하지 않습니다.
