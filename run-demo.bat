@echo off
chcp 65001 >nul
echo 🚀 啟動 Langflow MCP 案例演示
echo ========================================

REM 檢查 Python 是否可用
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 錯誤: 未找到 Python
    echo 請先安裝 Python 3.8 或更高版本
    pause
    exit /b 1
)

REM 檢查虛擬環境是否存在
if not exist "langflow-env" (
    echo ❌ 錯誤: 未找到 Langflow 虛擬環境
    echo 請先執行 install-langflow-mcp.bat 安裝 Langflow
    pause
    exit /b 1
)

REM 啟動虛擬環境
echo 🔧 啟動 Python 虛擬環境...
call langflow-env\Scripts\activate.bat

REM 檢查 Langflow 是否已安裝
python -c "import langflow" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 錯誤: Langflow 未正確安裝
    echo 請重新執行 install-langflow-mcp.bat
    pause
    exit /b 1
)

REM 檢查 Langflow 伺服器是否運行
echo 🔍 檢查 Langflow 伺服器狀態...
python -c "import requests; requests.get('http://localhost:7860/health', timeout=5)" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Langflow 伺服器未運行，正在啟動...
    echo 請在另一個命令提示字元中執行: start-langflow-mcp.bat
    echo 然後重新運行此演示
    pause
    exit /b 1
)

echo ✅ Langflow 伺服器運行正常

REM 執行演示腳本
echo 🎬 開始執行案例演示...
echo.
python examples\demo-script.py

echo.
echo 🎉 演示完成！
echo 按任意鍵退出...
pause >nul
