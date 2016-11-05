# encoding: utf-8

SECRET_KEY = 'jnw%0e8@u8ick5o(i7p2u&)0k3*u&p+0s*u2ts06j543jr&hb1'

from mail_words import *

try:
    from accounts import ACCOUNTS
    WORK_ACCOUNT = ACCOUNTS['buoyancy']
except ImportError:
    ACCOUNTS = None
    WORK_ACCOUNT = None

from tests import *
