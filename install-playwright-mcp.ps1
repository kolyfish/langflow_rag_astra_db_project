# Playwright MCP 安裝腳本
# 請確保已安裝 Node.js 後再執行此腳本

Write-Host "開始安裝 Playwright MCP..." -ForegroundColor Green

# 檢查 Node.js 是否已安裝
try {
    $nodeVersion = node --version
    $npmVersion = npm --version
    Write-Host "Node.js 版本: $nodeVersion" -ForegroundColor Cyan
    Write-Host "npm 版本: $npmVersion" -ForegroundColor Cyan
} catch {
    Write-Host "錯誤: 未找到 Node.js 或 npm。請先安裝 Node.js。" -ForegroundColor Red
    Write-Host "請前往 https://nodejs.org/ 下載並安裝 Node.js" -ForegroundColor Yellow
    exit 1
}

# 初始化 package.json
Write-Host "初始化 package.json..." -ForegroundColor Yellow
npm init -y

# 安裝 Playwright MCP
Write-Host "安裝 Playwright MCP..." -ForegroundColor Yellow
npm install @playwright/mcp

# 安裝 Playwright 瀏覽器
Write-Host "安裝 Playwright 瀏覽器..." -ForegroundColor Yellow
npx playwright install

# 創建基本配置檔案
Write-Host "創建配置檔案..." -ForegroundColor Yellow

# 創建 mcp-config.json
$mcpConfig = @"
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

$mcpConfig | Out-File -FilePath "mcp-config.json" -Encoding UTF8

# 創建基本使用範例
$exampleScript = @"
// Playwright MCP 使用範例
const { chromium } = require('playwright');

async function example() {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  // 導航到網頁
  await page.goto('https://example.com');
  
  // 截圖
  await page.screenshot({ path: 'example.png' });
  
  // 獲取頁面標題
  const title = await page.title();
  console.log('頁面標題:', title);
  
  await browser.close();
}

example().catch(console.error);
"@

$exampleScript | Out-File -FilePath "example.js" -Encoding UTF8

Write-Host "安裝完成！" -ForegroundColor Green
Write-Host "已創建以下檔案:" -ForegroundColor Cyan
Write-Host "- mcp-config.json (MCP 配置檔案)" -ForegroundColor White
Write-Host "- example.js (使用範例)" -ForegroundColor White
Write-Host "- package.json (專案配置)" -ForegroundColor White
Write-Host ""
Write-Host "要測試安裝，請執行: node example.js" -ForegroundColor Yellow


