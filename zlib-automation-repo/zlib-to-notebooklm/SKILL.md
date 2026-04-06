# zlib-to-notebooklm

一键从 Z-Library 下载书籍并上传到 Google NotebookLM。下载用纯 API，上传用 Playwright 操作浏览器。

## 触发条件

当用户提到以下意图时自动触发：
- Z-Library / Z站 / zlib 下载书籍并上传到 NotebookLM
- "搜索XX书传到Notebook"、"下载这本到NotebookLM"
- 提供 Z-Library 链接并要求上传到 NotebookLM

## 前置条件

### 1. Python 依赖
```bash
pip install requests playwright
playwright install chromium
```

### 2. Z-Library 登录
- 会话文件: `~/.zlibrary/session.json`
- 需包含 `remix_userid` 和 `remix_userkey`

### 3. NotebookLM 登录状态
- 登录态文件: `~/.notebooklm/storage_state.json`
- 首次使用会自动打开浏览器要求登录，登录后自动保存状态
- 后续使用会自动加载已保存的登录状态

### 4. Chromium 浏览器
- Playwright 自带的 Chromium 即可
- 安装: `playwright install chromium`

### 5. 下载目录
- 默认: `D:/zlib_downloads`（Windows）

## 脚本位置

```
d:\WorkBuddy\zlib-automation\zlib_api_to_notebooklm.py
```

## 使用方法

Python 解释器路径:
```
C:\Users\Administrator\.workbuddy\binaries\python\envs\default\Scripts\python.exe
```

### 场景 1: 按关键词搜索 + 下载 + 上传 NotebookLM

用户说: "帮我搜一本 python basics 的书传到 NotebookLM"

```bash
python d:\WorkBuddy\zlib-automation\zlib_api_to_notebooklm.py --search "python basics" --nb "Python学习笔记"
```

参数说明:
- `--search "关键词"`: 搜索书籍
- `--nb "笔记本标题"`: NotebookLM 笔记本标题（可选，默认用书名）
- `--ext pdf epub`: 限定文件格式（可选）
- `--limit 10`: 搜索结果数量（可选，默认 5）
- `--index 0`: 选择第几本（从 0 开始，可选，默认 0）

### 场景 2: 通过 Z-Library URL 下载 + 上传

用户说: "把这本书 https://z-lib.is/book/17507364 传到 NotebookLM"

```bash
python d:\WorkBuddy\zlib-automation\zlib_api_to_notebooklm.py --url "https://z-lib.is/book/17507364"
```

### 场景 3: 通过书籍 ID 下载 + 上传

```bash
python d:\WorkBuddy\zlib-automation\zlib_api_to_notebooklm.py --id 17507364 --nb "我的笔记本"
```

### 场景 4: 仅下载不上传

```bash
python d:\WorkBuddy\zlib-automation\zlib_api_to_notebooklm.py --search "python" --download-only
```

## AI 操作指南

1. 用户提到 Z-Library + NotebookLM 时，提取关键词/URL/ID
2. 如果用户提到笔记本标题，用 `--nb "标题"`；否则不传，默认用书名
3. 直接运行命令
4. **重要**: 上传阶段会弹出 Chromium 浏览器窗口（headless=False），提示用户不要关闭
5. 整个上传过程约需 30-40 秒
6. 检查输出中的 `[OK]` 或 `[FAIL]` 判断结果

## NotebookLM 上传流程（自动化）

1. 打开 Chromium（加载已保存的登录态）
2. 访问 `https://notebooklm.google.com`
3. 点击 "New" 按钮
4. 点击 "Upload files" 按钮
5. 选择文件并上传
6. 等待 NotebookLM 处理完成

## 故障排查

- **未找到登录会话**: 需要先登录 Z-Library
- **NotebookLM 需要登录**: 会自动弹出浏览器让用户手动登录，登录后状态会自动保存
- **New 按钮找不到**: NotebookLM UI 可能已更新，需要检查选择器
- **上传按钮找不到**: 同上，可能需要更新选择器
- **浏览器超时**: 网络问题或 Google 服务不可用

## 注意事项

- 上传时会打开可见的浏览器窗口，不要关闭
- NotebookLM UI 可能随时更新，选择器可能失效需要维护
- 首次使用需要手动登录 Google 账号
- 下载完成后会自动进入上传流程，期间需要网络通畅
