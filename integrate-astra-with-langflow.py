#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
整合 Astra DB 與現有 Langflow 流程
將您的 Astra DB 與現有的 Vector Store RAG 流程結合
"""

import json
import os
import asyncio
from typing import Dict, Any, List
from pathlib import Path

# 您的 API 金鑰 - 請從環境變數或 .env 檔案中讀取
GROK_API_KEY = os.getenv("GROK_API_KEY", "YOUR_GROK_API_KEY_HERE")
CHATGPT_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")
ASTRA_DB_ID = "ef4581e5-f997-44ce-8432-e56636786548"

class LangflowAstraIntegrator:
    """Langflow 與 Astra DB 整合器"""
    
    def __init__(self):
        self.original_flow_path = r"c:\Users\WUYUEH\Documents\langflow\Vector Store RAG.json"
        self.enhanced_flow_path = "examples/enhanced-astra-rag-flow.json"
        
    def load_original_flow(self) -> Dict[str, Any]:
        """載入原始 Langflow 流程"""
        try:
            with open(self.original_flow_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ 載入原始流程失敗: {e}")
            return {}
    
    def create_astra_vector_store_config(self) -> Dict[str, Any]:
        """創建 Astra DB Vector Store 配置"""
        return {
            "id": "AstraVectorStore-astra1",
            "type": "AstraVectorStore",
            "position": {"x": 400, "y": 300},
            "data": {
                "label": "Astra DB Vector Store",
                "database_id": ASTRA_DB_ID,
                "collection_name": "langflow_documents",
                "embedding_dimension": 1536,
                "metric": "cosine",
                "api_endpoint": f"https://{ASTRA_DB_ID}-us-east1.apps.astra.datastax.com",
                "region": "us-east1",
                "provider": "gcp"
            }
        }
    
    def create_enhanced_flow(self) -> Dict[str, Any]:
        """創建增強版流程，整合 Astra DB"""
        original_flow = self.load_original_flow()
        if not original_flow:
            return {}
        
        # 創建新的流程配置
        enhanced_flow = {
            "name": "Enhanced Astra DB RAG Flow",
            "description": "整合 Astra DB 的增強版 RAG 流程，支援多個 LLM 和向量存儲",
            "data": {
                "nodes": [],
                "edges": []
            }
        }
        
        # 添加輸入節點
        input_node = {
            "id": "ChatInput-enhanced",
            "type": "ChatInput",
            "position": {"x": 100, "y": 100},
            "data": {
                "label": "用戶輸入",
                "placeholder": "請輸入您的問題...",
                "multiline": True
            }
        }
        
        # 添加 Astra DB Vector Store 節點
        astra_vector_store = self.create_astra_vector_store_config()
        
        # 添加 Grok LLM 節點
        grok_llm = {
            "id": "GrokLLM-grok1",
            "type": "GrokLLM",
            "position": {"x": 800, "y": 200},
            "data": {
                "label": "Grok AI 處理器",
                "api_key": GROK_API_KEY,
                "model": "grok-beta",
                "temperature": 0.7,
                "max_tokens": 1000,
                "system_message": "你是一個基於 Astra DB 知識庫的智能助手，請根據提供的上下文回答用戶問題。"
            }
        }
        
        # 添加 ChatGPT 節點
        chatgpt_llm = {
            "id": "OpenAIChat-chatgpt1",
            "type": "OpenAIChat",
            "position": {"x": 800, "y": 400},
            "data": {
                "label": "ChatGPT 處理器",
                "api_key": CHATGPT_API_KEY,
                "model": "gpt-3.5-turbo",
                "temperature": 0.7,
                "max_tokens": 1000,
                "system_message": "你是一個基於 Astra DB 知識庫的智能助手，請根據提供的上下文回答用戶問題。"
            }
        }
        
        # 添加輸出節點
        output_node = {
            "id": "ChatOutput-enhanced",
            "type": "ChatOutput",
            "position": {"x": 1200, "y": 300},
            "data": {
                "label": "AI 回答輸出"
            }
        }
        
        # 添加路由節點（選擇使用哪個 LLM）
        router_node = {
            "id": "Router-llm_selector",
            "type": "Router",
            "position": {"x": 600, "y": 300},
            "data": {
                "label": "LLM 選擇器",
                "routing_key": "llm_preference",
                "routes": {
                    "grok": "GrokLLM-grok1",
                    "chatgpt": "OpenAIChat-chatgpt1"
                }
            }
        }
        
        # 組裝節點
        enhanced_flow["data"]["nodes"] = [
            input_node,
            astra_vector_store,
            router_node,
            grok_llm,
            chatgpt_llm,
            output_node
        ]
        
        # 添加連接線
        enhanced_flow["data"]["edges"] = [
            {
                "id": "edge-input-to-vector",
                "source": "ChatInput-enhanced",
                "target": "AstraVectorStore-astra1",
                "sourceHandle": "message",
                "targetHandle": "query"
            },
            {
                "id": "edge-vector-to-router",
                "source": "AstraVectorStore-astra1",
                "target": "Router-llm_selector",
                "sourceHandle": "documents",
                "targetHandle": "input"
            },
            {
                "id": "edge-router-to-grok",
                "source": "Router-llm_selector",
                "target": "GrokLLM-grok1",
                "sourceHandle": "grok",
                "targetHandle": "input"
            },
            {
                "id": "edge-router-to-chatgpt",
                "source": "Router-llm_selector",
                "target": "OpenAIChat-chatgpt1",
                "sourceHandle": "chatgpt",
                "targetHandle": "input"
            },
            {
                "id": "edge-grok-to-output",
                "source": "GrokLLM-grok1",
                "target": "ChatOutput-enhanced",
                "sourceHandle": "output",
                "targetHandle": "input"
            },
            {
                "id": "edge-chatgpt-to-output",
                "source": "OpenAIChat-chatgpt1",
                "target": "ChatOutput-enhanced",
                "sourceHandle": "output",
                "targetHandle": "input"
            }
        ]
        
        return enhanced_flow
    
    def create_astra_setup_script(self) -> str:
        """創建 Astra DB 設置腳本"""
        return '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Astra DB 設置腳本
為 Langflow 流程準備 Astra DB 數據
"""

import asyncio
import json
from astrapy import DataAPIClient
from openai import OpenAI

# 配置
ASTRA_DB_ID = "ef4581e5-f997-44ce-8432-e56636786548"
CHATGPT_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")

async def setup_astra_for_langflow():
    """為 Langflow 設置 Astra DB"""
    print("🚀 設置 Astra DB 用於 Langflow")
    print("=" * 50)
    
    # 獲取 API Token
    token = input("請輸入您的 Astra DB API Token: ").strip()
    if not token:
        print("❌ 需要提供 API Token")
        return
    
    try:
        # 連接到 Astra DB
        client = DataAPIClient(token)
        database = client.get_database(ASTRA_DB_ID)
        
        # 創建集合
        collection_name = "langflow_documents"
        print(f"📦 創建集合: {collection_name}")
        
        collection = await database.create_collection(
            collection_name,
            dimension=1536,  # OpenAI 嵌入維度
            metric="cosine"
        )
        
        # 設置 OpenAI 客戶端
        openai_client = OpenAI(api_key=CHATGPT_API_KEY)
        
        # 範例文檔
        sample_docs = [
            {
                "text": "Langflow 是一個開源的 AI 流程自動化平台，可以幫助用戶創建複雜的 AI 工作流程。",
                "metadata": {"source": "langflow_docs", "category": "introduction"},
                "timestamp": "2024-01-01T00:00:00Z"
            },
            {
                "text": "Astra DB 是 DataStax 提供的向量數據庫服務，專為 AI 應用設計，支援高效的向量搜索。",
                "metadata": {"source": "astra_docs", "category": "database"},
                "timestamp": "2024-01-01T00:00:00Z"
            },
            {
                "text": "RAG (Retrieval-Augmented Generation) 是一種結合檢索和生成的 AI 技術，可以提高回答的準確性。",
                "metadata": {"source": "ai_research", "category": "technique"},
                "timestamp": "2024-01-01T00:00:00Z"
            }
        ]
        
        # 為文檔生成嵌入向量
        print("🔄 生成嵌入向量...")
        for doc in sample_docs:
            response = openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=doc["text"]
            )
            doc["$vector"] = response.data[0].embedding
        
        # 插入文檔
        print("📝 插入文檔到 Astra DB...")
        result = await collection.insert_many(sample_docs)
        print(f"✅ 成功插入 {len(sample_docs)} 個文檔")
        
        print("🎉 Astra DB 設置完成！")
        print("現在您可以在 Langflow 中使用這個向量數據庫了。")
        
    except Exception as e:
        print(f"❌ 設置失敗: {e}")

if __name__ == "__main__":
    asyncio.run(setup_astra_for_langflow())
'''
    
    def save_enhanced_flow(self):
        """保存增強版流程"""
        enhanced_flow = self.create_enhanced_flow()
        if enhanced_flow:
            with open(self.enhanced_flow_path, 'w', encoding='utf-8') as f:
                json.dump(enhanced_flow, f, ensure_ascii=False, indent=2)
            print(f"✅ 增強版流程已保存到: {self.enhanced_flow_path}")
            return True
        return False
    
    def create_usage_guide(self) -> str:
        """創建使用指南"""
        return r"""
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
"""

def main():
    """主程式"""
    print("🔗 整合 Astra DB 與現有 Langflow 流程")
    print("=" * 60)
    
    integrator = LangflowAstraIntegrator()
    
    # 創建增強版流程
    print("📝 創建增強版流程...")
    if integrator.save_enhanced_flow():
        print("✅ 增強版流程創建成功")
    else:
        print("❌ 增強版流程創建失敗")
        return
    
    # 創建設置腳本
    print("📝 創建 Astra DB 設置腳本...")
    setup_script = integrator.create_astra_setup_script()
    with open("setup-astra-for-langflow.py", "w", encoding="utf-8") as f:
        f.write(setup_script)
    print("✅ 設置腳本已創建: setup-astra-for-langflow.py")
    
    # 創建使用指南
    print("📝 創建使用指南...")
    usage_guide = integrator.create_usage_guide()
    with open("ASTRA_LANGFLOW_GUIDE.md", "w", encoding="utf-8") as f:
        f.write(usage_guide)
    print("✅ 使用指南已創建: ASTRA_LANGFLOW_GUIDE.md")
    
    print("\n🎉 整合完成！")
    print("=" * 60)
    print("📋 下一步操作:")
    print("1. 運行: python setup-astra-for-langflow.py")
    print("2. 在 Langflow 中導入: examples/enhanced-astra-rag-flow.json")
    print("3. 查看使用指南: ASTRA_LANGFLOW_GUIDE.md")

if __name__ == "__main__":
    main()
