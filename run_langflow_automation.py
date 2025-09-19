#!/usr/bin/env python3
"""
簡化的 Langflow 自動化執行腳本
"""

import asyncio
import json
import os
from langflow_automation import LangflowAutomation

async def run_automation():
    """執行自動化流程"""
    
    # 讀取配置
    try:
        with open('langflow_config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ 找不到 langflow_config.json 檔案")
        return
    
    # 設定環境變數
    langflow_config = config['langflow']
    os.environ['LANGFLOW_URL'] = langflow_config['url']
    
    if langflow_config['login_method'] == 'api_key':
        os.environ['LANGFLOW_API_KEY'] = langflow_config['credentials']['api_key']
    else:
        os.environ['LANGFLOW_USERNAME'] = langflow_config['credentials']['username']
        os.environ['LANGFLOW_PASSWORD'] = langflow_config['credentials']['password']
    
    # 建立自動化實例
    automation = LangflowAutomation(langflow_config['url'])
    
    try:
        print("🚀 啟動 Langflow 自動化...")
        
        # 啟動瀏覽器
        await automation.start_browser()
        
        # 登入
        if langflow_config['login_method'] == 'api_key':
            success = await automation.login_to_langflow(api_key=langflow_config['credentials']['api_key'])
        else:
            success = await automation.login_to_langflow(
                username=langflow_config['credentials']['username'],
                password=langflow_config['credentials']['password']
            )
        
        if not success:
            print("❌ 登入失敗")
            return
        
        # 載入並執行流程
        for flow_name, flow_path in config['flows'].items():
            print(f"📁 載入流程: {flow_name}")
            if await automation.load_flow_from_file(flow_path):
                print(f"✅ {flow_name} 載入成功")
                await automation.run_flow()
            else:
                print(f"❌ {flow_name} 載入失敗")
        
        # 截圖
        if config['automation']['screenshot_on_complete']:
            await automation.take_screenshot("langflow_automation_result.png")
        
        print("🎉 自動化流程完成！")
        
    except Exception as e:
        print(f"❌ 發生錯誤: {e}")
    
    finally:
        await automation.close_browser()

if __name__ == "__main__":
    asyncio.run(run_automation())
