import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    IMAP_SERVER = os.getenv("IMAP_SERVER")
    IMAP_PORT = int(os.getenv("IMAP_PORT", 993))
    IMAP_USERNAME = os.getenv("IMAP_USERNAME")
    IMAP_PASSWORD = os.getenv("IMAP_PASSWORD")
    DOWNLOAD_FREQUENCY = int(os.getenv("DOWNLOAD_FREQUENCY", 60))  # in seconds
    ATTACHMENT_FOLDER = os.getenv("ATTACHMENT_FOLDER", "./attachments")
    PDF_FOLDER = os.getenv("PDF_FOLDER", "./pdfs")
    ALLOWED_ATTACHMENT_TYPES = os.getenv("ALLOWED_ATTACHMENT_TYPES", "pdf,docx,xlsx").split(",")
    MAX_EMAILS_TO_DOWNLOAD = int(os.getenv("MAX_EMAILS_TO_DOWNLOAD", 10))