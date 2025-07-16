import os
import logging
from typing import Optional
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from email_processor import ProcessedEmail

logger = logging.getLogger(__name__)

class PdfConverter:
    def __init__(self, output_dir: str = './pdfs'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def convert(self, processed_email: ProcessedEmail) -> Optional[str]:
        """
        Convert a processed email to PDF format
        
        Args:
            processed_email: ProcessedEmail object to convert
            
        Returns:
            Path to the created PDF file, or None if conversion failed
        """
        try:
            # Create a safe filename from email subject
            safe_subject = self._sanitize_filename(processed_email.subject or "No Subject")
            pdf_filename = f"{safe_subject}.pdf"
            pdf_path = os.path.join(self.output_dir, pdf_filename)
            
            # Create PDF document
            doc = SimpleDocTemplate(pdf_path, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Add email content to PDF
            story.append(Paragraph(f"<b>Subject:</b> {processed_email.subject}", styles['Normal']))
            story.append(Spacer(1, 12))
            story.append(Paragraph(f"<b>From:</b> {processed_email.sender}", styles['Normal']))
            story.append(Spacer(1, 12))
            story.append(Paragraph(f"<b>Date:</b> {processed_email.date}", styles['Normal']))
            story.append(Spacer(1, 24))
            story.append(Paragraph("<b>Body:</b>", styles['Normal']))
            story.append(Spacer(1, 12))
            story.append(Paragraph(processed_email.body, styles['Normal']))
            
            # Build the PDF
            doc.build(story)
            
            logger.info(f"Created PDF: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            logger.error(f"Failed to convert email to PDF: {e}")
            return None

    def _sanitize_filename(self, subject: str) -> str:
        """
        Sanitize the email subject to create a safe filename
        
        Args:
            subject: Email subject
            
        Returns:
            Sanitized subject string
        """
        # Remove any characters that are not alphanumeric, spaces, or underscores
        return ''.join(c for c in subject if c.isalnum() or c in (' ', '_')).rstrip()[:50]