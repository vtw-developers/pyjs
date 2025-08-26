import unittest

import d_ast_parse
import p_consts
import p_data_structures as pds
import p_generator
import p_generator_invalid_patterns as pat
import p_utils


logger = p_utils.setup_logger(__name__)


class TestGenerateTspsWithGenerator(unittest.TestCase):
  def load_template_dict(self, id: str) -> dict:
    template_dict = p_utils.read_json(p_consts.TEST_ARTIFACTS_DIR / 'tsp-generator' / f'template_dict_{id}.json')
    return template_dict

  def log_ctx_prob_nodes(self, template_dict: dict, test_name: str) -> None:
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

  def parse_snippet(self, snippet: str, template_dict: dict) -> pds.DuoGlotNode:
    '''
    Parse the snippet and return the root node of the tree.
    '''
    ast, _ = d_ast_parse.parse_text_dbg(snippet, template_dict['src_lang'])
    tree = pds.DuoGlotTree(ast)
    root_node = tree.get_root_node()
    return root_node

  def pre_order(self, node: pds.DuoGlotNode, boolean_callback: callable, *callback_args) -> bool:
    '''
    Pre-order traversal of the tree.
    '''
    result = boolean_callback(node, *callback_args)
    if result is True:
      return True
    for child in node.get_children():
      child_res = self.pre_order(child, boolean_callback, *callback_args)
      if child_res is True:
        return True
    return False

  def test_001(self):
    template_dict = self.load_template_dict('001')
    self.log_ctx_prob_nodes(template_dict, '001')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_002(self):
    template_dict = self.load_template_dict('002')
    self.log_ctx_prob_nodes(template_dict, '002')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_003(self):
    template_dict = self.load_template_dict('003')
    self.log_ctx_prob_nodes(template_dict, '003')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_004(self):
    template_dict = self.load_template_dict('004')
    self.log_ctx_prob_nodes(template_dict, '004')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_005(self):
    template_dict = self.load_template_dict('005')
    self.log_ctx_prob_nodes(template_dict, '005')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_006(self):
    template_dict = self.load_template_dict('006')
    self.log_ctx_prob_nodes(template_dict, '006')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_007(self):
    template_dict = self.load_template_dict('007')
    self.log_ctx_prob_nodes(template_dict, '007')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_008(self):
    template_dict = self.load_template_dict('008')
    self.log_ctx_prob_nodes(template_dict, '008')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_009(self):
    template_dict = self.load_template_dict('009')
    self.log_ctx_prob_nodes(template_dict, '009')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_010(self):
    template_dict = self.load_template_dict('010')
    self.log_ctx_prob_nodes(template_dict, '010')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_011(self):
    template_dict = self.load_template_dict('011')
    self.log_ctx_prob_nodes(template_dict, '011')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_012(self):
    template_dict = self.load_template_dict('012')
    self.log_ctx_prob_nodes(template_dict, '012')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_013(self):
    template_dict = self.load_template_dict('013')
    self.log_ctx_prob_nodes(template_dict, '013')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_014(self):
    template_dict = self.load_template_dict('014')
    self.log_ctx_prob_nodes(template_dict, '014')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_015(self):
    template_dict = self.load_template_dict('015')
    self.log_ctx_prob_nodes(template_dict, '015')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_016_special_case_flaky(self):
    '''
    This is a special case due to changes to the TSP generation algorithm.
    Please refer to p_generator.py::_gen_seq_fuzz_node_group()
    ``indices = sample(range(image_norm), p_consts.MAX_FUZZ_GROUP_LEN)`` line.
    '''
    template_dict = self.load_template_dict('016')
    self.log_ctx_prob_nodes(template_dict, '016')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertTrue(abs(len(tsps) - len(template_dict['tsps'])) <= 10, \
      f'Expected number of tsps to be close to {len(template_dict["tsps"])}, but got {len(tsps)}')
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_017(self):
    template_dict = self.load_template_dict('017')
    self.log_ctx_prob_nodes(template_dict, '017')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_018(self):
    template_dict = self.load_template_dict('018')
    self.log_ctx_prob_nodes(template_dict, '018')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_019(self):
    template_dict = self.load_template_dict('019')
    self.log_ctx_prob_nodes(template_dict, '019')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_020(self):
    template_dict = self.load_template_dict('020')
    self.log_ctx_prob_nodes(template_dict, '020')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_021(self):
    template_dict = self.load_template_dict('021')
    self.log_ctx_prob_nodes(template_dict, '021')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_022(self):
    template_dict = self.load_template_dict('022')
    self.log_ctx_prob_nodes(template_dict, '022')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_023(self):
    template_dict = self.load_template_dict('023')
    self.log_ctx_prob_nodes(template_dict, '023')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_024(self):
    template_dict = self.load_template_dict('024')
    self.log_ctx_prob_nodes(template_dict, '024')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_025(self):
    template_dict = self.load_template_dict('025')
    self.log_ctx_prob_nodes(template_dict, '025')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_026(self):
    template_dict = self.load_template_dict('026')
    self.log_ctx_prob_nodes(template_dict, '026')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_027(self):
    template_dict = self.load_template_dict('027')
    self.log_ctx_prob_nodes(template_dict, '027')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_028(self):
    template_dict = self.load_template_dict('028')
    self.log_ctx_prob_nodes(template_dict, '028')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_029(self):
    template_dict = self.load_template_dict('029')
    self.log_ctx_prob_nodes(template_dict, '029')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_030(self):
    template_dict = self.load_template_dict('030')
    self.log_ctx_prob_nodes(template_dict, '030')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_031(self):
    template_dict = self.load_template_dict('031')
    self.log_ctx_prob_nodes(template_dict, '031')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_032(self):
    template_dict = self.load_template_dict('032')
    self.log_ctx_prob_nodes(template_dict, '032')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_033(self):
    template_dict = self.load_template_dict('033')
    self.log_ctx_prob_nodes(template_dict, '033')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_034(self):
    template_dict = self.load_template_dict('034')
    self.log_ctx_prob_nodes(template_dict, '034')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_035(self):
    template_dict = self.load_template_dict('035')
    self.log_ctx_prob_nodes(template_dict, '035')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_036(self):
    template_dict = self.load_template_dict('036')
    self.log_ctx_prob_nodes(template_dict, '036')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_037(self):
    template_dict = self.load_template_dict('037')
    self.log_ctx_prob_nodes(template_dict, '037')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_038(self):
    template_dict = self.load_template_dict('038')
    self.log_ctx_prob_nodes(template_dict, '038')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_039(self):
    template_dict = self.load_template_dict('039')
    self.log_ctx_prob_nodes(template_dict, '039')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_040(self):
    template_dict = self.load_template_dict('040')
    self.log_ctx_prob_nodes(template_dict, '040')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_041(self):
    template_dict = self.load_template_dict('041')
    self.log_ctx_prob_nodes(template_dict, '041')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_042(self):
    template_dict = self.load_template_dict('042')
    self.log_ctx_prob_nodes(template_dict, '042')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_043(self):
    template_dict = self.load_template_dict('043')
    self.log_ctx_prob_nodes(template_dict, '043')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_044(self):
    template_dict = self.load_template_dict('044')
    self.log_ctx_prob_nodes(template_dict, '044')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_045(self):
    template_dict = self.load_template_dict('045')
    self.log_ctx_prob_nodes(template_dict, '045')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_046(self):
    template_dict = self.load_template_dict('046')
    self.log_ctx_prob_nodes(template_dict, '046')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_047(self):
    template_dict = self.load_template_dict('047')
    self.log_ctx_prob_nodes(template_dict, '047')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_048(self):
    template_dict = self.load_template_dict('048')
    self.log_ctx_prob_nodes(template_dict, '048')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_049(self):
    template_dict = self.load_template_dict('049')
    self.log_ctx_prob_nodes(template_dict, '049')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_050(self):
    template_dict = self.load_template_dict('050')
    self.log_ctx_prob_nodes(template_dict, '050')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_051(self):
    template_dict = self.load_template_dict('051')
    self.log_ctx_prob_nodes(template_dict, '051')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_052_special_case_flaky(self):
    '''
    This is a special case due to changes to the TSP generation algorithm.
    Please refer to p_generator.py::_gen_seq_fuzz_node_group()
    ``indices = sample(range(image_norm), p_consts.MAX_FUZZ_GROUP_LEN)`` line.
    '''
    template_dict = self.load_template_dict('052')
    self.log_ctx_prob_nodes(template_dict, '052')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertTrue(abs(len(tsps) - len(template_dict['tsps'])) <= 20, \
      f'Expected number of tsps to be close to {len(template_dict["tsps"])}, but got {len(tsps)}')
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_053(self):
    template_dict = self.load_template_dict('053')
    self.log_ctx_prob_nodes(template_dict, '053')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_054(self):
    template_dict = self.load_template_dict('054')
    self.log_ctx_prob_nodes(template_dict, '054')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_055(self):
    template_dict = self.load_template_dict('055')
    self.log_ctx_prob_nodes(template_dict, '055')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_056(self):
    template_dict = self.load_template_dict('056')
    self.log_ctx_prob_nodes(template_dict, '056')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_057(self):
    template_dict = self.load_template_dict('057')
    self.log_ctx_prob_nodes(template_dict, '057')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_058(self):
    template_dict = self.load_template_dict('058')
    self.log_ctx_prob_nodes(template_dict, '058')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')

  def test_059(self):
    template_dict = self.load_template_dict('059')
    self.log_ctx_prob_nodes(template_dict, '059')
    tsps = p_generator.generate_tsps_with_generator(template_dict)
    self.assertEqual(len(tsps), len(template_dict['tsps']))
    for tsp in tsps:
      for snippet in tsp:
        root_node = self.parse_snippet(snippet, template_dict)
        has_int_as_call_function = self.pre_order(root_node, pat.pattern_1_has_integer_as_function_name)
        self.assertFalse(has_int_as_call_function, f'Integer as function name found in "{snippet}"')
        has_block_with_return_statement = self.pre_order(root_node, pat.pattern_2_has_block_with_ret_stat_secretfn_flag_on, template_dict)
        self.assertFalse(has_block_with_return_statement, f'Return statement not expected in "{snippet}"')
        # Check for empty argument lists
        for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
          has_fn_with_empty_arglist = self.pre_order(root_node, pat.pattern_3_has_fn_with_empty_argument_list, ntype)
          self.assertFalse(has_fn_with_empty_arglist, f'Empty argument list for "{ntype}" found in "{snippet}"')


if __name__ == '__main__':
  unittest.main()
