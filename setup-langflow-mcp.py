#!/usr/bin/env python3
"""
設置 Langflow MCP 伺服器
"""

import json
import subprocess
import sys
import os
from pathlib import Path

def install_npm_package(package):
    """安裝 npm 套件"""
    try:
        print(f"📦 安裝 {package}...")
        subprocess.check_call(["npm", "install", "-g", package])
        print(f"✅ {package} 安裝成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {package} 安裝失敗: {e}")
        return False

def create_mcp_config():
    """建立 MCP 配置檔案"""
    config = {
        "mcpServers": {
            "playwright": {
                "command": "npx",
                "args": ["@playwright/mcp"],
                "env": {
                    "NODE_ENV": "production"
                }
            },
            "filesystem": {
                "command": "npx",
                "args": ["@modelcontextprotocol/server-filesystem", str(Path.cwd())],
                "env": {}
            },
            "memory": {
                "command": "npx",
                "args": ["@modelcontextprotocol/server-memory"],
                "env": {}
            },
            "brave-search": {
                "command": "npx",
                "args": ["@modelcontextprotocol/server-brave-search"],
                "env": {
                    "BRAVE_API_KEY": "YOUR_BRAVE_API_KEY_HERE"
                }
            }
        }
    }
    
    # 儲存配置檔案
    with open("langflow-mcp-config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ MCP 配置檔案已建立: langflow-mcp-config.json")
    return config

def create_simple_config():
    """建立簡化的 MCP 配置（僅 Playwright）"""
    config = {
        "mcpServers": {
            "playwright": {
                "command": "npx",
                "args": ["@playwright/mcp"],
                "env": {}
            }
        }
    }
    
    with open("langflow-mcp-simple.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ 簡化 MCP 配置檔案已建立: langflow-mcp-simple.json")
    return config

def main():
    """主函數"""
    print("🚀 開始設置 Langflow MCP 伺服器...")
    
    # 檢查 Node.js 是否已安裝
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        print(f"✅ Node.js 版本: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ 未找到 Node.js，請先安裝 Node.js")
        print("請前往 https://nodejs.org/ 下載並安裝")
        return
    
    # 檢查 npm 是否已安裝
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        print(f"✅ npm 版本: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ 未找到 npm")
        return
    
    # 安裝 MCP 伺服器套件
    packages = [
        "@playwright/mcp",
        "@modelcontextprotocol/server-filesystem", 
        "@modelcontextprotocol/server-memory",
        "@modelcontextprotocol/server-brave-search"
    ]
    
    print("\n📦 安裝 MCP 伺服器套件...")
    success_count = 0
    for package in packages:
        if install_npm_package(package):
            success_count += 1
    
    # 建立配置檔案
    print("\n📝 建立 MCP 配置檔案...")
    create_mcp_config()
    create_simple_config()
    
    print(f"\n📊 安裝完成: {success_count}/{len(packages)} 個套件成功安裝")
    
    print("\n🎯 下一步:")
    print("1. 複製 langflow-mcp-simple.json 的內容")
    print("2. 在 Langflow 設定中貼上 JSON 配置")
    print("3. 點擊 'Add Server' 按鈕")
    
    print("\n📋 簡化配置內容:")
    with open("langflow-mcp-simple.json", "r", encoding="utf-8") as f:
        print(f.read())

if __name__ == "__main__":
    main()
