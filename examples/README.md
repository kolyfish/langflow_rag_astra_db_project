# Langflow MCP 案例演示

這個目錄包含了 Langflow MCP 的實際使用案例，展示如何創建和執行智能助手流程。

## 📁 檔案結構

```
examples/
├── README.md                    # 本說明文件
├── smart-assistant-flow.json    # 智能助手流程配置
├── demo-script.py              # 演示腳本
└── test-cases.json             # 測試案例數據
```

## 🚀 快速開始

### 1. 前置準備

確保您已經安裝並啟動了 Langflow MCP：

```powershell
# 安裝 Langflow MCP
.\install-langflow-mcp.ps1

# 啟動 MCP 伺服器
.\start-langflow-mcp.ps1
```

### 2. 修復依賴問題（如果需要）

如果遇到 "no module named requests" 錯誤，請先修復：

```powershell
# 使用 PowerShell 修復
.\fix-requests.ps1

# 或使用批次檔修復
fix-requests.bat
```

### 3. 運行演示

```bash
# 執行演示腳本
python examples/demo-script.py

# 或使用啟動腳本（推薦）
.\run-demo.ps1
```

## 🤖 智能助手流程案例

### 流程概述

這個案例展示了一個智能助手流程，能夠：

- **任務分類**: 自動識別用戶輸入的任務類型
- **智能路由**: 根據任務類型選擇合適的處理器
- **多種處理**: 支援問答、分析、翻譯、摘要、創意等任務
- **統一輸出**: 提供一致的輸出格式

### 流程架構

```
用戶輸入 → 任務分類器 → 路由器 → 處理器 → 輸出
                ↓
            執行日誌
```

#### 節點說明

1. **輸入節點** (`input-1`)
   - 接收用戶的文字輸入
   - 支援多行文字輸入

2. **任務分類器** (`classifier-1`)
   - 使用 OpenAI 函數調用分析任務類型
   - 識別任務類型：question, analysis, translation, summary, creative
   - 檢測語言和複雜度

3. **路由器** (`router-1`)
   - 根據任務類型將輸入路由到相應的處理器

4. **處理器群組**
   - **問答處理器**: 回答一般性問題
   - **分析處理器**: 進行深度內容分析
   - **翻譯處理器**: 提供準確的翻譯服務
   - **摘要處理器**: 創建內容摘要
   - **創意處理器**: 生成創意內容

5. **輸出節點** (`output-1`)
   - 統一輸出格式
   - 整合所有處理器的結果

6. **日誌節點** (`logger-1`)
   - 記錄執行過程和分類結果

### 支援的任務類型

| 任務類型 | 描述 | 範例輸入 |
|---------|------|----------|
| `question` | 一般性問答 | "什麼是人工智慧？" |
| `analysis` | 內容分析 | "請分析這篇文章的寫作風格" |
| `translation` | 語言翻譯 | "請將英文翻譯成中文" |
| `summary` | 內容摘要 | "請為這篇長文創建摘要" |
| `creative` | 創意生成 | "請寫一個咖啡店廣告文案" |

## 🧪 測試案例

演示腳本包含以下測試案例：

### 1. 問答測試
- **輸入**: "什麼是人工智慧？"
- **預期**: 提供關於 AI 的詳細解釋

### 2. 分析測試
- **輸入**: "請分析這篇文章的寫作風格和主題：'春天來了，萬物復甦，大地充滿生機。'"
- **預期**: 分析文字風格、主題和修辭手法

### 3. 翻譯測試
- **輸入**: "請將以下英文翻譯成中文：'Hello, how are you today?'"
- **預期**: 準確的中文翻譯

### 4. 摘要測試
- **輸入**: 關於 AI 的長文段落
- **預期**: 簡潔明瞭的摘要

### 5. 創意測試
- **輸入**: "請為一個咖啡店寫一個創意的廣告文案"
- **預期**: 富有創意的廣告文案

## 🔧 自定義配置

### 修改流程配置

您可以編輯 `smart-assistant-flow.json` 來自定義流程：

1. **添加新的處理器**:
   ```json
   {
     "id": "new-handler",
     "type": "OpenAIChat",
     "data": {
       "label": "新處理器",
       "model": "gpt-4",
       "system_message": "自定義系統提示"
     }
   }
   ```

2. **修改路由器規則**:
   ```json
   {
     "id": "router-1",
     "type": "Router",
     "data": {
       "routing_key": "task_type",
       "routes": {
         "new_task": "new-handler"
       }
     }
   }
   ```

3. **調整模型參數**:
   ```json
   {
     "temperature": 0.7,
     "max_tokens": 1000,
     "model": "gpt-4"
   }
   ```

### 添加新的測試案例

在 `demo-script.py` 中的 `test_cases` 列表添加新案例：

```python
{
    "name": "自定義測試",
    "input": "您的測試輸入",
    "expected_type": "question"
}
```

## 📊 監控和日誌

### 查看執行日誌

流程執行時會自動記錄：
- 任務分類結果
- 執行時間
- 錯誤信息
- 處理器選擇

### 性能監控

演示腳本會顯示：
- 每個測試案例的執行時間
- 流程創建和執行狀態
- 錯誤和異常信息

## 🚨 故障排除

### 常見問題

1. **缺少 requests 套件**
   ```
   ModuleNotFoundError: No module named 'requests'
   ```
   **解決方案**: 執行 `.\fix-requests.ps1` 或 `fix-requests.bat`

2. **伺服器連接失敗**
   ```
   ❌ Langflow 伺服器未運行或無法連接
   ```
   **解決方案**: 確保 Langflow MCP 伺服器正在運行

3. **流程創建失敗**
   ```
   ❌ 創建流程失敗: HTTP 400
   ```
   **解決方案**: 檢查流程配置文件的 JSON 格式

4. **執行超時**
   ```
   ❌ 執行失敗: 連接錯誤: timeout
   ```
   **解決方案**: 增加超時時間或檢查網路連接

5. **模型調用失敗**
   ```
   ❌ 執行失敗: OpenAI API 錯誤
   ```
   **解決方案**: 檢查 OpenAI API 密鑰配置

### 調試技巧

1. **啟用詳細日誌**:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **檢查流程狀態**:
   ```python
   flows = demo.list_flows()
   print(json.dumps(flows, indent=2))
   ```

3. **測試單個組件**:
   ```python
   # 只測試分類器
   result = demo.run_flow(flow_id, {"input-1": "測試輸入"})
   ```

## 🔗 相關資源

- [Langflow 官方文檔](https://docs.langflow.org/)
- [OpenAI API 文檔](https://platform.openai.com/docs)
- [MCP 協議規範](https://modelcontextprotocol.io/)
- [Python requests 庫文檔](https://requests.readthedocs.io/)

## 📝 貢獻指南

歡迎提交改進建議和新的案例：

1. Fork 本專案
2. 創建功能分支
3. 提交變更
4. 發起 Pull Request

## 📄 授權

本案例遵循與主專案相同的授權條款。
