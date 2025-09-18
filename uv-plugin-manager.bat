@echo off
chcp 65001 >nul
echo 🔧 uv 插件管理工具
echo ================================

REM 檢查參數
if "%~1"=="" (
    echo 使用方法: uv-plugin-manager.bat ^<action^> [package] [version]
    echo.
    echo 可用操作:
    echo   install   - 安裝套件
    echo   uninstall - 卸載套件
    echo   list      - 列出已安裝套件
    echo   upgrade   - 升級套件
    echo   sync      - 同步專案依賴
    echo   add       - 添加套件到專案
    echo   remove    - 從專案移除套件
    echo.
    echo 範例:
    echo   uv-plugin-manager.bat install requests
    echo   uv-plugin-manager.bat list
    echo   uv-plugin-manager.bat upgrade langflow
    pause
    exit /b 1
)

REM 檢查虛擬環境是否存在
if not exist "langflow-env" (
    echo ❌ 錯誤: 未找到 Langflow 虛擬環境
    echo 請先執行 install-langflow-mcp.bat 安裝環境
    pause
    exit /b 1
)

REM 啟動虛擬環境
echo 🔧 啟動 Python 虛擬環境...
call langflow-env\Scripts\activate.bat

REM 檢查 uv 是否可用
uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 錯誤: uv 不可用
    echo 請先安裝 uv
    pause
    exit /b 1
)

REM 執行相應的操作
if "%1"=="install" (
    if "%2"=="" (
        echo 📦 安裝專案依賴...
        uv pip install -e .
    ) else (
        echo 📦 安裝套件: %2
        if "%3"=="" (
            uv pip install %2
        ) else (
            uv pip install %2==%3
        )
    )
) else if "%1"=="uninstall" (
    if "%2"=="" (
        echo ❌ 錯誤: 請指定要卸載的套件名稱
    ) else (
        echo 🗑️  卸載套件: %2
        uv pip uninstall %2
    )
) else if "%1"=="list" (
    echo 📋 已安裝的套件列表:
    uv pip list
) else if "%1"=="upgrade" (
    if "%2"=="" (
        echo ⬆️  升級所有套件...
        uv pip install --upgrade -e .
    ) else (
        echo ⬆️  升級套件: %2
        uv pip install --upgrade %2
    )
) else if "%1"=="sync" (
    echo 🔄 同步專案依賴...
    uv pip sync pyproject.toml
) else if "%1"=="add" (
    if "%2"=="" (
        echo ❌ 錯誤: 請指定要添加的套件名稱
    ) else (
        echo ➕ 添加套件到專案: %2
        if "%3"=="" (
            uv add %2
        ) else (
            uv add %2==%3
        )
    )
) else if "%1"=="remove" (
    if "%2"=="" (
        echo ❌ 錯誤: 請指定要移除的套件名稱
    ) else (
        echo ➖ 從專案移除套件: %2
        uv remove %2
    )
) else (
    echo ❌ 錯誤: 未知操作 '%1'
    echo 請使用 'uv-plugin-manager.bat' 查看可用操作
)

echo.
echo ✅ 操作完成！
echo.
echo 💡 使用範例:
echo   uv-plugin-manager.bat install requests
echo   uv-plugin-manager.bat list
echo   uv-plugin-manager.bat upgrade langflow
echo   uv-plugin-manager.bat add numpy
echo.
pause
