from abc import ABC
from typing import List, Set

import d_grammar_rules


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


class StartingRule(TRuleBase):
  '''
  A class that represents a translation rule that appears
  in the starting ruleset. It is assumed to be validated
  by the user manually.
  '''


class LearnedRule(TRuleBase, ABC):
  '''
  A translation rule that has been learned using LLM.
  '''
  def __init__(self, rule: dict, src_node_id: int, src_stat_node_id: int):
    '''
    PARAM src_node_id: ID of the node from which this rule was learned
    PARAM src_stat_node_id: ID of the statement node under which this rule was learned
    '''
    super().__init__(rule)
    assert isinstance(src_node_id, int), \
      f'Expected src_node_id to be an int, got {type(src_node_id)}'
    assert isinstance(src_stat_node_id, int), \
      f'Expected src_stat_node_id to be an int, got {type(src_stat_node_id)}'
    self.src_node_id = src_node_id
    self.src_stat_node_id = src_stat_node_id


class CheckedRule(LearnedRule):
  '''
  A translation rule that has been validated or invalidated
  by a test-driven approach.
  '''
  def __init__(self, rule: dict, src_node_id: int, src_stat_node_id: int):
    '''
    PARAM valid_for: a list of node IDs for which the rule is valid.
    PARAM invalid_for: a list of node IDs for which the rule is invalid.
    '''
    super().__init__(rule, src_node_id, src_stat_node_id)
    self.valid_for : Set[int] = set()
    self.invalid_for : Set[int] = set()

  def set_valid_for(self, node_id: int) -> None:
    assert node_id not in self.valid_for, 'redundant: Node ID already in valid_for'
    assert node_id not in self.invalid_for, 'clash: Node ID already in invalid_for'
    self.valid_for.add(node_id)

  def set_invalid_for(self, node_id: int) -> None:
    assert node_id not in self.valid_for, 'clash: Node ID already in valid_for'
    assert node_id not in self.invalid_for, 'redundant: Node ID already in invalid_for'
    self.invalid_for.add(node_id)

  @classmethod
  def from_unchecked_rule(cls, rule: 'UncheckedRule') -> 'CheckedRule':
    '''
    Create a CheckedRule from an UncheckedRule.
    '''
    return CheckedRule(rule.rule, rule.src_node_id, rule.src_stat_node_id)


class UncheckedRule(LearnedRule):
  '''
  A translation rule that was learned using LLM, but has not
  been validated or invalidated by a test-driven approach.
  '''
  @classmethod
  def from_str(cls, rule_str: str, src_node_id: int, src_stat_node_id: int) -> 'UncheckedRule':
    '''
    PARAM rule_str: a string representing a translation rule in the standard format.
    '''
    rules, _ = d_grammar_rules.parse_analyze_rules(rule_str)
    assert len(rules) == 1, f'Expected exactly one rule, got {len(rules)}'
    rule = rules[0]
    return UncheckedRule(rule, src_node_id, src_stat_node_id)


class Ruleset:
  def __init__(self):
    self.rules : List[TRuleBase] = []

  def __str__(self):
    return '\n\n'.join([str(rule) for rule in self.rules])

  def to_string(self) -> str:
    return str(self)

  def prepend_rule(self, rule: TRuleBase) -> None:
    self.rules.insert(0, rule)

  @classmethod
  def from_starting_ruleset(cls, rules_str: str):
    ruleset = cls()
    rules, _ = d_grammar_rules.parse_analyze_rules(rules_str)
    for rule in rules:
      ruleset.rules.append(StartingRule(rule))
    return ruleset
