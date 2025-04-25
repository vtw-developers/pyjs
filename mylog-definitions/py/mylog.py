import json

_default_print = print


def mylog_obj_to_comp(is_exact: bool, arg):
  if isinstance(arg, bool):
    return ["bool", arg]
  elif isinstance(arg, str):
    if is_exact:
      return ["string", len(arg), arg]
    else:
      return ["string", len(arg), arg if len(arg) < 10 else arg[0:10]]
  elif isinstance(arg, (int, float)):
    return ["num", arg]
  elif isinstance(arg, (list, tuple)):
    if is_exact:
      return [
        "list",
        len(arg),
        [mylog_obj_to_comp(is_exact, x) for x in arg]
      ]
    else:
      return [
        "list",
        len(arg),
        mylog_obj_to_comp(is_exact, arg[0]) if len(arg) > 0 else "EMPTY",
        mylog_obj_to_comp(is_exact, arg[1]) if len(arg) > 1 else "EMPTY",
      ]
  elif arg is None:
    return ["none"]
  else:
    str_result = str(arg)
    return ["Unknown", len(str_result), str_result]


def _mylog(is_exact, *args):
  prefix = "MYLOGEX:" if is_exact else "MYLOGAP:"
  info_list = [prefix + json.dumps(args[0], sort_keys=True, separators=(",", ":"))]
  for arg in args[1:]:
    info_list.append(mylog_obj_to_comp(is_exact, arg))
  _default_print("\\n" + json.dumps(info_list))


def mylog(*args):
  _mylog(False, *args)


def myexactlog(*args):
  _mylog(True, *args)


def print(*args, **kargs):
  myexactlog(-1, args)
  return _default_print(*args, **kargs)
