# 📜 Antigravity Standard Rules Index

## ⚖️ 규칙 우선순위 및 충돌 해결 (Priority & Conflict)
프로젝트 자체 지침과 상위 지침이 우선합니다. 선택한 범위 안에서는 다음 순서를 따릅니다.
1. 플랫폼별 지침 (PLATFORM)
2. 공통 지침 (COMMON)

규칙 충돌이 발견되면 `[RULE-CONFLICT]` 태그로 즉시 보고하고 플랫폼 지침을 우선 적용합니다.

---

## 🌐 공통 지침 (COMMON)
- [COMMUNICATION.md](./COMMON/COMMUNICATION.md): 소통, 문서 작성, 협업 규칙
- [VERSION_CONTROL_CONVENTION.md](./COMMON/VERSION_CONTROL_CONVENTION.md): 버전 관리, 커밋 메시지 규칙
- [CODE_ETHICS.md](./COMMON/CODE_ETHICS.md): 코드 명명, 주석, 검증 태도

## 📱 플랫폼별 지침 (PLATFORM)
### Android
- [ARCHITECTURE.md](./PLATFORM/ANDROID/ARCHITECTURE.md): 네이티브 책임·생명주기·검증 경계

### Web
- [ARCHITECTURE.md](./PLATFORM/WEB/ARCHITECTURE.md): 브라우저 책임·보안·검증 경계

### Server
- [ARCHITECTURE.md](./PLATFORM/SERVER/ARCHITECTURE.md): API·계정·데이터·운영 경계

## 제품 생명주기
- [DOCUMENT_LIFECYCLE.md](COMMON/DOCUMENT_LIFECYCLE.md) — PRD/계획/검증 연결
- [SESSION_HANDOFF.md](COMMON/SESSION_HANDOFF.md) — 새 세션 재개·현황보고·다음 작업 대기열

## iOS
- [ARCHITECTURE.md](PLATFORM/IOS/ARCHITECTURE.md) — 네이티브 적용 규칙
