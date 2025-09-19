# Langflow 自動化使用指南

這個專案現在包含了使用 Playwright MCP 來自動化 Langflow 操作的功能。

## 🚀 快速開始

### 1. 安裝依賴

```bash
# 安裝 Python 依賴
python install_automation_deps.py

# 或者手動安裝
pip install playwright
playwright install
```

### 2. 配置登入資訊

編輯 `langflow_config.json` 檔案：

```json
{
  "langflow": {
    "url": "http://localhost:7860",
    "login_method": "api_key",
    "credentials": {
      "username": "your_username_here",
      "password": "your_password_here", 
      "api_key": "your_langflow_api_key_here"
    }
  }
}
```

### 3. 執行自動化

```bash
# 執行自動化流程
python run_langflow_automation.py

# 或者直接使用主腳本
python langflow_automation.py
```

## 📁 檔案說明

- `langflow_automation.py` - 主要的自動化類別
- `run_langflow_automation.py` - 簡化的執行腳本
- `langflow_config.json` - 配置檔案
- `install_automation_deps.py` - 依賴安裝腳本

## 🔧 功能特色

- ✅ 自動登入 Langflow
- ✅ 載入您的流程檔案
- ✅ 自動執行流程
- ✅ 截圖記錄結果
- ✅ 支援多種登入方式（用戶名/密碼、API 金鑰）
- ✅ 可配置的等待時間和選項

## 🛠️ 自訂配置

### 登入方式

1. **API 金鑰登入**（推薦）：
   ```json
   "login_method": "api_key"
   ```

2. **用戶名/密碼登入**：
   ```json
   "login_method": "username_password"
   ```

### 流程配置

在 `langflow_config.json` 中配置要載入的流程：

```json
"flows": {
  "enhanced_astra_rag": "examples/enhanced-astra-rag-flow.json",
  "smart_assistant": "examples/smart-assistant-flow.json"
}
```

### 自動化選項

```json
"automation": {
  "headless": false,           // 是否隱藏瀏覽器視窗
  "screenshot_on_complete": true,  // 完成後是否截圖
  "wait_timeout": 5000        // 等待超時時間（毫秒）
}
```

## 🐛 故障排除

### 常見問題

1. **登入失敗**
   - 檢查 Langflow URL 是否正確
   - 確認登入資訊是否正確
   - 檢查 Langflow 服務是否正在運行

2. **流程載入失敗**
   - 檢查流程檔案路徑是否正確
   - 確認 JSON 格式是否有效
   - 檢查檔案權限

3. **瀏覽器啟動失敗**
   - 確認已安裝 Playwright 瀏覽器
   - 檢查系統權限
   - 嘗試設定 `headless: true`

### 除錯模式

設定 `headless: false` 可以看到瀏覽器操作過程，方便除錯。

## 📞 支援

如果遇到問題，請檢查：
1. 所有依賴是否正確安裝
2. 配置檔案格式是否正確
3. Langflow 服務是否正常運行
4. 網路連接是否正常
