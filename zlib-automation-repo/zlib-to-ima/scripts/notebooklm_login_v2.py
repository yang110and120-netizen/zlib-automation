#!/usr/bin/env python3
"""
NotebookLM 登录脚本 - 使用系统 Chrome
"""

import asyncio
import sys
from pathlib import Path

# 添加 notebooklm 虚拟环境的包路径
notebooklm_env = Path("C:/Users/Administrator/.workbuddy/binaries/python/envs/notebooklm/Lib/site-packages")
if str(notebooklm_env) not in sys.path:
    sys.path.insert(0, str(notebooklm_env))

from playwright.async_api import async_playwright
import json

# NotebookLM 登录页面
NOTEBOOKLM_LOGIN_URL = "https://notebooklm.google.com"

async def login_with_system_chrome():
    """使用系统 Chrome 登录 NotebookLM"""
    print("="*60)
    print("NotebookLM 登录 (使用系统 Chrome)")
    print("="*60)
    print("\n即将打开浏览器进行登录...")
    print("请使用 Google 账号登录 NotebookLM")
    print("登录完成后，请按回车键保存会话\n")
    
    # 存储路径
    storage_dir = Path.home() / ".notebooklm"
    storage_dir.mkdir(exist_ok=True)
    storage_file = storage_dir / "storage_state.json"
    browser_profile = storage_dir / "browser_profile"
    browser_profile.mkdir(exist_ok=True)
    
    async with async_playwright() as p:
        # 使用系统 Chrome
        print("[浏览器] 启动系统 Chrome...")
        try:
            browser = await p.chromium.launch(
                headless=False,
                channel="chrome",
                args=['--disable-blink-features=AutomationControlled']
            )
        except Exception as e:
            print(f"[FAIL] 无法启动 Chrome: {e}")
            print("       请确保已安装 Chrome 浏览器")
            return False
        
        # 创建上下文
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            # 访问 NotebookLM
            print("[登录] 打开 NotebookLM...")
            await page.goto(NOTEBOOKLM_LOGIN_URL, wait_until='networkidle', timeout=60000)
            
            print("\n" + "="*60)
            print("请在浏览器中完成 Google 登录")
            print("登录完成后，关闭浏览器窗口")
            print("="*60 + "\n")
            
            # 等待浏览器关闭
            while True:
                await asyncio.sleep(1)
                try:
                    # 检查页面是否还在
                    await page.evaluate("1")
                except:
                    # 浏览器已关闭
                    break
            
            # 保存会话状态
            print("\n[保存] 正在保存登录状态...")
            storage_state = await context.storage_state()
            with open(storage_file, 'w', encoding='utf-8') as f:
                json.dump(storage_state, f, indent=2)
            
            print(f"[OK] 登录状态已保存到: {storage_file}")
            print("[OK] 后续使用无需重复登录")
            return True
            
        except Exception as e:
            print(f"[FAIL] 登录过程出错: {e}")
            return False
        finally:
            try:
                await context.close()
                await browser.close()
            except:
                pass

if __name__ == "__main__":
    success = asyncio.run(login_with_system_chrome())
    sys.exit(0 if success else 1)
