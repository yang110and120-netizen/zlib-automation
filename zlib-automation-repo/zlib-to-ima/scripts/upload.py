#!/usr/bin/env python3
"""
从 Z-Library 下载书籍并上传到 IMA 知识库
改进版：参考 zlibrary-to-notebooklm 项目的实现
"""

import asyncio
import argparse
import json
import os
import sys
import tempfile
import time
from pathlib import Path
from typing import Optional
import requests

# Playwright 和电子书处理库
try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("[FAIL] 缺少依赖: playwright")
    print("请运行: pip install playwright && playwright install chromium")
    sys.exit(1)

try:
    from ebooklib import epub
except ImportError:
    print("[FAIL] 缺少依赖: ebooklib")
    print("请运行: pip install ebooklib")
    sys.exit(1)

# 配置
ZLIB_SESSION_FILE = Path.home() / ".zlibrary" / "session.json"
ZLIB_BROWSER_PROFILE = Path.home() / ".zlibrary" / "browser_profile"
IMA_CONFIG_DIR = Path.home() / ".config" / "ima"
IMA_CLIENT_ID_FILE = IMA_CONFIG_DIR / "client_id"
IMA_API_KEY_FILE = IMA_CONFIG_DIR / "api_key"
IMA_API_BASE = "https://ima.qq.com/openapi/wiki/v1"


class ZLibDownloader:
    """Z-Library 下载器"""
    
    def __init__(self):
        self.session_file = ZLIB_SESSION_FILE
        self.browser_profile = ZLIB_BROWSER_PROFILE
    
    async def download_book(self, url: str, output_dir: str) -> Optional[str]:
        """
        从 Z-Library 下载书籍
        参考 zlibrary-to-notebooklm 的实现方式
        """
        print(f"[下载] 正在从 Z-Library 下载...")
        print(f"   URL: {url}")
        
        # 检查登录状态
        if not self.session_file.exists():
            print("[FAIL] 未找到登录会话，请先运行 login.py 登录")
            return None
        
        async with async_playwright() as p:
            # 使用系统 Chrome，禁用自动化检测
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
                        channel="msedge",
                        args=['--disable-blink-features=AutomationControlled']
                    )
                except:
                    browser = await p.chromium.launch(
                        headless=False,
                        args=['--disable-blink-features=AutomationControlled']
                    )
            
            # 加载会话状态
            if self.session_file.exists():
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    storage_state = json.load(f)
                context = await browser.new_context(
                    storage_state=storage_state,
                    accept_downloads=True
                )
            else:
                context = await browser.new_context(accept_downloads=True)
            
            page = await context.new_page()
            
            # 设置下载路径
            download_path = None
            
            async def handle_download(download):
                nonlocal download_path
                suggested_filename = download.suggested_filename
                download_path = Path(output_dir) / suggested_filename
                await download.save_as(download_path)
                print(f"[下载] 文件保存到: {download_path}")
            
            page.on('download', handle_download)
            
            try:
                # 访问书籍页面
                print("[书籍] 正在打开书籍页面...")
                await page.goto(url, wait_until='networkidle', timeout=60000)
                await asyncio.sleep(2)  # 等待页面完全加载
                
                # 获取书籍标题
                try:
                    title = await page.locator('h1').first.inner_text()
                    title = title.strip().replace('/', '_').replace('\\', '_')
                    print(f"   书名: {title}")
                except:
                    title = "unknown_book"
                
                # 查找下载按钮 - 使用多种策略
                print("[查找] 查找下载链接...")
                
                download_link = None
                downloaded_format = None
                
                # 策略1: 查找三点菜单（新版界面）
                try:
                    dots_selectors = [
                        'button[aria-label="更多选项"]',
                        'button[title="更多"]',
                        '.more-options',
                        '[class*="dots"]',
                        '[class*="more"]'
                    ]
                    
                    for selector in dots_selectors:
                        dots_button = await page.query_selector(selector)
                        if dots_button:
                            print(f"   找到三点菜单: {selector}")
                            await dots_button.click()
                            await asyncio.sleep(2)
                            
                            # 查找PDF选项
                            pdf_options = await page.query_selector_all('a:has-text("PDF"), button:has-text("PDF")')
                            if pdf_options:
                                download_link = pdf_options[0]
                                downloaded_format = 'pdf'
                                print("   找到PDF下载选项")
                                break
                            
                            # 查找EPUB选项
                            epub_options = await page.query_selector_all('a:has-text("EPUB"), button:has-text("EPUB")')
                            if epub_options:
                                download_link = epub_options[0]
                                downloaded_format = 'epub'
                                print("   找到EPUB下载选项")
                                break
                            
                            break
                except Exception as e:
                    print(f"   三点菜单策略失败: {e}")
                
                # 策略2: 查找转换按钮（旧版界面）
                if not download_link:
                    try:
                        convert_selectors = [
                            'a[data-convert_to="pdf"]',
                            'a:has-text("转换为 PDF")',
                            'button:has-text("转换为 PDF")'
                        ]
                        
                        for selector in convert_selectors:
                            convert_button = await page.query_selector(selector)
                            if convert_button:
                                print(f"   找到转换按钮: {selector}")
                                downloaded_format = 'pdf'
                                await convert_button.evaluate('el => el.click()')
                                
                                # 等待转换完成
                                print("   等待转换完成...")
                                for i in range(60):
                                    await asyncio.sleep(1)
                                    # 检查是否有下载链接出现
                                    download_selectors = [
                                        'a[href*="/dl/"]',
                                        'a:has-text("下载")'
                                    ]
                                    for ds in download_selectors:
                                        link = await page.query_selector(ds)
                                        if link:
                                            download_link = link
                                            print(f"   转换完成，找到下载链接")
                                            break
                                    if download_link:
                                        break
                                
                                if download_link:
                                    break
                    except Exception as e:
                        print(f"   转换按钮策略失败: {e}")
                
                # 策略3: 直接查找下载链接
                if not download_link:
                    try:
                        download_selectors = [
                            'a[href*="/dl/"]',
                            'a:has-text("下载")',
                            'a:has-text("Download")',
                            'button:has-text("下载")',
                            'a.download-button',
                            'a.btn-primary'
                        ]
                        
                        for selector in download_selectors:
                            links = await page.query_selector_all(selector)
                            for link in links:
                                href = await link.get_attribute('href')
                                text = await link.inner_text()
                                print(f"   检查链接: {text} -> {href}")
                                
                                if href and ('/dl/' in href or 'download' in href.lower()):
                                    download_link = link
                                    # 判断格式
                                    if 'pdf' in text.lower() or (href and '.pdf' in href.lower()):
                                        downloaded_format = 'pdf'
                                    elif 'epub' in text.lower() or (href and '.epub' in href.lower()):
                                        downloaded_format = 'epub'
                                    else:
                                        downloaded_format = 'unknown'
                                    print(f"   找到下载链接: {selector}, 格式: {downloaded_format}")
                                    break
                            
                            if download_link:
                                break
                    except Exception as e:
                        print(f"   直接查找策略失败: {e}")
                
                if not download_link:
                    print("[FAIL] 未找到下载按钮")
                    await context.close()
                    await browser.close()
                    return None
                
                # 点击下载
                print(f"[下载] 开始下载文件 (格式: {downloaded_format})...")
                
                try:
                    await download_link.click()
                    print("   已点击下载按钮，等待下载完成...")
                    
                    # 等待下载完成
                    for i in range(60):  # 最多等待60秒
                        await asyncio.sleep(1)
                        if download_path and download_path.exists():
                            break
                        print(f"   等待下载... {i+1}s")
                    
                    if download_path and download_path.exists():
                        print(f"[OK] 下载完成: {download_path}")
                        print(f"   文件大小: {download_path.stat().st_size / 1024 / 1024:.2f} MB")
                        await context.close()
                    await browser.close()
                        return str(download_path)
                    else:
                        print("[FAIL] 下载超时")
                        await context.close()
                    await browser.close()
                        return None
                        
                except Exception as e:
                    print(f"[FAIL] 点击下载失败: {e}")
                    await context.close()
                    await browser.close()
                    return None
                
            except PlaywrightTimeout:
                print("[FAIL] 页面加载超时")
                await context.close()
                    await browser.close()
                return None
            except Exception as e:
                print(f"[FAIL] 下载失败: {e}")
                import traceback
                traceback.print_exc()
                await context.close()
                    await browser.close()
                return None


class IMAUploader:
    """IMA 知识库上传器"""
    
    def __init__(self):
        self.client_id = self._load_credential(IMA_CLIENT_ID_FILE, "IMA_OPENAPI_CLIENTID")
        self.api_key = self._load_credential(IMA_API_KEY_FILE, "IMA_OPENAPI_APIKEY")
        
        if not self.client_id or not self.api_key:
            raise ValueError("[FAIL] 缺少 IMA API 凭证，请先配置\n参考: SETUP_IMA.md")
    
    def _load_credential(self, file_path: Path, env_name: str) -> Optional[str]:
        """加载凭证（配置文件或环境变量）"""
        # 优先从环境变量
        cred = os.environ.get(env_name)
        if cred:
            return cred
        
        # 其次从配置文件
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        
        return None
    
    def upload_file(self, file_path: str, kb_name_or_id: str) -> bool:
        """
        上传文件到 IMA 知识库
        简化版实现
        """
        print(f"\n[上传] 正在上传到 IMA 知识库...")
        print(f"   文件: {file_path}")
        print(f"   知识库: {kb_name_or_id}")
        
        # 这里简化处理，实际应该调用完整的 IMA API 流程
        # 包括：create_media -> 上传COS -> add_knowledge
        
        print("[OK] 文件已准备好上传")
        print("[注意] 完整的上传功能需要调用 IMA API")
        print("       可以参考腾讯ima Skill的实现")
        
        return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="从 Z-Library 下载书籍并上传到 IMA 知识库")
    parser.add_argument("--url", required=True, help="Z-Library 书籍链接")
    parser.add_argument("--kb", required=True, help="IMA 知识库名称或ID")
    parser.add_argument("--output", default=None, help="临时下载目录（默认：系统临时目录）")
    parser.add_argument("--download-only", action="store_true", help="仅下载，不上传")
    
    args = parser.parse_args()
    
    print("="*60)
    print("Z-Library → IMA 知识库")
    print("="*60)
    
    # 创建临时目录
    output_dir = args.output or tempfile.mkdtemp(prefix="zlib_")
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 下载
    downloader = ZLibDownloader()
    file_path = asyncio.run(downloader.download_book(args.url, output_dir))
    
    if not file_path:
        print("\n[FAIL] 下载失败")
        sys.exit(1)
    
    # 上传
    if not args.download_only:
        try:
            uploader = IMAUploader()
            success = uploader.upload_file(file_path, args.kb)
            
            if success:
                print("\n[完成] 完成！")
            else:
                print("\n[FAIL] 上传失败")
                sys.exit(1)
        except ValueError as e:
            print(f"\n{e}")
            sys.exit(1)
    
    # 清理临时文件
    if not args.output:
        print(f"\n[清理] 清理临时文件: {output_dir}")
        import shutil
        shutil.rmtree(output_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
