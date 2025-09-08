import hashlib
import json
import math
from collections.abc import KeysView
from typing import Union

_default_print = print
JS_MAX_SAFE_INTEGER = 9_007_199_254_740_991
JS_MIN_SAFE_INTEGER = -9_007_199_254_740_991

def serialize_none():
  return ["null"]

def serialize_bool(arg: bool):
  return ["bool", arg]

def serialize_str(arg: str):
  return ["string", len(arg), arg]

def serialize_num(arg: Union[int, float]):
  if arg == float('inf'):
    return serialize_str("inf")
  if arg == -float('inf'):
    return serialize_str("-inf")
  if math.isnan(arg):
    return serialize_str("nan")
  if JS_MIN_SAFE_INTEGER <= arg <= JS_MAX_SAFE_INTEGER:
    return ["number", arg]
  return serialize_str('{:.6e}'.format(float(arg)))

def serialize_list(arg: Union[list, tuple]):
  serialized_vals = [serialize(val) for val in arg]
  serialized_vals_str = json.dumps(serialized_vals, separators=(',', ':'))
  hashed = hashlib.sha256(serialized_vals_str.encode('utf-8')).hexdigest()
  return ["hash", len(hashed), hashed]

def serialize_set(arg: set):
  sorted_vals = sorted(arg)
  serialized_vals = [serialize(val) for val in sorted_vals]
  return ["set", len(arg), serialized_vals]

def serialize_dict(arg: dict):
  serialized_key_value_pairs = []
  sorted_keys = sorted(arg.keys())
  for key in sorted_keys:
    serialized_key_value_pairs.append(serialize([key, arg[key]]))
  return ["dict", len(arg), serialized_key_value_pairs]

def serialize(arg):
  if arg is None:
    return serialize_none()
  if isinstance(arg, bool):
    return serialize_bool(arg)
  if isinstance(arg, str):
    return serialize_str(arg)
  if isinstance(arg, (int, float)):
    return serialize_num(arg)
  if isinstance(arg, (list, tuple)):
    return serialize_list(arg)
  if isinstance(arg, set):
    return serialize_set(arg)
  if isinstance(arg, dict):
    return serialize_dict(arg)
  if isinstance(arg, KeysView):
    # e.g. myexactlog(frequency.keys())
    return serialize_list(list(arg))
  if isinstance(arg, range):
    # e.g. myexactlog(range(n + 1))
    return serialize_list(list(arg))
  str_result = str(arg)
  return ["unknown", len(str_result), str_result]

def myexactlog(*args):
  info_list = ["MYLOGEX:"]
  for arg in args:
    info_list.append(serialize(arg))
  _default_print(json.dumps(info_list))

def mylog(*args):
  myexactlog(*args)

def print(*args, **kwargs):
  # myexactlog(args)
  # return _default_print(*args, **kwargs)
  pass

# this function is inserted into body node types' `block`
def secret_fun_4071():
  return 0
