import json
import unittest
from typing import Tuple

import p_consts
import p_code_runner
import p_rule_applicator


class TestCompareTraces(unittest.TestCase):
  '''
  Test cases for the are_traces_equal_rec function in p_rule_applicator.
  '''
  def setUp(self):
    self.fixture_dir_path = p_consts.TEST_ARTIFACTS_DIR / 'p-rule-applicator' / 'compare-traces'

  def get_fixtures(self, fixture_id: str) -> Tuple[list, list]:
    src_stdout = (self.fixture_dir_path / f'stdout-{fixture_id}-src.txt').read_text()
    tar_stdout = (self.fixture_dir_path / f'stdout-{fixture_id}-tar.txt').read_text()
    src_trace = p_code_runner._extract_trace_from_stdout(src_stdout)
    tar_trace = p_code_runner._extract_trace_from_stdout(tar_stdout)
    return src_trace, tar_trace

  def test_001(self):
    src_trace, tar_trace = self.get_fixtures('001')
    result = p_rule_applicator.are_traces_equal_rec(src_trace, tar_trace)
    self.assertFalse(result, 'Expected traces not to match')

  def test_002(self):
    src_trace, tar_trace = self.get_fixtures('002')
    result = p_rule_applicator.are_traces_equal_rec(src_trace, tar_trace)
    self.assertTrue(result, 'Expected traces not to match')

  def test_003(self):
    src_trace, tar_trace = self.get_fixtures('003')
    result = p_rule_applicator.are_traces_equal_rec(src_trace, tar_trace)
    self.assertFalse(result, 'Expected traces not to match')

  def test_004(self):
    src_trace, tar_trace = self.get_fixtures('004')
    result = p_rule_applicator.are_traces_equal_rec(src_trace, tar_trace)
    self.assertFalse(result, 'Expected traces not to match')

  def test_005(self):
    src_trace, tar_trace = self.get_fixtures('005')
    result = p_rule_applicator.are_traces_equal_rec(src_trace, tar_trace)
    self.assertTrue(result, 'Expected traces not to match')

  def test_006_very_large(self):
    src_trace, tar_trace = self.get_fixtures('006')
    result = p_rule_applicator.are_traces_equal_rec(src_trace, tar_trace)
    self.assertTrue(result, 'Expected traces not to match')

  def test_007(self):
    src_trace, tar_trace = self.get_fixtures('007')
    result = p_rule_applicator.are_traces_equal_rec(src_trace, tar_trace)
    self.assertTrue(result, 'Expected traces not to match')

  def test_008(self):
    src_trace, tar_trace = self.get_fixtures('008')
    result = p_rule_applicator.are_traces_equal_rec(src_trace, tar_trace)
    self.assertTrue(result, 'Expected traces not to match')

  def test_009_with_print_output(self):
    src_trace, tar_trace = self.get_fixtures('009')
    result = p_rule_applicator.are_traces_equal_rec(src_trace, tar_trace)
    self.assertTrue(result, 'Expected traces not to match')

  def test_010(self):
    src_trace, tar_trace = self.get_fixtures('010')
    result = p_rule_applicator.are_traces_equal_rec(src_trace, tar_trace)
    self.assertFalse(result, 'Expected traces not to match')

  def test_011_float_val(self):
    src_trace, tar_trace = self.get_fixtures('011')
    result = p_rule_applicator.are_traces_equal_rec(src_trace, tar_trace)
    self.assertTrue(result, 'Expected traces not to match')

  def test_012(self):
    src_trace, tar_trace = self.get_fixtures('012')
    result = p_rule_applicator.are_traces_equal_rec(src_trace, tar_trace)
    self.assertFalse(result, 'Expected traces not to match')

  def test_013(self):
    src_trace, tar_trace = self.get_fixtures('013')
    result = p_rule_applicator.are_traces_equal_rec(src_trace, tar_trace)
    self.assertFalse(result, 'Expected traces not to match')

  def test_014(self):
    src_trace, tar_trace = self.get_fixtures('014')
    result = p_rule_applicator.are_traces_equal_rec(src_trace, tar_trace)
    self.assertFalse(result, 'Expected traces not to match')

  def test_015(self):
    src_trace, tar_trace = self.get_fixtures('015')
    result = p_rule_applicator.are_traces_equal_rec(src_trace, tar_trace)
    self.assertFalse(result, 'Expected traces not to match')

  def test_016_indexed_log_statements(self):
    src_trace, tar_trace = self.get_fixtures('016')
    result = p_rule_applicator.are_traces_equal_rec(src_trace, tar_trace)
    self.assertFalse(result, 'Expected traces not to match')


class TestGetErrorLines(unittest.TestCase):
  '''
  Test cases for the _get_error_lines function in p_rule_applicator.
  '''
  def setUp(self):
    self.fixture_dir_path = p_consts.TEST_ARTIFACTS_DIR / 'p-rule-applicator' / 'get-error-lines'

  def get_fixture(self, fixture_id: str) -> str:
    return (self.fixture_dir_path / f'tar_program_instr_{fixture_id}.js').read_text()

  def are_dicts_equal(self, result: dict, gold: dict):
    result_str = json.dumps(result, sort_keys=True)
    gold_str = json.dumps(gold, sort_keys=True)
    print('result_str', result_str)
    print('gold_str  ', gold_str)
    return result_str == gold_str

  def test_001(self):
    tar_program_instr = self.get_fixture('001')

    result = p_rule_applicator._get_error_lines(tar_program_instr, 1)
    gold = {5: '    let n = 0;'}
    self.assertTrue(self.are_dicts_equal(result, gold), 'dicts are not equal')

    result = p_rule_applicator._get_error_lines(tar_program_instr, 2)
    gold = {}
    self.assertTrue(self.are_dicts_equal(result, gold), 'dicts must be empty')

    result = p_rule_applicator._get_error_lines(tar_program_instr, 3)
    gold = {8: '    n = 1;'}
    self.assertTrue(self.are_dicts_equal(result, gold), 'dicts are not equal')

    result = p_rule_applicator._get_error_lines(tar_program_instr, 4)
    gold = {10: '    while (n < 10) {'}
    self.assertTrue(self.are_dicts_equal(result, gold), 'dicts are not equal')

    result = p_rule_applicator._get_error_lines(tar_program_instr, 5)
    gold = {12: "        n += 'n';"}
    self.assertTrue(self.are_dicts_equal(result, gold), 'dicts are not equal')


if __name__ == '__main__':
  unittest.main()
