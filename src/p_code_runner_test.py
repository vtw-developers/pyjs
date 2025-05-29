import json
import unittest
from typing import Tuple

import p_code_runner
import p_consts
import p_utils


class TestExtractTraceFromStdout(unittest.TestCase):
  '''
  Test cases for the _extract_trace_from_stdout function in p_code_runner.
  '''
  def setUp(self):
    self.fixture_dir_path = p_consts.TEST_ARTIFACTS_DIR / 'p-code-runner' / 'extract-trace-from-stdout'

  def get_fixtures(self, fixture_id: str) -> Tuple[str, list]:
    stdout = (self.fixture_dir_path / f'stdout-{fixture_id}.txt').read_text()
    trace = p_utils.read_json(self.fixture_dir_path / f'trace-{fixture_id}.json')
    return stdout, trace

  def test_001(self):
    stdout, trace_gold = self.get_fixtures('001')
    trace = p_code_runner._extract_trace_from_stdout(stdout)
    trace_gold_str = json.dumps(trace_gold)
    trace_str = json.dumps(trace)
    self.assertEqual(trace_gold_str, trace_str, 'Expected traces to match')

  def test_002(self):
    stdout, trace_gold = self.get_fixtures('002')
    trace = p_code_runner._extract_trace_from_stdout(stdout)
    trace_gold_str = json.dumps(trace_gold)
    trace_str = json.dumps(trace)
    self.assertEqual(trace_gold_str, trace_str, 'Expected traces to match')

  def test_003(self):
    stdout, trace_gold = self.get_fixtures('003')
    trace = p_code_runner._extract_trace_from_stdout(stdout)
    trace_gold_str = json.dumps(trace_gold)
    trace_str = json.dumps(trace)
    self.assertEqual(trace_gold_str, trace_str, 'Expected traces to match')

  def test_004(self):
    stdout, trace_gold = self.get_fixtures('004')
    trace = p_code_runner._extract_trace_from_stdout(stdout)
    trace_gold_str = json.dumps(trace_gold)
    trace_str = json.dumps(trace)
    self.assertEqual(trace_gold_str, trace_str, 'Expected traces to match')

  def test_005(self):
    stdout, trace_gold = self.get_fixtures('005')
    trace = p_code_runner._extract_trace_from_stdout(stdout)
    trace_gold_str = json.dumps(trace_gold)
    trace_str = json.dumps(trace)
    self.assertEqual(trace_gold_str, trace_str, 'Expected traces to match')

  def test_006(self):
    stdout, trace_gold = self.get_fixtures('006')
    trace = p_code_runner._extract_trace_from_stdout(stdout)
    trace_gold_str = json.dumps(trace_gold)
    trace_str = json.dumps(trace)
    self.assertEqual(trace_gold_str, trace_str, 'Expected traces to match')

  def test_007(self):
    stdout, trace_gold = self.get_fixtures('007')
    trace = p_code_runner._extract_trace_from_stdout(stdout)
    trace_gold_str = json.dumps(trace_gold)
    trace_str = json.dumps(trace)
    self.assertEqual(trace_gold_str, trace_str, 'Expected traces to match')

  def test_008(self):
    stdout, trace_gold = self.get_fixtures('008')
    trace = p_code_runner._extract_trace_from_stdout(stdout)
    trace_gold_str = json.dumps(trace_gold)
    trace_str = json.dumps(trace)
    self.assertEqual(trace_gold_str, trace_str, 'Expected traces to match')

  def test_009(self):
    stdout, trace_gold = self.get_fixtures('009')
    trace = p_code_runner._extract_trace_from_stdout(stdout)
    trace_gold_str = json.dumps(trace_gold)
    trace_str = json.dumps(trace)
    self.assertEqual(trace_gold_str, trace_str, 'Expected traces to match')

  def test_010(self):
    stdout, trace_gold = self.get_fixtures('010')
    trace = p_code_runner._extract_trace_from_stdout(stdout)
    trace_gold_str = json.dumps(trace_gold)
    trace_str = json.dumps(trace)
    self.assertEqual(trace_gold_str, trace_str, 'Expected traces to match')

  def test_011(self):
    stdout, trace_gold = self.get_fixtures('011')
    trace = p_code_runner._extract_trace_from_stdout(stdout)
    trace_gold_str = json.dumps(trace_gold)
    trace_str = json.dumps(trace)
    self.assertEqual(trace_gold_str, trace_str, 'Expected traces to match')

  def test_012(self):
    stdout, trace_gold = self.get_fixtures('012')
    trace = p_code_runner._extract_trace_from_stdout(stdout)
    trace_gold_str = json.dumps(trace_gold)
    trace_str = json.dumps(trace)
    self.assertEqual(trace_gold_str, trace_str, 'Expected traces to match')

  def test_013(self):
    stdout, trace_gold = self.get_fixtures('013')
    trace = p_code_runner._extract_trace_from_stdout(stdout)
    trace_gold_str = json.dumps(trace_gold)
    trace_str = json.dumps(trace)
    self.assertEqual(trace_gold_str, trace_str, 'Expected traces to match')


if __name__ == '__main__':
  unittest.main()
