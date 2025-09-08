import unittest

import p_consts
import p_subject


class TestPirelSubject(unittest.TestCase):
  def setUp(self):
    self.maxDiff = None

  def get_three_split_program(self):
    src_program = '''
def test():
  pass
"-----------------"
def f_gold():
  pass
"-----------------"
test()
'''.strip()
    return src_program

  def create_gfg_subject(self) -> p_subject.PirelSubject:
    src_program = self.get_three_split_program()
    return p_subject.PirelSubject(
      benchmark_name='gfg',
      name='test_init_gfg',
      src_program=src_program,
      src_lang='py',
      tar_lang='js',
      is_three_split=True,
    )

  def test_init_gfg(self):
    src_program = self.get_three_split_program()
    subject = self.create_gfg_subject()
    self.assertEqual(subject.benchmark_name, 'gfg')
    self.assertEqual(subject.name, 'test_init_gfg')
    self.assertEqual(subject.src_program, src_program)
    self.assertEqual(subject.src_lang, 'py')
    self.assertEqual(subject.tar_lang, 'js')

    # by default, trans.rules for main code are None
    self.assertEqual(subject.translation_rules_main_code, None)
    self.assertTrue(subject.translation_rules_test_code is not None)

    self.assertEqual(subject.is_three_split, True)
    self.assertEqual(subject.get_src_test_code(), 'def test():\n  pass')
    self.assertEqual(subject.get_src_main_code(), 'def f_gold():\n  pass')
    self.assertEqual(subject.get_src_test_call_code(), 'test()')

  def test_to_json_str(self):
    subject = p_subject.PirelSubject(
      benchmark_name='custom',
      name='test_init_custom',
      src_program='print()',
      src_lang='py',
      tar_lang='js',
      is_three_split=False,
    )
    json_str = subject.to_json_str()
    expected_json_str = '''{"auto_backward": true, "benchmark_name": "custom", "choices": {"choices_list": [], "type": "ASTNODE"}, "is_three_split": false, "name": "test_init_custom", "readonly_choices_list": [], "src_lang": "py", "src_program": "print()", "tar_lang": "js", "translation_rules_main_code": null, "translation_rules_test_code": null}'''
    self.assertEqual(json_str, expected_json_str)

  def test_from_json_str(self):
    subject = self.create_gfg_subject()
    json_str = subject.to_json_str()
    new_subject = p_subject.PirelSubject.from_json_str(json_str)

    self.assertEqual(new_subject.benchmark_name, subject.benchmark_name)
    self.assertEqual(new_subject.name, subject.name)
    self.assertEqual(new_subject.src_program, subject.src_program)
    self.assertEqual(new_subject.src_lang, subject.src_lang)
    self.assertEqual(new_subject.tar_lang, subject.tar_lang)

    self.assertEqual(new_subject.auto_backward, subject.auto_backward)
    self.assertEqual(new_subject.choices, subject.choices)

    self.assertEqual(new_subject.translation_rules_main_code, subject.translation_rules_main_code)
    self.assertEqual(new_subject.translation_rules_test_code, subject.translation_rules_test_code)

    self.assertEqual(new_subject.is_three_split, subject.is_three_split)

    self.assertEqual(new_subject.get_src_test_code(), subject.get_src_test_code())
    self.assertEqual(new_subject.get_src_main_code(), subject.get_src_main_code())
    self.assertEqual(new_subject.get_src_test_call_code(), subject.get_src_test_call_code())

  def test_split_then_combine(self):
    subject = self.create_gfg_subject()
    test_code = subject.get_src_test_code()
    main_code = subject.get_src_main_code()
    test_call_code = subject.get_src_test_call_code()

    if subject.is_three_split:
      recombined_program = f'\n{p_consts.TEST_MAIN_CALL_DELIMITER}\n'.join([test_code, main_code, test_call_code])
    else:
      recombined_program = main_code

    self.assertEqual(recombined_program.strip(), subject.src_program.strip())

if __name__ == '__main__':
  unittest.main()
