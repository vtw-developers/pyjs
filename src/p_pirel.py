import json
from typing import List, Tuple, Union

import d_ast_pretty
import d_grammar_expand
import d_grammar_rules
import p_consts
import p_generator
import p_grammar
import p_llm_gen
import p_post_process_translation_rule as pptr
import p_rule_inferencer
import p_subject
import p_translators
import p_utils


logger = p_utils.setup_logger(__name__)


class PirelError(RuntimeError): pass


# PARTIAL PROGRAM GENERATION
def _get_partial_program(subject: p_subject.PirelSubject, translation_rules: str, template_dict: dict) -> str:
  '''
  A partial program (TODO is it a good name?) is a partially translated
  program in target language. Partial programs are used in LLM prompts
  to show the context of the code to be translated in the target program.

  IDEA
  Since translation is done in pre-order traversal, the sequence of nodes
  to be translated is:
  1. Nodes for which we have a translation rule
  2. Problematic node, for which we are attempting to learn a translation rule
  3. Nodes that are not translated yet.
  The algorithm is:
  a. Create a hacky rule for problematic node, that translates it into an
     identifier with a special name. This identifier will be the location
     of the translation. Everything around it will be the context.
  b. For each node in (3) create a hacky rule as in (a) with a different
     identifier with a special name, then just remove it from the code later.
     This way we get a partially translated program.
  '''

  def __append_hacky_rules(translation_rules: str, problematic_node_type: str, secret_identifier: str) -> str:
    '''
    Update `trans_rules` by appending all possible hacky rules
    to get a partial program.

    TODO HACKY this function is language dependent
    '''

    # contains possible ways to translate a node in the source language
    # into a node in the target language.
    HACKY_EXPANSIONS_PY_JS = {
      'pair': [
        # replacement for `pair` in `object`
        f'("js.shorthand_property_identifier" (val "{secret_identifier}"))',
      ],
      'default': [
        # convert a node into an identifier directly
        f'("js.identifier" (val "{secret_identifier}"))',

        # convert a node into an identifier under expression statement node
        f'("js.expression_statement" ("js.identifier" (val "{secret_identifier}")))',

        # ignore a node (do not translate)
        f''
      ]
    }

    matcher = f'"py.{problematic_node_type}" "*"'
    for hacky_expansion in HACKY_EXPANSIONS_PY_JS.get(problematic_node_type, HACKY_EXPANSIONS_PY_JS['default']):
      hacky_rule = f'(match_expand (fragment ({matcher}) "*") (fragment {hacky_expansion} "*2"))'
      translation_rules = translation_rules + f'\n\n{hacky_rule}'
    return translation_rules

  def __post_process_partial_program_remove_excess_replace_vars(partial_program: str) -> str:
    '''
    Problem: if a problematic node appears multiple times consecutively in the AST,
    what ends up happening is that partial program contains several consecutive
    replace_var's. This is not good for using with LLMs.
    This function solves this problem by str.replace() by replacing all occurences of
    replace_var's to dummy_var's except the first one.
    The solution is somewhat hacky and not complete, but it's much easier than
    intervening translation process where we require translate() to use different
    rules for the same consecutive node types.
    '''
    li = partial_program.rsplit(
      p_consts.PAR_PROG_PROB_NODE_REPLACE,
      partial_program.count(p_consts.PAR_PROG_PROB_NODE_REPLACE) - 1
    )
    return p_consts.PAR_PROG_DUMMY_IDENTIFIER.join(li)

  # NOTE if the first translation was successful, it means we have all necessary translation rules.
  # If it wasn't successful, then we run a loop in which we introduce `problematic_node -> identifier` rules
  # until we translate the program. This way we generate a partial program.
  logger.info(f'~~~ Starting p_pirel._get_partial_program')

  # 1 ADD HACKY RULES FOR THE MAIN PROBLEMATIC NODE
  prob_ntype_main = template_dict['problematic_node_type']
  new_trans_rules = __append_hacky_rules(translation_rules, prob_ntype_main, p_consts.PAR_PROG_PROB_NODE_REPLACE)
  new_src_code = template_dict['template_origin']

  logger.debug(f'problematic_node_type_main = "{prob_ntype_main}"')
  logger.debug(f'Appended hacky rules for the main problematic node to the ruleset')
  logger.debug(f'new_src_code = \n{new_src_code}')

  templates_dict = None
  try:
    duoglot_result_dict = duoglot_translate_wrapper(
      new_src_code,
      subject.src_lang,
      subject.tar_lang,
      new_trans_rules,
      subject.auto_backward,
      subject.choices,
      subject_name=subject.name,
      skip_template_extraction=True
    )
    logger.debug(f'SUCCESS. Partial program generation is complete. num_loops=0')
    tar_code = duoglot_result_dict['tar_code']
    partial_program = __post_process_partial_program_remove_excess_replace_vars(tar_code)
    return partial_program
  except d_grammar_expand.TranslationRuleNotFoundException as exc:
    templates_dict = exc.get_templates_dict()

  # 2 ADD HACKY RULES FOR THE SUBSEQUENT PROBLEMATIC NODES
  logger.debug(f'Translation is not over yet: there are still nodes to translate in a hacky way')
  loop_counter = 1

  while True:
    logger.debug(f'Entering partial program generation loop #{loop_counter}')
    assert templates_dict is not None, 'should not happen: templates_dict is None'
    prob_ntype_remaining = templates_dict['problematic_node_type']
    new_trans_rules = __append_hacky_rules(new_trans_rules, prob_ntype_remaining, p_consts.PAR_PROG_DUMMY_IDENTIFIER)

    logger.debug(f'prob_ntype_remaining = "{prob_ntype_remaining}"')
    logger.debug(f'Appended hacky rules to the ruleset')

    templates_dict = None
    try:
      duoglot_result_dict = duoglot_translate_wrapper(
        new_src_code,
        subject.src_lang,
        subject.tar_lang,
        new_trans_rules,
        subject.auto_backward,
        subject.choices,
        skip_template_extraction=True
      )
      tar_code = duoglot_result_dict['tar_code']
      partial_program = __post_process_partial_program_remove_excess_replace_vars(tar_code)
      logger.debug(f'SUCCESS. Partial program generation is complete. num_loops={loop_counter}')
      logger.debug(f'Partial program is:\n{partial_program}')
      return partial_program
    except d_grammar_expand.TranslationRuleNotFoundException as exc:
      templates_dict = exc.get_templates_dict()

    logger.debug(f'Partial program generation loop #{loop_counter} ended')
    loop_counter += 1


# PIREL TRANSLATION RULE LEARNING MODULE
def _is_valid_translation_rule(
  subject: p_subject.PirelSubject,
  translation_rule: str,
  existing_ruleset: str
) -> bool:
  '''
  Check if provided translation rule can translate the problematic node
  PRE: exising ruleset fails to translate the code
  '''

  p_utils.log_json_time(f'{subject.name}_args-is_valid_translation_rule.json', locals())

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
    _ = pptr.TranslationRule(match_pattern, expand_pattern)
  except pptr.RuleMappingError as err:
    msg = f'Translation rule is BAD:\n{translation_rule}\nis invalid due to rule mapping error:\n'
    msg += p_utils.exception_to_str(err)
    logger.warning(msg)
    return False

  # ~~~ SECOND, CHECK IF THE TRANSLATION RULE REALLY TRANSLATES THE PROBLEMATIC NODE
  # ~~ get the translation result with the existing ruleset
  dbg_history_before = None
  try:
    _ = duoglot_translate_wrapper(
      subject.src_main_code,
      subject.src_lang,
      subject.tar_lang,
      existing_ruleset,
      subject.auto_backward,
      subject.choices,
      subject_name=subject.name
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
    _ = duoglot_translate_wrapper(
      subject.src_main_code,
      subject.src_lang,
      subject.tar_lang,
      existing_ruleset + '\n\n' + translation_rule,
      subject.auto_backward,
      subject.choices,
      subject_name=subject.name
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


def _learn_trans_rules_from_tsp(
  tsp: Tuple[str, str],
  template_dict: dict,
  subject: p_subject.PirelSubject,
  translation_rules: str
) -> List[str]:
  '''
  RETURN All possible translation rules inferred from all possible translations of `tsp`.
  RAISE pass all exceptions to the caller
  '''

  logger.debug(f'Starting p.pirel._learn_rules_from_tsp')

  # translate TSP to get {SP1-TP1, SP2-TP2} (translation pair)
  translation_pairs = p_llm_gen.get_translation_pairs_from_tsp(subject, tsp, template_dict)

  # infer translation rules from translation pairs
  trules_list = p_rule_inferencer.infer_translation_rules(subject, template_dict, translation_pairs)

  # check translation rules
  checked_trules_list = []
  for idx, translation_rule in enumerate(trules_list, start=1):
    logger.debug(f'Checking translation rule {idx}/{len(trules_list)} for correctness')

    is_valid = _is_valid_translation_rule(subject, translation_rule, translation_rules)
    if is_valid:
      checked_trules_list.append(translation_rule)

    logger.debug(f'The number of correct translation rules so far is {len(checked_trules_list)}')

  return checked_trules_list


def _learn_trans_rules_from_tsp_with_retries(
  tsp: Tuple[str, str],
  template_dict: dict,
  subject: p_subject.PirelSubject,
  translation_rules: str
) -> List[str]:
  '''
  RETURN All possible translation rules inferred from all possible translations of `tsp`.
  NOTE may return zero translation rules
  '''

  logger.debug(f'Starting p.pirel._learn_rules_from_tsp_with_retries (num_attempts = {p_consts.LEARN_RULES_FROM_TSP_NUM_ATTEMPTS})')

  trules_list = []
  attempt = 1
  while attempt <= p_consts.LEARN_RULES_FROM_TSP_NUM_ATTEMPTS:
    logger.debug(f'Attempt at learning translation rules from a tsp #{attempt}')

    # catch only non-critical exceptions, after which
    # we can attempt to learn rules from a TSP again.
    # TODO how about regenerating a TSP?
    try:
      trules_list = _learn_trans_rules_from_tsp(tsp, template_dict, subject, translation_rules)
      if len(trules_list) > 0:
        logger.debug(f'Learned {len(trules_list)} translation rules from TSP.')
        return trules_list

    except p_llm_gen.CannotGetTranslationPairsFromTspError as err:
      msg = f'PiREL could not generate any translation pairs from a TSP:\n{json.dumps(tsp, indent=2)}\n'
      msg += f'This was attempt number {attempt}/{p_consts.LEARN_RULES_FROM_TSP_NUM_ATTEMPTS}'
      msg += p_utils.exception_to_str(err)
      logger.warning(msg)

    attempt += 1

  logger.debug(f'Spent {p_consts.LEARN_RULES_FROM_TSP_NUM_ATTEMPTS} attempts and did not learn any translation rules from TSP.')
  return trules_list


# FUNCTION THAT GLUES TOGETHER ALL DIFFERENT PIREL COMPONENTS
def learn_trans_rules_for_prob_node(
  subject: p_subject.PirelSubject,
  translation_rules: str,
  templates_dict: dict
) -> dict:
  '''
  Run PiREL translation rule learning module for a problematic node.

  PRE There is a translation error.
  RETURN {translation_rules, template_dict}
  RAISE `PirelError` if cannot generate a translation rule. Our goal is to never raise this error
  '''

  def _init_template_dict(subject: p_subject.PirelSubject, translation_rules: str, templates_dict: dict) -> dict:

    def __rerun_translation_for_context(subject: p_subject.PirelSubject, translation_rules: str, template_dict: dict) -> dict:
      '''
      Why do we need this function?
      We need this function to update certain values in `template_dict`:
      1. context_node_id
      2. problematic_node_id
      3. contexts (mainly)

      NOTE returns a new `template_dict`
      TODO optimize: context extraction is needed only at this step
      RETURN updated `template_dict`
      '''
      template_origin = template_dict['template_origin']
      try:
        _ = duoglot_translate_wrapper(
          template_origin,
          subject.src_lang,
          subject.tar_lang,
          translation_rules,
          subject.auto_backward,
          subject.choices,
          subject_name=subject.name,
        )
      except d_grammar_expand.TranslationRuleNotFoundException as exc:
        templates_dict = exc.get_templates_dict()
        template_dict = templates_dict[templates_dict['num_templates'] - 1]
        return template_dict
      raise RuntimeError('DuoGlot should fail to translate the context code')

    template_dict = templates_dict[templates_dict['num_templates'] - 1]
    p_utils.log_json_time(f'{subject.name}_TEMPLATE_DICT_0_init.json', template_dict)

    # Rerun DuoGlot translation to obtain `template_dict`
    # for the context code snippet, not the entire program.
    # This is done to get the updated values for
    # `context_node_id`, `problematic_node_id`, and `problematic_node_path`
    template_dict = __rerun_translation_for_context(subject, translation_rules, template_dict)
    p_utils.log_json_time(f'{subject.name}_TEMPLATE_DICT_1_context.json', template_dict)

    # simplify the context
    # template_dict = p_llm_gen.simplify_template(template_dict, **kwargs)  # LLM-based
    template_dict = p_grammar.simplify_template(subject, template_dict)  # generator-based
    p_utils.log_json_time(f'{subject.name}_TEMPLATE_DICT_2_simplify.json', template_dict)

    # prepare partial program
    partial_program = _get_partial_program(subject, translation_rules, template_dict)
    template_dict['partial_program'] = partial_program
    p_utils.log_json_time(f'{subject.name}_TEMPLATE_DICT_3_par_prog.json', template_dict)

    # `src_program` is needed for a prompt that uses it as a reference
    template_dict['src_program'] = subject.src_main_code
    p_utils.log_json_time(f'{subject.name}_TEMPLATE_DICT_4_final.json', template_dict)

    logger.debug(f'template_dict:\n{json.dumps(template_dict, indent=2)}')
    return template_dict

  def _init_tsps(subject: p_subject.PirelSubject, template_dict: dict) -> List[Tuple[str, str]]:
    # 1 generate all TSPs
    tsps = p_generator.generate_tsp_with_generator(template_dict)
    p_utils.log_json_time(f'{subject.name}_TSPs-only-generated.json', tsps)
    if len(tsps) == 0:
      logger.warning(f'Zero TSPs generated for the problematic node type "{template_dict["problematic_node_type"]}"')

    # 2 add (`template_origin`, `template_origin`) as a TSP for some cases such as `string`, `int`, etc.
    if template_dict['problematic_node_type'] in p_consts.TSP_INCLUDE_TEMPLATE_ORIGIN_NODE_TYPES[template_dict['src_lang']]:
      logger.debug('Adding `(template_origin, template_origin)` as a TSP')
      tsps.append((template_dict['template_origin'], template_dict['template_origin']))

    # 3 an overfitted TSP is a TSP where only literal values are different from that of `template_origin`.
    if p_consts.IS_GENERATE_OVERFITTED_TSP:
      overfitted_tsp = p_generator.generate_tsp_overfitted(template_dict)
      logger.debug('Adding an overfitted TSP')
      tsps.append(overfitted_tsp)

    assert len(tsps) > 0, 'Zero TSPs generated'
    p_utils.log_json_time(f'{subject.name}_TSPs-all.json', tsps)

    # 4 sort TSPs using LLM
    tsps = _sort_tsps_using_llm(tsps, subject, template_dict)
    p_utils.log_json_time(f'{subject.name}_TSPs-all-llm-sorted.json', tsps)
    return tsps

  def _sort_tsps_using_llm(tsps: List[Tuple[str, str]], subject: p_subject.PirelSubject, template_dict: dict, **kwargs) -> List[Tuple[str, str]]:
    '''
    Sort TSPs using LLM.
    We sort TSPs using LLM to get the most probable TSPs first.
    This way we can learn translation rules from the most probable TSPs.

    IDEA
    Iterate over TSPs, if a TSP has a syntactic error, move it to the end of the list.
    '''

    def __are_both_snippets_single_token_in_tsp(tsp: Tuple[str, str]) -> bool:
      '''
      Check if both snippets in a TSP are single tokens
      HACK assume that a single token is a token without spaces
      '''
      return len(tsp[0].split()) == 1 and len(tsp[1].split()) == 1

    logger.debug(f'Starting p_pirel._run_pirel._sort_tsps_using_llm')
    logger.debug(f'Number of unsorted TSPs is {len(tsps)}:\n{json.dumps(tsps, indent=2)}')

    syntactically_correct_tsps = []
    syntactically_incorrect_tsps = []

    for tsp_idx, tsp in enumerate(tsps, start=1):

      # early decision if both snippets are single tokens
      if __are_both_snippets_single_token_in_tsp(tsp):
        syntactically_incorrect_tsps.append(tsp)
        continue

      tsp_is_correct = None
      try:
        tsp_is_correct = p_llm_gen.is_tsp_syntactically_correct(tsp, subject, template_dict, **kwargs)
      except p_llm_gen.LLMResponseFormatError as err:
        logger.warning(f'Sorting TSPs: error in LLM response: {err}')
        continue

      assert tsp_is_correct is not None, 'should not happen: tsp_is_correct is None'
      if tsp_is_correct:
        syntactically_correct_tsps.append(tsp)
      else:
        syntactically_incorrect_tsps.append(tsp)

    logger.debug(f'Number of syntactically correct TSPs: {len(syntactically_correct_tsps)}')
    logger.debug(f'{json.dumps(syntactically_correct_tsps, indent=2)}')
    p_utils.log_json_time(f'{subject.name}_syntactically_correct_TSPs.json', syntactically_correct_tsps)

    logger.debug(f'Number of syntactically incorrect TSPs: {len(syntactically_incorrect_tsps)}')
    logger.debug(f'{json.dumps(syntactically_incorrect_tsps, indent=2)}')
    p_utils.log_json_time(f'{subject.name}_syntactically_incorrect_TSPs.json', syntactically_incorrect_tsps)

    if p_consts.IS_IGNORE_SYNTACTICALLY_INCORRECT_TSP_PER_LLM and len(syntactically_correct_tsps) > 0:
      logger.debug('Ignoring syntactically incorrect TSPs')
      return syntactically_correct_tsps

    logger.debug('Returning syntactically correct TSPs + syntactically incorrect TSPs')
    return syntactically_correct_tsps + syntactically_incorrect_tsps

  logger.debug(f'Starting p_pirel._run_pirel for {subject.name}')

  # ~~~ initialize template_dict and tsps
  template_dict = _init_template_dict(subject, translation_rules, templates_dict)
  tsps = _init_tsps(subject, template_dict)

  # ~~~ iterate over TSPs (from abstract to concrete)
  num_useful_tsps = 0
  all_translation_rules = []
  for tsp_idx, tsp in enumerate(tsps, start=1):
    msg = f'Learning translation rules using TSP ({tsp_idx}/{len(tsps)}):\n{json.dumps(tsp, indent=2)}'
    logger.info(msg)
    print(msg)

    trules_list = _learn_trans_rules_from_tsp_with_retries(tsp, template_dict, subject, translation_rules)
    if len(trules_list) == 0:
      logger.debug(f'Skipping a TSP: no translation rules were learnt from it (tsp_idx={tsp_idx})')
      logger.debug(f'TSP:\n{json.dumps(tsp, indent=2)}')
      continue

    all_translation_rules.extend(trules_list)
    num_useful_tsps += 1

    if num_useful_tsps == p_consts.MAX_NUM_USEFUL_TSPS:
      logger.info(f'GOOD: the number of translation rules is {len(all_translation_rules)}')
      logger.info(f'The number of TSPs used is {num_useful_tsps}')
      return all_translation_rules

  if num_useful_tsps > 0:
    logger.info(f'ALMOST GOOD: the number of translation rules is {len(all_translation_rules)}')
    logger.info(f'The number of TSPs used is {num_useful_tsps}')
    return all_translation_rules

  msg = f'Could not learn any translation rules to translate the problematic node.\n'
  msg += f'Problematic node type is "{template_dict["problematic_node_type"]}".\n'
  msg += f'Generated {len(tsps)} TSPs and none of them was successfully translated\n'
  msg += f'into target language to form translation pairs and further to infer translation rules.\n'
  msg += f'Here are the generated TSPs:\n{json.dumps(tsps, indent=2)}\n'
  msg += f'Here is the template_dict:\n{json.dumps(template_dict, indent=2)}'
  logger.critical(msg)
  raise PirelError(msg)


# ENTRY POINT FOR DUOGLOT TRANSLATION
def duoglot_translate_wrapper(
  src_code: str,
  src_lang: str,
  tar_lang: str,
  trans_rules: str,
  auto_backward: bool,
  choices: dict,
  **kwargs
) -> dict:
  '''
  Wrapper around DuoGlot's `grammar_expand.TransSession.get_translation()`.
  RAISE Propagate all exceptions to the caller.
  RETURN a dict containing all the relevant information about the target program.
  '''

  assert 'subject_name' in kwargs, 'subject_name is missing'
  subject_name = kwargs['subject_name']
  logger.info(f'Starting p_pirel.duoglot_translate_wrapper (subject_name={subject_name})')

  assert src_code.isascii()
  assert choices['type'] in ['STEP', 'ASTNODE'], 'Unknown choices type'
  slot_dedup_enabled = choices['type'] == 'ASTNODE'

  translator = p_translators.get_translator_cached(
    src_code,
    src_lang,
    tar_lang,
    trans_rules,
    slot_dedup_enabled
  )

  # NOTE raises all sorts of exceptions (check docs)
  tar_ast, dbg_history = translator.get_translation(choices, auto_backward, **kwargs)

  logger.info(f'SUCCESS DuoGlot translation is successful!')
  tar_code, map_to_exid = d_ast_pretty.ast_to_code(tar_ast, tar_lang)
  return {
    'src_ast': translator.source_ast,
    'src_ann': translator.source_ann,
    'tar_ast': tar_ast,
    'tar_code': tar_code,
    'map_to_exid': map_to_exid,
    'dbg_history': dbg_history,
    'translator_dbg_info': translator.get_session_dbg_info()
  }


# TEST HARNESSES
def _test_translate():
  test_harness_config : dict = p_utils.read_json('temporary_test_translate_config.json')
  args_dict = p_utils.read_json(test_harness_config['args_dict_fpath'])


def _test_translate_duoglot():
  test_harness_config : dict = p_utils.read_json('temporary_test_translate_duoglot_config.json')
  src_code = p_utils.read_text('temporary_test_translate_duoglot_src_code.py')
  src_lang = test_harness_config['src_lang']
  tar_lang = test_harness_config['tar_lang']
  trans_rules = p_utils.read_text('temporary_test_translate_duoglot_trans_rules.snart')
  auto_backward = test_harness_config['auto_backward']
  choices = test_harness_config['choices']
  _optional_dbg_info_save_func = lambda *x: None
  kwargs = test_harness_config['kwargs']

  result_dict = duoglot_translate_wrapper(
    src_code,
    src_lang,
    tar_lang,
    trans_rules,
    auto_backward,
    choices,
    _optional_dbg_info_save_func,
    **kwargs
  )
  print(json.dumps(result_dict, indent=2, default=str))
  p_utils.write_json('temporary_test_translate_duoglot.json', result_dict)


def _test_is_valid_translation_rule():
  test_harness_config : dict = p_utils.read_json('temporary_test_is_valid_translation_rule_config.json')
  args_dict = p_utils.read_json(test_harness_config['args_dict_fpath'])

  translation_rule = args_dict['translation_rule']
  src_code = args_dict['src_code']
  src_lang = args_dict['src_lang']
  tar_lang = args_dict['tar_lang']
  existing_ruleset = args_dict['existing_ruleset']
  auto_backward = args_dict['auto_backward']
  choices = args_dict['choices']
  _optional_dbg_info_save_func = lambda *x: None
  kwargs = args_dict['kwargs']

  result_dict = _is_valid_translation_rule(translation_rule, src_code, src_lang, tar_lang, existing_ruleset, auto_backward, choices, _optional_dbg_info_save_func, **kwargs)
  print(json.dumps(result_dict, indent=2))
  p_utils.write_json('temporary_test_is_valid_translation_rule.json', result_dict)


if __name__ == '__main__':
  # _test_translate()
  _test_translate_duoglot()
  # _test_is_valid_translation_rule()
