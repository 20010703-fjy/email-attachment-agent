@echo off
REM 163邮箱附件下载器启动脚本 (Windows)

cd /d "%~dp0"

if not exist ".env" (
    echo 错误: 未找到 .env 文件，请先复制 config.example.env 为 .env 并配置
    pause
    exit /b 1
)

if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo 安装依赖...
pip install -r requirements.txt

echo 启动附件下载器...
python main.py

pause
