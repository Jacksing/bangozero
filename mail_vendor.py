import poplib
from email import parser, message_from_string


def get_pop_conn(host, username, password):
    pop_conn = poplib.POP3(host)
    pop_conn.user(username)
    pop_conn.pass_(password)
    return pop_conn


def print_mail_statistics(pop_conn):
    print(pop_conn.list())


def get_all_messages(pop_conn):
    count, total_size = pop_conn.stat()
    return [pop_conn.retr(i) for i in range(1, count+1)]


def get_email_from_message(message):
    return message_from_string('\n'.join([b.decode('utf-8') for b in message[1]]))

