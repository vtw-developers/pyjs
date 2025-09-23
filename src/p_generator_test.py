import unittest
from itertools import chain
from typing import List

import d_ast_parse
import p_consts
import p_data_structures as pds
import p_generator
import p_utils


logger = p_utils.setup_logger(__name__)


class TestGenerateTspsWithGenerator(unittest.TestCase):
  def setUp(self):
    self.maxDiff = None

  def load_template_dict(self, id: str) -> dict:
    template_dict = p_utils.read_json(p_consts.TEST_ARTIFACTS_DIR / 'tsp-generator' / f'template_dict_{id}.json')
    return template_dict

  def _log(self, template_dict: dict, test_name: str) -> None:
    template_origin = template_dict['template_origin']
    context_node_type = template_dict['context_node_type']
    context_node_id = template_dict['context_node_id']
    problematic_node_type = template_dict['problematic_node_type']
    problematic_node_id = template_dict['problematic_node_id']
    problematic_node_path = template_dict['problematic_node_path']

    # get the context and problematic nodes
    ast_text, ann_text = d_ast_parse.parse_text_dbg(template_origin, template_dict['src_lang'], keep_text=True)
    tree_text = pds.PirelTree(ast_text, ann_text)
    tree_text._fix_indentation()
    root_node = tree_text.get_root_node()
    assert len(root_node.get_children()) == 1, 'Root node of template origin must have just a single child'
    context_node = root_node.get_children()[0]
    problematic_node = context_node.get_child_by_path(problematic_node_path)
    assert context_node.get_id() == context_node_id, 'sanity check'
    assert problematic_node.get_id() == problematic_node_id, 'sanity check'
    assert context_node.get_ts_node_type() == context_node_type, 'sanity check'
    assert problematic_node.get_ts_node_type() == problematic_node_type, 'sanity check'

    logger.debug(f'~~~~~~~~~~~~~~~~~~~~~~~~ {test_name} ~~~~~~~~~~~~~~~~~~~~~~~~')
    logger.debug(f'context code: \n"{context_node.get_ts_node_type()}"\n"\n{context_node.get_text()}\n"')
    logger.debug(f'problematic code: \n"{problematic_node.get_ts_node_type()}"\n"\n{problematic_node.get_text()}\n"')

  def _pre_order(self, node: pds.DuoGlotNode, boolean_callback: callable, *callback_args) -> bool:
    '''
    Pre-order traversal of the tree.
    '''
    result = boolean_callback(node, *callback_args)
    if result is True:
      return True
    for child in node.get_children():
      child_res = self._pre_order(child, boolean_callback, *callback_args)
      if child_res is True:
        return True
    return False

  def assertPatterns(self, tsps: List[List[str]], template_dict: dict) -> None:
    '''
    Check for invalid patterns in the generated snippets.
    '''
    for snippet in chain.from_iterable(tsps):
      tree = pds.DuoGlotTree.from_code_str(snippet, template_dict['src_lang'])
      root_node = tree.get_root_node()

      # Check for integer as function name
      has_int_as_call_function = self._pre_order(root_node, _pattern_1_has_integer_as_function_name)
      self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')

      # Check for return statement in block when is_insert_secret_fn flag is on
      has_block_with_return_statement = self._pre_order(root_node, _pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
      self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')

      # Check for empty argument lists
      for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
        has_fn_with_empty_arglist = self._pre_order(root_node, _pattern_3_has_fn_with_empty_argument_list, ntype)
        self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

      # Check for value of subscript being an integer
      has_int_as_value_of_sub = self._pre_order(root_node, _pattern_4_value_of_subscript_is_integer)
      self.assertFalse(has_int_as_value_of_sub, f'Value of subscript being an integer found in "{snippet}"')

      # Check for rhs of for_in_clause being an integer
      has_int_rhs_for_in_clause = self._pre_order(root_node, _pattern_5_rhs_for_in_clause_is_integer)
      self.assertFalse(has_int_rhs_for_in_clause, f'RHS of for_in_clause being an integer found in "{snippet}"')

  def test_all_general(self):
    NUM_TESTS = 63
    for i in range(1, NUM_TESTS + 1):
      test_name = str(i).zfill(3)
      with self.subTest(test_name=test_name):
        template_dict = self.load_template_dict(test_name)
        self._log(template_dict, test_name)
        tsps = p_generator.generate_tsps_with_generator(template_dict)
        self.assertEqual(len(tsps), len(template_dict['tsps']))
        self.assertPatterns(tsps, template_dict)

  def test_flaky_01(self):
    '''
    This is a special case due to changes to the TSP generation algorithm.
    Please refer to p_generator.py::_gen_seq_fuzz_node_group()
    ``indices = sample(range(image_norm), p_consts.MAX_FUZZ_GROUP_LEN)`` line.
    '''
    template_dict = self.load_template_dict('flaky_01')
    self._log(template_dict, 'flaky_01')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertTrue(abs(len(tsps) - len(template_dict['tsps'])) <= 10)
    self.assertPatterns(tsps, template_dict)

  def test_flaky_02(self):
    '''
    This is a special case due to changes to the TSP generation algorithm.
    Please refer to p_generator.py::_gen_seq_fuzz_node_group()
    ``indices = sample(range(image_norm), p_consts.MAX_FUZZ_GROUP_LEN)`` line.
    '''
    template_dict = self.load_template_dict('flaky_02')
    self._log(template_dict, 'flaky_02')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertTrue(abs(len(tsps) - len(template_dict['tsps'])) <= 20)
    self.assertPatterns(tsps, template_dict)

  def test_flaky_03(self):
    template_dict = self.load_template_dict('flaky_03')
    self._log(template_dict, 'flaky_03')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertTrue(abs(len(tsps) - len(template_dict['tsps'])) <= 10)
    self.assertPatterns(tsps, template_dict)


def _pattern_1_has_integer_as_function_name(node: pds.DuoGlotNode) -> bool:
  '''
  RETURN True if the snippet contains an integer as function name.
  NOTE Generator can generate a function with an integer as function name.
  '''
  # node must be non-terminal
  if node.is_terminal():
    return False
  # node must be call
  if node.get_ts_node_type() != 'call':
    return False
  # first child must be non-terminal
  first_child = node.get_children()[0]
  assert first_child.is_nonterminal(), 'first child must be non-terminal'
  # first child must be an integer
  if first_child.get_ts_node_type() != 'integer':
    return False
  return True


def _pattern_2_has_block_with_ret_stat_secretfn_flag_on(node: pds.DuoGlotNode, template_dict: dict) -> bool:
  '''
  RETURN True if the snippet contains a block with a return statement
  when is_insert_secret_fn flag is turned on.
  NOTE Generator may miss putting `secret_fn_4071()` in the `block` when it's necessary.
  '''
  # is_insert_secret_fn must be turned on
  if not template_dict['is_insert_secret_fn']:
    return False
  # node must be non-terminal
  if node.is_terminal():
    return False
  # node must be block
  if node.get_ts_node_type() != 'block':
    return False
  # must have a single non-terminal child
  if node.get_num_nt_children() != 1:
    return False
  # child must be an return_statement
  first_child = node.get_children()[0]
  if first_child.get_ts_node_type() != 'return_statement':
    return False
  return True


def _pattern_3_has_fn_with_empty_argument_list(node: pds.DuoGlotNode, fnname: str) -> bool:
  '''
  RETURN True if the snippet contains a function with an empty argument list.
  For example, float(), range(), len(), min().
  NOTE The simplest argument_list generated is `()`.
  '''
  # node must be non-terminal
  if node.is_terminal():
    return False
  # node must be call
  if node.get_ts_node_type() != 'call':
    return False
  # assert first child must be non-terminal
  first_child = node.get_children()[0]
  assert first_child.is_nonterminal(), 'first child must be non-terminal'
  # first child must be an identifier
  if first_child.get_ts_node_type() != 'identifier':
    return False
  # function name must be `fnname`
  fn_name = first_child.get_children()[0].node_type
  if fn_name != fnname:
    return False
  # assert second child must be non-terminal
  second_child = node.get_children()[1]
  assert second_child.is_nonterminal(), 'second child must be non-terminal'
  # second child must be an argument list
  if second_child.get_ts_node_type() != 'argument_list':
    return False
  # argument_list must have zero non-terminal children
  if second_child.get_num_nt_children() > 0:
    return False
  return True


def _pattern_4_value_of_subscript_is_integer(node: pds.DuoGlotNode) -> bool:
  '''
  RETURN True if the node is an integer that is used as the value of a subscript.
  For example, 3740 in retval_1 = 3740[id_jubr]
                                  ^^^^
  '''
  # node must be non-terminal
  if node.is_terminal():
    return False
  # node must have a parent
  if node.get_parent() is None:
    return False
  # parent of node must be a subscript
  parent = node.get_parent()
  if parent.get_ts_node_type() != 'subscript':
    return False
  # node must be the first child of parent
  if parent.children[0] != node:
    return False
  # node must be integer
  return node.get_ts_node_type() == 'integer'


def _pattern_5_rhs_for_in_clause_is_integer(node: pds.DuoGlotNode) -> bool:
  '''
  RETURN True if the node is an integer that is used as the rhs of a for_in_clause.
  For example, `dp = [2409 for id_frmu in 3645]`
  '''
  # node must be non-terminal
  if node.is_terminal():
    return False
  # node must have a parent
  if node.get_parent() is None:
    return False
  # parent of node must be a for_in_clause
  parent = node.get_parent()
  if parent.get_ts_node_type() != 'for_in_clause':
    return False
  # node must be the last child of parent
  if parent.children[-1] != node:
    return False
  # node must be integer
  return node.get_ts_node_type() == 'integer'


if __name__ == '__main__':
  unittest.main()
