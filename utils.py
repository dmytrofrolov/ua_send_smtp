import random
from os import listdir
from os.path import isfile, join
from contextlib import contextmanager
from smtplib import SMTPResponseException, SMTPServerDisconnected


def get_emails_list():
    with open('static/emails.txt', 'r') as emails_file:
        return emails_file.readlines()
    return ['']

def get_shuffled_headers():
    with open('static/headers.txt', 'r') as emails_file:
        return emails_file.readlines()
    return ['']

def get_shuffled_texts():
    path = 'static/letters'
    files = [f for f in listdir(path) if isfile(join(path, f))]
    file_contents = []
    for file in files:
        with open(f'{path}/{file}', 'r') as file_with_letter:
            file_contents += [file_with_letter.read()]
    random.shuffle(file_contents)
    return file_contents


@contextmanager
def quitting_smtp_cm(smtp):
    try:
        yield smtp
    finally:
        try:
            code, message = smtp.docmd("QUIT")
            if code != 221:
                raise SMTPResponseException(code, message)
        except SMTPServerDisconnected:
            pass
        finally:
            smtp.close()
