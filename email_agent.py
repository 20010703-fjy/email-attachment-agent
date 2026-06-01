import imaplib
import email
from email.header import decode_header
import os
import json
from pathlib import Path
from pathvalidate import sanitize_filename
import re


class EmailAttachmentAgent:
    def __init__(self, config):
        self.email_address = config['EMAIL_ADDRESS']
        self.email_password = config['EMAIL_PASSWORD']
        self.imap_server = config['IMAP_SERVER']
        self.imap_port = int(config['IMAP_PORT'])
        self.attachments_dir = Path(config['ATTACHMENTS_DIR'])
        self.search_criteria = config['SEARCH_CRITERIA']
        self.categories = json.loads(config['CATEGORIES'].replace("'", '"'))
        self.mark_as_read = config['MARK_AS_READ'].lower() == 'true'
        
        self.mail = None
        self._init_directories()

    def _init_directories(self):
        self.attachments_dir.mkdir(parents=True, exist_ok=True)
        for category in self.categories.keys():
            (self.attachments_dir / category).mkdir(exist_ok=True)

    def connect(self):
        self.mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
        self.mail.login(self.email_address, self.email_password)

    def disconnect(self):
        if self.mail:
            self.mail.logout()

    def _decode_filename(self, filename):
        if not filename:
            return None
        
        decoded_parts = decode_header(filename)
        decoded_filename = []
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                if encoding:
                    try:
                        decoded_filename.append(part.decode(encoding))
                    except:
                        decoded_filename.append(part.decode('utf-8', errors='ignore'))
                else:
                    decoded_filename.append(part.decode('utf-8', errors='ignore'))
            else:
                decoded_filename.append(part)
        
        return ''.join(decoded_filename)

    def _get_category(self, filename):
        ext = Path(filename).suffix.lower().lstrip('.')
        for category, extensions in self.categories.items():
            if ext in extensions:
                return category
        return 'others'

    def _sanitize_filename(self, filename):
        filename = sanitize_filename(filename)
        base = Path(filename).stem
        ext = Path(filename).suffix
        counter = 1
        while os.path.exists(os.path.join(self.attachments_dir, self._get_category(filename), filename)):
            filename = f"{base}_{counter}{ext}"
            counter += 1
        return filename

    def download_attachments(self):
        self.mail.select('INBOX')
        result, data = self.mail.search(None, self.search_criteria)
        
        if result != 'OK':
            print('没有找到邮件')
            return []

        email_ids = data[0].split()
        downloaded_files = []

        for email_id in email_ids:
            result, msg_data = self.mail.fetch(email_id, '(RFC822)')
            if result != 'OK':
                continue

            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject = self._decode_filename(msg['Subject'])
            print(f'处理邮件: {subject}')

            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue

                filename = part.get_filename()
                if not filename:
                    continue

                filename = self._decode_filename(filename)
                category = self._get_category(filename)
                filename = self._sanitize_filename(filename)
                filepath = self.attachments_dir / category / filename

                with open(filepath, 'wb') as f:
                    f.write(part.get_payload(decode=True))
                
                downloaded_files.append({
                    'filename': filename,
                    'category': category,
                    'path': str(filepath),
                    'email_subject': subject
                })
                print(f'下载附件: {filename} -> {category}/')

            if self.mark_as_read:
                self.mail.store(email_id, '+FLAGS', '\\Seen')

        return downloaded_files

    def run(self):
        try:
            print('正在连接邮箱服务器...')
            self.connect()
            print('连接成功！')
            print('开始下载附件...')
            downloaded = self.download_attachments()
            
            if downloaded:
                print(f'\n下载完成！共下载 {len(downloaded)} 个附件:')
                for file in downloaded:
                    print(f'  - [{file["category"]}] {file["filename"]} (来自: {file["email_subject"]})')
            else:
                print('没有找到新的附件')
                
        except Exception as e:
            print(f'发生错误: {str(e)}')
        finally:
            self.disconnect()
            print('已断开连接')
