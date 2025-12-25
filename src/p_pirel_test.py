import asyncio
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
    '''
    774 is multiline statement with indentation
    '''
    NUM_FIXTURES = 774
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


class TestGetStatementNodesEOT(unittest.TestCase):
  def setUp(self):
    self.artifacts_dir = p_consts.TEST_ARTIFACTS_DIR / 'p-pirel' / 'get-statement-nodes-eot'
    self.lang = 'py'
    self.maxDiff = None
    self.test_ids = ['bst_clean']

  def read_fixture(self, test_id: str) -> Tuple[str, list[int]]:
    src_main_code = p_utils.read_text(self.artifacts_dir / f'{test_id}.py').strip()
    lines = p_utils.read_text(self.artifacts_dir / f'{test_id}_stat_nids.txt').strip().splitlines()
    expected_eot_nids = [int(x.strip()) for x in lines if x.strip()]
    return src_main_code, expected_eot_nids

  def test_all(self):
    for i, test_id in enumerate(self.test_ids, start=1):
      with self.subTest(test_id=test_id):
        src_main_code, expected_eot_nids = self.read_fixture(test_id)
        eot_nids = asyncio.run(p_pirel.get_statement_nodes_eot(src_main_code, self.lang, return_node_ids=True))
        self.assertEqual(len(eot_nids), len(set(eot_nids)), f'Duplicate nids in {eot_nids}')
        self.assertEqual(eot_nids, expected_eot_nids)


class TestDuoglotTranslateWrapper(unittest.TestCase):
  def setUp(self):
    self.fixtures_dir_path = p_consts.TEST_ARTIFACTS_DIR / 'p-pirel' / 'duoglot-translate-wrapper'
    self.maxDiff = None

  def load_fixture(self, subdir: str, test_id: str) -> dict:
    data = p_utils.read_json(self.fixtures_dir_path / f'{subdir}' / f'{test_id}.json')
    return data

  def test_no_error(self):
    test_ids = sorted([p.stem for p in (self.fixtures_dir_path / 'no-error').glob('*.json')])
    for test_id in test_ids:
      with self.subTest(test_id=test_id):
        data = self.load_fixture('no-error', test_id)

        src_code = data['src_code']
        src_lang = data['src_lang']
        tar_lang = data['tar_lang']
        trans_rules = data['trans_rules']
        auto_backward = data['auto_backward']
        choices = data['choices']
        kwargs = data['kwargs']

        golden_return_dict = data['return_dict']
        src_ann = {int(k): v for k, v in golden_return_dict['src_ann'].items()}
        golden_return_dict['src_ann'] = src_ann
        map_to_exid = {int(k): v for k, v in golden_return_dict['map_to_exid'].items()}
        golden_return_dict['map_to_exid'] = map_to_exid

        return_dict = p_pirel.duoglot_translate_wrapper(
          src_code,
          src_lang,
          tar_lang,
          trans_rules,
          auto_backward,
          choices,
          **kwargs
        )
        eq, p, v1, v2 = p_utils.deep_json_diff(golden_return_dict, return_dict, coerce_types=True)
        self.assertTrue(eq, f'diff: {p}, {v1}, {v2}')

  def test_error(self):
    test_ids = sorted([p.stem for p in (self.fixtures_dir_path / 'error').glob('*.json')])
    for test_id in test_ids:
      with self.subTest(test_id=test_id):
        data = self.load_fixture('error', test_id)

        src_code = data['src_code']
        src_lang = data['src_lang']
        tar_lang = data['tar_lang']
        trans_rules = data['trans_rules']
        auto_backward = data['auto_backward']
        choices = data['choices']
        kwargs = data['kwargs']

        error_class = data['error_class']
        error_msg = data['error_msg']

        try:
          return_dict = p_pirel.duoglot_translate_wrapper(
            src_code,
            src_lang,
            tar_lang,
            trans_rules,
            auto_backward,
            choices,
            **kwargs
          )
        except Exception as err:
          self.assertEqual(err.__class__.__name__, error_class)
          self.assertEqual(error_msg.lower(), str(err).lower())


if __name__ == '__main__':
  unittest.main()
