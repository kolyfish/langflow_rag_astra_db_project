# Langflow MCP 案例演示啟動腳本
# 此腳本會檢查環境並執行演示

Write-Host "🚀 啟動 Langflow MCP 案例演示" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# 檢查 Python 是否可用
Write-Host "🔍 檢查 Python 環境..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python 未安裝"
    }
    Write-Host "✅ 找到 Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ 錯誤: 未找到 Python" -ForegroundColor Red
    Write-Host "請先安裝 Python 3.8 或更高版本" -ForegroundColor Yellow
    Read-Host "按 Enter 鍵退出"
    exit 1
}

# 檢查虛擬環境是否存在
Write-Host "🔍 檢查 Langflow 虛擬環境..." -ForegroundColor Yellow
if (!(Test-Path "langflow-env")) {
    Write-Host "❌ 錯誤: 未找到 Langflow 虛擬環境" -ForegroundColor Red
    Write-Host "請先執行 .\install-langflow-mcp.ps1 安裝 Langflow" -ForegroundColor Yellow
    Read-Host "按 Enter 鍵退出"
    exit 1
}

# 啟動虛擬環境
Write-Host "🔧 啟動 Python 虛擬環境..." -ForegroundColor Yellow
& ".\langflow-env\Scripts\Activate.ps1"

# 檢查 Langflow 是否已安裝
Write-Host "🔍 檢查 Langflow 安裝..." -ForegroundColor Yellow
try {
    python -c "import langflow" 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Langflow 未安裝"
    }
    Write-Host "✅ Langflow 已正確安裝" -ForegroundColor Green
} catch {
    Write-Host "❌ 錯誤: Langflow 未正確安裝" -ForegroundColor Red
    Write-Host "請重新執行 .\install-langflow-mcp.ps1" -ForegroundColor Yellow
    Read-Host "按 Enter 鍵退出"
    exit 1
}

# 檢查 Langflow 伺服器是否運行
Write-Host "🔍 檢查 Langflow 伺服器狀態..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:7860/health" -TimeoutSec 5 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Langflow 伺服器運行正常" -ForegroundColor Green
    } else {
        throw "伺服器回應異常"
    }
} catch {
    Write-Host "⚠️  Langflow 伺服器未運行" -ForegroundColor Yellow
    Write-Host "請在另一個 PowerShell 視窗中執行: .\start-langflow-mcp.ps1" -ForegroundColor Yellow
    Write-Host "然後重新運行此演示" -ForegroundColor Yellow
    Read-Host "按 Enter 鍵退出"
    exit 1
}

# 執行演示腳本
Write-Host "🎬 開始執行案例演示..." -ForegroundColor Green
Write-Host ""

try {
    python examples\demo-script.py
    Write-Host ""
    Write-Host "🎉 演示完成！" -ForegroundColor Green
} catch {
    Write-Host ""
    Write-Host "❌ 演示執行過程中發生錯誤: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "按任意鍵退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
