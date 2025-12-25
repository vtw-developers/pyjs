import asyncio
import json
import unittest
from typing import List, Tuple

import p_consts
import p_code_runner
import p_rule_applicator as prapp
import p_subject
import p_utils


class TestApplyTranslationRules(unittest.TestCase):
  '''
  Test cases for apply_translation_rules function in p_rule_applicator.py
  '''
  def setUp(self):
    self.maxDiff = None
    self.fixture_dir_path = p_consts.TEST_ARTIFACTS_DIR / 'p-rule-applicator' / 'apply-translation-rules'
    self.error_subdirs = sorted([
      d for d in self.fixture_dir_path.iterdir() if d.is_dir() and d.name != 'no-error'
    ])

  def get_args(self, subdir: str, test_id: str) -> Tuple[p_subject.PirelSubject, bool]:
    args_dict = p_utils.read_json(self.fixture_dir_path / subdir / f'{test_id}_in_args.json')
    src_program = p_utils.read_text(self.fixture_dir_path / subdir / f'{test_id}_in_src_program.py')
    translation_rules_main_code = p_utils.read_text(self.fixture_dir_path / subdir / f'{test_id}_in_translation_rules_main_code.snart')

    # arg 1
    subject = p_subject.PirelSubject(
      benchmark_name=args_dict['subject']['benchmark_name'],
      name=args_dict['subject']['name'],
      src_program=src_program,
      src_lang=args_dict['subject']['src_lang'],
      tar_lang=args_dict['subject']['tar_lang'],
      is_three_split=args_dict['subject']['is_three_split']
    )
    subject.translation_rules_main_code = translation_rules_main_code
    subject.translation_rules_test_code = args_dict['subject']['translation_rules_test_code']
    subject.is_three_split = args_dict['subject']['is_three_split']
    subject.choices = args_dict['subject']['choices']
    subject.verified_choice_options = args_dict['subject']['verified_choice_options']

    # arg 2
    raise_on_missing_vrf_rule = args_dict['raise_on_missing_vrf_rule']
    return subject, raise_on_missing_vrf_rule

  def get_result_no_error(self, test_id: str) -> Tuple[str, list]:
    tar_program_plausible = p_utils.read_text(self.fixture_dir_path / 'no-error' / f'{test_id}_out_tar_program_plausible.js')
    translate_dbg_history = p_utils.read_json(self.fixture_dir_path / 'no-error' / f'{test_id}_out_translate_dbg_history.json')
    return tar_program_plausible, translate_dbg_history

  def get_result_error(self, subdir: str, test_id: str) -> Tuple[str, str]:
    error_data = p_utils.read_json(self.fixture_dir_path / subdir / f'{test_id}_out_error.json')
    return error_data['error'], error_data['error_msg']

  def get_test_ids(self, subdir: str) -> List[str]:
    test_inputs = (self.fixture_dir_path / subdir).glob(f'*_in_args.json')
    test_ids = sorted([fpath.stem[:3] for fpath in test_inputs])
    return test_ids

  def test_no_error(self):
    subdir = 'no-error'
    test_ids = self.get_test_ids(subdir)
    for test_id in test_ids:
      with self.subTest(test_id=test_id):
        subject, raise_on_missing_vrf_rule = self.get_args(subdir, test_id)
        ref_tar_program_plausible, ref_translate_dbg_history = self.get_result_no_error(test_id)
        tar_program_plausible, translate_dbg_history = asyncio.run(prapp.apply_translation_rules(
          subject,
          raise_on_missing_vrf_rule
        ))
        self.assertEqual(tar_program_plausible, ref_tar_program_plausible, 'tar_program_plausible does not match')
        eq, p, v1, v2 = p_utils.deep_json_diff(
          translate_dbg_history,
          ref_translate_dbg_history,
          coerce_types=True,
        )
        self.assertTrue(eq, f'translate_dbg_history does not match: {p}\n{v1}\n{v2}')

  def test_all_error(self):
    for err_subdir in self.error_subdirs:
      test_ids = self.get_test_ids(err_subdir.name)
      for test_id in test_ids:
        with self.subTest(subdir=err_subdir.name, test_id=test_id):
          subject, raise_on_missing_vrf_rule = self.get_args(err_subdir.name, test_id)
          ref_error, ref_error_msg = self.get_result_error(err_subdir.name, test_id)
          error, error_msg = '', ''
          try:
            _ = asyncio.run(prapp.apply_translation_rules(
              subject,
              raise_on_missing_vrf_rule
            ))
          except Exception as e:
            error = e.__class__.__name__
            error_msg = str(e)
          self.assertEqual(error_msg, ref_error_msg, 'error message does not match')
          self.assertEqual(error, ref_error, 'error type does not match')


class TestMyExactlogSerialize(unittest.TestCase):
  '''
  Test cases for serialize() in mylog_pirel.py and mylog_pirel.js
  '''
  def setUp(self):
    self.fixture_dir_path = p_consts.TEST_ARTIFACTS_DIR / 'p-rule-applicator' / 'myexactlog-serialize'

  def get_fixture(self, test_id: str) -> Tuple[str, str]:
    src_program_instr = (self.fixture_dir_path / f'{test_id}.py').read_text()
    tar_program_instr = (self.fixture_dir_path / f'{test_id}.js').read_text()
    return src_program_instr, tar_program_instr

  def test_all(self):
    '''
    If prapp._run_tests runs without errors, it means that the serialized traces match.
    If the serializer functions produce inconsistent outputs, the traces will not match,
    and it will result in test failure.
    '''
    test_inputs = self.fixture_dir_path.glob('*.py')
    test_ids = sorted([fpath.stem for fpath in test_inputs])
    subject = type('PirelSubject', (), {
      'src_lang': 'py', 'tar_lang': 'js', 'name': 'myexactlog-serialize'
    })()
    for test_id in test_ids:
      with self.subTest(test_id=test_id):
        src_program_instr, tar_program_instr = self.get_fixture(test_id)
        asyncio.run(prapp._run_tests(src_program_instr, tar_program_instr, subject))


class TestCompareTraces(unittest.TestCase):
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
    result = prapp.are_traces_equal_rec(src_trace, tar_trace)
    self.assertFalse(result, 'Expected traces not to match')

  def test_002(self):
    src_trace, tar_trace = self.get_fixtures('002')
    result = prapp.are_traces_equal_rec(src_trace, tar_trace)
    self.assertTrue(result, 'Expected traces not to match')

  def test_003(self):
    src_trace, tar_trace = self.get_fixtures('003')
    result = prapp.are_traces_equal_rec(src_trace, tar_trace)
    self.assertFalse(result, 'Expected traces not to match')

  def test_004(self):
    src_trace, tar_trace = self.get_fixtures('004')
    result = prapp.are_traces_equal_rec(src_trace, tar_trace)
    self.assertFalse(result, 'Expected traces not to match')

  def test_005(self):
    src_trace, tar_trace = self.get_fixtures('005')
    result = prapp.are_traces_equal_rec(src_trace, tar_trace)
    self.assertTrue(result, 'Expected traces not to match')

  def test_006_very_large(self):
    src_trace, tar_trace = self.get_fixtures('006')
    result = prapp.are_traces_equal_rec(src_trace, tar_trace)
    self.assertTrue(result, 'Expected traces not to match')

  def test_007(self):
    src_trace, tar_trace = self.get_fixtures('007')
    result = prapp.are_traces_equal_rec(src_trace, tar_trace)
    self.assertTrue(result, 'Expected traces not to match')

  def test_008(self):
    src_trace, tar_trace = self.get_fixtures('008')
    result = prapp.are_traces_equal_rec(src_trace, tar_trace)
    self.assertTrue(result, 'Expected traces not to match')

  def test_009_with_print_output(self):
    src_trace, tar_trace = self.get_fixtures('009')
    result = prapp.are_traces_equal_rec(src_trace, tar_trace)
    self.assertTrue(result, 'Expected traces not to match')

  def test_010(self):
    src_trace, tar_trace = self.get_fixtures('010')
    result = prapp.are_traces_equal_rec(src_trace, tar_trace)
    self.assertFalse(result, 'Expected traces not to match')

  def test_011_float_val(self):
    src_trace, tar_trace = self.get_fixtures('011')
    result = prapp.are_traces_equal_rec(src_trace, tar_trace)
    self.assertTrue(result, 'Expected traces not to match')

  def test_012(self):
    src_trace, tar_trace = self.get_fixtures('012')
    result = prapp.are_traces_equal_rec(src_trace, tar_trace)
    self.assertFalse(result, 'Expected traces not to match')

  def test_013(self):
    src_trace, tar_trace = self.get_fixtures('013')
    result = prapp.are_traces_equal_rec(src_trace, tar_trace)
    self.assertFalse(result, 'Expected traces not to match')

  def test_014(self):
    src_trace, tar_trace = self.get_fixtures('014')
    result = prapp.are_traces_equal_rec(src_trace, tar_trace)
    self.assertFalse(result, 'Expected traces not to match')

  def test_015(self):
    src_trace, tar_trace = self.get_fixtures('015')
    result = prapp.are_traces_equal_rec(src_trace, tar_trace)
    self.assertFalse(result, 'Expected traces not to match')

  def test_016_indexed_log_statements(self):
    src_trace, tar_trace = self.get_fixtures('016')
    result = prapp.are_traces_equal_rec(src_trace, tar_trace)
    self.assertFalse(result, 'Expected traces not to match')


class TestGetErrorLines(unittest.TestCase):
  '''
  Test cases for the _get_error_lines function in prapp.
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

    result = prapp._get_error_lines(tar_program_instr, 1)
    gold = {
      5: '    let n = 0;'
    }
    self.assertTrue(self.are_dicts_equal(result, gold), 'dicts are not equal')

    result = prapp._get_error_lines(tar_program_instr, 2)
    gold = {

    }
    self.assertTrue(self.are_dicts_equal(result, gold), 'dicts are not equal')

    result = prapp._get_error_lines(tar_program_instr, 3)
    gold = {
      8: '    n = 1;'
    }
    self.assertTrue(self.are_dicts_equal(result, gold), 'dicts are not equal')

    result = prapp._get_error_lines(tar_program_instr, 4)
    gold = {
      10: '    while (n < 10) {'
    }
    self.assertTrue(self.are_dicts_equal(result, gold), 'dicts are not equal')

    result = prapp._get_error_lines(tar_program_instr, 5)
    gold = {
      12: "        n += 'n';"
    }
    self.assertTrue(self.are_dicts_equal(result, gold), 'dicts are not equal')

  def test_002_log_stat_before_return_stat(self):
    tar_program_instr = self.get_fixture('002')

    result = prapp._get_error_lines(tar_program_instr, 1)
    gold = {
      14: '  return 2 / 2;'
    }
    self.assertTrue(self.are_dicts_equal(result, gold), 'the error line is 3 with return statement')

  def test_003(self):
    tar_program_instr = self.get_fixture('003')

    result = prapp._get_error_lines(tar_program_instr, 1)
    gold = {
      22: '    var count = 0;'
    }
    self.assertTrue(self.are_dicts_equal(result, gold), 'between f_gold and log_statement')

    result = prapp._get_error_lines(tar_program_instr, 2)
    gold = {
      24: '    var ans = 1;'
    }
    self.assertTrue(self.are_dicts_equal(result, gold), 'between two log statements')

    result = prapp._get_error_lines(tar_program_instr, 3)
    gold = {
      26: '    while (n % 2 === 0) {'
    }
    self.assertTrue(self.are_dicts_equal(result, gold), 'between two log statements')

    result = prapp._get_error_lines(tar_program_instr, 4)
    gold = {
      28: '        var count = count + 1;'
    }
    self.assertTrue(self.are_dicts_equal(result, gold), 'between two log statements')

    result = prapp._get_error_lines(tar_program_instr, 5)
    gold = {
      30: '        var n = Math.floor(n / 2);'
    }
    self.assertTrue(self.are_dicts_equal(result, gold), 'between two log statements')

    result = prapp._get_error_lines(tar_program_instr, 6)
    gold = {
      33: '    if (count % 2 !== 0) {'
    }
    self.assertTrue(self.are_dicts_equal(result, gold), 'consecutive compound statements')

    result = prapp._get_error_lines(tar_program_instr, 7)
    gold = {
      35: '        var ans = ans * 2;'
    }
    self.assertTrue(self.are_dicts_equal(result, gold), 'between two log statements')

    result = prapp._get_error_lines(tar_program_instr, 8)
    gold = {
      38: '    for (var i = 3; i <= Math.floor(Math.sqrt(n)); i += 2) {'
    }
    self.assertTrue(self.are_dicts_equal(result, gold), 'consecutive compound statements')

    result = prapp._get_error_lines(tar_program_instr, 9)
    gold = {
      40: '        var count = 0;'
    }
    self.assertTrue(self.are_dicts_equal(result, gold), 'between two log statements')

    result = prapp._get_error_lines(tar_program_instr, 10)
    gold = {
      42: '        while (n % i === 0) {'
    }
    self.assertTrue(self.are_dicts_equal(result, gold), 'between two log statements')

    result = prapp._get_error_lines(tar_program_instr, 11)
    gold = {
      44: '            var count = count + 1;'
    }
    self.assertTrue(self.are_dicts_equal(result, gold), 'between two log statements')

    result = prapp._get_error_lines(tar_program_instr, 12)
    gold = {
      46: '            var n = Math.floor(n / i);'
    }
    self.assertTrue(self.are_dicts_equal(result, gold), 'between two log statements')

    result = prapp._get_error_lines(tar_program_instr, 13)
    gold = {
      49: '        if (count % 2 !== 0) {'
    }
    self.assertTrue(self.are_dicts_equal(result, gold), 'consecutive compound statements')

    result = prapp._get_error_lines(tar_program_instr, 14)
    gold = {
      51: '            var ans = ans * i;'
    }
    self.assertTrue(self.are_dicts_equal(result, gold), 'between two log statements')

    result = prapp._get_error_lines(tar_program_instr, 15)
    gold = {
      55: '    if (n > 2) {'
    }
    self.assertTrue(self.are_dicts_equal(result, gold), 'consecutive compound statements')

    result = prapp._get_error_lines(tar_program_instr, 16)
    gold = {
      57: '        var ans = ans * n;'
    }
    self.assertTrue(self.are_dicts_equal(result, gold), 'between two log statements')

    result = prapp._get_error_lines(tar_program_instr, 17)
    gold = {
      61: '    return ans;'
    }
    self.assertTrue(self.are_dicts_equal(result, gold), 'return statement')

  def test_003_second_of_consecutive_compound_statements(self):
   tar_program_instr = self.get_fixture('003')

   result = prapp._get_error_lines(tar_program_instr, 15)
   gold = {
     55: '    if (n > 2) {'
   }
   self.assertTrue(self.are_dicts_equal(result, gold), 'the error line is 15 with second of consecutive compound statements')


if __name__ == '__main__':
  unittest.main()
