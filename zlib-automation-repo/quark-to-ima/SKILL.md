# quark-to-ima

一键从夸克网盘下载文件并上传到腾讯 IMA 知识库。纯 API 方案，无需浏览器。

## 触发条件

当用户提到以下意图时自动触发：
- 夸克网盘 / quark 下载文件并上传到 IMA
- "把夸克分享链接传到IMA"、"这个链接上传到IMA"
- 提供夸克网盘分享链接（pan.quark.cn/s/xxx）并要求上传
- "从夸克下载XX上传到IMA"
- 上传本地文件到 IMA

## 前置条件

### 1. Python 依赖
```bash
pip install quarkpan cos-python-sdk-v5 requests
```

### 2. 夸克网盘登录
- Cookie 文件: `~/.config/quark/cookie.json`
- 如果不存在，运行: `python quark_to_ima.py --login` 扫码登录
- 登录后 cookie 自动保存，后续无需重复登录

### 3. IMA API 凭证
- 已内置默认 Client ID 和 API Key（代码内硬编码）
- 上传目标: IMA 知识库（通过名称模糊匹配）

### 4. 下载目录
- 默认: `D:/zlib_downloads`（Windows）

## 脚本位置

```
d:\WorkBuddy\zlib-automation\quark_to_ima.py
```

## 使用方法

Python 解释器路径:
```
C:\Users\Administrator\.workbuddy\binaries\python\envs\default\Scripts\python.exe
```

### 场景 1: 夸克分享链接 → 下载 → 上传 IMA

用户说: "把这个夸克链接上传到 IMA: https://pan.quark.cn/s/xxx 提取码 abc，知识库叫测试"

```bash
python d:\WorkBuddy\zlib-automation\quark_to_ima.py --url "https://pan.quark.cn/s/xxx" --pwd "abc" --kb "测试"
```

参数说明:
- `--url "分享链接"`: 夸克网盘分享链接（pan.quark.cn/s/xxx）
- `--pwd "提取码"`: 分享提取码（可选，无提取码可省略）
- `--kb "知识库名"`: IMA 知识库（模糊匹配，可选，默认第一个）
- `--download-only`: 仅下载不上传 IMA

### 场景 2: 搜索夸克网盘文件 → 下载 → 上传

用户说: "在夸克网盘搜机器学习相关的文件，上传到IMA"

```bash
python d:\WorkBuddy\zlib-automation\quark_to_ima.py --search "机器学习" --kb "AI知识"
```

### 场景 3: 上传本地文件到 IMA

用户说: "把 D:/books/test.pdf 上传到 IMA 测试知识库"

```bash
python d:\WorkBuddy\zlib-automation\quark_to_ima.py --file "D:/books/test.pdf" --kb "测试"
```

### 场景 4: 仅下载（不上传 IMA）

```bash
python d:\WorkBuddy\zlib-automation\quark_to_ima.py --url "https://pan.quark.cn/s/xxx" --pwd "abc" --download-only
```

### 场景 5: 查看 IMA 知识库列表

```bash
python d:\WorkBuddy\zlib-automation\quark_to_ima.py --list-kb
```

### 场景 6: 夸克网盘扫码登录

```bash
python d:\WorkBuddy\zlib-automation\quark_to_ima.py --login
```

## AI 操作指南

1. 用户提到夸克网盘链接时，提取 URL 和提取码
2. 如果用户提到知识库名，用 `--kb "名称"`；如果没提，先问或用 `--list-kb` 查看
3. 直接运行命令，不需要额外配置
4. 如果脚本提示 Cookie 过期，运行 `--login` 让用户扫码
5. 自己分享给自己的链接无法转存，但可以直接下载（脚本已处理此情况）
6. 检查输出中的 `[OK]` 或 `[FAIL]` 判断结果

## IMA 支持的文件格式

| 类型 | 格式 | 大小限制 |
|------|------|----------|
| 文档 | PDF, DOC, DOCX, PPT, PPTX | 200MB |
| 表格 | XLS, XLSX, CSV | 10MB |
| 文本 | MD, TXT | 10MB |
| 图片 | PNG, JPG, JPEG, WEBP | - |

## 故障排查

- **Cookie 过期/无效**: 运行 `--login` 重新扫码
- **转存失败（自己的分享）**: 正常现象，脚本会自动尝试直接下载
- **知识库未找到**: 用 `--list-kb` 查看可用知识库，检查名称
- **文件格式不支持**: 检查文件扩展名是否在支持列表中
- **上传大小超限**: PDF 最大 200MB，TXT/MD/CSV 最大 10MB
- **IMA 返回 "创建媒体失败"**: 检查 IMA API 凭证和网络连接

## 注意事项

- quarkpan SDK 的 `is_logged_in()` 有 bug，脚本用 `get_storage_info()` 替代验证
- quarkpan SDK 的 `ShareService` 构造函数不兼容，用 `client.shares` 代替
- IMA API 响应数据嵌套在 `data` 字段下: `resp.get("data", resp)`
- PowerShell 可能吞掉 Python 输出，如遇此问题改用日志重定向
