import unittest
from typing import List

import p_consts
import p_rule_inferencer
import p_utils


logger = p_utils.setup_logger(__name__)


class TestInferTranslationRule(unittest.TestCase):
  def setUp(self):
    self.fixtures_dir = p_consts.TEST_ARTIFACTS_DIR / 'p-rule-inferencer' / 'infer-translation-rule'
    self.maxDiff = None

  def load_data(self, subdir: str, test_id: str) -> dict:
    data = p_utils.read_json(self.fixtures_dir / subdir / f'{test_id}.json')
    return data

  def get_test_ids(self, subdir: str) -> List[str]:
    test_inputs = (self.fixtures_dir / subdir).glob(f'*.json')
    test_ids = sorted([fpath.stem for fpath in test_inputs])
    return test_ids

  def test_no_error(self):
    subdir = 'no-error'
    test_ids = self.get_test_ids(subdir)
    for test_id in test_ids:
      with self.subTest(test_id=test_id):
        data = self.load_data(subdir, test_id)

        translation_pair = data['translation_pair']
        src_lang = data['src_lang']
        tar_lang = data['tar_lang']
        context = data['context']
        is_insert_secret_fn = data['is_insert_secret_fn']
        choose_largest_node = data['choose_largest_node']
        is_ignore_semicolon = data['is_ignore_semicolon']
        golden_translation_rule = data['translation_rule']

        translation_rule = p_rule_inferencer.infer_translation_rule(
          translation_pair,
          src_lang,
          tar_lang,
          context,
          is_insert_secret_fn,
          choose_largest_node,
          is_ignore_semicolon,
          pretty_print_tree_like=False
        )
        self.assertEqual(translation_rule, golden_translation_rule)


  def test_error(self):
    subdir = 'error'
    test_ids = self.get_test_ids(subdir)
    for test_id in test_ids:
      with self.subTest(test_id=test_id):
        data = self.load_data(subdir, test_id)

        translation_pair = data['translation_pair']
        src_lang = data['src_lang']
        tar_lang = data['tar_lang']
        context = data['context']
        is_insert_secret_fn = data['is_insert_secret_fn']
        choose_largest_node = data['choose_largest_node']
        is_ignore_semicolon = data['is_ignore_semicolon']
        error_class = data['error_class']
        error_msg = data['error_msg']

        try:
          translation_rule = p_rule_inferencer.infer_translation_rule(
            translation_pair,
            src_lang,
            tar_lang,
            context,
            is_insert_secret_fn,
            choose_largest_node,
            is_ignore_semicolon,
            pretty_print_tree_like=False
          )
        except Exception as e:
          caught_error = e.__class__.__name__
          caught_error_msg = str(e)
        self.assertEqual(caught_error, error_class)
        self.assertEqual(caught_error_msg, error_msg)


if __name__ == '__main__':
  unittest.main()
