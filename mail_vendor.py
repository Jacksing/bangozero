import poplib
import imaplib
import smtplib
from email import parser, message_from_string
from email.header import decode_header

from utils import log


def connect(host, username, password):
    log("login with '%s' to '%s'" % (username, host))
    pop_conn = poplib.POP3(host)
    pop_conn.user(username)
    pop_conn.pass_(password)
    return pop_conn


def _get_all(pop_conn, as_message=True):
    """
    Get all mail content from the mail server.
    Return the format in message if 'as_message' is True,
    otherwise return the original mime format.
    """
    count, total_size = pop_conn.stat()
    if as_message:
        return [get_message_from_mime(pop_conn.retr(i)) for i in range(1, count+1)]
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


def get_message_from_mime(mime):
    """
    Parse an orginal Mime format into a Message object model.
    """
    return message_from_string('\n'.join([line.decode('utf-8') for line in mime[1]]))


def get_subject_from_message(message):
    subject, encode_str = decode_header(message['subject'])[0]
    return subject.decode(encode_str)


class ImapHelper:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def conn(self):
        pass


def rudiment1():
    from private import ACCOUNTS

    conn = connect(**ACCOUNTS['163'])
    message = get_message_from_mime(conn.retr(8))
    # conn.dele(8)
    conn.quit()

    print(get_subject_from_message(message))


def rudiment2():
    import os, sys, string
    import smtplib
    
    # 邮件服务器地址
    mailserver = "smtp.163.com"
    # smtp会话过程中的mail from地址
    from_addr = "bangozero@163.com"
    # smtp会话过程中的rcpt to地址
    to_addr = "bangozero@163.com"
    # 信件内容
    msg = "test mail"
    
    svr = smtplib.SMTP(mailserver)
    # 设置为调试模式，就是在会话过程中会有输出信息
    svr.set_debuglevel(1)
    # helo命令，docmd方法包括了获取对方服务器返回信息
    svr.docmd("HELO server")
    # mail from, 发送邮件发送者
    svr.docmd("MAIL FROM: <%s>" % from_addr)
    # rcpt to, 邮件接收者
    svr.docmd("RCPT TO: <%s>" % to_addr)
    # data命令，开始发送数据
    svr.docmd("DATA")
    # 发送正文数据
    svr.send(msg)
    # 比如以 . 作为正文发送结束的标记,用send发送的，所以要用getreply获取返回信息
    svr.send(" . ")
    svr.getreply()
    # 发送结束，退出
    svr.quit()


def rudiment3():
    import os, sys, string
    import smtplib
    import base64
    from private import ACCOUNTS

    work_account = ACCOUNTS['163']
    
    # 邮件服务器地址
    mailserver = "smtp.163.com"
    # 邮件用户名
    username = work_account['username']
    # 密码
    password = work_account['password']
    # smtp会话过程中的mail from地址
    from_addr = "bangozero@163.com"
    # smtp会话过程中的rcpt to地址
    to_addr = "bangozero@163.com"
    # 信件内容
    msg = "my test mail"
    
    svr = smtplib.SMTP(mailserver)
    # 设置为调试模式，就是在会话过程中会有输出信息
    svr.set_debuglevel(1)
    # ehlo命令，docmd方法包括了获取对方服务器返回信息
    svr.docmd("EHLO server")
    # auth login 命令
    svr.docmd("AUTH LOGIN")
    # 发送用户名，是base64编码过的，用send发送的，所以要用getreply获取返回信息
    svr.send(base64.encodestring(username))
    svr.getreply()
    # 发送密码
    svr.send(base64.encodestring(password))
    svr.getreply()
    # mail from, 发送邮件发送者
    svr.docmd("MAIL FROM: <%s>" % from_addr)
    # rcpt to, 邮件接收者
    svr.docmd("RCPT TO: <%s>" % to_addr)
    # data命令，开始发送数据
    svr.docmd("DATA")
    # 发送正文数据
    svr.send(msg)
    # 比如以 . 作为正文发送结束的标记
    svr.send(" . ")
    svr.getreply()
    # 发送结束，退出
    svr.quit()


def rudiment4(work_account, to, subject, text):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText  
    from email.utils import COMMASPACE, formatdate
    from email import encoders

    msg = MIMEMultipart()
    msg['From'] = work_account['username']
    msg['Subject'] = subject
    msg['To'] = COMMASPACE.join(to)  #COMMASPACE==', '
    # msg['To'] = to
    msg['Date'] = formatdate(localtime=True)
    msg.attach(MIMEText(text))

    smtp = smtplib.SMTP(work_account['smtpsvr'])
    smtp.login(work_account['username'], work_account['password'])
    smtp.sendmail(work_account['username'], to, msg.as_string())
    smtp.close()


if __name__ == '__main__':
    from private import ACCOUNTS
    
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
    work_account = ACCOUNTS['buoyancy']

    rudiment4(work_account, target_mail_addresses[1], 'this is test mail from python', context)

