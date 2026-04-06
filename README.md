zlib-自动化
这是三个技能，一个是z站的链接，然后由agent直接帮你上传到IMA和notebooklm；另一个是夸克网盘的下载链接，可以直接上传到IMA（前提是格式支持）
我做这个主要是为了方便懒人，还能让CLAW快速下载资料，然后让它学习，把IMA和notebooklm的上传与整理工作交给agent来做，省得自己手动操作了。

WorkBuddy / OpenClaw 用于书籍自动化的技能——只需一条命令，即可搜索、下载并将内容推送至您的知识库。

一组人工智能代理技能，可将Z-Library和夸克网盘与热门的知识管理工具相连接。

技能

zlib-to-ima 从Z-Library搜索并下载图书 → 上传至腾讯IMA知识库
zlib-to-notebooklm 从Z-Library搜索并下载图书 → 上传至Google NotebookLM
从夸克网盘下载文件 → 上传至腾讯IMA知识库

每项技能都存放在各自的子目录中。请将该文件夹复制到您的WorkBuddy技能目录：

~/.workbuddy/skills/<技能名称>/
然后重新加载您的代理会话——该技能将自动检测。

zlib-to-ima
一键从 Z-Library 搜索/下载书籍，自动上传到腾讯 IMA 知识库。

依赖

pip install requests cos-python-sdk-v5 playwright
前置配置

Z-Library 会话: ~/.zlibrary/session.json（含 remix_userid + remix_userkey）
IMA API 凭证: ~/.config/ima/client_id 和 ~/.config/ima/api_key
在 ima.qq.com/agent-interface 申请
示例

# 搜索 + 下载 + 上传
python zlib_api_to_ima.py --search "python basics" --kb "技术书库"

# 通过 URL 上传
python zlib_api_to_ima.py --url "https://z-lib.is/book/17507364" --kb "知识库名"

# 仅下载
python zlib_api_to_ima.py --search "机器学习" --download-only
zlib-to-notebooklm
一键从 Z-Library 搜索/下载书籍，自动上传到 Google NotebookLM。

依赖

pip install requests playwright
playwright install chromium
前置配置

Z-Library 会话: ~/.zlibrary/session.json
NotebookLM 登录态: ~/.notebooklm/storage_state.json（首次运行会弹浏览器让你登录）
示例

# 搜索 + 上传到 NotebookLM
python zlib_api_to_notebooklm.py --search "deep learning" --nb "AI Reading"

# 通过 URL 上传
python zlib_api_to_notebooklm.py --url "https://z-lib.is/book/17507364"
quark-to-ima
一键从夸克网盘下载文件，自动上传到腾讯 IMA 知识库。

依赖

pip install quarkpan cos-python-sdk-v5 requests
前置配置

夸克网盘登录: 运行 python quark_to_ima.py --login 扫码登录，自动保存到 ~/.config/quark/cookie.json
IMA API 凭证: ~/.config/ima/client_id 和 ~/.config/ima/api_key
IMA 支持的文件格式

类型	格式	大小限制
文档	PDF, DOC, DOCX, PPT, PPTX	200MB
表格	XLS, XLSX, CSV	10MB
文本	MD, TXT	10MB
图片	PNG, JPG, JPEG, WEBP	—
示例

# 夸克分享链接 → IMA
python quark_to_ima.py --url "https://pan.quark.cn/s/xxx" --pwd "提取码" --kb "知识库名"

# 上传本地文件
python quark_to_ima.py --file "D:/books/book.pdf" --kb "技术书库"

# 查看 IMA 知识库列表
python quark_to_ima.py --list-kb

# 扫码登录夸克
python quark_to_ima.py --login
IMA API 凭证配置
所有用到 IMA 的 skill 都需要配置凭证：

访问 ima.qq.com/agent-interface 申请 OpenAPI 权限
获取 Client ID 和 API Key
保存到本地：
# Linux / macOS
mkdir -p ~/.config/ima
echo "YOUR_CLIENT_ID" > ~/.config/ima/client_id
echo "YOUR_API_KEY"   > ~/.config/ima/api_key

# Windows PowerShell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.config\ima"
"YOUR_CLIENT_ID" | Out-File "$env:USERPROFILE\.config\ima\client_id" -Encoding UTF8
"YOUR_API_KEY"   | Out-File "$env:USERPROFILE\.config\ima\api_key"   -Encoding UTF8
Python 解释器
推荐使用 WorkBuddy 内置 Python 环境（已预装所有依赖）：

C:\Users\<你的用户名>\.workbuddy\binaries\python\envs\default\Scripts\python.exe
License
MIT
