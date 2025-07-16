import email
import os
import mimetypes
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ProcessedEmail:
    def __init__(self, subject, sender, date, body, attachments=None):
        self.subject = subject
        self.sender = sender
        self.date = date
        self.body = body
        self.attachments = attachments or []
        self.should_convert_to_pdf = True  # Default behavior
        self.saved_attachments = []  # Paths to saved attachments

class EmailProcessor:
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the EmailProcessor with configuration options.
        
        Args:
            config: Dictionary containing filtering and processing configuration
        """
        self.config = config or {}
        self.attachment_dir = self.config.get('attachment_dir', './attachments')
        self.ingestor_dir = '/ingestor'
        self.date_filter_days = self.config.get('date_filter_days', 30)
        self.allowed_senders = self.config.get('allowed_senders', [])
        self.blocked_senders = self.config.get('blocked_senders', [])
        self.pdf_conversion_criteria = self.config.get('pdf_conversion_criteria', {
            'convert_all': False,
            'convert_by_sender': [],
            'convert_by_subject_keywords': [],
            'max_email_size_mb': 10
        })
        
        # Ensure directories exist
        os.makedirs(self.attachment_dir, exist_ok=True)
        os.makedirs(self.ingestor_dir, exist_ok=True)

    def process(self, email: Dict[str, Any]) -> ProcessedEmail:
        """Process an email and extract relevant information"""
        try:
            subject = email.get('subject', '')
            sender = email.get('sender', '')
            date = email.get('date', '')
            body = email.get('body', '')
            attachments = email.get('attachments', [])
            
            # Process and save attachments
            saved_attachments = self._save_attachments(attachments, subject)
            
            # Create processed email object
            processed_email = ProcessedEmail(
                subject=subject,
                sender=sender,
                date=date,
                body=body,
                attachments=attachments
            )
            processed_email.saved_attachments = saved_attachments
            
            logger.info(f"Processed email from {sender} with subject: {subject}, {len(saved_attachments)} attachments saved")
            return processed_email
            
        except Exception as e:
            logger.error(f"Error processing email: {e}")
            raise

    def _save_attachments(self, attachments: List[Dict], email_subject: str) -> List[str]:
        """Save email attachments to the ingestor folder"""
        saved_files = []
        
        for i, attachment in enumerate(attachments):
            try:
                filename = attachment.get('filename', f'attachment_{i}')
                data = attachment.get('data')
                
                if not data:
                    continue
                
                # Sanitize filename
                safe_filename = self._sanitize_filename(filename)
                
                # Save to ingestor folder
                file_path = os.path.join(self.ingestor_dir, safe_filename)
                
                # Handle duplicate filenames
                counter = 1
                original_path = file_path
                while os.path.exists(file_path):
                    name, ext = os.path.splitext(original_path)
                    file_path = f"{name}_{counter}{ext}"
                    counter += 1
                
                # Write attachment data to file
                with open(file_path, 'wb') as f:
                    f.write(data)
                
                saved_files.append(file_path)
                logger.info(f"Saved attachment: {file_path}")
                
            except Exception as e:
                logger.error(f"Failed to save attachment {filename}: {e}")
        
        return saved_files

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to be safe for filesystem"""
        # Remove any characters that are not alphanumeric, dots, or underscores
        safe_chars = []
        for c in filename:
            if c.isalnum() or c in ('_', '.', '-'):
                safe_chars.append(c)
            else:
                safe_chars.append('_')
        
        return ''.join(safe_chars)[:100]  # Limit length to 100 chars