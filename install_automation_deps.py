#!/usr/bin/env python3
"""
安裝 Langflow 自動化所需的依賴
"""

import subprocess
import sys
import os

def install_package(package):
    """安裝 Python 套件"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ 已安裝 {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 安裝 {package} 失敗: {e}")
        return False

def main():
    """主函數"""
    print("🚀 開始安裝 Langflow 自動化依賴...")
    
    # 需要安裝的套件
    packages = [
        "playwright",
        "asyncio",
        "pathlib"
    ]
    
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
    
    # 安裝 Playwright 瀏覽器
    print("\n🌐 安裝 Playwright 瀏覽器...")
    try:
        subprocess.check_call([sys.executable, "-m", "playwright", "install"])
        print("✅ Playwright 瀏覽器安裝完成")
        success_count += 1
    except subprocess.CalledProcessError as e:
        print(f"❌ Playwright 瀏覽器安裝失敗: {e}")
    
    print(f"\n📊 安裝完成: {success_count}/{len(packages)+1} 個套件成功安裝")
    
    if success_count == len(packages) + 1:
        print("🎉 所有依賴安裝完成！")
        print("\n📝 下一步:")
        print("1. 編輯 langflow_config.json 填入您的登入資訊")
        print("2. 執行: python run_langflow_automation.py")
    else:
        print("⚠️ 部分套件安裝失敗，請手動安裝")

if __name__ == "__main__":
    main()
