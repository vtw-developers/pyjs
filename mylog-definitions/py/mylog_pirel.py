import json

_default_print = print

def mylog_obj_to_comp(arg):
  if isinstance(arg, bool):
    return ["bool", arg]
  if isinstance(arg, str):
    return ["string", len(arg), arg]
  if isinstance(arg, (int, float)):
    return ["num", arg]
  if isinstance(arg, (list, tuple)):
    rec_arg = [mylog_obj_to_comp(x) for x in arg]
    return ["list", len(arg), rec_arg]
  if arg is None:
    return ["none"]
  str_result = str(arg)
  return ["Unknown", len(str_result), str_result]

def pirel_obj_serialize(obj):
  if isinstance(obj, set):
    return list(obj)
  return obj

def myexactlog(*args):
  prefix = "MYLOGEX:"
  info_list = [prefix + json.dumps(args[0], sort_keys=True, separators=(",", ":"), default=pirel_obj_serialize)]
  for arg in args[1:]:
    info_list.append(mylog_obj_to_comp(arg))
  _default_print(json.dumps(info_list))

def print(*args, **kwargs):
  myexactlog(args)
  return _default_print(*args, **kwargs)

# this function is inserted into body node types' `block`
def secret_fun_4071():
  return 0
