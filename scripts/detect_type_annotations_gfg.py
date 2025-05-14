'''
debug config:
    {
      "name": "detect_typed_annotations_gfg.py",
      "type": "debugpy",
      "request": "launch",
      "cwd": "${workspaceFolder}/src/",
      "program": "detect_typed_annotations_gfg.py",
      "console": "integratedTerminal",
      "justMyCode": true
    },
'''

import tree_sitter

import p_consts
import p_utils


def has_typed_parameter(code: str, tree: tree_sitter.Tree) -> bool:
  '''
  RETURN False if `tree` does not have a typed parameter
  '''
  global QUERY_TYPED_PARAMETER
  captures = QUERY_TYPED_PARAMETER.captures(tree.root_node)
  if len(captures) == 0:
    return False
  for capture in captures:
    node, capture_name = capture
    print(f"Capture name: {capture_name}, Text: {code[node.start_byte:node.end_byte]}")
  return True


def has_return_type(code: str, tree: tree_sitter.Tree) -> bool:
  '''
  RETURN False if `tree` does not have a return type annotation
  '''
  global QUERY_RETURN_TYPE
  captures = QUERY_RETURN_TYPE.captures(tree.root_node)
  if len(captures) == 0:
    return False
  for capture in captures:
    node, capture_name = capture
    print(f"Capture name: {capture_name}, Text: {code[node.start_byte:node.end_byte]}")
  return True


PARSER = p_consts._py_parser
LANGUAGE = p_consts._py_language

QUERY_RETURN_TYPE_STR = '''
(function_definition
  return_type: (type) @return_type
)
'''
QUERY_TYPED_PARAMETER_STR = '''
(parameters (typed_parameter) @typed_parameter)
'''
QUERY_RETURN_TYPE = LANGUAGE.query(QUERY_RETURN_TYPE_STR)
QUERY_TYPED_PARAMETER = LANGUAGE.query(QUERY_TYPED_PARAMETER_STR)

fpaths = list(p_consts.GFG_BENCHMARK_DIR.glob("L*.py"))
for fpath in fpaths:
  code = p_utils.read_text(fpath)
  test, main, call = code.split(p_consts.TEST_MAIN_CALL_DELIMITER)
  tree = PARSER.parse(bytes(main, "utf8"))

  hastp = has_typed_parameter(main, tree)
  if hastp:
    print(f"Typed parameter found in {fpath}")
    input()

  hasrt = has_return_type(main, tree)
  if hasrt:
    print(f"Return type found in {fpath}")
    input()
