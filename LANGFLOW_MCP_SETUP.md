# Langflow MCP 設置指南

## 🚀 快速設置步驟

### 1. 安裝 Node.js

首先需要安裝 Node.js：

1. 前往 [Node.js 官網](https://nodejs.org/)
2. 下載 LTS 版本（推薦）
3. 執行安裝程式
4. 重新啟動命令提示字元

### 2. 驗證安裝

開啟命令提示字元，執行：

```bash
node --version
npm --version
```

應該會顯示版本號碼。

### 3. 安裝 MCP 伺服器

執行以下其中一個腳本：

**PowerShell 腳本（推薦）：**
```powershell
.\setup-langflow-mcp.ps1
```

**Python 腳本：**
```bash
python setup-langflow-mcp.py
```

### 4. 在 Langflow 中設置 MCP

1. 開啟 Langflow
2. 前往 **Settings** → **MCP Servers**
3. 點擊 **+ Add MCP Server**
4. 選擇 **JSON** 類型
5. 複製並貼上以下配置：

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp"],
      "env": {}
    }
  }
}
```

6. 點擊 **Add Server**

## 📋 可用的 MCP 伺服器

### 基本配置（僅 Playwright）
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp"],
      "env": {}
    }
  }
}
```

### 完整配置（包含多個伺服器）
```json
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
      "args": ["@modelcontextprotocol/server-filesystem", "/path/to/your/project"],
      "env": {}
    },
    "memory": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-memory"],
      "env": {}
    }
  }
}
```

## 🔧 手動安裝 MCP 伺服器

如果腳本執行失敗，可以手動安裝：

```bash
# 安裝 Playwright MCP
npm install -g @playwright/mcp

# 安裝檔案系統 MCP
npm install -g @modelcontextprotocol/server-filesystem

# 安裝記憶體 MCP
npm install -g @modelcontextprotocol/server-memory

# 安裝搜尋 MCP
npm install -g @modelcontextprotocol/server-brave-search
```

## 🐛 故障排除

### 常見問題

1. **Node.js 未安裝**
   - 前往 https://nodejs.org/ 下載安裝
   - 重新啟動命令提示字元

2. **npm 權限問題**
   ```bash
   # 設定 npm 全域安裝目錄
   npm config set prefix %APPDATA%\npm
   ```

3. **MCP 伺服器連接失敗**
   - 檢查 Node.js 和 npm 是否正確安裝
   - 確認 MCP 套件已全域安裝
   - 檢查 JSON 配置格式是否正確

4. **Playwright 瀏覽器問題**
   ```bash
   # 安裝 Playwright 瀏覽器
   npx playwright install
   ```

## 📞 支援

如果遇到問題：
1. 檢查所有依賴是否正確安裝
2. 確認 JSON 配置格式正確
3. 重新啟動 Langflow
4. 檢查命令提示字元權限

## 🎯 下一步

MCP 設置完成後，您就可以：
1. 使用 Playwright 自動化瀏覽器操作
2. 在 Langflow 中直接控制網頁
3. 執行您的自動化腳本
4. 整合多個 MCP 伺服器功能
