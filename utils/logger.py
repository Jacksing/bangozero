"""
Common function and tools
"""

def logif(condition, msg, pre_newline=0, post_newline=0, sep='*', sep_length=0, indent=0):
    if not condition:
        return
    log(msg, pre_newline, post_newline, sep, sep_length, indent)


def logifelse(condition, msg, elsemsg, pre_newline=0, post_newline=0, sep="*", sep_length=0, indent=0):
    log(condition and msg or elsemsg, pre_newline, post_newline, sep, sep_length, indent)


def log(msg, pre_newline=0, post_newline=0, sep='*', sep_length=0, indent=0):
    if pre_newline != 0:
        _print('\n' * pre_newline, indent)
    if sep_length > 0:
        _print(sep * sep_length, indent)
    _print(msg, indent)
    if sep_length > 0:
        _print(sep * sep_length, indent)
    if post_newline != 0:
        _print('\n' * post_newline, indent)

def _print(msg, indent=0):
    if indent != 0:
        msg = '\n'.join([' ' * indent + m for m in msg.split('\n')])
    print(msg)


log_if = logif
log_ifelse = logifelse

