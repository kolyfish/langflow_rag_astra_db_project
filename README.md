# MCP 工具集安裝指南

這個專案包含了多種 MCP (Model Context Protocol) 工具的安裝腳本和配置檔案。

## 可用的 MCP 工具

### 1. Playwright MCP
網頁自動化工具，提供強大的瀏覽器控制功能。

### 2. Langflow MCP
流程自動化工具，提供 AI 代理和工具集成功能。

---

## Playwright MCP 安裝

### 前置需求

在安裝 Playwright MCP 之前，您需要先安裝 Node.js：

1. 前往 [Node.js 官網](https://nodejs.org/) 下載並安裝最新版本的 Node.js (建議選擇 LTS 版本)
2. 或者使用 Windows 包管理器安裝：
   - **Chocolatey**: `choco install nodejs`
   - **winget**: `winget install OpenJS.NodeJS`

### 安裝方法

#### 方法 1: 使用 PowerShell 腳本 (推薦)
```powershell
.\install-playwright-mcp.ps1
```

#### 方法 2: 使用批次檔
```cmd
install-playwright-mcp.bat
```

#### 方法 3: 手動安裝
```bash
# 初始化專案
npm init -y

# 安裝 Playwright MCP
npm install @playwright/mcp

# 安裝 Playwright 瀏覽器
npx playwright install
```

### Playwright MCP 功能

- 網頁導航和互動
- 元素選擇和操作
- 截圖和 PDF 生成
- 表單填寫和提交
- 等待和斷言
- 多瀏覽器支援 (Chromium, Firefox, Safari)

---

## Langflow MCP 安裝 (使用 uv 管理)

### 前置需求

在安裝 Langflow MCP 之前，您需要先安裝 Python：

1. 前往 [Python 官網](https://www.python.org/downloads/) 下載並安裝 Python 3.8 或更高版本
2. 安裝腳本會自動安裝 `uv` 包管理器

### 安裝方法

#### 方法 1: 使用 PowerShell 腳本 (推薦)
```powershell
.\install-langflow-mcp.ps1
```

#### 方法 2: 使用批次檔
```cmd
install-langflow-mcp.bat
```

#### 方法 3: 手動安裝
```bash
# 安裝 uv (如果尚未安裝)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 創建虛擬環境
uv venv langflow-env

# 啟動虛擬環境
# Windows:
langflow-env\Scripts\activate
# Linux/Mac:
source langflow-env/bin/activate

# 安裝專案依賴
uv pip install -e .
```

### Langflow MCP 功能

- **流程管理**: 創建和管理 AI 代理流程
- **工具集成**: 連接外部工具和 API
- **代理配置**: 設置 AI 代理的行為和參數
- **數據源連接**: 連接到各種數據源
- **MCP 伺服器**: 將流程作為 MCP 工具公開
- **MCP 客戶端**: 連接到其他 MCP 伺服器

### 啟動 Langflow MCP 伺服器

```powershell
# 使用 PowerShell
.\start-langflow-mcp.ps1

# 或使用批次檔
start-langflow-mcp.bat
```

### 使用 uv 管理插件

我們提供了專門的插件管理工具：

```powershell
# 使用 PowerShell 管理工具
.\uv-plugin-manager.ps1 -Action list                    # 列出已安裝套件
.\uv-plugin-manager.ps1 -Action install -Package numpy  # 安裝新套件
.\uv-plugin-manager.ps1 -Action upgrade -Package langflow # 升級套件
.\uv-plugin-manager.ps1 -Action add -Package pandas     # 添加套件到專案

# 或使用批次檔
uv-plugin-manager.bat list
uv-plugin-manager.bat install requests
uv-plugin-manager.bat upgrade langflow
```

### uv 管理命令

```bash
# 基本命令
uv pip list                    # 列出已安裝套件
uv pip install <套件名>        # 安裝套件
uv pip uninstall <套件名>      # 卸載套件
uv pip install --upgrade <套件名> # 升級套件

# 專案管理
uv add <套件名>                # 添加套件到專案
uv remove <套件名>             # 從專案移除套件
uv sync                        # 同步專案依賴
uv pip install -e .            # 安裝專案依賴
```

### 在 Cursor 中配置 Langflow MCP

1. 打開 Cursor 設定
2. 找到 MCP 伺服器配置
3. 添加以下配置：

```json
{
  "mcpServers": {
    "langflow": {
      "command": "python",
      "args": ["-m", "langflow", "run", "--mcp-server"],
      "cwd": "C:\\Users\\WUYUEH\\cursor_project"
    }
  }
}
```

### 測試 Langflow MCP

執行範例程式來測試安裝：

```bash
python langflow-mcp-example.py
```

---

## 專案結構

```
cursor_project/
├── install-playwright-mcp.ps1      # Playwright MCP 安裝腳本
├── install-playwright-mcp.bat      # Playwright MCP 批次安裝腳本
├── install-langflow-mcp.ps1        # Langflow MCP 安裝腳本 (uv)
├── install-langflow-mcp.bat        # Langflow MCP 批次安裝腳本 (uv)
├── start-langflow-mcp.ps1          # Langflow MCP 啟動腳本
├── start-langflow-mcp.bat          # Langflow MCP 啟動批次檔
├── uv-plugin-manager.ps1           # uv 插件管理腳本 (PowerShell)
├── uv-plugin-manager.bat           # uv 插件管理腳本 (批次檔)
├── pyproject.toml                  # Python 專案配置 (uv)
├── config/
│   └── mcp-config.json             # MCP 伺服器配置
├── examples/
│   ├── README.md                   # 案例說明文檔
│   ├── demo-script.py              # 演示腳本
│   ├── smart-assistant-flow.json   # 智能助手流程配置
│   └── test-cases.json             # 測試案例數據
├── langflow-env/                   # Python 虛擬環境 (安裝後生成)
└── README.md                       # 本文件
```

## 故障排除

### Playwright MCP 問題

1. 確保 Node.js 已正確安裝：`node --version`
2. 確保 npm 可用：`npm --version`
3. 檢查網路連線（下載瀏覽器需要網路）
4. 如果權限不足，請以管理員身份執行腳本

### Langflow MCP 問題

1. 確保 Python 已正確安裝：`python --version`
2. 確保 pip 可用：`pip --version`
3. 確保虛擬環境已啟動
4. 檢查端口 7860 是否被占用
5. 確保所有依賴已正確安裝

## 更多資源

- [Playwright 官方文檔](https://playwright.dev/)
- [Langflow 官方文檔](https://docs.langflow.org/)
- [MCP 協議文檔](https://modelcontextprotocol.io/)
- [Node.js 官方文檔](https://nodejs.org/docs/)
- [Python 官方文檔](https://docs.python.org/)

