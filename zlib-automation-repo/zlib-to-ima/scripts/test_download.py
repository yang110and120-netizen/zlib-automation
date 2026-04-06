#!/usr/bin/env python3
"""
测试下载脚本
"""

import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

ZLIB_SESSION_FILE = Path.home() / ".zlibrary" / "session.json"

async def test_download():
    url = "https://zh.zlib.li/book/w9pzqBZP8b/%E9%95%BF%E5%AE%89%E7%9A%84%E8%8D%94%E6%9E%9D.html"
    
    print("Testing download...")
    print(f"Session file: {ZLIB_SESSION_FILE}")
    print(f"Session exists: {ZLIB_SESSION_FILE.exists()}")
    
    if not ZLIB_SESSION_FILE.exists():
        print("Session not found!")
        return
    
    async with async_playwright() as p:
        # 加载会话
        with open(ZLIB_SESSION_FILE, 'r', encoding='utf-8') as f:
            storage_state = json.load(f)
        
        print("Launching browser...")
        try:
            browser = await p.chromium.launch(headless=True, channel="chrome")
            print("Using Chrome")
        except Exception as e:
            print(f"Chrome failed: {e}")
            try:
                browser = await p.chromium.launch(headless=True, channel="msedge")
                print("Using Edge")
            except Exception as e:
                print(f"Edge failed: {e}")
                browser = await p.chromium.launch(headless=True)
                print("Using default chromium")
        
        context = await browser.new_context(storage_state=storage_state)
        page = await context.new_page()
        
        print(f"Navigating to: {url}")
        await page.goto(url, wait_until='networkidle', timeout=60000)
        
        # 获取标题
        title = await page.locator('h1').first.inner_text()
        print(f"Book title: {title}")
        
        await browser.close()
        print("Test completed!")

if __name__ == "__main__":
    asyncio.run(test_download())
