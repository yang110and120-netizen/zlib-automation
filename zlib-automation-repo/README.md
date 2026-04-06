# zlib-automation

> WorkBuddy / OpenClaw Skills for book automation — search, download, and push to your knowledge base in one command.

A collection of AI agent skills that connect **Z-Library** and **Quark Drive (夸克网盘)** to popular knowledge management tools.

---

## Skills

| Skill | What it does |
|-------|-------------|
| [zlib-to-ima](./zlib-to-ima/) | Search & download books from Z-Library → upload to Tencent IMA knowledge base |
| [zlib-to-notebooklm](./zlib-to-notebooklm/) | Search & download books from Z-Library → upload to Google NotebookLM |
| [quark-to-ima](./quark-to-ima/) | Download files from Quark Drive (夸克网盘) → upload to Tencent IMA knowledge base |

---

## Quick Install

Each skill lives in its own subdirectory. Copy the folder into your WorkBuddy skills directory:

```
~/.workbuddy/skills/<skill-name>/
```

Then reload your agent session — the skill is auto-detected.

---

## zlib-to-ima

一键从 Z-Library 搜索/下载书籍，自动上传到腾讯 IMA 知识库。

**依赖**
```bash
pip install requests cos-python-sdk-v5 playwright
```

**前置配置**
- Z-Library 会话: `~/.zlibrary/session.json`（含 `remix_userid` + `remix_userkey`）
- IMA API 凭证: `~/.config/ima/client_id` 和 `~/.config/ima/api_key`
  - 在 [ima.qq.com/agent-interface](https://ima.qq.com/agent-interface) 申请

**示例**
```bash
# 搜索 + 下载 + 上传
python zlib_api_to_ima.py --search "python basics" --kb "技术书库"

# 通过 URL 上传
python zlib_api_to_ima.py --url "https://z-lib.is/book/17507364" --kb "知识库名"

# 仅下载
python zlib_api_to_ima.py --search "机器学习" --download-only
```

---

## zlib-to-notebooklm

一键从 Z-Library 搜索/下载书籍，自动上传到 Google NotebookLM。

**依赖**
```bash
pip install requests playwright
playwright install chromium
```

**前置配置**
- Z-Library 会话: `~/.zlibrary/session.json`
- NotebookLM 登录态: `~/.notebooklm/storage_state.json`（首次运行会弹浏览器让你登录）

**示例**
```bash
# 搜索 + 上传到 NotebookLM
python zlib_api_to_notebooklm.py --search "deep learning" --nb "AI Reading"

# 通过 URL 上传
python zlib_api_to_notebooklm.py --url "https://z-lib.is/book/17507364"
```

---

## quark-to-ima

一键从夸克网盘下载文件，自动上传到腾讯 IMA 知识库。

**依赖**
```bash
pip install quarkpan cos-python-sdk-v5 requests
```

**前置配置**
- 夸克网盘登录: 运行 `python quark_to_ima.py --login` 扫码登录，自动保存到 `~/.config/quark/cookie.json`
- IMA API 凭证: `~/.config/ima/client_id` 和 `~/.config/ima/api_key`

**IMA 支持的文件格式**

| 类型 | 格式 | 大小限制 |
|------|------|----------|
| 文档 | PDF, DOC, DOCX, PPT, PPTX | 200MB |
| 表格 | XLS, XLSX, CSV | 10MB |
| 文本 | MD, TXT | 10MB |
| 图片 | PNG, JPG, JPEG, WEBP | — |

**示例**
```bash
# 夸克分享链接 → IMA
python quark_to_ima.py --url "https://pan.quark.cn/s/xxx" --pwd "提取码" --kb "知识库名"

# 上传本地文件
python quark_to_ima.py --file "D:/books/book.pdf" --kb "技术书库"

# 查看 IMA 知识库列表
python quark_to_ima.py --list-kb

# 扫码登录夸克
python quark_to_ima.py --login
```

---

## IMA API 凭证配置

所有用到 IMA 的 skill 都需要配置凭证：

1. 访问 [ima.qq.com/agent-interface](https://ima.qq.com/agent-interface) 申请 OpenAPI 权限
2. 获取 Client ID 和 API Key
3. 保存到本地：

```bash
# Linux / macOS
mkdir -p ~/.config/ima
echo "YOUR_CLIENT_ID" > ~/.config/ima/client_id
echo "YOUR_API_KEY"   > ~/.config/ima/api_key

# Windows PowerShell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.config\ima"
"YOUR_CLIENT_ID" | Out-File "$env:USERPROFILE\.config\ima\client_id" -Encoding UTF8
"YOUR_API_KEY"   | Out-File "$env:USERPROFILE\.config\ima\api_key"   -Encoding UTF8
```

---

## Python 解释器

推荐使用 WorkBuddy 内置 Python 环境（已预装所有依赖）：

```
C:\Users\<你的用户名>\.workbuddy\binaries\python\envs\default\Scripts\python.exe
```

---

## License

MIT
