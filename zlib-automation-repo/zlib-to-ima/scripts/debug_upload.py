#!/usr/bin/env python3
"""
调试上传脚本
"""

import sys
import os

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Python version:", sys.version)
print("Starting debug...")

try:
    print("Importing modules...")
    import asyncio
    import argparse
    import json
    import tempfile
    from pathlib import Path
    
    print("Importing playwright...")
    from playwright.async_api import async_playwright
    
    print("Importing requests...")
    import requests
    
    print("All imports successful!")
    
    # 测试参数解析
    print("\nTesting argument parsing...")
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--kb", required=True)
    args = parser.parse_args(['--url', 'https://zh.zlib.li/book/w9pzqBZP8b/%E9%95%BF%E5%AE%89%E7%9A%84%E8%8D%94%E6%9E%9D.html', '--kb', '默认知识库'])
    print(f"URL: {args.url}")
    print(f"KB: {args.kb}")
    
    # 测试配置加载
    print("\nTesting config loading...")
    ZLIB_SESSION_FILE = Path.home() / ".zlibrary" / "session.json"
    IMA_CONFIG_DIR = Path.home() / ".config" / "ima"
    
    print(f"Session file: {ZLIB_SESSION_FILE}")
    print(f"Session exists: {ZLIB_SESSION_FILE.exists()}")
    print(f"IMA config dir: {IMA_CONFIG_DIR}")
    
    if IMA_CONFIG_DIR.exists():
        client_id_file = IMA_CONFIG_DIR / "client_id"
        api_key_file = IMA_CONFIG_DIR / "api_key"
        print(f"Client ID exists: {client_id_file.exists()}")
        print(f"API Key exists: {api_key_file.exists()}")
    
    print("\nDebug completed successfully!")
    
except Exception as e:
    import traceback
    print(f"\nError occurred: {e}")
    traceback.print_exc()
    sys.exit(1)
