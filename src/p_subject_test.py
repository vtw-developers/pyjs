import unittest

import p_consts
from p_subject import PirelSubject


class TestPirelSubject(unittest.TestCase):
  def test_init_ctci(self):
    subject = PirelSubject(
      benchmark_name='ctci',
      name='test_init_ctci',
      src_program='print()',
      src_lang='py',
      tar_lang='js'
    )
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


if __name__ == '__main__':
  unittest.main()
