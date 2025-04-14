import unittest

import p_consts
from p_subject import PirelSubject


class TestPirelSubject(unittest.TestCase):
  def create_ctci_subject(self) -> PirelSubject:
    return PirelSubject(
      benchmark_name='ctci',
      name='test_init_ctci',
      src_program='print()',
      src_lang='py',
      tar_lang='js'
    )

  def test_init_ctci(self):
    subject = self.create_ctci_subject()
    self.assertEqual(subject.benchmark_name, 'ctci')
    self.assertEqual(subject.name, 'test_init_ctci')
    self.assertEqual(subject.src_program, 'print()')
    self.assertEqual(subject.src_lang, 'py')
    self.assertEqual(subject.tar_lang, 'js')

    # by default, trans.rules for main code are None
    self.assertEqual(subject.translation_rules_main_code, None)
    self.assertEqual(subject.translation_rules_test_code, None)
    self.assertEqual(subject.translation_rules_instr_src, None)
    self.assertEqual(subject.translation_rules_instr_tar, None)

    self.assertEqual(subject.is_three_split, p_consts.BENCHMARK_CONFIGS['ctci']['is_three_split'])
    self.assertEqual(subject.is_mylog_inserted, p_consts.BENCHMARK_CONFIGS['ctci']['is_mylog_inserted'])
    self.assertEqual(subject.needs_instrumentation, p_consts.BENCHMARK_CONFIGS['ctci']['needs_instrumentation'])

    self.assertFalse(subject.is_long_requires_processing)

    self.assertEqual(subject.src_test_code, None)
    self.assertEqual(subject.src_main_code, subject.src_program)
    self.assertEqual(subject.src_test_call_code, None)

  def test_to_json_str(self):
    subject = PirelSubject(
      benchmark_name='ctci',
      name='test_init_ctci',
      src_program='print()',
      src_lang='py',
      tar_lang='js'
    )
    json_str = subject.to_json_str()
    expected_json_str = '''{"auto_backward": true, "benchmark_name": "ctci", "choices": {"choices_list": [], "type": "ASTNODE"}, "is_long_requires_processing": false, "is_mylog_inserted": false, "is_three_split": false, "name": "test_init_ctci", "needs_instrumentation": false, "src_lang": "py", "src_main_code": "print()", "src_program": "print()", "src_test_call_code": null, "src_test_code": null, "tar_lang": "js", "translation_rules_instr_src": null, "translation_rules_instr_tar": null, "translation_rules_main_code": null, "translation_rules_test_code": null}'''
    self.assertEqual(json_str, expected_json_str)

  def test_from_json_str(self):
    subject = self.create_ctci_subject()
    json_str = subject.to_json_str()
    new_subject = PirelSubject.from_json_str(json_str)

    self.assertEqual(new_subject.benchmark_name, subject.benchmark_name)
    self.assertEqual(new_subject.name, subject.name)
    self.assertEqual(new_subject.src_program, subject.src_program)
    self.assertEqual(new_subject.src_lang, subject.src_lang)
    self.assertEqual(new_subject.tar_lang, subject.tar_lang)

    self.assertEqual(new_subject.auto_backward, subject.auto_backward)
    self.assertEqual(new_subject.choices, subject.choices)

    self.assertEqual(new_subject.translation_rules_main_code, subject.translation_rules_main_code)
    self.assertEqual(new_subject.translation_rules_test_code, subject.translation_rules_test_code)
    self.assertEqual(new_subject.translation_rules_instr_src, subject.translation_rules_instr_src)
    self.assertEqual(new_subject.translation_rules_instr_tar, subject.translation_rules_instr_tar)

    self.assertEqual(new_subject.is_three_split, subject.is_three_split)
    self.assertEqual(new_subject.is_mylog_inserted, subject.is_mylog_inserted)
    self.assertEqual(new_subject.needs_instrumentation, subject.needs_instrumentation)

    self.assertEqual(new_subject.is_long_requires_processing, subject.is_long_requires_processing)
    self.assertEqual(new_subject.src_test_code, subject.src_test_code)
    self.assertEqual(new_subject.src_main_code, subject.src_main_code)
    self.assertEqual(new_subject.src_test_call_code, subject.src_test_call_code)

if __name__ == '__main__':
  unittest.main()
