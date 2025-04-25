MYLOG_LIST = {MYLOG_LIST}
import json
mylog_callcount = 0
def _list_compare(ls1, ls2):
  raise NotImplementedError
def mylog_obj_to_comp(arg):
  if isinstance(arg, bool): return ["bool", arg]
  elif isinstance(arg, str): return ["string", len(arg), arg if len(arg) < 10 else arg[0:10]]
  elif isinstance(arg, int) or isinstance(arg, float): return ["num", arg]
  elif isinstance(arg, list) or isinstance(arg, tuple): return ["list", len(arg), mylog_obj_to_comp(arg[0]) if len(arg) > 0 else "EMPTY", mylog_obj_to_comp(arg[1]) if len(arg) > 1 else "EMPTY"]
  elif arg is None: return ["none"]
  else: return ["Unknown"]
def mylog(*args):
  info_list = ["MYLOG:" + str(args[0])]
  for arg in args[1:]:
    info_list.append(mylog_obj_to_comp(arg))
  print("\\n" + json.dumps(info_list))
  if _list_compare(info_list, MYLOG_LIST[mylog_callcount]):
    mylog_callcount += 1
    return
  else:
    raise Exception("MyLogError CALL_ID:" + str(args[0]) + " MISMATCH_IDX:" + str(mylog_callcount))
def myexactlog(*args):
  mylog(*args)