import os

class Settings:
    def __init__(self):
        self.imap_server = os.environ.get('IMAP_SERVER')
        self.imap_port = int(os.environ.get('IMAP_PORT', 993))
        self.imap_user = os.environ.get('IMAP_USER')
        self.imap_password = os.environ.get('IMAP_PASSWORD')
        self.download_frequency = int(os.environ.get('DOWNLOAD_FREQUENCY', 60))  # in seconds
        self.attachment_folder = os.environ.get('ATTACHMENT_FOLDER', './attachments')
        self.pdf_folder = os.environ.get('PDF_FOLDER', './pdfs')
        self.allowed_attachment_types = os.environ.get('ALLOWED_ATTACHMENT_TYPES', 'pdf,docx,xlsx').split(',')
        self.max_emails_to_download = int(os.environ.get('MAX_EMAILS_TO_DOWNLOAD', 10))