import time
import logging
import shutil
import os
from config.settings import Settings
from imap_client import ImapClient
from email_processor import EmailProcessor
from pdf_converter import PdfConverter
from papra_client import PapraClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Load settings from environment variables
    settings = Settings()
    
    # Ensure ingestor directory exists
    ingestor_folder = '/ingestor'
    os.makedirs(ingestor_folder, exist_ok=True)
    
    imap_client = ImapClient(
        settings.IMAP_SERVER,
        settings.IMAP_USER,
        settings.IMAP_PASSWORD,
        settings.IMAP_PORT
    )
    email_processor = EmailProcessor()
    pdf_converter = PdfConverter()

    logger.info(f"Starting IMAP ingestor, checking every {settings.DOWNLOAD_FREQUENCY} minutes")

    while True:
        try:
            # Connect to the IMAP server and fetch new emails
            imap_client.connect()
            emails = imap_client.fetch_new_emails()
            
            logger.info(f"Found {len(emails)} new emails")

            for email in emails:
                # Process the email
                processed_email = email_processor.process(email)

                # Convert email to PDF if needed
                if processed_email.should_convert_to_pdf:
                    pdf_file = pdf_converter.convert(processed_email)
                    
                    # Move PDF to ingestor folder
                    if pdf_file and os.path.exists(pdf_file):
                        pdf_filename = os.path.basename(pdf_file)
                        destination_path = os.path.join(ingestor_folder, pdf_filename)
                        shutil.move(pdf_file, destination_path)
                        logger.info(f"Moved PDF to ingestor folder: {destination_path}")

            # Disconnect from the IMAP server
            imap_client.disconnect()
            
            logger.info(f"Processed {len(emails)} emails successfully")

        except Exception as e:
            logger.error(f"Error processing emails: {e}")

        # Wait for the specified download frequency before checking for new emails again
        time.sleep(settings.DOWNLOAD_FREQUENCY * 60)  # Convert minutes to seconds

if __name__ == "__main__":
    main()