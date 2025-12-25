import json
import re
from typing import Dict, List, Optional, Tuple, Set

import d_ast_parse
import p_consts
import p_pirel
import p_ruleset
import p_rule_applicator as prapp
import p_subject
import p_utils
import p_visitor as pvis
import p_visitor_py as pvpy


logger = p_utils.setup_logger(__name__)


class NoRuleToHandleRangeCursorError(Exception): pass
class UnhandledRangeCursorExistsError(Exception): pass
class RuleCombinationsExhaustedError(RuntimeError): pass
class ExprLogStatHasParseError(RuntimeError): pass
class ExprLogStatContextError(RuntimeError): pass
class QueueInfiniteLoopError(RuntimeError): pass

class AllRulesInMatcherGroupImplausibleError(RuntimeError):
  def __init__(self, not_matching_rules_str: str, snippet: str):
    '''
    PARAM snippet: string repr of the node for which
    there are no plausible rules in the matcher group.
    PARAM not_matching_rules_str: ruleset without
    the rules that match the snippet.
    '''
    self.not_matching_rules_str = not_matching_rules_str
    self.snippet = snippet
  def __str__(self):
    return (f'All rules in the matcher group are implausible for the snippet {self.snippet!r}')

class VerifiedRulesExhaustedError(RuntimeError):
  def __init__(self, choice_identifier: Tuple[int, int, int]):
    '''
    PARAM choice_identifier: range info of the node for which
    all existing verified rules have been exhausted.
    FIELD no_choices_snippet: string repr of the node.
    FIELD not_matching_rules_str: ruleset without
    the rules that match the snippet.
    '''
    self.choice_identifier = choice_identifier
    self.no_choices_snippet = None
    self.not_matching_rules_str = None
  def __str__(self):
    return (f'None of the verified rules work for {self.no_choices_snippet!r} at {self.choice_identifier}')


# GENERATING READONLY CHOICES LIST
def _match_rule_to_range_cursor(
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
    pvpy.WhileStatementNode,
    pvpy.AssertStatementNode,
    pvpy.DeleteStatementNode,
  )
  is_context_node = lambda node: \
    isinstance(node, _CONTEXT_NODE_TYPES)

  cursor = node.parent
  while cursor is not None:
    if is_context_node(cursor):
      return cursor
    cursor = cursor.parent
  raise ValueError('No context node found')


def _reset_expr_subject(
  expr_subject: p_subject.PirelSubject,
  test_scr_matched_rc_chid: Tuple[int, int, int],
  rule_idx: int
) -> None:
  '''
  Modifies expr_subject in-place to reset its choices and verified choice options.
  '''
  expr_subject.choices['choices_list'] = []

  '''
  Update the verified choice options with the new choice option.
  '''
  vrf_ch_opts_dict = {
    chid: rule_idxs for chid, rule_idxs in expr_subject.verified_choice_options
  }
  vrf_ch_opts_dict[test_scr_matched_rc_chid] = [rule_idx]
  vrf_ch_opts = list(vrf_ch_opts_dict.items())
  vrf_ch_opts.sort(key=lambda x: x[0])  # sort by choice identifier

  expr_subject.verified_choice_options = vrf_ch_opts


def _find_logged_expr_in_test_script_str(
  test_script_str: str,
  test_script_ast: list,
  test_script_ann: dict,
  expr_str: str,
) -> tuple:
  '''
  Find all range cursors in the test_script_str that match the expr_str.
  PARAM test_script_str: instrumented script that is passed to the rule applicator
  '''
  re_expr = re.compile(rf'myexactlog\((\d+), ({re.escape(expr_str)})\)')
  matches = re.finditer(re_expr, test_script_str)
  matches = list(matches)

  '''
  There should be exactly one match for the logged expression.
  '''
  assert len(matches) == 1, 'Expected exactly one match for logged expression in test script'
  expr_st_idx = matches[0].start(2)
  expr_end_idx = matches[0].end(2)

  # get the AST node id that correspond to the expr_str
  for nid, (sidx, eidx, _, _) in test_script_ann.items():
    if sidx == expr_st_idx and eidx == expr_end_idx:
      range_cursor = d_ast_parse.get_range_cursor(test_script_ast, nid)
      return range_cursor

  raise ValueError('Should not happen: no range cursor found for logged expression')


def _create_subject_for_expr(
  src_test_script: str,
  is_three_split: bool,
  translation_rules_test_code: str,
  ruleset: p_ruleset.Ruleset,
  subject_name: str,
) -> p_subject.PirelSubject:
  '''
  Create a subject for validating a rule for expression.
  '''

  # all attributes of PirelSubject instance set explicitly
  benchmark_name = 'n/a'
  name = subject_name
  src_program = src_test_script
  src_lang = 'py'
  tar_lang = 'js'
  translation_rules_main_code = \
    ruleset.to_str_ruleset() + '\n\n' + \
    p_utils.read_text(p_consts.LOG_STAT_RULE_FPATH) + '\n\n' + \
    p_utils.read_text(p_consts.RULE_VAL_EXTRA_RULES_FPATH)
  # translation_rules_test_code  # already set
  auto_backward = True
  choices = {'type': 'ASTNODE', 'choices_list': []}
  verified_choice_options = []

  # create a subject instance
  expr_subject = p_subject.PirelSubject(
    benchmark_name, name, src_program, src_lang, tar_lang, is_three_split)
  expr_subject.translation_rules_main_code = translation_rules_main_code
  expr_subject.translation_rules_test_code = translation_rules_test_code
  expr_subject.auto_backward = auto_backward
  expr_subject.choices = choices
  expr_subject.verified_choice_options = verified_choice_options

  # override verified_choice_options with verified rules
  expr_subject.verified_choice_options = ruleset.get_choice_options_from_verified_rules(
    expr_subject.get_src_main_code())

  return expr_subject


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
  matched_ast_encoded = d_ast_parse.range_cursor_encode(matched_range_cursor, dgann, src_main_code)
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
      ruleset.update_unverifiable_rules(matched_ast_encoded, trule)
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
      ruleset.update_unverifiable_rules(matched_ast_encoded, trule)
    raise ExprLogStatContextError()

  return log_stat_str


def _create_test_script_str_for_expr(
  is_three_split: bool,
  matched_range_cursor: tuple,
  matcher_group: List[p_ruleset.TRuleBase],
  src_test_code: Optional[str],
  src_main_code: str,
  pre_context: str,
  dgann: dict,
  ruleset: p_ruleset.Ruleset,
) -> str:
  '''
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
  log_stat_str = _create_log_stat_str_for_expr(
    matched_range_cursor,
    dgann,
    src_main_code,
    matcher_group,
    ruleset
  )

  expr_src_main_code = p_pirel._create_src_main_code_for_val(
    src_main_code,
    pre_context,
    log_stat_str,
    is_three_split
  )

  if is_three_split:
    test_script_str = p_consts.TEST_SCRIPT_TEMPLATE.format(
      test_code=src_test_code,
      main_code=expr_src_main_code,
      test_call_code='test()')
    return test_script_str

  return expr_src_main_code


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

  '''
  All rules from matcher_group must be present in starting_ruleset
  to be considered base rules.
  '''
  flag_all_rules_in_starting_ruleset = True
  for trule in matcher_group:
    if trule not in starting_ruleset.rules:
      flag_all_rules_in_starting_ruleset = False
      break

  if not flag_all_rules_in_starting_ruleset:
    logger.debug('Not all rules in the matcher group are present in the starting ruleset.')
    return False

  '''
  TODO instead of marking all rules as verified, consider checking them one by one.
  '''
  for trule in matcher_group:
    range_cursor_encoded = d_ast_parse.range_cursor_encode(
      matched_range_cursor, dgann, src_main_code)
    ruleset.update_verified_rules(range_cursor_encoded, trule)

  return True


async def _process_match_obj(
  match_obj: dict,
  matcher_group: List[p_ruleset.TRuleBase],
  ruleset: p_ruleset.Ruleset,
  src_main_code: str,
  pre_context: str,
  src_test_code: Optional[str],
  translation_rules_test_code: str,
  dgast: list,
  dgann: dict,
  subject_name: str,
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
  PARAM src_main_code: pre_context + simple_ntext
  '''

  logger.debug('~~~ Starting match object processing')

  assert match_obj['is_matched'], 'Expected match_obj to be matched'
  matched_range_cursor = match_obj['range_cursor']

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
    logger.debug('~~~~~ Validation is complete. Matcher group is a list of one base rule.')
    return

  '''
  Prepare test script and subject for expression.
  '''
  is_three_split = src_test_code is not None

  test_script_str = _create_test_script_str_for_expr(
    is_three_split,
    matched_range_cursor,
    matcher_group,
    src_test_code,
    src_main_code,
    pre_context,
    dgann,
    ruleset,
  )

  expr_subject = _create_subject_for_expr(
    test_script_str,
    is_three_split,
    translation_rules_test_code,
    ruleset,
    subject_name
  )

  '''
  Need to find matched_range_cursor in test_script_str
  '''
  test_scr_ast, test_scr_ann = d_ast_parse.parse_text_dbg(test_script_str, 'py')

  expr_str = d_ast_parse.range_cursor_pretty_print(matched_range_cursor, dgann, src_main_code)
  test_scr_matched_rc = _find_logged_expr_in_test_script_str(
    test_script_str,
    test_scr_ast,
    test_scr_ann,
    expr_str
  )

  test_scr_matched_rc_chid = d_ast_parse.range_cursor_to_choice_identifier(test_scr_matched_rc)
  test_scr_matched_rc_enc = d_ast_parse.range_cursor_encode(test_scr_matched_rc, test_scr_ann, test_script_str)
  test_scr_matched_rc_pp = d_ast_parse.range_cursor_pretty_print(test_scr_matched_rc, test_scr_ann, test_script_str)

  flag_vrf_rule_found = False
  for rule_idx, rule_ut in enumerate(matcher_group):
    logger.debug(f'~~~~~ Rule {rule_idx + 1}/{len(matcher_group)} in matcher group:\n{rule_ut}')
    _reset_expr_subject(expr_subject, test_scr_matched_rc_chid, rule_idx)

    '''
    If this translation succeeds, it means that the rule is plausible
    with respect to the matched AST.
    '''
    try:
      tar_program_plausible, translate_dbg_history = \
        await prapp.apply_translation_rules(expr_subject, raise_on_missing_vrf_rule=True)
      ruleset.update_verified_rules(test_scr_matched_rc_enc, rule_ut)
      flag_vrf_rule_found = True
      logger.debug(
        f'~~~~~ Rule {rule_idx + 1}/{len(matcher_group)} is plausible with respect to the matched AST:\n{rule_ut}\n'
        f'Matched AST: "{test_scr_matched_rc_pp}"')

    except VerifiedRulesExhaustedError as err:
      logger.warning(
        f'While verifying translation rules for a matched AST, stumbled upon '
        f'an AST node that cannot be plausibly translated with any of the '
        f'verified rules.')

      # the node itself is missing a rule
      if err.choice_identifier == test_scr_matched_rc_chid:
        continue

      no_choices_rc = d_ast_parse.choice_identifier_to_range_cursor(
        err.choice_identifier, test_scr_ast)
      no_choices_rc_encoded = d_ast_parse.range_cursor_encode(
        no_choices_rc, dgann, src_main_code)
      assert ruleset.verified_rules_exist(no_choices_rc_encoded), 'precondition failed'
      ruleset.remove_verified_rules_for(no_choices_rc_encoded)
      no_choices_snippet = d_ast_parse.range_cursor_pretty_print(
        no_choices_rc, dgann, src_main_code)

      not_matching_rules : List[p_ruleset.TRuleBase] = []
      for matcher_group in ruleset.matcher_groups.values():
        matcher = matcher_group[0].rule_parsed['match']
        match_obj = _match_rule_to_range_cursor(matcher, no_choices_rc)
        if match_obj['is_matched']:
          continue
        not_matching_rules.extend(matcher_group)
      not_matching_rules_str = '\n\n'.join([r.to_rule_str() for r in not_matching_rules])

      err.no_choices_snippet = no_choices_snippet
      err.not_matching_rules_str = not_matching_rules_str
      raise err

    except Exception as err:
      logger.warning(
        f'~~~~~ Error while applying translation rules:\n{p_utils.exception_to_str(err)}\n'
        f'Rule {rule_idx + 1}/{len(matcher_group)} is not plausible with respect to the matched AST:\n{rule_ut}\n'
        f'Matched AST: "{test_scr_matched_rc_pp}"')
      continue

  if not flag_vrf_rule_found:
    not_matching_rules : List[p_ruleset.TRuleBase] = []
    for matcher_group in ruleset.matcher_groups.values():
      matcher = matcher_group[0].rule_parsed['match']
      match_obj = _match_rule_to_range_cursor(matcher, test_scr_matched_rc)
      if match_obj['is_matched']:
        continue
      not_matching_rules.extend(matcher_group)
    not_matching_rules_str = '\n\n'.join([r.to_rule_str() for r in not_matching_rules])
    err_obj = AllRulesInMatcherGroupImplausibleError(
      not_matching_rules_str, test_scr_matched_rc_pp)
    raise err_obj


async def _process_choicable_range_cursor(
  matcher_group: List[p_ruleset.TRuleBase],
  all_range_cursors: List[Tuple[list, int, int]],
  ruleset: p_ruleset.Ruleset,
  src_main_code: str,
  pre_context: str,
  src_test_code: Optional[str],
  translation_rules_test_code: str,
  dgast: list,
  dgann: dict,
  processed_match_objs: Dict[str, list],
  subject_name: str,
):
  '''
  PARAM matcher_group: a list of rules that have the same matcher signature.

  NOTE a range cursor is a different representation of an AST node.
  Duoglot-style AST allows us to identify ASTs using their node ids
  and range cursors. We can get an AST from a range cursor, but
  we cannot get a range cursor from an AST node, because range cursors
  need a reference to the parent AST node.
  '''
  assert_matchers_match(matcher_group)
  matcher = matcher_group[0].rule_parsed['match']
  matcher_signature = matcher_group[0].get_matcher_signature()

  '''
  Keep only those range cursors that have not been processed yet.
  '''
  all_range_cursors = [
    rc for rc in all_range_cursors
    if d_ast_parse.range_cursor_to_choice_identifier(rc) not in processed_match_objs.get(matcher_signature, [])
  ]
  match_objs = [_match_rule_to_range_cursor(matcher, range_cursor) for range_cursor in all_range_cursors]
  match_objs = [match_obj for match_obj in match_objs if match_obj['is_matched']]

  if len(match_objs) == 0:
    return

  logger.debug(f'~~ Matcher: {matcher}')
  logger.debug(f'~~ Number of range cursors that match the matcher: {len(match_objs)}')
  flag_unhandled_exists = False

  '''
  Process each matched AST that matched the rule (matcher).
  '''
  for idx, match_obj in enumerate(match_objs, start=1):

    range_cursor = match_obj['range_cursor']
    logger.debug(
      f'~~ Processing match_obj {idx}/{len(match_objs)}:\n'
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
        dgast,
        dgann,
        subject_name,
      )
      logger.debug('~~ Successfully processed the match_obj.')
      processed_match_objs.setdefault(matcher_signature, []).append(
        d_ast_parse.range_cursor_to_choice_identifier(range_cursor))

    except NoRuleToHandleRangeCursorError:
      logger.debug('~~ Not enough rules to handle the slot cursor. Continuing with the next match_obj.')
      flag_unhandled_exists = True
      continue

    except ExprLogStatHasParseError:
      logger.debug(
        '~~ Logged expression has parse error. Unlinking the range cursor '
        'from matcher group (rules that match this range cursor):\n'
        f'{d_ast_parse.range_cursor_pretty_print(range_cursor, dgann, src_main_code)}')
      processed_match_objs.setdefault(matcher_signature, []).append(
        d_ast_parse.range_cursor_to_choice_identifier(range_cursor))

    except ExprLogStatContextError:
      logger.debug(
        '~~ Logged expression cannot be used as an argument to a log statement '
        '(context issue).\nUnlinking the range cursor '
        'from matcher group (rules that match this range cursor):\n'
        f'{d_ast_parse.range_cursor_pretty_print(range_cursor, dgann, src_main_code)}')
      processed_match_objs.setdefault(matcher_signature, []).append(
        d_ast_parse.range_cursor_to_choice_identifier(range_cursor))

  if flag_unhandled_exists:
    raise UnhandledRangeCursorExistsError


def _is_excluded_range_cursor(
  root_range_cursor: tuple,
  range_cursor: tuple,
  dgann: dict,
  src_main_code: str
) -> bool:
  '''
  Check if the given range cursor is excluded from consideration.
  PRE: range_cursor[1] + 1 == range_cursor[2]  # range_cursor specifies exactly one AST node
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

  def __pattern_2_descendant_of_string(root_ast: list, ast: list, ann: dict) -> bool:
    '''
    Any nodes under string: string_content, interpolation, etc. since
    we learn overfitted rules for f-strings (and alike).
    PARAM ast: duoglot-style AST
    '''
    root_ast_ntype = root_ast[0]
    if root_ast_ntype != 'py.string':
      return False
    root_ast_nid = root_ast[1]
    rsidx, reidx, _, _ = ann[root_ast_nid]
    ast_nid = ast[1]
    asidx, aeidx, _, _ = ann[ast_nid]
    assert rsidx <= asidx, 'start idx of root_ast <= start idx of ast'
    assert reidx >= aeidx, 'end idx of root_ast >= end idx of ast'
    if asidx == rsidx and aeidx == reidx:
      return False
    return True

  ast = d_ast_parse.range_cursor_to_ast_node(range_cursor)
  if __pattern_1_recursive_call_to_f_gold(ast):
    logger.debug(
      f'Excluding range cursor (recursive call to `f_gold`): '
      f'"{d_ast_parse.range_cursor_pretty_print(range_cursor, dgann, src_main_code)}"')
    return True

  root_ast = d_ast_parse.range_cursor_to_ast_node(root_range_cursor)
  if __pattern_2_descendant_of_string(root_ast, ast, dgann):
    logger.debug(
      f'Excluding range cursor (descendant of string): '
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
  root_range_cursor = range_cursors[0]
  for range_cursor in range_cursors:
    if not _is_excluded_range_cursor(root_range_cursor, range_cursor, dgann, src_main_code):
      result.append(range_cursor)
      continue
    range_cursor_unparsed = d_ast_parse.range_cursor_pretty_print(range_cursor, dgann, src_main_code)
    range_cursor_encoded = d_ast_parse.range_cursor_encode(range_cursor, dgann, src_main_code)

    # if we reach here, it means the range cursor is excluded
    # matcher_group is a list of rules that share the same matcher
    for matcher_sig, matcher_group in ruleset.matcher_groups.items():
      assert_matchers_match(matcher_group)
      matcher = matcher_group[0].rule_parsed['match']
      match_obj = _match_rule_to_range_cursor(matcher, range_cursor)
      if not match_obj['is_matched']:
        continue
      # if we reach here, it means that matcher_group contains rules
      # that match the range_cursor
      logger.debug(
        f'Updating unverifiable rules for range cursor: '
        f'{range_cursor_unparsed}')
      for rule in matcher_group:
        ruleset.update_unverifiable_rules(
          range_cursor_encoded,
          rule
        )

  return result


async def _get_validated_stat_nid_in_instr_code(
  src_main_code: str,
  simple_ntext: str,
  all_stat_nids: List[int],
) -> int:
  '''
  PARAM src_main_code: instrumented source code prepared for rule applicator.
  RETURN the node id of the statement rules of which are
  to be validated.
  '''

  _GFG_STAT_NTYPES = [
    pvpy.ImportFromStatementNode,
    pvpy.ImportStatementNode,
    pvpy.BreakStatementNode,
    pvpy.ContinueStatementNode,
    pvpy.ReturnStatementNode,
    pvpy.ExpressionStatementNode,
    pvpy.IfStatementNode,
    pvpy.WhileStatementNode,
    pvpy.ForStatementNode,
    pvpy.TryStatementNode,
    pvpy.PassStatementNode,  # never used in f_gold, but added by instrumentation
  ]

  _SKEL_STAT_NTYPES = _GFG_STAT_NTYPES +[
    pvpy.WithStatementNode,
    pvpy.DeleteStatementNode,
    pvpy.AssertStatementNode,
    pvpy.NonlocalStatementNode,
    pvpy.RaiseStatementNode,
  ]

  tree = pvpy.Tree.from_str(src_main_code)
  root_node = tree.root_node
  nid_node_map = root_node.get_nid_node_map()

  simple_ntree = pvpy.Tree.from_str(simple_ntext)
  assert len(simple_ntree.root_node.get_nt_children()) == 1, 'Expected exactly one statement node'
  simple_node = simple_ntree.root_node.get_nt_children()[0]

  '''
  Need to ignore all statements that were added as
  part of instrumentation: break statements, log statements,
  pass statements.
  TODO with break statements, it's a bit tricky; for now, just return
  the latest break statement node id even if it's inserted by instrumentation,
  because it has "no" effect on p_ext_rule_chooser.stat_node_validate_exprs().
  '''
  pp = pvpy.PrettyPrinter(indent_with='    ')
  for stat_nid in reversed(all_stat_nids):
    stat_node = nid_node_map[stat_nid]
    assert isinstance(stat_node, tuple(_SKEL_STAT_NTYPES)), \
      f'unexpected type: {stat_node.__class__.__name__}'

    # skip if statement types do not match
    if type(stat_node) != type(simple_node):
      continue

    # skip myexactlog(...) statements
    if isinstance(stat_node, pvpy.ExpressionStatementNode):
      assert len(stat_node.get_nt_children()) == 1, 'sanity check'
      child = stat_node.get_nt_children()[0]
      if isinstance(child, pvpy.CallNode):
        unparsed_child : str = pp.visit(child)
        if unparsed_child.lstrip().startswith('myexactlog('):
          continue

    return stat_nid

  raise ValueError('No statement node found that matches the simple_ntext statement node.')


async def _get_stat_nids_in_pre_context(
  src_main_code: str,
  simple_ntext: str,
  is_three_split: bool,
) -> List[int]:
  '''
  RETURN a list of statement node ids that appear in pre_context.
  '''
  if is_three_split:
    all_stat_nids = await p_pirel._get_statement_nodes(
      src_main_code, 'py', is_three_split, return_node_ids=True)
    assert all_stat_nids == sorted(all_stat_nids)
  else:
    all_stat_nids = await p_pirel.get_statement_nodes_eot(
      src_main_code, 'py', return_node_ids=True)

  val_stat_nid = await _get_validated_stat_nid_in_instr_code(
    src_main_code, simple_ntext, all_stat_nids)

  stat_nids_pre_context = [nid for nid in all_stat_nids if nid < val_stat_nid]
  return stat_nids_pre_context


async def _get_exluded_stat_nids(
  src_main_code: str,
  simple_ntext: str,
  ruleset: p_ruleset.Ruleset,
  is_three_split: bool,
) -> List[int]:
  '''
  RETURN a list of statement node ids that should be excluded
  from consideration when generating choices for translation.
  These are statement nodes that appear in pre_context
  and statement nodes that match overfitted rules.
  '''
  excluded_stat_nids = set()

  '''
  Nodes in pre context are excluded since they are already processed.
  '''
  stat_nids_pre_context = await _get_stat_nids_in_pre_context(
    src_main_code, simple_ntext, is_three_split)
  excluded_stat_nids.update(stat_nids_pre_context)

  '''
  Nodes that match overfitted rules are excluded.
  '''
  rc_src_main_code, dgann = d_ast_parse.parse_text_to_range_cursor(src_main_code, 'py')
  if is_three_split:
    assert rc_src_main_code[1] + 1 == rc_src_main_code[2], \
      'range cursor must specify just one node (function f_gold)'
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
      match_obj = _match_rule_to_range_cursor(matcher, range_cursor)
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
  excluded_stat_nids.update(overfitted_stat_nids)

  excluded_stat_nids = sorted(excluded_stat_nids)
  return excluded_stat_nids


async def _stat_node_validate_exprs_init(
  src_main_code: str,
  ruleset: p_ruleset.Ruleset,
  is_three_split: bool,
  simple_ntext: str,
) -> tuple:
  '''
  Given a duoglot-style AST, collect all nodes under AST,
  for which we should "cleverly" generate choices that
  result in a plausible translation.
  RETURN a list of tuples (range cursor, pre-context).
  '''
  excluded_stat_nids = await _get_exluded_stat_nids(
    src_main_code, simple_ntext, ruleset, is_three_split)

  choicable_nodes = pvpy.ChoicableNodeExtractor.extract_choicable_nodes(
    src_main_code, exclude_statement_nodes_ids=excluded_stat_nids)
  logger.debug(f'There are {len(choicable_nodes)} choicable nodes in src_main_code.')
  p_utils.log_file_time('src_main_code.py', src_main_code)

  chable_rc_prectxs = []  # choicable range cursors with pre-context
  dgast, dgann = d_ast_parse.parse_text_dbg(src_main_code, 'py')

  for i, choicable_node in enumerate(choicable_nodes, start=1):
    choicable_range_cursor = d_ast_parse.get_range_cursor(dgast, choicable_node.get_node_id())  # $$$$
    stat_node = _choicable_node_get_context_node(choicable_node)
    # For subject without the three-split format,
    # statements yet to be translated (by the order of execution)
    # are already purged from src_main_code,
    # hence the node blacklist is empty here.
    pre_context = p_pirel.get_pre_context(
      src_main_code, 'py', is_three_split, stat_node.get_node_id(), [])
    pre_context = pvpy.LogStatementRemover.remove_log_statements(pre_context)
    chable_rc_prectxs.append((choicable_range_cursor, pre_context))
    logger.debug(
      f'-> Choicable_node {i}/{len(choicable_nodes)}: '
      f'"{d_ast_parse.range_cursor_pretty_print(choicable_range_cursor, dgann, src_main_code)}"')

  return chable_rc_prectxs, dgast, dgann


async def stat_node_validate_exprs(
  src_main_code: str,
  src_test_code: Optional[str],
  translation_rules_test_code: str,
  ruleset: p_ruleset.Ruleset,
  simple_ntext: str,
  subject_name: str
) -> None:
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
  PARAM subject_name: to know what subject we are dealing with.

  NOTE This function should not add or remove rules from the ruleset.
  '''

  p_utils.log_json_time('args-stat_node_validate_exprs.json', locals())
  logger.debug('readonly-main: Starting generation of read-only choices list')

  '''
  `choicable_range_cursors` - a list of range cursors
  for which we need to create readonly choices list
  that results in a plausible translation.
  retval_0 = ((15 + (7 * (math.sqrt(5)))) / 4) * (math.pow(side, 3))
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  if h < 0 or m < 0 or h > 12 or m > 60:
     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  '''
  chable_rc_prectxs, dgast, dgann = await _stat_node_validate_exprs_init(
    src_main_code, ruleset, src_test_code is not None, simple_ntext)

  for i, (choicable_range_cursor, pre_context) in enumerate(chable_rc_prectxs, start=1):

    logger.debug(
      f'readonly-main: processing choicable_range_cursor {i}/{len(chable_rc_prectxs)}: '
      f'"{d_ast_parse.range_cursor_pretty_print(choicable_range_cursor, dgann, src_main_code)}"')

    '''
    Verified or unverifiable rules may already contain rules that can handle
    the choicable_range_cursor. If so, we skip processing it.
    '''
    choicable_range_cursor_encoded = d_ast_parse.range_cursor_encode(
      choicable_range_cursor, dgann, src_main_code)
    if ruleset.verified_rules_exist(choicable_range_cursor_encoded):
      logger.debug('Skipping processing of choicable_range_cursor, since it is already handled by verified rules.')
      continue
    if ruleset.unverifiable_rules_exist(choicable_range_cursor_encoded):
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
    This includes the choicable_range_cursor itself (as the first elem) and all its subtrees.
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
        await _process_choicable_range_cursor(
          matcher_group,
          all_range_cursors,
          ruleset,
          src_main_code,
          pre_context,
          src_test_code,
          translation_rules_test_code,
          dgast,
          dgann,
          processed_match_objs,
          subject_name
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

  logger.debug('readonly-main: Finished generation of read-only choices list')
  verified_choice_options = ruleset.get_choice_options_from_verified_rules(src_main_code)
  return verified_choice_options


# GENERATING NEW CHOICES LIST BASED ON ERRORS
def _sanity_check_choices_list(
  choices_list: List[Tuple[Tuple[int, int, int], int]]
) -> None:
  '''
  Perform sanity checks on the choices list.
  POST: choice identifiers are unique and sorted.
  '''
  seen = set()
  prev_range_info = None
  for range_info, choice_idx in choices_list:
    assert range_info not in seen, f'duplicate choice identifier found in choices_list: {range_info}'
    seen.add(range_info)
    if prev_range_info is not None:
      assert range_info > prev_range_info, f'choices list is not sorted: {choices_list}'
    prev_range_info = range_info


def _sanity_check_choice_options(
  choice_options: List[Tuple[Tuple[int, int, int], List[int]]],
  assert_uniq_choice_ids: bool = True,
  assert_sorted: bool = True,
) -> None:
  '''
  Perform sanity checks on the choice options.
  POST: choice identifiers are unique and sorted.
  '''
  seen = set()
  prev_range_info = None
  for range_info, choice_idxs in choice_options:
    if assert_uniq_choice_ids:
      assert range_info not in seen, f'duplicate choice identifier found in choice_options: {range_info}'
    seen.add(range_info)
    if assert_sorted and prev_range_info is not None:
      assert range_info > prev_range_info, f'choice options list is not sorted: {choice_options}'
    prev_range_info = range_info


def merge_choices_list_and_choice_options(
  choices_list: List[Tuple[Tuple[int, int, int], int]],
  choice_options: List[Tuple[Tuple[int, int, int], List[int]]],
  raise_on_conflict: bool = False
) -> List[Tuple[Tuple[int, int, int], int]]:
  '''
  Create a union of two choices lists.
  If a choice exists in both lists and raise_on_conflict is True,
  raise an error if the choice indices are different.
  RETURN the merged choices list.
  PRE: choice identifiers are unique and sorted.
  '''
  result = []
  idx_li = 0
  idx_op = 0
  len_li = len(choices_list)
  len_op = len(choice_options)

  while idx_li < len_li and idx_op < len_op:
    range_info_li, choice_idx_li = choices_list[idx_li]
    range_info_op, choice_idxs_op = choice_options[idx_op]
    assert len(choice_idxs_op) > 0, 'sanity check: choice options must have at least one choice idx'

    if range_info_li < range_info_op:
      result.append((range_info_li, choice_idx_li))
      idx_li += 1
    elif range_info_li > range_info_op:
      result.append((range_info_op, choice_idxs_op[0]))  # take the first choice idx
      idx_op += 1
    else:
      # range_info_a == range_info_b
      if raise_on_conflict and choice_idx_li != choice_idxs_op[0]:
        raise ValueError(
          f'Conflict in choices lists for range_info {range_info_li}: '
          f'choice_idx_li={choice_idx_li}, choice_idx_op={choice_idxs_op[0]}')
      assert choice_idx_li in choice_idxs_op, 'choice_idx_li must be in choice_idxs_op'
      result.append((range_info_li, choice_idx_li))
      idx_li += 1
      idx_op += 1

  # append remaining choices from choices_list_a
  while idx_li < len_li:
    result.append(choices_list[idx_li])
    idx_li += 1

  # append remaining choices from choices_list_b
  while idx_op < len_op:
    range_info_op, choice_idxs_op = choice_options[idx_op]
    assert len(choice_idxs_op) > 0, 'sanity check: choice options must have at least one choice idx'
    result.append((range_info_op, choice_idxs_op[0]))  # take the first choice idx
    idx_op += 1

  return result


def choices_list_sorted(
  choices_list: List[Tuple[Tuple[int, int, int], int]],
  reverse: bool = False
) -> List[Tuple[Tuple[int, int, int], int]]:
  '''
  Sort the choices list by range_info.
  '''
  return sorted(choices_list, key=lambda x: x[0], reverse=reverse)


def rel_alt_step_info_remove_duplicates(
  rel_alt_step_infos: dict
) -> dict:
  '''
  For some unknown reason, DuoGlot translator includes duplicate
  entries in translate_dbg_history structure. Duplicate entries
  have the same range_info. Having duplicates causes
  duplicate choices in the generated choices list.
  '''
  seen = set()
  result = dict()
  for alt_step, entries in rel_alt_step_infos.items():
    current_range_info = entries['current_range_info']
    if current_range_info in seen:
      logger.debug(f'removing duplicate entry for alt_step for range: {current_range_info}')
      continue
    seen.add(current_range_info)
    result[alt_step] = entries
  return result


def _add_verified_choice_options(
  all_choices_list: List[Tuple[Tuple[int, int, int], int]],
  verified_choice_options: List[Tuple[Tuple[int, int, int], List[int]]]
) -> List[Tuple[Tuple[int, int, int], int]]:
  '''
  Add readonly choices to the all_choices_list.
  '''
  _sanity_check_choices_list(all_choices_list)
  _sanity_check_choice_options(verified_choice_options)
  return merge_choices_list_and_choice_options(
    all_choices_list,
    verified_choice_options,
    raise_on_conflict=False  # choice may have been made from verified choices
  )


def _choices_list_history_to_choices_list(
  choices_list_history: List[List[Tuple[Tuple[int, int, int], int]]]
) -> List[Tuple[Tuple[int, int, int], int]]:
  '''
  Convert a history of choices lists to a single choices list.
  The history is a list of lists, where each inner list is a choices list.
  The function returns a single choices list that contains all the choices
  from the history, preserving the order of choices.
  '''
  merged = {}
  for choices_list in choices_list_history:
    for choice in choices_list:
      range_info, choice_idx = choice
      merged[range_info] = choice_idx  # later ones overwrite earlier ones
  merged_choices_list = [(range_info, choice_idx) for range_info, choice_idx in merged.items()]
  return merged_choices_list


def _get_new_choices_list_rec(
  choice_options: List[Tuple[Tuple[int], List[int]]],
  vrf_range_infos: Set[Tuple[int, int, int]],
  raise_on_missing_vrf_rule: bool = False,
) -> Tuple[Optional[list], bool]:
  '''
  PARAM choice_options: a list of tuples, each tuple contains:
    - current_range_info: choice_identifier of the current node
    - choice_idxs: list of possible choice indices at the current node

  RETURN a tuple of (new_choices_list, is_new_choice_created)
  '''

  '''
  The idea is to choose the next combination at the lower level.
  If there are no more choices at the lower level, choose the next
  combination one level up.
  '''
  current_range_info, choice_idxs = choice_options[0]

  # base case
  if len(choice_options) == 1:
    # no choices left at this node
    if len(choice_idxs) == 1:
      if raise_on_missing_vrf_rule and current_range_info in vrf_range_infos:
        raise VerifiedRulesExhaustedError(current_range_info)
      return [], False
    node_choice = (current_range_info, choice_idxs[1])
    return [node_choice], True

  # recursive call
  choices_down_the_line, is_new_choice_created = _get_new_choices_list_rec(
    choice_options[1:],
    vrf_range_infos,
    raise_on_missing_vrf_rule,
  )

  # if a new choice was created at the lower level,
  # we need to return it as a new choice at the current level
  if is_new_choice_created:
    assert len(choices_down_the_line) > 0, 'Expected choices_down_the_line to be non-empty'
    # repeat the same choice at the current level
    node_choice = (current_range_info, choice_idxs[0])
    return [node_choice] + choices_down_the_line, True

  # no choices left at this node
  if len(choice_idxs) == 1:
    if raise_on_missing_vrf_rule and current_range_info in vrf_range_infos:
      raise VerifiedRulesExhaustedError(current_range_info)
    return choices_down_the_line, False

  # make the next choice at the current node
  node_choice = (current_range_info, choice_idxs[1])
  return [node_choice] + choices_down_the_line, True


def get_next_unique_choices(
  rel_alt_step_infos: Dict[int, dict],
  choices_list_history: list,
  verified_choice_options: List[Tuple[Tuple[int, int, int], List[int]]],
  raise_on_missing_vrf_rule: bool = False,
) -> dict:
  '''
  PARAM rel_alt_step_infos: (rasis) contains information about all the possible
  translation rules that can be applied to obtain a different translation
  at the location of an error.
  NOTE Exhaustively checks all possible choices.
  '''

  '''
  `err_line_choices_list` contains current rule choices at lines with error.
  The fact that we are inside this function tells that these choices
  were invalid and must be replaced.
  '''
  err_line_choices_list = [
    (info['current_range_info'], info['current_choose_idx'])
    for info in list(rel_alt_step_infos.values())
  ]
  err_line_choices_list = choices_list_sorted(err_line_choices_list)

  '''
  Create new choices list at the error lines.
  Sorting order of choice_options defines the order of
  node combinations, i.e., trying different rules at parent nodes vs child nodes.
  Sorting choice_options in descending order means that
  we try different rules at child nodes first.
  '''
  choice_options = []
  for rasis_value in rel_alt_step_infos.values():
    next_choices_count = rasis_value['next_choices_count']
    current_choose_idx = rasis_value['current_choose_idx']
    current_range_info = rasis_value['current_range_info']
    choice_options.append(
      (current_range_info, list(range(current_choose_idx, next_choices_count)))
    )
  choice_options.sort(key=lambda elem: elem[0], reverse=True)

  '''
  Overwrite choice_options to only include the verified choices from
  verified_choice_options
  '''
  _sanity_check_choice_options(choice_options, assert_sorted=False)
  _sanity_check_choice_options(verified_choice_options)
  for vrf_choice_option in verified_choice_options:
    vrf_range_info, vrf_choice_idxs = vrf_choice_option
    for i in range(len(choice_options)):
      cur_range_info, cur_choice_idxs = choice_options[i]
      if cur_range_info == vrf_range_info:
        # update choice options to only include the verified choice
        # however, do not add vrf_choice_idxs that were previously in err_line_choices_list
        intn_choice_idxs = list(set(vrf_choice_idxs) & set(cur_choice_idxs))
        choice_options[i] = (cur_range_info, intn_choice_idxs)
        break

  vrf_range_infos = set(vrf_choice_option[0] for vrf_choice_option in verified_choice_options)
  new_choices_list, is_new_choices_created = _get_new_choices_list_rec(
    choice_options,
    vrf_range_infos,
    raise_on_missing_vrf_rule,
  )
  new_choices_list = choices_list_sorted(new_choices_list)

  if not is_new_choices_created:
    raise RuleCombinationsExhaustedError('Exhaustively checked all possible choices')

  assert len(new_choices_list) > 0, 'Expected new_choices_list to be non-empty'
  choices_list_history.append(new_choices_list)

  all_choices_list = _choices_list_history_to_choices_list(choices_list_history)
  all_choices_list = choices_list_sorted(all_choices_list)
  all_choices_list = _add_verified_choice_options(all_choices_list, verified_choice_options)
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
  choices_list_history: list,
  map_to_exid: Dict[int, List[dict]],
  translate_dbg_history: List[dict],
  verified_choice_options: List[Tuple[Tuple[int, int, int], List[int]]],
  raise_on_missing_vrf_rule: bool = False,
):
  '''
  PARAM tar_main_code: main code (f_gold) of the target program.
  PARAM err_line_idxs: a list of 0-based indices of the lines in
  `tar_main_code` where the error occurred.
  PARAM verified_choice_options: a list of choices that should not be modified.
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
      assert line_si <= line_ei, 'sanity check: start line should be <= end line'
      if line_si == line_ei:
        assert token in main_code_lines[line_si], \
          f'sanity check: single-line token not found in tar_main_code'
      else:
        assert token in '\n'.join(main_code_lines[line_si:line_ei + 1]), \
          f'sanity check: multi-line token not found in tar_main_code'
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

  rel_alt_step_infos = rel_alt_step_info_remove_duplicates(rel_alt_step_infos)
  new_choices = get_next_unique_choices(
    rel_alt_step_infos,
    choices_list_history,
    verified_choice_options,
    raise_on_missing_vrf_rule,
  )
  return new_choices


def get_proposed_choices_compile_error(
  tar_program_instr: str,
  tar_main_code: str,
  tar_error_dict: dict,
  choices_list_history: list,
  map_to_exid: Dict[int, List[dict]],
  translate_dbg_history: List[dict],
  verified_choice_options: List[Tuple[Tuple[int, int, int], List[int]]] = [],
  raise_on_missing_vrf_rule: bool = False,
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
  assert error_type in p_consts.SUPPORTED_ERROR_TYPES_JS, f'unsupported error type {error_type}'

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
    choices_list_history,
    map_to_exid,
    translate_dbg_history,
    verified_choice_options,
    raise_on_missing_vrf_rule,
  )
  return new_choices


def get_proposed_choices_semantic_error(
  tar_program_instr: str,
  tar_main_code: str,
  error_lines: dict,
  choices_list_history: list,
  map_to_exid: Dict[int, List[dict]],
  translate_dbg_history: List[dict],
  verified_choice_options: List[Tuple[Tuple[int, int, int], List[int]]] = [],
  raise_on_missing_vrf_rule: bool = False,
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

  '''
  line_num is 0-based line index of a trace mismatch in
  tar_program_instr, we need to get the 0-based line index in tar_main_code.
  '''
  err_line_idxs = [
    get_err_line_idx_in_tar_main_code(
      line_content, line_num + 1, tar_program_instr, tar_main_code)
    for line_num, line_content in error_lines.items()
  ]

  new_choices = get_proposed_choices_based_on_line_idxs(
    tar_main_code,
    err_line_idxs,
    choices_list_history,
    map_to_exid,
    translate_dbg_history,
    verified_choice_options,
    raise_on_missing_vrf_rule,
  )
  return new_choices
