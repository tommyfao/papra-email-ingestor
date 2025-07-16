import os

class Settings:
    def __init__(self):
        self.IMAP_SERVER = os.environ.get('IMAP_SERVER')
        self.IMAP_PORT = int(os.environ.get('IMAP_PORT', 993))
        self.IMAP_USER = os.environ.get('IMAP_USER')
        self.IMAP_PASSWORD = os.environ.get('IMAP_PASSWORD')
        self.DOWNLOAD_FREQUENCY = int(os.environ.get('DOWNLOAD_FREQUENCY', 60))  # in seconds
        self.ATTACHMENT_FOLDER = os.environ.get('ATTACHMENT_FOLDER', './attachments')
        self.PDF_FOLDER = os.environ.get('PDF_FOLDER', './pdfs')
        self.ALLOWED_ATTACHMENT_TYPES = os.environ.get('ALLOWED_ATTACHMENT_TYPES', 'pdf,docx,xlsx').split(',')
        self.MAX_EMAILS_TO_DOWNLOAD = int(os.environ.get('MAX_EMAILS_TO_DOWNLOAD', 10))