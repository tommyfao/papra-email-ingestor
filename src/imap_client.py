import imaplib

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
            emails.append(msg_data[0][1])
        return emails

    def disconnect(self):
        if self.connection:
            self.connection.logout()