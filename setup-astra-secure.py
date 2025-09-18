#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全的 Astra DB 設置腳本
使用環境變數或配置文件來安全存儲 API Token
"""

import os
import json
import asyncio
from pathlib import Path
from astrapy import DataAPIClient
from openai import OpenAI

# 您的配置
ASTRA_DB_ID = "ef4581e5-f997-44ce-8432-e56636786548"
CHATGPT_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")

def get_astra_token():
    """安全獲取 Astra DB Token"""
    # 方法1: 從環境變數獲取
    token = os.getenv('ASTRA_DB_TOKEN')
    if token:
        print("✅ 從環境變數獲取到 Astra DB Token")
        return token
    
    # 方法2: 從配置文件獲取
    config_file = Path("config/astra-token.txt")
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                token = f.read().strip()
            if token:
                print("✅ 從配置文件獲取到 Astra DB Token")
                return token
        except Exception as e:
            print(f"⚠️  讀取配置文件失敗: {e}")
    
    # 方法3: 提示用戶輸入
    print("🔐 請輸入您的 Astra DB API Token:")
    print("💡 提示: 您也可以將 Token 保存到 config/astra-token.txt 文件中")
    token = input("Token: ").strip()
    
    if token:
        # 保存到配置文件供下次使用
        try:
            config_file.parent.mkdir(exist_ok=True)
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(token)
            print("✅ Token 已保存到配置文件")
        except Exception as e:
            print(f"⚠️  保存 Token 失敗: {e}")
    
    return token

async def setup_astra_database():
    """設置 Astra DB 數據庫"""
    print("🚀 設置 Astra DB 數據庫")
    print("=" * 50)
    print(f"📊 數據庫 ID: {ASTRA_DB_ID}")
    
    # 獲取 Token
    token = get_astra_token()
    if not token:
        print("❌ 未提供 Astra DB Token")
        return False
    
    try:
        # 連接到 Astra DB
        print("📡 連接到 Astra DB...")
        client = DataAPIClient(token)
        database = client.get_database(ASTRA_DB_ID)
        
        # 測試連接
        print("✅ 成功連接到 Astra DB!")
        
        # 獲取數據庫信息
        print("\n📋 數據庫信息:")
        info = await database.info()
        print(f"   - 名稱: {info.get('name', 'N/A')}")
        print(f"   - 區域: {info.get('region', 'N/A')}")
        print(f"   - 狀態: {info.get('status', 'N/A')}")
        
        # 創建集合
        collection_name = "langflow_documents"
        print(f"\n📦 創建集合: {collection_name}")
        
        try:
            collection = await database.create_collection(
                collection_name,
                dimension=1536,  # OpenAI 嵌入維度
                metric="cosine"
            )
            print(f"✅ 集合 '{collection_name}' 創建成功")
        except Exception as e:
            if "already exists" in str(e).lower():
                print(f"ℹ️  集合 '{collection_name}' 已存在")
                collection = database.get_collection(collection_name)
            else:
                raise e
        
        # 設置 OpenAI 客戶端
        print("\n🤖 設置 OpenAI 客戶端...")
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
        
        # 測試搜索
        print("\n🔍 測試向量搜索...")
        test_query = "什麼是 Langflow？"
        query_response = openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=test_query
        )
        query_vector = query_response.data[0].embedding
        
        search_results = await collection.vector_find(
            query_vector,
            limit=2,
            fields=["text", "metadata"]
        )
        
        print(f"查詢: {test_query}")
        print("搜索結果:")
        for i, result in enumerate(search_results, 1):
            print(f"{i}. {result.get('text', 'N/A')}")
            print(f"   元數據: {result.get('metadata', {})}")
            print()
        
        print("🎉 Astra DB 設置完成！")
        print("現在您可以在 Langflow 中使用這個向量數據庫了。")
        
        return True
        
    except Exception as e:
        print(f"❌ 設置失敗: {e}")
        print("\n💡 可能的解決方案:")
        print("1. 檢查 API Token 是否正確")
        print("2. 確認數據庫 ID 是否正確")
        print("3. 檢查網路連接")
        return False

def create_env_file():
    """創建環境變數文件"""
    env_content = f"""# Astra DB 配置
ASTRA_DB_ID={ASTRA_DB_ID}
ASTRA_DB_TOKEN=your_token_here

# OpenAI 配置
OPENAI_API_KEY={CHATGPT_API_KEY}

# 使用說明:
# 1. 將 your_token_here 替換為您的實際 Astra DB Token
# 2. 在 PowerShell 中運行: . .env
# 3. 或者直接運行此腳本，它會自動處理 Token
"""
    
    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_content)
    
    print("📝 已創建 .env 文件")
    print("💡 您可以編輯 .env 文件來設置您的 Astra DB Token")

async def main():
    """主程式"""
    print("🔐 安全的 Astra DB 設置")
    print("=" * 50)
    
    # 創建環境變數文件
    create_env_file()
    
    # 設置數據庫
    success = await setup_astra_database()
    
    if success:
        print("\n✅ 設置完成！")
        print("📋 下一步:")
        print("1. 在 Langflow 中導入: examples/enhanced-astra-rag-flow.json")
        print("2. 開始使用您的 Astra DB 向量數據庫")
    else:
        print("\n❌ 設置失敗，請檢查錯誤信息")

if __name__ == "__main__":
    asyncio.run(main())
