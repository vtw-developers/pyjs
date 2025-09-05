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
  def __init__(self, rule_parsed: dict):
    '''
    PARAM rule_parsed: a dictionary representing a translation rule
    as parsed by d_grammar_rules.parse_analyze_rules().
    '''
    assert isinstance(rule_parsed, dict), f'Expected rule to be a dict, got {type(rule_parsed)}'
    assert 'type' in rule_parsed, 'Rule must have a "type" key'
    assert 'match' in rule_parsed, 'Rule must have a "match" key'
    assert 'expand' in rule_parsed, 'Rule must have a "expand" key'
    self.rule_parsed = rule_parsed

  def __str__(self):
    return self.to_rule_str()

  def __repr__(self):
    return f'{self.__class__.__name__} {str(self.rule_parsed)}'

  def __eq__(self, obj) -> bool:
    if not isinstance(obj, TRuleBase):
      raise ValueError(f'Cannot use == with {type(obj)}')
    return str(self.rule_parsed) == str(obj.rule_parsed)

  def get_matcher_signature(self) -> str:
    return str(self.rule_parsed['match'])

  @classmethod
  def parse_rule_str(cls, rule_str: str) -> dict:
    '''
    Parse a rule string into a rule dict.
    '''
    rules_parsed, _ = d_grammar_rules.parse_analyze_rules(rule_str)
    assert len(rules_parsed) == 1, f'Expected exactly one rule, got {len(rules_parsed)}'
    return rules_parsed[0]

  # SERIALIZATION METHODS
  def to_rule_str(self) -> str:
    '''
    Convert the rule to a plain string representation.
    '''
    return d_grammar_rules.pretty_rule(self.rule_parsed)

  def to_dict(self) -> dict:
    '''
    Serialize the rule to a dict.
    '''
    res = {
      'type': self.__class__.__name__,
      'rule_str': self.to_rule_str(),
    }
    return res

  @classmethod
  def from_dict(cls, rule_serialized: dict) -> TRuleBase:
    '''
    Create a rule instance from a serialized dict.
    '''
    if rule_serialized['type'] == 'StartingTRule':
      return StartingTRule.from_dict(rule_serialized)
    elif rule_serialized['type'] == 'StandardTRule':
      return StandardTRule.from_dict(rule_serialized)
    elif rule_serialized['type'] == 'StatementOverfittedTRule':
      return StatementOverfittedTRule.from_dict(rule_serialized)
    else:
      raise ValueError(f'Unknown rule type: {rule_serialized["type"]}')


class StartingTRule(TRuleBase):
  '''
  A class that represents a translation rule that appears
  in the starting ruleset. It is assumed to be valid.
  '''
  @classmethod
  def from_dict(cls, rule_serialized: dict) -> StartingTRule:
    '''
    Create a StartingTRule instance from a serialized dict.
    '''
    assert rule_serialized['type'] == 'StartingTRule', f'Expected type to be StartingTRule, got {rule_serialized["type"]}'
    rule_str = rule_serialized['rule_str']
    rule_parsed = cls.parse_rule_str(rule_str)
    return cls(rule_parsed)


class LearnedTRuleBase(TRuleBase, ABC):
  '''
  An abstract class that represents a learned translation rule.
  '''
  def __init__(
    self,
    rule_parsed: dict,
    stat_nid: int,
    simple_ntext: str,
  ):
    super().__init__(rule_parsed)
    self.stat_nid = stat_nid
    self.simple_ntext = simple_ntext

  # SERIALIZATION METHODS
  def to_dict(self) -> dict:
    '''
    Serialize the learned rule to a dict.
    '''
    res = super().to_dict()
    res.update({
      'stat_nid': self.stat_nid,
      'simple_ntext': self.simple_ntext,
    })
    return res


class StandardTRule(LearnedTRuleBase):
  '''
  A class that represents a translation rule that was
  learned using the standard learning method.
  '''
  @classmethod
  def from_dict(cls, rule_serialized: dict) -> StandardTRule:
    '''
    Create a StandardTRule instance from a serialized dict.
    '''
    assert rule_serialized['type'] == 'StandardTRule', f'Expected type to be StandardTRule, got {rule_serialized["type"]}'
    rule_str = rule_serialized['rule_str']
    rule_parsed = cls.parse_rule_str(rule_str)
    stat_nid = rule_serialized['stat_nid']
    simple_ntext = rule_serialized['simple_ntext']
    return cls(rule_parsed, stat_nid, simple_ntext)


class StatementOverfittedTRule(LearnedTRuleBase):
  '''
  A class that represents a translation rule that was
  learned using the recovery learning method to translate
  a specific statement directly.
  '''
  @classmethod
  def from_dict(cls, rule_serialized: dict) -> StatementOverfittedTRule:
    '''
    Create a StatementOverfittedTRule instance from a serialized dict.
    '''
    assert rule_serialized['type'] == 'StatementOverfittedTRule', f'Expected type to be StatementOverfittedTRule, got {rule_serialized["type"]}'
    rule_str = rule_serialized['rule_str']
    rule_parsed = cls.parse_rule_str(rule_str)
    stat_nid = rule_serialized['stat_nid']
    simple_ntext = rule_serialized['simple_ntext']
    return cls(rule_parsed, stat_nid, simple_ntext)


class Ruleset:
  '''
  Represents a set of translation rules.

  PROPERTY matcher_groups: is a dictionary that groups rules
  by their matcher signatures.
  INV: rules in self._verified_rules are also in self.rules
  '''
  def __init__(self):
    self.rules : List[TRuleBase] = []

    '''
    Matcher groups contains groups of rules that share the same matcher signature.
    '''
    self.matcher_groups: Dict[str, List[TRuleBase]] = {}

    '''
    Verified rules are rules that were validated based on tests
    to be able to correctly translate a specific AST node.
    Verified rules are "guaranteed" to work for the matched AST.
    '''
    self._verified_rules: Dict[str, TRuleBase] = {}

    '''
    Unverifiable rules are rules that could not be verified
    based on tests because the AST nodes they match are not
    loggable. Unlike verified rules, a single AST node can
    map to multiple unverifiable rules, because they might share
    the same matcher signature but have different expansions.
    '''
    self._unverifiable_rules: Dict[str, List[TRuleBase]] = {}

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

  def get_stat_overfitted_rules(self) -> List[StatementOverfittedTRule]:
    '''
    Get all StatementOverfittedTRule rules in the ruleset.
    '''
    return [rule for rule in self.rules if isinstance(rule, StatementOverfittedTRule)]

  # VERIFIED RULES RELATED
  def update_verified_rules(self, unparsed_ast: str, rule: TRuleBase) -> None:
    assert isinstance(unparsed_ast, str), f'Unexpected type {type(unparsed_ast)}'
    assert isinstance(rule, TRuleBase), f'Unexpected type {type(rule)}'
    assert self.get_rule_ref(rule) is not None, \
      'Rule must be in self.rules to be added to verified rules'

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

  def merge_verified_rules_from(self, ruleset_serialized: dict) -> None:
    '''
    NOTE if ruleset_serialized has a verified rule for an AST that
    already exists in self._verified_rules, it will be ignored.
    If ruleset_serialized has a rule that does not exist in self.rules,
    it will be ignored. This makes sure that self.rules are the only
    rules that we have.
    '''
    assert isinstance(ruleset_serialized, dict), f'Unexpected type {type(ruleset_serialized)}'
    for unparsed_ast, serialized_trule in \
      ruleset_serialized.get('verified_rules', {}).items():
      other_rule = TRuleBase.from_dict(serialized_trule)
      rule = self.get_rule_ref(other_rule)  # None if rule not in self.rules
      if rule:
        self.update_verified_rules(unparsed_ast, rule)
      else:
        logger.warning(f'Ignoring verified rule for "{unparsed_ast}" because it is not in self.rules.')

  # UNVERIFIABLE RULES RELATED
  def update_unverifiable_rules(self, unparsed_ast: str, rule: TRuleBase) -> None:
    assert isinstance(unparsed_ast, str), f'Unexpected type {type(unparsed_ast)}'
    assert isinstance(rule, TRuleBase), f'Unexpected type {type(rule)}'
    assert self.get_rule_ref(rule) is not None, \
      'Rule must be in self.rules to be added to unverifiable rules'
    self._unverifiable_rules.setdefault(unparsed_ast, []).append(rule)

  def get_unverifiable_rules(self, unparsed_ast: str) -> List[TRuleBase]:
    assert isinstance(unparsed_ast, str), f'Unexpected type {type(unparsed_ast)}'
    assert unparsed_ast in self._unverifiable_rules, f'No unverifiable rules for "{unparsed_ast}"'
    return self._unverifiable_rules[unparsed_ast]

  def unverifiable_rules_exist(self, unparsed_ast: str) -> bool:
    assert isinstance(unparsed_ast, str), f'Unexpected type {type(unparsed_ast)}'
    return unparsed_ast in self._unverifiable_rules

  def merge_unverifiable_rules_from(self, ruleset_serialized: dict) -> None:
    '''
    Check docs for merge_verified_rules_from().
    '''
    assert isinstance(ruleset_serialized, dict), f'Unexpected type {type(ruleset_serialized)}'
    for unparsed_ast, serialized_trules in \
      ruleset_serialized.get('unverifiable_rules', {}).items():
      for serialized_trule in serialized_trules:
        other_rule = TRuleBase.from_dict(serialized_trule)
        rule = self.get_rule_ref(other_rule)  # None if rule not in self.rules
        if rule:
          self.update_unverifiable_rules(unparsed_ast, rule)
        else:
          logger.warning(f'Ignoring unverifiable rule for "{unparsed_ast}" because it is not in self.rules.')

  # OTHER METHODS
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
    return '\n\n'.join([rule.to_rule_str() for rule in self.rules])

  def to_dict(self) -> dict:
    '''
    Serialize the Ruleset to a dict.
    '''
    res = {
      'type': 'Ruleset',
      'rules': [rule.to_dict() for rule in self.rules],
      'verified_rules': {k: v.to_dict() for k, v in self._verified_rules.items()},
      'unverifiable_rules': {
        k: [r.to_dict() for r in v] for k, v in self._unverifiable_rules.items()
      },
    }
    return res

  @classmethod
  def from_starting_ruleset(cls, starting_ruleset: str) -> Ruleset:
    '''
    Create a Ruleset from a plain string representation of starting rules.
    '''
    ruleset = cls()
    rules_parsed, _ = d_grammar_rules.parse_analyze_rules(starting_ruleset)
    for rule_parsed in rules_parsed:
      ruleset.rules.append(StartingTRule(rule_parsed))
    ruleset._update_matcher_groups()
    return ruleset

  @classmethod
  def from_dict(cls, ruleset_serialized: dict) -> Ruleset:
    '''
    Create a Ruleset from a serialized dict.
    '''
    assert ruleset_serialized['type'] == 'Ruleset', 'Expected type to be Ruleset'
    ruleset = cls()

    # ruleset.rules
    for rule_serialized in ruleset_serialized['rules']:
      rule = TRuleBase.from_dict(rule_serialized)
      ruleset.rules.append(rule)

    # ruleset.matcher_groups
    ruleset._update_matcher_groups()

    # ruleset.verified_rules
    ruleset.merge_verified_rules_from(ruleset_serialized)

    # ruleset._unverifiable_rules
    ruleset.merge_unverifiable_rules_from(ruleset_serialized)

    return ruleset
