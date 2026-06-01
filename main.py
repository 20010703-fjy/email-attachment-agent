import os
from dotenv import load_dotenv
from email_agent import EmailAttachmentAgent


def main():
    load_dotenv()
    
    config = {
        'EMAIL_ADDRESS': os.getenv('EMAIL_ADDRESS'),
        'EMAIL_PASSWORD': os.getenv('EMAIL_PASSWORD'),
        'IMAP_SERVER': os.getenv('IMAP_SERVER', 'imap.163.com'),
        'IMAP_PORT': os.getenv('IMAP_PORT', '993'),
        'ATTACHMENTS_DIR': os.getenv('ATTACHMENTS_DIR', './attachments'),
        'SEARCH_CRITERIA': os.getenv('SEARCH_CRITERIA', 'UNSEEN'),
        'CATEGORIES': os.getenv('CATEGORIES', '{"documents": ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt"], "images": ["jpg", "jpeg", "png", "gif", "bmp", "svg"], "archives": ["zip", "rar", "7z", "tar", "gz"], "videos": ["mp4", "avi", "mov", "mkv"], "audios": ["mp3", "wav", "flac", "aac"], "others": []}'),
        'MARK_AS_READ': os.getenv('MARK_AS_READ', 'true')
    }
    
    if not config['EMAIL_ADDRESS'] or not config['EMAIL_PASSWORD']:
        print('错误: 请在 .env 文件中配置邮箱地址和授权码')
        return
    
    agent = EmailAttachmentAgent(config)
    agent.run()


if __name__ == '__main__':
    main()
