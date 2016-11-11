# encoding: utf8
# pylint: skip-file

import json
import poplib
from email import message_from_string
from email.header import decode_header
from email.mime.base import MIMEBase

from django.conf import settings

from crypto import decrypt_json
from utils.logger import logif, logifelse, log


def connect(host, username, passwd):
    log("login with '%s' to '%s'" % (username, host))
    pop_conn = poplib.POP3(host)
    pop_conn.user(username)
    pop_conn.pass_(passwd)
    return pop_conn


def _get_all(pop_conn, as_message=True):
    """
    Get all mail content from the mail server.
    Return the format in message if 'as_message' is True,
    otherwise return the original mime format.
    """
    count, total_size = pop_conn.stat()
    if as_message:
        return [parse_message_from_mime(pop_conn.retr(i)) for i in range(1, count+1)]
    else:
        return [pop_conn.retr(i) for i in range(1, count+1)]


def get_all_mimes(pop_conn):
    """
    Get all mail content in the Mime format from mail server.
    """
    return _get_all(pop_conn, False)


def get_all_messages(pop_conn):
    """
    Get all mail content in the Message object format from mail server.
    """
    return _get_all(pop_conn)


def get_message(host, username, passwd, index=-1):
    """
    Get the specified mail message with the given arguments.
    The mail is specified by 'index'.
    If the mail box is empty or 'index' is not in range of
    the count of the mails, it will return None object.
    """
    conn = None
    try:
        conn = connect(host, username, passwd)
        count = conn.stat()[0]
        if count == 0:
            return None
        if index == -1:
            index = count
        if index > count:
            return None
        return parse_message_from_mime(conn.retr(count))
    except Exception as ex:
        log(ex.message)
        return None
    finally:
        if conn:
            conn.quit()


def parse_message_from_mime(mime):
    """
    Parse an orginal Mime format into a Message object model.
    """
    return message_from_string('\n'.join([line.decode('utf-8') for line in mime[1]]))


def get_headstring_from_message(message, item):
    """
    Get decoded head value of the specified item.
    """
    subject, encode_str = decode_header(message[item])[0]
    return encode_str and subject.decode(encode_str) or subject


def get_telegraph_obj_from_message(message):
    """
    Get telegraph object form message.
    If there is no telegraph information in, return `None`
    """
    if not message:
        return None
    try:
        telegraph = get_telegraph_from_message(message)
        if telegraph == None:
            return None
        if settings.ENCRYPT_TELEGRAPH:
            return decrypt_json(telegraph)
        else:
            return json.loads(telegraph.decode('utf-8'))
    except Exception as ex:
        log(ex.message)
        return None


def get_telegraph_from_message(message):
    """
    Search telegraph information from message.
    Return a bytearray object.
    """
    if message.is_multipart():
        for part in message.get_payload():
            telegraph = get_telegraph_from_message(part)
            if telegraph != None:
                return telegraph
    else:
        mime = MIMEBase(settings.TG_CONTENT_MAIN_TYPE, settings.TG_CONTENT_SUB_TYPE)
        if message.get_content_type() == mime.get_content_type() and message.get_filename() == settings.TG_FILENAME:
            return message.get_payload(decode=message['Content-Transfer-Encoding'])
    return None


def walk_message(message, isdeep=False, heads=['subject', 'from']):
    '''
    List primary heads and all human readable message content.
    '''
    if not isdeep:
        for h in heads:
            log('%s: %s' % (h, get_headstring_from_message(message, h)))

    if message.is_multipart():
        for part in message.get_payload():
            logif(isdeep==False, 'payload', 2, sep_length=10)
            logif(isdeep==True, 'sub-payload', sep_length=10, indent=4)
            walk_message(part, True)
    else:
        charset = message.get_content_charset()
        if charset == None:
            print('---   %s   ---' % message['Content-Type'])
            print(message.get_payload())
        else:
            try:
                print('---   %s   ---' % message['Content-Type'])
                print(message.get_payload(decode=message['Content-Transfer-Encoding']).decode(charset))
            except UnicodeDecodeError:
                print(message)

