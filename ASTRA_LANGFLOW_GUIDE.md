
# 🚀 Astra DB + Langflow 整合使用指南

## 📋 您現有的資源
- ✅ Astra DB ID: ef4581e5-f997-44ce-8432-e56636786548
- ✅ Grok API Key: 已配置
- ✅ ChatGPT API Key: 已配置
- ✅ 原始 Langflow RAG 流程: Vector Store RAG.json

## 🔧 設置步驟

### 1. 安裝依賴套件
```bash
# 安裝 Astra DB 相關套件
.\uv-plugin-manager.ps1 -Action install -Package astrapy
.\uv-plugin-manager.ps1 -Action install -Package openai
```

### 2. 設置 Astra DB
```bash
# 運行設置腳本
python setup-astra-for-langflow.py
```

### 3. 導入增強版流程
1. 打開 Langflow 界面
2. 點擊 "Import Flow"
3. 選擇 `examples/enhanced-astra-rag-flow.json`

## 🎯 新功能特色

### 雙 LLM 支援
- **Grok AI**: 用於創意性和分析性問題
- **ChatGPT**: 用於一般性問答和技術問題

### Astra DB 集成
- 自動向量搜索
- 語義相似性匹配
- 可擴展的知識庫

### 智能路由
- 根據問題類型選擇最適合的 LLM
- 自動上下文構建
- 多源知識整合

## 🔍 使用範例

### 問答測試
- "什麼是 Langflow？" → 使用 ChatGPT
- "分析 AI 的未來趨勢" → 使用 Grok AI
- "如何設置向量數據庫？" → 使用 ChatGPT

### 知識庫查詢
- 自動從 Astra DB 檢索相關文檔
- 結合多個 LLM 的優勢
- 提供準確且詳細的回答

## 📊 監控和優化

### 性能指標
- 搜索響應時間
- LLM 選擇準確性
- 用戶滿意度

### 優化建議
- 定期更新知識庫
- 調整 LLM 參數
- 監控 API 使用量

## 🆘 故障排除

### 常見問題
1. **Astra DB 連接失敗**: 檢查 API Token
2. **LLM 無響應**: 驗證 API Key
3. **搜索結果不準確**: 調整嵌入模型參數

### 支援資源
- Langflow 文檔: https://docs.langflow.org/
- Astra DB 文檔: https://docs.datastax.com/en/astra/
- 本專案文檔: examples/README.md
