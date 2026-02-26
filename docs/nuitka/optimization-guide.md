# Nuitka 최적화 및 빌드 가이드 (Python 3.14.2)

[System-Context]
- Environment: Windows 11
- Target Python: 3.14.2
- Compiler: MSVC (Visual Studio 2022+)

## 1. Python 3.14.2 호환성
Python 3.14.2의 최신 바이트코드 아키텍처 변화로 인해 Nuitka는 **반복 최적화(Iterative Optimization)**를 더 깊이 수행하게 됩니다. 
의존성 추적 및 캐시 생성 과정에서 상당히 높은 메모리와 안정적인 MSVC 컴파일러 구성이 필수적입니다.

## 2. 빌드 정체 대응 (Not finished with the module)
분석(Analyzing) 과정이 90% 이상 구간에서 정체되거나, "Not finished with the module" 혹은 유사한 메시지가 발생한 상태로 무한 반복될 수 있습니다. 
이러한 상황에서는 다음 옵션들을 명령에 포함하여 세부 로그를 반드시 노출시켜야 합니다.

- **`--show-progress`**: 컴파일 과정의 세부 단계를 강제로 출력하여 어디서 멈추었는지 물리적 식별
- **`--show-memory`**: 메모리 할당량을 관찰하여, Out of Memory로 인한 무한 루프인지 확인

## 3. 표준 빌드 명령 구조 (PowerShell)
다음은 Windows 11 환경에서 보안 옵션 및 부가 콘솔 창이 없는 단일 실행 파일(`.exe`)을 생성하기 위한 핵심 템플릿입니다.

```powershell
python -m nuitka `
    --standalone `
    --onefile `
    --windows-disable-console `
    --output-dir=dist `
    {main_script_path}
```

> **[CAUTION]** 환경에 따라 백신(Windows Defender 등)의 감시 및 탐지로 인하여 최종 링링 과정이 취소되거나 파일이 삭제될 수 있습니다. **빌드를 수행하기 전 C:\develop 디렉토리 및 프로젝트 `dist/` 내부를 백신 검사 예외 디렉토리로 설정**할 것을 명확히 권고해야 합니다.
