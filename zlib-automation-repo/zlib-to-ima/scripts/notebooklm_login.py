#!/usr/bin/env python3
"""
NotebookLM 登录脚本
"""

import asyncio
import sys
from pathlib import Path

# 添加 notebooklm 虚拟环境的包路径
notebooklm_env = Path("C:/Users/Administrator/.workbuddy/binaries/python/envs/notebooklm/Lib/site-packages")
if str(notebooklm_env) not in sys.path:
    sys.path.insert(0, str(notebooklm_env))

from notebooklm import NotebookLMClient

async def login():
    """登录 NotebookLM"""
    print("="*60)
    print("NotebookLM 登录")
    print("="*60)
    print("\n即将打开浏览器进行登录...")
    print("请使用 Google 账号登录 NotebookLM")
    print("登录完成后，关闭浏览器即可\n")
    
    try:
        # 这会打开浏览器进行登录
        client = await NotebookLMClient.create_with_browser_login()
        print("[OK] 登录成功!")
        print("   凭据已保存，后续使用无需重复登录")
        return True
    except Exception as e:
        print(f"[FAIL] 登录失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(login())
    sys.exit(0 if success else 1)
