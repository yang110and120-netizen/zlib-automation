#!/usr/bin/env python3
"""
Z-Library 登录脚本
保存登录会话到本地，后续下载时自动使用
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright

# 配置
ZLIB_SESSION_FILE = Path.home() / ".zlibrary" / "session.json"
ZLIB_LOGIN_URL = "https://zh.zlib.li/"

async def login_zlibrary():
    """打开浏览器登录Z-Library并保存会话"""
    
    print("[浏览器] 正在启动浏览器...")
    
    async with async_playwright() as p:
        # 启动浏览器（非无头模式，用户需要手动登录）
        # 优先使用系统已安装的 Chrome，避免下载 Chromium
        try:
            browser = await p.chromium.launch(
                headless=False,
                channel="chrome"  # 使用系统 Chrome
            )
        except Exception:
            # 如果 Chrome 不可用，尝试 Edge
            try:
                browser = await p.chromium.launch(
                    headless=False,
                    channel="msedge"
                )
            except Exception:
                # 最后尝试默认 chromium
                browser = await p.chromium.launch(headless=False)
        
        context = await browser.new_context()
        page = await context.new_page()
        
        print(f"[Z-Library] 正在打开: {ZLIB_LOGIN_URL}")
        await page.goto(ZLIB_LOGIN_URL)
        
        print("\n" + "="*60)
        print("请在浏览器中完成以下操作：")
        print("1. 登录你的 Z-Library 账号")
        print("2. 确保登录成功后")
        print("3. 回到此终端按回车键继续")
        print("="*60)
        
        try:
            input("\n按回车键保存登录状态...")
        except EOFError:
            # 如果无法读取输入（比如在某些IDE中），等待30秒后自动保存
            print("\n[等待] 30秒后将自动保存会话...")
            await asyncio.sleep(30)
        
        # 保存会话状态
        print("[保存] 正在保存登录状态...")
        session_dir = ZLIB_SESSION_FILE.parent
        session_dir.mkdir(parents=True, exist_ok=True)
        
        # 获取cookies和storage状态
        storage_state = await context.storage_state()
        
        with open(ZLIB_SESSION_FILE, 'w', encoding='utf-8') as f:
            json.dump(storage_state, f, ensure_ascii=False, indent=2)
        
        print(f"[OK] 登录状态已保存到: {ZLIB_SESSION_FILE}")
        
        await browser.close()

def main():
    """主函数"""
    print("="*60)
    print("Z-Library 登录工具")
    print("="*60)
    
    # 检查是否已登录
    if ZLIB_SESSION_FILE.exists():
        print(f"\n[注意] 已存在登录会话: {ZLIB_SESSION_FILE}")
        choice = input("是否重新登录？(y/n): ").strip().lower()
        if choice != 'y':
            print("取消登录")
            return
    
    # 执行登录
    try:
        asyncio.run(login_zlibrary())
        print("\n[完成] 登录完成！现在可以使用 upload.py 下载书籍了")
    except KeyboardInterrupt:
        print("\n[中断] 登录被中断")
    except Exception as e:
        print(f"\n[错误] 登录失败: {e}")

if __name__ == "__main__":
    main()
