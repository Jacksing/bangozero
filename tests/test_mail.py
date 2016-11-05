# encoding: utf-8

import json
from datetime import datetime
from uuid import uuid1

from django.conf import settings

from telegraph.reader import \
    connect, get_message, parse_message_from_mime, \
    get_telegraph_obj_from_message, walk_message
from telegraph.sender import send_telegraph
from utils.logger import log, logifelse
from utils.inspect import has_all_key

target_mail_addresses = [
    'bangozero@163.com',
    'bangozero@sina.com',
    'jacksingtang@buoyancyinfo.com',
]


def _check_test_settings():
    accounts = getattr(settings, 'ACCOUNTS', None)
    if not accounts or not type(accounts) is dict:
        raise ValueError('cannot find valid test accounts in settings')
    for value in accounts.values():
        if not has_all_key(value, ['svr', 'name', 'addr', 'pw']):
            raise ValueError('invalid accounts in settings')
_check_test_settings()


def send_mail_to_all_with_work_account(to_addrs=target_mail_addresses):
    context = '''
    hello bangozero

    this is a mail from python sender for test purpose.
    if you subscripted this service, please ignore this mail.
    otherwise please send a mail to us to reject this subscrption.

    best regards
    python sender group, shanghai
    '''

    identify_key = str(uuid1())
    telegraph = json.dumps({
        'id': identify_key,
        'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
    })

    log('begin sending to following address with id "%s"' % identify_key)
    log('\n'.join(['%s%s' % (' ' * 4, addr) for addr in to_addrs]))

    try:
        send_telegraph(to_addrs, 'this is test mail from test_mail module', context, [telegraph])
    except Exception as ex:
        log('send mail failed, %s' % ex.message)
        return False, identify_key

    log('send mail successed.')

    return True, identify_key


def read_latest_graph_with_account(account_key):
    try:
        account =  settings.ACCOUNTS[account_key]
    except KeyError:
        log('cannot find account with key "%s"' % account_key)
        return False

    addr = account['addr']
    log('begin read latest mail from %s' % addr)

    conn = connect(account['svr']['pop'], addr, account['pw'])

    count = conn.stat()[0]
    if count == 0:
        log("the mail '%s' box is empty." % addr)
        return False

    message = parse_message_from_mime(conn.retr(count))

    conn.quit()

    telegraph_obj = get_telegraph_obj_from_message(message)
    if telegraph_obj:
        log('find telegraph in latest mail:')
        log(json.dumps(telegraph_obj, indent=2))
    else:
        log('cannot find telegraph in latest mail, so walk through it:')
        walk_message(message)


def send_mail_to_all_with_work_account_and_check_receiving():
    account_list = settings.ACCOUNTS.values()
    to_addrs = [account['addr'] for account in account_list]
    result, identify_key = send_mail_to_all_with_work_account(to_addrs)

    # Read each mail box which had been sent mail above,
    # check whether the latest mail contains the 'identify_key'.
    # The check action will do multi times that specifed in settings
    # util the 'identify_key' be found.
    # 
    # After all the check loop, the account(s) that failed to find
    # 'identify_key' will be listed in log output.
    check_ok_accounts = []

    def _check_receiving():
        for account in account_list:
            if account in check_ok_accounts:
                continue
            
            # get telegraph object
            message = get_message(account['svr']['pop'], account['addr'], account['pw'])
            telegraph_obj = get_telegraph_obj_from_message(message)
            if not type(telegraph_obj) is dict:
                continue
            
            # check identify key, if check ok, add the account to check ok list
            if 'id' in telegraph_obj and telegraph_obj['id'] == identify_key:
                log('%s, check receiving ok.' % account['addr'])
                check_ok_accounts.append(account)

    for _ in range(settings.TRY_READ_TIMES):
        _check_receiving()

    check_failed_account = [account for account in account_list if not account in check_ok_accounts]
    if check_failed_account:
        log('following account(s) check failed:')
        log('\n'.join(['%s%s' % (' ' * 4, account['addr']) for account in check_failed_account]))