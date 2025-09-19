# Langflow MCP 設置腳本
# 請確保已安裝 Node.js 後再執行此腳本

Write-Host "🚀 開始設置 Langflow MCP 伺服器..." -ForegroundColor Green

# 檢查 Node.js 是否已安裝
try {
    $nodeVersion = node --version
    $npmVersion = npm --version
    Write-Host "✅ Node.js 版本: $nodeVersion" -ForegroundColor Cyan
    Write-Host "✅ npm 版本: $npmVersion" -ForegroundColor Cyan
} catch {
    Write-Host "❌ 未找到 Node.js 或 npm。請先安裝 Node.js。" -ForegroundColor Red
    Write-Host "請前往 https://nodejs.org/ 下載並安裝 Node.js" -ForegroundColor Yellow
    exit 1
}

# 安裝 MCP 伺服器套件
Write-Host "`n📦 安裝 MCP 伺服器套件..." -ForegroundColor Yellow

$packages = @(
    "@playwright/mcp",
    "@modelcontextprotocol/server-filesystem",
    "@modelcontextprotocol/server-memory"
)

$successCount = 0
foreach ($package in $packages) {
    try {
        Write-Host "正在安裝 $package..." -ForegroundColor Cyan
        npm install -g $package
        Write-Host "✅ $package 安裝成功" -ForegroundColor Green
        $successCount++
    } catch {
        Write-Host "❌ $package 安裝失敗" -ForegroundColor Red
    }
}

# 建立簡化的 MCP 配置
Write-Host "`n📝 建立 MCP 配置檔案..." -ForegroundColor Yellow

$simpleConfig = @"
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp"],
      "env": {}
    }
  }
}
"@

$simpleConfig | Out-File -FilePath "langflow-mcp-simple.json" -Encoding UTF8

# 建立完整的 MCP 配置
$fullConfig = @"
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp"],
      "env": {
        "NODE_ENV": "production"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "$(Get-Location)"],
      "env": {}
    },
    "memory": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-memory"],
      "env": {}
    }
  }
}
"@

$fullConfig | Out-File -FilePath "langflow-mcp-config.json" -Encoding UTF8

Write-Host "✅ 配置檔案已建立" -ForegroundColor Green
Write-Host "`n📊 安裝完成: $successCount/$($packages.Count) 個套件成功安裝" -ForegroundColor Cyan

Write-Host "`n🎯 下一步:" -ForegroundColor Yellow
Write-Host "1. 複製 langflow-mcp-simple.json 的內容" -ForegroundColor White
Write-Host "2. 在 Langflow 設定中貼上 JSON 配置" -ForegroundColor White
Write-Host "3. 點擊 'Add Server' 按鈕" -ForegroundColor White

Write-Host "`n📋 簡化配置內容:" -ForegroundColor Cyan
Get-Content "langflow-mcp-simple.json" | Write-Host -ForegroundColor White

Write-Host "`n🎉 設置完成！" -ForegroundColor Green
