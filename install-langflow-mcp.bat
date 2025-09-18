@echo off
chcp 65001 >nul
echo 開始安裝 Langflow MCP (使用 uv 管理)...

REM 檢查 uv 是否已安裝
echo 檢查 uv 安裝狀態...
uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo uv 未安裝，正在安裝 uv...
    powershell -Command "Invoke-WebRequest -Uri 'https://astral.sh/uv/install.ps1' -OutFile 'install-uv.ps1'; Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force; .\install-uv.ps1; Remove-Item 'install-uv.ps1' -Force"
    if %errorlevel% neq 0 (
        echo 錯誤: uv 安裝失敗
        echo 請手動安裝 uv: curl -LsSf https://astral.sh/uv/install.sh ^| sh
        pause
        exit /b 1
    )
    echo uv 安裝成功
)

REM 創建虛擬環境
echo 創建 Python 虛擬環境...
if exist "langflow-env" (
    echo 虛擬環境已存在，正在移除舊環境...
    rmdir /s /q "langflow-env"
)

uv venv langflow-env
if %errorlevel% neq 0 (
    echo 錯誤: 無法創建虛擬環境
    pause
    exit /b 1
)

REM 創建 pyproject.toml 檔案
echo 創建專案配置文件...
(
echo [project]
echo name = "langflow-mcp"
echo version = "1.0.0"
echo description = "Langflow MCP 插件管理專案"
echo requires-python = "^>=3.8"
echo dependencies = [
echo     "langflow^>=1.0.0",
echo     "mcp",
echo     "requests",
echo     "uvicorn",
echo     "fastapi",
echo     "pydantic"
echo ]
echo.
echo [build-system]
echo requires = ["hatchling"]
echo build-backend = "hatchling.build"
echo.
echo [tool.uv]
echo dev-dependencies = [
echo     "pytest",
echo     "black",
echo     "flake8"
echo ]
) > pyproject.toml

REM 使用 uv 安裝依賴
echo 使用 uv 安裝依賴套件...
uv pip install -e .
if %errorlevel% neq 0 (
    echo 錯誤: 無法安裝依賴套件
    pause
    exit /b 1
)

REM 安裝額外的 MCP 相關套件
echo 安裝 MCP 相關套件...
uv pip install mcp

REM 安裝演示腳本所需的套件
echo 安裝演示腳本所需套件...
uv pip install requests

REM 創建配置目錄
echo 創建配置目錄...
if not exist "config" mkdir config

REM 創建 MCP 配置檔案
echo 創建 MCP 配置檔案...
(
echo {
echo   "mcpServers": {
echo     "langflow": {
echo       "command": "python",
echo       "args": ["-m", "langflow", "run", "--mcp-server"],
echo       "env": {
echo         "LANGFLOW_HOST": "localhost",
echo         "LANGFLOW_PORT": "7860"
echo       }
echo     }
echo   }
echo }
) > config\mcp-config.json

REM 創建啟動腳本
echo 創建啟動腳本...
(
echo @echo off
echo echo 啟動 Langflow MCP 伺服器 (使用 uv)...
echo call langflow-env\Scripts\activate.bat
echo uv run langflow run --mcp-server --host localhost --port 7860
echo pause
) > start-langflow-mcp.bat

echo Langflow MCP 安裝完成！(使用 uv 管理)
echo.
echo 已安裝的套件：
echo - langflow (AI 流程管理)
echo - mcp (Model Context Protocol)
echo - requests (HTTP 客戶端)
echo - uvicorn (ASGI 伺服器)
echo - fastapi (Web 框架)
echo - pydantic (數據驗證)
echo.
echo uv 管理命令：
echo - uv pip list                    # 列出已安裝套件
echo - uv pip install ^<套件名^>        # 安裝新套件
echo - uv pip uninstall ^<套件名^>      # 卸載套件
echo - uv pip install --upgrade ^<套件名^> # 升級套件
echo.
echo 下一步：
echo 1. 執行 start-langflow-mcp.bat 啟動伺服器
echo 2. 在 Cursor 中配置 MCP 客戶端
echo 3. 查看 examples/README.md 了解詳細使用方法
echo.
pause
