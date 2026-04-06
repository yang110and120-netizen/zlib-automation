#!/usr/bin/env python3
"""
测试 Z-Library 下载 + NotebookLM 上传
"""

import asyncio
import json
import os
import sys
import tempfile
from pathlib import Path

# 添加 notebooklm 虚拟环境的包路径
notebooklm_env = Path("C:/Users/Administrator/.workbuddy/binaries/python/envs/notebooklm/Lib/site-packages")
if str(notebooklm_env) not in sys.path:
    sys.path.insert(0, str(notebooklm_env))

from playwright.async_api import async_playwright

# 配置
ZLIB_SESSION_FILE = Path.home() / ".zlibrary" / "session.json"
NOTEBOOKLM_STORAGE_FILE = Path.home() / ".notebooklm" / "storage_state.json"

async def download_book(url: str, output_dir: str):
    """从 Z-Library 下载书籍"""
    print("[下载] 正在从 Z-Library 下载...")
    print(f"   URL: {url}")
    
    if not ZLIB_SESSION_FILE.exists():
        print("[FAIL] 未找到登录会话，请先运行 login.py")
        return None
    
    async with async_playwright() as p:
        print("[浏览器] 启动浏览器...")
        try:
            browser = await p.chromium.launch(
                headless=False,
                channel="chrome",
                args=['--disable-blink-features=AutomationControlled']
            )
        except:
            try:
                browser = await p.chromium.launch(
                    headless=False,
                    channel="msedge"
                )
            except:
                browser = await p.chromium.launch(headless=False)
        
        # 加载会话
        with open(ZLIB_SESSION_FILE, 'r', encoding='utf-8') as f:
            storage_state = json.load(f)
        
        context = await browser.new_context(
            storage_state=storage_state,
            accept_downloads=True
        )
        page = await context.new_page()
        
        # 设置下载处理
        download_path = None
        async def handle_download(download):
            nonlocal download_path
            download_path = Path(output_dir) / download.suggested_filename
            await download.save_as(download_path)
        page.on('download', handle_download)
        
        try:
            # 访问页面
            print("[书籍] 正在打开书籍页面...")
            await page.goto(url, wait_until='networkidle', timeout=60000)
            await asyncio.sleep(2)
            
            # 获取标题
            try:
                title = await page.locator('h1').first.inner_text()
                print(f"   书名: {title.strip()}")
            except:
                pass
            
            # 查找下载按钮
            print("[查找] 查找下载链接...")
            
            download_link = None
            
            # 策略1: 三点菜单
            dots_selectors = [
                'button[aria-label="更多选项"]',
                'button[title="更多"]',
                '.more-options',
                '[class*="dots"]'
            ]
            
            for selector in dots_selectors:
                try:
                    btn = await page.query_selector(selector)
                    if btn:
                        print(f"   找到三点菜单")
                        await btn.click()
                        await asyncio.sleep(2)
                        
                        # 查找PDF
                        pdf_links = await page.query_selector_all('a:has-text("PDF")')
                        if pdf_links:
                            download_link = pdf_links[0]
                            print("   找到PDF选项")
                            break
                        break
                except:
                    continue
            
            # 策略2: 直接查找下载链接
            if not download_link:
                selectors = [
                    'a[href*="/dl/"]',
                    'a:has-text("下载")',
                    'a:has-text("Download")',
                    'button:has-text("下载")'
                ]
                
                for selector in selectors:
                    try:
                        links = await page.query_selector_all(selector)
                        for link in links:
                            href = await link.get_attribute('href')
                            if href and ('/dl/' in href or 'download' in href.lower()):
                                download_link = link
                                print(f"   找到下载链接")
                                break
                        if download_link:
                            break
                    except:
                        continue
            
            if not download_link:
                print("[FAIL] 未找到下载按钮")
                await context.close()
                await browser.close()
                return None
            
            # 点击下载
            print("[下载] 开始下载...")
            await download_link.click()
            
            # 等待下载完成
            print("   等待下载完成...")
            for i in range(60):
                await asyncio.sleep(1)
                if download_path and download_path.exists():
                    break
                print(f"   等待... {i+1}s")
            
            if download_path and download_path.exists():
                print(f"[OK] 下载完成: {download_path}")
                print(f"   大小: {download_path.stat().st_size / 1024 / 1024:.2f} MB")
                await context.close()
                await browser.close()
                return str(download_path)
            else:
                print("[FAIL] 下载超时")
                await context.close()
                await browser.close()
                return None
                
        except Exception as e:
            print(f"[FAIL] 错误: {e}")
            await context.close()
            await browser.close()
            return None

async def upload_to_notebooklm(file_path: str, notebook_name: str = "Z-Library 书籍"):
    """上传文件到 NotebookLM"""
    print("\n[NotebookLM] 正在上传...")
    
    if not NOTEBOOKLM_STORAGE_FILE.exists():
        print("[FAIL] 未找到 NotebookLM 登录状态")
        print("       请先运行: notebooklm_login_v2.py")
        return None
    
    try:
        from notebooklm import NotebookLMClient
        
        async with await NotebookLMClient.from_storage() as client:
            # 创建笔记本
            print(f"   创建笔记本: {notebook_name}")
            nb = await client.notebooks.create(notebook_name)
            print(f"   笔记本ID: {nb.id}")
            
            # 添加文件
            print(f"   上传文件: {Path(file_path).name}")
            await client.sources.add_file(nb.id, file_path, wait=True)
            print("[OK] 上传成功!")
            
            return nb.id
            
    except Exception as e:
        print(f"[FAIL] 上传失败: {e}")
        import traceback
        traceback.print_exc()
        return None

async def main():
    url = "https://zh.zlib.li/book/w9pzqBZP8b/%E9%95%BF%E5%AE%89%E7%9A%84%E8%8D%94%E6%9E%9D.html"
    output_dir = "D:/zlib_downloads"
    
    print("="*60)
    print("Z-Library -> NotebookLM 测试")
    print("="*60)
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 下载
    file_path = await download_book(url, output_dir)
    
    if not file_path:
        print("\n[FAIL] 下载失败")
        return
    
    print(f"\n[OK] 下载成功: {file_path}")
    
    # 上传到 NotebookLM
    notebook_id = await upload_to_notebooklm(file_path)
    
    if notebook_id:
        print(f"\n[完成] 笔记本ID: {notebook_id}")
        print("       请访问 https://notebooklm.google.com 查看")
    else:
        print("\n[FAIL] 上传到 NotebookLM 失败")

if __name__ == "__main__":
    asyncio.run(main())
