# 修復 requests 套件問題的 PowerShell 腳本
Write-Host "🔧 修復 requests 套件問題" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# 檢查虛擬環境是否存在
if (!(Test-Path "langflow-env")) {
    Write-Host "❌ 錯誤: 未找到 Langflow 虛擬環境" -ForegroundColor Red
    Write-Host "請先執行 .\install-langflow-mcp.ps1" -ForegroundColor Yellow
    Read-Host "按 Enter 鍵退出"
    exit 1
}

# 啟動虛擬環境
Write-Host "🔧 啟動 Python 虛擬環境..." -ForegroundColor Yellow
& ".\langflow-env\Scripts\Activate.ps1"

# 安裝 requests 套件
Write-Host "📦 安裝 requests 套件..." -ForegroundColor Yellow
pip install requests

# 驗證安裝
Write-Host "✅ 驗證 requests 安裝..." -ForegroundColor Yellow
try {
    $version = python -c "import requests; print('requests 版本:', requests.__version__)" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ requests 套件安裝成功！" -ForegroundColor Green
        Write-Host $version -ForegroundColor Green
        Write-Host "現在可以運行演示腳本了" -ForegroundColor Green
    } else {
        Write-Host "❌ requests 套件安裝失敗" -ForegroundColor Red
        Write-Host $version -ForegroundColor Red
    }
} catch {
    Write-Host "❌ 驗證過程中發生錯誤: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Read-Host "按 Enter 鍵退出"
