# 一键安装脚本（Windows PowerShell）

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Z-Library to IMA 知识库 - 安装向导" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ 未找到 Python，请先安装 Python 3.8+" -ForegroundColor Red
    exit 1
}

# 安装依赖
Write-Host ""
Write-Host "📦 安装 Python 依赖..." -ForegroundColor Yellow
pip install -r requirements.txt

# 安装浏览器
Write-Host ""
Write-Host "🌐 安装浏览器..." -ForegroundColor Yellow
playwright install chromium

# 检查配置
Write-Host ""
Write-Host "🔍 检查配置..." -ForegroundColor Yellow
python scripts/test_config.py

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "安装完成！" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步：" -ForegroundColor Yellow
Write-Host "1. 配置 IMA API 凭证（参考 SETUP_IMA.md）"
Write-Host "2. 登录 Z-Library: python scripts/login.py"
Write-Host "3. 开始使用: python scripts/upload.py --help"
Write-Host ""