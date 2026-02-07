# 프로젝트 환경 설정 (Project Environment Setup)

> 이 문서는 프로젝트의 개발 환경, 의존성, SDK 버전을 정의합니다.
> 개발 팀원 간의 환경을 일치시키기 위해 필수적으로 참고해야 합니다.

## 1. 기본 정보 (Basic Info)
- **앱 이름**: {App Name}
- **패키지명**: {Package Name} 예: `us.xusx.appname`
- **Minimum SDK**: {API Level} (Android X.X)
- **Target SDK**: {API Level} (Android XX)
- **Language**: Kotlin

## 2. 개발 도구 버전 (IDE & Tools)
- **Android Studio**: {Version Check Required} (예: Koala 2024.1.1 이상)
- **Gradle Plugin**: {Version} (예: 8.5.1)
- **Gradle Wrapper**: {Version} (예: 8.7)
- **JDK (Java Development Kit)**: {Version} (예: jbr-17, Java 17)

## 3. 핵심 라이브러리 (Key Dependencies)
주요 의존성 라이브러리와 버전 정책을 기술합니다.

### Android Jetpack
- `androidx.core:core-ktx:XXX`
- `androidx.appcompat:appcompat:XXX`
- `androidx.constraintlayout:constraintlayout:XXX`
- `androidx.navigation:navigation-fragment-ktx:XXX`
- `androidx.lifecycle:lifecycle-viewmodel-ktx:XXX`

### CameraX (If Applicable)
- `androidx.camera:camera-core:XXX`
- `androidx.camera:camera-camera2:XXX`
- `androidx.camera:camera-lifecycle:XXX`
- `androidx.camera:camera-view:XXX`

### Hardware / USB (If Applicable)
- `usb-serial-for-android` (Optional)

## 4. 환경 변수 및 키 관리 (Env Variables & Keys)
- `local.properties`: SDK 경로 설정 (`sdk.dir=...`)
- `keystore`: 릴리즈 키스토어 파일 위치 및Alias (보안상 값은 기재하지 않음)

## 5. 빌드 변형 (Build Variants)
- **debug**: 개발용, 로그 활성화, 디버그 서명
- **release**: 배포용, Proguard 적용, 릴리즈 서명
