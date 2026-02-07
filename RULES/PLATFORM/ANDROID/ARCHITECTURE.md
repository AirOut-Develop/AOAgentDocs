# 🏗️ 안드로이드 아키텍처 가이드 (Android Architecture)

## 1. 기술 스택
- **언어:** Kotlin (100%)
- **UI:** XML Layout (View System)
- **권장 패턴:** MVVM (Model-View-ViewModel)

## 2. 레이어 구조 (Layer Structure)
- **ui:** Activity, Fragment (UI 로직)
- **viewmodel:** ViewModel (상태 관리, 비즈니스 로직 연결)
- **data:** Repository, DataSource, Model (데이터 처리)

## 3. 상태 관리
- **전역 상태:** Singleton (object) 패턴 사용 권장.
- **UI 상태:** LiveData 또는 StateFlow 사용.
