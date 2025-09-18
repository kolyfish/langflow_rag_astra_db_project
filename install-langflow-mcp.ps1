# Langflow MCP 安裝腳本 (使用 uv 管理)
# 此腳本將安裝 Langflow 並配置 MCP 功能

Write-Host "開始安裝 Langflow MCP (使用 uv 管理)..." -ForegroundColor Green

# 檢查 uv 是否已安裝
Write-Host "檢查 uv 安裝狀態..." -ForegroundColor Yellow
try {
    $uvVersion = uv --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "uv 未安裝"
    }
    Write-Host "找到 uv: $uvVersion" -ForegroundColor Green
} catch {
    Write-Host "uv 未安裝，正在安裝 uv..." -ForegroundColor Yellow
    try {
        # 使用 PowerShell 安裝 uv
        Invoke-WebRequest -Uri "https://astral.sh/uv/install.ps1" -OutFile "install-uv.ps1"
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
        .\install-uv.ps1
        Remove-Item "install-uv.ps1" -Force
        
        # 重新載入環境變數
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
        
        # 驗證安裝
        $uvVersion = uv --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ uv 安裝成功: $uvVersion" -ForegroundColor Green
        } else {
            throw "uv 安裝失敗"
        }
    } catch {
        Write-Host "❌ uv 安裝失敗，請手動安裝 uv" -ForegroundColor Red
        Write-Host "安裝命令: curl -LsSf https://astral.sh/uv/install.sh | sh" -ForegroundColor Yellow
        Write-Host "或訪問: https://docs.astral.sh/uv/getting-started/installation/" -ForegroundColor Yellow
        exit 1
    }
}

# 創建專案目錄和虛擬環境
Write-Host "創建專案目錄和虛擬環境..." -ForegroundColor Yellow
if (Test-Path "langflow-env") {
    Write-Host "虛擬環境已存在，正在移除舊環境..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "langflow-env"
}

# 使用 uv 創建虛擬環境
uv venv langflow-env
if ($LASTEXITCODE -ne 0) {
    Write-Host "錯誤: 無法創建虛擬環境" -ForegroundColor Red
    exit 1
}

# 創建 pyproject.toml 檔案
Write-Host "創建專案配置文件..." -ForegroundColor Yellow
$pyprojectContent = @"
[project]
name = "langflow-mcp"
version = "1.0.0"
description = "Langflow MCP 插件管理專案"
requires-python = ">=3.8"
dependencies = [
    "langflow>=1.0.0",
    "mcp",
    "requests",
    "uvicorn",
    "fastapi",
    "pydantic"
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
    "pytest",
    "black",
    "flake8"
]
"@

$pyprojectContent | Out-File -FilePath "pyproject.toml" -Encoding UTF8

# 使用 uv 安裝依賴
Write-Host "使用 uv 安裝依賴套件..." -ForegroundColor Yellow
uv pip install -e .
if ($LASTEXITCODE -ne 0) {
    Write-Host "錯誤: 無法安裝依賴套件" -ForegroundColor Red
    exit 1
}

# 安裝額外的 MCP 相關套件
Write-Host "安裝 MCP 相關套件..." -ForegroundColor Yellow
uv pip install mcp

# 安裝演示腳本所需的套件
Write-Host "安裝演示腳本所需套件..." -ForegroundColor Yellow
uv pip install requests

# 創建配置目錄
Write-Host "創建配置目錄..." -ForegroundColor Yellow
if (!(Test-Path "config")) {
    New-Item -ItemType Directory -Path "config"
}

# 創建 MCP 配置檔案
Write-Host "創建 MCP 配置檔案..." -ForegroundColor Yellow
$mcpConfig = @"
{
  "mcpServers": {
    "langflow": {
      "command": "python",
      "args": ["-m", "langflow", "run", "--mcp-server"],
      "env": {
        "LANGFLOW_HOST": "localhost",
        "LANGFLOW_PORT": "7860"
      }
    }
  }
}
"@

$mcpConfig | Out-File -FilePath "config\mcp-config.json" -Encoding UTF8

# 創建啟動腳本
Write-Host "創建啟動腳本..." -ForegroundColor Yellow
$startScript = @"
@echo off
echo 啟動 Langflow MCP 伺服器 (使用 uv)...
call langflow-env\Scripts\activate.bat
uv run langflow run --mcp-server --host localhost --port 7860
pause
"@

$startScript | Out-File -FilePath "start-langflow-mcp.bat" -Encoding UTF8

# 創建 PowerShell 啟動腳本
$startScriptPs = @"
# 啟動 Langflow MCP 伺服器 (使用 uv)
Write-Host "啟動 Langflow MCP 伺服器 (使用 uv)..." -ForegroundColor Green
& ".\langflow-env\Scripts\Activate.ps1"
uv run langflow run --mcp-server --host localhost --port 7860
"@

$startScriptPs | Out-File -FilePath "start-langflow-mcp.ps1" -Encoding UTF8

# 創建範例配置
Write-Host "創建範例配置..." -ForegroundColor Yellow
$exampleConfig = @"
# Langflow MCP 範例配置

## 基本使用

1. 啟動 Langflow MCP 伺服器：
   ```powershell
   .\start-langflow-mcp.ps1
   ```

2. 在 Cursor 中配置 MCP 客戶端：
   - 打開 Cursor 設定
   - 添加 MCP 伺服器配置
   - 使用以下配置：
     ```json
     {
       "mcpServers": {
         "langflow": {
           "command": "python",
           "args": ["-m", "langflow", "run", "--mcp-server"],
           "cwd": "C:\Users\WUYUEH\cursor_project"
         }
       }
     }
     ```

## MCP 功能

Langflow MCP 提供以下功能：
- 流程管理
- 工具集成
- 代理配置
- 數據源連接

## 故障排除

如果遇到問題：
1. 確保虛擬環境已啟動
2. 檢查 Python 版本 (需要 3.8+)
3. 確保所有依賴已正確安裝
4. 檢查端口 7860 是否被占用
"@

$exampleConfig | Out-File -FilePath "langflow-mcp-example.md" -Encoding UTF8

Write-Host "Langflow MCP 安裝完成！(使用 uv 管理)" -ForegroundColor Green
Write-Host ""
Write-Host "📦 已安裝的套件："
Write-Host "- langflow (AI 流程管理)" -ForegroundColor Cyan
Write-Host "- mcp (Model Context Protocol)" -ForegroundColor Cyan
Write-Host "- requests (HTTP 客戶端)" -ForegroundColor Cyan
Write-Host "- uvicorn (ASGI 伺服器)" -ForegroundColor Cyan
Write-Host "- fastapi (Web 框架)" -ForegroundColor Cyan
Write-Host "- pydantic (數據驗證)" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔧 uv 管理命令："
Write-Host "- uv pip list                    # 列出已安裝套件" -ForegroundColor Yellow
Write-Host "- uv pip install <套件名>        # 安裝新套件" -ForegroundColor Yellow
Write-Host "- uv pip uninstall <套件名>      # 卸載套件" -ForegroundColor Yellow
Write-Host "- uv pip install --upgrade <套件名> # 升級套件" -ForegroundColor Yellow
Write-Host ""
Write-Host "下一步："
Write-Host "1. 執行 .\start-langflow-mcp.ps1 啟動伺服器" -ForegroundColor Yellow
Write-Host "2. 在 Cursor 中配置 MCP 客戶端" -ForegroundColor Yellow
Write-Host "3. 查看 examples/README.md 了解詳細使用方法" -ForegroundColor Yellow
Write-Host ""
Write-Host "按任意鍵繼續..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
