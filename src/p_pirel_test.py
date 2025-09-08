import unittest

import d_ast_parse
import p_consts
import p_data_structures as pds
import p_pirel
import p_utils


logger = p_utils.setup_logger(__name__)


class TestAdaptRuleChoicesGetNewNid(unittest.TestCase):
  def setUp(self):
    pass

  def test_01(self):
    code = '''
def f_gold(s):
    myexactlog(1, (3 * math.sqrt(3) * (s * s)) / 2)
    return (3 * math.sqrt(3) * (s * s)) / 2
'''.strip()

    new_code = '''
return (3 * math.sqrt(3) * (s * s)) / 2
'''.strip()

    tree = pds.DuoGlotTree.from_code_str(code, 'py')
    new_tree = pds.DuoGlotTree.from_code_str(new_code, 'py')

    nid = 27
    new_id = p_pirel._adapt_rule_choices_get_new_nid(tree, nid, new_tree)
    self.assertEqual(new_id, 1)

    nid = 28
    new_id = p_pirel._adapt_rule_choices_get_new_nid(tree, nid, new_tree)
    self.assertEqual(new_id, 2)

    nid = 29
    new_id = p_pirel._adapt_rule_choices_get_new_nid(tree, nid, new_tree)
    self.assertEqual(new_id, 3)

    nid = 30
    new_id = p_pirel._adapt_rule_choices_get_new_nid(tree, nid, new_tree)
    self.assertEqual(new_id, 4)

    nid = 33
    new_id = p_pirel._adapt_rule_choices_get_new_nid(tree, nid, new_tree)
    self.assertEqual(new_id, 7)

  def test_expect_assertion_single_node_in_code(self):
    code = '''
def f_gold(s):
    duplicate = (3 * math.sqrt(3) * (s * s)) / 2
    myexactlog(1, (3 * math.sqrt(3) * (s * s)) / 2)
    return (3 * math.sqrt(3) * (s * s)) / 2
'''.strip()

    new_code = '''
return (3 * math.sqrt(3) * (s * s)) / 2
'''.strip()

    tree = pds.DuoGlotTree.from_code_str(code, 'py')
    new_tree = pds.DuoGlotTree.from_code_str(new_code, 'py')

    nid = 9  # `(3 * math.sqrt(3) * (s * s)) / 2`
    with self.assertRaises(AssertionError) as cm:
      p_pirel._adapt_rule_choices_get_new_nid(tree, nid, new_tree)
    self.assertEqual(str(cm.exception), 'support only one similar node in the tree')

  def test_expect_assertion_single_new_node(self):
    code = '''
def f_gold(s):
    myexactlog(1, (3 * math.sqrt(3) * (s * s)) / 2)
    return (3 * math.sqrt(3) * (s * s)) / 2
'''.strip()

    new_code = '''
duplicate = (3 * math.sqrt(3) * (s * s)) / 2
return (3 * math.sqrt(3) * (s * s)) / 2
'''.strip()

    tree = pds.DuoGlotTree.from_code_str(code, 'py')
    new_tree = pds.DuoGlotTree.from_code_str(new_code, 'py')

    nid = 28  # `(3 * math.sqrt(3) * (s * s)) / 2`
    with self.assertRaises(AssertionError) as cm:
      p_pirel._adapt_rule_choices_get_new_nid(tree, nid, new_tree)
    self.assertEqual(str(cm.exception), 'support only one similar node in the new_tree')


class TestGetPreContext(unittest.TestCase):
  def setUp(self):
    self.artifacts_dir = p_consts.TEST_ARTIFACTS_DIR / 'p-pirel' / 'get-pre-context'
    self.lang = 'py'
    self.maxDiff = None

  def read_fixture(self, fid: str) -> tuple[str, str, int]:
    src_main_code = p_utils.read_text(self.artifacts_dir / f'{fid}_in.py')
    expected_pre_context = p_utils.read_text(self.artifacts_dir / f'{fid}_out.py')
    stat_nid = int(p_utils.read_text(self.artifacts_dir / f'{fid}_stat_nid.txt'))
    return src_main_code, expected_pre_context, stat_nid

  def test_all_common(self):
    NUM_FIXTURES = 74
    for i in range(1, NUM_FIXTURES + 1):
      with self.subTest(i=i):
        src_main_code, expected_pre_context, stat_nid = self.read_fixture(f'{i:03}')
        stat_ntext = d_ast_parse.node_id_pretty_print(src_main_code, self.lang, stat_nid)
        pre_context = p_pirel.get_pre_context(src_main_code, self.lang, stat_nid)
        logger.debug(
          f'\n\n~~~ Test case {i}, stat_nid={stat_nid}\n'
          f'~~~ Test case {i}, src_main_code=\n```\n{src_main_code}\n```\n'
          f'~~~ Test case {i}, stat_ntext=\n```\n{stat_ntext}\n```\n'
          f'~~~ Test case {i}, expected_pre_context=\n```\n{expected_pre_context}\n```\n'
          f'~~~ Test case {i}, pre_context=\n```\n{pre_context}\n```\n\n\n')
        self.assertEqual(pre_context.strip(), expected_pre_context.strip())

  def test_if_in_try(self):
    src_main_code, expected_pre_context, stat_nid = self.read_fixture('try_except')
    stat_ntext = d_ast_parse.node_id_pretty_print(src_main_code, self.lang, stat_nid)
    pre_context = p_pirel.get_pre_context(src_main_code, self.lang, stat_nid)
    logger.debug(
      f'~~~ stat_nid={stat_nid}\n'
      f'~~~ src_main_code=\n```\n{src_main_code}\n```\n'
      f'~~~ stat_ntext=\n```\n{stat_ntext}\n```\n'
      f'~~~ expected_pre_context=\n```\n{expected_pre_context}\n```\n'
      f'~~~ pre_context=\n```\n{pre_context}\n```\n\n\n')
    self.assertEqual(pre_context.strip(), expected_pre_context.strip())


if __name__ == '__main__':
  unittest.main()
