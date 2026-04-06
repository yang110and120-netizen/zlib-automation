#!/bin/bash
# 一键安装脚本（Linux/macOS）

set -e

echo "=================================="
echo "Z-Library to IMA 知识库 - 安装向导"
echo "=================================="

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装"
    exit 1
fi

echo "✅ Python: $(python3 --version)"

# 安装依赖
echo ""
echo "📦 安装 Python 依赖..."
pip3 install -r requirements.txt

# 安装浏览器
echo ""
echo "🌐 安装浏览器..."
playwright install chromium

# 检查配置
echo ""
echo "🔍 检查配置..."
python3 scripts/test_config.py

echo ""
echo "=================================="
echo "安装完成！"
echo "=================================="
echo ""
echo "下一步："
echo "1. 配置 IMA API 凭证（参考 SETUP_IMA.md）"
echo "2. 登录 Z-Library: python scripts/login.py"
echo "3. 开始使用: python scripts/upload.py --help"