import json
from typing import List, Tuple

import d_grammar_expand
import d_grammar_rules
import p_consts
import p_pirel
import p_pynguin
import p_rule_applicator as prapp
import p_rule_postprocessor as prpp
import p_subject
import p_tree_log as ptlog
import p_utils
import p_visitor_py as pvpy


logger = p_utils.setup_logger(__name__)


def is_valid_translation_rule_syntactic(
  subject: p_subject.PirelSubject,
  translation_rule: str,
  existing_ruleset: str,
  ltrule: ptlog.TRule
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

  def _process_used_rules(
    rule_ids_before: List[int],
    rule_ids_after: List[int],
    ltrule_syntax_val_res: ptlog.TRuleSyntaxValRes
  ) -> bool:
    nonlocal existing_ruleset
    logger.debug('~~ checking rule under test based on the rule ids used')
    logger.debug(f'rule_ids_before: {rule_ids_before}')
    logger.debug(f'rule_ids_after: {rule_ids_after}')

    # number of rules used after must be strictly greater than the number of rules used before
    logger.debug('~ checking if the number of rules used after is greater than before')
    if not (len(rule_ids_after) > len(rule_ids_before)):
      msg = (
        f'Translation rule is BAD:\n'
        f'number of rules used after ({len(rule_ids_after)}) {str(rule_ids_after)}\n'
        f'must be strictly greater than the\n'
        f'number of rules used before ({len(rule_ids_before)}) {str(rule_ids_before)}'
      )
      logger.warning(msg)
      ltrule_syntax_val_res.is_valid = False
      ltrule_syntax_val_res.reason = msg
      return False
    logger.debug('~ [good] the number of rules used after is greater than before')

    # used rule id's before must be identical to the first rule id's after
    logger.debug('~ checking if the used rule ids after are prefixed with the rule ids before')
    for i in range(len(rule_ids_before)):
      if rule_ids_before[i] != rule_ids_after[i]:
        msg = (
          'Translation rule is BAD:\n'
          f'used rule ids at index {i} are different.\n'
          'Should not happen under normal circumstances.\n'
          'More debugging needed.'
        )
        logger.warning(msg)
        ltrule_syntax_val_res.is_valid = False
        ltrule_syntax_val_res.reason = msg
        return False
    logger.debug('~ [good] used rule ids after are prefixed with the rule ids before')

    # id of the first rule used must be of rule under test
    # `rule_ids_before = [3, 10, 4, 5, 6, 0]`
    # `rule_ids_after  = [3, 10, 4, 5, 6, 0, 17, 8, 7]`
    # as in the example above, `17` must be id of the rule under test
    logger.debug('~ checking if rule under test is used for the problematic node')
    existing_rules_list, _ = d_grammar_rules.parse_analyze_rules(existing_ruleset)
    num_rules_in_before_ruleset = len(existing_rules_list)
    # this will be id of the rule under test
    rule_under_test_idx_in_after_ruleset = num_rules_in_before_ruleset
    num_rules_used_in_before_rule_ids = len(rule_ids_before)
    rule_under_test_idx_in_after_rule_ids = num_rules_used_in_before_rule_ids
    if rule_under_test_idx_in_after_ruleset != rule_ids_after[rule_under_test_idx_in_after_rule_ids]:
      msg = (
        'Translation rule is BAD:\n'
        'The last used rule id is not of the rule under test.\n'
        'Should not happen under normal circumstances.\n'
        'More debugging needed.'
      )
      logger.warning(msg)
      ltrule_syntax_val_res.is_valid = False
      ltrule_syntax_val_res.reason = msg
      return False
    logger.debug('~ [good] rule under test is used for the problematic node')

    logger.debug('translation rule is syntactically valid')
    ltrule_syntax_val_res.is_valid = True
    return True

  msg = (
    f'~~ Checking if translation rule is syntactically valid:\n'
    f'Rule hash value: {ltrule.hash}\n'
    f'{translation_rule}'
  )
  logger.debug(msg)
  ltrule_syntax_val_res = ptlog.TRuleSyntaxValRes()
  ltrule.syntax_val_res = ltrule_syntax_val_res

  # ~~~ FIRST, CHECK IF THE MAPPINGS IN THE TRANSLATION RULE ARE CORRECT
  logger.debug('~ checking if the mappings in the translation rule are correct')
  expansion_programs, _ = d_grammar_rules.parse_analyze_rules(translation_rule)
  assert len(expansion_programs) == 1, 'should not happen: there must be exactly one translation rule'
  match_pattern, expand_pattern = expansion_programs[0]['match'], expansion_programs[0]['expand']
  try:
    _ = prpp.TranslationRule(match_pattern, expand_pattern)
  except prpp.RuleMappingError as err:
    msg = (
      f'Translation rule is BAD:\n'
      f'is invalid due to rule mapping error:\n'
      f'{p_utils.exception_to_str(err)}'
    )
    logger.warning(msg)
    ltrule_syntax_val_res.is_valid = False
    ltrule_syntax_val_res.reason = msg
    return False
  logger.debug('~ the mappings in the translation rule are correct')

  # ~~~ SECOND, CHECK IF THE TRANSLATION RULE REALLY TRANSLATES THE PROBLEMATIC NODE
  # ~~ get the translation result with the existing ruleset
  logger.debug('~ checking translation with the existing ruleset')
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
    logger.debug('[expected] Existing ruleset fails to translate as expected')
    # NOTE dbg_history should have been set in duoglot_translate_wrapper
    dbg_history_before = exc.dbg_history
  except:
    msg = 'Translation failed with the existing ruleset. Should not happen.'
    logger.error(msg)
    ltrule_syntax_val_res.is_valid = False
    ltrule_syntax_val_res.reason = msg
    raise RuntimeError('Only TranslationRuleNotFoundException is expected')
  else:
    msg = (
      '[unexpected] existing ruleset translated the code\n'
      'This case needs to be debugged.'
    )
    logger.error(msg)
    ltrule_syntax_val_res.is_valid = False
    ltrule_syntax_val_res.reason = msg
    return False

  # ~~ get the translation result with the (existing ruleset + rule under test)
  logger.debug('~ checking translation with the (existing ruleset + rule under test)')
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
    msg = (
      'Translation rule is GOOD:\n'
      'It translated the last problematic node(s).'
    )
    logger.debug(msg)
    ltrule_syntax_val_res.is_valid = True
    return True
  except d_grammar_expand.TranslationRuleNotFoundException as exc:
    msg = (
      '[expected] (existing ruleset + rule under test) failed to translate the code.\n'
      'Will further check the rule ids used before and after the translation'
    )
    # NOTE dbg_history should have been set in duoglot_translate_wrapper
    dbg_history_after = exc.dbg_history
  except Exception as exc:
    msg = (
      'Translation rule is BAD:\n'
      'Exception other than TranslationRuleNotFoundException occurred.\n'
      'Translation rule under test is bad.\n'
      'If the rule looks good to the eye, it might be a good idea to debug this case.\n'
      f'Exception: {p_utils.exception_to_str(exc)}'
    )
    logger.debug(msg)
    ltrule_syntax_val_res.is_valid = False
    ltrule_syntax_val_res.reason = msg
    return False

  # there still is a problematic node
  rule_ids_before = _get_used_translation_rule_ids(dbg_history_before)
  rule_ids_after = _get_used_translation_rule_ids(dbg_history_after)

  return _process_used_rules(rule_ids_before, rule_ids_after, ltrule_syntax_val_res)


def is_valid_translation_rule_test_based(
  subject: p_subject.PirelSubject,
  snippet_under_test: str,
  trule_under_test: str,
  existing_ruleset: str,
  ltrule: ptlog.TRule
) -> bool:
  '''
  Entry point for test-based checking if the provided translation rule is valid.
  '''

  p_utils.log_json_time(f'{subject.name}_args-is_valid_translation_rule_test_based.json', locals())

  msg = (
    f'~~ Checking if translation rule is valid based on tests:\n'
    f'Rule hash value: {ltrule.hash}\n'
    f'{trule_under_test}\n'
    f'Snippet to test translation rule:\n'
    f'{snippet_under_test}\n'
  )
  logger.debug(msg)

  ltrule_test_based_val_res = ptlog.TRuleTestBasedValRes()
  ltrule_test_based_val_res.snippet_under_test = snippet_under_test
  ltrule.test_based_val_res = ltrule_test_based_val_res

  src_parser = p_consts.PARSER_DICT[subject.src_lang]
  log_statement_rule = p_utils.read_text(p_consts.LOG_STAT_RULE_FPATH)
  pirel_subject_snippet_conf : dict = p_utils.read_yaml(p_consts.SNIPPET_UNDER_TEST_CONF_FPATH)

  # 1. extract parametrizable identifiers from the snippet
  logger.debug('~ extracting parametrizable identifiers from the snippet')
  _ts_tree = src_parser.parse(bytes(snippet_under_test, 'utf-8'))
  _tree = pvpy.Tree.from_ts_tree(_ts_tree)
  _param_collector = pvpy.ParametrizableVariablesCollector()
  _param_collector.visit(_tree.root_node)
  _parametrizable_identifiers = _param_collector.get_parametrizable_identifiers()
  logger.debug(f'~ parametrizable identifiers: {_parametrizable_identifiers}')

  if len(_parametrizable_identifiers) == 0:
    msg = 'No parametrizable identifiers found. Cannot generate tests.'
    logger.warning(msg)
    ltrule_test_based_val_res.is_valid = False
    ltrule_test_based_val_res.reason = msg
    return False

  # 2. prepare f_gold() function
  logger.debug('~ preparing f_gold() function for Pynguin')
  _params = ', '.join(_parametrizable_identifiers)
  _indented_snippet_block = p_utils.indent(snippet_under_test, 4)
  _f_gold_fn_str = p_consts.F_GOLD_SNIPPET_TEMPLATE.format(params=_params, indented_snippet_block=_indented_snippet_block)
  ltrule_test_based_val_res.f_gold_for_pynguin = _f_gold_fn_str
  logger.debug(f'~ f_gold() function:\n{_f_gold_fn_str}')

  # 3. generate pynguin tests
  # TODO improve error handling: detail all possible errors
  _test_fn_strs = None
  try:
    _test_fn_strs = p_pynguin.run_pynguin(_f_gold_fn_str)
  except Exception as err:
    msg = f'Pynguin failed to generate tests: {err}'
    logger.warning(msg)
    ltrule_test_based_val_res.is_valid = False
    ltrule_test_based_val_res.reason = msg
    return False

  assert len(_test_fn_strs) >= 1, 'expecting at least single test function'
  if len(_test_fn_strs) > 1:
    msg = (
      'Pynguin generated multiple test functions:\n'
      f'{json.dumps(_test_fn_strs, indent=2)}\n'
      'Will use the first one. Debug this case.\n'
    )
    logger.warning(msg)

  ltrule_test_based_val_res.num_generated_tests = len(_test_fn_strs)
  ltrule_test_based_val_res.pynguin_generated_tests = _test_fn_strs
  _test_fn_str = _test_fn_strs[0]
  logger.debug(f'generated test function:\n{_test_fn_str}')
  ltrule_test_based_val_res.generated_test_that_is_used = _test_fn_str

  # 4. combine into a test script without log statements
  _test_script_str = p_consts.TEST_SCRIPT_TEMPLATE.format(
    test_fn_str=_test_fn_str,
    f_gold_fn_str=_f_gold_fn_str,
    test_call_str='test()'
  )
  logger.debug('combined test function and f_gold() into a test script')

  # 5. insert log statements into the test script
  logger.debug('~ inserting log statements into the test script')
  _ts_tree = src_parser.parse(bytes(_test_script_str, 'utf-8'))
  _tree = pvpy.Tree.from_ts_tree(_ts_tree)
  _ls_inserter = pvpy.LogStatementInserter(function_name='f_gold')
  _ls_inserter.visit(_tree.root_node)
  _test_script_str = pvpy.PrettyPrinter(indent_with='    ').visit(_tree.root_node).strip()
  logger.debug('~ instrumented the test script with log statements:\n{_test_script_str}')
  ltrule_test_based_val_res.test_script = _test_script_str

  # 6. translate the test script into the target language
  _translation_rules_main_code = trule_under_test + '\n\n' + log_statement_rule + '\n\n' + existing_ruleset

  pirel_subject_snippet_conf['src_program'] = _test_script_str
  pirel_subject_snippet_conf['translation_rules_main_code'] = _translation_rules_main_code
  _pirel_subject = p_subject.PirelSubject.from_dict_config(pirel_subject_snippet_conf)

  logger.debug('~ attempting to obtain a plausible translation of the snippet under test')
  try:
    _tar_program_plausible = prapp.apply_translation_rules(_pirel_subject)
  except Exception as err:
    msg = (
      f'Failed to obtain a plausible translation of the test script:\n'
      f'{p_utils.exception_to_str(err)}\n'
    )
    logger.warning(msg)
    ltrule_test_based_val_res.is_valid = False
    ltrule_test_based_val_res.reason = msg
    return False

  logger.debug('successfully obtained the translation of the test script')
  logger.debug('translation rule is valid based on tests')
  ltrule_test_based_val_res.is_valid = True
  return True


def filter_translation_rules(
  trules_list: List[str],
  subject: p_subject.PirelSubject,
  translation_rules: str,
  tsp: Tuple[str, str, str],
  lprule_val_log: ptlog.PRuleValLog
) -> List[str]:
  '''
  Filter out translation rules that are not valid.
  The filtering is done by checking if the translation rule is valid syntactically and test-based.
  '''
  logger.debug('~~~ Starting p_rule_validator.filter_translation_rules')

  # filter out invalid translation rules
  checked_trules_list = []
  for idx, translation_rule in enumerate(trules_list, start=1):
    logger.debug(f'Checking translation rule {idx}/{len(trules_list)} for correctness')

    ltrule = ptlog.TRule.from_str(translation_rule)
    lprule_val_log.translation_rules.append(ltrule)

    is_syntax_valid = is_valid_translation_rule_syntactic(subject, translation_rule, translation_rules, ltrule)
    if not is_syntax_valid:
      logger.warning(f'Translation rule is not syntactically valid:\n{translation_rule}')
      continue

    is_semantics_valid = is_valid_translation_rule_test_based(subject, tsp[2], translation_rule, translation_rules, ltrule)
    if not is_semantics_valid:
      logger.warning(f'Translation rule is not semantically valid:\n{translation_rule}')
      continue

    checked_trules_list.append(translation_rule)
    logger.debug(f'The number of correct translation rules so far is {len(checked_trules_list)}')

  return checked_trules_list


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


# TEST HARNESSES
def _test_is_valid_translation_rule_syntactic():
  '''
  def is_valid_translation_rule_syntactic(
    subject: p_subject.PirelSubject,
    translation_rule: str,
    existing_ruleset: str,
    ltrule: ptlog.TRule
  ) -> bool:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_is_valid_translation_rule_syntactic_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  subject = p_subject.PirelSubject.from_dict_config(json.loads(args_dict['subject']))
  translation_rule = args_dict['translation_rule']
  existing_ruleset = args_dict['existing_ruleset']
  ltrule = ptlog.TRule.from_str(translation_rule)

  is_valid = is_valid_translation_rule_syntactic(
    subject,
    translation_rule,
    existing_ruleset,
    ltrule
  )
  print(is_valid)


if __name__ == '__main__':
  # _validate_translation_rule_usage()
  _test_is_valid_translation_rule_syntactic()
