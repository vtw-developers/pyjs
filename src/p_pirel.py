import json
from typing import List, Tuple

import d_ast_pretty
import d_grammar_expand
import p_consts
import p_generator
import p_grammar
import p_llm_gen
import p_rule_inferencer
import p_rule_validator
import p_subject
import p_translators
import p_tree_log as ptlog
import p_utils
import p_visitor as pvis
import p_visitor_py as pvpy


logger = p_utils.setup_logger(__name__)


class PirelError(RuntimeError): pass


def get_partial_program(subject: p_subject.PirelSubject, translation_rules: str, template_dict: dict) -> str:
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
  logger.info(f'~~~ Starting p_pirel.get_partial_program')

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
        subject_name=subject.name,
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


def learn_trans_rules_from_tsp(
  tsp: Tuple[str, str, str],
  template_dict: dict,
  subject: p_subject.PirelSubject,
  translation_rules: str,
  ltrule_learn_attempt: ptlog.TRuleLearnAttempt
) -> List[str]:
  '''
  RETURN All possible valid translation rules inferred from all possible translations of `tsp`.
  RAISE Nothing. Pass all exceptions to the caller.
  '''

  logger.debug(f'Starting p.pirel.learn_trans_rules_from_tsp')
  p_utils.log_json_time(f'{subject.name}_args-learn_trans_rules_from_tsp.json', locals())

  # TRANSLATE TSP TO GET {SP1-TP1, SP2-TP2} (TRANSLATION PAIR)
  lpllm_gen_log = ptlog.PLLMGenLog()
  ltrule_learn_attempt.p_llm_gen_log = lpllm_gen_log

  translation_pairs = p_llm_gen.get_translation_pairs_from_tsp(subject, tsp, template_dict, lpllm_gen_log)
  assert len(translation_pairs) > 0, 'sanity check: translation_pairs must not be empty'

  # INFER TRANSLATION RULES FROM TRANSLATION PAIRS
  lprule_inf_log = ptlog.PRuleInfLog()
  ltrule_learn_attempt.p_rule_inferencer_log = lprule_inf_log
  trules_list = p_rule_inferencer.infer_translation_rules(subject, template_dict, translation_pairs, lprule_inf_log)

  # CHECK TRANSLATION RULES
  lprule_val_log = ptlog.PRuleValLog()
  ltrule_learn_attempt.p_rule_validator_log = lprule_val_log
  checked_trules_list = p_rule_validator.filter_translation_rules(
    trules_list, subject, translation_rules, tsp, template_dict, lprule_val_log)
  return checked_trules_list


def learn_trans_rules_from_tsp_with_retries(
  tsp: Tuple[str, str, str],
  template_dict: dict,
  subject: p_subject.PirelSubject,
  translation_rules: str,
  ltsp: ptlog.TSP
) -> List[str]:
  '''
  RETURN All possible translation rules inferred from all possible translations of `tsp`.
  NOTE may return zero translation rules
  '''

  logger.debug(f'Starting p.pirel.learn_trans_rules_from_tsp_with_retries (num_attempts={p_consts.LEARN_RULES_FROM_TSP_NUM_ATTEMPTS})')

  trules_list = []
  attempt_idx = 1
  while attempt_idx <= p_consts.LEARN_RULES_FROM_TSP_NUM_ATTEMPTS:
    msg = (
      f'Attempt at learning translation rules from a TSP #{attempt_idx}\n'
      f'tsp.id = {ltsp.id}, trans_rule_learn_attempt.id = {attempt_idx}\n'
    )
    logger.debug(msg)

    ltrule_learn_attempt = ptlog.TRuleLearnAttempt(attempt_idx)
    ltsp.trans_rule_learn_attempts.append(ltrule_learn_attempt)

    # catch only non-critical exceptions, after which
    # we can attempt to learn rules from a TSP again.
    # TODO how about regenerating a TSP?
    try:
      trules_list = learn_trans_rules_from_tsp(tsp, template_dict, subject, translation_rules, ltrule_learn_attempt)
      if len(trules_list) > 0:
        logger.debug(f'Learned {len(trules_list)} translation rules from TSP.')
        ltrule_learn_attempt.num_trules = len(trules_list)
        ltrule_learn_attempt.success = True
        ltsp.success = True
        ltsp.learned_translation_rules = [ptlog.TRule.from_str(trule) for trule in trules_list]
        return trules_list
      else:
        logger.debug(f'No translation rules were learned from TSP.')
        ltrule_learn_attempt.success = False
        ltrule_learn_attempt.reason = 'No translation rules were learned from TSP.'

    except p_llm_gen.NoTransPairsFromTSPError as err:
      msg = (
        f'Error: {str(err)}\n'
        f'PiREL could not generate any translation pairs from a TSP:\n'
        f'{json.dumps(tsp, indent=2)}\n'
        f'This was attempt number {attempt_idx}/{p_consts.LEARN_RULES_FROM_TSP_NUM_ATTEMPTS}'
      )
      ltrule_learn_attempt.success = False
      ltrule_learn_attempt.reason = msg
      logger.warning(msg)

    attempt_idx += 1

  msg = f'Spent {p_consts.LEARN_RULES_FROM_TSP_NUM_ATTEMPTS} attempts and did not learn any translation rules from TSP.'
  logger.warning(msg)
  ltsp.success = False
  ltsp.reason = msg
  return trules_list


def learn_trans_rules_for_prob_node(
  subject: p_subject.PirelSubject,
  translation_rules: str,
  templates_dict: dict,
  lprob_node: ptlog.ProbNode
) -> list:
  '''
  Run PiREL translation rule learning module for a problematic node.

  PRE There is a translation error.
  RETURN [translation_rules]
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

        # in cases when templates_dict is loaded from str, keys are strings
        _valid_template_idx = p_utils.to_int(templates_dict['num_templates']) - 1
        template_dict = templates_dict.get(_valid_template_idx) or templates_dict.get(str(_valid_template_idx))
        return template_dict
      raise RuntimeError('DuoGlot should fail to translate the context code')

    def __get_pre_context_global(subject: p_subject.PirelSubject, templates_dict: dict) -> str:
      '''
      A pre-context is part of the code that appears before the context node
      of the problematic node inside a function body.

      The goal of this function is to extract pre-context for the snippet
      that is used to validate the translation rule. The idea of extraction
      algorithm is to find the enclosing `function_definition`s `block` node,
      and remove all nodes that appear after the context node. What is left
      is the pre-context that we need. After that, we replace the context
      node with a special identifier, that is later string-replaced by the
      actual snippet.
      '''
      tree = pvpy.Tree.from_str(subject.src_main_code)
      context_node = tree.root_node.get_child_by_path(templates_dict['context_node_path'])

      # 1. find the enclosing function_definition node's block
      cursor_node = context_node
      while cursor_node.get_parent() is not None:
        # remove siblings to the right of cursor_node as we are moving up
        next_sibling = cursor_node.next_sibling()
        while next_sibling is not None:
          # need to get the pointer to the next_sibling++
          # before removing next_sibling itself
          next_next_sibling = next_sibling.next_sibling()
          next_sibling.get_parent().get_children().remove(next_sibling)
          next_sibling.parent = None
          next_sibling = next_next_sibling
        # move up the tree
        cursor_node = cursor_node.get_parent()
        if isinstance(cursor_node, pvpy.BlockNode):
          if isinstance(cursor_node.get_parent(), pvpy.FunctionDefinitionNode):
            break

      # 2. replace the context node with a special identifier
      spec_id_stat = pvpy.ExpressionStatementNode.build(
        pvpy.IdentifierNode.build(p_consts.PRE_CTX_SPEC_IDENT)
      )
      spec_id_stat.set_parent(context_node.get_parent())
      context_node_idx_as_child = context_node.parent.children.index(context_node)
      context_node.parent.children[context_node_idx_as_child] = spec_id_stat

      # 3. pretty print the block
      pp = pvpy.PrettyPrinter(indent_with='    ')
      pp.visit(cursor_node)
      pre_context = '\n'.join(pp.lines)
      return pre_context

    # deprecated
    def __get_pre_context_local_deprecated(subject: p_subject.PirelSubject, templates_dict: dict) -> str:
      '''
      A pre-context is part of the code that appears before the context node
      of the problematic node inside a function body.

      The goal of this function is to extract local pre-context for the snippet
      that is used to validate the translation rule. The idea of extraction
      algorithm is to find the enclosing `block` node,
      and remove all nodes that appear after the context node. What is left
      is the pre-context that we need. After that, we replace the context
      node with a special identifier, that is later string-replaced by the
      actual snippet.
      '''
      tree = pvpy.Tree.from_str(subject.src_main_code)
      context_node = tree.root_node.get_child_by_path(templates_dict['context_node_path'])

      # 1. find the enclosing function_definition node's block
      cursor_node = context_node
      while cursor_node.get_parent() is not None:
        # remove siblings to the right of cursor_node as we are moving up
        next_sibling = cursor_node.next_sibling()
        while next_sibling is not None:
          # need to get the pointer to the next_sibling++
          # before removing next_sibling itself
          next_next_sibling = next_sibling.next_sibling()
          next_sibling.get_parent().get_children().remove(next_sibling)
          next_sibling.parent = None
          next_sibling = next_next_sibling
        # move up the tree
        cursor_node = cursor_node.get_parent()
        if isinstance(cursor_node, pvpy.BlockNode):
          break

      # 2. replace the context node with a special identifier
      spec_id_stat = pvpy.ExpressionStatementNode.build(
        pvpy.IdentifierNode.build(p_consts.PRE_CTX_SPEC_IDENT)
      )
      spec_id_stat.set_parent(context_node.get_parent())
      context_node_idx_as_child = context_node.parent.children.index(context_node)
      context_node.parent.children[context_node_idx_as_child] = spec_id_stat

      # 3. pretty print the parent of `block`
      # cursor_node is a block node, so we need to go up one more level
      block_parent = cursor_node.get_parent()
      if any(map(lambda x: isinstance(x, pvpy.BlockNode), context_node.get_nt_children())):
        # if the context node contains a block node, we stay at context node
        # e.g. if_statement, for_statement, etc.
        block_parent = spec_id_stat
      elif isinstance(cursor_node.get_parent(), pvpy.FunctionDefinitionNode):
        # if the block is a function body, we stay at cursor_node
        # cursor_node is a block node, that's ok, pretty printer can handle it
        block_parent = cursor_node
      pp = pvpy.PrettyPrinter(indent_with='    ')
      pp.visit(block_parent)
      pre_context = '\n'.join(pp.lines)
      return pre_context

    def __get_pre_context_local(subject: p_subject.PirelSubject, templates_dict: dict) -> str:
      '''
      A pre-context is part of the code that appears before the context node
      of the problematic node inside a function body.

      The goal of this function is to extract local pre-context for the snippet
      that is used to validate the translation rule. The idea of extraction
      algorithm is to find the enclosing `block` node,
      and remove all nodes that appear after the context node. What is left
      is the pre-context that we need. After that, we replace the context
      node with a special identifier, that is later string-replaced by the
      actual snippet.
      '''
      tree = pvpy.Tree.from_str(subject.src_main_code)
      context_node = tree.root_node.get_child_by_path(templates_dict['context_node_path'])

      # 1. find the closest enclosing block
      cursor_node = context_node
      while cursor_node.get_parent() is not None:
        # remove siblings to the right of cursor_node as we are moving up
        next_sibling = cursor_node.next_sibling()
        while next_sibling is not None:
          # need to get the pointer to the next_sibling++
          # before removing next_sibling itself
          next_next_sibling = next_sibling.next_sibling()
          next_sibling.get_parent().get_children().remove(next_sibling)
          next_sibling.parent = None
          next_sibling = next_next_sibling
        # move up the tree
        cursor_node = cursor_node.get_parent()
        if isinstance(cursor_node, pvpy.BlockNode):
          break

      # 2. replace the context node with a special identifier
      spec_id_stat = pvpy.ExpressionStatementNode.build(
        pvpy.IdentifierNode.build(p_consts.PRE_CTX_SPEC_IDENT)
      )
      spec_id_stat.set_parent(context_node.get_parent())
      context_node_idx_as_child = context_node.parent.children.index(context_node)
      context_node.parent.children[context_node_idx_as_child] = spec_id_stat

      # 3. pretty print the `block`
      pp = pvpy.PrettyPrinter(indent_with='    ')
      pp.visit(cursor_node)
      pre_context = '\n'.join(pp.lines)
      return pre_context

    logger.debug('Starting template_dict initialization')

    # in cases when templates_dict is loaded from str, keys are strings
    _valid_template_idx = p_utils.to_int(templates_dict['num_templates']) - 1
    template_dict = templates_dict.get(_valid_template_idx) or templates_dict.get(str(_valid_template_idx))
    p_utils.log_json_time(f'{subject.name}_TEMPLATE_DICT_0_init.json', template_dict)

    # Rerun DuoGlot translation to obtain `template_dict`
    # for the context code snippet, not the entire program.
    # This is done to get the updated values for
    # `context_node_id`, `problematic_node_id`, and `problematic_node_path`
    template_dict = __rerun_translation_for_context(subject, translation_rules, template_dict)
    p_utils.log_json_time(f'{subject.name}_TEMPLATE_DICT_1_context_1.json', template_dict)

    # simplify the context
    template_dict = p_grammar.simplify_template(subject, template_dict)
    p_utils.log_json_time(f'{subject.name}_TEMPLATE_DICT_2_simplify_1.json', template_dict)

    # simplify the template using the generator
    template_dict = p_generator.simplify_template_with_generator(subject, template_dict)
    p_utils.log_json_time(f'{subject.name}_TEMPLATE_DICT_3_simplify_2.json', template_dict)

    # Rerun DuoGlot translation to obtain `template_dict`
    # for the context code snippet, not the entire program.
    # This is done to get the updated values for
    # `context_node_id`, `problematic_node_id`, and `problematic_node_path`
    template_dict = __rerun_translation_for_context(subject, translation_rules, template_dict)
    p_utils.log_json_time(f'{subject.name}_TEMPLATE_DICT_4_context_2.json', template_dict)

    # prepare partial program
    partial_program = get_partial_program(subject, translation_rules, template_dict)
    template_dict['partial_program'] = partial_program
    p_utils.log_json_time(f'{subject.name}_TEMPLATE_DICT_5_par_prog.json', template_dict)

    # `src_program` is needed for a prompt that uses it as a reference
    template_dict['src_program'] = subject.src_main_code
    p_utils.log_json_time(f'{subject.name}_TEMPLATE_DICT_6_src_program.json', template_dict)

    # prepare pre-context of the context node of the problematic node
    # NOTE pre-context is used in translation rule validation
    pre_context = __get_pre_context_local(subject, templates_dict)
    template_dict['pre_context'] = pre_context
    p_utils.log_json_time(f'{subject.name}_TEMPLATE_DICT_7_pre_context_FINAL.json', template_dict)

    logger.debug('Finished template_dict initialization')
    logger.debug(f'template_dict:\n{json.dumps(template_dict, indent=2)}')
    return template_dict

  def _init_tsps(subject: p_subject.PirelSubject, template_dict: dict) -> List[Tuple[str, str, str]]:
    '''
    Generate TSPs using a new algorithm.
    TODO consider built-in function names
    '''
    logger.debug(f'Starting TSP generation')

    tsps = p_generator.generate_tsps_with_generator(template_dict)
    assert len(tsps) > 0, 'Zero TSPs generated'

    logger.debug(f'Finished TSP generation')
    p_utils.log_json_time(f'{subject.name}_TSPs-generated.json', tsps)
    return tsps

  msg = (
    f'Starting p_pirel.learn_trans_rules_for_prob_node for "{subject.name}"\n'
    f'problematic_node.node_id = {lprob_node.node_id}, problematic_node.node_type = {lprob_node.node_type}\n'
  )
  logger.debug(msg)
  p_utils.log_json_time(f'{subject.name}_args-learn_trans_rules_for_prob_node.json', locals())

  # ~~~ initialize template_dict and TSPs
  template_dict = _init_template_dict(subject, translation_rules, templates_dict)
  tsps = _init_tsps(subject, template_dict)

  lprob_node.template_origin = template_dict['template_origin']

  # ~~~ iterate over TSPs (from abstract to concrete)
  # NOTE since we are using an updated TSP generation algorithm,
  # we stop at the first TSP from which we have learned a translation rule(s).
  # There is a high chance that such a TSP is the first one in `tsps` list
  # according to our new algorithm.
  num_useful_tsps = 0
  all_trules_list = []
  for tsp_idx, tsp in enumerate(tsps, start=1):
    msg = (
      f'Learning translation rules using TSP ({tsp_idx}/{len(tsps)}):\n'
      f'tsp.id = {tsp_idx}\n'
      f'{json.dumps(tsp, indent=2)}\n'
    )
    logger.info(msg)
    print(msg)

    ltsp = ptlog.TSP(tsp_idx, *tsp)
    lprob_node.tsps.append(ltsp)

    # `learn_trans_rules_from_tsp` is responsible for translation rule validation
    # it is called in `learn_trans_rules_from_tsp_with_retries`
    trules_list = learn_trans_rules_from_tsp_with_retries(tsp, template_dict, subject, translation_rules, ltsp)

    # go to the next TSP if no translation rules were learned
    if len(trules_list) == 0:
      logger.debug(f'Skipping a TSP: no translation rules were learnt from it (tsp_idx={tsp_idx})')
      logger.debug(f'TSP:\n{json.dumps(tsp, indent=2)}')
      continue

    num_useful_tsps += 1
    all_trules_list.extend(trules_list)
    if num_useful_tsps >= p_consts.MAX_NUM_USEFUL_TSPS:
      break

  if len(all_trules_list) > 0:
    lprob_node.success = True
    return all_trules_list

  msg = (
    f'Could not learn valid translation rules to translate\n'
    f'the problematic node with any of the {len(tsps)} TSPs.\n'
    f'problematic_node_type = "{template_dict["problematic_node_type"]}".\n'
    f'len(tsps) = {len(tsps)}\n'
  )
  logger.critical(msg)
  lprob_node.success = False
  lprob_node.reason = msg
  raise PirelError(msg)


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

  KWARGS
  - subject_name: str
  - skip_template_extraction: bool (optional)
  '''

  assert 'subject_name' in kwargs, 'subject_name is missing'

  # since this function may be invoked many times, log locals() only for debugging
  p_utils.log_json_time(f'{kwargs["subject_name"]}_args-duoglot_translate_wrapper.json', locals())

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
  # If there are no raised exceptions, it means that the translation was successful.
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
def _test_learn_trans_rules_for_prob_node():
  '''
  def learn_trans_rules_for_prob_node(
    subject: p_subject.PirelSubject,
    translation_rules: str,
    templates_dict: dict,
    lprob_node: ptlog.ProbNode
  ) -> list:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_learn_trans_rules_for_prob_node_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  subject = p_subject.PirelSubject.from_dict_config(json.loads(args_dict['subject']))
  translation_rules = args_dict['translation_rules']
  templates_dict = args_dict['templates_dict']
  lprob_node = ptlog.ProbNode(0, 'some_type')

  result = learn_trans_rules_for_prob_node(subject, translation_rules, templates_dict, lprob_node)
  print('\n\n'.join(result))


def _test_duoglot_translate_wrapper():
  '''
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
  config_fpath = p_consts.TMP_DIR / 'test_duoglot_translate_wrapper_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  src_code = args_dict['src_code']
  src_lang = args_dict['src_lang']
  tar_lang = args_dict['tar_lang']
  trans_rules = args_dict['trans_rules']
  auto_backward = args_dict['auto_backward']
  choices = args_dict['choices']
  kwargs = args_dict['kwargs']

  try:
    result = duoglot_translate_wrapper(
      src_code,
      src_lang,
      tar_lang,
      trans_rules,
      auto_backward,
      choices,
      **kwargs
    )
    print(json.dumps(result, indent=2))
    print(result['tar_code'])
  except d_grammar_expand.TranslationRuleNotFoundException as exc:
    templates_dict = exc.get_templates_dict()
    print(f'Error: {exc}')
    print(f'Templates dict:\n{json.dumps(templates_dict, indent=2)}')


if __name__ == '__main__':
  # _test_learn_trans_rules_for_prob_node()
  _test_duoglot_translate_wrapper()
