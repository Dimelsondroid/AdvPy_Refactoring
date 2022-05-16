import email
import smtplib
import imaplib

from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

class Mailer:
    GMAIL_SMTP = "smtp.gmail.com"
    GMAIL_IMAP = "imap.gmail.com"

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def send_message(self, message, subject, recipients):
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))

        send_message = smtplib.SMTP(self.GMAIL_SMTP, 587)
        # identify ourselves to smtp gmail client
        send_message.ehlo()
        # secure our email with tls encryption
        send_message.starttls()
        # re-identify ourselves as an encrypted connection
        send_message.ehlo()

        send_message.login(self.login, self.password)
        send_message.sendmail(self.login, recipients, msg.as_string())

        send_message.quit()
        return 'Mail sent'

    def receive_message(self, header):
        mail = imaplib.IMAP4_SSL(self.GMAIL_IMAP)
        mail.login(self.login, self.password)
        mail.list()
        mail.select("inbox")
        criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        mail.logout()
        return email_message


if __name__ == '__main__':
    # login = 'login@gmail.com'
    # password = 'qwerty'
    # subject = 'Subject'
    # recipients = ['vasya@email.com', 'petya@email.com']
    # message = 'Message'
    # header = None
    # mailer = Mailer(login, password)
    # mailer.receive_message(header)
    # mailer.send_message(message, subject, recipients)

    mailer = Mailer('login@gmail.com', 'qwerty')
    mailer.receive_message(None)
    mailer.send_message('Message', 'Subject', ['vasya@email.com', 'petya@email.com'])
