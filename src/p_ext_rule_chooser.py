import asyncio
import json
from typing import Dict, List, Optional, Tuple, Set

import d_ast_parse
import d_grammar_rules
import p_consts
import p_llm_gen
import p_rule_applicator as prapp
import p_subject
import p_tree_log as ptlog
import p_utils
import p_visitor_py as pvpy


logger = p_utils.setup_logger(__name__)


class NoRuleToHandleRangeCursorError(Exception): pass
class UnhandledRangeCursorExistsError(Exception): pass
class RuleCombinationsExhaustedError(RuntimeError): pass
class AllRulesInMatcherGroupImplausibleError(RuntimeError): pass


class TranslationRule:
  def __init__(self, rule: dict, idx: int):
    '''
    PARAM rule: a dictionary representing a translation rule
    as parsed by d_grammar_rules.parse_analyze_rules().
    PARAM idx: index of the rule in the ruleset.
    '''
    assert isinstance(rule, dict), f'Expected rule to be a dict, got {type(rule)}'
    assert 'type' in rule, 'Rule must have a "type" key'
    assert 'match' in rule, 'Rule must have a "match" key'
    assert 'expand' in rule, 'Rule must have a "expand" key'
    self.rule = rule
    self.idx = idx

  def __str__(self):
    return d_grammar_rules.pretty_rule(self.rule)

  def __repr__(self):
    return f'{self.__class__.__name__} {str(self.rule)}'

  def __eq__(self, obj) -> bool:
    if not isinstance(obj, TranslationRule):
      raise ValueError(f'Cannot use == with {type(obj)}')
    return str(self.rule) == str(obj.rule)

  def get_matcher_signature(self) -> str:
    return str(self.rule['match'])


class Ruleset:
  '''
  Parsed version of a ruleset as a string.
  Since the ruleset is immutable, rule idxs are maintained
  by TranslationRule class.
  INV: translation rules come in the order of their idxs.

  `matcher_groups` is a dictionary that groups rules
  by their matcher signatures.
  '''
  def __init__(self):
    self.rules: List[TranslationRule] = []
    self.matcher_groups: Dict[str, List[TranslationRule]] = {}
    self.verified_rules: Dict[tuple, TranslationRule] = {}  # choice identifier -> TranslationRule

  def assert_invariants(self):
    for idx, rule in enumerate(self.rules):
      assert isinstance(rule, TranslationRule), f'Expected rule to be a TranslationRule, got {type(rule)}'
      assert rule.idx == idx, f'Translation rule #{idx} is out of order, must be #{rule.idx}'

  def to_str(self) -> str:
    self.assert_invariants()
    return '\n\n'.join([str(rule) for rule in self.rules])

  def intersect_matcher_groups(self, matcher_groups: Dict[str, List[TranslationRule]]) -> List[TranslationRule]:
    '''
    Return a list of all rules, for matcher signatures that are in matcher_groups,
    use the rules from matcher_groups and for the rest use the rules from self.matcher_groups.
    '''
    trules = []
    for mat_sig, mat_gr_rules in self.matcher_groups.items():
      if mat_sig in matcher_groups:
        trules.extend(matcher_groups[mat_sig])
      else:
        trules.extend(mat_gr_rules)
    return trules

  def get_rule_idx_in_matcher_group(self, rule: 'TranslationRule') -> int:
    '''
    Get the index of a rule in its matcher group.
    '''
    if rule.get_matcher_signature() not in self.matcher_groups:
      raise ValueError(f'No matcher group with signature {rule.get_matcher_signature()}')
    matcher_group = self.matcher_groups[rule.get_matcher_signature()]
    for idx, r in enumerate(matcher_group):
      if r == rule:
        return idx
    raise ValueError(f'Rule is not in the ruleset: {rule}')

  def get_choices_list_from_verified_rules(self) -> List[Tuple[Tuple[int, int, int], int]]:
    choices = []
    for choice_identifier, rule in self.verified_rules.items():
      rule_idx_in_matcher_group = self.get_rule_idx_in_matcher_group(rule)
      choices.append((choice_identifier, rule_idx_in_matcher_group))
    return choices

  @classmethod
  def from_str(cls, rules_str: str) -> 'Ruleset':
    trules, dbg_info = d_grammar_rules.parse_analyze_rules(rules_str)
    ruleset = cls()
    for idx, trule in enumerate(trules):
      rule = TranslationRule(trule, idx)
      signature = rule.get_matcher_signature()
      ruleset.rules.append(rule)
      ruleset.matcher_groups.setdefault(signature, []).append(rule)
    return ruleset


# GENERATING INITIAL CHOICES LIST
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
    # print("matcher_anno:", matcher_anno, file=sys.stderr)
    # print("intree_anno:", intree_anno, file=sys.stderr)
    # return True
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
        if _is_elem_NT(visit_elem):
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
      assert current_range_elem[0] == "anno", '_anno_ meet none-annotation element: elem head: ' + current_range_elem[0]
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

      assert _is_elem_NT(visit_elem)
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


def _is_elem_NT(elem) -> bool:
  '''
  Return True if the element is a non-terminal.
  '''
  if not isinstance(elem, list):
    return False
  if elem[0] == "anno":
    return False
  assert elem[0] != "fragment"
  assert isinstance(elem[1], int)
  return True


def _range_cursor_to_ast_node(range_cursor: tuple) -> list:
  '''
  Convert a range cursor to an AST node.
  range_cursor: Tuple[ List[src_ast] , int , int ]
  '''
  assert isinstance(range_cursor, tuple) and len(range_cursor) == 3
  assert isinstance(range_cursor[0], list)
  assert isinstance(range_cursor[1], int)
  assert isinstance(range_cursor[2], int)
  assert range_cursor[1] + 1 == range_cursor[2], 'range cursors specify exactly one AST node'

  # Convert the range cursor to an AST node
  parent_ast = range_cursor[0]
  child_ast_idx = range_cursor[1]
  child_ast = parent_ast[child_ast_idx]
  return child_ast


def _range_cursor_to_choice_identifier(range_cursor: tuple) -> tuple:
  '''
  Choice identifier is a tuple of (node_id, start_idx, end_idx).
  It is used for identifying the node in the AST for which a rule
  choice is made. It is used in choices_list.
  '''
  node, start_idx, end_idx = range_cursor
  assert _is_elem_NT(node), 'sanity check'
  node_id = node[1]
  assert isinstance(node_id, int), 'sanity check'
  return (node_id, start_idx, end_idx)


def _get_nt_children_as_range_cursors(nt_node: list) -> list:
  '''
  Given a duoglot-style AST node, return a list of non-terminal
  children as range cursors.
  NOTE range cursors specify exactly one AST node.
  '''
  assert _is_elem_NT(nt_node), 'expected non-terminal node'
  result = []
  for i in range(2, len(nt_node)):
    if _is_elem_NT(nt_node[i]):
      result.append((nt_node, i, i + 1))
  return result


def _range_cursor_seq_descending_from_ast(ast: list) -> list:
  '''
  Given a duoglot-style AST, generate a sequence of range cursors
  in pre-order traversal. Sequence does not include the AST itself,
  only the subtrees.
  '''
  assert _is_elem_NT(ast), 'expected non-terminal node'
  result = []
  def _rec_pre_order(node: list):
    nonlocal result
    if not _is_elem_NT(node):
      return
    for child_range_cursor in _get_nt_children_as_range_cursors(node):
      result.append(child_range_cursor)
      child_idx = child_range_cursor[1]
      child_ast = child_range_cursor[0][child_idx]
      _rec_pre_order(child_ast)
  _rec_pre_order(ast)
  return result


def _ast_pretty_print_primitive(ast: list) -> str:
  '''
  Pretty print the AST node by concatenating all terminals without whitespaces.
  PARAM ast: duoglot-style AST node
  '''
  def _rec_pre_order(node) -> str:
    # duoglot-style ASTs contain annotations under string nodes
    # must be handled separately
    if node[0] == 'py.string':
      quote = node[2][2][1]
      quote = quote[1:-1].replace('\\', '')
      return f'{quote}{node[4][2].strip('"')}{quote}'
    if not _is_elem_NT(node):
      assert isinstance(node, str), 'expected string here'
      return node.strip('"')
    result = ''
    for child in node[2:]:
      result += _rec_pre_order(child)
    return result
  result = _rec_pre_order(ast)
  return result.strip()


def _ast_pretty_print(ast: list) -> str:
  '''
  Pretty print the AST.
  PARAM ast: duoglot-style AST node
  '''
  primitive_res = _ast_pretty_print_primitive(ast)
  tree = pvpy.Tree.from_str(primitive_res)
  pp = pvpy.PrettyPrinter(indent_with='    ')
  result = pp.visit(tree.root_node)
  return result.strip()


def rules_contains(rules: List[TranslationRule], rule: TranslationRule) -> bool:
  '''
  Check if the rules list contains the rule.
  '''
  for r in rules:
    if r == rule:
      return True
  return False


def rules_deduplicate(rules: List[TranslationRule]) -> List[TranslationRule]:
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
  rules_a: List[TranslationRule],
  rules_b: List[TranslationRule]
) -> List[TranslationRule]:
  '''
  Return a list of rules that are in both rules_a and rules_b.
  '''
  intersection = []
  for rule_a in rules_a:
    for rule_b in rules_b:
      if rule_a == rule_b:
        intersection.append(rule_a)
  return intersection


def rules_group_by_matcher(rules: List[TranslationRule]) -> Dict[str, List[TranslationRule]]:
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


def assert_matchers_match(matcher_group: List[TranslationRule]) -> None:
  '''
  Assert that all rules in the list have the same matcher signature.
  Assert that rule idx are sorted in ascending order.
  PARAM matcher_group: a list of TranslationRule objects.
  '''
  assert len(matcher_group) > 0, 'Expected at least one rule'
  first_rule_signature = matcher_group[0].get_matcher_signature()
  for rule in matcher_group[1:]:
    assert rule.get_matcher_signature() == first_rule_signature, \
      f'Expected all rules to have the same matcher signature, got {rule.get_matcher_signature()}'

  # Assert that rule idx are sorted in ascending order.
  rule_ids = [rule.idx for rule in matcher_group]
  assert rule_ids == sorted(rule_ids), 'Expected rule idx to be sorted in ascending order'


def slot_cursor_remove_empty(slot_cursors: List[Tuple[list, int, int]]) -> List[Tuple[list, int, int]]:
  '''
  Remove empty slot cursors from the list.
  An empty slot cursor is a cursor that has the same start and end indices.
  '''
  non_empty_slot_cursors = []
  for slot_cursor in slot_cursors:
    # end_idx must be strictly greater than start_idx
    if slot_cursor[1] < slot_cursor[2]:
      non_empty_slot_cursors.append(slot_cursor)
  return non_empty_slot_cursors


async def gen_test_fn_str_llm(
  paramable_ids: List[str],
  f_gold_fn_str: str,
) -> Optional[str]:
  '''
  Generate a test function string using the LLM.
  This test function will be used to validate translation rules.

  p_llm_gen.gen_test_function uses the following attributes of
  - subject
    - name
    - src_lang
    - tar_lang
  - template_dict
    - src_lang
  '''
  if len(paramable_ids) == 0:
    return '''def test():\n    f_gold()'''

  # TODO so that PirelSubject does not complain
  _dummy = p_consts.TEST_SCRIPT_TEMPLATE.format(
    test_fn_str='_dummy',
    f_gold_fn_str='_dummy',
    test_call_str='_dummy'
  )

  pirel_subject_snippet_conf : dict = p_utils.read_yaml(p_consts.SNIPPET_UNDER_TEST_CONF_FPATH)
  pirel_subject_snippet_conf['src_program'] = _dummy
  pirel_subject = p_subject.PirelSubject.from_dict_config(pirel_subject_snippet_conf)

  # TODO so that p_llm_gen.gen_test_function() works
  # since we are intervening in the middle of the pipeline
  template_dict = {
    'src_lang': pirel_subject.src_lang,
  }
  lrules_validation = ptlog.RulesValidation()

  test_fn_str = await p_llm_gen.gen_test_function(f_gold_fn_str, pirel_subject, template_dict, lrules_validation)
  return test_fn_str


def get_f_gold_fn_str(paramable_ids: List[str], log_stat_str: str) -> str:
  '''
  Given a list of parameterable identifiers and a log statement string,
  return a formatted string for the f_gold function.
  '''
  _params = ', '.join(paramable_ids)
  _indented_snippet_block = p_utils.indent(log_stat_str, 4)
  f_gold_fn_str = p_consts.F_GOLD_SNIPPET_TEMPLATE.format(params=_params, indented_snippet_block=_indented_snippet_block)
  return f_gold_fn_str


def get_log_statement(choicable_ast: list) -> str:
  '''
  Return a log statement that logs the AST.
  '''
  ast_str = _ast_pretty_print(choicable_ast)
  return f'myexactlog({ast_str})'


def get_rules_that_handle_range_cursor_rec(
  range_cursor: tuple,
  ruleset: Ruleset,
  rules_mut_list: List[TranslationRule] = []
) -> Optional[List[TranslationRule]]:
  '''
  Recursively retrieve all rules that can handle the range cursor,
  and all slots that belong to the range cursor.
  '''
  choice_identifier = _range_cursor_to_choice_identifier(range_cursor)

  # base case: rule for range cursor not found
  if choice_identifier not in ruleset.verified_rules:
    return None

  rule = ruleset.verified_rules[choice_identifier]
  rules_mut_list.append(rule)

  # get all slot cursors of range cursor
  match_obj = match_rule_to_range_cursor(rule.rule['match'], range_cursor)
  assert match_obj['is_matched'], 'Expected rule to match the range cursor'
  slot_cursors = match_obj['slot_cursors']
  slot_cursors = slot_cursor_remove_empty(slot_cursors)

  # base case: rule has no slot cursors
  if len(slot_cursors) == 0:
    return rules_mut_list

  # recursive case: rule has slot cursors
  for slot_cursor in slot_cursors:
    rules = get_rules_that_handle_range_cursor_rec(slot_cursor, ruleset, rules_mut_list)
    if rules is None:
      return None

  return rules_mut_list


def _check_for_base_rules(
  matcher_group: List[TranslationRule],
  subtrees_rules: List[TranslationRule],
  matched_range_cursor: tuple,
  ruleset: Ruleset,
) -> bool:
  '''
  When validating matching rules, check if the matched rules are base rules.
  RETURN True if the matched rules are base rules.
  '''
  logger.debug(f'~~~ starting _check_for_base_rules')

  STARTING_RULESET_STR = p_utils.read_text(p_consts.STARTING_RULESET_FPATH)
  starting_ruleset = Ruleset.from_str(STARTING_RULESET_STR)

  # base rules do not have slot cursors -> no subtrees_rules
  if len(subtrees_rules) > 0:
    logger.debug('Matched rules are not base rules, since subtrees_rules is not empty.')
    return False

  # base rules usually have only one rule
  # TODO this needs to be improved
  if len(matcher_group) > 1:
    logger.warning('Matched rules are not base rules, since there is more than one matching rule.')
    return False

  assert len(matcher_group) == 1, 'Expected exactly one matching rule for base rules'
  matching_rule = matcher_group[0]
  for rule in starting_ruleset.rules:
    if rule == matching_rule:
      logger.debug(f'Matched rule appears in a starting ruleset: {matching_rule}')
      choice_identifier = _range_cursor_to_choice_identifier(matched_range_cursor)
      ruleset.verified_rules[choice_identifier] = rule
      return True

  raise NotImplementedError('new case for base rules? ' + str(matching_rule))


async def _validate_matcher_group_no_intersection(
  matched_range_cursor: tuple,
  matcher_group: List[TranslationRule],
  subtrees_rules: List[TranslationRule],
  ruleset: Ruleset,
  test_script_str: str,
) -> None:
  '''
  PARAM matched_range_cursor: range cursor that was matched by the matcher_group.
  PARAM matcher_group: a list of TranslationRule objects that matched the range cursor.
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
    subtrees_rules,
    matched_range_cursor,
    ruleset,
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
  rules_wo = ruleset.intersect_matcher_groups(joined_matcher_groups)
  logger.debug(f'len(rules_wo): {len(rules_wo)}')

  '''
  Add rules from matcher_group to rules_wo and validate them one by one.
  '''
  for idx, rule in enumerate(matcher_group, start=1):
    logger.debug(f'validating rule {idx}/{len(matcher_group)}:\n{rule}')

    rules_w = rules_wo + [rule]
    rules_w_str = '\n\n'.join([str(r) for r in rules_w])

    pirel_subject_snippet_conf : dict = p_utils.read_yaml(p_consts.SNIPPET_UNDER_TEST_CONF_FPATH)
    pirel_subject_snippet_conf['src_program'] = test_script_str
    pirel_subject_snippet_conf['translation_rules_main_code'] = rules_w_str
    pirel_subject = p_subject.PirelSubject.from_dict_config(pirel_subject_snippet_conf)

    '''
    If this translation succeeds, it means that the rule is plausible
    with respect to the matched AST.
    '''
    try:
      tar_program_plausible, used_rule_ids_history = await prapp.apply_translation_rules(pirel_subject)

      choice_identifier = _range_cursor_to_choice_identifier(matched_range_cursor)
      ruleset.verified_rules[choice_identifier] = rule
      logger.debug(
        f'Rule {idx} is plausible with respect to the matched AST: {rule}\n'
        f'Matched AST: {_ast_pretty_print(_range_cursor_to_ast_node(matched_range_cursor))}')
      return

    except Exception as err:
      logger.warning(f'Error while applying translation rules: {err}')
      logger.warning(
        f'Rule {idx} is not plausible with respect to the matched AST: {rule}\n'
        f'Matched AST: {_ast_pretty_print(_range_cursor_to_ast_node(matched_range_cursor))}')
      continue

  raise AllRulesInMatcherGroupImplausibleError(
    'No plausible translation found for the matched AST with the given ruleset. This is not desired.')


async def _validate_matcher_group_single_intersection(
  matched_range_cursor: tuple,
  matcher_group: List[TranslationRule],
  subtrees_rules: List[TranslationRule],
  ruleset: Ruleset,
  test_script_str: str,
) -> None:
  '''
  PARAM matched_range_cursor: range cursor that was matched by the matcher_group.
  PARAM matcher_group: a list of TranslationRule objects that matched the range cursor.
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
  assert len(subtrees_matcher_groups[matcher_signature]) == 1, 'expected exactly one rule in the matcher group'

  intersect_rule = subtrees_matcher_groups[matcher_signature][0]
  other_rules = [rule for rule in matcher_group if rule != intersect_rule]
  del subtrees_matcher_groups[matcher_signature]

  '''
  rules_wo contains all rules that can handle everything except
  the matched_range_cursor. This is used to validate the matcher_group.
  '''
  joined_matcher_groups = {**subtrees_matcher_groups, **{matcher_signature: []}}
  rules_wo = ruleset.intersect_matcher_groups(joined_matcher_groups)
  logger.debug(f'len(rules_wo): {len(rules_wo)}')

  '''
  Add rules from matcher_group to rules_wo and validate them one by one.
  '''
  for idx, rule in enumerate([intersect_rule] + other_rules, start=1):
    logger.debug(f'validating rule {idx}/{len(other_rules) + 1}:\n{rule}')

    rules_w = rules_wo + [rule]
    rules_w_str = '\n\n'.join([str(r) for r in rules_w])

    pirel_subject_snippet_conf : dict = p_utils.read_yaml(p_consts.SNIPPET_UNDER_TEST_CONF_FPATH)
    pirel_subject_snippet_conf['src_program'] = test_script_str
    pirel_subject_snippet_conf['translation_rules_main_code'] = rules_w_str
    pirel_subject = p_subject.PirelSubject.from_dict_config(pirel_subject_snippet_conf)

    '''
    If this translation succeeds, it means that the rule is plausible
    with respect to the matched AST.
    '''
    try:
      tar_program_plausible, used_rule_ids_history = await prapp.apply_translation_rules(pirel_subject)

      choice_identifier = _range_cursor_to_choice_identifier(matched_range_cursor)
      ruleset.verified_rules[choice_identifier] = rule
      logger.debug(
        f'Rule {idx} is plausible with respect to the matched AST: {rule}\n'
        f'Matched AST: {_ast_pretty_print(_range_cursor_to_ast_node(matched_range_cursor))}')
      return

    except Exception as err:
      logger.warning(f'Error while applying translation rules: {err}')
      logger.warning(
        f'Rule {idx} is not plausible with respect to the matched AST: {rule}\n'
        f'Matched AST: {_ast_pretty_print(_range_cursor_to_ast_node(matched_range_cursor))}')
      continue

  raise AllRulesInMatcherGroupImplausibleError(
    'No plausible translation found for the matched AST with the given ruleset. This is not desired.')


async def validate_matcher_group(
  matched_range_cursor: tuple,
  matcher_group: List[TranslationRule],
  subtrees_rules: List[TranslationRule],
  ruleset: Ruleset,
  paramable_ids: List[str],
  test_fn_str: str,
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

  '''
  Need to create a f_gold() function for the matched AST.
  '''
  matched_ast = _range_cursor_to_ast_node(matched_range_cursor)
  log_stat_str = get_log_statement(matched_ast)
  f_gold_fn_str = get_f_gold_fn_str(paramable_ids, log_stat_str)

  test_script_str = p_consts.TEST_SCRIPT_TEMPLATE.format(
    test_fn_str=test_fn_str,
    f_gold_fn_str=f_gold_fn_str,
    test_call_str='test()'
  )
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
      test_script_str
    )

  elif len(reusable_rules) == 1:
    await _validate_matcher_group_single_intersection(
      matched_range_cursor,
      matcher_group,
      subtrees_rules,
      ruleset,
      test_script_str
    )

  else:
    raise NotImplementedError('consider this case')


async def _process_match_obj(
  match_obj: dict,
  matcher_group: List[TranslationRule],
  ruleset: Ruleset,
  paramable_ids: List[str],
  test_fn_str: str,
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
  logger.debug('~~~ starting _process_match_obj')
  assert match_obj['is_matched'], 'Expected match_obj to be matched'
  range_cursor = match_obj['range_cursor']

  '''
  slot_cursors are range_cursors that appear under the range_cursor.
  '''
  slot_cursors = match_obj['slot_cursors']
  slot_cursors = slot_cursor_remove_empty(slot_cursors)
  logger.debug(f'Matched AST has {len(slot_cursors)} slots')

  '''
  BASE CASE
  The rule is non-recursive (leaf rule). It might be a rule in the starting ruleset.
  '''
  if len(slot_cursors) == 0:
    logger.debug('Matched rule is non-recursive. Validating matching rules.')
    await validate_matcher_group(
      range_cursor,
      matcher_group,
      [],  # subtrees_rules
      ruleset,
      paramable_ids,
      test_fn_str
    )
    return

  '''
  RECURSIVE CASE
  The rule is recursive, i.e. it has at least one slot cursor under the matched range cursor.
  Need to check if we can handle all slot cursors.
  '''
  subtrees_rules = []
  for slot_cursor in slot_cursors:
    '''
    We need to check if there are rules that plausibly translate the slot_cursors
    under the matched range_cursor.
    '''
    subtrees_plausible_rules = get_rules_that_handle_range_cursor_rec(slot_cursor, ruleset)
    logger.debug(f'Slot cursor AST: {_ast_pretty_print(_range_cursor_to_ast_node(slot_cursor))}')

    '''
    If there is no rule that can handle the range_cursor,
    it means we need to check the next matching rule group.
    '''
    if subtrees_plausible_rules is None:
      logger.warning('No rule to handle the slot cursor')
      raise NoRuleToHandleRangeCursorError

    logger.debug(f'Number of rules that can handle the slot cursor: {len(subtrees_plausible_rules)}')
    subtrees_rules.extend(subtrees_plausible_rules)

  '''
  This range_cursor is handled by the rule. Mark it as handled.
  '''
  await validate_matcher_group(
    range_cursor,
    matcher_group,
    subtrees_rules,
    ruleset,
    paramable_ids,
    test_fn_str,
  )


async def process_choicable_range_cursor(
  matcher_group: List[TranslationRule],
  all_range_cursors: List[Tuple[list, int, int]],
  ruleset: Ruleset,
  paramable_ids: List[str],
  test_fn_str: str,
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
  logger.debug('~~~ starting process_choicable_range_cursor()')

  assert_matchers_match(matcher_group)
  matcher = matcher_group[0].rule['match']
  matcher_signature = matcher_group[0].get_matcher_signature()
  logger.debug(f'Matcher: {matcher}')

  '''
  Keep only those range cursors that have not been processed yet.
  '''
  all_range_cursors = [
    rc for rc in all_range_cursors
    if _range_cursor_to_choice_identifier(rc) not in processed_match_objs.get(matcher_signature, [])
  ]
  match_objs = [match_rule_to_range_cursor(matcher, range_cursor) for range_cursor in all_range_cursors]
  match_objs = [match_obj for match_obj in match_objs if match_obj['is_matched']]

  if len(match_objs) == 0:
    logger.debug('No range cursor matches the matcher. Exiting.')
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
      f'matcher_signature: {matcher_signature}\n'
      f'matched AST: {_ast_pretty_print(_range_cursor_to_ast_node(range_cursor))}')

    # Process the match object
    try:
      await _process_match_obj(
        match_obj,
        matcher_group,
        ruleset,
        paramable_ids,
        test_fn_str
      )
      logger.debug('Successfully processed the match_obj.')
      processed_match_objs.setdefault(matcher_signature, []).append(_range_cursor_to_choice_identifier(range_cursor))
    except NoRuleToHandleRangeCursorError:
      logger.warning('No rule to handle the range cursor. Continuing with the next match_obj.')
      flag_unhandled_exists = True
      continue

  if flag_unhandled_exists:
    raise UnhandledRangeCursorExistsError


async def _process_choicable_range_cursor_init(
  choicable_range_cursor: Tuple[list, int, int],
) -> Tuple[List[str], str, list]:
  '''
  Before we proceed with doing anything, we generate a test
  function using the choicable_range_cursor. This is done
  to ensure that we generate the test function only for
  subtrees under the choicable_range_cursor.
  '''

  choicable_ast = _range_cursor_to_ast_node(choicable_range_cursor)

  log_stat_str = get_log_statement(choicable_ast)
  paramable_ids = pvpy.ParametrizableVariablesCollector.get_paramable_ids(log_stat_str)
  f_gold_fn_str = get_f_gold_fn_str(paramable_ids, log_stat_str)
  test_fn_str = await gen_test_fn_str_llm(paramable_ids, f_gold_fn_str)

  '''
  Need to add itself, because _range_cursor_seq_descending_from_ast()
  will include only the subtrees. all_range_cursors are all possible
  range cursors under the choicable_range_cursor.
  '''
  all_range_cursors = [choicable_range_cursor]
  choicable_range_cursor_children = _range_cursor_seq_descending_from_ast(choicable_ast)
  all_range_cursors.extend(choicable_range_cursor_children)

  return paramable_ids, test_fn_str, all_range_cursors


def get_choicable_range_cursors(ast: list) -> List[Tuple[list, int, int]]:
  '''
  Given a duoglot-style AST, collect all nodes under AST,
  for which we should "cleverly" generate choices that
  result in a plausible translation.
  NOTE can add more inner functions for more cases (e.g. binary expressions).
  '''
  def _get_assignment_rhs_as_range_cursor(node: list) -> Tuple[list, int, int]:
    assert node[0] == 'py.assignment', 'expected assignment node'
    assert node[3].strip('"') == '=', 'expected assignment operator'
    if node[4][0] == 'py.assignment':
      # assignment to assignment, e.g. "a = b = 1"
      return _get_assignment_rhs_as_range_cursor(node[4])
    return (node, 4, 5)

  def _rec_collect_assignment_rhs(node):
    nonlocal assignment_rhs
    # base case: terminal node
    if not _is_elem_NT(node):
      return
    # recursive case: non-terminal node
    for child in node[2:]:
      _rec_collect_assignment_rhs(child)
    # check the current node
    if node[0] != 'py.expression_statement':
      return
    children = node[2:]
    if len(children) != 1:
      return
    child = children[0]
    assert _is_elem_NT(child), 'expected non-terminal node'
    if child[0] != 'py.assignment':
      return
    # at this point we have "expr_statement -> assignment"
    rhs = _get_assignment_rhs_as_range_cursor(child)
    assignment_rhs.append(rhs)

  # TODO handle conditions of if statements, e.g. "if x == 1" -> "x == 1"
  def _rec_collect_boolean_exprs(node):
    nonlocal boolean_exprs
    # base case: terminal node
    if not _is_elem_NT(node):
      return

  assignment_rhs = []
  boolean_exprs = []
  _rec_collect_assignment_rhs(ast)
  return assignment_rhs


async def get_initial_choices_list(
  src_main_code: str,
  rules: str
) -> list:
  '''
  Generate an initial choices list for the given source code and rules.
  Initial choices list contains choices to validated rules that result
  in plausible translation. This is much better than blindly iterating
  over all possible rule combinations to get a plausible translation.
  '''

  ast, ann = d_ast_parse.parse_text_dbg(src_main_code, 'py', keep_text=False)
  ruleset = Ruleset.from_str(rules)

  '''
  `choicable_range_cursors` - a list of range cursors
  for which we need to create initial choices list
  that results in a plausible translation.
  retval_0 = ((15 + (7 * (math.sqrt(5)))) / 4) * (math.pow(side, 3))
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  if h < 0 or m < 0 or h > 12 or m > 60:
     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  '''
  choicable_range_cursors = get_choicable_range_cursors(ast)

  for i, choicable_range_cursor in enumerate(choicable_range_cursors):

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
    paramable_ids, test_fn_str, all_range_cursors = await _process_choicable_range_cursor_init(choicable_range_cursor)

    while queue_matcher_groups:
      logger.debug(f'queue size: {len(queue_matcher_groups)}')
      matcher_group = queue_matcher_groups.pop(0)
      try:
        await process_choicable_range_cursor(
          matcher_group,
          all_range_cursors,
          ruleset,
          paramable_ids,
          test_fn_str,
          processed_match_objs
        )
      except UnhandledRangeCursorExistsError as err:
        logger.debug(f'Moving the matcher group to the end of the queue')
        queue_matcher_groups.append(matcher_group)

  initial_choices_list = ruleset.get_choices_list_from_verified_rules()
  return initial_choices_list


# GENERATING NEW CHOICES LIST BASED ON ERRORS
def are_choices_lists_equal(
  gen_choices_list: List[tuple],
  actual_choices_list: List[tuple]
) -> bool:
  '''
  An actual choices list may be longer, because a new choice may
  create new choice nodes down the line. For example,
  [
    ((11, 3, 5), 0),
    ((19, 4, 5), 1)
  ]
  we choose "1" in (19, 4, 5), and this is the actual choices after applying it:
  [
    ((11, 3, 5), 0),
    ((19, 4, 5), 1),
    ((23, 2, 3), 0),
    ((24, 3, 4), 0)
  ]
  As you see, (23, 2, 3) and (24, 3, 4) are new nodes at which we can make new choices.
  '''

  # The following assertion does not hold for all cases.
  # Refer to "debug-35-gfg20-rate-14" / G0001.
  # assert len(actual_choices_list) >= len(gen_choices_list), \
  #   'sanity check: actual choices list must be longer or equal to generated choices list'

  if len(actual_choices_list) > len(gen_choices_list):
    for choice in actual_choices_list[len(gen_choices_list):]:
      range_info, choice_idx = choice
      assert choice_idx == 0, 'sanity check: actual choices list must contain only 0 choice_idx for new nodes'

  '''
  In case actuall list is longer, the new nodes are not considered.
  '''
  for choice_a, choice_b in zip(gen_choices_list, actual_choices_list):
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
    f'{error_type} "{error_msg}" on line {err_line_idx + 1} of "{line_content}"\n')

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
    f'{json.dumps(error_lines, indent=2)}\n')

  assert len(error_lines) > 0, 'there must be at least one semantic error line'
  error_line_nums = list(error_lines.keys())
  error_line_num = error_line_nums[0]
  error_line_content = error_lines[error_line_num]

  '''
  error_line_num is 0-based line index of a trace mismatch in
  tar_program_instr, we need to get the 0-based line index in tar_main_code.
  '''
  err_line_idx = get_err_line_idx_in_tar_main_code(error_line_content, error_line_num + 1, tar_program_instr, tar_main_code)

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


# USAGE EXAMPLE
async def get_initial_choices_list_usage() -> list:
  '''
  `choicable_range_cursors` - a list of range cursors
  for which we need to create initial choices list
  that results in a plausible translation.
  retval_0 = ((15 + (7 * (math.sqrt(5)))) / 4) * (math.pow(side, 3))
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  '''

  code = p_utils.read_tmp_text('ext_rule_chooser_code.py')
  rules = p_utils.read_tmp_text('ext_rule_chooser_rules.snart')

  ast, ann = d_ast_parse.parse_text_dbg(code, 'py', keep_text=False)
  ruleset = Ruleset.from_str(rules)
  choicable_range_cursors = get_choicable_range_cursors(ast)

  for i, choicable_range_cursor in enumerate(choicable_range_cursors):

    queue_matcher_groups = list(ruleset.matcher_groups.values())
    processed_match_objs : Dict[str, list] = {}
    paramable_ids, test_fn_str, all_range_cursors = await _process_choicable_range_cursor_init(choicable_range_cursor)

    while queue_matcher_groups:
      logger.debug(f'queue size: {len(queue_matcher_groups)}')
      matcher_group = queue_matcher_groups.pop(0)
      try:
        await process_choicable_range_cursor(
          matcher_group,
          all_range_cursors,
          ruleset,
          paramable_ids,
          test_fn_str,
          processed_match_objs
        )
      except UnhandledRangeCursorExistsError as err:
        logger.debug(f'Moving the matcher group to the end of the queue')
        queue_matcher_groups.append(matcher_group)

  initial_choices_list = ruleset.get_choices_list_from_verified_rules()
  p_utils.write_tmp_json('ext_rule_chooser_initial_choices_list.json', initial_choices_list)
  return initial_choices_list


if __name__ == '__main__':
  _test_get_proposed_choices_compile_error()
  # asyncio.run(get_initial_choices_list_usage())
