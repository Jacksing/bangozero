# encoding: utf8

import json

import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

from django.conf import settings


_work_smtpserver =settings.WORK_ACCOUNT['svr']['smtp']
_work_name = settings.WORK_ACCOUNT['name']
_work_mailaddr = settings.WORK_ACCOUNT['addr']
_work_passwd = settings.WORK_ACCOUNT['pw']


def _generate_graph(json_content):
    """
    Parse json string/object into 'graph' multipart object.
    'graph' contains the specified main/sub content type and filename.
    """
    if type(json_content) == dict:
        json_content = json.dumps(json_content)
    else:
        try:
            if type(json.loads(json_content)) != dict:
                raise ValueError("'json_content' should be a dict json string.")
        except (ValueError, TypeError) as ex:
            raise ex
    mime = MIMEBase(settings.TG_CONTENT_MAIN_TYPE, settings.TG_CONTENT_SUB_TYPE)
    mime.set_payload(json_content)
    encoders.encode_base64(mime)
    mime.add_header('Content-Disposition', 'attachment; filename="%s"' % settings.TG_FILENAME)
    return mime


def send_telegraph(to_addrs, subject, text, telegraphs=[]):
    """
    Send mail with the globally configed mail sender account.
    """
    telegraphs = [_generate_graph(tl) for tl in telegraphs]
    return send_mail(
        _work_smtpserver,
        _work_name,
        _work_mailaddr,
        _work_passwd,
        to_addrs, subject, text, telegraphs
    )


def send_mail(smtp_server, from_name, from_addr, from_addr_passwd, to_addrs, subject, text, payloads=[]):
    """
    Send mail with the information given in arguments.
    """
    message = MIMEMultipart()
    message['From'] = from_name
    message['To'] = ','.join(to_addrs)
    message['Date'] = formatdate(localtime=True)
    message['Subject'] = subject

    context = MIMEText(text, _charset='utf-8')
    # <ref>: http://outofmemory.cn/code-snippet/1464/python-send-youjian-resolve-suoyou-luanma-question
    # uncomment following line if messy code appear in mail context
    #
    # context["Accept-Language"]="zh-CN"
    # context["Accept-Charset"]="ISO-8859-1,utf-8"
    message.attach(context)

    for pl in payloads:
        message.attach(pl)

    smtp = smtplib.SMTP(smtp_server)
    smtp.login(from_addr, from_addr_passwd)
    smtp.sendmail(from_addr, to_addrs, message.as_string())
    smtp.close()
