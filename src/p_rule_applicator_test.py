import unittest
from typing import Tuple

import p_consts
import p_code_runner
import p_rule_applicator


class TestCompareTraces(unittest.TestCase):
  '''
  Test cases for the _compare_traces function in p_rule_applicator.
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
    result = p_rule_applicator._compare_traces(src_trace, tar_trace)
    self.assertFalse(result, 'Expected traces not to match')

  def test_002(self):
    src_trace, tar_trace = self.get_fixtures('002')
    result = p_rule_applicator._compare_traces(src_trace, tar_trace)
    self.assertTrue(result, 'Expected traces not to match')

  def test_003(self):
    src_trace, tar_trace = self.get_fixtures('003')
    result = p_rule_applicator._compare_traces(src_trace, tar_trace)
    self.assertFalse(result, 'Expected traces not to match')

  def test_004(self):
    src_trace, tar_trace = self.get_fixtures('004')
    result = p_rule_applicator._compare_traces(src_trace, tar_trace)
    self.assertFalse(result, 'Expected traces not to match')

  def test_005(self):
    src_trace, tar_trace = self.get_fixtures('005')
    result = p_rule_applicator._compare_traces(src_trace, tar_trace)
    self.assertTrue(result, 'Expected traces not to match')

  def test_006_very_large(self):
    src_trace, tar_trace = self.get_fixtures('006')
    result = p_rule_applicator._compare_traces(src_trace, tar_trace)
    self.assertTrue(result, 'Expected traces not to match')

  def test_007(self):
    src_trace, tar_trace = self.get_fixtures('007')
    result = p_rule_applicator._compare_traces(src_trace, tar_trace)
    self.assertTrue(result, 'Expected traces not to match')

  def test_008(self):
    src_trace, tar_trace = self.get_fixtures('008')
    result = p_rule_applicator._compare_traces(src_trace, tar_trace)
    self.assertTrue(result, 'Expected traces not to match')

  def test_009_with_print_output(self):
    src_trace, tar_trace = self.get_fixtures('009')
    result = p_rule_applicator._compare_traces(src_trace, tar_trace)
    self.assertTrue(result, 'Expected traces not to match')

  def test_010(self):
    src_trace, tar_trace = self.get_fixtures('010')
    result = p_rule_applicator._compare_traces(src_trace, tar_trace)
    self.assertFalse(result, 'Expected traces not to match')

  def test_011_float_val(self):
    src_trace, tar_trace = self.get_fixtures('011')
    result = p_rule_applicator._compare_traces(src_trace, tar_trace)
    self.assertTrue(result, 'Expected traces not to match')

  def test_012(self):
    src_trace, tar_trace = self.get_fixtures('012')
    result = p_rule_applicator._compare_traces(src_trace, tar_trace)
    self.assertFalse(result, 'Expected traces not to match')

  def test_013(self):
    src_trace, tar_trace = self.get_fixtures('013')
    result = p_rule_applicator._compare_traces(src_trace, tar_trace)
    self.assertFalse(result, 'Expected traces not to match')

  def test_014(self):
    src_trace, tar_trace = self.get_fixtures('014')
    result = p_rule_applicator._compare_traces(src_trace, tar_trace)
    self.assertFalse(result, 'Expected traces not to match')

  def test_015(self):
    src_trace, tar_trace = self.get_fixtures('015')
    result = p_rule_applicator._compare_traces(src_trace, tar_trace)
    self.assertFalse(result, 'Expected traces not to match')


if __name__ == '__main__':
  unittest.main()
