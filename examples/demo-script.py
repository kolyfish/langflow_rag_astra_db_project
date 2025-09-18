#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Langflow MCP 案例演示腳本
展示如何使用 Langflow MCP 創建和執行智能助手流程
"""

import json
import requests
import time
import os
from typing import Dict, Any, List
from datetime import datetime

class LangflowMCPDemo:
    """Langflow MCP 案例演示類"""
    
    def __init__(self, host: str = "localhost", port: int = 7860):
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self.api_url = f"{self.base_url}/api/v1"
        self.mcp_url = f"{self.base_url}/mcp"
        self.session = requests.Session()
    
    def check_server_status(self) -> bool:
        """檢查 Langflow 伺服器狀態"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def create_flow(self, flow_config: Dict[str, Any]) -> Dict[str, Any]:
        """創建新的流程"""
        try:
            response = self.session.post(
                f"{self.api_url}/flows",
                json=flow_config,
                timeout=30
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}: {response.text}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"連接錯誤: {str(e)}"}
    
    def run_flow(self, flow_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """執行流程"""
        try:
            payload = {
                "inputs": inputs,
                "tweaks": {}
            }
            response = self.session.post(
                f"{self.api_url}/flows/{flow_id}/run",
                json=payload,
                timeout=60
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}: {response.text}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"連接錯誤: {str(e)}"}
    
    def list_flows(self) -> List[Dict[str, Any]]:
        """列出所有流程"""
        try:
            response = self.session.get(f"{self.api_url}/flows", timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                return []
        except requests.exceptions.RequestException:
            return []
    
    def test_smart_assistant(self) -> None:
        """測試智能助手流程"""
        print("🤖 智能助手流程測試")
        print("=" * 50)
        
        # 載入流程配置
        flow_config_path = "examples/smart-assistant-flow.json"
        if not os.path.exists(flow_config_path):
            print(f"❌ 找不到流程配置文件: {flow_config_path}")
            return
        
        with open(flow_config_path, 'r', encoding='utf-8') as f:
            flow_config = json.load(f)
        
        # 創建流程
        print("📝 創建智能助手流程...")
        result = self.create_flow(flow_config)
        if "error" in result:
            print(f"❌ 創建流程失敗: {result['error']}")
            return
        
        flow_id = result.get('id')
        print(f"✅ 流程創建成功，ID: {flow_id}")
        
        # 測試案例
        test_cases = [
            {
                "name": "問答測試",
                "input": "什麼是人工智慧？",
                "expected_type": "question"
            },
            {
                "name": "分析測試",
                "input": "請分析這篇文章的寫作風格和主題：'春天來了，萬物復甦，大地充滿生機。'",
                "expected_type": "analysis"
            },
            {
                "name": "翻譯測試",
                "input": "請將以下英文翻譯成中文：'Hello, how are you today?'",
                "expected_type": "translation"
            },
            {
                "name": "摘要測試",
                "input": "請為以下長文創建摘要：'人工智慧（AI）是計算機科學的一個分支，旨在創建能夠執行通常需要人類智能的任務的機器。AI 包括機器學習、深度學習、自然語言處理等領域。近年來，AI 技術快速發展，在醫療、金融、交通等行業都有廣泛應用。'",
                "expected_type": "summary"
            },
            {
                "name": "創意測試",
                "input": "請為一個咖啡店寫一個創意的廣告文案",
                "expected_type": "creative"
            }
        ]
        
        # 執行測試案例
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🧪 測試案例 {i}: {test_case['name']}")
            print(f"📝 輸入: {test_case['input']}")
            print("⏳ 處理中...")
            
            # 執行流程
            inputs = {"input-1": test_case['input']}
            result = self.run_flow(flow_id, inputs)
            
            if "error" in result:
                print(f"❌ 執行失敗: {result['error']}")
            else:
                # 提取輸出結果
                outputs = result.get('outputs', {})
                final_output = outputs.get('output-1', '無輸出')
                print(f"✅ 輸出結果:")
                print(f"   {final_output}")
                
                # 記錄執行時間
                execution_time = result.get('execution_time', 0)
                print(f"⏱️  執行時間: {execution_time:.2f} 秒")
            
            print("-" * 30)
            time.sleep(1)  # 避免請求過於頻繁
    
    def demonstrate_mcp_tools(self) -> None:
        """演示 MCP 工具功能"""
        print("\n🔧 MCP 工具演示")
        print("=" * 50)
        
        # 列出可用的 MCP 工具
        try:
            response = self.session.get(f"{self.mcp_url}/tools", timeout=10)
            if response.status_code == 200:
                tools = response.json()
                print("📋 可用的 MCP 工具:")
                for tool_name, tool_info in tools.items():
                    print(f"   - {tool_name}: {tool_info.get('description', '無描述')}")
            else:
                print("❌ 無法獲取 MCP 工具列表")
        except requests.exceptions.RequestException as e:
            print(f"❌ 連接 MCP 工具時發生錯誤: {str(e)}")
    
    def show_flow_statistics(self) -> None:
        """顯示流程統計資訊"""
        print("\n📊 流程統計資訊")
        print("=" * 50)
        
        flows = self.list_flows()
        if flows:
            print(f"📈 總流程數: {len(flows)}")
            print("📝 流程列表:")
            for flow in flows:
                print(f"   - {flow.get('name', '未命名')} (ID: {flow.get('id', '未知')})")
                print(f"     描述: {flow.get('description', '無描述')}")
                print(f"     創建時間: {flow.get('created_at', '未知')}")
                print()
        else:
            print("❌ 無法獲取流程列表")

def main():
    """主程式"""
    print("🚀 Langflow MCP 案例演示")
    print("=" * 60)
    print(f"⏰ 開始時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 創建演示實例
    demo = LangflowMCPDemo()
    
    # 檢查伺服器狀態
    print("🔍 檢查 Langflow 伺服器狀態...")
    if not demo.check_server_status():
        print("❌ Langflow 伺服器未運行或無法連接")
        print("請先執行以下命令啟動伺服器:")
        print("   .\\start-langflow-mcp.ps1")
        return
    
    print("✅ Langflow 伺服器運行正常")
    
    # 執行演示
    try:
        # 顯示流程統計
        demo.show_flow_statistics()
        
        # 演示 MCP 工具
        demo.demonstrate_mcp_tools()
        
        # 測試智能助手流程
        demo.test_smart_assistant()
        
        print("\n🎉 演示完成！")
        print("=" * 60)
        print(f"⏰ 結束時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  演示被用戶中斷")
    except Exception as e:
        print(f"\n❌ 演示過程中發生錯誤: {str(e)}")

if __name__ == "__main__":
    main()
