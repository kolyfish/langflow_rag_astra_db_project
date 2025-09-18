#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Astra DB 集成範例
展示如何在 Langflow MCP 中使用 Astra DB 向量數據庫
"""

import json
import os
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import numpy as np
import pandas as pd

try:
    from astrapy import DataAPIClient, Collection
    from astrapy.info import CollectionVectorServiceOptions
    from astrapy.constants import VectorMetric
    from openai import OpenAI
    from sentence_transformers import SentenceTransformer
except ImportError as e:
    print(f"❌ 缺少必要的套件: {e}")
    print("請執行: uv pip install astrapy openai sentence-transformers")
    exit(1)

class AstraDBManager:
    """Astra DB 管理器"""
    
    def __init__(self, config_path: str = "config/astra-config.json"):
        """初始化 Astra DB 管理器"""
        self.config = self._load_config(config_path)
        self.client = None
        self.collections = {}
        self.openai_client = None
        self.embedding_model = None
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """載入配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ 找不到配置文件: {config_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"❌ 配置文件格式錯誤: {e}")
            return {}
    
    def connect(self, token: str) -> bool:
        """連接到 Astra DB"""
        try:
            self.client = DataAPIClient(token)
            database_id = self.config['astra_db']['database_id']
            self.database = self.client.get_database(database_id)
            print(f"✅ 成功連接到 Astra DB: {database_id}")
            return True
        except Exception as e:
            print(f"❌ 連接 Astra DB 失敗: {e}")
            return False
    
    def setup_embedding_models(self, openai_api_key: str = None):
        """設置嵌入模型"""
        # OpenAI 嵌入模型
        if openai_api_key:
            self.openai_client = OpenAI(api_key=openai_api_key)
            print("✅ OpenAI 客戶端已設置")
        
        # Sentence Transformers 模型
        try:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✅ Sentence Transformers 模型已載入")
        except Exception as e:
            print(f"⚠️  Sentence Transformers 模型載入失敗: {e}")
    
    async def create_collections(self) -> bool:
        """創建向量集合"""
        try:
            for collection_name, collection_config in self.config['astra_db']['collections'].items():
                print(f"📦 創建集合: {collection_name}")
                
                # 設置向量服務選項
                vector_service = CollectionVectorServiceOptions(
                    provider=collection_config['service']
                )
                
                # 創建集合
                collection = await self.database.create_collection(
                    collection_config['name'],
                    metric=VectorMetric[collection_config['vector_metric'].upper()],
                    dimension=collection_config['dimension'],
                    service=vector_service
                )
                
                self.collections[collection_name] = collection
                print(f"✅ 集合 '{collection_name}' 創建成功")
            
            return True
        except Exception as e:
            print(f"❌ 創建集合失敗: {e}")
            return False
    
    def get_embedding_openai(self, text: str) -> List[float]:
        """使用 OpenAI 獲取嵌入向量"""
        if not self.openai_client:
            raise ValueError("OpenAI 客戶端未設置")
        
        response = self.openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    
    def get_embedding_sentence_transformers(self, text: str) -> List[float]:
        """使用 Sentence Transformers 獲取嵌入向量"""
        if not self.embedding_model:
            raise ValueError("Sentence Transformers 模型未載入")
        
        return self.embedding_model.encode(text).tolist()
    
    async def insert_documents(self, documents: List[Dict[str, Any]], collection_name: str = "documents") -> bool:
        """插入文檔到向量數據庫"""
        try:
            if collection_name not in self.collections:
                print(f"❌ 集合 '{collection_name}' 不存在")
                return False
            
            collection = self.collections[collection_name]
            
            # 為每個文檔生成嵌入向量
            for doc in documents:
                if 'text' in doc:
                    # 根據集合配置選擇嵌入模型
                    collection_config = self.config['astra_db']['collections'][collection_name]
                    if collection_config['service'] == 'openai':
                        doc['$vector'] = self.get_embedding_openai(doc['text'])
                    else:
                        doc['$vector'] = self.get_embedding_sentence_transformers(doc['text'])
            
            # 批量插入文檔
            result = await collection.insert_many(documents)
            print(f"✅ 成功插入 {len(documents)} 個文檔到集合 '{collection_name}'")
            return True
            
        except Exception as e:
            print(f"❌ 插入文檔失敗: {e}")
            return False
    
    async def search_similar(self, query: str, collection_name: str = "documents", limit: int = 5) -> List[Dict[str, Any]]:
        """搜索相似文檔"""
        try:
            if collection_name not in self.collections:
                print(f"❌ 集合 '{collection_name}' 不存在")
                return []
            
            collection = self.collections[collection_name]
            
            # 生成查詢向量
            collection_config = self.config['astra_db']['collections'][collection_name]
            if collection_config['service'] == 'openai':
                query_vector = self.get_embedding_openai(query)
            else:
                query_vector = self.get_embedding_sentence_transformers(query)
            
            # 執行向量搜索
            results = await collection.vector_find(
                query_vector,
                limit=limit,
                fields=["text", "metadata", "score"]
            )
            
            print(f"🔍 找到 {len(results)} 個相似文檔")
            return results
            
        except Exception as e:
            print(f"❌ 搜索失敗: {e}")
            return []
    
    async def get_collection_info(self, collection_name: str) -> Dict[str, Any]:
        """獲取集合信息"""
        try:
            if collection_name not in self.collections:
                return {}
            
            collection = self.collections[collection_name]
            info = await collection.info()
            return info
        except Exception as e:
            print(f"❌ 獲取集合信息失敗: {e}")
            return {}

class LangflowAstraIntegration:
    """Langflow 與 Astra DB 集成"""
    
    def __init__(self, astra_manager: AstraDBManager):
        self.astra_manager = astra_manager
    
    async def create_knowledge_base_flow(self) -> Dict[str, Any]:
        """創建知識庫流程配置"""
        flow_config = {
            "name": "Astra DB 知識庫流程",
            "description": "使用 Astra DB 向量數據庫的知識庫問答流程",
            "data": {
                "nodes": [
                    {
                        "id": "input-1",
                        "type": "TextInput",
                        "position": {"x": 100, "y": 100},
                        "data": {
                            "label": "用戶問題",
                            "placeholder": "請輸入您的問題...",
                            "multiline": True
                        }
                    },
                    {
                        "id": "vector-search",
                        "type": "AstraVectorSearch",
                        "position": {"x": 400, "y": 100},
                        "data": {
                            "label": "向量搜索",
                            "collection_name": "knowledge_base",
                            "limit": 5,
                            "threshold": 0.7
                        }
                    },
                    {
                        "id": "context-builder",
                        "type": "ContextBuilder",
                        "position": {"x": 700, "y": 100},
                        "data": {
                            "label": "上下文構建器",
                            "max_context_length": 2000
                        }
                    },
                    {
                        "id": "llm-processor",
                        "type": "OpenAIChat",
                        "position": {"x": 1000, "y": 100},
                        "data": {
                            "label": "LLM 處理器",
                            "model": "gpt-3.5-turbo",
                            "temperature": 0.7,
                            "max_tokens": 1000,
                            "system_message": "你是一個知識庫助手，基於提供的上下文回答用戶問題。"
                        }
                    },
                    {
                        "id": "output-1",
                        "type": "TextOutput",
                        "position": {"x": 1300, "y": 100},
                        "data": {
                            "label": "回答輸出"
                        }
                    }
                ],
                "edges": [
                    {
                        "id": "edge-1",
                        "source": "input-1",
                        "target": "vector-search",
                        "sourceHandle": "output",
                        "targetHandle": "input"
                    },
                    {
                        "id": "edge-2",
                        "source": "vector-search",
                        "target": "context-builder",
                        "sourceHandle": "output",
                        "targetHandle": "input"
                    },
                    {
                        "id": "edge-3",
                        "source": "context-builder",
                        "target": "llm-processor",
                        "sourceHandle": "output",
                        "targetHandle": "input"
                    },
                    {
                        "id": "edge-4",
                        "source": "llm-processor",
                        "target": "output-1",
                        "sourceHandle": "output",
                        "targetHandle": "input"
                    }
                ]
            }
        }
        return flow_config

async def main():
    """主程式"""
    print("🚀 Astra DB 集成範例")
    print("=" * 50)
    
    # 創建 Astra DB 管理器
    astra_manager = AstraDBManager()
    
    # 檢查配置
    if not astra_manager.config:
        print("❌ 配置文件載入失敗")
        return
    
    # 獲取 API Token (需要用戶提供)
    token = input("請輸入您的 Astra DB API Token: ").strip()
    if not token:
        print("❌ 需要提供 API Token")
        return
    
    # 連接到 Astra DB
    if not astra_manager.connect(token):
        return
    
    # 設置嵌入模型
    openai_key = input("請輸入 OpenAI API Key (可選): ").strip()
    astra_manager.setup_embedding_models(openai_key if openai_key else None)
    
    # 創建集合
    print("\n📦 創建向量集合...")
    if not await astra_manager.create_collections():
        return
    
    # 範例文檔
    sample_documents = [
        {
            "text": "人工智慧是計算機科學的一個分支，旨在創建能夠執行通常需要人類智能的任務的機器。",
            "metadata": {"category": "AI", "source": "wikipedia"},
            "timestamp": datetime.now().isoformat()
        },
        {
            "text": "機器學習是人工智慧的一個子領域，使計算機能夠在沒有明確編程的情況下學習和改進。",
            "metadata": {"category": "ML", "source": "textbook"},
            "timestamp": datetime.now().isoformat()
        },
        {
            "text": "深度學習是機器學習的一個分支，使用人工神經網路來模擬人腦的學習過程。",
            "metadata": {"category": "DL", "source": "research_paper"},
            "timestamp": datetime.now().isoformat()
        }
    ]
    
    # 插入範例文檔
    print("\n📝 插入範例文檔...")
    await astra_manager.insert_documents(sample_documents, "knowledge_base")
    
    # 搜索測試
    print("\n🔍 測試向量搜索...")
    query = "什麼是機器學習？"
    results = await astra_manager.search_similar(query, "knowledge_base", 3)
    
    print(f"\n查詢: {query}")
    print("搜索結果:")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result.get('text', 'N/A')}")
        print(f"   相似度: {result.get('score', 'N/A')}")
        print(f"   元數據: {result.get('metadata', {})}")
        print()
    
    # 創建 Langflow 集成
    integration = LangflowAstraIntegration(astra_manager)
    flow_config = await integration.create_knowledge_base_flow()
    
    # 保存流程配置
    with open("examples/astra-knowledge-flow.json", "w", encoding="utf-8") as f:
        json.dump(flow_config, f, ensure_ascii=False, indent=2)
    
    print("✅ Astra DB 集成範例完成！")
    print("📁 流程配置已保存到: examples/astra-knowledge-flow.json")

if __name__ == "__main__":
    asyncio.run(main())
