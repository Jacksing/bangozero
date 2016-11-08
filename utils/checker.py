# encoding: utf-8
import json
from six import string_types


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


def _ensure_json_str_or_dict(target):
    def _ensure_json_str_or_dict_l2(func):
        def _ensure_json_str_or_dict_l3(value, *args):
            if isinstance(value, string_types):
                json_obj = json.loads(value)
                json_str = value
            else:
                json_obj = value
                json_str = json.dumps(value)
            if type(json_obj) is dict:
                if target == 'str':
                    return func(json_str, *args)
                else:
                    return func(json_obj, *args)
            raise ValueError("'value' is not in a json dict format.")
        return _ensure_json_str_or_dict_l3
    return _ensure_json_str_or_dict_l2


"""
Ensure the first argument passed by is in json format and pass
json string to inner function.

The 'value' must be in the format of dict, while list like
object is rejected. If check is ok pass a json string argument
to inner function. Otherwise it will throw out any error during
the check progress.
"""
ensure_json_str = _ensure_json_str_or_dict('str')

"""
Ensure the first argument passed by is in json format and pass
json dict to inner function.

The 'value' must be in the format of dict, while list like
object is rejected. If check is ok pass a json dict argument
to inner function. Otherwise it will throw out any error during
the check progress.
"""
ensure_json_dict = _ensure_json_str_or_dict('dict')
