# ✅ 에이전트 온보딩 체크리스트 (Agent Onboarding Checklist)

> 이 체크리스트를 복사하여 작업 문서의 온보딩 절에 작성하세요.
> 체크박스([x])를 모두 채운 후 작업을 시작합니다.

## 🤖 [Agent Name / Session ID]
**작성 일시:** (YYYY-MM-DD HH:MM)
**할당된 작업:** (예: 로그인 기능 구현)

### 1. 📘 핵심 규칙 숙지 (Core Rules)
- [ ] [CONTRIBUTING.md](../CONTRIBUTING.md)를 읽었습니다.
- [ ] [COMMUNICATION.md](./COMMON/COMMUNICATION.md)를 읽었습니다.
- [ ] [VERSION_CONTROL_CONVENTION.md](./COMMON/VERSION_CONTROL_CONVENTION.md)를 읽었습니다.
- [ ] 프로젝트 플랫폼 유형을 확인했습니다.

### 2. 📱 플랫폼별 규칙 확인 (Platform Rules)
- [ ] Android 프로젝트인 경우 [ARCHITECTURE.md](./PLATFORM/ANDROID/ARCHITECTURE.md)를 확인했습니다.
- [ ] 프로젝트별 UI/디버깅 규칙 파일이 있다면 별도로 확인했습니다.

### 3. 🚨 비상 행동 수칙 (Emergency Protocol)
- [ ] 규칙 충돌 시 PLATFORM > COMMON 우선순위를 적용합니다.
- [ ] 충돌 발견 시 `[RULE-CONFLICT]`로 즉시 보고합니다.
- [ ] 작업 완료 전 빌드/테스트 등 검증을 수행합니다.

- [ ] [제품 생명주기](COMMON/DOCUMENT_LIFECYCLE.md)를 확인하고 활성/계획 플랫폼을 구분했습니다.
- [ ] 프로젝트에 `docs/STATUS.md`가 있다면 [세션 인수인계 규칙](COMMON/SESSION_HANDOFF.md)에 따라 확인했습니다.
- [ ] iOS 대상이면 [iOS 지침](PLATFORM/IOS/ARCHITECTURE.md)을 확인했습니다.
