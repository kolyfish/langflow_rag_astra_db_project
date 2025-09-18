@echo off
REM Playwright MCP 安裝腳本 (批次檔版本)
REM 請確保已安裝 Node.js 後再執行此腳本

echo 開始安裝 Playwright MCP...

REM 檢查 Node.js 是否已安裝
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 錯誤: 未找到 Node.js 或 npm。請先安裝 Node.js。
    echo 請前往 https://nodejs.org/ 下載並安裝 Node.js
    pause
    exit /b 1
)

npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 錯誤: 未找到 npm。請先安裝 Node.js。
    echo 請前往 https://nodejs.org/ 下載並安裝 Node.js
    pause
    exit /b 1
)

echo Node.js 和 npm 已安裝，繼續安裝...

REM 初始化 package.json
echo 初始化 package.json...
npm init -y

REM 安裝 Playwright MCP
echo 安裝 Playwright MCP...
npm install @playwright/mcp

REM 安裝 Playwright 瀏覽器
echo 安裝 Playwright 瀏覽器...
npx playwright install

REM 創建基本配置檔案
echo 創建配置檔案...

REM 創建 mcp-config.json
(
echo {
echo   "mcpServers": {
echo     "playwright": {
echo       "command": "npx",
echo       "args": ["@playwright/mcp"],
echo       "env": {}
echo     }
echo   }
echo }
) > mcp-config.json

REM 創建基本使用範例
(
echo // Playwright MCP 使用範例
echo const { chromium } = require('playwright'^);
echo.
echo async function example(^) {
echo   const browser = await chromium.launch(^);
echo   const page = await browser.newPage(^);
echo   
echo   // 導航到網頁
echo   await page.goto('https://example.com'^);
echo   
echo   // 截圖
echo   await page.screenshot({ path: 'example.png' }^);
echo   
echo   // 獲取頁面標題
echo   const title = await page.title(^);
echo   console.log('頁面標題:', title^);
echo   
echo   await browser.close(^);
echo }
echo.
echo example(^).catch(console.error^);
) > example.js

echo 安裝完成！
echo 已創建以下檔案:
echo - mcp-config.json (MCP 配置檔案)
echo - example.js (使用範例)
echo - package.json (專案配置)
echo.
echo 要測試安裝，請執行: node example.js
pause


