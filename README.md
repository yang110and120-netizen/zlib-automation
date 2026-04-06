# 📚 Zlib Automation

本项目基于 [zstmfhy/zlibrary-to-notebooklm](https://github.com/zstmfhy/zlibrary-to-notebooklm) 二次开发，并扩展支持 WorkBuddy / OpenClaw。

---

## ✨ 特性（Features）
- **zlib-to-ima**：一键检索并下载 Z-Library 图书，上传至腾讯 IMA 知识库。
- **zlib-to-notebooklm**：方便将 Z-Library 图书自动上传至 Google NotebookLM。
- **quark-to-ima**：支持从夸克网盘下载资料自动转存至腾讯 IMA。

---

## ⚡ 安装与用法（Quick Start）

### 基础依赖

```bash
pip install requests playwright cos-python-sdk-v5 quarkpan
playwright install chromium
```

### zlib-to-ima 示例

```bash
python zlib_api_to_ima.py --search "python" --kb "技术书库"
python zlib_api_to_ima.py --url "https://z-lib.is/book/xxxx" --kb "知识库名"
```

### zlib-to-notebooklm 示例

```bash
python zlib_api_to_notebooklm.py --search "人工智能" --nb "AI资料库"
python zlib_api_to_notebooklm.py --url "https://z-lib.is/book/xxxx"
```

### quark-to-ima 示例

```bash
python quark_to_ima.py --url "https://pan.quark.cn/s/xxx" --pwd "提取码" --kb "知识库名"
python quark_to_ima.py --file "路径/书.pdf" --kb "技术书库"
```

---

## ℹ️ 配置说明
- Z-Library 会话：`~/.zlibrary/session.json`   （含 remix_userid + remix_userkey）
- NotebookLM 登录：`~/.notebooklm/storage_state.json`（首次运行扫码登陆）
- IMA API 凭证：`~/.config/ima/client_id` 及 `api_key`
- 夸克网盘登录：`~/.config/quark/cookie.json`

---

## 📦 文件格式支持
| 类型   | 格式                        | 大小限���    |
|--------|-----------------------------|-------------|
| 文档   | PDF, DOC, DOCX, PPT, PPTX   | 200MB       |
| 表格   | XLS, XLSX, CSV              | 10MB        |
| 文本   | MD, TXT                     | 10MB        |
| 图片   | PNG, JPG, JPEG, WEBP        | --          |

---

## 🙏 致谢（Acknowledgments）
本工具感谢原项目 [zstmfhy/zlibrary-to-notebooklm](https://github.com/zstmfhy/zlibrary-to-notebooklm) 的优秀基础和启发。

---

## 📄 License
MIT