#!/usr/bin/env python3
"""
NotebookLM 登录 - 使用系统 Chrome 并正确保存认证
"""

import asyncio
import json
import sys
from pathlib import Path

# 添加 notebooklm 虚拟环境的包路径
notebooklm_env = Path("C:/Users/Administrator/.workbuddy/binaries/python/envs/notebooklm/Lib/site-packages")
if str(notebooklm_env) not in sys.path:
    sys.path.insert(0, str(notebooklm_env))

from playwright.async_api import async_playwright
import httpx

# NotebookLM 相关 URL
NOTEBOOKLM_URL = "https://notebooklm.google.com"

def save_auth_tokens(cookies, storage_path):
    """保存认证令牌到 notebooklm-py 需要的格式"""
    # notebooklm-py 需要的格式
    auth_data = {
        "cookies": cookies,
        "version": 1
    }
    with open(storage_path, 'w', encoding='utf-8') as f:
        json.dump(auth_data, f, indent=2)
    print(f"[保存] 认证信息已保存到: {storage_path}")

async def login():
    """使用系统 Chrome 登录 NotebookLM"""
    print("="*60)
    print("NotebookLM 登录")
    print("="*60)
    
    # 存储路径
    storage_dir = Path.home() / ".notebooklm"
    storage_dir.mkdir(exist_ok=True)
    storage_file = storage_dir / "storage_state.json"
    
    async with async_playwright() as p:
        print("[浏览器] 启动系统 Chrome...")
        try:
            browser = await p.chromium.launch(
                headless=False,
                channel="chrome",
                args=['--disable-blink-features=AutomationControlled']
            )
        except Exception as e:
            print(f"[FAIL] 无法启动 Chrome: {e}")
            return False
        
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            print("[登录] 打开 NotebookLM...")
            await page.goto(NOTEBOOKLM_URL, wait_until='networkidle', timeout=120000)
            
            # 检查是否已经登录
            current_url = page.url
            if "signin" in current_url or "accounts.google" in current_url:
                print("\n" + "="*60)
                print("请在浏览器中完成 Google 登录")
                print("登录成功后，页面会自动跳转到 NotebookLM")
                print("然后关闭浏览器窗口即可")
                print("="*60 + "\n")
            else:
                print("[OK] 已经登录到 NotebookLM")
            
            # 等待用户完成登录
            print("等待登录完成...")
            while True:
                await asyncio.sleep(2)
                try:
                    current_url = page.url
                    # 检查是否已登录到 NotebookLM
                    if "notebooklm.google.com" in current_url and "signin" not in current_url:
                        print("[OK] 检测到已登录到 NotebookLM")
                        break
                    await page.evaluate("1")  # 检查页面是否还在
                except:
                    print("[注意] 浏览器已关闭")
                    return False
            
            # 等待一下确保所有 cookies 都设置好了
            await asyncio.sleep(3)
            
            # 获取 storage state
            storage_state = await context.storage_state()
            
            # 保存认证信息
            save_auth_tokens(storage_state, storage_file)
            
            print("\n[OK] 登录成功！")
            print(f"   认证信息已保存")
            
            await context.close()
            await browser.close()
            return True
            
        except Exception as e:
            print(f"[FAIL] 登录过程出错: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            try:
                await context.close()
                await browser.close()
            except:
                pass

if __name__ == "__main__":
    success = asyncio.run(login())
    sys.exit(0 if success else 1)
