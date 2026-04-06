#!/usr/bin/env python3
"""
简化版上传脚本
"""

import asyncio
import json
import os
import sys
import tempfile
from pathlib import Path
import requests

# 配置
ZLIB_SESSION_FILE = Path.home() / ".zlibrary" / "session.json"
IMA_CONFIG_DIR = Path.home() / ".config" / "ima"
IMA_API_BASE = "https://ima.qq.com/openapi/wiki/v1"

async def download_book(url: str, output_dir: str):
    """从 Z-Library 下载书籍"""
    from playwright.async_api import async_playwright
    
    print("[下载] 正在从 Z-Library 下载...")
    print(f"   URL: {url}")
    
    if not ZLIB_SESSION_FILE.exists():
        print("[FAIL] 未找到登录会话")
        return None
    
    async with async_playwright() as p:
        with open(ZLIB_SESSION_FILE, 'r', encoding='utf-8') as f:
            storage_state = json.load(f)
        
        try:
            browser = await p.chromium.launch(headless=False, channel="chrome")
        except:
            try:
                browser = await p.chromium.launch(headless=False, channel="msedge")
            except:
                browser = await p.chromium.launch(headless=False)
        
        context = await browser.new_context(storage_state=storage_state)
        page = await context.new_page()
        
        try:
            print("[书籍] 正在打开书籍页面...")
            await page.goto(url, wait_until='networkidle', timeout=60000)
            
            title = await page.locator('h1').first.inner_text()
            title = title.strip().replace('/', '_').replace('\\', '_')
            print(f"   书名: {title}")
            
            print("[查找] 查找下载链接...")
            
            # 尝试多种选择器
            selectors = [
                'a[href*="download"]',
                'a:has-text("下载")',
                'button:has-text("下载")',
                '.download-button',
                '#download-button',
                'a.btn-primary',
            ]
            
            download_button = None
            for selector in selectors:
                try:
                    button = page.locator(selector).first
                    if await button.count() > 0:
                        print(f"   找到按钮: {selector}")
                        download_button = button
                        break
                except:
                    continue
            
            if not download_button:
                print("[FAIL] 未找到下载按钮")
                await browser.close()
                return None
            
            print("[下载] 开始下载文件...")
            
            # 获取下载链接并访问下载页面
            download_href = await download_button.get_attribute('href')
            print(f"   下载链接: {download_href}")
            
            # 构建完整URL并访问下载页面
            base_url = "https://zh.zlib.li"
            if download_href.startswith('/'):
                download_page_url = base_url + download_href
            else:
                download_page_url = download_href
            
            print(f"   访问下载页面: {download_page_url}")
            await page.goto(download_page_url, wait_until='networkidle', timeout=60000)
            
            # 在下载页面查找实际的下载按钮
            print("[查找] 在下载页面查找下载按钮...")
            download_page_selectors = [
                'a[href*="download"]',
                'a:has-text("下载")',
                'button:has-text("下载")',
                '.download-link',
                'a.btn-primary',
            ]
            
            actual_download_button = None
            for selector in download_page_selectors:
                try:
                    button = page.locator(selector).first
                    if await button.count() > 0:
                        print(f"   找到下载按钮: {selector}")
                        actual_download_button = button
                        break
                except:
                    continue
            
            if not actual_download_button:
                print("[FAIL] 在下载页面未找到下载按钮")
                await browser.close()
                return None
            
            # 等待下载
            async with page.expect_download(timeout=300000) as download_info:
                await actual_download_button.click()
            
            download = await download_info.value
            file_path = Path(output_dir) / f"{title}.{download.suggested_filename.split('.')[-1]}"
            await download.save_as(file_path)
            
            print(f"[OK] 下载完成: {file_path}")
            print(f"   文件大小: {file_path.stat().st_size / 1024 / 1024:.2f} MB")
            
            await browser.close()
            return str(file_path)
            
        except Exception as e:
            print(f"[FAIL] 下载失败: {e}")
            await browser.close()
            return None

def upload_to_ima(file_path: str, kb_name: str):
    """上传到 IMA 知识库"""
    print("\n[上传] 正在上传到 IMA 知识库...")
    
    # 加载凭证
    client_id_file = IMA_CONFIG_DIR / "client_id"
    api_key_file = IMA_CONFIG_DIR / "api_key"
    
    client_id = client_id_file.read_text(encoding='utf-8').strip()
    api_key = api_key_file.read_text(encoding='utf-8').strip()
    
    print(f"[OK] 文件已准备好上传: {file_path}")
    print(f"   目标知识库: {kb_name}")
    print("[注意] 完整的上传功能需要调用 IMA API")
    
    return True

async def main():
    url = "https://zh.zlib.li/book/w9pzqBZP8b/%E9%95%BF%E5%AE%89%E7%9A%84%E8%8D%94%E6%9E%9D.html"
    kb_name = "默认知识库"
    
    print("="*60)
    print("Z-Library → IMA 知识库")
    print("="*60)
    
    # 创建临时目录
    output_dir = tempfile.mkdtemp(prefix="zlib_")
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 下载
    file_path = await download_book(url, output_dir)
    
    if not file_path:
        print("\n[FAIL] 下载失败")
        return
    
    # 上传
    upload_to_ima(file_path, kb_name)
    
    print("\n[完成] 处理完成！")

if __name__ == "__main__":
    asyncio.run(main())
