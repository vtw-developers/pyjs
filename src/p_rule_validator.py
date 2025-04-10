from typing import List

import d_grammar_expand
import d_grammar_rules
import p_consts
import p_pirel
import p_pynguin
import p_rule_applicator as prapp
import p_rule_postprocessor as prpp
import p_subject
import p_utils
import p_visitor_py as pvpy


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
  snippet_under_test: str,
  trule_under_test: str,
  existing_ruleset: str
) -> bool:
  '''
  Entry point for test-based checking if the provided translation rule is valid.
  '''
  logger.debug('starting is_valid_translation_rule_test_based')
  logger.debug(f'snippet_under_test:\n{snippet_under_test}')
  logger.debug(f'trule_under_test:\n{trule_under_test}')

  src_parser = p_consts.PARSER_DICT[subject.src_lang]
  log_statement_rule = p_utils.read_text(p_consts.LOG_STAT_RULE_FPATH)
  pirel_subject_snippet_conf : dict = p_utils.read_yaml(p_consts.SNIPPET_UNDER_TEST_CONF_FPATH)

  # 1. extract parametrizable identifiers from the snippet
  _ts_tree = src_parser.parse(bytes(snippet_under_test, 'utf-8'))
  _tree = pvpy.Tree.from_ts_tree(_ts_tree)
  _param_collector = pvpy.ParametrizableVariablesCollector()
  _param_collector.visit(_tree.root_node)
  _parametrizable_identifiers = _param_collector.get_parametrizable_identifiers()
  logger.debug(f'parametrizable identifiers: {_parametrizable_identifiers}')

  if len(_parametrizable_identifiers) == 0:
    logger.warning('No parametrizable identifiers found. Cannot generate tests.')
    return False

  # 2. prepare f_gold() function
  _params = ', '.join(_parametrizable_identifiers)
  _indented_snippet_block = p_utils.indent(snippet_under_test, 4)
  _f_gold_fn_str = p_consts.F_GOLD_SNIPPET_TEMPLATE.format(params=_params, indented_snippet_block=_indented_snippet_block)

  # 3. generate pynguin tests
  # TODO improve error handling: detail all possible errors
  _test_fn_strs = None
  try:
    _test_fn_strs = p_pynguin.run_pynguin(_f_gold_fn_str)
  except Exception as err:
    logger.warning(f'Pynguin failed to generate tests: {err}')
    return False

  assert len(_test_fn_strs) == 1, 'expecting a single test function'
  _test_fn_str = _test_fn_strs[0]
  logger.debug(f'generated test function:\n{_test_fn_str}')

  # 4. combine into a test script without log statements
  _test_script_str = p_consts.TEST_SCRIPT_TEMPLATE.format(
    test_fn_str=_test_fn_str,
    f_gold_fn_str=_f_gold_fn_str,
    test_call_str='test()'
  )
  logger.debug('combined test function and f_gold() into a test script')

  # 5. insert log statements into the test script
  _ts_tree = src_parser.parse(bytes(_test_script_str, 'utf-8'))
  _tree = pvpy.Tree.from_ts_tree(_ts_tree)
  _ls_inserter = pvpy.LogStatementInserter(function_name='f_gold')
  _ls_inserter.visit(_tree.root_node)
  _test_script_str = pvpy.PrettyPrinter(indent_with='    ').visit(_tree.root_node).strip()
  logger.debug('instrumented the test script with log statements')

  # 6. translate the test script into the target language
  _translation_rules_main_code = trule_under_test + '\n\n' + log_statement_rule + '\n\n' + existing_ruleset

  pirel_subject_snippet_conf['src_program'] = _test_script_str
  pirel_subject_snippet_conf['translation_rules_main_code'] = _translation_rules_main_code
  _pirel_subject = p_subject.PirelSubject.from_dict_config(pirel_subject_snippet_conf)

  try:
    _tar_program_plausible = prapp.apply_translation_rules(_pirel_subject)
  except Exception as err:
    logger.warning(f'Failed to obtain the translation of the test script: {err}')
    return False

  logger.debug('obtained the translation of the test script')
  logger.debug('translation rule is valid')
  return True


# INDIVIDUAL RULE VALIDATION USAGE
def _validate_translation_rule_usage():
  # we will check the translation of this snippet
  snippet_under_test = 'c = d'
  trule_under_test = p_utils.read_text(p_consts.ROOT_DIR / 'individual-trule-validation' / 'rule-validation-module-artifacts' / 'rule1-lex-decl.snart')
  existing_ruleset = p_utils.read_text(p_consts.STARTING_RULESET_FPATH)
  src_lang = 'py'

  src_parser = p_consts.PARSER_DICT[src_lang]
  log_statement_rule = p_utils.read_text(p_consts.LOG_STAT_RULE_FPATH)
  pirel_subject_snippet_conf : dict = p_utils.read_yaml(p_consts.SNIPPET_UNDER_TEST_CONF_FPATH)

  # 1. extract parametrizable identifiers from the snippet
  _ts_tree = src_parser.parse(bytes(snippet_under_test, 'utf-8'))
  _tree = pvpy.Tree.from_ts_tree(_ts_tree)
  _param_collector = pvpy.ParametrizableVariablesCollector()
  _param_collector.visit(_tree.root_node)
  _parametrizable_identifiers = _param_collector.get_parametrizable_identifiers()

  # 2. prepare f_gold() function
  _params = ', '.join(_parametrizable_identifiers)
  _indented_snippet_block = p_utils.indent(snippet_under_test, 4)
  _f_gold_fn_str = p_consts.F_GOLD_SNIPPET_TEMPLATE.format(params=_params, indented_snippet_block=_indented_snippet_block)

  # 3. generate pynguin tests
  _test_fn_strs = p_pynguin.run_pynguin(_f_gold_fn_str)
  assert len(_test_fn_strs) == 1, 'expecting a single test function'
  _test_fn_str = _test_fn_strs[0]

  # 4. combine into a test script without log statements
  _test_script_str = p_consts.TEST_SCRIPT_TEMPLATE.format(
    test_fn_str=_test_fn_str,
    f_gold_fn_str=_f_gold_fn_str,
    test_call_str='test()'
  )

  # 5. insert log statements into the test script
  _ts_tree = src_parser.parse(bytes(_test_script_str, 'utf-8'))
  _tree = pvpy.Tree.from_ts_tree(_ts_tree)
  _ls_inserter = pvpy.LogStatementInserter(function_name='f_gold')
  _ls_inserter.visit(_tree.root_node)
  _test_script_str = pvpy.PrettyPrinter(indent_with='    ').visit(_tree.root_node).strip()

  # 6. translate the test script into the target language
  _translation_rules_main_code = trule_under_test + '\n\n' + log_statement_rule + '\n\n' + existing_ruleset

  pirel_subject_snippet_conf['src_program'] = _test_script_str
  pirel_subject_snippet_conf['translation_rules_main_code'] = _translation_rules_main_code
  _pirel_subject = p_subject.PirelSubject.from_dict_config(pirel_subject_snippet_conf)
  _tar_program_plausible = prapp.apply_translation_rules(_pirel_subject)

  p_utils.write_tmp_text('test_script.py', _test_script_str)
  p_utils.write_tmp_text('tar_program_plausible.js', _tar_program_plausible)

  print('the translation rule is good')


if __name__ == '__main__':
  _validate_translation_rule_usage()
