# pylint: skip-file

import json
from email.header import decode_header

from mail_vendor import *
from utils import logif, logifelse, log

try:
    from private import ACCOUNTS
except ImportError:
    account = {}


TELEGRAPH_FILENAME = 'telegraph'
TELEGRAPH_CONTENT_TYPE = 'application/octet-stream'


def start(account='163'):
    conn = connect(**ACCOUNTS[account])
    messages = get_all_mines(conn)
    conn.quit()

    mail = get_message_from_mine(messages[-1])
    # analyze_mail(mail)

    telegraph_obj = get_telegraph_obj_from_mail(mail)
    if telegraph_obj:
        print(json.dumps(telegraph_obj, indent=2))

    print('finish')


def analyze_mail(mail):
    subject, encode_str = decode_header(mail['subject'])[0]
    print(subject.decode(encode_str))  # py3: str(subject, encode_str)

    show_message(mail)


def show_message(mail, isdeep=False):
    '''
    List all human readable message content.
    '''
    if mail.is_multipart():
        for part in mail.get_payload():
            logif(isdeep==False, 'payload', 2, sep_length=10)
            logif(isdeep==True, 'sub-payload', sep_length=10, indent=4)
            show_message(part, True)
    else:
        charset = mail.get_content_charset()
        if charset == None:
            print('---   %s   ---' % mail['Content-Type'])
            print(mail.get_payload())
        else:
            try:
                print('---   %s   ---' % mail['Content-Type'])
                print(mail.get_payload(decode=mail['Content-Transfer-Encoding']).decode(charset))
            except UnicodeDecodeError:
                print(mail)


def get_telegraph_obj_from_mail(mail):
    """
    Get telegraph object form mail.
    If there is no telegraph information in, return `None`
    """
    try:
        telegraph = get_telegraph_from_mail(mail)
        if telegraph == None:
            return None
        return json.loads(telegraph.decode('utf-8'))
    except Exception as ex:
        log(ex.message)
        return None


def get_telegraph_from_mail(mail):
    """
    Search telegraph information from mail.
    Return a bytearray object.
    """
    if mail.is_multipart():
        for part in mail.get_payload():
            telegraph = get_telegraph_from_mail(part)
            if telegraph != None:
                return telegraph
    else:
        if mail.get_content_type() == TELEGRAPH_CONTENT_TYPE and mail.get_filename() == TELEGRAPH_FILENAME:
            return mail.get_payload(decode=mail['Content-Transfer-Encoding'])
    return None


if __name__ == '__main__':
    start('163')

