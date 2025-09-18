#!/usr/bin/env python3
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
