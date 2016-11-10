# encoding: utf-8

import os
from random import Random

CN_CHARS = '''
山不在高有仙则名水不在深有龙则灵斯是陋室惟吾德馨苔
痕上阶绿草色入帘青谈笑有鸿儒往来无白丁可以调素琴阅
金经无丝竹之乱耳无案牍之劳形南阳诸葛庐西蜀子云亭孔
子云何陋之有'''

JP_CHARS = '''
あかさたなはまやらわアカサタナハマヤラワんン
いきしちにひみいりいイキシチニヒミイリイ
うくすつぬふむゆるうウクスツヌフムユルウ
えけせてねへめえれえエケセテネヘメエレエ
おこそとのほもよろをオコソトノホモヨロヲ
'''

def random_str(randomlength=8, chars=None):
    str = ''
    if not chars:
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        # chars += CN_CHARS + JP_CHARS
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str


def execmd(cmd):
    with os.popen(cmd) as c:
        return c.read()
