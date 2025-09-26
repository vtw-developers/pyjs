import unittest
from typing import Tuple

import d_ast_parse
import p_consts
import p_data_structures as pds
import p_pirel
import p_utils


logger = p_utils.setup_logger(__name__)


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
        pre_context = p_pirel.get_pre_context(src_main_code, self.lang, True, stat_nid, [])
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
    pre_context = p_pirel.get_pre_context(src_main_code, self.lang, True, stat_nid, [])
    logger.debug(
      f'~~~ stat_nid={stat_nid}\n'
      f'~~~ src_main_code=\n```\n{src_main_code}\n```\n'
      f'~~~ stat_ntext=\n```\n{stat_ntext}\n```\n'
      f'~~~ expected_pre_context=\n```\n{expected_pre_context}\n```\n'
      f'~~~ pre_context=\n```\n{pre_context}\n```\n\n\n')
    self.assertEqual(pre_context.strip(), expected_pre_context.strip())


class TestRFindStatNodeByText(unittest.TestCase):
  def setUp(self):
    self.artifacts_dir = p_consts.TEST_ARTIFACTS_DIR / 'p-pirel' / 'rfind-stat-node-by-text'
    self.lang = 'py'
    self.maxDiff = None

  def read_fixture(self, test_id: str) -> Tuple[str, str, int]:
    src_main_code = p_utils.read_text(self.artifacts_dir / f'{test_id}_in.py').strip()
    stat_ntext = p_utils.read_text(self.artifacts_dir / f'{test_id}_statement.py').strip()
    expected_stat_nid = int(p_utils.read_text(self.artifacts_dir / f'{test_id}_gold_nid.txt'))
    return src_main_code, stat_ntext, expected_stat_nid

  def test_all_common(self):
    NUM_FIXTURES = 773
    for i in range(1, NUM_FIXTURES + 1):
      test_id = f'{i:03}'
      with self.subTest(test_id=test_id):
        src_main_code, statement, expected_stat_nid = self.read_fixture(test_id)
        stat_nid = p_pirel._rfind_statement_nid_by_text(src_main_code, statement)
        self.assertEqual(stat_nid, expected_stat_nid)


class TestCreateSrcMainCodeForVal(unittest.TestCase):
  def setUp(self):
    self.artifacts_dir = p_consts.TEST_ARTIFACTS_DIR / 'p-pirel' / 'instrument-with-break-statements'
    self.lang = 'py'
    self.maxDiff = None

  def read_fixture(self, test_id: str) -> Tuple[str, str, str, str]:
    src_main_code = p_utils.read_text(self.artifacts_dir / f'{test_id}_src_main_code.py').strip()
    statement = p_utils.read_text(self.artifacts_dir / f'{test_id}_statement.py').strip()
    pre_context = p_utils.read_text(self.artifacts_dir / f'{test_id}_pre_context.py').strip()
    expected_instrumented_code = p_utils.read_text(self.artifacts_dir / f'{test_id}_gold_instrumented.py').strip()
    return src_main_code, statement, pre_context, expected_instrumented_code

  def test_all_three_split(self):
    NUM_FIXTURES = 24
    for i in range(1, NUM_FIXTURES + 1):
      test_id = f'{i:03}'
      with self.subTest(test_id=test_id):
        src_main_code, statement, pre_context, expected_instrumented_code = self.read_fixture(test_id)
        instrumented_code = p_pirel._create_src_main_code_for_val(
          src_main_code, pre_context, statement, True)
        self.assertEqual(instrumented_code.strip(), expected_instrumented_code.strip())


if __name__ == '__main__':
  unittest.main()
