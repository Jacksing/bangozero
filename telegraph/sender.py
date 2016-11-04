# encoding: utf8

import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

from constrants.mail_words import TG_CONTENT_MAIN_TYPE, TG_CONTENT_SUB_TYPE, TG_FILENAME
from private import ACCOUNTS


work_account = ACCOUNTS['sina']


def send_telegraph(to, subject, text, telegraphs=[]):
    msg = MIMEMultipart()
    msg['From'] = work_account['username']
    msg['To'] = to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    for tl in telegraphs:
        part = MIMEBase(TG_CONTENT_MAIN_TYPE, TG_CONTENT_SUB_TYPE)
        part.set_payload(tl)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % TG_FILENAME)
        msg.attach(part)

    smtp = smtplib.SMTP(work_account['smtp'])
    smtp.login(work_account['username'], work_account['password'])
    smtp.sendmail(work_account['username'], to, msg.as_string())
    smtp.close()


if __name__ == '__main__':
    context = '''
    hello bangozero

    this is a mail from python sender for test purpose.
    if you subscripted this service, please ignore this mail.
    otherwise please send a mail to us to reject this subscrption.

    best regards
    python sender group, shanghai
    '''
    target_mail_addresses = [
        'bangozero@163.com',
        'bangozero@sina.com',
        'jacksingtang@buoyancyinfo.com',
    ]

    telegraph = '{"errno":0,"data":{"userInfo":null,"logInfoExt":[],"sampleHit":0,"login_id":""},"msg":"success"}'

    send_telegraph(target_mail_addresses[0], 'this is test mail from python11', context, [telegraph])
