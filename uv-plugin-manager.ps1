# uv 插件管理腳本
# 用於管理 Langflow MCP 專案的 Python 套件

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("install", "uninstall", "list", "upgrade", "sync", "add", "remove")]
    [string]$Action,
    
    [Parameter(Mandatory=$false)]
    [string]$Package,
    
    [Parameter(Mandatory=$false)]
    [string]$Version
)

Write-Host "🔧 uv 插件管理工具" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# 檢查虛擬環境是否存在
if (!(Test-Path "langflow-env")) {
    Write-Host "❌ 錯誤: 未找到 Langflow 虛擬環境" -ForegroundColor Red
    Write-Host "請先執行 .\install-langflow-mcp.ps1 安裝環境" -ForegroundColor Yellow
    exit 1
}

# 啟動虛擬環境
Write-Host "🔧 啟動 Python 虛擬環境..." -ForegroundColor Yellow
& ".\langflow-env\Scripts\Activate.ps1"

# 檢查 uv 是否可用
try {
    $uvVersion = uv --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "uv 不可用"
    }
    Write-Host "✅ 使用 uv: $uvVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ 錯誤: uv 不可用" -ForegroundColor Red
    Write-Host "請先安裝 uv" -ForegroundColor Yellow
    exit 1
}

# 執行相應的操作
switch ($Action) {
    "install" {
        if ($Package) {
            Write-Host "📦 安裝套件: $Package" -ForegroundColor Yellow
            if ($Version) {
                uv pip install "${Package}==${Version}"
            } else {
                uv pip install $Package
            }
        } else {
            Write-Host "📦 安裝專案依賴..." -ForegroundColor Yellow
            uv pip install -e .
        }
    }
    
    "uninstall" {
        if ($Package) {
            Write-Host "🗑️  卸載套件: $Package" -ForegroundColor Yellow
            uv pip uninstall $Package
        } else {
            Write-Host "❌ 錯誤: 請指定要卸載的套件名稱" -ForegroundColor Red
        }
    }
    
    "list" {
        Write-Host "📋 已安裝的套件列表:" -ForegroundColor Yellow
        uv pip list
    }
    
    "upgrade" {
        if ($Package) {
            Write-Host "⬆️  升級套件: $Package" -ForegroundColor Yellow
            uv pip install --upgrade $Package
        } else {
            Write-Host "⬆️  升級所有套件..." -ForegroundColor Yellow
            uv pip install --upgrade -e .
        }
    }
    
    "sync" {
        Write-Host "🔄 同步專案依賴..." -ForegroundColor Yellow
        uv pip sync pyproject.toml
    }
    
    "add" {
        if ($Package) {
            Write-Host "➕ 添加套件到專案: $Package" -ForegroundColor Yellow
            if ($Version) {
                uv add "${Package}==${Version}"
            } else {
                uv add $Package
            }
        } else {
            Write-Host "❌ 錯誤: 請指定要添加的套件名稱" -ForegroundColor Red
        }
    }
    
    "remove" {
        if ($Package) {
            Write-Host "➖ 從專案移除套件: $Package" -ForegroundColor Yellow
            uv remove $Package
        } else {
            Write-Host "❌ 錯誤: 請指定要移除的套件名稱" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "✅ 操作完成！" -ForegroundColor Green
Write-Host ""
Write-Host "💡 使用範例:" -ForegroundColor Cyan
Write-Host "  .\uv-plugin-manager.ps1 -Action install -Package requests" -ForegroundColor Gray
Write-Host "  .\uv-plugin-manager.ps1 -Action list" -ForegroundColor Gray
Write-Host "  .\uv-plugin-manager.ps1 -Action upgrade -Package langflow" -ForegroundColor Gray
Write-Host "  .\uv-plugin-manager.ps1 -Action add -Package numpy" -ForegroundColor Gray
