import json
from typing import List, Tuple, Union

import d_grammar_expand
import d_grammar_rules
import p_consts
import p_llm_gen
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
  current_ruleset: str,
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
    nonlocal current_ruleset
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
    existing_rules_list, _ = d_grammar_rules.parse_analyze_rules(current_ruleset)
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
      current_ruleset,
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
      current_ruleset + '\n\n' + translation_rule,
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
  current_ruleset: str,
  template_dict: dict,
  ltrule: ptlog.TRule
) -> bool:
  '''
  Entry point for test-based checking if the provided translation rule is valid.

  1. Start with snippet_under_test -> `a = b`
  2. Extract paramable_ids from snippet_under_test -> `[b]`
  3. Prepare f_gold_fn_str using snippet_under_test and paramable_ids
  ```
  def f_gold(b):
      a = b
  ```
  4. Generate Pynguin tests for test_fn_str
  ```
  def test():
      args_sets = [[1], [2]]
      for idx, args_set in enumerate(args_sets):
          f_gold(*args_set)
  ```
  5. Combine test_fn_str and f_gold_fn_str into a test script
  ```
  def test():
      args_sets = [[1], [2]]
      for idx, args_set in enumerate(args_sets):
          f_gold(*args_set)
  def f_gold(b):
      a = b
  test()
  ```
  6. Insert log statements into the test script
  ```
  def test():
      args_sets = [[1], [2]]
      for idx, args_set in enumerate(args_sets):
          f_gold(*args_set)
  def f_gold(b):
      a = b
      myexactlog(b)
  test()
  ```
  7. Translate the test script into the target language and compare output traces.
  '''

  def _combine_pre_context_and_sut(pre_context: str, snippet_under_test: str) -> str:
    logger.debug('~ combining pre_context and snippet_under_test')
    assert pre_context.count(p_consts.PRE_CTX_SPEC_IDENT) == 1, \
      'should not happen: pre_context must contain exactly one line with special identifier'
    prectx_lines = pre_context.split('\n')
    spec_id_line_idx = -1
    for i, line in enumerate(prectx_lines):
      if p_consts.PRE_CTX_SPEC_IDENT in line:
        spec_id_line_idx = i
        break
    spec_id_indentation = p_utils.count_leading_spaces(prectx_lines[spec_id_line_idx])
    indented_sut = p_utils.indent(snippet_under_test, spec_id_indentation)
    indented_sut_lines = indented_sut.split('\n')
    prectx_lines = prectx_lines[:spec_id_line_idx] + indented_sut_lines + prectx_lines[spec_id_line_idx + 1:]
    prectx_w_sut = '\n'.join(prectx_lines)
    logger.debug(f'~ combined pre_context and snippet_under_test:\n{prectx_w_sut}')
    return prectx_w_sut

  def _get_f_gold_fn_str(paramable_ids: List[str], pcsut: str) -> str:
    logger.debug('~ preparing f_gold() function')
    _params = ', '.join(paramable_ids)

    # 1. prepare f_gold() function
    _indented_snippet_block = p_utils.indent(pcsut, 4)
    f_gold_fn_str = p_consts.F_GOLD_SNIPPET_TEMPLATE.format(params=_params, indented_snippet_block=_indented_snippet_block)

    # 2. insert break statements in loops
    # this is needed to avoid infinite loops
    # NOTE: this is a workaround for Pynguin
    if p_consts.PRE_CTX_INSERT_BREAK_IN_LOOPS:
      tree = pvpy.Tree.from_str(f_gold_fn_str)
      break_inserter = pvpy.BreakStatementInserter()
      break_inserter.visit(tree.root_node)
      f_gold_fn_str = pvpy.PrettyPrinter(indent_with='    ').visit(tree.root_node)

    logger.debug(f'~ f_gold() function:\n{f_gold_fn_str}')
    return f_gold_fn_str

  def _get_test_fn_str_llm(
    paramable_ids: List[str],
    f_gold_fn_str: str,
    subject: p_subject.PirelSubject,
    template_dict: dict,
    ltrule_test_based_val_res: ptlog.TRuleTestBasedValRes,
  ) -> Union[str, bool]:
    '''
    RETURN str | bool: If str is returned, it is the test function.
    If bool is returned, it means that no test function was generated.
    '''

    # cases such as `helper = {}` (L0001)
    # in such cases, the test function just invokes the f_gold() function
    if len(paramable_ids) == 0:
      msg = (
        'No parametrizable identifiers found.\n'
        'Will not generate Pynguin tests for this snippet.\n'
        'Will run the snippet directly after inserting the log statements.'
      )
      logger.debug(msg)
      return '''def test():\n    f_gold()'''

    test_fn_str = p_llm_gen.gen_test_function(f_gold_fn_str, subject, template_dict, ltrule_test_based_val_res)
    if test_fn_str is None:
      ltrule_test_based_val_res.is_valid = False
      ltrule_test_based_val_res.reason = 'LLM failed to generate test function'
      return False

    logger.debug(f'generated test function:\n{test_fn_str}')
    return test_fn_str

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

  # 1. combine pre_context and snippet_under_test
  pcsut = _combine_pre_context_and_sut(template_dict['pre_context'], snippet_under_test)

  # 2. extract parametrizable identifiers from pre_context + snippet_under_test
  # these identifiers are used as parameters of f_gold() function
  paramable_ids = pvpy.ParametrizableVariablesCollector.get_paramable_ids(pcsut)
  ltrule_test_based_val_res.paramable_ids = paramable_ids
  logger.debug(f'~ parametrizable identifiers: {paramable_ids}')

  # 3. prepare f_gold() function
  # f_gold() function is a wrapper function that contains the snippet under test
  f_gold_fn_str = _get_f_gold_fn_str(paramable_ids, pcsut)
  ltrule_test_based_val_res.f_gold_fn_str = f_gold_fn_str

  # 4. generate Pynguin tests for f_gold() function
  # Pynguin uses parameters of f_gold() function to generate test() function
  _result = _get_test_fn_str_llm(
    paramable_ids,
    f_gold_fn_str,
    subject,
    template_dict,
    ltrule_test_based_val_res
  )
  if isinstance(_result, bool):
    return _result
  test_fn_str = _result

  # 5. combine into a test script without log statements
  # a test script contains a test() function, f_gold() function
  # and test function invocation
  test_script_str = p_consts.TEST_SCRIPT_TEMPLATE.format(
    test_fn_str=test_fn_str,
    f_gold_fn_str=f_gold_fn_str,
    test_call_str='test()'
  )
  logger.debug(f'combined test function and f_gold() into a test script:\n{test_script_str}')

  # 6. insert log statements into the test script
  # log statements are inserted into the test script
  # log statements print the values of assigned variables to produce a trace
  test_script_str = pvpy.LogStatementInserter.insert_log_statements(test_script_str)
  logger.debug(f'~ instrumented the test script with log statements:\n{test_script_str}')
  ltrule_test_based_val_res.test_script = test_script_str

  # 7. translate the test script into the target language
  # the test script is translated into the target language
  # to compare its trace to the traces generated by test script in src language
  log_statement_rule = p_utils.read_text(p_consts.LOG_STAT_RULE_FPATH)
  extra_ruleset = p_utils.read_text(p_consts.RULE_VAL_EXTRA_RULES_FPATH)
  translation_rules_main_code = (
    f'{trule_under_test}\n\n'
    f'{log_statement_rule}\n\n'
    f'{extra_ruleset}\n\n'
    f'{current_ruleset}'
  )

  pirel_subject_snippet_conf : dict = p_utils.read_yaml(p_consts.SNIPPET_UNDER_TEST_CONF_FPATH)
  pirel_subject_snippet_conf['src_program'] = test_script_str
  pirel_subject_snippet_conf['translation_rules_main_code'] = translation_rules_main_code
  pirel_subject = p_subject.PirelSubject.from_dict_config(pirel_subject_snippet_conf)

  logger.debug('~ attempting to obtain a plausible translation of the snippet under test')
  try:
    tar_program_plausible = prapp.apply_translation_rules(pirel_subject)
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
  current_ruleset: str,
  template_dict: dict,
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

    is_syntax_valid = is_valid_translation_rule_syntactic(subject, translation_rule, current_ruleset, ltrule)
    if not is_syntax_valid:
      logger.warning(f'Translation rule is not syntactically valid:\n{translation_rule}')
      continue

    is_semantics_valid = is_valid_translation_rule_test_based(
      subject,
      'REPLACE WITH SNIPPET UNDER TEST',  # TODO: replace with the actual snippet under test
      translation_rule,
      current_ruleset,
      template_dict,
      ltrule
    )
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
  paramable_ids = _param_collector.get_parametrizable_identifiers()

  # 2. prepare f_gold() function
  _params = ', '.join(paramable_ids)
  _indented_snippet_block = p_utils.indent(snippet_under_test, 4)
  f_gold_fn_str = p_consts.F_GOLD_SNIPPET_TEMPLATE.format(params=_params, indented_snippet_block=_indented_snippet_block)

  # 3. generate pynguin tests
  test_fn_strs = p_pynguin.run_pynguin(f_gold_fn_str)
  assert len(test_fn_strs) == 1, 'expecting a single test function'
  test_fn_str = test_fn_strs[0]

  # 4. combine into a test script without log statements
  test_script_str = p_consts.TEST_SCRIPT_TEMPLATE.format(
    test_fn_str=test_fn_str,
    f_gold_fn_str=f_gold_fn_str,
    test_call_str='test()'
  )

  # 5. insert log statements into the test script
  _ts_tree = src_parser.parse(bytes(test_script_str, 'utf-8'))
  _tree = pvpy.Tree.from_ts_tree(_ts_tree)
  _ls_inserter = pvpy.LogStatementInserter(function_name='f_gold')
  _ls_inserter.visit(_tree.root_node)
  test_script_str = pvpy.PrettyPrinter(indent_with='    ').visit(_tree.root_node).strip()

  # 6. translate the test script into the target language
  translation_rules_main_code = trule_under_test + '\n\n' + log_statement_rule + '\n\n' + existing_ruleset

  pirel_subject_snippet_conf['src_program'] = test_script_str
  pirel_subject_snippet_conf['translation_rules_main_code'] = translation_rules_main_code
  pirel_subject = p_subject.PirelSubject.from_dict_config(pirel_subject_snippet_conf)
  tar_program_plausible = prapp.apply_translation_rules(pirel_subject)

  p_utils.write_tmp_text('test_script.py', test_script_str)
  p_utils.write_tmp_text('tar_program_plausible.js', tar_program_plausible)

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


def _test_is_valid_translation_rule_test_based():
  '''
  def is_valid_translation_rule_test_based(
    subject: p_subject.PirelSubject,
    snippet_under_test: str,
    trule_under_test: str,
    existing_ruleset: str,
    template_dict: dict,
    ltrule: ptlog.TRule
  ) -> bool:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_is_valid_translation_rule_test_based_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  subject = p_subject.PirelSubject.from_dict_config(json.loads(args_dict['subject']))
  snippet_under_test = args_dict['snippet_under_test']
  trule_under_test = args_dict['trule_under_test']
  existing_ruleset = args_dict['existing_ruleset']
  template_dict = args_dict['template_dict']
  ltrule = ptlog.TRule.from_str(trule_under_test)

  is_valid = is_valid_translation_rule_test_based(
    subject,
    snippet_under_test,
    trule_under_test,
    existing_ruleset,
    template_dict,
    ltrule
  )
  print(is_valid)


if __name__ == '__main__':
  # _validate_translation_rule_usage()
  # _test_is_valid_translation_rule_syntactic()
  _test_is_valid_translation_rule_test_based()
