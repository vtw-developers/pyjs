import json
from abc import ABC
from typing import List

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
  def asdict(self) -> str:
    res = {
      'type': 'StartingRule',
      'rule_str': self.__str__(),
    }
    return res

  @classmethod
  def from_dict(self, data: dict) -> 'StartingRule':
    '''
    Create a StartingRule from a dict.
    PARAM data: a dictionary representing a StartingRule.
    '''
    assert data['type'] == 'StartingRule', 'Expected type to be StartingRule'
    parsed_rules, _ = d_grammar_rules.parse_analyze_rules(data['rule_str'])
    assert len(parsed_rules) == 1, f'Expected exactly one rule, got {len(parsed_rules)}'
    rule = parsed_rules[0]
    return StartingRule(rule)


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
  def asdict(self) -> dict:
    res = {
      'type': 'CheckedRule',
      'rule_str': self.__str__(),
      'src_node_id': self.src_node_id,
      'src_stat_node_id': self.src_stat_node_id,
    }
    return res

  @classmethod
  def from_dict(cls, data: dict) -> 'CheckedRule':
    '''
    Create a CheckedRule from a dict.
    PARAM data: a dictionary representing a CheckedRule.
    '''
    assert data['type'] == 'CheckedRule', 'Expected type to be CheckedRule'
    parsed_rules, _ = d_grammar_rules.parse_analyze_rules(data['rule_str'])
    assert len(parsed_rules) == 1, f'Expected exactly one rule, got {len(parsed_rules)}'
    rule = parsed_rules[0]
    assert 'src_node_id' in data, 'Expected src_node_id in data'
    assert 'src_stat_node_id' in data, 'Expected src_stat_node_id in data'
    src_node_id = data['src_node_id']
    src_stat_node_id = data['src_stat_node_id']
    assert isinstance(src_node_id, int), 'Expected src_node_id to be an int'
    assert isinstance(src_stat_node_id, int), 'Expected src_stat_node_id to be an int'
    return CheckedRule(rule, src_node_id, src_stat_node_id)

  @classmethod
  def from_unchecked_rule(cls, rule: 'UncheckedRule') -> 'CheckedRule':
    '''
    Create a CheckedRule from an UncheckedRule.
    '''
    assert isinstance(rule, UncheckedRule), 'Expected rule to be an UncheckedRule'
    return CheckedRule(rule.rule, rule.src_node_id, rule.src_stat_node_id)


class UncheckedRule(LearnedRule):
  '''
  A translation rule that was learned using LLM, but has not
  been validated or invalidated by a test-driven approach.
  '''
  def asdict(self) -> dict:
    res = {
      'type': 'UncheckedRule',
      'rule_str': self.__str__(),
      'src_node_id': self.src_node_id,
      'src_stat_node_id': self.src_stat_node_id,
    }
    return res

  @classmethod
  def from_dict(cls, data: dict) -> 'UncheckedRule':
    '''
    Create an UncheckedRule from a dict.
    PARAM data: a dictionary representing an UncheckedRule.
    '''
    assert data['type'] == 'UncheckedRule', 'Expected type to be UncheckedRule'
    parsed_rules, _ = d_grammar_rules.parse_analyze_rules(data['rule_str'])
    assert len(parsed_rules) == 1, f'Expected exactly one rule, got {len(parsed_rules)}'
    rule = parsed_rules[0]
    assert 'src_node_id' in data, 'Expected src_node_id in data'
    assert 'src_stat_node_id' in data, 'Expected src_stat_node_id in data'
    src_node_id = data['src_node_id']
    src_stat_node_id = data['src_stat_node_id']
    assert isinstance(src_node_id, int), 'Expected src_node_id to be an int'
    assert isinstance(src_stat_node_id, int), 'Expected src_stat_node_id to be an int'
    return UncheckedRule(rule, src_node_id, src_stat_node_id)

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

  def exists(self, rule_id: int) -> bool:
    '''
    Check if a rule with the given ID exists in the ruleset.
    '''
    assert isinstance(rule_id, int), 'Expected rule_id to be an int'
    if rule_id < 0 or rule_id >= len(self.rules):
      return False
    return True

  def get_rule(self, rule_id: int) -> TRuleBase:
    '''
    Get a rule by its ID.
    PARAM rule_id: ID of the rule to get.
    '''
    assert isinstance(rule_id, int), 'Expected rule_id to be an int'
    if not self.exists(rule_id):
      raise IndexError(f'Rule with ID {rule_id} does not exist')
    return self.rules[rule_id]

  def set_rule(self, rule_id: int, rule: TRuleBase) -> None:
    '''
    Set a rule at the given ID.
    PARAM rule_id: ID of the rule to set.
    PARAM rule: the rule to set.
    '''
    assert isinstance(rule_id, int), 'Expected rule_id to be an int'
    if not self.exists(rule_id):
      raise IndexError(f'Rule with ID {rule_id} does not exist')
    assert isinstance(rule, TRuleBase), 'Expected rule to be an instance of TRuleBase'
    self.rules[rule_id] = rule

  def to_string(self) -> str:
    return str(self)

  def to_json(self) -> str:
    '''
    Convert the ruleset to a JSON string.
    '''
    return json.dumps(self.asdict(), indent=2)

  def asdict(self) -> dict:
    res = {
      'type': 'Ruleset',
      'rules': [rule.asdict() for rule in self.rules],
    }
    return res

  @classmethod
  def from_dict(cls, data: dict) -> 'Ruleset':
    '''
    Create a Ruleset from a dict.
    PARAM data: a dictionary representing a Ruleset.
    '''
    assert data['type'] == 'Ruleset', 'Expected type to be Ruleset'
    ruleset = cls()
    for rule_data in data['rules']:
      if rule_data['type'] == 'StartingRule':
        rule = StartingRule.from_dict(rule_data)
      elif rule_data['type'] == 'CheckedRule':
        rule = CheckedRule.from_dict(rule_data)
      elif rule_data['type'] == 'UncheckedRule':
        rule = UncheckedRule.from_dict(rule_data)
      else:
        raise ValueError(f'Unknown rule type: {rule_data["type"]}')
      ruleset.rules.append(rule)
    return ruleset

  def prepend_rule(self, rule: TRuleBase) -> None:
    self.rules.insert(0, rule)

  @classmethod
  def from_starting_ruleset(cls, rules_str: str):
    ruleset = cls()
    rules, _ = d_grammar_rules.parse_analyze_rules(rules_str)
    for rule in rules:
      ruleset.rules.append(StartingRule(rule))
    return ruleset
