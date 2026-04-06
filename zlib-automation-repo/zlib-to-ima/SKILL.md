# zlib-to-ima

一键从 Z-Library 下载书籍并上传到腾讯 IMA 知识库。纯 API 方案，无需浏览器。

## 触发条件

当用户提到以下意图时自动触发：
- Z-Library / Z站 / zlib 下载书籍并上传到 IMA
- "搜索XX书上传到IMA"、"下载这本到IMA"
- 提供 Z-Library 链接并要求上传到 IMA 知识库
- 搜索 Z-Library 书籍并指定 IMA 知识库

## 前置条件

### 1. Python 依赖
```bash
pip install requests cos-python-sdk-v5
```

### 2. Z-Library 登录
- 会话文件: `~/.zlibrary/session.json`
- 如果不存在，提示用户需要先登录 Z-Library
- 登录方式: 用浏览器登录 Z-Library 后，导出 cookie 中的 `remix_userid` 和 `remix_userkey`，存入 session.json

### 3. IMA API 凭证
- 已内置默认 Client ID 和 API Key
- 存储位置: 代码内硬编码（脚本自带）
- 上传目标: IMA 知识库（通过名称模糊匹配）

### 4. 下载目录
- 默认: `D:/zlib_downloads`（Windows）
- 自动创建

## 脚本位置

```
d:\WorkBuddy\zlib-automation\zlib_api_to_ima.py
```

## 使用方法

AI 应该直接用 `execute_command` 运行脚本，Python 解释器路径：
```
C:\Users\Administrator\.workbuddy\binaries\python\envs\default\Scripts\python.exe
```

### 场景 1: 按关键词搜索 + 下载 + 上传 IMA

用户说: "帮我搜一本关于 python basics 的书，上传到IMA的测试知识库"

```bash
python d:\WorkBuddy\zlib-automation\zlib_api_to_ima.py --search "python basics" --kb "测试"
```

参数说明:
- `--search "关键词"`: 搜索书籍
- `--kb "知识库名"`: IMA 知识库（模糊匹配，可选，默认第一个）
- `--ext pdf epub`: 限定文件格式（可选）
- `--limit 10`: 搜索结果数量（可选，默认 5）
- `--index 0`: 选择第几本（从 0 开始，可选，默认 0）

### 场景 2: 通过 Z-Library URL 下载 + 上传

用户说: "把这本书 https://z-lib.is/book/17507364 上传到 IMA"

```bash
python d:\WorkBuddy\zlib-automation\zlib_api_to_ima.py --url "https://z-lib.is/book/17507364" --kb "知识库名"
```

### 场景 3: 通过书籍 ID 下载 + 上传

```bash
python d:\WorkBuddy\zlib-automation\zlib_api_to_ima.py --id 17507364 --kb "知识库名"
```

### 场景 4: 仅下载不上传

```bash
python d:\WorkBuddy\zlib-automation\zlib_api_to_ima.py --search "python" --download-only
```

## AI 操作指南

1. 用户提到 Z-Library + IMA 时，提取关键词/URL/ID
2. 如果用户提到知识库名，用 `--kb "名称"`
3. 如果用户没提知识库，问一下要上传到哪个知识库（或用 `--list-kb` 查看）
4. 直接运行对应命令，不需要额外配置
5. 检查输出中的 `[OK]` 或 `[FAIL]` 判断结果

## 故障排查

- **未找到登录会话**: 用户需要先登录 Z-Library，确保 `~/.zlibrary/session.json` 存在
- **登录失败**: session.json 中的 cookie 已过期，需要重新登录
- **下载额度用完**: Z-Library 每日有下载限制
- **知识库未找到**: 用 `--list-kb`（quark_to_ima.py）查看可用知识库，或检查名称拼写
- **上传失败**: 检查文件大小是否超过 200MB（PDF）或 10MB（TXT/MD/CSV）

## 注意事项

- 脚本内引用了 `upload_to_ima.py` 作为子进程，该文件在同一目录下
- PowerShell 可能吞掉 Python 输出，如果看不到输出，改用日志重定向方式
- IMA API 响应格式: `{"code": 0, "data": {...}}`，数据嵌套在 `data` 字段下
