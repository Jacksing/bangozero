# encoding: utf8
# pylint: skip-file

import json
from email.header import decode_header
from email.mime.base import MIMEBase

from vendor import *
from utils import logif, logifelse, log

from constrants.mail_words import \
    TG_CONTENT_MAIN_TYPE, TG_CONTENT_SUB_TYPE, TG_FILENAME

try:
    from private import ACCOUNTS
except ImportError:
    account = {}


def start(account='163'):
    wa = ACCOUNTS[account]
    conn = connect(wa['pop'], wa['username'], wa['password'])
    # messages = get_all_mimes(conn)
    # conn.quit()

    # mail = get_message_from_mime(messages[-1])
    # analyze_mail(mail)

    mail = get_message_from_mime(conn.retr(conn.stat()[0]))

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
        mime = MIMEBase(TG_CONTENT_MAIN_TYPE, TG_CONTENT_SUB_TYPE)
        if mail.get_content_type() == mime.get_content_type() and mail.get_filename() == TG_FILENAME:
            return mail.get_payload(decode=mail['Content-Transfer-Encoding'])
    return None


if __name__ == '__main__':
    start('163')
