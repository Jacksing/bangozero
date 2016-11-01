# pylint: skip-file

from mail_vendor import *
import email

from utils import logif, logifelse

try:
    from private import ACCOUNTS
except ImportError:
    account = {}


def start(account='163'):
    conn = get_pop_conn(**ACCOUNTS[account])
    print_mail_statistics(conn)
    messages = get_all_messages(conn)

    mail = get_email_from_message(messages[6])
    analyze_mail(mail)

    print('finish')


def analyze_mail(mail):
    subject, encode_str = email.Header.decode_header(mail['subject'])[0]
    print(subject.decode(encode_str))  # py3: str(subject, encode_str)

    show_message(mail)


def show_message(mail, isdeep=False):
    if mail.is_multipart():
        for part in mail.get_payload():
            logif(isdeep==False, 'payload', 2, sep_length=10)
            logif(isdeep==True, 'sub-payload', sep_length=10, indent=4)
            show_message(part, True)
    else:
        content_type = mail.get_content_charset()
        if content_type == None:
            print('---   %s   ---' % mail['Content-Type'])
            print(mail.get_payload())
        else:
            try:
                print('---   %s   ---' % mail['Content-Type'])
                print(mail.get_payload(decode=mail['Content-Transfer-Encoding']).decode(content_type))
            except UnicodeDecodeError:
                print(mail)


if __name__ == '__main__':
    start()

