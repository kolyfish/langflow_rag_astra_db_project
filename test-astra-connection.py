#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Astra DB 連接測試腳本
快速測試您的 Astra DB 是否正常工作
"""

import json
import asyncio
from astrapy import DataAPIClient

async def test_astra_connection():
    """測試 Astra DB 連接"""
    print("🔍 測試 Astra DB 連接")
    print("=" * 40)
    
    # 您的數據庫 ID
    database_id = "ef4581e5-f997-44ce-8432-e56636786548"
    
    # 獲取 API Token
    token = input("請輸入您的 Astra DB API Token: ").strip()
    if not token:
        print("❌ 需要提供 API Token")
        return False
    
    try:
        # 創建客戶端
        print("📡 連接到 Astra DB...")
        client = DataAPIClient(token)
        database = client.get_database(database_id)
        
        # 測試連接
        print("✅ 成功連接到 Astra DB!")
        print(f"📊 數據庫 ID: {database_id}")
        
        # 獲取數據庫信息
        print("\n📋 數據庫信息:")
        info = await database.info()
        print(f"   - 名稱: {info.get('name', 'N/A')}")
        print(f"   - 區域: {info.get('region', 'N/A')}")
        print(f"   - 狀態: {info.get('status', 'N/A')}")
        
        # 列出現有集合
        print("\n📦 現有集合:")
        collections = await database.list_collections()
        if collections:
            for collection in collections:
                print(f"   - {collection.name}")
        else:
            print("   (無集合)")
        
        print("\n🎉 Astra DB 連接測試成功！")
        print("您現在可以開始使用向量數據庫功能了。")
        
        return True
        
    except Exception as e:
        print(f"❌ 連接失敗: {e}")
        print("\n💡 可能的解決方案:")
        print("1. 檢查 API Token 是否正確")
        print("2. 確認數據庫 ID 是否正確")
        print("3. 檢查網路連接")
        return False

if __name__ == "__main__":
    asyncio.run(test_astra_connection())
