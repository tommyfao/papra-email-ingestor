# Papra IMAP Ingestor

## Overview
The Papra IMAP Ingestor is a Python application designed to connect to an IMAP server, download new emails, convert them to PDF format, and integrate with the Papra document archiver. This project provides a robust solution for managing email attachments and archiving documents efficiently.

## Features
- Connects to an IMAP server to fetch new emails.
- Processes emails to filter and extract attachments.
- Converts emails and attachments to PDF format.
- Integrates with the Papra document archiver for document management.
- Configurable settings for IMAP connection, attachment handling, and download frequency.

## Project Structure
```
papra-imap-ingestor
├── src
│   ├── main.py               # Entry point of the application
│   ├── imap_client.py        # Handles IMAP server connections
│   ├── email_processor.py     # Processes downloaded emails
│   ├── pdf_converter.py       # Converts emails to PDF
│   ├── papra_client.py        # Interacts with the Papra archiver
│   └── config
│       └── settings.py       # Configuration settings
├── requirements.txt          # Project dependencies
├── Dockerfile                # Docker image instructions
├── docker-compose.yml        # Docker Compose configuration
├── .env.example              # Example environment variables
└── README.md                 # Project documentation
```

## Setup Instructions
1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd papra-imap-ingestor
   ```

2. **Create a virtual environment (optional but recommended):**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Copy the `.env.example` to `.env` and fill in the required values for your IMAP server and other settings.

5. **Run the application:**
   You can run the application directly or use Docker:
   - **Directly:**
     ```
     python src/main.py
     ```
   - **Using Docker:**
     ```
     docker-compose up
     ```

## Configuration
The application settings can be configured in the `src/config/settings.py` file. Key settings include:
- IMAP server details (host, port, username, password)
- Download frequency (how often to check for new emails)
- Attachment handling options (whether to download attachments)

## Usage
Once configured, the application will connect to the specified IMAP server, download new emails at the defined frequency, process them, and convert them to PDF format. The PDFs will be stored in the mounted folder specified in the Docker Compose configuration.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.