import asyncio
from typing import Tuple, Optional

import p_pirel
import p_learn_apply_rules
import p_utils
import p_consts
import p_ruleset
import p_subject
import p_rule_applicator
import p_config


def _deinstrument_target_code(tar_code: str) -> str:
  '''
  Remove any instrumentation code added during the translation process.
  '''
  clean_lines = [line for line in tar_code.splitlines()
                 if not line.lstrip().startswith('myexactlog(')]
  return '\n'.join(clean_lines)


def translate(
  python_code: str,
  translation_rules: str,
  llm_api_url: Optional[str],  # falls back to _DEFAULT_API_URL in p_llm_gen.query_llm_qwen_vtw()
  llm_model: Optional[str],  # falls back to _DEFAULT_MODEL in p_llm_gen.query_llm_qwen_vtw()
  llm_temperature: Optional[float],  # falls back to _DEFAULT_TEMPERATURE in p_llm_gen.query_llm_qwen_vtw()
) -> Tuple[
  bool,           # success
  Optional[str],  # translated_code
  str,            # translation_rules_updated
  Optional[str],  # error_message
]:
  '''
  NOTE python_code must include executed statements, e.g. a function call at the end.
       This will not work:
       ```py
       def add(a, b):
           return a + b
       ```
       This will work:
       ```py
       def add(a, b):
           return a + b
       add(2, 3)
       ```
       This will work:
       ```py
       a = 1
       ```
       Executed statements are needed for Execution Order Translation (EOT) to work properly.
  '''

  # some defaults that can be used as parameters later
  benchmark_name = 'n/a'   # used during experiments for publication, can be ignored
  subject_name = 'pyprog'  # can be any string that describes `python_code`
  src_lang = 'py'
  tar_lang = 'js'
  is_three_split = False   # True only for cases such as
                           # benchmarks/gfg/py/G0001_ADD_1_TO_A_GIVEN_NUMBER.py
                           # i.e. programs must have a specific structure
                           # with a test function, f_gold function, and a call to test().
                           # For general translation tasks, this should be False.

  # set LLM configs
  p_config.Config.llm_api_url = llm_api_url
  p_config.Config.llm_model = llm_model
  p_config.Config.llm_temperature = llm_temperature

  python_code = p_utils.remove_comments_and_docstrings_py(python_code)
  subject = p_subject.PirelSubject(benchmark_name=benchmark_name,
                                   name=subject_name,
                                   src_program=python_code,
                                   src_lang=src_lang,
                                   tar_lang=tar_lang,
                                   is_three_split=is_three_split)

  starting_ruleset = p_ruleset.Ruleset.from_starting_ruleset(translation_rules)

  try:
    # writes new rules to starting_ruleset
    asyncio.run(p_pirel.learn_trans_rules_for_subject(subject, starting_ruleset))
  except Exception as e:
    return (False,
            None,
            starting_ruleset.to_str_ruleset(),
            'Error during learn phase: ' + str(e))

  apply_subject = p_learn_apply_rules._create_subject_for_apply_phase(subject,
                                                                      starting_ruleset)

  try:
    tar_program_plausible, translate_dbg_history = \
      asyncio.run(p_rule_applicator.apply_translation_rules(apply_subject))
  except Exception as e:
    return (False,
            None,
            starting_ruleset.to_str_ruleset(),
            'Error during apply phase: ' + str(e))
  else:
    return (True,
            _deinstrument_target_code(tar_program_plausible),
            starting_ruleset.to_str_ruleset(),
            None)


def example_usage():
  '''
  Refer to docs in translate() for requirements on python_code.
  '''

  python_code_good_1 = '''
def add(a, b):
    return a + b
add(2, 3)
'''.strip()
  python_code_good_2 = '''
a = 1
'''.strip()
  python_code_bad_1 = '''
def add(a, b):
    return a + b
'''.strip()
  
  translation_rules = p_utils.read_text(p_consts.STARTING_RULESET_FPATH)
  llm_api_url = None  # 'http://localhost:11434/v1/chat/completions'
  llm_model = None  # 'Qwen/Qwen3-Coder-30B-A3B-Instruct'
  llm_temperature = None  # 0.0

  success, translated_code, updated_rules, error_message = translate(
    python_code=python_code_good_1,
    translation_rules=translation_rules,
    llm_api_url=llm_api_url,
    llm_model=llm_model,
    llm_temperature=llm_temperature,
  )

  if success:
    print('Translated code:')
    print(translated_code)
    print('Updated translation rules:')
    print(updated_rules)
  else:
    print('Translation failed with error message:')
    print(error_message)


if __name__ == '__main__':
  example_usage()
