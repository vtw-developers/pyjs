import asyncio
import json
import unittest
from typing import Tuple

import d_ast_parse
import p_consts
import p_ext_rule_chooser
import p_utils


class TestGetNextUniqueChoices(unittest.TestCase):
  def setUp(self):
    self.fixtures_dir_path = p_consts.TEST_ARTIFACTS_DIR / 'p-ext-rule-chooser' / 'get-next-unique-choices'
    self.maxDiff = None

  def load_fixture(self, fixture_name: str) -> Tuple[dict, list]:
    data = p_utils.read_json(self.fixtures_dir_path / f'{fixture_name}.json')
    return data['rel_alt_step_infos'], data['choices_list_stack'], data['new_choices']

  def obj_to_str(self, obj: dict) -> str:
    return json.dumps(obj, indent=2, sort_keys=True)

  def test_001(self):
    rel_alt_step_infos, choices_list_stack, golden_choices = self.load_fixture('001')
    new_choices = p_ext_rule_chooser.get_next_unique_choices(rel_alt_step_infos, choices_list_stack, [])
    self.assertEqual(self.obj_to_str(new_choices), self.obj_to_str(golden_choices))

  def test_002(self):
    rel_alt_step_infos, choices_list_stack, golden_choices = self.load_fixture('002')
    new_choices = p_ext_rule_chooser.get_next_unique_choices(rel_alt_step_infos, choices_list_stack, [])
    self.assertEqual(self.obj_to_str(new_choices), self.obj_to_str(golden_choices))

  def test_003(self):
    rel_alt_step_infos, choices_list_stack, golden_choices = self.load_fixture('003')
    new_choices = p_ext_rule_chooser.get_next_unique_choices(rel_alt_step_infos, choices_list_stack, [])
    self.assertEqual(self.obj_to_str(new_choices), self.obj_to_str(golden_choices))

  def test_004(self):
    rel_alt_step_infos, choices_list_stack, golden_choices = self.load_fixture('004')
    new_choices = p_ext_rule_chooser.get_next_unique_choices(rel_alt_step_infos, choices_list_stack, [])
    self.assertEqual(self.obj_to_str(new_choices), self.obj_to_str(golden_choices))

  def test_005(self):
    rel_alt_step_infos, choices_list_stack, golden_choices = self.load_fixture('005')
    new_choices = p_ext_rule_chooser.get_next_unique_choices(rel_alt_step_infos, choices_list_stack, [])
    self.assertEqual(self.obj_to_str(new_choices), self.obj_to_str(golden_choices))

  def test_exhausted_all_choices(self):
    rel_alt_step_infos, choices_list_stack, golden_choices = self.load_fixture('006')
    self.assertRaises(
      p_ext_rule_chooser.RuleCombinationsExhaustedError,
      p_ext_rule_chooser.get_next_unique_choices,
      rel_alt_step_infos,
      choices_list_stack,
      []
    )


class TestGetValidatedStatNidInInstrCode(unittest.TestCase):
  def setUp(self):
    self.fixtures_dir_path = p_consts.TEST_ARTIFACTS_DIR / 'p-ext-rule-chooser' / 'get-validated-stat-nid-in-instr-code'
    self.maxDiff = None

  def load_fixture(self, test_id: str) -> Tuple[str, str, int]:
    src_main_code = p_utils.read_text(self.fixtures_dir_path / f'{test_id}_src_main_code_instr.py')
    simple_ntext = p_utils.read_text(self.fixtures_dir_path / f'{test_id}_simple_ntext.py')
    golden = p_utils.read_text(self.fixtures_dir_path / f'{test_id}_golden.py')
    return src_main_code, simple_ntext, golden

  def test_all_common_gfg(self):
    NUM_TESTS = 200
    for i in range(1, NUM_TESTS + 1):
      test_id = f'{i:03d}'
      with self.subTest(test_id=test_id):
        src_main_code, simple_ntext, golden = self.load_fixture(test_id)
        all_stat_nids = asyncio.run(p_ext_rule_chooser._get_all_stat_nids(
          src_main_code, True))
        val_stat_nid = asyncio.run(p_ext_rule_chooser._get_validated_stat_nid_in_instr_code(
          src_main_code, simple_ntext, all_stat_nids))
        stat_text = d_ast_parse.node_id_pretty_print(src_main_code, 'py', val_stat_nid)
        self.assertEqual(stat_text, golden)


if __name__ == '__main__':
  unittest.main()
