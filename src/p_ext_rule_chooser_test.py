import copy
import asyncio
import json
import shutil
import unittest
from typing import Tuple

import d_ast_parse
import p_consts
import p_ext_rule_chooser
import p_pirel
import p_ruleset
import p_utils


class TestGetNextUniqueChoices(unittest.TestCase):
  def setUp(self):
    self.fixtures_dir_path = p_consts.TEST_ARTIFACTS_DIR / 'p-ext-rule-chooser' / 'get-next-unique-choices'
    self.maxDiff = None

  def load_fixture(self, subdir: str, fixture_name: str) -> Tuple[dict, list]:
    data = p_utils.read_json(self.fixtures_dir_path / f'{subdir}' / f'{fixture_name}.json')
    choices_list_history = data['choices_list_history']
    for choices_list in choices_list_history:
      for i in range(len(choices_list)):
        elem = choices_list[i]
        choices_list[i] = tuple(elem[0]), elem[1]
    verified_choice_options = data['verified_choice_options']
    verified_choice_options = [(tuple(a[0]), a[1]) for a in verified_choice_options]
    rel_alt_step_infos = data['rel_alt_step_infos']
    new_choices = data['new_choices']
    for k, v in rel_alt_step_infos.items():
      v['current_range_info'] = tuple(v['current_range_info'])
    for i in range(len(new_choices['choices_list'])):
      choice = new_choices['choices_list'][i]
      new_choices['choices_list'][i] = (tuple(choice[0]), choice[1])
    return choices_list_history, verified_choice_options, rel_alt_step_infos, new_choices

  def rerun_and_reorganize_tests(self):
    '''
    Rerun tests and reorganize them into new directories based on their outcomes.
    '''
    subdir_no_error = 'no-error'
    subdir_rule_comb_exh = 'rule-comb-exh'
    subdir_vrf_rules_exh = 'vrf-rules-exh'

    nsubdir_no_error = f'new-{subdir_no_error}'
    nsubdir_rule_comb_exh = f'new-{subdir_rule_comb_exh}'
    nsubdir_vrf_rules_exh = f'new-{subdir_vrf_rules_exh}'

    test_fpaths = list((self.fixtures_dir_path / subdir_no_error).glob('*.json'))
    test_fpaths += list((self.fixtures_dir_path / subdir_rule_comb_exh).glob('*.json'))
    test_fpaths += list((self.fixtures_dir_path / subdir_vrf_rules_exh).glob('*.json'))

    cnt_no_error = 1
    cnt_rule_comb_exh = 1
    cnt_vrf_rules_exh = 1

    for fpath in test_fpaths:
      test_id = fpath.stem
      subdir = fpath.parent.name

      test_id_no_error = f'no-error-{cnt_no_error:03d}'
      test_id_rule_comb_exh = f'rule-comb-exh-{cnt_rule_comb_exh:03d}'
      test_id_vrf_rules_exh = f'vrf-rules-exh-{cnt_vrf_rules_exh:03d}'

      with self.subTest(test_id=test_id):
        choices_list_history, verified_choice_options, rel_alt_step_infos, gold_new_choices = self.load_fixture(subdir, test_id)
        try:
          new_choices = p_ext_rule_chooser.get_next_unique_choices(
            rel_alt_step_infos,
            choices_list_history,
            verified_choice_options,
            raise_on_missing_vrf_rule=True,
          )
          eq, p, v1, v2 = p_utils.deep_json_diff(gold_new_choices, new_choices, coerce_types=True)
          self.assertTrue(eq)
          shutil.copy(fpath, self.fixtures_dir_path / nsubdir_no_error / f'{test_id_no_error}.json')
          cnt_no_error += 1
        except p_ext_rule_chooser.RuleCombinationsExhaustedError as e:
          shutil.copy(fpath, self.fixtures_dir_path / nsubdir_rule_comb_exh / f'{test_id_rule_comb_exh}.json')
          cnt_rule_comb_exh += 1
        except p_ext_rule_chooser.VerifiedRulesExhaustedError as e:
          shutil.copy(fpath, self.fixtures_dir_path / nsubdir_vrf_rules_exh / f'{test_id_vrf_rules_exh}.json')
          cnt_vrf_rules_exh += 1

  def test_no_errors(self):
    subdir = 'no-error'
    test_fpaths = sorted((self.fixtures_dir_path / subdir).glob('*.json'))
    for fpath in test_fpaths:
      test_id = fpath.stem
      with self.subTest(test_id=test_id):
        choices_list_history, verified_choice_options, rel_alt_step_infos, gold_new_choices = self.load_fixture(subdir, test_id)
        new_choices = p_ext_rule_chooser.get_next_unique_choices(
          rel_alt_step_infos,
          choices_list_history,
          verified_choice_options,
          raise_on_missing_vrf_rule=True,
        )
        eq, p, v1, v2 = p_utils.deep_json_diff(gold_new_choices, new_choices, coerce_types=True)
        self.assertTrue(eq)

  def test_rule_comb_exh_error(self):
    subdir = 'rule-comb-exh'
    test_fpaths = sorted((self.fixtures_dir_path / subdir).glob('*.json'))
    for fpath in test_fpaths:
      test_id = fpath.stem
      with self.subTest(test_id=test_id):
        choices_list_history, verified_choice_options, rel_alt_step_infos, gold_new_choices = self.load_fixture(subdir, test_id)
        with self.assertRaises(p_ext_rule_chooser.RuleCombinationsExhaustedError):
          new_choices = p_ext_rule_chooser.get_next_unique_choices(
            rel_alt_step_infos,
            choices_list_history,
            verified_choice_options,
            raise_on_missing_vrf_rule=True,
          )

  def test_vrf_rules_exh_error(self):
    subdir = 'vrf-rules-exh'
    test_fpaths = sorted((self.fixtures_dir_path / subdir).glob('*.json'))
    for fpath in test_fpaths:
      test_id = fpath.stem
      with self.subTest(test_id=test_id):
        choices_list_history, verified_choice_options, rel_alt_step_infos, gold_new_choices = self.load_fixture(subdir, test_id)
        with self.assertRaises(p_ext_rule_chooser.VerifiedRulesExhaustedError):
          new_choices = p_ext_rule_chooser.get_next_unique_choices(
            rel_alt_step_infos,
            choices_list_history,
            verified_choice_options,
            raise_on_missing_vrf_rule=True,
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
    test_ids = sorted([fpath.stem.split('_')[0] for fpath in self.fixtures_dir_path.glob('*_golden.py')])
    for test_id in test_ids:
      with self.subTest(test_id=test_id):
        src_main_code, simple_ntext, golden = self.load_fixture(test_id)
        all_stat_nids = asyncio.run(p_pirel._get_statement_nodes(src_main_code, 'py', True, return_node_ids=True))
        val_stat_nid = asyncio.run(p_ext_rule_chooser._get_validated_stat_nid_in_instr_code(
          src_main_code, simple_ntext, all_stat_nids))
        stat_text = d_ast_parse.node_id_pretty_print(src_main_code, 'py', val_stat_nid)
        self.assertEqual(stat_text, golden)


class TestStatNodeValidateExprs(unittest.TestCase):
  def setUp(self):
    self.fixtures_dir_path = p_consts.TEST_ARTIFACTS_DIR / 'p-ext-rule-chooser' / 'stat-node-validate-exprs'
    self.maxDiff = None

  def load_fixture(self, subdir: str, test_id: str) -> dict:
    data = p_utils.read_json(self.fixtures_dir_path / f'{subdir}' / f'{test_id}.json')
    return data

  def test_no_error(self):
    test_ids = sorted([p.stem for p in (self.fixtures_dir_path / 'no-error').glob('*.json')])
    for test_id in test_ids:
      with self.subTest(test_id=test_id):
        data = self.load_fixture('no-error', test_id)

        src_main_code = data['src_main_code']
        src_test_code = data['src_test_code']
        translation_rules_test_code = data['translation_rules_test_code']
        ruleset = p_ruleset.Ruleset.from_dict(data['ruleset'])
        simple_ntext = data['simple_ntext']
        subject_name = data['subject_name']
        gold_verified_choice_options = data['verified_choice_options']

        asyncio.run(p_ext_rule_chooser.stat_node_validate_exprs(
          src_main_code,
          src_test_code,
          translation_rules_test_code,
          ruleset,
          simple_ntext,
          subject_name,
        ))
        verified_choice_options = ruleset.get_choice_options_from_verified_rules(src_main_code)
        eq, p, v1, v2 = p_utils.deep_json_diff(gold_verified_choice_options, verified_choice_options, coerce_types=True)
        self.assertTrue(eq, f'Difference found:\n{p}\nGold:\n{v1}\nNew:\n{v2}')

  def test_error(self):
    test_ids = sorted([p.stem for p in (self.fixtures_dir_path / 'error').glob('*.json')])
    for test_id in test_ids:
      with self.subTest(test_id=test_id):
        data = self.load_fixture('error', test_id)

        src_main_code = data['src_main_code']
        src_test_code = data['src_test_code']
        translation_rules_test_code = data['translation_rules_test_code']
        ruleset = p_ruleset.Ruleset.from_dict(data['ruleset'])
        simple_ntext = data['simple_ntext']
        subject_name = data['subject_name']
        error_class = data['error_class']
        error_msg = data['error_msg']

        try:
          asyncio.run(p_ext_rule_chooser.stat_node_validate_exprs(
            src_main_code,
            src_test_code,
            translation_rules_test_code,
            ruleset,
            simple_ntext,
            subject_name,
          ))
        except Exception as err:
          self.assertEqual(err.__class__.__name__, error_class)
          self.assertEqual(error_msg.lower(), str(err).lower())


if __name__ == '__main__':
  unittest.main()
