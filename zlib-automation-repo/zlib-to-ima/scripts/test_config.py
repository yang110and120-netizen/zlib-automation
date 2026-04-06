#!/usr/bin/env python3
"""
配置检查脚本
验证 IMA API 凭证和 Z-Library 会话是否正确配置
"""

import os
from pathlib import Path

def check_ima_config():
    """检查 IMA API 配置"""
    print("="*60)
    print("检查 IMA API 配置")
    print("="*60)
    
    # 检查环境变量
    client_id_env = os.environ.get("IMA_OPENAPI_CLIENTID")
    api_key_env = os.environ.get("IMA_OPENAPI_APIKEY")
    
    # 检查配置文件
    config_dir = Path.home() / ".config" / "ima"
    client_id_file = config_dir / "client_id"
    api_key_file = config_dir / "api_key"
    
    client_id = client_id_env or (client_id_file.read_text(encoding='utf-8').strip() if client_id_file.exists() else None)
    api_key = api_key_env or (api_key_file.read_text(encoding='utf-8').strip() if api_key_file.exists() else None)
    
    if client_id and api_key:
        print("[OK] IMA API 凭证已配置")
        print(f"   Client ID: {client_id[:10]}...{client_id[-10:]}")
        print(f"   API Key: {api_key[:10]}...{api_key[-10:]}")
        return True
    else:
        print("[FAIL] IMA API 凭证未配置")
        print("\n配置方法：")
        print("1. 访问 https://ima.qq.com/agent-interface")
        print("2. 获取 Client ID 和 API Key")
        print("3. 运行以下命令：")
        print(f"   mkdir -p {config_dir}")
        print(f"   echo 'YOUR_CLIENT_ID' > {client_id_file}")
        print(f"   echo 'YOUR_API_KEY' > {api_key_file}")
        return False

def check_zlib_session():
    """检查 Z-Library 会话"""
    print("\n" + "="*60)
    print("检查 Z-Library 会话")
    print("="*60)
    
    session_file = Path.home() / ".zlibrary" / "session.json"
    
    if session_file.exists():
        print("[OK] Z-Library 会话已保存")
        print(f"   位置: {session_file}")
        return True
    else:
        print("[FAIL] Z-Library 会话未找到")
        print("\n登录方法：")
        print("python ~/.workbuddy/skills/zlib-to-ima/scripts/login.py")
        return False

def check_dependencies():
    """检查依赖"""
    print("\n" + "="*60)
    print("检查依赖")
    print("="*60)
    
    deps = {
        'playwright': False,
        'ebooklib': False,
        'requests': False
    }
    
    for dep in deps:
        try:
            __import__(dep)
            deps[dep] = True
            print(f"[OK] {dep}")
        except ImportError:
            print(f"[FAIL] {dep} 未安装")
    
    return all(deps.values())

def main():
    """主函数"""
    print("\n[配置检查工具]\n")
    
    ima_ok = check_ima_config()
    zlib_ok = check_zlib_session()
    deps_ok = check_dependencies()
    
    print("\n" + "="*60)
    print("检查结果")
    print("="*60)
    
    if all([ima_ok, zlib_ok, deps_ok]):
        print("[OK] 所有配置正确！可以开始使用了")
        print("\n使用示例：")
        print('python scripts/upload.py --url "Z站链接" --kb "知识库名"')
    else:
        print("[FAIL] 部分配置缺失，请按照上述提示完成配置")
    
    print()

if __name__ == "__main__":
    main()
