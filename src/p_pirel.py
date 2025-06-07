import json
from typing import List, Tuple

import d_ast_parse
import d_ast_pretty
import d_grammar_expand
import p_consts
import p_data_structures as pds
import p_generator
import p_grammar
import p_llm_gen
import p_rule_applicator
import p_rule_chooser
import p_rule_inferencer
import p_rule_validator
import p_ruleset
import p_subject
import p_translators
import p_tree_log as ptlog
import p_utils
import p_visitor_py as pvpy


logger = p_utils.setup_logger(__name__)


class CannotLearnRulesForProblematicNode(RuntimeError): pass
class NoTransRulesFromTSPError(RuntimeError): pass


def get_pre_context_global(src_main_code: str, stat_npath: List[int]) -> str:
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
  def _process_elif_clauses(else_clause_node: pvpy.ElifClauseNode) -> None:
    '''
    Replace all children of `elif` clause's body with a pass statement.
    '''
    pass_statement_node = pvpy.PassStatementNode.build()
    else_clause_node.consequence.children = [pass_statement_node]
    pass_statement_node.set_parent(else_clause_node.consequence)

  def _process_else_clauses(else_clause_node: pvpy.ElseClauseNode) -> None:
    '''
    Replace all children of `else` clause's body with a pass statement.
    '''
    pass_statement_node = pvpy.PassStatementNode.build()
    else_clause_node.body.children = [pass_statement_node]
    pass_statement_node.set_parent(else_clause_node.body)

  tree = pvpy.Tree.from_str(src_main_code)
  statement_node = tree.root_node.get_child_by_path(stat_npath)

  # 1. find the enclosing function_definition node's block
  cursor_node = statement_node
  while cursor_node.get_parent() is not None:

    # remove siblings to the right of cursor_node as we are moving up
    next_sibling = cursor_node.next_sibling()

    while next_sibling is not None:
      # need to get the pointer to the next_sibling++
      # before removing next_sibling itself
      next_next_sibling = next_sibling.next_sibling()

      # keep elif and else clauses because they are part of the translation rule
      # they are part of the translation rule due to the fact that
      # they are not simplified. Refer to p_grammar.simplify_template() for more information.
      if isinstance(next_sibling, pvpy.ElifClauseNode):
        _process_elif_clauses(next_sibling)
        next_sibling = next_next_sibling
        continue
      if isinstance(next_sibling, pvpy.ElseClauseNode):
        _process_else_clauses(next_sibling)
        next_sibling = next_next_sibling
        continue

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
    pvpy.IdentifierNode.build(p_consts.PRE_CTX_SPEC_IDENT))
  spec_id_stat.set_parent(statement_node.get_parent())
  context_node_idx_as_child = statement_node.parent.children.index(statement_node)
  statement_node.parent.children[context_node_idx_as_child] = spec_id_stat

  # 3. pretty print the block
  pp = pvpy.PrettyPrinter(indent_with='    ')
  pp.visit(cursor_node)
  pre_context = '\n'.join(pp.lines)
  return pre_context


def get_pre_context_global_deprecated(src_main_code: str, context_node_path: List[int]) -> str:
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
  tree = pvpy.Tree.from_str(src_main_code)
  context_node = tree.root_node.get_child_by_path(context_node_path)

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


def get_pre_context_local_deprecated(src_main_code: str, context_node_path: List[int]) -> str:
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
  tree = pvpy.Tree.from_str(src_main_code)
  context_node = tree.root_node.get_child_by_path(context_node_path)

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


def get_pre_context(src_main_code: str, lang: str, statement_nid: int) -> str:
  '''
  Get pre-context for the statement node.
  The pre-context is the code that appears before the statement node
  in the source code up to the closest enclosing function definition.
  '''
  p_utils.log_json_time(f'args-get_pre_context.json', locals())

  tree = pds.PirelTree.from_code_str(src_main_code, lang)
  statement_node = tree.get_root_node().get_node_by_id(statement_nid)
  statement_npath = tree.get_root_node().get_path_to_child(statement_node)
  pre_context = get_pre_context_global(src_main_code, statement_npath)
  return pre_context


def validate_translation_rules_for_statement_node(
  subject: p_subject.PirelSubject,
  statement_subject: p_subject.PirelSubject,
  current_ruleset_obj: p_ruleset.Ruleset,
  statement_nid: int,
  enable_error_recovery: bool = True,
) -> p_ruleset.Ruleset:
  '''
  RETURN the validated ruleset.
  '''

  statement_node = get_statement_node_by_id(subject.src_main_code, subject.src_lang, statement_nid)
  simple_ntext = simplify_statement_node_text(statement_node)
  pre_context = get_pre_context(subject.src_main_code, subject.src_lang, statement_nid)

  '''
  template_dict is required by `p_llm_gen.gen_test_function`
  which is invoked by `p_rule_validator.is_valid_translation_rule_test_based`.
  However, due to the updated control flow of the program, we do not have
  a template_dict corresponding to the group of nodes from which
  we have obtained the translation rules. To solve this problem,
  we "fabricate" a template_dict that contains the necessary information
  to run the validation. To see what information is needed,
  refer to `p_llm_gen.gen_test_function`.
  '''
  template_dict = {
    'src_lang': subject.src_lang,
  }

  while True:
    '''
    Run test-based rule validation to validate the learned translation rules
    that translate the statement node. This invocation has a call to
    p_rule_applicator.apply_translation_rules() that checks all possible
    translation rule combinations that result in a plausible translation
    of the source test script using the learned translation rules.
    '''
    try:
      is_valid = p_rule_validator.is_valid_translation_rule_test_based(
        simple_ntext,
        pre_context,
        current_ruleset_obj,
        statement_subject,
        template_dict
      )

      # ideal case: translation rules are valid
      assert is_valid, 'consider this case'
      return current_ruleset_obj

    except p_rule_applicator.TRuleNotFoundError as err:
      raise
    except p_rule_chooser.NoUniqueChoicesError as err:
      raise
    except p_rule_applicator.TraceMismatchError as err:
      raise

    break


def learn_trans_rules_from_tsp(
  tsp: Tuple[str, str],
  template_dict: dict,
  subject: p_subject.PirelSubject,
  current_ruleset: str
) -> List[str]:
  '''
  RETURN All possible valid translation rules inferred from all possible translations of `tsp`.
  RAISE `NoTransRulesFromTSPError` if no translation rules were learned from TSP.
  '''

  logger.debug(f'Starting p.pirel.learn_trans_rules_from_tsp')
  p_utils.log_json_time(f'{subject.name}_args-learn_trans_rules_from_tsp.json', locals())

  # TRANSLATE TSP TO GET {SP1-TP1, SP2-TP2} (TRANSLATION PAIR)
  lpllm_gen_log = ptlog.PLLMGenLog()
  translation_pairs = p_llm_gen.get_translation_pairs_from_tsp(subject, tsp, template_dict, lpllm_gen_log)
  assert len(translation_pairs) > 0, 'sanity check: translation_pairs must not be empty'

  # INFER TRANSLATION RULES FROM TRANSLATION PAIRS
  lprule_inf_log = ptlog.PRuleInfLog()
  trules_list = p_rule_inferencer.infer_translation_rules(subject, template_dict, translation_pairs, lprule_inf_log)

  # CHECK TRANSLATION RULES
  lprule_val_log = ptlog.PRuleValLog()
  checked_trules_list = p_rule_validator.filter_translation_rules(
    trules_list, subject, current_ruleset, lprule_val_log)

  if len(checked_trules_list) == 0:
    logger.warning('No translation rules were learned from TSP.')
    raise NoTransRulesFromTSPError('No translation rules were learned from TSP.')

  return checked_trules_list


def learn_trans_rules_from_tsp_with_retries(
  tsp: Tuple[str, str],
  template_dict: dict,
  subject: p_subject.PirelSubject,
  current_ruleset: str
) -> List[str]:
  '''
  RETURN All possible translation rules inferred from all possible translations of `tsp`.
  NOTE may return zero translation rules
  '''

  logger.debug(f'Starting p.pirel.learn_trans_rules_from_tsp_with_retries (num_attempts={p_consts.LEARN_RULES_FROM_TSP_NUM_ATTEMPTS})')

  attempt_idx = 0
  while attempt_idx < p_consts.LEARN_RULES_FROM_TSP_NUM_ATTEMPTS:
    attempt_idx += 1
    logger.debug(f'Attempting to learn some translation rules from a TSP #{attempt_idx}')
    try:
      trules_list = learn_trans_rules_from_tsp(tsp, template_dict, subject, current_ruleset)
      return trules_list
    except p_llm_gen.NoTransPairsFromTSPError as err:
      logger.warning('Attempt to learn translation rules from TSP failed')
    except NoTransRulesFromTSPError as err:
      logger.warning('Attempt to learn translation rules from TSP failed')

  msg = f'Spent {p_consts.LEARN_RULES_FROM_TSP_NUM_ATTEMPTS} attempts and did not learn any translation rules from TSP.'
  logger.warning(msg)
  return []


def init_tsps(subject: p_subject.PirelSubject, template_dict: dict) -> List[Tuple[str, str]]:
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


def get_partial_program(subject: p_subject.PirelSubject, current_ruleset: str, template_dict: dict) -> str:
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

  def _append_hacky_rules(current_ruleset: str, problematic_node_type: str, secret_identifier: str) -> str:
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
      current_ruleset = current_ruleset + f'\n\n{hacky_rule}'
    return current_ruleset

  def _post_process_partial_program_remove_excess_replace_vars(partial_program: str) -> str:
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
  new_trans_rules = _append_hacky_rules(current_ruleset, prob_ntype_main, p_consts.PAR_PROG_PROB_NODE_REPLACE)
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
    partial_program = _post_process_partial_program_remove_excess_replace_vars(tar_code)
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
    new_trans_rules = _append_hacky_rules(new_trans_rules, prob_ntype_remaining, p_consts.PAR_PROG_DUMMY_IDENTIFIER)

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
      partial_program = _post_process_partial_program_remove_excess_replace_vars(tar_code)
      logger.debug(f'SUCCESS. Partial program generation is complete. num_loops={loop_counter}')
      logger.debug(f'Partial program is:\n{partial_program}')
      return partial_program
    except d_grammar_expand.TranslationRuleNotFoundException as exc:
      templates_dict = exc.get_templates_dict()

    logger.debug(f'Partial program generation loop #{loop_counter} ended')
    loop_counter += 1


def init_template_dict(subject: p_subject.PirelSubject, current_ruleset: str, templates_dict: dict) -> dict:

  def _rerun_translation_for_context(subject: p_subject.PirelSubject, current_ruleset: str, template_origin: str) -> dict:
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
    try:
      _ = duoglot_translate_wrapper(
        template_origin,
        subject.src_lang,
        subject.tar_lang,
        current_ruleset,
        subject.auto_backward,
        subject.choices,
        subject_name=subject.name,
      )
    except d_grammar_expand.TranslationRuleNotFoundException as exc:
      templates_dict = exc.get_templates_dict()
      template_idx = templates_dict['num_templates'] - 1
      return templates_dict[template_idx]
    raise RuntimeError('DuoGlot should have failed to translate the context code')

  logger.debug('Starting template_dict initialization')

  # in cases when templates_dict is loaded from str, keys are strings
  _valid_template_idx = p_utils.to_int(templates_dict['num_templates']) - 1
  template_dict = templates_dict.get(_valid_template_idx) or templates_dict.get(str(_valid_template_idx))
  p_utils.log_json_time(f'{subject.name}_TEMPLATE_DICT_0_init.json', template_dict)

  # Rerun DuoGlot translation to obtain `template_dict`
  # for the context code snippet, not the entire program.
  # This is done to get the updated values for
  # `context_node_id`, `problematic_node_id`, and `problematic_node_path`
  template_dict = _rerun_translation_for_context(subject, current_ruleset, template_dict['template_origin'])
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
  template_dict = _rerun_translation_for_context(subject, current_ruleset, template_dict['template_origin'])
  p_utils.log_json_time(f'{subject.name}_TEMPLATE_DICT_4_context_2.json', template_dict)

  # prepare partial program
  partial_program = get_partial_program(subject, current_ruleset, template_dict)
  template_dict['partial_program'] = partial_program
  p_utils.log_json_time(f'{subject.name}_TEMPLATE_DICT_5_par_prog.json', template_dict)

  # `src_program` is needed for a prompt that uses it as a reference
  template_dict['src_program'] = subject.src_main_code
  p_utils.log_json_time(f'{subject.name}_TEMPLATE_DICT_6_src_program.json', template_dict)

  # prepare pre-context of the context node of the problematic node
  # NOTE pre-context is used in translation rule validation
  # pre_context = get_pre_context_global(subject, templates_dict)
  # template_dict['pre_context'] = pre_context
  # p_utils.log_json_time(f'{subject.name}_TEMPLATE_DICT_7_pre_context_FINAL.json', template_dict)

  logger.debug('Finished template_dict initialization')
  logger.debug(f'template_dict:\n{json.dumps(template_dict, indent=2)}')
  return template_dict


def learn_trans_rules_for_prob_node(
  subject: p_subject.PirelSubject,
  current_ruleset: str,
  templates_dict: dict
) -> List[str]:
  '''
  Run PiREL translation rule learning module for a problematic node.
  PRE There is a translation error.
  RETURN [translation_rules]
  RAISE `CannotLearnRulesForProblematicNode` if cannot generate a translation rule.
  Our goal is to never raise this error
  '''

  logger.debug(f'Starting p_pirel.learn_trans_rules_for_prob_node for "{subject.name}"')
  p_utils.log_json_time(f'{subject.name}_args-learn_trans_rules_for_prob_node.json', locals())

  # ~~~ initialize template_dict and TSPs
  template_dict = init_template_dict(subject, current_ruleset, templates_dict)
  tsps = init_tsps(subject, template_dict)

  # ~~~ iterate over TSPs (from abstract to concrete)
  num_useful_tsps = 0
  all_trules_list : List[str] = []
  for tsp_idx, tsp in enumerate(tsps, start=1):
    msg = (
      f'Learning translation rules using TSP ({tsp_idx}/{len(tsps)}):\n'
      f'tsp.id = {tsp_idx}\n'
      f'{json.dumps(tsp, indent=2)}\n')
    logger.info(msg)

    trules_list = learn_trans_rules_from_tsp_with_retries(tsp, template_dict, subject, current_ruleset)
    if len(trules_list) == 0:
      msg = (
        f'Skipping a TSP: no translation rules were learnt from it (tsp.id = {tsp_idx}):\n'
        f'{json.dumps(tsp, indent=2)}\n')
      logger.debug(msg)
      continue

    num_useful_tsps += 1
    all_trules_list.extend(trules_list)
    if num_useful_tsps >= p_consts.MAX_NUM_USEFUL_TSPS:
      break

  if len(all_trules_list) > 0:
    return all_trules_list

  msg = (
    f'Could not learn any valid translation rules to translate\n'
    f'the problematic node with any of the {len(tsps)} TSPs.\n'
    f'problematic_node_type = "{template_dict["problematic_node_type"]}".\n'
    f'len(tsps) = {len(tsps)}\n')
  logger.critical(msg)
  raise CannotLearnRulesForProblematicNode(msg)


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


def get_statement_node_text(node: pds.PirelNode) -> str:
  '''
  RETURN text of the statement node.
  '''
  text = node.get_text()
  text = p_utils.deindent(text, p_utils.count_leading_spaces(text))
  return text


def simplify_statement_node_text(node: pds.PirelNode) -> str:
  '''
  Replaces children of `block` nodes with a pass statement.
  '''
  text = get_statement_node_text(node)
  tree = pvpy.Tree.from_str(text)
  sn_simplifier = pvpy.StatementNodeSimplifier()
  sn_simplifier.visit(tree.root_node)
  pp = pvpy.PrettyPrinter(indent_with='    ')
  simplified_text = pp.visit(tree.root_node)
  return simplified_text


def get_statement_node_by_id(src_main_code: str, lang: str, node_id: int) -> pds.PirelNode:
  '''
  Given an id of the statement node, return the node from the source code.
  '''
  tree = pds.PirelTree.from_code_str(src_main_code, lang)
  node = tree.get_root_node().get_node_by_id(node_id)
  return node


def learn_trans_rules_for_statement_node(
  subject: p_subject.PirelSubject,
  current_ruleset_obj: p_ruleset.Ruleset,
  statement_nid: int
) -> None:
  '''
  NOTE adds new translation rules to the current_ruleset_obj.
  '''

  '''
  We have a loop that iterates over the nodes in the AST of a statement node.
  Learning rules to translate the statement node and obtain some candidate translation
  (not necessarily plausible) signals that we can stop the loop.
  That is the reason for the first simplification step in the pipeline:
  simplifying blocks (body/scope node) of compound statements.
  If we keep the blocks of compound nodes as they are, then the loop will
  try to obtain translation rules for all the nodes in the block.
  '''
  statement_node = get_statement_node_by_id(subject.src_main_code, subject.src_lang, statement_nid)
  simple_ntext = simplify_statement_node_text(statement_node)

  '''
  At this point, we may have:
  1. no translation rules to handle the statement node
  2. some translation rules to handle the statement node
  3. all translation rules to handle the statement node
  The goal of this loop is to learn all translation rules to handle the statement node.

  In cases when we have some/all translation rules, we need to
  distinguish them from the ones that will be newly learned.
  If a rule is invalid (as will be decided after this loop):
  1. we keep it in the ruleset, if it was previously learned
  2. we remove it from the ruleset, if it was newly learned
  NOTE for now, we keep all the rules in the ruleset.
  '''
  statement_subject_dict_config = p_utils.read_yaml(p_consts.STAT_NODE_CONF_FPATH)
  statement_subject_dict_config['src_program'] = simple_ntext
  statement_subject = p_subject.PirelSubject.from_dict_config(statement_subject_dict_config)

  iteration = 0
  while True:
    iteration += 1

    '''
    Attempt to translate the statement code using the current ruleset.
    If it succeeds, then we break out of the loop.
    If it fails with TranslationRuleNotFoundException, then we learn rules
    to address the problematic node.
    If it fails with some other exception, then this error is bubbled up
    to the caller.
    '''
    templates_dict = None
    try:
      duoglot_result_dict = duoglot_translate_wrapper(
        simple_ntext,
        statement_subject.src_lang,
        statement_subject.tar_lang,
        current_ruleset_obj.to_string(),
        statement_subject.auto_backward,
        statement_subject.choices,
        subject_name=statement_subject.name,
      )
      break
    except d_grammar_expand.TranslationRuleNotFoundException as exc:
      templates_dict = exc.get_templates_dict()

    '''
    At this point we have a problematic node that we cannot translate.
    We need to learn translation rules for this node.
    '''
    assert templates_dict is not None, 'TranslationRuleNotFoundException must have templates_dict'
    trules_list = learn_trans_rules_for_prob_node(statement_subject, current_ruleset_obj.to_string(), templates_dict)
    problematic_node_id = templates_dict['problematic_node_id']
    for trule in trules_list:
      current_ruleset_obj.prepend_rule(p_ruleset.UncheckedRule.from_str(trule, problematic_node_id, statement_nid))

  '''
  At this point, we have enough rules to obtain some translation of the
  statement node. Now it's time to validate the translation rules, and
  if necessary launch an error correction module to fix the problematic rules.
  Fixing is done by replacing the problematic rules with the new ones.
  '''
  validated_ruleset_obj = validate_translation_rules_for_statement_node(
    subject,
    statement_subject,
    current_ruleset_obj,
    statement_nid,
    enable_error_recovery=True
  )
  current_ruleset_obj = validated_ruleset_obj


def can_be_context_node(node: pds.PirelNode, lang: str) -> bool:
  '''
  A node is a context node if AST of its text,
  when parsed on its own, is isomorphic to itself.
  Refer to p_templates._validate_template() for more information.
  '''
  # must be non-terminal
  if node.is_terminal():
    return False
  # node text must not have errors when parsed as it is
  if p_utils.does_have_parse_error(node.get_text(), lang):
    return False
  # parse the node text as a program on its own
  ast_text, ast_ann = d_ast_parse.parse_text_dbg(node.get_text(), lang, keep_text=True)
  tree = pds.PirelTree(ast_text, ast_ann)
  # there should be exactly one context node
  if len(tree.get_root_node().get_children()) != 1:
    return False
  context_node = tree.get_root_node().get_children()[0]
  # context node must be isomorphic to the original node
  if not node.is_type_isomorphic_to(context_node):
    return False
  return True


def get_statement_nodes_PY(source_program: str, lang: str) -> List[pds.PirelNode]:
  '''
  Statement nodes are primary units of code in the source code.
  In other words, a source code is a sequence of statement nodes.
  '''
  def _rec_pre_order(node: pds.PirelNode, lang: str) -> None:
    nonlocal nodes
    if can_be_context_node(node, lang):
      nodes.append(node)
    for child in node.get_children():
      _rec_pre_order(child, lang)

  tree = pds.PirelTree.from_code_str(source_program, lang)
  nodes : List[pds.PirelNode] = []

  _rec_pre_order(tree.get_root_node(), lang)

  # hacky: remove function definitions as we have rules to translate their headers
  nodes = [n for n in nodes if n.get_ts_node_type() != 'function_definition']

  return nodes


def learn_trans_rules_for_subject(
  subject: p_subject.PirelSubject,
  starting_ruleset: str
) -> str:
  '''
  RETURN Learned translation rules.
  RAISE All errors propagate to the caller.
  '''

  logger.info(f'Starting translation of "{subject.name}"')
  current_ruleset_obj = p_ruleset.Ruleset.from_starting_ruleset(starting_ruleset)
  p_utils.log_file_time(f'{subject.name}_starting-ruleset.snart', current_ruleset_obj.to_string())

  '''
  Iterate over statement nodes (simple statements, compound statements).
  It happens that the statement nodes are also context nodes for any problematic node.
  Using this relation between context nodes and statement nodes,
  we will make a list of such nodes.
  '''
  statement_nodes = get_statement_nodes_PY(subject.src_main_code, subject.src_lang)
  for sn_idx, statement_node in enumerate(statement_nodes, start=1):

    '''
    The following function call mutates the `current_ruleset_obj`
    by adding the learned translation rules.
    '''
    learn_trans_rules_for_statement_node(subject, current_ruleset_obj, statement_node.get_id())

  return current_ruleset_obj.to_string()


# TEST HARNESSES
def _test_learn_trans_rules_for_prob_node():
  '''
  def learn_trans_rules_for_prob_node(
    subject: p_subject.PirelSubject,
    current_ruleset: str,
    templates_dict: dict
  ) -> list:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_learn_trans_rules_for_prob_node_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  subject = p_subject.PirelSubject.from_dict_config(json.loads(args_dict['subject']))
  current_ruleset = args_dict['current_ruleset']
  templates_dict = args_dict['templates_dict']

  result = learn_trans_rules_for_prob_node(subject, current_ruleset, templates_dict)
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
  except Exception as exc:
    p_utils.write_tmp_json('dbg_history.json', exc.dbg_history)
    print(f'Unexpected error: {exc}')


def _test_get_pre_context():
  '''
  def get_pre_context(src_main_code: str, lang: str, statement_nid: int) -> str:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_get_pre_context_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  src_main_code = args_dict['src_main_code']
  lang = args_dict['lang']
  statement_nid = args_dict['statement_nid']

  pre_context = get_pre_context(src_main_code, lang, statement_nid)
  print(f'Pre-context for statement node {statement_nid}:\n{pre_context}')


if __name__ == '__main__':
  _test_learn_trans_rules_for_prob_node()
  # _test_duoglot_translate_wrapper()
  # _test_get_pre_context()
