@echo off
chcp 65001 >nul
echo 🔧 修復 requests 套件問題
echo ================================

REM 檢查虛擬環境是否存在
if not exist "langflow-env" (
    echo ❌ 錯誤: 未找到 Langflow 虛擬環境
    echo 請先執行 install-langflow-mcp.bat
    pause
    exit /b 1
)

REM 啟動虛擬環境
echo 🔧 啟動 Python 虛擬環境...
call langflow-env\Scripts\activate.bat

REM 安裝 requests 套件
echo 📦 安裝 requests 套件...
pip install requests

REM 驗證安裝
echo ✅ 驗證 requests 安裝...
python -c "import requests; print('requests 版本:', requests.__version__)"

if %errorlevel% equ 0 (
    echo ✅ requests 套件安裝成功！
    echo 現在可以運行演示腳本了
) else (
    echo ❌ requests 套件安裝失敗
)

echo.
pause
