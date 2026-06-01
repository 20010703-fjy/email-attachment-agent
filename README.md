# 163邮箱附件自动下载Agent

一个自动从163邮箱下载附件并按文件类型分类的Python工具。

## 功能特性

- 自动连接163邮箱IMAP服务器
- 下载指定邮件（默认未读邮件）的附件
- 按文件类型自动分类保存
- 支持自定义分类规则
- 自动标记已下载的邮件为已读
- 文件名自动去重

## 项目结构

```
email-attachment-agent/
├── main.py              # 主程序入口
├── email_agent.py       # 核心功能模块
├── config.example.env   # 配置文件示例
├── requirements.txt     # Python依赖
├── run.sh               # Linux/Mac启动脚本
├── run.bat              # Windows启动脚本
└── README.md            # 使用说明
```

## 快速开始

### 1. 获取163邮箱授权码

1. 登录163邮箱网页版
2. 进入「设置」→「POP3/SMTP/IMAP」
3. 开启IMAP服务
4. 获取授权码（不是邮箱登录密码）

### 2. 配置

复制配置示例文件：

```bash
cp config.example.env .env
```

编辑 `.env` 文件，填入你的邮箱信息：

```env
EMAIL_ADDRESS=your_email@163.com
EMAIL_PASSWORD=your_authorization_code
```

### 3. 运行

#### Linux/Mac:

```bash
./run.sh
```

#### Windows:

```cmd
run.bat
```

#### 手动运行:

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate.bat

# 安装依赖
pip install -r requirements.txt

# 运行程序
python main.py
```

## 配置说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| EMAIL_ADDRESS | 163邮箱地址 | - |
| EMAIL_PASSWORD | 163邮箱授权码 | - |
| IMAP_SERVER | IMAP服务器地址 | imap.163.com |
| IMAP_PORT | IMAP端口 | 993 |
| ATTACHMENTS_DIR | 附件保存路径 | ./attachments |
| SEARCH_CRITERIA | 邮件搜索条件 | UNSEEN |
| CATEGORIES | 分类规则（JSON格式） | 见下文 |
| MARK_AS_READ | 是否标记为已读 | true |

### 邮件搜索条件

- `UNSEEN` - 未读邮件
- `SEEN` - 已读邮件
- `ALL` - 所有邮件
- `RECENT` - 最近邮件

### 分类规则

默认分类：

```json
{
    "documents": ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt"],
    "images": ["jpg", "jpeg", "png", "gif", "bmp", "svg"],
    "archives": ["zip", "rar", "7z", "tar", "gz"],
    "videos": ["mp4", "avi", "mov", "mkv"],
    "audios": ["mp3", "wav", "flac", "aac"],
    "others": []
}
```

## 定时运行

### Linux/Mac (使用 crontab)

```bash
# 编辑 crontab
crontab -e

# 添加定时任务（例如每小时运行一次）
0 * * * * cd /path/to/project && ./run.sh >> /var/log/email-agent.log 2>&1
```

### Windows (使用任务计划程序)

1. 打开「任务计划程序」
2. 创建基本任务
3. 设置触发器（例如每天/每小时）
4. 操作选择「启动程序」
5. 程序选择 `run.bat`
6. 起始于填写项目目录路径

## 部署给他人使用

### 方式一：打包分发

1. 将整个项目文件夹打包
2. 告诉用户：
   - 复制 `config.example.env` 为 `.env`
   - 编辑 `.env` 填入自己的邮箱信息
   - 运行对应系统的启动脚本

### 方式二：Docker部署

创建 `Dockerfile`：

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

构建并运行：

```bash
docker build -t email-agent .
docker run --env-file .env email-agent
```

### 方式三：GitHub仓库

1. 将代码推送到GitHub（注意：不要提交 `.env` 文件）
2. 用户克隆仓库后按照快速开始步骤操作

## 注意事项

1. 确保163邮箱已开启IMAP服务
2. 使用授权码而非登录密码
3. 首次运行建议先测试少量邮件
4. 定期检查附件保存目录空间
5. 不要将 `.env` 文件提交到公开仓库

## 故障排除

### 连接失败

- 检查网络连接
- 确认IMAP服务已开启
- 验证授权码是否正确

### 附件下载失败

- 检查附件大小是否超出限制
- 确认磁盘空间充足
- 查看错误日志信息

## 许可证

MIT License
