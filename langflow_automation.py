#!/usr/bin/env python3
"""
Langflow 自動化登入和使用腳本
使用 Playwright MCP 來自動化 Langflow 操作
"""

import asyncio
import os
from playwright.async_api import async_playwright
import json
from pathlib import Path

class LangflowAutomation:
    def __init__(self, langflow_url="http://localhost:7860"):
        self.langflow_url = langflow_url
        self.browser = None
        self.page = None
        
    async def start_browser(self):
        """啟動瀏覽器"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=False,  # 設為 True 可隱藏瀏覽器視窗
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        self.page = await self.browser.new_page()
        
    async def login_to_langflow(self, username=None, password=None, api_key=None):
        """登入 Langflow"""
        print(f"🌐 正在連接到 Langflow: {self.langflow_url}")
        await self.page.goto(self.langflow_url)
        
        # 等待頁面載入
        await self.page.wait_for_load_state('networkidle')
        
        # 檢查是否需要登入
        try:
            # 尋找登入按鈕或表單
            login_button = await self.page.query_selector('button:has-text("Login")')
            if login_button:
                print("🔐 發現登入按鈕，開始登入流程...")
                await login_button.click()
                await self.page.wait_for_timeout(2000)
                
                # 填入用戶名和密碼
                if username and password:
                    username_input = await self.page.query_selector('input[type="text"], input[name="username"], input[name="email"]')
                    if username_input:
                        await username_input.fill(username)
                        print(f"✅ 已填入用戶名: {username}")
                    
                    password_input = await self.page.query_selector('input[type="password"]')
                    if password_input:
                        await password_input.fill(password)
                        print("✅ 已填入密碼")
                    
                    # 提交登入表單
                    submit_button = await self.page.query_selector('button[type="submit"], button:has-text("Sign In"), button:has-text("Login")')
                    if submit_button:
                        await submit_button.click()
                        print("🚀 已提交登入表單")
                        await self.page.wait_for_load_state('networkidle')
                
                # 或者使用 API 金鑰登入
                elif api_key:
                    api_key_input = await self.page.query_selector('input[name="api_key"], input[placeholder*="API"], input[placeholder*="key"]')
                    if api_key_input:
                        await api_key_input.fill(api_key)
                        print("✅ 已填入 API 金鑰")
                        
                        submit_button = await self.page.query_selector('button[type="submit"], button:has-text("Connect")')
                        if submit_button:
                            await submit_button.click()
                            print("🚀 已提交 API 金鑰")
                            await self.page.wait_for_load_state('networkidle')
            
            print("✅ 登入完成！")
            return True
            
        except Exception as e:
            print(f"❌ 登入過程中發生錯誤: {e}")
            return False
    
    async def load_flow_from_file(self, flow_file_path):
        """從檔案載入 Langflow 流程"""
        try:
            print(f"📁 正在載入流程檔案: {flow_file_path}")
            
            # 讀取流程檔案
            with open(flow_file_path, 'r', encoding='utf-8') as f:
                flow_data = json.load(f)
            
            # 尋找載入流程的按鈕
            load_button = await self.page.query_selector('button:has-text("Load"), button:has-text("Import"), button:has-text("Upload")')
            if load_button:
                await load_button.click()
                await self.page.wait_for_timeout(1000)
            
            # 尋找檔案上傳輸入
            file_input = await self.page.query_selector('input[type="file"]')
            if file_input:
                await file_input.set_input_files(flow_file_path)
                print("✅ 已上傳流程檔案")
                await self.page.wait_for_timeout(2000)
            
            # 或者直接貼上 JSON 內容
            else:
                # 尋找 JSON 輸入區域
                json_input = await self.page.query_selector('textarea, .json-editor, [contenteditable="true"]')
                if json_input:
                    await json_input.click()
                    await json_input.fill(json.dumps(flow_data, indent=2))
                    print("✅ 已貼上流程 JSON 內容")
                    
                    # 尋找應用按鈕
                    apply_button = await self.page.query_selector('button:has-text("Apply"), button:has-text("Load"), button:has-text("Import")')
                    if apply_button:
                        await apply_button.click()
                        print("🚀 已應用流程配置")
                        await self.page.wait_for_timeout(2000)
            
            return True
            
        except Exception as e:
            print(f"❌ 載入流程時發生錯誤: {e}")
            return False
    
    async def run_flow(self):
        """執行流程"""
        try:
            print("▶️ 正在執行流程...")
            
            # 尋找執行按鈕
            run_button = await self.page.query_selector('button:has-text("Run"), button:has-text("Start"), button:has-text("Execute")')
            if run_button:
                await run_button.click()
                print("🚀 已開始執行流程")
                
                # 等待執行完成
                await self.page.wait_for_timeout(5000)
                
                # 檢查執行結果
                result_area = await self.page.query_selector('.result, .output, .response')
                if result_area:
                    result_text = await result_area.text_content()
                    print(f"📊 執行結果: {result_text}")
                
                return True
            else:
                print("❌ 找不到執行按鈕")
                return False
                
        except Exception as e:
            print(f"❌ 執行流程時發生錯誤: {e}")
            return False
    
    async def take_screenshot(self, filename="langflow_screenshot.png"):
        """截圖"""
        try:
            await self.page.screenshot(path=filename)
            print(f"📸 已截圖保存到: {filename}")
        except Exception as e:
            print(f"❌ 截圖失敗: {e}")
    
    async def close_browser(self):
        """關閉瀏覽器"""
        if self.browser:
            await self.browser.close()
            print("🔒 瀏覽器已關閉")

async def main():
    """主函數"""
    # 從環境變數讀取配置
    langflow_url = os.getenv("LANGFLOW_URL", "http://localhost:7860")
    username = os.getenv("LANGFLOW_USERNAME")
    password = os.getenv("LANGFLOW_PASSWORD")
    api_key = os.getenv("LANGFLOW_API_KEY")
    
    # 流程檔案路徑
    flow_file = "examples/enhanced-astra-rag-flow.json"
    
    # 建立自動化實例
    automation = LangflowAutomation(langflow_url)
    
    try:
        # 啟動瀏覽器
        await automation.start_browser()
        
        # 登入
        login_success = await automation.login_to_langflow(username, password, api_key)
        if not login_success:
            print("❌ 登入失敗，無法繼續")
            return
        
        # 載入流程
        if Path(flow_file).exists():
            load_success = await automation.load_flow_from_file(flow_file)
            if load_success:
                print("✅ 流程載入成功")
                
                # 執行流程
                await automation.run_flow()
            else:
                print("❌ 流程載入失敗")
        else:
            print(f"❌ 找不到流程檔案: {flow_file}")
        
        # 截圖
        await automation.take_screenshot()
        
    except Exception as e:
        print(f"❌ 發生錯誤: {e}")
    
    finally:
        # 關閉瀏覽器
        await automation.close_browser()

if __name__ == "__main__":
    print("🚀 開始 Langflow 自動化流程...")
    asyncio.run(main())
