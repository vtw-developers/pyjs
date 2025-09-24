import hashlib
import json
import math
import random
import sys
from collections.abc import Iterable
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
    # force whole numbers to be int type
    if arg % 1 == 0:
      return ["number", int(arg)]
    return ["number", arg]
  return serialize_str('{:.6e}'.format(float(arg)))

def serialize_list(arg: Iterable):
  serialized_vals = [serialize(val) for val in arg]
  serialized_vals_str = json.dumps(serialized_vals, separators=(',', ':'))
  hashed = hashlib.sha256(serialized_vals_str.encode('utf-8')).hexdigest()
  return ["hash", len(hashed), hashed]

def serialize_set(arg: set):
  sorted_vals = sorted(arg)
  serialized_vals = [serialize(val) for val in sorted_vals]
  return ["set", len(arg), serialized_vals]

def serialize_dict(arg: dict):
  keys = list(arg.keys())
  # convert int and float keys to strings
  # since JS object keys are always strings
  for key in keys:
    if isinstance(key, str):
      continue
    if isinstance(key, (int, float)):
      new_key = str(key)
      arg[new_key] = arg[key]
      del arg[key]
      continue
    raise NotImplementedError
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
  if isinstance(arg, (set, frozenset)):
    return serialize_set(arg)
  if isinstance(arg, dict):
    return serialize_dict(arg)
  if isinstance(arg, Iterable):
    return serialize_list(list(arg))
  if callable(arg):
    return ["function"]
  str_result = str(arg)
  return ["unknown", len(str_result), str_result]

_trace_idx = 0  # for debugging
def myexactlog(*args):
  global _trace_idx
  info_list = ["MYLOGEX:"]
  for arg in args:
    info_list.append(serialize(arg))
  _default_print(json.dumps(info_list))
  _trace_idx += 1

def mylog(*args):
  myexactlog(*args)

def print(*args, **kwargs):
  # myexactlog(args)
  # return _default_print(*args, **kwargs)
  pass

# this function is inserted into body node types' `block`
def secret_fun_4071():
  return 0
