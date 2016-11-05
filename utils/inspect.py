# encoding: utf-8

def has_all_attr(object, name_list):
    for name in name_list:
        if not hasattr(object, name):
            return False
    return True


def has_all_key(object, key_list):
    if not type(object) is dict:
        raise TypeError("'object' is not a dict object.")
    for key in key_list:
        if not key in object:
            return False
    return True
