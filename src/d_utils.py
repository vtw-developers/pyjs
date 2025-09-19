# This module is a collection of functions from multiple modules
# in DuoGlot source codebase. They are
# util_hash.py, util_log.py, util_sexpr.py, util_string.py, util_traverse.py


import hashlib
import json
import os
from functools import cache
from pathlib import Path

import pyparsing as pp


# util_hash.py
def string_sha256(string):
  """
  Return a SHA-256 hash of the given string
  """
  return hashlib.sha256(string.encode('utf-8')).hexdigest()

def strings_sha256(string_list):
  """
  Return a SHA-256 hash of the concatenation of all the strings in the list
  """
  return hashlib.sha256(b''.join([string.encode('utf-8') for string in string_list])).hexdigest()

def file_sha256(filepath):
  with open(filepath, 'rb') as f:
    return hashlib.sha256(f.read()).hexdigest()


# util_log.py
_SRC_DIR = Path(__file__).resolve().parent
_ROOT_DIR = _SRC_DIR.parent
_LOG_DIR = _ROOT_DIR / 'logs' / 'duoglot'

def _get_log_filename(filename):
  return os.path.join(_LOG_DIR, filename)

class SetEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, set):
      return str(obj)
    return json.JSONEncoder.default(self, obj)

def log_json(key, jobj):
  fname = _get_log_filename(key + ".json")
  # print(f"# Logging JSON to {fname} (NOTICE: Not for accurate serializing)...")
  with open(fname, 'w') as f:
    json.dump(jobj, f, cls=SetEncoder, indent=1)


# d_util_sexpr.py
# https://gist.github.com/hastern/ac2d7eab7a2a85f588d1
# S-expression grammar
LP = pp.Literal("(").suppress()
RP = pp.Literal(")").suppress()
String = pp.Word(pp.alphanums + '_')
SingleQuoteString = pp.QuotedString(quoteChar="'", esc_char="\\", esc_quote="\\'", unquoteResults=False)
DoubleQuoteString = pp.QuotedString(quoteChar='"', esc_char="\\", esc_quote='\\"', unquoteResults=False)
QuotedString = SingleQuoteString | DoubleQuoteString
Atom = String | QuotedString
Comment = (pp.Literal(";") + pp.restOfLine()).suppress().ignore(QuotedString)
SExpr = pp.Forward()
SExprList = pp.Group(pp.Located(pp.ZeroOrMore(SExpr | Atom | Comment))) # replace pp.Group by pp.Located
SExpr << LP + SExprList + RP


@cache
def parse_sexpr_list(sexprlist_str):
  try:
    pr = SExprList.parseString(sexprlist_str)
    pr_list = pr[0].as_list()
    # print(pr_list)
    def _get_expr_list(pr_list):
      if not isinstance(pr_list, list): return pr_list
      assert len(pr_list) == 3
      return [_get_expr_list(x) for x in pr_list[1]]
    def _get_loc_list(pr_list):
      if not isinstance(pr_list, list): return pr_list
      assert len(pr_list) == 3
      return [(pr_list[0], pr_list[2])] + [_get_loc_list(x) for x in pr_list[1]]
    return _get_expr_list(pr_list), _get_loc_list(pr_list), None
  except pp.ParseException as e:
    return None, None, e


if __name__ == "__main__":
  print("test sexpr list parse.")

  def test_str(s):
    print("------- test_str -------")
    print(s)
    result, loc, err = parse_sexpr_list(s)
    if result is not None:
      print(result)
      print(loc)
    else:
      print("--- error ---")
      print(err)

  test_str("""(a (b "hello")) (c)""")
  test_str("""(a (b "hello"))
(c)""")
  test_str("""
(a (b "hello"))
; what's this?
(c)
""")
  test_str("""
(a (b "hello")) ; what's (a and b)?
; what's this?
(c) ; what's (c and d)?
""")
  test_str("""(a "\\"\\"\\"") (c)""")


# util_string.py
ALLOW_REMOVING_CHARS = set([" ", "\n", "\t"])
ALLOW_ADDING_CHARS = set([" ", "\n", ";"])

def get_string_mapping_a(s1, s2):
  i1 = 0
  i2 = 0
  mapping = []
  while True:
    if i1 >= len(s1): break
    if i2 >= len(s2):
      if s1[i1] in ALLOW_REMOVING_CHARS:
        i1 += 1
        mapping.append(None)
      else:
        around = s1[max(i1-20,0):min(i1+20,len(s1)-1)]
        print(f"ERROR! code_beautifier find unexpected char removal (s2 already ends) [{i1}]:", json.dumps(s1[i1]), json.dumps(around))
        assert "code_beautifier find unexpected char removal in s1 while s2 finished" == 0
    else:
      if s1[i1] == s2[i2]:
        mapping.append(i2)
        i1 += 1
        i2 += 1
      elif s1[i1] != s2[i2]:
        if s1[i1] in ALLOW_REMOVING_CHARS:
          i1 += 1
          mapping.append(None)
        elif s2[i2] in ALLOW_ADDING_CHARS:
          i2 += 1
        else:
            around = s1[max(i1-20,0):min(i1+20,len(s1)-1)]
            targetaround = s2[max(i2-30,0):min(i2+30,len(s2)-1)]
            print(f"ERROR! code_beautifier find unexpected char removal [{i1}]:", json.dumps(s1[i1]), json.dumps(around), json.dumps(targetaround))
            assert "code_beautifier find unexpected char removal" == 0

  assert len(mapping) == len(s1)
  return mapping


# util_traverse.py
def traverse_nested_list_replace(nested_list, node_replacer_func):
  """
  node_replacer_func: node -> should_skip, should_replace, is_subarray, replace_node
  """
  if isinstance(nested_list, list):
    replace_count = 0
    i = 0
    maxlen = len(nested_list)
    while i < maxlen:
      should_skip, should_replace, is_subarray, replace_node = node_replacer_func(nested_list[i])
      if should_skip:
        i += 1
        continue
      if should_replace:
        if not is_subarray:
          nested_list[i] = replace_node
          replace_count += 1
          i += 1
        else:
          replace_count += 1
          nested_list.pop(i)
          maxlen -= 1
          for rep_elem in replace_node:
            nested_list.insert(i, rep_elem)
            i += 1
            maxlen += 1
      else:
        replace_count += traverse_nested_list_replace(nested_list[i], node_replacer_func)
        i += 1
    assert i == len(nested_list)

  else:
    return 0

  return replace_count


def traverse_nested_list_and_dict(list_or_dict, node_reader_func) -> bool:
  """
  node_replacer_func: node -> should_skip, should_stop

  Return True if stop was called
  Return False if stop was never called

  Visit elements in nested list/dict structures in pre-order traversal
  """

  def _traverse_rec(list_or_dict_or_else):

    # is list
    if isinstance(list_or_dict_or_else, list):
      for i in range(len(list_or_dict_or_else)):

        should_skip, should_stop = node_reader_func(i, list_or_dict_or_else[i])
        if should_skip:
          continue
        if should_stop:
          return True

        rec_shold_stop = _traverse_rec(list_or_dict_or_else[i])
        if rec_shold_stop:
          return True

      return False

    # is dict
    elif isinstance(list_or_dict_or_else, dict):
      for key in list_or_dict_or_else:

        should_skip, should_stop = node_reader_func(key, list_or_dict_or_else[key])
        if should_skip:
          continue
        if should_stop:
          return True

        rec_shold_stop = _traverse_rec(list_or_dict_or_else[key])
        if rec_shold_stop:
          return True

      return False

    # not list nor dict
    if not isinstance(list_or_dict_or_else, (int, str)):
      print("TRAVERSE TYPE ERROR:", type(list_or_dict_or_else), list_or_dict_or_else)
      assert 0 == "list_or_dict_or_else_NOT_int_OR_str"

  return _traverse_rec(list_or_dict)
