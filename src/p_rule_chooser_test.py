import json
import unittest
from typing import Tuple

import p_consts
import p_rule_chooser
import p_utils


class TestGetNextUniqueChoices(unittest.TestCase):
  def setUp(self):
    self.fixtures_dir_path = p_consts.TEST_ARTIFACTS_DIR / 'p-rule-chooser' / 'get-next-unique-choices'
    self.maxDiff = None

  def load_fixture(self, fixture_name: str) -> Tuple[dict, list]:
    data = p_utils.read_json(self.fixtures_dir_path / f'{fixture_name}.json')
    return data['rel_alt_step_infos'], data['choices_list_stack'], data['new_choices']

  def obj_to_str(self, obj: dict) -> str:
    return json.dumps(obj, indent=2, sort_keys=True)

  def test_001(self):
    rel_alt_step_infos, choices_list_stack, golden_choices = self.load_fixture('001')
    new_choices = p_rule_chooser.get_next_unique_choices(rel_alt_step_infos, choices_list_stack)
    self.assertEqual(self.obj_to_str(new_choices), self.obj_to_str(golden_choices))

  def test_002(self):
    rel_alt_step_infos, choices_list_stack, golden_choices = self.load_fixture('002')
    new_choices = p_rule_chooser.get_next_unique_choices(rel_alt_step_infos, choices_list_stack)
    self.assertEqual(self.obj_to_str(new_choices), self.obj_to_str(golden_choices))

  def test_003(self):
    rel_alt_step_infos, choices_list_stack, golden_choices = self.load_fixture('003')
    new_choices = p_rule_chooser.get_next_unique_choices(rel_alt_step_infos, choices_list_stack)
    self.assertEqual(self.obj_to_str(new_choices), self.obj_to_str(golden_choices))

  def test_004(self):
    rel_alt_step_infos, choices_list_stack, golden_choices = self.load_fixture('004')
    new_choices = p_rule_chooser.get_next_unique_choices(rel_alt_step_infos, choices_list_stack)
    self.assertEqual(self.obj_to_str(new_choices), self.obj_to_str(golden_choices))

  def test_005(self):
    rel_alt_step_infos, choices_list_stack, golden_choices = self.load_fixture('005')
    new_choices = p_rule_chooser.get_next_unique_choices(rel_alt_step_infos, choices_list_stack)
    self.assertEqual(self.obj_to_str(new_choices), self.obj_to_str(golden_choices))

  def test_exhausted_all_choices(self):
    rel_alt_step_infos, choices_list_stack, golden_choices = self.load_fixture('006')
    self.assertRaises(
      p_rule_chooser.RuleCombinationsExhaustedError,
      p_rule_chooser.get_next_unique_choices,
      rel_alt_step_infos,
      choices_list_stack
    )
    

if __name__ == '__main__':
  unittest.main()
