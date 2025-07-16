import os

class Settings:
    def __init__(self):
        self.IMAP_SERVER = os.environ.get('IMAP_SERVER')
        self.IMAP_PORT = int(os.environ.get('IMAP_PORT', 993))
        self.IMAP_USER = os.environ.get('IMAP_USER')
        self.IMAP_PASSWORD = os.environ.get('IMAP_PASSWORD')
        self.DOWNLOAD_FREQUENCY = int(os.environ.get('DOWNLOAD_FREQUENCY', 60))  # in minutes