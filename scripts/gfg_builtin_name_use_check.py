'''
Semi-automated script to check for the use of forbidden names in the main code of GFG benchmark files.
'''


import os
from typing import List, Tuple

import p_consts
import p_utils
import p_visitor as pv
import p_visitor_py as pvpy


class BuiltinNameUseChecker(pv.Visitor):
  def __init__(self, forbidden_names: List[str]) -> None:
    super().__init__()
    self.forbidden_names = set(forbidden_names)
    self.used_forbidden_names = set()
    self.used_forbidden_names_as_fn_call = set()

  # VISIT METHODS
  def visit_IdentifierNode(self, node: pvpy.IdentifierNode) -> None:
    '''
    Check if the identifier node's name is in the forbidden names.
    If it is, print a warning message.
    '''
    # if the identifier is not in the forbidden names, skip it
    if node.val() not in self.forbidden_names:
      return

    # check if the identifier is used in a function call
    parent = node.parent
    if isinstance(parent, pvpy.CallNode):
      if parent.children[0] is node:
        # the identifier is used as a function call
        self.used_forbidden_names_as_fn_call.add(node.val())
        return

    self.used_forbidden_names.add(node.val())

  @classmethod
  def get_used_forbidden_names(
    cls,
    main_code: str,
    forbidden_names: List[str]
  ) -> Tuple[List[str], List[str]]:
    src_parser = p_consts.PARSER_DICT['py']
    ts_tree = src_parser.parse(bytes(main_code, 'utf-8'))
    tree = pvpy.Tree.from_ts_tree(ts_tree)
    checker = cls(forbidden_names)
    checker.visit(tree.root_node)
    return list(checker.used_forbidden_names), list(checker.used_forbidden_names_as_fn_call)

FORBIDDEN_NAMES = list(p_consts.PY_BUILT_IN_FUNCTIONS) + list(p_consts.PY_BUILT_IN_MODULES)

fpaths = sorted(p_consts.GFG_BENCHMARK_DIR.glob("G*.py"))
for fidx, fpath in enumerate(fpaths, start=1):
  # if fidx < 447: continue  # for testing purposes, skip first 12 files

  code = p_utils.read_text(fpath)
  test, main, call = code.split(p_consts.TEST_MAIN_CALL_DELIMITER)

  ufn, ufn_afc = BuiltinNameUseChecker.get_used_forbidden_names(main, FORBIDDEN_NAMES)

  # INTERACTIVE CHECKING
  os.system('clear')
  print(f'Processing file {fidx}/{len(fpaths)}: {fpath}')

  if len(ufn) == 0:
    print('============== No used forbidden names ===============')
    print(f'Used forbidden names: {ufn}')
    print('Used forbidden names as function call:', ufn_afc)
    print(main)

  elif len(ufn) > 0:
    print('============== There are used forbidden names ===============')
    print(f'Used forbidden names: {ufn}')
    print('Used forbidden names as function call:', ufn_afc)
    print(main)

    input()


  # UPDATE THE FILE
  # updated_code = p_consts.TEST_MAIN_CALL_DELIMITER.join([
  #     test,
  #     f'\n{processed_main}\n',
  #     call
  # ])
  # print(updated_code)
  # p_utils.write_text(fpath, updated_code)
  # input()
