import asyncio
import json
from typing import List, Optional

import d_grammar_expand
import d_grammar_rules
import p_consts
import p_ext_rule_chooser
import p_pirel
import p_rule_applicator as prapp
import p_rule_postprocessor as prpp
import p_ruleset
import p_subject
import p_tree_log as ptlog
import p_utils


logger = p_utils.setup_logger(__name__)


def get_used_translation_rule_ids(
  dbg_history: List[dict]
) -> List[int]:
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
  current_ruleset: str,
  ltrule_syntax_val_res: Optional[ptlog.TRuleSyntaxValRes] = None
) -> bool:

  logger.debug('~~ checking rule under test based on the rule ids used')
  logger.debug(f'rule_ids_before: {rule_ids_before}')
  logger.debug(f'rule_ids_after: {rule_ids_after}')
  ltrule_syntax_val_res = ltrule_syntax_val_res or ptlog.TRuleSyntaxValRes()

  # number of rules used after must be strictly greater than the number of rules used before
  logger.debug('~ checking if the number of rules used after is greater than before')
  if not (len(rule_ids_after) > len(rule_ids_before)):
    msg = (
      f'Translation rule is BAD:\n'
      f'number of rules used after ({len(rule_ids_after)}) {str(rule_ids_after)}\n'
      f'must be strictly greater than the\n'
      f'number of rules used before ({len(rule_ids_before)}) {str(rule_ids_before)}')
    logger.debug(msg)
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
      logger.debug(msg)
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
    logger.debug(msg)
    ltrule_syntax_val_res.is_valid = False
    ltrule_syntax_val_res.reason = msg
    return False
  logger.debug('~ [good] rule under test is used for the problematic node')

  logger.debug('translation rule is syntactically valid')
  ltrule_syntax_val_res.is_valid = True
  return True


def is_valid_translation_rule_syntactic(
  subject: p_subject.PirelSubject,
  translation_rule: str,
  current_ruleset: str,
  ltrule: Optional[ptlog.TRule] = None
) -> bool:
  '''
  Check if the provided translation rule:
  1. Has its placeholder mappings correct.
  2. Can translate the problematic node.
  PRE: exising ruleset fails to translate the code
  '''

  p_utils.log_json_time(f'args-is_valid_translation_rule_syntactic.json', locals())
  logger.debug(
    f'~~ Checking if translation rule is syntactically valid:\n'
    f'Rule hash value: {ltrule.hash}\n{translation_rule}')
  ltrule = ltrule or ptlog.TRule.from_str(translation_rule)
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
    logger.debug(msg)
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
      subject.get_src_main_code(),
      subject.src_lang,
      subject.tar_lang,
      current_ruleset,
      subject.auto_backward,
      subject.choices,
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
      subject.get_src_main_code(),
      subject.src_lang,
      subject.tar_lang,
      current_ruleset + '\n\n' + translation_rule,
      subject.auto_backward,
      subject.choices,
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
  rule_ids_before = get_used_translation_rule_ids(dbg_history_before)
  rule_ids_after = get_used_translation_rule_ids(dbg_history_after)

  return _process_used_rules(
    rule_ids_before,
    rule_ids_after,
    current_ruleset,
    ltrule_syntax_val_res
  )


def find_pirel_keyword_in_trule(
  trule: str
) -> Optional[str]:
  '''
  Very simple check for PiREL keywords in the translation rule.
  RETURN the first matching keyword or None if no match is found.
  '''
  pirel_keywords = [
    p_consts.GENERIC_SECRET_FN,
    p_consts.PAR_PROG_PROB_NODE_REPLACE,
    p_consts.PAR_PROG_DUMMY_IDENTIFIER,
    p_consts.PIREL_LOG_OBJ_FN_NAME,
    p_consts.PRE_CTX_SPEC_IDENT
  ]
  for keyword in pirel_keywords:
    if keyword in trule:
      return keyword
  return None


def is_invalid_pattern_detected(
  trule_str: str
) -> bool:
  '''
  Check if the translation rule contains some invalid patterns.
  RETURN True if an invalid pattern is detected, False otherwise.

  NOTE This is a temporary hacky solution. It does not solve the
  root cause of the problem. Solving the root cause will lift the
  need for this function.
  '''

  def _pattern1_par_expr_to_number(trule: prpp.TranslationRule) -> bool:
    '''
    Check for the patterns like this:
      (match_expand
        (fragment ("py.parenthesized_expression" (str "(") "." (str ")")) "*")
        (fragment ("js.number" (val "2")) "*2")
      )
    where a parenthesized expression is translated to anything
    other than a parenthesized expression.
    '''
    mroot_node = trule.src_root_node.children[0]
    if mroot_node.is_terminal():
      return False
    if mroot_node.get_type() != '"py.parenthesized_expression"':
      return False
    # number of placeholders in match pattern must be 2
    if len(trule.S) != 2:
      return False
    eroot_node = trule.tar_root_node.children[0]
    if eroot_node.is_terminal():
      return False
    if eroot_node.get_type() != '"js.parenthesized_expression"':
      return True
    # number of placeholders in expand pattern must be 2
    if len(trule.T) != 2:
      return True
    return False

  parsed_rules, _ = d_grammar_rules.parse_analyze_rules(trule_str)
  assert len(parsed_rules) == 1, 'should not happen: there must be exactly one translation rule'
  match_pattern, expand_pattern = parsed_rules[0]['match'], parsed_rules[0]['expand']
  trule = prpp.TranslationRule(match_pattern, expand_pattern)

  all_pattern_checks = [
    _pattern1_par_expr_to_number,
  ]
  for pattern_check in all_pattern_checks:
    if pattern_check(trule):
      logger.warning(
        f'Invalid pattern detected by {pattern_check.__name__} '
        f'in translation rule:\n{trule_str}')
      return True
  return False


def filter_translation_rules(
  trules_list: List[str],
  subject: p_subject.PirelSubject,
  current_ruleset: str,
  lprule_filter_log: Optional[ptlog.PRuleFilterLog] = None
) -> List[str]:
  '''
  Filter out translation rules that are not syntactically correct.

  subject must contain the following attributes:
  - get_src_main_code()
  - src_lang
  - tar_lang
  - auto_backward
  - choices
  '''
  logger.debug(
    f'rule-filter: ~~~ Starting p_rule_validator.filter_translation_rules. '
    f'Number of rules before: {len(trules_list)}')
  lprule_filter_log = lprule_filter_log or ptlog.PRuleFilterLog()

  syn_cor_trules = []
  for idx, trule in enumerate(trules_list, start=1):
    logger.debug(f'Checking translation rule {idx}/{len(trules_list)}:\n{trule}')
    ltrule = ptlog.TRule.from_str(trule)
    lprule_filter_log.trules_all.append(ltrule)

    is_syntax_valid = is_valid_translation_rule_syntactic(subject, trule, current_ruleset, ltrule)
    if not is_syntax_valid:
      logger.debug(f'rule-filter: translation rule is not syntactically valid:\n{trule}')
      continue

    pirel_keyword = find_pirel_keyword_in_trule(trule)
    if pirel_keyword is not None:
      logger.debug(f'rule-filter: found PiREL keyword "{pirel_keyword}" in translation rule:\n{trule}')
      continue

    is_inv_pat = is_invalid_pattern_detected(trule)
    if is_inv_pat:
      logger.debug(f'rule-filter: found invalid pattern in translation rule:\n{trule}')
      continue

    lprule_filter_log.trules_syn_valid.append(ltrule)
    syn_cor_trules.append(trule)

  logger.debug(
    f'rule-filter: ~~~ Finished filtering translation rules. '
    f'Number of rules after: {len(syn_cor_trules)}')
  return syn_cor_trules


async def check_trules_test_based(
  stat_val_subject: p_subject.PirelSubject,
  current_ruleset: p_ruleset.Ruleset,
  simple_ntext: str,
  lstat_node_val: Optional[ptlog.StatNodeVal] = None
) -> None:
  '''
  A valid ruleset is one that can translate the source program
  plausibly, i.e. both source and target programs behave
  the same on the tests.
  NOTE it is assumed that stat_val_subject.src_main_code is instrumented.
  '''

  p_utils.log_json_time(f'args-check_trules_test_based.json', locals())
  logger.debug('~~ Starting test-based validation of translation rules')

  lstat_node_val = lstat_node_val or ptlog.StatNodeVal()
  lstat_node_val.v2_expr_valid_stms = p_utils.current_time_msec()

  '''
  1. Raises AllRulesInMatcherGroupImplausibleError
  2. ruleset_serialized contains verified rules that can be copied
     to current_ruleset
  '''
  logger.debug('stat-val: getting readonly choices list before applying translation rules')
  readonly_choices_list = await p_ext_rule_chooser.get_readonly_choices_list(
    stat_val_subject.get_src_main_code(),
    stat_val_subject.get_src_test_code(),
    stat_val_subject.translation_rules_test_code,
    current_ruleset,
    simple_ntext,
    stat_val_subject.name
  )
  stat_val_subject.readonly_choices_list = readonly_choices_list
  logger.debug('stat-val: saved readonly choices list')

  lstat_node_val.v2_expr_valid_ok = True
  lstat_node_val.v2_expr_valid_etms = p_utils.current_time_msec()
  lstat_node_val.v3_rule_apply_stms = p_utils.current_time_msec()

  logger.debug('stat-val: applying translation rules to get the target program')
  tar_program_plausible, translate_dbg_history = \
    await prapp.apply_translation_rules(stat_val_subject)
  stat_val_subject.readonly_choices_list = []  # reset
  logger.debug('stat-val: finished applying translation rules')

  lstat_node_val.v3_rule_apply_ok = True
  lstat_node_val.v3_rule_apply_etms = p_utils.current_time_msec()


# TEST HARNESSES
def _test_is_valid_translation_rule_syntactic():
  '''
  def is_valid_translation_rule_syntactic(
    subject: p_subject.PirelSubject,
    translation_rule: str,
    current_ruleset: str,
    ltrule: Optional[ptlog.TRule] = None
  ) -> bool:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_is_valid_translation_rule_syntactic_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  subject = p_subject.PirelSubject.from_dict(args_dict['subject'])
  translation_rule = args_dict['translation_rule']
  current_ruleset = args_dict['current_ruleset']

  is_valid = is_valid_translation_rule_syntactic(
    subject,
    translation_rule,
    current_ruleset,
  )
  print(is_valid)


async def _test_check_trules_test_based():
  '''
  async def check_trules_test_based(
    stat_val_subject: p_subject.PirelSubject,
    current_ruleset: p_ruleset.Ruleset,
    simple_ntext: str,
    lstat_node_val: Optional[ptlog.StatNodeVal] = None
  ) -> None:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_check_trules_test_based_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  stat_val_subject = p_subject.PirelSubject.from_dict(args_dict['stat_val_subject'])
  current_ruleset = p_ruleset.Ruleset.from_dict(args_dict['current_ruleset'])
  simple_ntext = args_dict['simple_ntext']

  await check_trules_test_based(
    stat_val_subject,
    current_ruleset,
    simple_ntext,
    None
  )


if __name__ == '__main__':
  # _test_is_valid_translation_rule_syntactic()
  asyncio.run(_test_check_trules_test_based())
