class PdfConverter:
    def __init__(self):
        pass

    def format_email_content(self, email):
        # Format the email content for PDF conversion
        formatted_content = f"Subject: {email['subject']}\n\n{email['body']}"
        return formatted_content

    def save_pdf(self, formatted_content, filename):
        from fpdf import FPDF

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, formatted_content)
        pdf.output(filename)

    def convert_email_to_pdf(self, email, output_folder):
        formatted_content = self.format_email_content(email)
        filename = f"{output_folder}/{email['subject']}.pdf"
        self.save_pdf(formatted_content, filename)