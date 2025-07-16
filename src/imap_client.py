import imaplib
import email
from email.header import decode_header

class ImapClient:
    def __init__(self, host, username, password, port=993):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.connection = None

    def connect(self):
        if self.port == 993:
            self.connection = imaplib.IMAP4_SSL(self.host, self.port)
        else:
            self.connection = imaplib.IMAP4(self.host, self.port)
        self.connection.login(self.username, self.password)

    def fetch_new_emails(self, folder='INBOX'):
        self.connection.select(folder)
        status, messages = self.connection.search(None, 'UNSEEN')
        email_ids = messages[0].split()
        emails = []
        for email_id in email_ids:
            status, msg_data = self.connection.fetch(email_id, '(RFC822)')
            raw_email = msg_data[0][1]
            parsed_email = email.message_from_bytes(raw_email)
            emails.append(self.parse_email(parsed_email))
        return emails

    def parse_email(self, msg):
        """Parse email message and extract key information"""
        subject = self.decode_header_value(msg.get("Subject", ""))
        sender = msg.get("From", "")
        date = msg.get("Date", "")
        
        # Extract body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    break
        else:
            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        
        return {
            'subject': subject,
            'sender': sender,
            'date': date,
            'body': body
        }

    def decode_header_value(self, value):
        """Decode email header values"""
        if value:
            decoded_value, encoding = decode_header(value)[0]
            if isinstance(decoded_value, bytes):
                return decoded_value.decode(encoding or 'utf-8', errors='ignore')
            return decoded_value
        return ""

    def disconnect(self):
        if self.connection:
            self.connection.logout()