import os
import smtplib
import random
import time

from email.message import EmailMessage
from utils import get_emails_list, get_shuffled_headers, get_shuffled_texts, quitting_smtp_cm

sender = os.environ.get('FROM')
smtp_host = os.environ.get('HOST')
USER = os.environ.get('USER')
PASSWORD = os.environ.get('PASSWORD')
EMAILS_LIMIT = int(os.environ.get('EMAILS_LIMIT'))
SLEEP_TIME_IN_SECONDS = 0.500

def send_emails():
    emails_list = get_emails_list()
    shuffled_headers = get_shuffled_headers()
    shuffled_texts = get_shuffled_texts()

    with quitting_smtp_cm(smtplib.SMTP_SSL(smtp_host)) as smtp_sender:
        smtp_sender.login(USER, PASSWORD)

        for (email, limit_index) in zip(emails_list, range(EMAILS_LIMIT)):
            email = email.strip()

            msg = EmailMessage()
            msg.set_content(random.choice(shuffled_texts).strip())

            msg['Subject'] = random.choice(shuffled_headers).strip()
            msg['From'] = f'Stop The War <{sender}>'
            msg['To'] = email

            try:
                receivers = [email]
                senderrs = smtp_sender.sendmail(sender, receivers, msg.as_string())
                print(f"Successfully sent email to {email}")
            except smtplib.SMTPException:
                print(f"Error: unable to send email to {email}")

            time.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ == '__main__':
    send_emails()
