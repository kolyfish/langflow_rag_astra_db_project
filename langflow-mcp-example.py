#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Langflow MCP 範例程式
此程式展示如何使用 Langflow MCP 功能
"""

import json
import requests
import time
from typing import Dict, Any

class LangflowMCPClient:
    """Langflow MCP 客戶端範例"""
    
    def __init__(self, host: str = "localhost", port: int = 7860):
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self.mcp_url = f"{self.base_url}/mcp"
    
    def check_server_status(self) -> bool:
        """檢查 Langflow MCP 伺服器狀態"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def list_tools(self) -> Dict[str, Any]:
        """列出可用的 MCP 工具"""
        try:
            response = requests.get(f"{self.mcp_url}/tools", timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}: {response.text}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"連接錯誤: {str(e)}"}
    
    def call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """呼叫指定的 MCP 工具"""
        try:
            payload = {
                "tool": tool_name,
                "parameters": parameters
            }
            response = requests.post(
                f"{self.mcp_url}/call",
                json=payload,
                timeout=30
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}: {response.text}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"連接錯誤: {str(e)}"}
    
    def create_flow(self, flow_config: Dict[str, Any]) -> Dict[str, Any]:
        """創建新的 Langflow 流程"""
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/flows",
                json=flow_config,
                timeout=30
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}: {response.text}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"連接錯誤: {str(e)}"}

def main():
    """主程式"""
    print("Langflow MCP 範例程式")
    print("=" * 50)
    
    # 創建 MCP 客戶端
    client = LangflowMCPClient()
    
    # 檢查伺服器狀態
    print("檢查 Langflow MCP 伺服器狀態...")
    if client.check_server_status():
        print("✓ 伺服器運行正常")
    else:
        print("✗ 伺服器未運行或無法連接")
        print("請先執行 start-langflow-mcp.ps1 啟動伺服器")
        return
    
    # 列出可用工具
    print("\n列出可用的 MCP 工具...")
    tools = client.list_tools()
    if "error" in tools:
        print(f"錯誤: {tools['error']}")
    else:
        print("可用工具:")
        for tool_name, tool_info in tools.items():
            print(f"  - {tool_name}: {tool_info.get('description', '無描述')}")
    
    # 範例：創建簡單的流程
    print("\n創建範例流程...")
    flow_config = {
        "name": "MCP 範例流程",
        "description": "使用 MCP 創建的範例流程",
        "data": {
            "nodes": [
                {
                    "id": "input-1",
                    "type": "TextInput",
                    "data": {
                        "label": "輸入文字",
                        "placeholder": "請輸入文字..."
                    }
                },
                {
                    "id": "output-1",
                    "type": "TextOutput",
                    "data": {
                        "label": "輸出結果"
                    }
                }
            ],
            "edges": [
                {
                    "source": "input-1",
                    "target": "output-1"
                }
            ]
        }
    }
    
    result = client.create_flow(flow_config)
    if "error" in result:
        print(f"創建流程時發生錯誤: {result['error']}")
    else:
        print(f"✓ 流程創建成功，ID: {result.get('id', '未知')}")
    
    print("\n範例程式執行完成！")

if __name__ == "__main__":
    main()
