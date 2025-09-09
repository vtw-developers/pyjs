import asyncio
import json
from typing import Dict, List, Optional, Tuple, Set

import d_ast_parse
import d_grammar_rules
import p_consts
import p_llm_gen
import p_pirel
import p_ruleset
import p_rule_applicator as prapp
import p_subject
import p_tree_log as ptlog
import p_utils
import p_visitor as pvis
import p_visitor_py as pvpy


logger = p_utils.setup_logger(__name__)


class NoRuleToHandleRangeCursorError(Exception): pass
class UnhandledRangeCursorExistsError(Exception): pass
class RuleCombinationsExhaustedError(RuntimeError): pass
class AllRulesInMatcherGroupImplausibleError(RuntimeError): pass
class ExprLogStatHasParseError(RuntimeError): pass
class ExprLogStatContextError(RuntimeError): pass
class QueueInfiniteLoopError(RuntimeError): pass


# GENERATING READONLY CHOICES LIST
def match_rule_to_range_cursor(
  matcher: list,
  range_cursor: tuple
) -> dict:
  '''
  Match matcher to range_cursor and return a match object.
  This function is copied from d_grammar_expand.TransSession._try_get_expansion_if_match_on_slot()

  PARAM matcher: matcher of a translation rule
  PARAM range_cursor: internal data structure used in TransSession class.

  RETURN a match object {is_matched: bool, slot_cursors: list}
  '''
  def _is_anno_compatible(matcher_anno, intree_anno):
    matcher_anno_dict = {x[0]:x[1] for x in matcher_anno[1:]}
    intree_anno_dict = {x[0]:x[1] for x in intree_anno[1:]}
    for key in matcher_anno_dict:
      if key not in intree_anno_dict: return False
      if matcher_anno_dict[key] != intree_anno_dict[key]: return False
    return True

  def _try_match_rec_inner_fun(
    range_cursor,
    range_cursor_idx: int,
    matcher,
    matcher_idx: int
  ) -> bool:
    '''
    PARAMETERS:
    range_cursor:             Slot.range_cursor           Tuple[ List[src_ast] , int , int ]
    range_cursor_idx:         int                         start index in the AST list
    matcher:                  list                        [['"py.argument_list"', '"*"'], '"*"']
    matcher_idx:              int                         index in the matcher

    LOCALS:
    current_matcher_elem:     list                        ['"py.argument_list"', '"*"']
    matcher_operator:         str                         '"py.argument_list"'  # with double quotes as in rules
    current_matcher_type:     str                         'py.argument_list'  # without double quotes

    returns bool
    '''

    nonlocal slot_cursors

    # assert range_cursor[2] <= len(range_cursor[0])
    if range_cursor_idx >= range_cursor[2] and matcher_idx >= len(matcher):
      return True

    # 1 matcher element is empty
    if matcher_idx >= len(matcher):
      # the rest of the cursor must all be terminals
      for visit_cur_idx in range(range_cursor_idx, range_cursor[2]):
        visit_elem = range_cursor[0][visit_cur_idx]
        if isinstance(visit_elem, str): continue
        else: return False  # contains non terminal
      return True  # loop done. All of them are terminals.

    # 2 matcher element is not empty
    assert len(matcher) > 0
    current_matcher_elem = matcher[matcher_idx]

    # case 1 current_matcher_elem
    if current_matcher_elem == '"*"':
      slot_cursors.append((range_cursor[0], range_cursor_idx, range_cursor[2]))
      return True

    # case 2 current_matcher_elem
    elif current_matcher_elem == '"."':
      # everything until the next NT is a cursor
      # everything after the next NT would be the rest to match
      split_idx = None
      for visit_cur_idx in range(range_cursor_idx, range_cursor[2]):
        visit_elem = range_cursor[0][visit_cur_idx]
        if d_ast_parse.is_elem_non_terminal(visit_elem):
          split_idx = visit_cur_idx + 1
          break

      # NT not found
      if split_idx is None:
        return False

      # NT found, cursor endswith NT
      slot_cursors.append((range_cursor[0], range_cursor_idx, split_idx))
      return _try_match_rec_inner_fun(
        range_cursor,  # range_cursor
        split_idx,  # range_cursor_idx
        matcher,  # matcher
        matcher_idx + 1  # matcher_idx
      )

    # case 3 current_matcher_elem
    elif current_matcher_elem == '"_val_"':
      assert len(matcher) == 1
      is_invalid = len(range_cursor[0]) != 3 or (range_cursor[2] - range_cursor[1]) != 1 or range_cursor_idx != 2
      assert not is_invalid, 'UNEXPECTED range_cursor'
      return True

    # case 4 current_matcher_elem
    elif current_matcher_elem == '"_str_"':
      if range_cursor_idx >= range_cursor[2]:
        return False # TOCHECK: out of length is failed to match.
      current_range_elem = range_cursor[0][range_cursor_idx]
      if not isinstance(current_range_elem, str):
        return False
      return _try_match_rec_inner_fun(
        range_cursor,  # range_cursor
        range_cursor_idx + 1,  # range_cursor_idx
        matcher,  # matcher
        matcher_idx + 1  # matcher_idx
      )

    # case 6 current_matcher_elem
    elif current_matcher_elem == '"_anno_"':
      current_range_elem = range_cursor[0][range_cursor_idx]
      assert isinstance(current_range_elem, list), '_anno_ meet none-annotation element: Not a list.'
      assert current_range_elem[0] == "anno", \
        '_anno_ meet none-annotation element: elem head: ' + current_range_elem[0]
      return _try_match_rec_inner_fun(
        range_cursor,  # range_cursor
        range_cursor_idx + 1,  # range_cursor_idx
        matcher,  # matcher
        matcher_idx + 1  # matcher_idx
      )

    # case 7 current_matcher_elem (non-terminal) not direct string, must be a list (all prev if's are False)
    assert isinstance(current_matcher_elem, list)
    matcher_operator = current_matcher_elem[0]

    # case 7.1
    if range_cursor_idx >= range_cursor[2]:
      if matcher_operator == "val" or matcher_operator == "str" or matcher_operator.startswith('"'):
        return False
      elif matcher_operator == "nostr":
        return _try_match_rec_inner_fun(
          range_cursor,  # range_cursor
          range_cursor_idx,  # range_cursor_idx
          matcher,  # matcher
          matcher_idx + 1  # matcher_idx
        )
      raise ValueError("UNEXPECTED range_cursor_idx out of length")

    # case 7.2
    if matcher_operator == "val":
      assert len(current_matcher_elem) == 2
      match_val = current_matcher_elem[1]
      is_invalid = len(range_cursor[0]) != 3 or (range_cursor[2] - range_cursor[1]) != 1 or range_cursor_idx != 2
      if is_invalid:
        print("# UNEXPECTED range_cursor for val match: ", range_cursor, range_cursor_idx)
        assert "UNEXPECTED range_cursor for val match" == 0
      range_val = range_cursor[0][range_cursor_idx]
      if not isinstance(range_val, str) and not isinstance(range_val, int) and not isinstance(range_val, float):
        return False
      if str(range_val) == str(match_val):
        return True
      return False

    # case 7.3
    elif matcher_operator == 'str':
      assert len(current_matcher_elem) == 2
      match_val = current_matcher_elem[1]
      should_be_str_val = range_cursor[0][range_cursor_idx]

      # @satbek: skip `anno` in range_cursor when it's matched by `str`
      # for reference: L0004 (leetcode), long rule
      if isinstance(should_be_str_val, list) and len(should_be_str_val) > 0 and should_be_str_val[0] == 'anno':
        return _try_match_rec_inner_fun(
          range_cursor,  # range_cursor
          range_cursor_idx + 1,  # range_cursor_idx
          matcher,  # matcher
          matcher_idx  # matcher_idx
        )

      if not isinstance(should_be_str_val, str):
        return False
      if str(should_be_str_val) != str(match_val):
        return False
      return _try_match_rec_inner_fun(
        range_cursor,  # range_cursor
        range_cursor_idx + 1,  # range_cursor_idx
        matcher,  # matcher
        matcher_idx + 1  # matcher_idx
      )

    # case 7.4
    elif matcher_operator == "nostr":
      assert len(current_matcher_elem) == 1
      should_not_be_str_val = range_cursor[0][range_cursor_idx]
      if isinstance(should_not_be_str_val, str):
        return False
      return _try_match_rec_inner_fun(
        range_cursor,  # range_cursor
        range_cursor_idx,  # range_cursor_idx
        matcher,  # matcher
        matcher_idx + 1  # matcher_idx
      )

    # case 7.5
    elif matcher_operator == "anno":
      should_be_anno = range_cursor[0][range_cursor_idx]
      assert isinstance(should_be_anno, list), '(anno ...) meet none-annotation element: Not a list.'
      assert should_be_anno[0] == "anno", '(anno ...) meet none-annotation element: elem head: ' + should_be_anno[0]
      if not _is_anno_compatible(current_matcher_elem, should_be_anno):
        return False
      return _try_match_rec_inner_fun(
        range_cursor,  # range_cursor
        range_cursor_idx + 1,  # range_cursor_idx
        matcher,  # matcher
        matcher_idx + 1  # matcher_idx
      )

    # case 7.6 not special operators, must be grammar NT constructs
    assert matcher_operator.startswith('"'), 'UNEXPECTED matcher_operator: ' + matcher_operator
    current_matcher_type = matcher_operator[1:-1]
    assert current_matcher_type != "fragment" and current_matcher_type != "anno"

    for visit_cur_idx in range(range_cursor_idx, range_cursor[2]):
      visit_elem = range_cursor[0][visit_cur_idx]

      # this is not an NT. It is a T. We are currently matching against an NT.
      if isinstance(visit_elem, str):
        continue
      # we are currently matching against NT. anno if not caputured in earlier cases, in this case it will be skipped.
      if visit_elem[0] == "anno":
        continue

      assert d_ast_parse.is_elem_non_terminal(visit_elem)
      if visit_elem[0] == current_matcher_type:
        # check if the matching element is matched
        children_matcher = current_matcher_elem[1:]
        is_elem_matching = _try_match_rec_inner_fun(
          (visit_elem, 2, len(visit_elem)),  # range_cursor
          2,  # range_cursor_idx
          children_matcher,  # matcher
          0  # matcher_idx
        )

        if not is_elem_matching:
          return False

        return _try_match_rec_inner_fun(
          range_cursor,  # range_cursor
          visit_cur_idx + 1,  # range_cursor_idx
          matcher,  # matcher
          matcher_idx + 1  # matcher_idx
        )

      # mismatch
      return False

    # no match or mismatch
    return False

  assert matcher[0] == 'fragment', 'UNEXPECTED matcher: ' + str(matcher)
  slot_cursors = []

  is_matched = _try_match_rec_inner_fun(
    range_cursor,
    range_cursor[1],
    matcher[1:],
    0
  )

  return {
    'matcher': matcher,
    'range_cursor': range_cursor,
    'is_matched': is_matched,
    'slot_cursors': slot_cursors
  }


def rules_contains(rules: List[p_ruleset.TRuleBase], rule: p_ruleset.TRuleBase) -> bool:
  '''
  Check if the rules list contains the rule.
  '''
  for r in rules:
    if r == rule:
      return True
  return False


def rules_deduplicate(rules: List[p_ruleset.TRuleBase]) -> List[p_ruleset.TRuleBase]:
  '''
  Deduplicate a list of translation rules.
  '''
  deduplicated = []
  for rule in rules:
    if not rules_contains(deduplicated, rule):
      deduplicated.append(rule)
  logger.debug(
    f'Number of rules before deduplication: {len(rules)}\n'
    f'Number of rules after deduplication: {len(deduplicated)}\n'
    f'Number of deduplicated rules: {len(rules) - len(deduplicated)}')
  return deduplicated


def rules_intersection(
  rules_a: List[p_ruleset.TRuleBase],
  rules_b: List[p_ruleset.TRuleBase]
) -> List[p_ruleset.TRuleBase]:
  '''
  Return a list of rules that are in both rules_a and rules_b.
  '''
  intersection = []
  for rule_a in rules_a:
    for rule_b in rules_b:
      if rule_a == rule_b:
        intersection.append(rule_a)
  return intersection


def rules_group_by_matcher(rules: List[p_ruleset.TRuleBase]) -> Dict[str, List[p_ruleset.TRuleBase]]:
  '''
  Group rules by their matcher signature.
  '''
  matcher_groups = {}
  for rule in rules:
    matcher_signature = rule.get_matcher_signature()
    if matcher_signature not in matcher_groups:
      matcher_groups[matcher_signature] = []
    matcher_groups[matcher_signature].append(rule)
  return matcher_groups


def assert_matchers_match(matcher_group: List[p_ruleset.TRuleBase]) -> None:
  '''
  Assert that all rules in the list have the same matcher signature.
  Assert that rule idx are sorted in ascending order.
  PARAM matcher_group: a list of TRuleBase objects.
  '''
  assert len(matcher_group) > 0, 'Expected at least one rule'
  first_rule_signature = matcher_group[0].get_matcher_signature()
  for rule in matcher_group[1:]:
    assert rule.get_matcher_signature() == first_rule_signature, \
      f'Expected all rules to have the same matcher signature, got {rule.get_matcher_signature()}'


def _choicable_node_get_context_node(node: pvis.AbstractNode) -> pvis.AbstractNode:
  '''
  Given a choicable node, return its context node.
  Context node is the nearest ancestor that is either
  an ExpressionStatementNode, IfStatementNode, or WhileStatementNode.
  '''

  _CONTEXT_NODE_TYPES = (
    pvpy.ExpressionStatementNode,
    pvpy.ForStatementNode,
    pvpy.IfStatementNode,
    pvpy.ReturnStatementNode,
    pvpy.WhileStatementNode
  )
  is_context_node = lambda node: \
    isinstance(node, _CONTEXT_NODE_TYPES)

  cursor = node.parent
  while cursor is not None:
    if is_context_node(cursor):
      return cursor
    cursor = cursor.parent
  raise ValueError('No context node found')


def _create_log_stat_str_for_expr(
  matched_range_cursor: tuple,
  dgann: dict,
  src_main_code: str,
  matcher_group: List[p_ruleset.TRuleBase],
  ruleset: p_ruleset.Ruleset
) -> str:
  '''
  Return a log statement that logs the AST.
  If we cannot validate the matched_range_cursor with the given matcher_group,
  then we need to mark the matching rules as unverifiable for the matched_range_cursor.
  '''
  matched_ast_str = d_ast_parse.range_cursor_pretty_print(matched_range_cursor, dgann, src_main_code)
  log_stat_str = f'myexactlog({matched_ast_str})'

  '''
  Make sure that the log statement is parseable.
  Examples where there are parse errors:
  a = m[i:j]
        ^^^
  myexactlog(i:j)
  '''
  if p_utils.does_have_parse_error(log_stat_str, 'py'):
    logger.debug(
      f'Expression "{matched_ast_str}" is unverifiable due to '
      f'parse error in log statement "{log_stat_str}".')
    for trule in matcher_group:
      ruleset.update_unverifiable_rules(matched_ast_str, trule)
    raise ExprLogStatHasParseError()

  '''
  Make sure that the logged expression has the same AST
  structure as the original expression.
  ["py.module", 0, ["py.expression_statement", 1, ["py.call", 2,
    ["py.identifier", 3, "\"myexactlog\""],
    ["py.argument_list", 4,
      "\"(\"",
      <sub-AST for logged expression is rooted here>,
      "\")\""
    ]
  ]]]
  '''
  matched_ast = d_ast_parse.range_cursor_to_ast_node(matched_range_cursor)
  log_stat_ast, _ = d_ast_parse.parse_text_dbg(log_stat_str, 'py')
  logged_expr_ast = log_stat_ast[2][2][3][3]

  if not d_ast_parse.are_nodes_equal(matched_ast, logged_expr_ast):
    logger.debug(
      f'Expression "{matched_ast_str}" is unverifiable due to '
      f'tree non-isomorphism in log statement "{log_stat_str}".')
    for trule in matcher_group:
      ruleset.update_unverifiable_rules(matched_ast_str, trule)
    raise ExprLogStatContextError()

  return log_stat_str


def _create_subject_for_expr(
  src_test_script: str,
  is_three_split: bool,
  translation_rules_test_code: str,
  rules_w_str: str,
  ruleset: p_ruleset.Ruleset
) -> p_subject.PirelSubject:
  '''
  Create a subject for validating a rule for expression.
  '''

  # all attributes of PirelSubject instance set explicitly
  benchmark_name = 'n/a'
  name = 'expr'
  src_program = src_test_script
  src_lang = 'py'
  tar_lang = 'js'
  translation_rules_main_code = \
    rules_w_str + '\n\n' + \
    p_utils.read_text(p_consts.LOG_STAT_RULE_FPATH) + '\n\n' + \
    p_utils.read_text(p_consts.RULE_VAL_EXTRA_RULES_FPATH)
  # translation_rules_test_code  # already set
  auto_backward = True
  choices = {'type': 'ASTNODE', 'choices_list': []}
  readonly_choices_list = []

  # create a subject instance
  expr_subject = p_subject.PirelSubject(
    benchmark_name, name, src_program, src_lang, tar_lang, is_three_split)
  expr_subject.translation_rules_main_code = translation_rules_main_code
  expr_subject.translation_rules_test_code = translation_rules_test_code
  expr_subject.auto_backward = auto_backward
  expr_subject.choices = choices
  expr_subject.readonly_choices_list = readonly_choices_list

  # override readonly_choices_list with verified rules
  expr_subject.readonly_choices_list = ruleset.get_choices_list_from_verified_rules(
    expr_subject.get_src_main_code())

  return expr_subject


def get_rules_that_handle_range_cursor_rec(
  range_cursor: tuple,
  ruleset: p_ruleset.Ruleset,
  dgann: dict,
  src_main_code: str,
) -> Optional[List[p_ruleset.TRuleBase]]:
  '''
  Recursively retrieve both verified and unverifiable rules
  that can handle the range cursor.

  NOTE returns ALL VERIFIED AND UNVERIFIABLE rules
  which defeats the purpose of identifying the failing matcher group.
  TODO This can/should be optimized.
  '''
  trules : List[p_ruleset.TRuleBase] = []
  range_cursor_unparsed = d_ast_parse.range_cursor_pretty_print(
    range_cursor, dgann, src_main_code)
  if ruleset.verified_rule_exists(range_cursor_unparsed):
    trules.append(ruleset.get_verified_rule(range_cursor_unparsed))
  if ruleset.unverifiable_rules_exist(range_cursor_unparsed):
    trules.extend(ruleset.get_unverifiable_rules(range_cursor_unparsed))

  # base case: no rule for range cursor not found
  if len(trules) == 0:
    return None

  assert ruleset.verified_rule_exists(range_cursor_unparsed) != \
    ruleset.unverifiable_rules_exist(range_cursor_unparsed), \
    'Expected either verified or unverifiable rules to exist, but not both.'

  # get all slot cursors of range cursor
  all_slot_cursors = []  # exist under the range_cursor
  for trule in trules:
    match_obj = match_rule_to_range_cursor(trule.rule_parsed['match'], range_cursor)
    assert match_obj['is_matched'], 'Expected rule to match the range cursor'
    all_slot_cursors.extend(match_obj['slot_cursors'])

  all_slot_cursors = d_ast_parse.range_cursor_remove_empty(all_slot_cursors)
  all_slot_cursors = d_ast_parse.deduplicate_range_cursors(all_slot_cursors)

  # base case: rule has no slot cursors
  if len(all_slot_cursors) == 0:
    return trules

  # recursive case: rule has slot cursors
  for slot_cursor in all_slot_cursors:
    child_rules = get_rules_that_handle_range_cursor_rec(
      slot_cursor, ruleset, dgann, src_main_code)
    if child_rules is not None:
      trules.extend(child_rules)

  return trules


def _check_for_base_rules(
  matcher_group: List[p_ruleset.TRuleBase],
  matched_range_cursor: tuple,
  ruleset: p_ruleset.Ruleset,
  dgann: dict,
  src_main_code: str
) -> bool:
  '''
  When validating matching rules, check if the matched rules are base rules.
  The logic is this: if a rule that matched a range cursor is a rule
  from starting ruleset, then we don't need to run test based validation
  to verify that rule; we just mark that the range cursor can be
  handled by that rule.
  RETURN True if the matched rules are base rules.
  '''
  logger.debug(f'~~~ Checking if rule(s) in the matcher group are base rules')

  STARTING_RULESET_STR = p_utils.read_text(p_consts.STARTING_RULESET_FPATH)
  starting_ruleset = p_ruleset.Ruleset.from_starting_ruleset(STARTING_RULESET_STR)

  # base rules usually just single rules in their matcher group
  # i.e. there is just a single way to translate a matched AST
  # TODO this needs to be improved
  if len(matcher_group) > 1:
    logger.debug(
      'The matcher group contains more than one rule. '
      'The rules in this group are removed from consideration as base rules.')
    return False

  assert len(matcher_group) == 1, 'Expected exactly one matching rule for base rules'
  matching_rule = matcher_group[0]
  for st_trule in starting_ruleset.rules:
    if st_trule == matching_rule:
      logger.debug(f'Matched rule appears in the starting ruleset: {matching_rule}')
      range_cursor_unparsed = d_ast_parse.range_cursor_pretty_print(
        matched_range_cursor, dgann, src_main_code)
      ruleset.update_verified_rules(range_cursor_unparsed, st_trule)
      return True

  return False


async def _validate_matcher_group_no_intersection(
  matched_range_cursor: tuple,
  matcher_group: List[p_ruleset.TRuleBase],
  subtrees_rules: List[p_ruleset.TRuleBase],
  ruleset: p_ruleset.Ruleset,
  test_script_str: str,
  translation_rules_test_code: str,
  dgann: dict,
  src_main_code: str,
  is_three_split: bool,
) -> None:
  '''
  PARAM matched_range_cursor: range cursor that was matched by the matcher_group.
  PARAM matcher_group: a list of TRuleBase objects that matched the range cursor.
  PARAM subtrees_rules: rules that handle the descending slot cursors
  of the matched range cursor.

  *_no_intersection in the name of this function implies that
  there are no rules in subtrees_rules that handle the matched_range_cursor.
  '''

  logger.debug(f'~~~ starting _validate_matcher_group_no_intersection')
  assert_matchers_match(matcher_group)
  matcher_signature = matcher_group[0].get_matcher_signature()

  '''
  Check if the rule(s) in the matcher_group are base rules.
  If so, we do not need to validate them, since they are already verified.
  '''
  flag_check_base_rule = _check_for_base_rules(
    matcher_group,
    matched_range_cursor,
    ruleset,
    dgann,
    src_main_code
  )
  if flag_check_base_rule:
    logger.debug('Validation is complete. Matcher group is a list of base rules.')
    return

  '''
  From each matcher group, we keep only those that are in subtrees_rules.
  '''
  subtrees_matcher_groups = rules_group_by_matcher(subtrees_rules)
  assert matcher_signature not in subtrees_matcher_groups, 'supposed to be no intersection'

  '''
  rules_wo contains all rules that can handle everything except
  the matched_range_cursor. This is used to validate the matcher_group.
  '''
  joined_matcher_groups = {**subtrees_matcher_groups, **{matcher_signature: []}}
  rules_wo = ruleset.add_all_rules_from_missing_matcher_groups(joined_matcher_groups)
  logger.debug(f'len(rules_wo): {len(rules_wo)}')

  '''
  Add rules from matcher_group to rules_wo and validate them one by one.
  '''
  for idx, rule in enumerate(matcher_group, start=1):
    logger.debug(f'validating rule {idx}/{len(matcher_group)}:\n{rule}')

    rules_w = rules_wo + [rule]
    rules_w_str = '\n\n'.join([str(r) for r in rules_w])
    expr_subject = _create_subject_for_expr(
      test_script_str, is_three_split,
      translation_rules_test_code, rules_w_str, ruleset)

    '''
    If this translation succeeds, it means that the rule is plausible
    with respect to the matched AST.
    '''
    try:
      tar_program_plausible = await prapp.apply_translation_rules(expr_subject)
      range_cursor_unparsed = d_ast_parse.range_cursor_pretty_print(
        matched_range_cursor, dgann, src_main_code)
      ruleset.update_verified_rules(range_cursor_unparsed, rule)
      logger.debug(
        f'Rule {idx}/{len(matcher_group)} is plausible with respect to the matched AST:\n{rule}\n'
        f'Matched AST: "{d_ast_parse.range_cursor_pretty_print(matched_range_cursor, dgann, src_main_code)}"')
      return

    except Exception as err:
      logger.warning(
        f'Error while applying translation rules:\n{p_utils.exception_to_str(err)}\n'
        f'Rule {idx}/{len(matcher_group)} is not plausible with respect to the matched AST:\n{rule}\n'
        f'Matched AST: "{d_ast_parse.range_cursor_pretty_print(matched_range_cursor, dgann, src_main_code)}"')
      continue

  raise AllRulesInMatcherGroupImplausibleError(
    'No plausible translation found for the matched AST with the given ruleset. This is not desired.')


async def _validate_matcher_group_single_intersection(
  matched_range_cursor: tuple,
  matcher_group: List[p_ruleset.TRuleBase],
  subtrees_rules: List[p_ruleset.TRuleBase],
  ruleset: p_ruleset.Ruleset,
  test_script_str: str,
  translation_rules_test_code: str,
  dgann: dict,
  src_main_code: str,
  is_three_split: bool,
) -> None:
  '''
  PARAM matched_range_cursor: range cursor that was matched by the matcher_group.
  PARAM matcher_group: a list of TRuleBase objects that matched the range cursor.
  PARAM subtrees_rules: rules that handle the descending slot cursors
  of the matched range cursor.

  *_single_intersection in the name of this function implies that
  there is exactly one rule in subtrees_rules that handle the matched_range_cursor.
  '''

  logger.debug(f'~~~ starting _validate_matcher_group_single_intersection')
  assert_matchers_match(matcher_group)
  matcher_signature = matcher_group[0].get_matcher_signature()

  '''
  From each matcher group, we keep only those that are in subtrees_rules.
  '''
  subtrees_matcher_groups = rules_group_by_matcher(subtrees_rules)
  assert matcher_signature in subtrees_matcher_groups, 'supposed to be no intersection'
  assert len(subtrees_matcher_groups[matcher_signature]) == 1, \
    'expected exactly one rule in the matcher group'

  intersect_rule = subtrees_matcher_groups[matcher_signature][0]
  other_rules = [rule for rule in matcher_group if rule != intersect_rule]
  del subtrees_matcher_groups[matcher_signature]

  '''
  rules_wo contains all rules that can handle everything except
  the matched_range_cursor. This is used to validate the matcher_group.
  '''
  joined_matcher_groups = {**subtrees_matcher_groups, **{matcher_signature: []}}
  rules_wo = ruleset.add_all_rules_from_missing_matcher_groups(joined_matcher_groups)
  logger.debug(f'len(rules_wo): {len(rules_wo)}')

  '''
  Add rules from matcher_group to rules_wo and validate them one by one.
  '''
  for idx, rule in enumerate([intersect_rule] + other_rules, start=1):
    logger.debug(f'validating rule {idx}/{len(other_rules) + 1}:\n{rule}')

    rules_w = rules_wo + [rule]
    rules_w_str = '\n\n'.join([str(r) for r in rules_w])
    expr_subject = _create_subject_for_expr(
      test_script_str, is_three_split,
      translation_rules_test_code, rules_w_str, ruleset)

    '''
    If this translation succeeds, it means that the rule is plausible
    with respect to the matched AST.
    '''
    try:
      tar_program_plausible = await prapp.apply_translation_rules(expr_subject)
      range_cursor_unparsed = d_ast_parse.range_cursor_pretty_print(
        matched_range_cursor, dgann, src_main_code)
      ruleset.update_verified_rules(range_cursor_unparsed, rule)
      logger.debug(
        f'Rule {idx}/{len(matcher_group)} is plausible with respect to the matched AST:\n{rule}\n'
        f'Matched AST: "{d_ast_parse.range_cursor_pretty_print(matched_range_cursor, dgann, src_main_code)}"')
      return

    except Exception as err:
      logger.warning(
        f'Error while applying translation rules:\n{p_utils.exception_to_str(err)}\n'
        f'Rule {idx}/{len(matcher_group)} is not plausible with respect to the matched AST:\n{rule}\n'
        f'Matched AST: "{d_ast_parse.range_cursor_pretty_print(matched_range_cursor, dgann, src_main_code)}"')
      continue

  raise AllRulesInMatcherGroupImplausibleError(
    'No plausible translation found for the matched AST with the given ruleset. This is not desired.')


async def validate_matcher_group(
  matched_range_cursor: tuple,
  matcher_group: List[p_ruleset.TRuleBase],
  subtrees_rules: List[p_ruleset.TRuleBase],
  ruleset: p_ruleset.Ruleset,
  src_main_code: str,
  pre_context: str,
  log_stat_str: str,
  src_test_code: Optional[str],
  translation_rules_test_code: str,
  dgann: dict,
) -> None:
  '''
  Validating a matcher group means checking if the rules in the matcher group
  can be applied to the matched range cursor and if they are plausible
  with respect to the matched AST.

  PARAM subtrees_rules: a list of rules that can handle (verified) slot cursors
  under the matched range cursor.

  a = ((15 + (   7 * (math.sqrt(5))   )) / 4) * (math.pow(side, 3))
                 ^^^^^^^^^^^^^^^^^^

  myexactlog(7 * (math.sqrt(5)))

  def test():
    f_gold()
  def f_gold():
    myexactlog(7 * (math.sqrt(5)))
  test()

  NOTE We need to create a test script which combines
  1. the test function - use the test function that we generated previously
  2. the f_gold function
  3. the test function call
  '''
  logger.debug(f'~~~ starting validate_matcher_group')
  assert_matchers_match(matcher_group)

  is_three_split = src_test_code is not None
  expr_src_main_code = p_pirel._create_src_main_code_for_val(
    src_main_code, pre_context, log_stat_str, is_three_split)
  if is_three_split:
    # Create a f_gold() function for the matched AST.
    test_script_str = p_consts.TEST_SCRIPT_TEMPLATE.format(
      test_code=src_test_code,
      main_code=expr_src_main_code,
      test_call_code='test()')
  else:
    test_script_str = expr_src_main_code
  logger.debug(f'test_script_str:\n{test_script_str}')

  '''
  We need to deduplicate the rules in subtrees_rules.
  '''
  subtrees_rules = rules_deduplicate(subtrees_rules)
  logger.debug(f'Number of rules to handle sub-ASTs: {len(subtrees_rules)}')

  '''
  Check if subtrees_rules contains a rule from matcher_group.
  In other words, a rule that handles one of the descending slot cursors,
  can also handle the matched range cursor.
  '''
  reusable_rules = rules_intersection(matcher_group, subtrees_rules)
  logger.debug(f'Number of rules handling sub-ASTs that can also handle the matched AST: {len(reusable_rules)}')

  if len(reusable_rules) == 0:
    await _validate_matcher_group_no_intersection(
      matched_range_cursor,
      matcher_group,
      subtrees_rules,
      ruleset,
      test_script_str,
      translation_rules_test_code,
      dgann,
      src_main_code,
      is_three_split,
    )

  elif len(reusable_rules) == 1:
    await _validate_matcher_group_single_intersection(
      matched_range_cursor,
      matcher_group,
      subtrees_rules,
      ruleset,
      test_script_str,
      translation_rules_test_code,
      dgann,
      src_main_code,
      is_three_split,
    )

  else:
    logger.critical(
      f'The number of reusable rules is {len(reusable_rules)}. '
      f'This case has not yet been implemented.')
    p_utils.log_json_time('locals.json', locals())
    raise NotImplementedError('consider this case')


async def _process_match_obj(
  match_obj: dict,
  matcher_group: List[p_ruleset.TRuleBase],
  ruleset: p_ruleset.Ruleset,
  src_main_code: str,
  pre_context: str,
  src_test_code: Optional[str],
  translation_rules_test_code: str,
  dgann: dict,
) -> None:
  '''
  Process the match object and log the information.
  A match object contains a reference to an AST node that matched some rule.

  PARAM match_obj: {
    'matcher': matcher,  # matcher signature
    'range_cursor': range_cursor,  # range cursor that matches the matcher
    'is_matched': is_matched,  # whether the matcher matches the range cursor
    'slot_cursors': slot_cursors  # list of slot cursors that match the range cursor
  }
  '''
  logger.debug('~~~ Starting match object processing')
  assert match_obj['is_matched'], 'Expected match_obj to be matched'
  matched_range_cursor = match_obj['range_cursor']
  log_stat_str = _create_log_stat_str_for_expr(
    matched_range_cursor, dgann, src_main_code, matcher_group, ruleset)

  '''
  slot_cursors are range_cursors that appear under the range_cursor.
  '''
  slot_cursors = match_obj['slot_cursors']
  slot_cursors = d_ast_parse.range_cursor_remove_empty(slot_cursors)
  logger.debug(f'Matched AST has {len(slot_cursors)} slots')

  '''
  BASE CASE
  The rule is non-recursive (leaf rule). It might be a rule in the starting ruleset.
  '''
  if len(slot_cursors) == 0:
    logger.debug('Matched rule is non-recursive. Validating matching rules.')
    await validate_matcher_group(
      matched_range_cursor,
      matcher_group,
      [],  # subtrees_rules
      ruleset,
      src_main_code,
      pre_context,
      log_stat_str,
      src_test_code,
      translation_rules_test_code,
      dgann
    )
    return

  '''
  RECURSIVE CASE
  The rule is recursive, i.e. it has at least one slot cursor under the matched range cursor.
  Need to check if we can handle all slot cursors.
  '''
  subtrees_rules = []
  for idx, slot_cursor in enumerate(slot_cursors, start=1):
    '''
    Need to check if slot_cursor spans multiple AST nodes. That might be the case
    if matching rule contains a "*" placeholder. For example,
    (match_expand
      (fragment ("py.list" (str "[") "*" (str "]")) "*")
      (fragment ("js.array" (str "[") "*1" (str "]")) "*2")
    )
    that matches
    `[1, 2, 3, 4]`
    '''
    sub_slot_cursors = d_ast_parse.range_cursor_split(slot_cursor)
    if len(sub_slot_cursors) > 1:
      logger.debug(
        f'Slot cursor {idx}/{len(slot_cursors)} has {len(sub_slot_cursors)} '
        f'sub-slot cursors. This is likely due to a "*" in the matcher.')

    for sub_idx, sub_slot_cursor in enumerate(sub_slot_cursors, start=1):
      '''
      We need to check if there are rules that plausibly translate the slot_cursors
      under the matched range_cursor.
      '''
      subtrees_rules = get_rules_that_handle_range_cursor_rec(
        sub_slot_cursor, ruleset, dgann, src_main_code)
      logger.debug(
        f'Slot cursor {sub_idx}/{len(sub_slot_cursors)} {idx}/{len(slot_cursors)} AST: '
        f'"{d_ast_parse.range_cursor_pretty_print(sub_slot_cursor, dgann, src_main_code)}"')

      '''
      If there is no rule that can handle the range_cursor,
      it means we need to check the next matching rule group.
      '''
      if subtrees_rules is None:
        raise NoRuleToHandleRangeCursorError

      logger.debug(f'Number of rules that can handle the slot cursor: {len(subtrees_rules)}')
      subtrees_rules.extend(subtrees_rules)

  '''
  This range_cursor is handled by the rule. Mark it as handled.
  '''
  await validate_matcher_group(
    matched_range_cursor,
    matcher_group,
    subtrees_rules,
    ruleset,
    src_main_code,
    pre_context,
    log_stat_str,
    src_test_code,
    translation_rules_test_code,
    dgann
  )

  logger.debug('~~~ Ended match object processing')


async def process_choicable_range_cursor(
  matcher_group: List[p_ruleset.TRuleBase],
  all_range_cursors: List[Tuple[list, int, int]],
  ruleset: p_ruleset.Ruleset,
  src_main_code: str,
  pre_context: str,
  src_test_code: Optional[str],
  translation_rules_test_code: str,
  dgann: dict,
  processed_match_objs: Dict[str, list],
):
  '''
  PARAM matcher_group: a list of rules that have the same matcher signature.

  NOTE a range cursor is a different representation of an AST node.
  Duoglot-style AST allows us to identify ASTs using their node ids
  and range cursors. We can get an AST from a range cursor, but
  we cannot get a range cursor from an AST node, because range cursors
  need a reference to the parent AST node.
  '''
  logger.debug('~~~ starting process_choicable_range_cursor')

  assert_matchers_match(matcher_group)
  matcher = matcher_group[0].rule_parsed['match']
  matcher_signature = matcher_group[0].get_matcher_signature()
  logger.debug(f'Matcher: {matcher}')

  '''
  Keep only those range cursors that have not been processed yet.
  '''
  all_range_cursors = [
    rc for rc in all_range_cursors
    if d_ast_parse.range_cursor_to_choice_identifier(rc) not in processed_match_objs.get(matcher_signature, [])
  ]
  match_objs = [match_rule_to_range_cursor(matcher, range_cursor) for range_cursor in all_range_cursors]
  match_objs = [match_obj for match_obj in match_objs if match_obj['is_matched']]

  if len(match_objs) == 0:
    logger.debug('No range cursor matches the matcher. Matcher group will be removed from the queue.')
    return

  logger.debug(f'Number of range cursors that match the matcher: {len(match_objs)}')
  flag_unhandled_exists = False

  '''
  Process each matched AST that matched the rule (matcher).
  '''
  for idx, match_obj in enumerate(match_objs, start=1):

    range_cursor = match_obj['range_cursor']
    logger.debug(
      f'Processing match_obj {idx}/{len(match_objs)}:\n'
      f'-> matcher signature: {matcher_signature}\n'
      f'-> matched AST: "{d_ast_parse.range_cursor_pretty_print(range_cursor, dgann, src_main_code)}"')

    # Process the match object
    try:
      await _process_match_obj(
        match_obj,
        matcher_group,
        ruleset,
        src_main_code,
        pre_context,
        src_test_code,
        translation_rules_test_code,
        dgann
      )
      logger.debug('Successfully processed the match_obj.')
      processed_match_objs.setdefault(matcher_signature, []).append(
        d_ast_parse.range_cursor_to_choice_identifier(range_cursor))

    except NoRuleToHandleRangeCursorError:
      logger.debug('Not enough rules to handle the slot cursor. Continuing with the next match_obj.')
      flag_unhandled_exists = True
      continue

    except ExprLogStatHasParseError:
      logger.debug(
        'Logged expression has parse error. Unlinking the range cursor '
        'from matcher group (rules that match this range cursor):\n'
        f'{d_ast_parse.range_cursor_pretty_print(range_cursor, dgann, src_main_code)}')
      processed_match_objs.setdefault(matcher_signature, []).append(
        d_ast_parse.range_cursor_to_choice_identifier(range_cursor))

    except ExprLogStatContextError:
      logger.debug(
        'Logged expression cannot be used as an argument to a log statement '
        '(context issue).\nUnlinking the range cursor '
        'from matcher group (rules that match this range cursor):\n'
        f'{d_ast_parse.range_cursor_pretty_print(range_cursor, dgann, src_main_code)}')
      processed_match_objs.setdefault(matcher_signature, []).append(
        d_ast_parse.range_cursor_to_choice_identifier(range_cursor))

  if flag_unhandled_exists:
    raise UnhandledRangeCursorExistsError


def _get_readonly_choices_list_init(
  src_main_code: str,
  ruleset: p_ruleset.Ruleset,
  is_three_split: bool,
) -> tuple:
  '''
  Given a duoglot-style AST, collect all nodes under AST,
  for which we should "cleverly" generate choices that
  result in a plausible translation.
  RETURN a list of tuples (range cursor, pre-context).
  '''

  '''
  First we collect all nodes that match the overfitted rules.
  Then we pass their node ids to ChoicableNodeExtractor.
  '''
  rc_src_main_code, dgann = d_ast_parse.parse_text_to_range_cursor(src_main_code, 'py')
  if is_three_split:
    assert rc_src_main_code[1] + 1 == rc_src_main_code[2], \
      'range cursor must specify just one node'
    all_range_cursors = d_ast_parse.get_all_range_cursors_under(
      rc_src_main_code)
  else:
    all_range_cursors = d_ast_parse.range_cursor_seq_descending_from_ast(
      rc_src_main_code[0])

  overfitted_stat_nids = set()
  overfitted_rules = ruleset.get_stat_overfitted_rules()
  for rule in overfitted_rules:
    matcher = rule.rule_parsed['match']
    for range_cursor in all_range_cursors:
      match_obj = match_rule_to_range_cursor(matcher, range_cursor)
      if not match_obj['is_matched']:
        continue
      matched_ast = d_ast_parse.range_cursor_to_ast_node(range_cursor)
      assert d_ast_parse.is_elem_non_terminal(matched_ast), 'sanity check'
      stat_nid = matched_ast[1]
      assert isinstance(stat_nid, int), 'sanity check'
      logger.debug(
        f'Will exclude statement node id {stat_nid}:\n'
        f'"{d_ast_parse.range_cursor_pretty_print(range_cursor, dgann, src_main_code)}"\n'
        f'since it matches overfitted rule:\n{rule.to_rule_str()}')
      overfitted_stat_nids.add(stat_nid)

  choicable_nodes = pvpy.ChoicableNodeExtractor.extract_choicable_nodes(
    src_main_code, exclude_statement_nodes_ids=list(overfitted_stat_nids))
  logger.debug(f'There are {len(choicable_nodes)} choicable nodes in:\n{src_main_code}')

  chable_rc_prectxs = []  # choices range cursors with pre-context
  dgast, dgann = d_ast_parse.parse_text_dbg(src_main_code, 'py')

  for i, choicable_node in enumerate(choicable_nodes, start=1):
    choicable_range_cursor = d_ast_parse.get_range_cursor(dgast, choicable_node.get_node_id())
    stat_node = _choicable_node_get_context_node(choicable_node)
    pre_context = p_pirel.get_pre_context(src_main_code, 'py', stat_node.get_node_id())
    pre_context = pvpy.LogStatementRemover.remove_log_statements(pre_context)
    chable_rc_prectxs.append((choicable_range_cursor, pre_context))
    logger.debug(
      f'-> Choicable_node {i}/{len(choicable_nodes)}: '
      f'"{d_ast_parse.range_cursor_pretty_print(choicable_range_cursor, dgann, src_main_code)}"\n'
      f'pre_context:\n{pre_context}')

  return chable_rc_prectxs, dgann


def _is_excluded_range_cursor(
  range_cursor: tuple,
  dgann: dict,
  src_main_code: str
) -> bool:
  '''
  Check if the given range cursor is excluded from consideration.
  '''
  def __pattern_1_recursive_call_to_f_gold(ast: list) -> bool:
    '''
    PARAM ast: duoglot-style AST
    '''
    # must be non-terminal
    if not isinstance(ast, list):
      return False
    ntype = ast[0]
    nid = ast[1]
    assert isinstance(nid, int), 'sanity check'
    if ntype != 'py.call':
      return False
    children = ast[2:]
    ch1 = children[0]
    ch1_type = ch1[0]
    if ch1_type != 'py.identifier':
      return False
    assert len(ch1) == 3, 'sanity check'
    ch_literal = ch1[2]
    if ch_literal == '"f_gold"':
      return True
    return False

  ast = d_ast_parse.range_cursor_to_ast_node(range_cursor)
  if __pattern_1_recursive_call_to_f_gold(ast):
    logger.debug(
      f'Excluding range cursor (recursive call to `f_gold`): '
      f'"{d_ast_parse.range_cursor_pretty_print(range_cursor, dgann, src_main_code)}"')
    return True
  return False


def _filter_range_cursors(
  range_cursors: list,
  dgann: dict,
  src_main_code: str,
  ruleset: p_ruleset.Ruleset
) -> list:
  '''
  Exclude some nodes from consideration.
  All rules that match the removed range cursors must be
  added to unverifiable rules.
  '''
  result = []
  for range_cursor in range_cursors:
    if not _is_excluded_range_cursor(range_cursor, dgann, src_main_code):
      result.append(range_cursor)
      continue
    unparsed_range_cursor = d_ast_parse.range_cursor_pretty_print(range_cursor, dgann, src_main_code)

    # if we reach here, it means the range cursor is excluded
    # matcher_group is a list of rules that share the same matcher
    for matcher_sig, matcher_group in ruleset.matcher_groups.items():
      assert_matchers_match(matcher_group)
      matcher = matcher_group[0].rule_parsed['match']
      match_obj = match_rule_to_range_cursor(matcher, range_cursor)
      if not match_obj['is_matched']:
        continue
      # if we reach here, it means that matcher_group contains rules
      # that match the range_cursor
      logger.debug(
        f'Updating unverifiable rules for range cursor: '
        f'{unparsed_range_cursor}')
      for rule in matcher_group:
        ruleset.update_unverifiable_rules(
          unparsed_range_cursor,
          rule
        )

  return result


async def get_readonly_choices_list(
  src_main_code: str,
  src_test_code: Optional[str],
  translation_rules_test_code: str,
  ruleset: p_ruleset.Ruleset
) -> list:
  '''
  Generate a readonly choices list for the given source code and rules.
  Readonly choices list contains choices to validated rules that result
  in plausible translation. This is much better than blindly iterating
  over all possible rule combinations to get a plausible translation.

  Readonly choices contains choices to right hand side of assignments,
  and conditions of if statements.

  PARAM src_main_code (check p_pirel._create_src_program_for_stat_val()):
  - instrumented with log statements
  - break statements inserted

  NOTE This function should not add or remove rules from the ruleset.
  '''

  p_utils.log_json_time('args-get_readonly_choices_list.json', locals())
  logger.info('readonly-main: Starting generation of read-only choices list')

  '''
  `choicable_range_cursors` - a list of range cursors
  for which we need to create readonly choices list
  that results in a plausible translation.
  retval_0 = ((15 + (7 * (math.sqrt(5)))) / 4) * (math.pow(side, 3))
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  if h < 0 or m < 0 or h > 12 or m > 60:
     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  '''
  chable_rc_prectxs, dgann = _get_readonly_choices_list_init(
    src_main_code, ruleset, src_test_code is not None)

  for i, (choicable_range_cursor, pre_context) in enumerate(chable_rc_prectxs, start=1):

    logger.debug(
      f'readonly-main: processing choicable_range_cursor {i}/{len(chable_rc_prectxs)}: '
      f'"{d_ast_parse.range_cursor_pretty_print(choicable_range_cursor, dgann, src_main_code)}"')

    '''
    Verified or unverifiable rules may already contain rules that can handle
    the choicable_range_cursor. If so, we skip processing it.
    '''
    choicable_range_cursor_unparsed = d_ast_parse.range_cursor_pretty_print(
      choicable_range_cursor, dgann, src_main_code)
    if ruleset.verified_rule_exists(choicable_range_cursor_unparsed):
      logger.debug('Skipping processing of choicable_range_cursor, since it is already handled by verified rules.')
      continue
    if ruleset.unverifiable_rules_exist(choicable_range_cursor_unparsed):
      logger.debug('Skipping processing of choicable_range_cursor, since it is already handled by unverifiable rules.')
      continue

    '''
    Matcher groups are groups of rules that have the same matcher signature.
    We make a queue of matcher groups to process them one by one.
    '''
    queue_matcher_groups = list(ruleset.matcher_groups.values())

    '''
    Each matcher matches to a number of ASTs, in order to avoid
    processing the same matched AST multiple times, we keep
    track of processed match objects.
    '''
    processed_match_objs : Dict[str, list] = {}

    '''
    paramable_ids: a list of parameterable identifiers under choicable_range_cursor.
    test_fn_str: a test function string that will be used to validate translation rules.
    all_range_cursors: a list of all range cursors under choicable_range_cursor.
    This includes the choicable_range_cursor itself and all its subtrees.
    '''
    all_range_cursors = d_ast_parse.get_all_range_cursors_under(choicable_range_cursor)
    all_range_cursors = _filter_range_cursors(
      all_range_cursors, dgann, src_main_code, ruleset)
    logger.debug(f'Number of range cursors under choicable_range_cursor: {len(all_range_cursors)}')

    '''
    Attempt to control the infinite loop that may arise from
    unchanging queue size.
    '''
    unchanged_count = 0
    prev_queue_size = len(queue_matcher_groups)
    _MAX_QUEUE_UNCHANGED_COUNT = len(queue_matcher_groups) * 2

    while queue_matcher_groups:
      logger.debug(f'~ Queue size: {len(queue_matcher_groups)}')
      matcher_group = queue_matcher_groups.pop(0)
      try:
        await process_choicable_range_cursor(
          matcher_group,
          all_range_cursors,
          ruleset,
          src_main_code,
          pre_context,
          src_test_code,
          translation_rules_test_code,
          dgann,
          processed_match_objs
        )
      except UnhandledRangeCursorExistsError as err:
        logger.debug(f'Moving the matcher group to the end of the queue')
        queue_matcher_groups.append(matcher_group)

      # prevent infinite loop
      if len(queue_matcher_groups) == prev_queue_size:
        unchanged_count += 1
      else:
        unchanged_count = 0
      prev_queue_size = len(queue_matcher_groups)
      if unchanged_count >= _MAX_QUEUE_UNCHANGED_COUNT:
        logger.error(f'Infinite loop detected. Stopping processing for matcher group: {matcher_group}')
        raise QueueInfiniteLoopError('Infinite loop detected')

  logger.info('readonly-main: Finished generation of read-only choices list')
  readonly_choices_list = ruleset.get_choices_list_from_verified_rules(src_main_code)
  return readonly_choices_list


# GENERATING NEW CHOICES LIST BASED ON ERRORS
def are_choices_lists_equal(
  gen_choices_list: List[tuple],
  actual_choices_list: List[tuple]
) -> bool:
  '''
  Choices lists may be of different lengths. For example,
  [
    ((11, 3, 5), 0),
    ((19, 4, 5), 1)
  ]
  and
  [
    ((11, 3, 5), 0),
    ((19, 4, 5), 1),
    ((23, 2, 3), 0),
    ((24, 3, 4), 0)
  ]
  In this case, we remove choices with choice_idx == 0
  from both lists and compare the remaining choices.

  PRE: choice identifiers are unique and sorted.
  '''
  list_a = _choices_list_remove_default_choice_idxs(gen_choices_list)
  list_b = _choices_list_remove_default_choice_idxs(actual_choices_list)

  # base case
  if len(list_a) != len(list_b):
    return False

  for choice_a, choice_b in zip(list_a, list_b):
    range_info_a, choice_idx_a = choice_a
    range_info_b, choice_idx_b = choice_b
    if range_info_a != range_info_b:
      return False
    if choice_idx_a != choice_idx_b:
      return False
  return True


def choices_stack_list_to_choices_list(
  choices_list_stack: List[List[Tuple[Tuple[int], int]]]
) -> List[Tuple[Tuple[int], int]]:
  '''
  Convert a stack of choices lists to a single choices list.
  The stack is a list of lists, where each inner list is a choices list.
  The function returns a single choices list that contains all the choices
  from the stack, preserving the order of choices.
  '''
  choices_list = []
  for choices in choices_list_stack:
    for choice in choices:
      assert choice not in choices_list, f'duplicate choice found: {choice}'
      choices_list.append(choice)
  return choices_list


def _choices_list_remove_default_choice_idxs(
  choices_list: List[Tuple[Tuple[int], int]]
) -> List[Tuple[Tuple[int], int]]:
  '''
  Remove choices with choice_idx == 0 from the choices_list.
  '''
  return [choice for choice in choices_list if choice[1] != 0]


def _choices_list_get(
  choices_list: List[Tuple[Tuple[int], int]],
  range_info: Tuple[int, int, int]
) -> Optional[int]:
  '''
  Get the choice index for the given range_info from the choices_list.
  This is a generic function that can be used when choices_list
  is a nested list of lists, or range_info is a list.
  '''
  for range_info_seq, choice_idx in choices_list:
    assert len(range_info_seq) == 3, 'Expected range_info_seq to be a tuple of (node_id, start_idx, end_idx)'
    if range_info_seq[0] == range_info[0] and \
       range_info_seq[1] == range_info[1] and \
       range_info_seq[2] == range_info[2]:
      return choice_idx
  return None


def _get_new_choices_list_rec(
  rasis_values: List[dict],
  readonly_choices_list: List[Tuple[Tuple[int], int]]
) -> Tuple[Optional[list], bool]:
  '''
  PARAM rasis_values: a list of dictionaries, each dictionary contains:
    - 'next_choices_count': number of rules that can be applied
    - 'current_choose_idx': index of the chosen rule
    - 'current_range_info': range_info of the current alt object

  RETURN a tuple of (new_choices_list, is_new_choice_created)
  '''

  '''
  The idea is to choose the next combination at the lower level.
  If there are no more choices at the lower level, choose the next
  combination one level up.
  '''
  rasis_value = rasis_values[0]
  next_choices_count = rasis_value['next_choices_count']
  current_choose_idx = rasis_value['current_choose_idx']
  current_range_info = rasis_value['current_range_info']

  # base case
  if len(rasis_values) == 1:
    readonly_val = _choices_list_get(readonly_choices_list, current_range_info)
    # the current range_info is in readonly_choices_list, we cannot change it
    if readonly_val is not None:
      node_choice = (current_range_info, readonly_val)
      return [node_choice], False
    # there are no choices left at this node
    if current_choose_idx + 1 == next_choices_count:
      return [], False
    # make the next choice at the current node
    node_choice = (current_range_info, current_choose_idx + 1)
    return [node_choice], True

  # recursive call
  choices_down_the_line, is_new_choice_created = _get_new_choices_list_rec(rasis_values[1:], readonly_choices_list)

  # if a new choice was created at the lower level,
  # we need to return it as a new choice at the current level
  if is_new_choice_created:
    assert len(choices_down_the_line) > 0, 'Expected choices_down_the_line to be non-empty'
    # repeat the same choice at the current level
    node_choice = (current_range_info, current_choose_idx)
    return [node_choice] + choices_down_the_line, True

  # the current range_info is in readonly_choices_list, we cannot change it
  readonly_val = _choices_list_get(readonly_choices_list, current_range_info)
  if readonly_val is not None:
    node_choice = (current_range_info, readonly_val)
    return [node_choice] + choices_down_the_line, False

  # there are no choices left at this node
  if current_choose_idx + 1 == next_choices_count:
    return choices_down_the_line, False

  # make the next choice at the current node
  node_choice = (current_range_info, current_choose_idx + 1)
  return [node_choice] + choices_down_the_line, True


def get_next_unique_choices(
  rel_alt_step_infos: Dict[int, dict],
  choices_list_stack: list,
  readonly_choices_list: List[Tuple[Tuple[int], int]]
) -> dict:
  '''
  Updated and fixed version. Exhaustively checks all possible choices.
  '''

  '''
  `rel_alt_step_infos` contains information about all the possible
  translation rules that can be applied to obtain a different translation.
  '''
  rasis_values = list(rel_alt_step_infos.values())

  '''
  `choices_list` contains current choices of rules at certain AST nodes.
  The fact that we are inside this function tells that these choices
  were invalid and must be replaced.
  '''
  choices_list = [
    (info['current_range_info'], info['current_choose_idx'])
    for info in rasis_values
  ]

  '''
  This is done only once (to bootstrap the stack).
  '''
  if len(choices_list_stack) == 0:
    choices_list_stack.append(choices_list)

  '''
  This makes sure that we pop the invalid choices_list from the stack.
  '''
  if are_choices_lists_equal(choices_list_stack[-1], choices_list):
    choices_list_stack.pop()

  new_choices_list, is_new_choices_created = _get_new_choices_list_rec(rasis_values, readonly_choices_list)
  if not is_new_choices_created:
    raise RuleCombinationsExhaustedError('Exhaustively checked all possible choices')

  assert len(new_choices_list) > 0, 'Expected new_choices_list to be non-empty'
  choices_list_stack.append(new_choices_list)

  all_choices_list = choices_stack_list_to_choices_list(choices_list_stack)
  return {'type': 'ASTNODE', 'choices_list': all_choices_list}


def get_char_line_col_idxs(main_code_lines: List[str]) -> Tuple[List[int], List[int]]:
  '''
  Given the code split into lines, return the line and column indices of each character.
  The column index is -1 for the newline character.
  '''
  line_idxs = []
  col_idxs = []
  for i, line in enumerate(main_code_lines):
    for j, _ in enumerate(line):
      line_idxs.append(i)
      col_idxs.append(j)
    # the newline char
    line_idxs.append(i)
    col_idxs.append(-1)
  return line_idxs, col_idxs


def get_err_line_idx_in_tar_main_code(
  line_content: str,
  err_line_tpi: int,
  tar_program_instr: str,
  tar_main_code: str
) -> int:
  '''
  Get the index of the line in `tar_main_code` that corresponds to the error line.
  PARAM tar_program_instr: instrumented target program (test, main, test call)
  PARAM tar_main_code: main code of the target program (main)
  PARAM err_line_tpi: line number in `tar_program_instr` where the error occurred (1 indexed)
  PARAM line_content: content of the line where the error occurred in `tar_program_instr`
  '''
  tpi_chunks = tar_program_instr.split(tar_main_code)
  assert len(tpi_chunks) == 2, 'sanity check: tar_main_code should appear exactly once in wrapper'

  pre_main_code = tpi_chunks[0]
  pre_main_code_line_count = len(pre_main_code.split('\n'))

  err_line_idx = err_line_tpi - pre_main_code_line_count
  main_code_lines = tar_main_code.split('\n')
  assert err_line_idx < len(main_code_lines), 'sanity check: err_line_idx should be within main_code_lines'

  expected_line = main_code_lines[err_line_idx]
  assert line_content in expected_line, \
    (f'Expected line does not contain error line content.\n'
     f'Expected: "{expected_line}"\n'
     f'Actual: "{line_content}"\n')

  return err_line_idx


def get_proposed_choices_based_on_line_idxs(
  tar_main_code: str,
  err_line_idxs: List[int],
  choices_list_stack: list,
  map_to_exid: Dict[int, List[dict]],
  translate_dbg_history: List[dict],
  readonly_choices_list: List[Tuple[Tuple[int], int]],
):
  '''
  PARAM tar_main_code: main code (f_gold) of the target program.
  PARAM err_line_idxs: a list of 0-based indices of the lines in
  `tar_main_code` where the error occurred.
  PARAM readonly_choices_list: a list of choices that should not be modified.
  '''

  '''
  The following function returns the line indices of every character
  in tar_main_code.
  '''
  main_code_lines = tar_main_code.split('\n')
  line_idxs, col_idxs = get_char_line_col_idxs(main_code_lines)

  '''
  The following loop creates `line_idx_to_exids` - a mapping of
  line indices to expansion ids that are present at the line.
  '''
  line_idx_to_exids : Dict[int, Set[int]] = {}
  for exid, tokens_by_ex in map_to_exid.items():
    for token_by_ex in tokens_by_ex:
      # token in tar_main_code and its range
      token = token_by_ex['str']
      token_range = token_by_ex['range']
      _si, _ei = token_range  # start and end indices of the token in tar_main_code
      assert tar_main_code[_si:_ei] == token, f'sanity check: discrepancy in token range'
      line_si : int = line_idxs[_si]
      line_ei : int = line_idxs[_ei]
      assert line_si == line_ei, 'sanity check: token spans multiple lines'
      assert token in main_code_lines[line_si], f'sanity check: token not found in tar_main_code'
      line_idx_to_exids.setdefault(line_si, set()).add(exid)

  '''
  Create two objects:
  1. mod_dbg_history - a modified version of `translate_dbg_history` that contains
     only the necessary information for the rule chooser.
  2. exid_to_mod_dbg_history_elem - a mapping of expansion ids to the corresponding
     elements in `mod_dbg_history`.
  This is used to quickly access the debug history element for a given expansion id.
  '''
  mod_dbg_history : Dict[int, dict] = {}
  exid_to_mod_dbg_history_elem : Dict[int, dict] = {}
  for elem in translate_dbg_history:
    alt_step = elem['alt_step']
    exid = elem['dbg_info']['ex_id']
    # the assertion below ensures that the dbg_history elements
    # come in the order of alt_step starting from 1.
    assert alt_step - 1 == len(mod_dbg_history), 'sanity check: dbg history elems should come in order'
    mod_dbg_history_elem = {
      'alt_step': alt_step,
      'next_choices_count': elem['next_choices_status']['count'],
      'next_choices_all_known': elem['next_choices_status']['done'],
      'ex_id': exid,
      'current_choose_idx': elem['dbg_info']['notes']['choose_idx'],
      'current_rule_id': elem['dbg_info']['notes']['rule_id'],
      'current_range_info': elem['range_info']
    }
    mod_dbg_history[alt_step] = mod_dbg_history_elem
    exid_to_mod_dbg_history_elem[exid] = mod_dbg_history_elem

  '''
  INVARIANT: `alt_step` starts from 1
  Iterate over expansions on the error line, and for each expansion:
  1. Get the `mod_dbg_history_elem` for the expansion (alt object).
  2. For the given alt object, get the previous `_RELATED_WINDOW_SIZE` elements
  3. From the selected alt objects, keep only those that have more than
     one rule that can be applied at that alt object.
  '''
  _RELATED_WINDOW_SIZE = 0
  exids_err_line : List[int] = list(sorted(set(
    [exid for err_line_idx in err_line_idxs for exid in line_idx_to_exids[err_line_idx]]
  )))
  rel_alt_step_infos : Dict[int, dict] = {}

  for exid_err_line in exids_err_line:
    mod_dbg_history_elem = exid_to_mod_dbg_history_elem[exid_err_line]
    alt_step : int = mod_dbg_history_elem['alt_step']

    # previous _RELATED_WINDOW_SIZE elements + alt_step itself
    rel_alt_steps = list(range(alt_step - _RELATED_WINDOW_SIZE, alt_step + 1))
    for rel_alt_step in rel_alt_steps:
      # because we use `rel_alt_step - 1` below
      if rel_alt_step - 1 < 1:
        continue
      # keep only if number of rules at that step is greater than 1
      if mod_dbg_history[rel_alt_step - 1]['next_choices_count'] <= 1:
        continue
      rel_alt_step_infos[rel_alt_step] = {
        'next_choices_count': mod_dbg_history[rel_alt_step - 1]['next_choices_count'],
        'current_choose_idx': mod_dbg_history[rel_alt_step]['current_choose_idx'],
        # 'ex_id': mod_dbg_history[rel_alt_step]['ex_id'],  # not used
        # 'current_rule_id': mod_dbg_history[rel_alt_step]['current_rule_id'],  # not used
        'current_range_info': mod_dbg_history[rel_alt_step]['current_range_info']
      }

  if len(rel_alt_step_infos) == 0:
    raise RuleCombinationsExhaustedError('No alternative rules found for the error line')

  new_choices = get_next_unique_choices(rel_alt_step_infos, choices_list_stack, readonly_choices_list)
  return new_choices


def get_proposed_choices_compile_error(
  tar_program_instr: str,
  tar_main_code: str,
  tar_error_dict: dict,
  choices_list_stack: list,
  map_to_exid: Dict[int, List[dict]],
  translate_dbg_history: List[dict],
  readonly_choices_list: List[Tuple[Tuple[int], int]] = [],
) -> dict:
  '''
  NOTE PARAM map_to_exid:
  <map_to_exid> -> Dict[<exid>, List[<token_info>]]
  <map_to_exid>: (id of expansion: list of all tokens that were created by this expansion)
  <token_info> -> {
    'ex_id': (id of expansion this token belongs to),
    'str': (token in tar_main_code),
    'range': (range of token in tar_main_code)
  }
  In informal words, map_to_exid contains expansion ids and all tokens that
  were created by this expansion + ranges of every token.
  map_to_exid is created by `d_ast_pretty.ast_to_code()` function.
  The function `d_ast_pretty.ast_to_code()` is called in `p_pirel.duoglot_translate_wrapper()`.

  NOTE PARAM translate_dbg_history:
  <translate_dbg_history> -> List[<history_elem>]
  <history_elem> -> {
    'alt_step' -> (translation step id),
    'range_info' -> (source AST to which the rule was mapped),
    'next_choices_status' -> <next_choices_status>,
    'dbg_info' -> <dbg_info>
  }
  <next_choices_status> -> {
    'count' -> (number of rules that matched a source AST),
    'done' -> (next_choices_all_known?)
  }
  <dbg_info> -> {
    'ex_id' -> (expansion.ex_id, id of expansion that was created from source AST),
    'corres_slot_id' -> (expansion.corres_slot_id, id of slot in source AST),
    'src_matching_node_ids' -> (expansion.matching_node_ids),
    'slot_src_matching_node_ids' -> ([_get_node_ids_from_range_cursor(x) for x in expansion.src_slot_cursors]),
    'notes' -> <notes>,
    'slot_names' -> (expansion.slot_names),
    'slot_ids' -> ([(x.slot_id if x is not None else None) for x in expansion.slots]),
    'outcome' -> (AC, RE, or ER),
    'elem_list_info_id' -> (self._optional_dbg_info_func((self._tail_stack, len(self._tail_stack)), _tail_stack_length_to_elem_list)),
    'loop_count' -> (DelimitedParser._loop_idx)
  }
  <notes> -> {
    'choose_idx': (index of rule from a list of matched rules),
    'rule_id': (id of the rule in the ruleset)
  }
  <notes>: (expansion.notes)
  This object is created in `d_grammar_expand.TransSession._get_alt_debug_history()`
  and is passed to `p_pirel.duoglot_translate_wrapper()`.
  <dbg_info> is a dictionary that is created by
  `d_grammar_dlmparser.DelimitedParser.add_expansion_parse_until_stuck()`,
  which in turn is called by `d_grammar_expand.TransSession._ensure_parser_result()`.
  '''

  p_utils.log_json_time(f'args-get_proposed_choices_compile_error.json', locals())
  logger.debug('Starting p_ext_rule_chooser.get_proposed_choices_compile_error')

  # Unpack `tar_error_dict`. "tpi" stands for "tar_program_instr"
  error_msg = tar_error_dict['error_msg']  # e.g. 'SyntaxError: invalid syntax'
  error_type = tar_error_dict['error_type']  # e.g. 'SyntaxError'
  line_content = tar_error_dict['line_content']  # code snippet at the line of error in `tar_program_instr`
  file_path = tar_error_dict['file_path']  # absolute path to the file where the error occurred
  err_line_tpi = tar_error_dict['line_num']  # line number in the file where the error occurred (0 indexed)

  '''
  Current implementation of `get_proposed_choices_compile_error()` can propose choices
  only on the basis of errors in "tar_program_run.js". And the following
  are the errors that are supported.
  '''
  _SUPPORTED_ERROR_TYPES_JS = ['SyntaxError:', 'ReferenceError:', 'TypeError:']
  assert error_type in _SUPPORTED_ERROR_TYPES_JS, f'unsupported error type {error_type}'

  '''
  The following function returns the error line number in tar_main_code.
  We need to do this because the `err_line_tpi` points to the line number
  in "tar_program_run.js", which is the wrapper code that runs the main code.
  err_line_idx is 0-based.
  '''
  err_line_idx = get_err_line_idx_in_tar_main_code(line_content, err_line_tpi, tar_program_instr, tar_main_code)

  logger.debug(
    f'there was an error running `tar_program_instr`\n'
    f'{error_type} "{error_msg}" on line {err_line_idx + 1} of "{line_content}"')

  new_choices = get_proposed_choices_based_on_line_idxs(
    tar_main_code,
    [err_line_idx],
    choices_list_stack,
    map_to_exid,
    translate_dbg_history,
    readonly_choices_list,
  )
  return new_choices


def get_proposed_choices_semantic_error(
  tar_program_instr: str,
  tar_main_code: str,
  error_lines: dict,
  choices_list_stack: list,
  map_to_exid: Dict[int, List[dict]],
  translate_dbg_history: List[dict],
  readonly_choices_list: List[Tuple[Tuple[int], int]] = [],
) -> dict:
  '''
  Propose new choices based on a semantic error. A semantic error occurs
  when traces of src and tar test scripts do not match.

  PARAM error_lines: a dictionary where keys are line numbers (0-based) and values
  are the content of the lines that caused the semantic error. Sample:
  {
    12: "    while (x && m) {"
  }
  '''

  p_utils.log_json_time(f'args-get_proposed_choices_semantic_error.json', locals())
  logger.debug('Starting p_ext_rule_chooser.get_proposed_choices_compile_error')
  logger.debug(
    f'There are {len(error_lines)} error lines in the semantic error\n'
    f'{json.dumps(error_lines, indent=2)}')

  assert len(error_lines) > 0, 'there must be at least one semantic error line'
  error_line_num = min(error_lines.keys())
  assert (set(range(error_line_num, max(error_lines.keys())+1))
          == set(error_lines)), 'error lines must be continuous'
  error_line_content = error_lines[error_line_num]

  '''
  error_line_num is 0-based line index of a trace mismatch in
  tar_program_instr, we need to get the 0-based line index in tar_main_code.
  '''
  err_line_idx = get_err_line_idx_in_tar_main_code(
    error_line_content, error_line_num + 1, tar_program_instr, tar_main_code)

  '''
  Depending on the locations of log statements (myexactlog), we may end up
  in a situation where there are multiple lines in `error_lines`. For example:
  {
    21: "        break;",
    22: "    }",
    23: "    var x = (x && !m) || (!x && m);"
  }
  taken from:
  ```js
          // ...
          myexactlog(4, m);
          break;
      }
      var x = (x && !m) || (!x && m);
      myexactlog(5, x);  // trace mismatch occurs here
      // ...
  ```
  In this case, we pass all error lines to get_proposed_choices_based_on_line_idxs.
  '''
  err_line_idxs = list(range(err_line_idx, err_line_idx + len(error_lines)))

  new_choices = get_proposed_choices_based_on_line_idxs(
    tar_main_code,
    err_line_idxs,
    choices_list_stack,
    map_to_exid,
    translate_dbg_history,
    readonly_choices_list,
  )
  return new_choices


# TEST HARNESSES
def _test_get_proposed_choices_compile_error():
  '''
  def get_proposed_choices_compile_error(
    tar_program_instr: str,
    tar_main_code: str,
    tar_error_dict: dict,
    choices_list_stack: list,
    map_to_exid: Dict[int, List[dict]],
    translate_dbg_history: List[dict],
    readonly_choices_list: List[Tuple[Tuple[int], int]],
  ) -> dict:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_get_proposed_choices_compile_error_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  tar_program_instr = args_dict['tar_program_instr']
  tar_main_code = args_dict['tar_main_code']
  tar_error_dict = args_dict['tar_error_dict']
  choices_list_stack = args_dict['choices_list_stack']
  map_to_exid = args_dict['map_to_exid']
  map_to_exid = {int(k): v for k, v in map_to_exid.items()}  # ensure keys are int
  translate_dbg_history = args_dict['translate_dbg_history']
  readonly_choices_list = args_dict['readonly_choices_list']

  new_choices = get_proposed_choices_compile_error(
    tar_program_instr,
    tar_main_code,
    tar_error_dict,
    choices_list_stack,
    map_to_exid,
    translate_dbg_history,
    readonly_choices_list
  )
  print(f'New choices: {json.dumps(new_choices, indent=2)}')
  p_utils.write_tmp_json('new_choices.json', new_choices)


def _test_get_readonly_choices_list():
  '''
  async def get_readonly_choices_list(
    src_main_code: str,
    src_test_code: str,
    translation_rules_test_code: str,
    ruleset: p_ruleset.Ruleset
  ) -> list:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_get_readonly_choices_list_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  src_main_code = args_dict['src_main_code']
  src_test_code = args_dict['src_test_code']
  translation_rules_test_code = args_dict['translation_rules_test_code']
  ruleset = p_ruleset.Ruleset.from_dict(json.loads(args_dict['ruleset']))

  readonly_choices_list = asyncio.run(get_readonly_choices_list(
    src_main_code,
    src_test_code,
    translation_rules_test_code,
    ruleset
  ))


if __name__ == '__main__':
  # _test_get_proposed_choices_compile_error()
  _test_get_readonly_choices_list()
