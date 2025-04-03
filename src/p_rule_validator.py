import json
from pathlib import Path
from typing import List

import d_ast_parse
import d_grammar_expand
import d_grammar_rules
import p_consts
import p_data_structures as pds
import p_rule_postprocessor as prpp
import p_pirel
import p_subject
import p_utils


logger = p_utils.setup_logger(__name__)


def is_valid_translation_rule_syntactic(
  subject: p_subject.PirelSubject,
  translation_rule: str,
  existing_ruleset: str
) -> bool:
  '''
  Check if the provided translation rule:
  1. Has its placeholder mappings correct.
  2. Can translate the problematic node.
  PRE: exising ruleset fails to translate the code
  '''

  p_utils.log_json_time(f'{subject.name}_args-is_valid_translation_rule_syntactic.json', locals())

  def _get_used_translation_rule_ids(dbg_history: List[dict]) -> List[int]:
    used_rule_ids : List[int] = []
    for history_elem in dbg_history:
      dbg_info : dict = history_elem['dbg_info']
      notes : dict = dbg_info['notes']
      rule_id = notes['rule_id']
      used_rule_ids.append(rule_id)
    return used_rule_ids

  def _process_used_rules(rule_ids_before: List[int], rule_ids_after: List[int]) -> bool:
    nonlocal existing_ruleset
    logger.debug(f'rule_ids_before: {rule_ids_before}')
    logger.debug(f'rule_ids_after: {rule_ids_after}')

    # number of rules used after must be strictly greater than number of rules used before
    if len(rule_ids_after) <= len(rule_ids_before):
      logger.warning('Translation rule is BAD: rule_ids_after must strictly be greater than rule_ids_before')
      return False

    # used rule id's before must be identical to the first rule id's after
    for i in range(len(rule_ids_before)):
      if rule_ids_before[i] != rule_ids_after[i]:
        logger.warning(f'Translation rule is BAD: used rules at index {i} are different')
        logger.warning('Should not happen under normal circumstances. More debugging needed.')
        return False

    # id of the first rule used must be of rule under test
    # `rule_ids_before = [3, 10, 4, 5, 6, 0]`
    # `rule_ids_after  = [3, 10, 4, 5, 6, 0, 17, 8, 7]`
    # as in the example above, `17` must be id of the rule under test
    num_rules_before = existing_ruleset.count('match_expand')
    num_rules_after = num_rules_before + 1
    rule_under_test_idx_in_after = len(rule_ids_before)
    rule_under_test_id = num_rules_after - 1
    if rule_under_test_id != rule_ids_after[rule_under_test_idx_in_after]:
      logger.warning('Translation rule is BAD: the last used rule id is not of the rule under test')
      logger.warning('Should not happen under normal circumstances. More debugging needed.')
      return False

    return True

  logger.debug(f'Checking if translation rule is valid:\n{translation_rule}')

  # ~~~ FIRST, CHECK IF THE MAPPINGS IN THE TRANSLATION RULE ARE CORRECT
  expansion_programs, _ = d_grammar_rules.parse_analyze_rules(translation_rule)
  assert len(expansion_programs) == 1, 'should not happen: there must be exactly one translation rule'
  match_pattern, expand_pattern = expansion_programs[0]['match'], expansion_programs[0]['expand']
  try:
    _ = prpp.TranslationRule(match_pattern, expand_pattern)
  except prpp.RuleMappingError as err:
    msg = f'Translation rule is BAD:\n{translation_rule}\nis invalid due to rule mapping error:\n'
    msg += p_utils.exception_to_str(err)
    logger.warning(msg)
    return False

  # ~~~ SECOND, CHECK IF THE TRANSLATION RULE REALLY TRANSLATES THE PROBLEMATIC NODE
  # ~~ get the translation result with the existing ruleset
  dbg_history_before = None
  try:
    _ = p_pirel.duoglot_translate_wrapper(
      subject.src_main_code,
      subject.src_lang,
      subject.tar_lang,
      existing_ruleset,
      subject.auto_backward,
      subject.choices,
      subject_name=subject.name,
      skip_template_extraction=True
    )
  except d_grammar_expand.TranslationRuleNotFoundException as exc:
    logger.debug('Existing ruleset fails to translate as expected')
    # NOTE dbg_history should have been set in duoglot_translate_wrapper
    dbg_history_before = exc.dbg_history
  except:
    logger.error('Translation failed due to some error. Should not happen.')
    raise RuntimeError('Only TranslationRuleNotFoundException is expected')

  # ~~ get the translation result with the existing ruleset + rule under test
  dbg_history_after = None
  try:
    _ = p_pirel.duoglot_translate_wrapper(
      subject.src_main_code,
      subject.src_lang,
      subject.tar_lang,
      existing_ruleset + '\n\n' + translation_rule,
      subject.auto_backward,
      subject.choices,
      subject_name=subject.name,
      skip_template_extraction=True
    )
    # translation rule translated the remaining nodes
    logger.debug('Translation rule is GOOD. It translated the last problematic node.')
    return True
  except d_grammar_expand.TranslationRuleNotFoundException as exc:
    logger.debug('Existing ruleset and the rule under test failed to translate the code')
    # NOTE dbg_history should have been set in duoglot_translate_wrapper
    dbg_history_after = exc.dbg_history
  except:
    logger.debug('Exception other than TranslationRuleNotFoundException occurred')
    logger.debug('Translation rule under test is bad')
    return False

  # there still is a problematic node
  rule_ids_before = _get_used_translation_rule_ids(dbg_history_before)
  rule_ids_after = _get_used_translation_rule_ids(dbg_history_after)

  return _process_used_rules(rule_ids_before, rule_ids_after)


def is_valid_translation_rule_test_based(
  subject: p_subject.PirelSubject,
  translation_rule: str,
  existing_ruleset: str
) -> bool:
  '''
  Entry point for test-based checking if the provided translation rule is valid.
  '''


def collect_paramable_identifiers(
  subject: p_subject.PirelSubject,
  snippet: str
) -> List[str]:
  '''
  Given a snippet of code that is used to test the newly learned translation rule,
  collect all the identifiers that can be parametrized and used as parameters in
  test program.

  LOGIC
  '''
  ast, _ = d_ast_parse.parse_text_dbg(snippet, subject.src_lang, keep_text=False)
  tree = pds.DuoGlotTree(ast)
  return ['a','a']


# INDIVIDUAL RULE VALIDATION USAGE
def _validate_translation_rule_usage():
  ''''''
  # MINIMAL INPUTS REQUIRED:
  # 1. GENERATED SAMPLE
  # 2. TRANSLATION RULE
  config = p_utils.read_tmp_json('_validate_translation_rule_usage_config.json')
  args_dict_fpath = config['args_dict_fpath']
  args_dict = p_utils.read_tmp_json(args_dict_fpath)

  # args to _learn_trans_rules_from_tsp
  tsp = args_dict['tsp']
  template_dict = args_dict['template_dict']
  subject = p_subject.PirelSubject(**json.loads(args_dict['subject']))
  translation_rules = args_dict['translation_rules']

  # checked translation rules
  checked_trules_fpath = config['checked_trules_fpath']
  checked_trules = p_utils.read_tmp_json(checked_trules_fpath)

  # this is the third generated sample that has the same properties as TSPs
  # it will be used to validate the translation rule
  generated_sample = 'id_aqr = 32'

  # the following is the translation rule to be validated
  trule = checked_trules[0]

  print('fin')


# COLLECTING VARIABLES THAT CAN BE USED AS PARAMETERS USAGE
def _collect_variables_that_can_be_used_as_parameters_usage():
  # inputs
  snippet = p_utils.read_tmp_text('L0001_TwoSum.py')
  src_lang = 'py'

  # logic
  parser = p_consts.PARSER_DICT[src_lang]
  tree = parser.parse(bytes(snippet, 'utf8'))
  print()



# TEST HARNESSES
def _test_collect_paramable_identifiers():
  snippet = p_utils.read_tmp_text('L0001_TwoSum.py')
  subject = p_subject.PirelSubject(
    'leetcode',
    'L0001',
    p_utils.read_text(p_consts.ROOT_DIR / Path('benchmarks/leetcode/py/L0001_TwoSum.py')),
    'py',
    'js'
  )
  identifiers = collect_paramable_identifiers(subject, snippet)
  print(identifiers)


if __name__ == '__main__':
  # _validate_translation_rule_usage()
  # _test_collect_paramable_identifiers()
  _collect_variables_that_can_be_used_as_parameters_usage()
