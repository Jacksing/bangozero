# encoding: utf-8

from test_mail import \
    send_mail_to_all_with_work_account, \
    read_latest_graph_with_account, \
    send_mail_to_all_with_work_account_and_check_receiving


def start():
    # send_mail_to_all_with_work_account()
    # read_latest_graph_with_account('163')
    send_mail_to_all_with_work_account_and_check_receiving()
