from __future__ import annotations

import json
from abc import ABC
from typing import Dict, List, Optional, Tuple

import d_ast_parse
import d_grammar_rules
import p_visitor_py as pvpy
import p_utils


logger = p_utils.setup_logger(__name__)


class TRuleBase(ABC):
  '''
  An abstract base class representing a translation rule.
  '''
  def __init__(self, rule: dict):
    '''
    PARAM rule: a dictionary representing a translation rule
    as parsed by d_grammar_rules.parse_analyze_rules().
    '''
    assert isinstance(rule, dict), f'Expected rule to be a dict, got {type(rule)}'
    assert 'type' in rule, 'Rule must have a "type" key'
    assert 'match' in rule, 'Rule must have a "match" key'
    assert 'expand' in rule, 'Rule must have a "expand" key'
    self.rule = rule

  def __str__(self):
    return d_grammar_rules.pretty_rule(self.rule)

  def __repr__(self):
    return f'{self.__class__.__name__} {str(self.rule)}'

  def __eq__(self, obj) -> bool:
    if not isinstance(obj, TRuleBase):
      raise ValueError(f'Cannot use == with {type(obj)}')
    return str(self.rule) == str(obj.rule)

  def get_matcher_signature(self) -> str:
    return str(self.rule['match'])

  def to_dict(self) -> dict:
    res = {
      'type': self.__class__.__name__,
      'rule_str': self.__str__(),
    }
    return res

  @classmethod
  def from_dict(cls, data: dict) -> TRuleBase:
    '''
    Create a rule instance from a dict.
    '''
    parsed_rules, _ = d_grammar_rules.parse_analyze_rules(data['rule_str'])
    assert len(parsed_rules) == 1, f'Expected exactly one rule, got {len(parsed_rules)}'
    rule = parsed_rules[0]
    if data['type'] == 'StartingTRule':
      return StartingTRule(rule)
    elif data['type'] == 'LearnedTRule':
      return LearnedTRule(rule)
    else:
      raise ValueError(f'Unknown rule type: {data["type"]}')

  @classmethod
  def from_rule_str(cls, rule_str: str) -> TRuleBase:
    '''
    Create a rule instance from a rule string.
    '''
    parsed_rules, _ = d_grammar_rules.parse_analyze_rules(rule_str)
    assert len(parsed_rules) == 1, f'Expected exactly one rule, got {len(parsed_rules)}'
    rule = parsed_rules[0]
    return cls(rule)


class StartingTRule(TRuleBase):
  '''
  A class that represents a translation rule that appears
  in the starting ruleset. It is assumed to be valid.
  '''


class LearnedTRule(TRuleBase):
  '''
  A class that represents a translation rule that appears
  in the starting ruleset. It is assumed to be valid.
  '''


class Ruleset:
  '''
  Represents a set of translation rules.

  PROPERTY matcher_groups: is a dictionary that groups rules
  by their matcher signatures.
  INV: rules in self._verified_rules are also in self.rules
  '''
  def __init__(self):
    self.rules : List[TRuleBase] = []
    # Each time the ruleset is modified, call _update_matcher_groups() to update this property.
    self.matcher_groups: Dict[str, List[TRuleBase]] = {}
    # unparsed AST node -> TRuleBase
    self._verified_rules: Dict[str, TRuleBase] = {}

  def __str__(self):
    return json.dumps(self.to_dict(), indent=2)

  def _update_matcher_groups(self):
    self.matcher_groups = {}
    for rule in self.rules:
      sig = rule.get_matcher_signature()
      self.matcher_groups.setdefault(sig, []).append(rule)

  def append_rule(self, rule: TRuleBase):
    '''
    Append a rule to the ruleset and update matcher_groups.
    '''
    assert isinstance(rule, TRuleBase), \
      f'Expected rule to be subclass of TRuleBase, got {type(rule)}'
    self.rules.append(rule)
    self._update_matcher_groups()

  def prepend_rule(self, rule: TRuleBase):
    '''
    Prepend a rule to the ruleset and update matcher_groups.
    '''
    assert isinstance(rule, TRuleBase), \
      f'Expected rule to be subclass of TRuleBase, got {type(rule)}'
    self.rules.insert(0, rule)
    self._update_matcher_groups()

  def get_rule_ref(self, other_rule: TRuleBase) -> Optional[TRuleBase]:
    '''
    Get a reference to a rule in the ruleset that is equal to other_rule.
    '''
    assert isinstance(other_rule, TRuleBase), \
      f'Expected other_rule to be subclass of TRuleBase, got {type(other_rule)}'
    for rule in self.rules:
      if rule == other_rule:
        return rule
    return None

  def update_verified_rules(self, unparsed_ast: str, rule: TRuleBase) -> None:
    assert isinstance(unparsed_ast, str), f'Unexpected type {type(unparsed_ast)}'
    assert isinstance(rule, TRuleBase), f'Unexpected type {type(rule)}'

    '''
    Check if a verified rule for unparsed_ast already exists.
    Current policy, if it exists and is different, log a warning and ignore the new rule.
    TODO policy: update only if different ASTs?
    '''
    if unparsed_ast in self._verified_rules:
      existing_vrf_rule = self._verified_rules[unparsed_ast]
      # the existing verified rule is different from the new one
      if existing_vrf_rule != rule:
        logger.warning(f'Verified rule for "{unparsed_ast}" was about to be updated.')
        logger.warning(f'Old rule: {existing_vrf_rule}')
        logger.warning(f'New rule: {rule}')
        # raise RuntimeError('Verified rule is being changed')
        return

    self._verified_rules[unparsed_ast] = rule

  def get_verified_rule(self, unparsed_ast: str) -> TRuleBase:
    assert isinstance(unparsed_ast, str), f'Unexpected type {type(unparsed_ast)}'
    assert unparsed_ast in self._verified_rules, f'No verified rule for "{unparsed_ast}"'
    return self._verified_rules[unparsed_ast]

  def verified_rule_exists(self, unparsed_ast: str) -> bool:
    assert isinstance(unparsed_ast, str), f'Unexpected type {type(unparsed_ast)}'
    return unparsed_ast in self._verified_rules

  def merge_verified_rules_from(self, serialized_ruleset: dict) -> None:
    assert isinstance(serialized_ruleset, dict), f'Unexpected type {type(serialized_ruleset)}'
    for unparsed_ast, serialized_trule in \
      serialized_ruleset.get('verified_rules', {}).items():
      other_rule = TRuleBase.from_dict(serialized_trule)
      rule = self.get_rule_ref(other_rule)
      if rule:
        self.update_verified_rules(unparsed_ast, rule)

  def get_rule_idx_in_matcher_group(self, rule: TRuleBase) -> int:
    '''
    Get the index of a rule in its matcher group.
    '''
    sig = rule.get_matcher_signature()
    if sig not in self.matcher_groups:
      raise ValueError(f'No matcher group with signature {sig}')
    matcher_group = self.matcher_groups[sig]
    for idx, r in enumerate(matcher_group):
      if r == rule:
        return idx
    raise ValueError(f'Rule is not in the ruleset: {rule}')

  def add_all_rules_from_missing_matcher_groups(
    self, matcher_groups: Dict[str, List[TRuleBase]]
  ) -> List[TRuleBase]:
    '''
    Return a list of all rules, for matcher signatures that are in `matcher_groups`,
    use the rules from `matcher_groups` and for the rest use the rules from `self.matcher_groups`.
    Example:
    self.matcher_groups   matcher_groups   result
    {a, b, c}             {a}              {a}
    {d}                                    {d}
    {e, f}                {e}              {e}
    {g, h, i, j}                           {g, h, i, j}
    '''
    trules = []
    for mat_sig, mat_gr_rules in self.matcher_groups.items():
      if mat_sig in matcher_groups:
        trules.extend(matcher_groups[mat_sig])
      else:
        trules.extend(mat_gr_rules)
    return trules

  def get_choices_list_from_verified_rules(
    self,
    code: str
  ) -> List[Tuple[Tuple[int, int, int], int]]:
    '''
    Given a code string, self.rules, and self._verified_rules
    return a list of choices for all choicable nodes in `code`
    according to self._verified_rules.
    '''
    choices = []

    dgast, dgann = d_ast_parse.parse_text_dbg(code, 'py')
    choicable_nodes = pvpy.ChoicableNodeExtractor.extract_choicable_nodes(code)

    for choicable_node in choicable_nodes:
      choicable_range_cursor = d_ast_parse.get_range_cursor(dgast, choicable_node.get_node_id())
      all_range_cursors = d_ast_parse.get_all_range_cursors_under(choicable_range_cursor)
      for range_cursor in all_range_cursors:
        range_cursor_unparsed = d_ast_parse.range_cursor_pretty_print(range_cursor, dgann, code)
        if range_cursor_unparsed in self._verified_rules:
          rule = self._verified_rules[range_cursor_unparsed]
          rule_idx_in_matcher_group = self.get_rule_idx_in_matcher_group(rule)
          choice_identifier = d_ast_parse.range_cursor_to_choice_identifier(range_cursor)
          choices.append((choice_identifier, rule_idx_in_matcher_group))

    return choices

  # SERIALIZATION METHODS
  def to_str_ruleset(self) -> str:
    '''
    Convert the ruleset to a plain string representation.
    '''
    return '\n\n'.join([str(rule) for rule in self.rules])

  def to_dict(self) -> dict:
    '''
    Serialize the Ruleset to a dict.
    '''
    res = {
      'type': 'Ruleset',
      'rules': [rule.to_dict() for rule in self.rules],
      'verified_rules': {k: v.to_dict() for k, v in self._verified_rules.items()},
    }
    return res

  @classmethod
  def from_starting_ruleset(cls, starting_ruleset: str) -> Ruleset:
    '''
    Create a Ruleset from a plain string representation of starting rules.
    '''
    ruleset = cls()
    rules, _ = d_grammar_rules.parse_analyze_rules(starting_ruleset)
    for rule in rules:
      ruleset.rules.append(StartingTRule(rule))
    ruleset._update_matcher_groups()
    return ruleset

  @classmethod
  def from_dict(cls, data: dict) -> Ruleset:
    '''
    Create a Ruleset from a serialized dict.
    '''
    assert data['type'] == 'Ruleset', 'Expected type to be Ruleset'
    ruleset = cls()
    for rule_data in data['rules']:
      if rule_data['type'] == 'StartingTRule':
        rule = StartingTRule.from_dict(rule_data)
      elif rule_data['type'] == 'LearnedTRule':
        rule = LearnedTRule.from_dict(rule_data)
      else:
        raise ValueError(f'Unknown rule type: {rule_data["type"]}')
      ruleset.rules.append(rule)
    ruleset._update_matcher_groups()
    return ruleset
