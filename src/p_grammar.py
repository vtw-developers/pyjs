from __future__ import annotations

import copy
import json
import random
import string
from collections import deque
from typing import Callable, Dict, List, Optional, Set, Tuple, Union

import d_ast_parse
import p_consts
import p_data_structures
import p_grammar
import p_subject
import p_utils
import p_visitor_py


logger = p_utils.setup_logger(__name__)


ERR_SCHEMA = 'grammar schema is violated'
ERR_INVRULE = 'invalid rule type'


# Functions that generate tokens
def PY_gen_identifier() -> str:
  '''Generate an identifier according to Python grammar'''
  size = random.randint(1, 4)
  chars = list(string.ascii_lowercase)
  sample = random.sample(population=chars, k=size)
  # prepend `id_` to make sure that we don't return a reserved word like `if`
  return 'id_' + ''.join(sample)


def PY_gen_integer() -> str:
  '''Generate an integer according to Python grammar'''
  minval, maxval = 1, 10000
  value = random.randint(minval, maxval)
  return str(value)


def PY_gen_float() -> str:
  '''Generate a float according to Python grammar'''
  decimals = 2
  minval, maxval = 1, 100
  value = round(random.uniform(minval, maxval), decimals)
  return str(value)


def PY_gen_string() -> str:
  '''Generate a string literal according to Python grammar'''
  size = 5
  value = ''.join(random.sample(string.ascii_lowercase, size))
  return f'"{value}"'


# This dictionary stores generators for some Python nodes in tree-sitter grammar.
# We need this as a temporary solution to generating tokens from patterns.
# NOTE This dictionary is used in ranking node types in `get_alternative_starting_node_type`,
# Node types with better generators should appear first.
PY_GEN : Dict[str, Callable] = {
  'identifier': PY_gen_identifier,
  'integer': PY_gen_integer,
  'float': PY_gen_float,
  'string': PY_gen_string,
}

# PP - production path
class PP_UnreachableError(RuntimeError): pass
class PP_CycleError(RuntimeError): pass

# AM - AST mapping
class AM_UnmappableError(RuntimeError): pass

# GA - generate AST
class GA_CycleError(RuntimeError): pass
class GA_NoValidChoiceError(RuntimeError): pass
class GA_NotImplementedError(RuntimeError): pass

# RS - rule sequence
class RS_UnreachableError(RuntimeError): pass

# Errors that are raised in intended API
class API_NoAlternativeError(RuntimeError): pass


class TreeSitterGrammar():
  '''
  Rule types: alias, blank, string, pattern, symbol, seq, choice, repeat1, repeat, token, field, prec
  Composite rule types: sep1, commaSep1, optional
  '''

  # cache use id `self.get_production_paths_deprecated`
  get_production_paths_cache_deprecated = {}

  def __init__(self, name, rules, extras, precedences, externals, inline, conflicts, supertypes) -> None:
    self.name : str = name
    self.rules : Dict[str, Rule] = rules
    self.extras = extras
    self.precedences = precedences
    self.externals : List[SymbolRule] = externals
    self.inline = inline
    self.conflicts = conflicts
    self.supertypes : List[str] = supertypes

  def __str__(self) -> str:
    return f'name={self.name}, {len(self.rules)} rules'

  @classmethod
  def from_dict(cls, grammar_obj: dict) -> TreeSitterGrammar:
    '''
    parse according to https://github.com/tree-sitter/tree-sitter/blob/master/cli/src/generate/grammar-schema.json
    '''
    assert 'name' in grammar_obj
    assert 'rules' in grammar_obj

    name = grammar_obj['name']
    rules = cls._parse_rules(grammar_obj['rules'])
    extras, precedences, externals, inline, conflicts, supertypes = [None] * 6

    if 'extras' in grammar_obj:
      extras = cls._parse_extras(grammar_obj['extras'])
    if 'precedences' in grammar_obj:
      precedences = cls._parse_precedences(grammar_obj['precedences'])
    if 'externals' in grammar_obj:
      externals = cls._parse_externals(grammar_obj['externals'])
    if 'inline' in grammar_obj:
      inline: List[str] = grammar_obj['inline']
    if 'conflicts' in grammar_obj:
      conflicts: List[List[str]] = grammar_obj['conflicts']
    if 'supertypes' in grammar_obj:
      supertypes: List[str] = grammar_obj['supertypes']

    return TreeSitterGrammar(name, rules, extras, precedences, externals, inline, conflicts, supertypes)

  @classmethod
  def _parse_rules(cls, rules_dict: dict) -> Dict[str, Rule]:
    rules = {}
    for rule_name, rule_dict in rules_dict.items():
      rule = Rule.from_dict(rule_dict, None)
      rules[rule_name] = rule
    return rules

  @classmethod
  def _parse_extras(cls, extras: list) -> List[Rule]:
    extras_parsed = [Rule.from_dict(rule, None) for rule in extras]
    return extras_parsed

  @classmethod
  def _parse_precedences(cls, precedences: list) -> List[List[Rule]]:
    precedences_parsed = []
    for precs_row in precedences:
      precs = [Rule.from_dict(rule, None) for rule in precs_row]
      precedences_parsed.append(precs)
    return precedences_parsed

  @classmethod
  def _parse_externals(cls, externals: list) -> List[SymbolRule]:
    externals_parsed = []
    for rule_dict in externals:
      assert rule_dict['type'] == 'SYMBOL', 'grammar.externals is expected to have only symbol rules'
      externals_parsed.append(SymbolRule.from_dict(rule_dict, None))
    return externals_parsed

  def is_external(self, rule_name: str) -> bool:
    return any(map(lambda rule: rule.name == rule_name, self.externals))

  def is_hidden(self, rule_name: str) -> bool:
    '''
    Hidden rules do not appear in AST.
    https://tree-sitter.github.io/tree-sitter/creating-parsers#hiding-rules
    '''
    if rule_name.startswith('_'):
      return True
    if rule_name in self.supertypes:
      return True
    return False

  def is_supertype(self, rule_name: str) -> bool:
    '''
    https://tree-sitter.github.io/tree-sitter/using-parsers#static-node-types
    '''
    return rule_name in self.supertypes

  def is_comma_sep1(self, rule: Rule) -> bool:
    '''
    Return True if `rule` is commaSep1 rule, False otherwise
    commaSep1 appears in tree-sitter grammars as a convenience function (grammar.js)

    seq:
      - $.rule
      - repeat:
        - seq:
          - String(",")
          - $.rule

    NOTE TODO we may not need this method, as `self.is_sep1` would be sufficient.
    '''
    result = self.is_sep1(rule)
    return result is not None and result[1] == ','

  def is_sep1(self, rule: Rule) -> Union[None, Tuple[Rule, str]]:
    '''
    Return None if `rule` is not a sep1 rule.
    Return Tuple[repeating_rule, separator] otherwise.

    sep1 appears in tree-sitter grammars as a convenience function (grammar.js).

    Structure of sep1 in grammar.json:
    seq:
      - $.rule
      - repeat:
        - seq:
          - String("<anything>")
          - $.rule
    '''
    # has to be sequence rule
    if not isinstance(rule, SeqRule):
      return None
    # has to have two members
    if len(rule.members) != 2:
      return None
    # second member has to be repeat
    _second = rule.members[1]
    if not isinstance(_second, RepeatRule):
      return None
    # content of repeat should be sequence
    __rep_content = _second.content
    if not isinstance(__rep_content, SeqRule):
      return None
    # sequence should have two elements
    ___seq_members = __rep_content.members
    if len(___seq_members) != 2:
      return None
    # the first member should be String("<anything>")
    ___first = ___seq_members[0]
    if not isinstance(___first, StringRule):
      return None
    # the second member should be equal to whatever is being repeated
    ___rule = ___seq_members[1]
    if ___rule != rule.members[0]:
      return None

    # the rule is a sep1 rule at this point
    # capture separator, and the repeating rule
    separator = ___first.value
    rep_rule = rule.members[0]
    return rep_rule, separator

  def is_optional(self, rule: Rule) -> Union[None, Rule]:
    '''
    Return None if `rule` is not an optional rule.
    Return `optional_rule` otherwise.

    Optional rule is a choice between something and `BlankRule`

    Structure of sep1 in grammar.json:
    choice:
      - $.rule
      - blank

    NOTE In more complex cases, some other rules may be optional. For example:
    - alias(optional($.else_clause), $.else_clause)
    - field('alternative', optional($.else_clause))
    '''
    if isinstance(rule, AliasRule):
      return self.is_optional(rule.content)
    if isinstance(rule, FieldRule):
      return self.is_optional(rule.content)

    # NOTE tree-sitter grammar for python does not include the cases below.
    # They can be removed/commented for improving performance.
    if isinstance(rule, PrecRule):
      is_optional_res = self.is_optional(rule.content)
      assert is_optional_res is None, 'prec rule contains an optional, consider adding this case'
    if isinstance(rule, RepeatRule):
      is_optional_res = self.is_optional(rule.content)
      assert is_optional_res is None, 'rep rule contains an optional, consider adding this case'
    if isinstance(rule, Repeat1Rule):
      is_optional_res = self.is_optional(rule.content)
      assert is_optional_res is None, 'rep1 rule contains an optional, consider adding this case'

    # rule has to be choice
    if not isinstance(rule, ChoiceRule):
      return None
    # should contain two members
    if len(rule.members) != 2:
      return None
    # second member should be blank
    if not isinstance(rule.members[1], BlankRule):
      return None
    # first member should not be blank
    if isinstance(rule.members[0], BlankRule):
      return None
    optional_rule = rule.members[0]
    return optional_rule

  def get_production_paths_deprecated(self, from_rule: str, to_rule: str) -> List[List[str]]:
    '''
    Uses tree search algorithm (recursive).
    Raises PP_UnreachableError if path is not found.
    The path contains all symbols (even hidden rules)
    from the grammar including `from_rule` and `to_rule`.

    RAISE PP_UnreachableError
    '''
    def _get_symbols_under(rule_name: str) -> Set[str]:
      if self.is_external(rule_name):
        raise PP_UnreachableError
      all_symbols = self.rules[rule_name].get_all_symbols()
      return set(map(lambda r: r.name, all_symbols))

    def _get_production_paths_rec(from_rule: str, to_rule: str, parent_path: List[str]) -> List[List[str]]:
      # base case 1: `to_rule` is found
      if from_rule == to_rule:
        return [[to_rule]]
      # base case 2: cycle detected
      if from_rule in parent_path:
        raise PP_CycleError
      # recursive section
      paths = []
      children = _get_symbols_under(from_rule)
      for child in children:
        try:
          child_paths = _get_production_paths_rec(child, to_rule, parent_path + [from_rule])
        except (PP_CycleError, PP_UnreachableError):
          continue
        for path in child_paths:
          path.insert(0, from_rule)
        paths.extend(child_paths)

      if len(paths) == 0:
        raise PP_UnreachableError
      return paths

    if (from_rule, to_rule) in TreeSitterGrammar.get_production_paths_cache_deprecated:
      return TreeSitterGrammar.get_production_paths_cache_deprecated[(from_rule, to_rule)]
    paths = _get_production_paths_rec(from_rule, to_rule, [])
    TreeSitterGrammar.get_production_paths_cache_deprecated[(from_rule, to_rule)] = paths

    return paths

  def generate_simplest_ast(self, root_node: str) -> list:
    '''
    Given a starting node type return the simplest randomly generated DuoGlot-style AST.
    This method is a starting point for constraint-based generation.
    '''

    # Some sanity check. This may be incomplete.
    assert not self.is_external(root_node)
    assert root_node in self.rules

    # NOTE assume that the grammar language is Python
    # Return pre-made AST for certain node types,
    # for which we cannot generate an AST (e.g. `integer`, `float`, etc.)
    if root_node in PY_GEN:
      value = PY_GEN[root_node]()
      return [root_node, value]

    # `Rule.stack_generation` is used to detect and avoid cycles
    Rule.stack_generation.clear()  # reset it first
    Rule.stack_generation.append(root_node)

    rule = self.rules[root_node]
    simplest_ast, complexity, flatten = rule.generate_simplest_ast(self)

    Rule.stack_generation.clear()

    # in some cases, `simplest_ast` can be none (e.g. `block`)
    if simplest_ast is None:
      return [root_node]

    ast = [root_node]
    if isinstance(simplest_ast, list) and flatten:
      ast.extend(simplest_ast)
    else:
      ast.append(simplest_ast)
    return ast

  def get_symbols_under(self, rule_name: str) -> Set[str]:
    '''
    Return all symbols under `rule_name`.
    '''
    if self.is_external(rule_name):
      return set()
    all_symbols = self.rules[rule_name].get_all_symbols()
    return set(map(lambda r: r.name, all_symbols))


class Rule():
  # stack used by `self.get_ast_mapping` to detect cycles
  stack_ast_mapping : List[str] = []
  # stack used by `self.generate_simplest_ast` to detect cycles
  stack_generation : List[str] = []

  def __init__(self) -> None:
    self.parent: Rule = None

  def __str__(self) -> str:
    return self.__class__.__name__

  def __repr__(self) -> str:
    return self.__class__.__name__

  # abstract method
  def __eq__(self, value: object) -> bool:
    raise NotImplementedError

  def __ne__(self, value: object) -> bool:
    return not self.__eq__(value)

  @classmethod
  def from_dict(cls, rule_dict: dict, parent: Rule) -> Rule:
    '''create a rule object from a dict containing a rule definition'''
    assert 'type' in rule_dict,  ERR_SCHEMA
    rule_type = rule_dict['type']

    if rule_type == 'REPEAT':
       return RepeatRule.from_dict(rule_dict, parent)
    elif rule_type == 'REPEAT1':
      return Repeat1Rule.from_dict(rule_dict, parent)
    elif rule_type == 'SYMBOL':
      return SymbolRule.from_dict(rule_dict, parent)
    elif rule_type == 'CHOICE':
      return ChoiceRule.from_dict(rule_dict, parent)
    elif rule_type == 'SEQ':
      return SeqRule.from_dict(rule_dict, parent)
    elif rule_type == 'STRING':
      return StringRule.from_dict(rule_dict, parent)
    elif rule_type == 'BLANK':
      return BlankRule.from_dict(rule_dict, parent)
    elif rule_type == 'PATTERN':
      return PatternRule.from_dict(rule_dict, parent)
    elif rule_type == 'ALIAS':
      return AliasRule.from_dict(rule_dict, parent)
    elif rule_type == 'FIELD':
      return FieldRule.from_dict(rule_dict, parent)
    elif rule_type in ['TOKEN', 'IMMEDIATE_TOKEN']:
      return TokenRule.from_dict(rule_dict, parent)
    elif rule_type in ['PREC', 'PREC_LEFT', 'PREC_RIGHT', 'PREC_DYNAMIC']:
      return PrecRule.from_dict(rule_dict, parent)
    else:
      raise TypeError(ERR_INVRULE)

  def set_parent(self, parent: Rule) -> None:
    self.parent = parent

  # abstract method
  def get_all_symbols(self) -> List[SymbolRule]:
    '''return all symbols under self'''
    raise NotImplementedError(repr(self))

  # abstract method
  def get_ast_mapping(
    self,
    nodes: List[p_data_structures.DuoGlotNode],
    grammar: TreeSitterGrammar
  ) -> List[Tuple[p_data_structures.DuoGlotNode, SymbolRule|AliasRule, List[str]]]:
    '''
    Given a list of AST nodes, return a mapping of
    each non-terminal node to a SymbolRule (or AliasRule) instance.

    RETURN [(NTNode, SymbolRule|AliasRule, List[str])]
    RAISE AM_UnmappableError

    PRE1: are_siblings(nodes)
    PRE2: all([node.node_type != 'py.comment' for node in nodes])

    TODO cannot handle grammar extras such as comments
    '''
    raise NotImplementedError(repr(self))

  # abstract method
  def generate_simplest_ast(self, grammar: TreeSitterGrammar) -> tuple:
    '''
    For documentation, check `TreeSitterGrammar.generate_simplest_ast`.

    The method generates a sequence of AST nodes that match the expansion of rule `self`.

    The format of the generated AST is identical/similar to DuoGlot-style AST.

    Return a list of tuples, where each tuple contains:
    1. Generated AST
       - None - if no AST can be generated
       - str - if the generated AST node is terminal
       - list - if the generated AST node is non-terminal
    2. Complexity of the generated AST
    3. Whether to flatten the generated AST or not. `flatten` makes sure that
       nodes at the same depth level are identical in `list` depth.
       For example, seq(seq(A, B), seq(C, D)) should be [A, B, C, D],
       but not [[A, B], [C, D]].
    '''
    raise NotImplementedError(repr(self))

  # abstract method
  def get_rule_seq_to_symbol_rule(self, sym_rule_name: str, grammar: TreeSitterGrammar) -> List[List[str]]:
    '''
    WHAT IT DOES?
    Get sequence of rules from a production to a SymbolRule.

    EXAMPLE
    assignment: $ => seq(
      field('left', $._left_hand_side),
      choice(
        seq('=', field('right', $._right_hand_side)),
        seq(':', field('type', $.type)),
        seq(':', field('type', $.type), '=', field('right', $._right_hand_side))
      )
    )

    for `assignment -> _left_hand_side` return [seq, field]

    RETURN
    if not found -> exception
    if found exactly one path -> path
    if found several paths -> all paths (should not happen?)
    '''
    raise NotImplementedError(repr(self))


class AliasRule(Rule):
  def __init__(self, named: bool, content: Rule, value: str) -> None:
    super().__init__()
    self.named = named
    self.content = content
    self.value = value

  def __str__(self) -> str:
    return f'alias to (\n{p_utils.indent(str(self.content))}\n)'

  # overrides an abstract method
  def __eq__(self, value: object) -> bool:
    if not isinstance(value, AliasRule):
      return False
    if self.named != value.named:
      return False
    if self.value != value.value:
      return False
    return self.content == value.content

  @classmethod
  def from_dict(cls, rule_dict: dict, parent: Rule) -> AliasRule:
    assert 'named' in rule_dict, ERR_SCHEMA
    assert 'content' in rule_dict, ERR_SCHEMA
    assert 'value' in rule_dict, ERR_SCHEMA
    named = rule_dict['named']
    content = Rule.from_dict(rule_dict['content'], None)
    value = rule_dict['value']
    this_rule = AliasRule(named, content, value)
    this_rule.set_parent(parent)
    content.set_parent(this_rule)
    return this_rule

  # overrides an abstract method
  def get_all_symbols(self) -> List[SymbolRule]:
    if isinstance(self.content, SymbolRule):
      return [self.content]
    return self.content.get_all_symbols()

  # overrides an abstract method
  def get_ast_mapping(self, nodes: List[p_data_structures.DuoGlotNode], grammar: TreeSitterGrammar) -> List[Tuple]:
    if len(nodes) == 1:
      node = nodes[0]
      # TODO what to do in else case of this if statement?
      if node.is_nonterminal() and node.get_ts_node_type() == self.value:
        return [(node, self, Rule.stack_ast_mapping[:])]
    return self.content.get_ast_mapping(nodes, grammar)

  # overrides an abstract method
  def generate_simplest_ast(self, grammar: TreeSitterGrammar) -> tuple:
    '''
    Generate an AST rooted at `self.content` and name the root node as `self.value`.
    '''
    simplest_ast, complexity, flatten = self.content.generate_simplest_ast(grammar)

    # if no AST is generated, then `self.value` becomes a terminal
    # TODO this might be a buggy behavior in cases where `self.value` is non-terminal
    if simplest_ast is None:
      # cannot handle cases where we need to generate external rules
      if isinstance(self.content, SymbolRule) and grammar.is_external(self.content.name):
        msg = f'AliasRule({self.value}) cannot generate an AST for external rule "{self.content.name}"'
        raise GA_NotImplementedError(msg)
      return self.value, 1, False

    # if generated AST is non-terminal, replace the root node with `self.value`
    if isinstance(simplest_ast, list):
      simplest_ast[0] = self.value
      return simplest_ast, complexity, flatten

    # generated AST is terminal
    return [self.value, simplest_ast], complexity, flatten

  # overrides an abstract method
  def get_rule_seq_to_symbol_rule(self, sym_rule_name: str, grammar: TreeSitterGrammar) -> List[List[str]]:
    # we can return `self.name` if we want to include it in rule sequence
    if self.value == sym_rule_name:
      return [[]]
    raise RS_UnreachableError


class BlankRule(Rule):
  def __str__(self) -> str:
    return f'BLANK'

  # overrides an abstract method
  def __eq__(self, value: object) -> bool:
    if not isinstance(value, BlankRule):
      return False
    return True

  @classmethod
  def from_dict(cls, rule_dict: dict, parent: Rule) -> BlankRule:
    this_rule = BlankRule()
    this_rule.set_parent(parent)
    return this_rule

  # overrides an abstract method
  def get_all_symbols(self) -> List[SymbolRule]:
    return []

  # overrides an abstract method
  def get_ast_mapping(self, nodes: List[p_data_structures.DuoGlotNode], grammar: TreeSitterGrammar) -> List[Tuple]:
    raise AM_UnmappableError

  # overrides an abstract method
  def generate_simplest_ast(self, grammar: TreeSitterGrammar) -> tuple:
    return None, 0, False

  # overrides an abstract method
  def get_rule_seq_to_symbol_rule(self, sym_rule_name: str, grammar: TreeSitterGrammar) -> List[List[str]]:
    raise RS_UnreachableError


class ChoiceRule(Rule):
  def __init__(self, members: List[Rule]) -> None:
    super().__init__()
    self.members = members

  def __str__(self) -> str:
    choices = ', '.join(map(str, self.members))
    return f'choose from [\n{p_utils.indent(choices)}\n]'

  # overrides an abstract method
  def __eq__(self, value: object) -> bool:
    if not isinstance(value, ChoiceRule):
      return False
    for member, vmember in zip(self.members, value.members):
      if member != vmember:
        return False
    return True

  @classmethod
  def from_dict(cls, rule_dict: dict, parent: Rule) -> ChoiceRule:
    assert 'members' in rule_dict, ERR_SCHEMA
    members = [Rule.from_dict(member, None) for member in rule_dict['members']]
    this_rule = ChoiceRule(members)
    this_rule.set_parent(parent)
    for member in members:
      member.set_parent(this_rule)
    return this_rule

  # overrides an abstract method
  def get_all_symbols(self) -> List[SymbolRule]:
    symbol_rules = []
    for member in self.members:
      if isinstance(member, SymbolRule):
        symbol_rules.append(member)
      else:
        symbol_rules.extend(member.get_all_symbols())
    return symbol_rules

  # overrides an abstract method
  def get_ast_mapping(self, nodes: List[p_data_structures.DuoGlotNode], grammar: TreeSitterGrammar) -> List[tuple]:
    is_optional_res = grammar.is_optional(self)
    if is_optional_res is not None:
      optional_rule = is_optional_res
      mapping = optional_rule.get_ast_mapping(nodes, grammar)
      return mapping

    # NOTE can there be multiple matches? For now, return the mappings from the first member that matches.
    for member in self.members:
      try:
        mapping = member.get_ast_mapping(nodes, grammar)
        return mapping
      except AM_UnmappableError:
        continue
    raise AM_UnmappableError

  # overrides an abstract method
  def generate_simplest_ast(self, grammar: TreeSitterGrammar) -> tuple:
    '''
    Generate ASTs for each of choice options, and return the simplest one.
    '''
    gen_astcmplx : List[tuple] = []
    for member in self.members:
      try:
        member_astcmplx = member.generate_simplest_ast(grammar)
        gen_astcmplx.append(member_astcmplx)
      # skip members which cannot be used for generation
      except GA_CycleError:
        pass
      except GA_NoValidChoiceError:
        pass
      except GA_NotImplementedError:
        pass

    # have not generated anything from choice options
    if len(gen_astcmplx) == 0:
      raise GA_NoValidChoiceError

    # simplest AST is the one with minimum complexity
    simplest_ast = min(gen_astcmplx, key=lambda elem: elem[1])
    return simplest_ast

  # overrides an abstract method
  def get_rule_seq_to_symbol_rule(self, sym_rule_name: str, grammar: TreeSitterGrammar) -> List[List[str]]:
    # NOTE optional rules are `ChoiceRule`s in nature
    if grammar.is_optional(self):
      opt_rule = self.members[0]
      opt_rule_paths : List[List[str]] = opt_rule.get_rule_seq_to_symbol_rule(sym_rule_name, grammar)
      assert len(opt_rule_paths) > 0
      paths = [['optional'] + mp for mp in opt_rule_paths]
      return paths

    members_paths : List[List[str]] = []
    for member in self.members:
      try:
        member_paths = member.get_rule_seq_to_symbol_rule(sym_rule_name, grammar)
        members_paths.extend(member_paths)
      except RS_UnreachableError:
        pass
    if len(members_paths) == 0:
      raise RS_UnreachableError
    paths = [['choice'] + mp for mp in members_paths]
    return paths


class FieldRule(Rule):
  def __init__(self, name: str, content: Rule) -> None:
    super().__init__()
    self.name = name
    self.content = content

  def __str__(self) -> str:
    return f'field "{self.name}" to (\n{p_utils.indent(str(self.content))}\n)'

  # overrides an abstract method
  def __eq__(self, value: object) -> bool:
    if not isinstance(value, FieldRule):
      return False
    if self.name != value.name:
      return False
    return self.content == value.content

  @classmethod
  def from_dict(cls, rule_dict: dict, parent: Rule) -> FieldRule:
    assert 'name' in rule_dict, ERR_SCHEMA
    assert 'content' in rule_dict, ERR_SCHEMA
    name = rule_dict['name']
    content = Rule.from_dict(rule_dict['content'], None)
    this_rule = FieldRule(name, content)
    this_rule.set_parent(parent)
    content.set_parent(this_rule)
    return this_rule

  # overrides an abstract method
  def get_all_symbols(self) -> List[SymbolRule]:
    if isinstance(self.content, SymbolRule):
      return [self.content]
    return self.content.get_all_symbols()

  # overrides an abstract method
  def get_ast_mapping(self, nodes: List[p_data_structures.DuoGlotNode], grammar: TreeSitterGrammar) -> List[Tuple]:
    return self.content.get_ast_mapping(nodes, grammar)

  # overrides an abstract method
  def generate_simplest_ast(self, grammar: TreeSitterGrammar) -> tuple:
    return self.content.generate_simplest_ast(grammar)

  # overrides an abstract method
  def get_rule_seq_to_symbol_rule(self, sym_rule_name: str, grammar: TreeSitterGrammar) -> List[List[str]]:
    content_paths : List[List[str]] = self.content.get_rule_seq_to_symbol_rule(sym_rule_name, grammar)
    assert len(content_paths) > 0
    paths = [['field'] + mp for mp in content_paths]
    return paths


class PatternRule(Rule):
  def __init__(self, value: str) -> None:
    super().__init__()
    self.value = value

  def __str__(self) -> str:
    return f'pattern "{self.value}"'

  # overrides an abstract method
  def __eq__(self, value: object) -> bool:
    if not isinstance(value, PatternRule):
      return False
    return self.value == value.value

  @classmethod
  def from_dict(cls, rule_dict: dict, parent: Rule) -> PatternRule:
    assert 'value' in rule_dict, ERR_SCHEMA
    value = rule_dict['value']
    this_rule = PatternRule(value)
    this_rule.set_parent(parent)
    return this_rule

  # overrides an abstract method
  def get_all_symbols(self) -> List[SymbolRule]:
    return []

  # overrides an abstract method
  def get_ast_mapping(self, nodes: List[p_data_structures.DuoGlotNode], grammar: TreeSitterGrammar) -> List[Tuple]:
    raise AM_UnmappableError

  # overrides an abstract method
  def generate_simplest_ast(self, grammar: TreeSitterGrammar) -> tuple:
    raise GA_NotImplementedError('Cannot generate patterns at the moment.')

  # overrides an abstract method
  def get_rule_seq_to_symbol_rule(self, sym_rule_name: str, grammar: TreeSitterGrammar) -> List[List[str]]:
    raise RS_UnreachableError


class PrecRule(Rule):
  def __init__(self, content: Rule, value: Union[int, str]) -> None:
    super().__init__()
    self.content = content
    self.value = value

  def __str__(self) -> str:
    return f'precedence "{self.value}" to (\n{p_utils.indent(str(self.content))}\n)'

  # overrides an abstract method
  def __eq__(self, value: object) -> bool:
    if not isinstance(value, PrecRule):
      return False
    if self.value != value.value:
      return False
    return self.content == value.content

  @classmethod
  def from_dict(cls, rule_dict: dict, parent: Rule) -> PrecRule:
    assert 'content' in rule_dict, ERR_SCHEMA
    assert 'value' in rule_dict, ERR_SCHEMA
    content = Rule.from_dict(rule_dict['content'], None)
    value = rule_dict['value']
    this_rule = PrecRule(content, value)
    this_rule.set_parent(parent)
    content.set_parent(this_rule)
    return this_rule

  # overrides an abstract method
  def get_all_symbols(self) -> List[SymbolRule]:
    if isinstance(self.content, SymbolRule):
      return [self.content]
    return self.content.get_all_symbols()

  # overrides an abstract method
  def get_ast_mapping(self, nodes: List[p_data_structures.DuoGlotNode], grammar: TreeSitterGrammar) -> List[Tuple]:
    return self.content.get_ast_mapping(nodes, grammar)

  # overrides an abstract method
  def generate_simplest_ast(self, grammar: TreeSitterGrammar) -> tuple:
    return self.content.generate_simplest_ast(grammar)

  # overrides an abstract method
  def get_rule_seq_to_symbol_rule(self, sym_rule_name: str, grammar: TreeSitterGrammar) -> List[List[str]]:
    content_paths : List[List[str]] = self.content.get_rule_seq_to_symbol_rule(sym_rule_name, grammar)
    assert len(content_paths) > 0
    paths = [['prec'] + mp for mp in content_paths]
    return paths


class RepeatRule(Rule):
  def __init__(self, content: Rule) -> None:
    super().__init__()
    self.content = content

  def __str__(self) -> str:
    return f'repeating (\n{p_utils.indent(str(self.content))}\n)'

  # overrides an abstract method
  def __eq__(self, value: object) -> bool:
    if not isinstance(value, RepeatRule):
      return False
    return self.content == value.content

  @classmethod
  def from_dict(cls, rule_dict: dict, parent: Rule) -> RepeatRule:
    assert 'content' in rule_dict, ERR_SCHEMA
    content = Rule.from_dict(rule_dict['content'], None)
    this_rule = RepeatRule(content)
    this_rule.set_parent(parent)
    content.set_parent(this_rule)
    return this_rule

  # overrides an abstract method
  def get_all_symbols(self) -> List[SymbolRule]:
    if isinstance(self.content, SymbolRule):
      return [self.content]
    return self.content.get_all_symbols()

  # overrides an abstract method
  def get_ast_mapping(self, nodes: List[p_data_structures.DuoGlotNode], grammar: TreeSitterGrammar) -> List[Tuple]:
    '''Every node in `nodes` should match `self.content`'''
    mappings = []
    for node in nodes:
      mapping = self.content.get_ast_mapping([node], grammar)
      mappings.extend(mapping)
    return mappings

  # overrides an abstract method
  def generate_simplest_ast(self, grammar: TreeSitterGrammar) -> tuple:
    '''
    The simplest AST is the one with zero repeats for `self.content`.
    In some cases we might better return at least one repetition of `self.content`,
    like in the rule for `block`, where `block` is a `rep(statement)`
    '''
    # Treat `block` specially for now. If we avoid such special cases,
    # we might have to use the solution below where we treat `rep` as `rep1`
    # NOTE HACK
    if isinstance(self.parent, SeqRule) and Rule.stack_generation[-1] == 'block':
      return self.content.generate_simplest_ast(grammar)

    # This is how `rep` rule should behave.
    return None, 0, False

    # This variant returns a single repetition of `self.content`
    # to make sure that we don't have dangling non-terminal nodes.
    # return self.content.generate_simplest_ast(grammar)

  # overrides an abstract method
  def get_rule_seq_to_symbol_rule(self, sym_rule_name: str, grammar: TreeSitterGrammar) -> List[List[str]]:
    content_paths : List[List[str]] = self.content.get_rule_seq_to_symbol_rule(sym_rule_name, grammar)
    assert len(content_paths) > 0
    paths = [['repeat'] + mp for mp in content_paths]
    return paths


class Repeat1Rule(Rule):
  def __init__(self, content: Rule) -> None:
    super().__init__()
    self.content = content

  def __str__(self) -> str:
    return f'repeat1-ing (\n{p_utils.indent(str(self.content))}\n)'

  # overrides an abstract method
  def __eq__(self, value: object) -> bool:
    if not isinstance(value, Repeat1Rule):
      return False
    return self.content == value.content

  @classmethod
  def from_dict(cls, rule_dict: dict, parent: Rule) -> Repeat1Rule:
    assert 'content' in rule_dict, ERR_SCHEMA
    content = Rule.from_dict(rule_dict['content'], None)
    this_rule = Repeat1Rule(content)
    this_rule.set_parent(parent)
    content.set_parent(this_rule)
    return this_rule

  # overrides an abstract method
  def get_all_symbols(self) -> List[SymbolRule]:
    if isinstance(self.content, SymbolRule):
      return [self.content]
    return self.content.get_all_symbols()

  # overrides an abstract method
  def get_ast_mapping(self, nodes: List[p_data_structures.DuoGlotNode], grammar: TreeSitterGrammar) -> List[Tuple]:
    '''Every node in `nodes` should match `self.content`'''
    mappings = []
    for node in nodes:
      mapping = self.content.get_ast_mapping([node], grammar)
      mappings.extend(mapping)
    return mappings

  # overrides an abstract method
  def generate_simplest_ast(self, grammar: TreeSitterGrammar) -> tuple:
    '''
    Unlike rep(), here we should return a single repetition of `self.content`
    as the simplest AST.
    '''
    return self.content.generate_simplest_ast(grammar)

  # overrides an abstract method
  def get_rule_seq_to_symbol_rule(self, sym_rule_name: str, grammar: TreeSitterGrammar) -> List[List[str]]:
    content_paths : List[List[str]] = self.content.get_rule_seq_to_symbol_rule(sym_rule_name, grammar)
    assert len(content_paths) > 0
    paths = [['repeat1'] + mp for mp in content_paths]
    return paths


class SeqRule(Rule):
  def __init__(self, members: List[Rule]) -> None:
    super().__init__()
    self.members = members

  def __str__(self) -> str:
    choices = ', '.join(map(str, self.members))
    return f'sequence of [\n{p_utils.indent(choices)}\n]'

  # overrides an abstract method
  def __eq__(self, value: object) -> bool:
    if not isinstance(value, SeqRule):
      return False
    for member, vmember in zip(self.members, value.members):
      if member != vmember:
        return False
    return True

  @classmethod
  def from_dict(cls, rule_dict: dict, parent: Rule) -> SeqRule:
    assert 'members' in rule_dict, ERR_SCHEMA
    members = [Rule.from_dict(member, None) for member in rule_dict['members']]
    this_rule = SeqRule(members)
    this_rule.set_parent(parent)
    for member in members:
      member.set_parent(this_rule)
    return this_rule

  # overrides an abstract method
  def get_all_symbols(self) -> List[SymbolRule]:
    symbol_rules = []
    for member in self.members:
      if isinstance(member, SymbolRule):
        symbol_rules.append(member)
      else:
        symbol_rules.extend(member.get_all_symbols())
    return symbol_rules

  # overrides an abstract method
  def get_ast_mapping(self, nodes: List[p_data_structures.DuoGlotNode], grammar: TreeSitterGrammar) -> List[Tuple]:
    '''
    Greedy top-down parsing algorithm.

    NODES             RULES
    'def'             optional('async')
    identifier        'def'
    parameters        identifier
    '->'              parameters
    type              optional('->'  type)
    ':'               ':'
    block             block
    '''

    def _match_first_nodes_greedy(rule: Rule, nodes: List[p_data_structures.DuoGlotNode], grammar: TreeSitterGrammar) -> Tuple[int, List[tuple]]:
      '''
      greedy = match as much as possible
      Returns number of matched nodes and the mappings.
      Raises AM_UnmappableError.
      '''
      # When there are no nodes left to match, but there are still rules 'unused',
      # check whether the `rule` is obligated to be `used`.
      # For example, optional rule can match zero nodes, but ChoiceRule cannot.
      if len(nodes) == 0:
        is_optional_res = grammar.is_optional(rule)
        if isinstance(rule, RepeatRule):
          return 0, []
        elif is_optional_res is not None:
          return 0, []
        # as `_newline` in `_simple_statements` of Python grammar
        elif isinstance(rule, SymbolRule) and grammar.is_external(rule.name):
          return 0, []
        elif isinstance(rule, StringRule):
          return 0, []
        else:
          raise AM_UnmappableError

      # Starting from a `span` of 1, try to match first `span` elements of nodes by `rule`
      largest_span_mapping = None
      largest_span = 0
      for span in range(1, len(nodes) + 1):
        try:
          nodes_to_match = nodes[:span]
          mapping = rule.get_ast_mapping(nodes_to_match, grammar)
          largest_span_mapping = mapping
          largest_span = span
        except AM_UnmappableError:
          continue
      if largest_span_mapping is None:
        raise AM_UnmappableError
      return largest_span, largest_span_mapping

    def _get_rules_must_match() -> List[Rule]:
      '''
      Return a list of rules that have to be matched by AST nodes.
      For example, optionals do not have to be matched, as well as hidden rules.
      # TODO how about external rules?
      '''
      nonlocal grammar
      must_match_rules = []
      for rule in self.members:
        # optional rule doesn't have to match
        is_optional_res = grammar.is_optional(rule)
        if is_optional_res is not None:
          continue
        # hidden rule doesn't have to match
        if isinstance(rule, SymbolRule) and grammar.is_hidden(rule.name):
          continue
        # repeat rule doesn't have to match
        if isinstance(rule, RepeatRule):
          continue
        must_match_rules.append(rule)
      return must_match_rules

    def _treat_rep1_in_seq(rule: Repeat1Rule, nodes: List[p_data_structures.DuoGlotNode], grammar: TreeSitterGrammar) -> Tuple[int, List[tuple]]:
      '''
      Treat `Repeat1Rule` in `SeqRule` as a special case.
      `Repeat1Rule` must match at least one node
      '''
      assert isinstance(rule, Repeat1Rule), 'sanity check: rule must be a Repeat1Rule'

      total_span = 0
      all_mappings = []
      while True:
        try:
          if total_span >= len(nodes):
            assert total_span == len(nodes), 'sanity check: should not match more nodes than there are'
            break
          span, mapping = _match_first_nodes_greedy(rule.content, nodes[total_span:], grammar)
          total_span += span
          all_mappings.extend(mapping)
        except AM_UnmappableError:
          if total_span == 0:
            raise AM_UnmappableError
          else:
            return total_span, all_mappings
      return total_span, all_mappings

    # Since sep1 is a sequence rule, first we check if `self` is a sep1 rule.
    # If `self` is a sep1 rule, then each node in `nodes` excluding separators
    # should match the repeating rule in sep1.
    is_sep1_result = grammar.is_sep1(self)
    if bool(is_sep1_result):
      rep_rule, separator = is_sep1_result
      # NOTE separator is left unmatched
      # NOTE a premise that there are no rules after `sep1` is wrong (py.subscript)
      # rep_nodes = [n for n in nodes if not (n.is_terminal() and n.node_type == separator)]
      rep_nodes = [n for n in nodes if n.is_nonterminal()]
      mappings = []
      for rep_node in rep_nodes:
        mapping = rep_rule.get_ast_mapping([rep_node], grammar)
        mappings.extend(mapping)
      return mappings

    # nodes has to be at least of length
    # of the number of rules that have to be matched in the sequence
    must_match_rules = _get_rules_must_match()
    if len(nodes) < len(must_match_rules):
      raise AM_UnmappableError

    # try to match every rule in sequence with as many nodes as possible
    mappings = []
    num_nodes_matched = 0
    for rule_in_seq in self.members:
      nodes_to_match = nodes[num_nodes_matched:]

      is_sep1_res = grammar.is_sep1(rule_in_seq)
      is_optional_res = grammar.is_optional(rule_in_seq)

      # sep1 rule must match at least one node
      if is_sep1_res is not None:
        # NOTE rely on the premise that `sep1` rules always appear last
        # and match all the remaining nodes
        # TODO counterexample: py.subscript
        mapping = rule_in_seq.get_ast_mapping(nodes_to_match, grammar)
        span = len(nodes_to_match)

      # optional rule can match zero nodes
      elif is_optional_res is not None:
        optional_rule = is_optional_res
        # optional_nodes = [n for n in nodes_to_match if not n.is_terminal()]
        try:
          span, mapping = _match_first_nodes_greedy(optional_rule, nodes_to_match, grammar)
        except AM_UnmappableError:
          continue

      # `RepeatRule` can match zero nodes
      elif isinstance(rule_in_seq, RepeatRule):
        try:
          span, mapping = _match_first_nodes_greedy(rule_in_seq, nodes_to_match, grammar)
        except AM_UnmappableError:
          continue

      # `Repeat1Rule` must match at least one node
      elif isinstance(rule_in_seq, Repeat1Rule):
        # do not surround with try-except because `Repeat1Rule` must match at least one node
        span, mapping = _treat_rep1_in_seq(rule_in_seq, nodes_to_match, grammar)

      # all other types of rules must match at least one node
      else:
        span, mapping = _match_first_nodes_greedy(rule_in_seq, nodes_to_match, grammar)

      num_nodes_matched += span
      mappings.extend(mapping)

    # there are some nodes that haven't been matched
    assert num_nodes_matched <= len(nodes), 'should not match more nodes than there are'
    if num_nodes_matched != len(nodes):
      raise AM_UnmappableError

    return mappings

  # overrides an abstract method
  def generate_simplest_ast(self, grammar: TreeSitterGrammar) -> tuple:
    '''
    In seq, we generate AST's for each of the members and put them in a list.
    '''
    children_ast = []
    complexities = []

    for member in self.members:

      # NOTE special treatment of `sep1` rules
      # we just need one expansion of the rule in `sep1`
      _is_sep1_res = grammar.is_sep1(member)
      if _is_sep1_res is not None:
        sep1_rule = _is_sep1_res[0]
        member_ast, member_ast_complexity, flatten = sep1_rule.generate_simplest_ast(grammar)

        # no need to add
        if member_ast is None:
          continue

        if isinstance(member_ast, list) and flatten:
          children_ast.extend(member_ast)
        else:
          children_ast.append(member_ast)
        complexities.append(member_ast_complexity)
        continue

      # NOTE special treatment of `optional` rules
      # we can ignore optionals
      is_optional_res = grammar.is_optional(member)
      if is_optional_res is not None:
        continue

      # NOTE member is not `sep1` nor `optional`
      member_ast, member_ast_complexity, flatten = member.generate_simplest_ast(grammar)

      # no need to add
      if member_ast is None:
        continue

      if isinstance(member_ast, list) and flatten:
        children_ast.extend(member_ast)
      else:
        children_ast.append(member_ast)
      complexities.append(member_ast_complexity)

    # no ASTs were generated for members in the sequence
    if len(children_ast) == 0:
      return None, 0, False

    complexity = max(complexities)

    # The result from `seq` rule is always flattened.
    return children_ast, complexity, True

  # overrides an abstract method
  def get_rule_seq_to_symbol_rule(self, sym_rule_name: str, grammar: TreeSitterGrammar) -> List[List[str]]:
    # NOTE sep1, commaSep1 rules are `SeqRule`s in nature
    is_sep1_res = grammar.is_sep1(self)
    if is_sep1_res is not None:
      sep1_rule, separator = is_sep1_res
      sep1_rule_paths : List[List[str]] = sep1_rule.get_rule_seq_to_symbol_rule(sym_rule_name, grammar)
      assert len(sep1_rule_paths) > 0
      paths = [['sep1'] + mp for mp in sep1_rule_paths]
      return paths

    members_paths : List[List[str]] = []
    for member in self.members:
      try:
        member_paths = member.get_rule_seq_to_symbol_rule(sym_rule_name, grammar)
        members_paths.extend(member_paths)
      except RS_UnreachableError:
        pass
    if len(members_paths) == 0:
      raise RS_UnreachableError
    paths = [['seq'] + mp for mp in members_paths]
    return paths


class StringRule(Rule):
  def __init__(self, value: str) -> None:
    super().__init__()
    self.value = value

  def __str__(self) -> str:
    return f'"{self.value}"'

  # overrides an abstract method
  def __eq__(self, value: object) -> bool:
    if not isinstance(value, StringRule):
      return False
    return self.value == value.value

  @classmethod
  def from_dict(cls, rule_dict: dict, parent: Rule) -> StringRule:
    assert 'value' in rule_dict, ERR_SCHEMA
    this_rule = StringRule(rule_dict['value'])
    this_rule.set_parent(parent)
    return this_rule

  # overrides an abstract method
  def get_all_symbols(self) -> List[SymbolRule]:
    return []

  # overrides an abstract method
  def get_ast_mapping(self, nodes: List[p_data_structures.DuoGlotNode], grammar: TreeSitterGrammar) -> List[Tuple]:
    if len(nodes) != 1:
      raise AM_UnmappableError
    node = nodes[0]
    if node.is_nonterminal():
      raise AM_UnmappableError
    if node.node_type == self.value:
      # TODO what do we return?
      return []
    raise AM_UnmappableError

  # overrides an abstract method
  def generate_simplest_ast(self, grammar: TreeSitterGrammar) -> tuple:
    '''
    StringRule always returns terminals.
    '''
    return self.value, 1, False

  # overrides an abstract method
  def get_rule_seq_to_symbol_rule(self, sym_rule_name: str, grammar: TreeSitterGrammar) -> List[List[str]]:
    raise RS_UnreachableError


class SymbolRule(Rule):
  def __init__(self, name: str) -> None:
    super().__init__()
    self.name = name

  def __str__(self) -> str:
    return f'symbol to {self.name}'

  def __repr__(self) -> str:
    return super().__repr__() + f'({self.name})'

  # overrides an abstract method
  def __eq__(self, value: object) -> bool:
    if not isinstance(value, SymbolRule):
      return False
    return self.name == value.name

  @classmethod
  def from_dict(cls, rule_dict: dict, parent: Rule) -> SymbolRule:
    assert 'name' in rule_dict, ERR_SCHEMA
    name = rule_dict['name']
    this_rule = SymbolRule(name)
    this_rule.set_parent(parent)
    return this_rule

  # overrides an abstract method
  def get_all_symbols(self) -> List[SymbolRule]:
    return [self]

  # overrides an abstract method
  def get_ast_mapping(self, nodes: List[p_data_structures.DuoGlotNode], grammar: TreeSitterGrammar) -> List[Tuple]:
    num_nodes = len(nodes)

    # `nodes` does not have any nodes
    if num_nodes == 0:
      raise AM_UnmappableError

    # `nodes` has exactly one node
    elif num_nodes == 1:
      node = nodes[0]
      if node.is_nonterminal():
        if self.name == node.get_ts_node_type():
          return [(node, self, Rule.stack_ast_mapping[:])]
        if grammar.is_external(self.name):
          raise AM_UnmappableError

        # check for cycles
        if self.name in Rule.stack_ast_mapping:
          raise AM_UnmappableError
        Rule.stack_ast_mapping.append(self.name)
        try:
          mapping = grammar.rules[self.name].get_ast_mapping([node], grammar)
          Rule.stack_ast_mapping.pop()
          return mapping
        except AM_UnmappableError:
          Rule.stack_ast_mapping.pop()
          raise
      else:
        raise AM_UnmappableError

    # `nodes` has two or more nodes
    else:
      if grammar.is_external(self.name):
        raise AM_UnmappableError

      # check for cycles
      if self.name in Rule.stack_ast_mapping:
        raise AM_UnmappableError
      Rule.stack_ast_mapping.append(self.name)
      try:
        mapping = grammar.rules[self.name].get_ast_mapping(nodes, grammar)
        Rule.stack_ast_mapping.pop()
        return mapping
      except AM_UnmappableError:
        Rule.stack_ast_mapping.pop()
        raise

  # overrides an abstract method
  def generate_simplest_ast(self, grammar: TreeSitterGrammar) -> tuple:
    '''
    The result from this method is never flattened, as opposed to
    `SeqRule.generate_simplest_ast`.
    '''

    # cannot generate ASTs for external rules
    if grammar.is_external(self.name):
      return None, 0, False

    # NOTE assume that the grammar language is Python
    if self.name in PY_GEN:
      value = PY_GEN[self.name]()
      return [self.name, value], 2, False

    if self.name in Rule.stack_generation:
      raise GA_CycleError

    try:
      Rule.stack_generation.append(self.name)
      symbol_rule = grammar.rules[self.name]
      simplest_ast, complexity, flatten = symbol_rule.generate_simplest_ast(grammar)
      Rule.stack_generation.pop()

      # `self.name` appears as a terminal
      # TODO might be buggy in case `self.name` is actually a non-terminal
      if simplest_ast is None:
        return self.name, 1, False

      # increment complexity since we prepended `self.name`
      ast = [self.name]
      if isinstance(simplest_ast, list) and flatten:
        ast.extend(simplest_ast)
      else:
        ast.append(simplest_ast)
      complexity_increment = 0 if grammar.is_hidden(self.name) else 1
      return ast, complexity + complexity_increment, False

    # don't forget to pop the stack in case of errors during AST generation
    except (GA_CycleError, GA_NoValidChoiceError, GA_NotImplementedError):
      Rule.stack_generation.pop()
      raise

  # overrides an abstract method
  def get_rule_seq_to_symbol_rule(self, sym_rule_name: str, grammar: TreeSitterGrammar) -> List[List[str]]:
    # we can return `self.name` if we want to include it in rule sequence
    if self.name == sym_rule_name:
      return [[]]
    raise RS_UnreachableError


class TokenRule(Rule):
  def __init__(self, content: Rule) -> None:
    super().__init__()
    self.content = content

  def __str__(self) -> str:
    return f'token (\n{p_utils.indent(str(self.content))}\n)'

  def __eq__(self, value: object) -> bool:
    if not isinstance(value, TokenRule):
      return False
    return self.content == value.content

  @classmethod
  def from_dict(cls, rule_dict: dict, parent: Rule) -> TokenRule:
    assert 'content' in rule_dict, ERR_SCHEMA
    content = Rule.from_dict(rule_dict['content'], None)
    this_rule = TokenRule(content)
    this_rule.set_parent(parent)
    content.set_parent(this_rule)
    return this_rule

  # overrides an abstract method
  def get_all_symbols(self) -> List[SymbolRule]:
    return []

  # overrides an abstract method
  def get_ast_mapping(self, nodes: List[p_data_structures.DuoGlotNode], grammar: TreeSitterGrammar) -> List[Tuple]:
    raise AM_UnmappableError

  # overrides an abstract method
  def generate_simplest_ast(self, grammar: TreeSitterGrammar) -> tuple:
    raise GA_NotImplementedError('Cannot generate tokens at the moment.')

  # overrides an abstract method
  def get_rule_seq_to_symbol_rule(self, sym_rule_name: str, grammar: TreeSitterGrammar) -> List[List[str]]:
    raise RS_UnreachableError


# API for program context simplification
def simplify_template(subject: p_subject.PirelSubject, template_dict: dict) -> dict:
  '''
  An alternative to `p_llm_gen.simplify_template` whereby program
  context simplification is performed with the help of grammar
  of the source language.

  For more documentation, refer to `p_grammar.simplify_program_context_usage`.

  NOTE writes to `template_dict`.
  The following keys are updated:
  - `problematic_node_id`
  - `problematic_node_path`
  - `template_origin`
  The following keys are created:
  - `template_origin_before_simplification`

  Simplification strategies:
  1. simplify container nodes that do not have `problematic_node` as a child
  2. simplify container nodes that do have `problematic_node` as a child
  3. simplify remaining nodes individually

  NOTE when we are simplifying the program context,
  `problematic_node_id` and `problematic_node_path` must be preserved.  '''

  # GENERIC FUNCTIONS
  def _get_context_problematic_nodes_context_tree(
    program_text: str,
    lang: str,
    *,
    problematic_node_id: int = None,
    problematic_node_path: List[int] = None,
  ) -> Tuple[p_data_structures.DuoGlotNode, p_data_structures.DuoGlotNode, p_data_structures.PirelTree]:

    ast, ann = d_ast_parse.parse_text_dbg(program_text, lang, keep_text=False)
    tree = p_data_structures.DuoGlotTree(ast)
    root_node = tree.root_node
    assert len(root_node.get_children()) == 1, 'sanity check: root node must have exactly one child'

    context_node = root_node.get_children()[0]

    # problematic node
    assert problematic_node_id is not None or problematic_node_path is not None, 'sanity check'
    if problematic_node_id is not None:
      assert isinstance(problematic_node_id, int), 'sanity check'
      problematic_node = tree.get_node_with_id(problematic_node_id)
    else:
      assert isinstance(problematic_node_path, list), 'sanity check'
      problematic_node = context_node.get_child_by_path(problematic_node_path)

    # context tree (PirelTree) for annotation and node texts
    ast_text, ann_text = d_ast_parse.parse_text_dbg(program_text, lang, keep_text=True)
    tree_text = p_data_structures.PirelTree(ast_text, ann_text)
    tree_text._fix_indentation()

    return context_node, problematic_node, tree_text

  def _gen_code_for_node_type(node_type: str, grammar: p_grammar.TreeSitterGrammar) -> str:
    ast = grammar.generate_simplest_ast(node_type)
    ast_tree = p_visitor_py.Tree.from_gen_ast(ast)
    code = p_visitor_py.PrettyPrinterForGeneratedCode().visit(ast_tree.root_node)
    return code

  def _get_num_nt_nodes(code: str, lang: str) -> int:
    '''RETURN number of non-terminal nodes in AST of `code`'''
    ast, _ = d_ast_parse.parse_text_dbg(code, lang, keep_text=False)
    tree = p_data_structures.DuoGlotTree(ast)
    return tree.get_num_nt_nodes()

  # STRATEGY 1
  def _all_siblings_can_be_simplified_prob_no(
    nodes_can_be_simplified_dict: Dict[int, Dict[int, bool]],
    problematic_node_id: int,
    strat1_num_children_nodes_threshold: int = 5
  ) -> Optional[int]:
    '''
    Return the smallest `node_id` (either parent or previous sibling)
    for which all siblings can be simplified and problematic node is not one of the siblings
    '''
    for nid in sorted(nodes_can_be_simplified_dict):
      can_be_simplified_values = nodes_can_be_simplified_dict[nid]
      if len(can_be_simplified_values) <= strat1_num_children_nodes_threshold:
        return None
      if all(can_be_simplified_values.values()) and problematic_node_id not in can_be_simplified_values:
        return nid
    return None

  def _process_all_siblings_can_be_simplified_node_prob_no(
    siblings_can_be_removed_node_id: int,
    nodes_can_be_simplified_dict: Dict[int, Dict[int, bool]],
    pot_simplifiable_nodes: Dict[int, p_data_structures.DuoGlotNode]
  ) -> p_data_structures.DuoGlotNode:
    '''
    NOTE modifies `nodes_can_be_simplified_dict`
    Return a reference to a node whose all non-terminal children
    can be simplified. In other words, return a reference to a
    parent node of a node whose all siblings can be simplified.
    '''
    # get the parent node of siblings that can all be simplified
    parent_node = pot_simplifiable_nodes[siblings_can_be_removed_node_id].get_parent()

    # remove `siblings_can_be_removed_node_id` and its descendants
    siblings_can_be_simplified_nids = list(nodes_can_be_simplified_dict[siblings_can_be_removed_node_id].keys())
    for sibling_can_be_simplified_nid in sorted(siblings_can_be_simplified_nids):
      sibling_can_be_simplified = pot_simplifiable_nodes[sibling_can_be_simplified_nid]
      # remove the descendants in reverse order (why?)
      descendants = sibling_can_be_simplified.get_nonterminal_descendants()
      descendants.sort(key=lambda node: node.get_id(), reverse=True)
      for descendant in descendants:
        if descendant.get_id() in nodes_can_be_simplified_dict:
          nodes_can_be_simplified_dict.pop(descendant.get_id())
      # remove the node itself
      nodes_can_be_simplified_dict.pop(sibling_can_be_simplified_nid)

    return parent_node

  def _strategy_1(
    problematic_node: p_data_structures.DuoGlotNode,
    context_tree: p_data_structures.PirelTree,
    orig_text: str,
    nodes_can_be_simplified_dict: Dict[int, Dict[int, bool]],
    pot_simplifiable_nodes: Dict[int, p_data_structures.DuoGlotNode],
    grammar: p_grammar.TreeSitterGrammar,
    strat1_num_children_nodes_threshold: int = 5
  ) -> Tuple[str, int]:
    '''
    Go over nodes for which all siblings can be simplified and
    problematic node IS NOT one of the siblings
    in this case, we replace all simplifiable nodes with the simplest generated code
    For example, `nums = [1, 2, 3, 4, 5]` is simplified into `nums = []`

    PARAM strat1_num_children_nodes_threshold - if a parent node has less than or equal
    to `strat1_num_children_nodes_threshold` children nodes, then do not simplify it.

    RETURN
    1. simplified code with this strategy
    2. updated problematic node id (in case of simplifying nodes before prob. node)

    NOTE modifies `nodes_can_be_simplified_dict`
    '''

    logger.debug('Starting context simplification using strategy 1')

    # ~~~ collect container nodes children of which are removed
    all_children_can_be_removed_nodes_list : List[p_data_structures.DuoGlotNode] = []
    while True:
      siblings_can_be_removed_node_id = _all_siblings_can_be_simplified_prob_no(
        nodes_can_be_simplified_dict,
        problematic_node.get_id(),
        strat1_num_children_nodes_threshold=strat1_num_children_nodes_threshold
      )
      if siblings_can_be_removed_node_id is None:
        break
      parent_node_of_simpl_nodes = _process_all_siblings_can_be_simplified_node_prob_no(
        siblings_can_be_removed_node_id,
        nodes_can_be_simplified_dict,
        pot_simplifiable_nodes
      )
      all_children_can_be_removed_nodes_list.append(parent_node_of_simpl_nodes)

    # ~~~ do the actual simplification
    # sort in reverse so we do not mess up the annotation marks
    all_children_can_be_removed_nodes_list.sort(key=lambda node: node.get_id(), reverse=True)
    upd_prob_nid = problematic_node.get_id()

    for parent_node in all_children_can_be_removed_nodes_list:
      logger.debug(f'Simplifying context node using strategy 1: {parent_node}')

      replacement_code = _gen_code_for_node_type(parent_node.get_ts_node_type(), grammar)
      start_point = context_tree.annotation[parent_node.get_id()][0]
      end_point = context_tree.annotation[parent_node.get_id()][1]
      simplified_code = orig_text[:start_point] + replacement_code + orig_text[end_point:]

      # need to adjust the `problematic_node_id`
      if parent_node.get_id() < problematic_node.get_id():
        num_nt_nodes_before = _get_num_nt_nodes(orig_text, template_dict['src_lang'])
        num_nt_nodes_after = _get_num_nt_nodes(simplified_code, template_dict['src_lang'])
        upd_prob_nid -= (num_nt_nodes_before - num_nt_nodes_after)

      orig_text = simplified_code

    return orig_text, upd_prob_nid

  # STRATEGY 2
  def _all_siblings_can_be_simplified_prob_yes(
    nodes_can_be_simplified_dict: Dict[int, Dict[int, bool]],
    problematic_node_id: int
  ) -> Optional[int]:
    '''
    Return the smallest `node_id` (either parent or previous sibling)
    for which all siblings can be simplified and problematic node is one of the siblings
    NOTE this function should return a value no more than once

    TODO `problematic_node_id` itself cannot be simplified
    (according to `_get_simplification_metadata`), so this function always returns None.
    '''
    for nid in sorted(nodes_can_be_simplified_dict):
      can_be_simplified_values = nodes_can_be_simplified_dict[nid]
      if all(can_be_simplified_values.values()) and problematic_node_id in can_be_simplified_values:
        return nid
    return None

  def _process_all_siblings_can_be_simplified_node_prob_yes(
    siblings_can_be_removed_node_id: int,
    nodes_can_be_simplified_dict: Dict[int, Dict[int, bool]],
    pot_simplifiable_nodes: Dict[int, p_data_structures.DuoGlotNode]
  ) -> Tuple[p_data_structures.DuoGlotNode, p_data_structures.DuoGlotNode]:
    '''
    NOTE modifies `nodes_can_be_simplified_dict`

    `siblings_can_be_removed_node_id` is a `node_id` of the problematic node
    whose all siblings can be removed.

    What do we do?
    1. get the leftmost non-terminal sibling (L)
    2. get the rightmost non-terminal sibling (R)
    3. remove everything between (L) and (R) but keep the problematic node itself

    How do we remove?
    By getting the start point of the leftmost node, and end point
    of the rightmost node, and replacing everything with problematic node's text.

    What do we return?
    Reference to the leftmost, and the rightmost non-terminal nodes.
    '''
    # get the leftmost and rightmost siblings of problematic node
    node_can_be_simplified_dict = nodes_can_be_simplified_dict[siblings_can_be_removed_node_id]
    assert all(node_can_be_simplified_dict.values()), 'sanity check'
    node_ids = node_can_be_simplified_dict.keys()
    leftmost_node = pot_simplifiable_nodes[min(node_ids)]
    rightmost_node = pot_simplifiable_nodes[max(node_ids)]

    siblings_can_be_simplified_nids = list(nodes_can_be_simplified_dict[siblings_can_be_removed_node_id].keys())
    for sibling_can_be_simplified_nid in sorted(siblings_can_be_simplified_nids):
      sibling_can_be_simplified = pot_simplifiable_nodes[sibling_can_be_simplified_nid]
      # remove the descendants in reverse order (why?)
      descendants = sibling_can_be_simplified.get_nonterminal_descendants()
      descendants.sort(key=lambda node: node.get_id(), reverse=True)
      for descendant in descendants:
        if descendant.get_id() in nodes_can_be_simplified_dict:
          nodes_can_be_simplified_dict.pop(descendant.get_id())
      # remove the node itself
      nodes_can_be_simplified_dict.pop(sibling_can_be_simplified_nid)

    return leftmost_node, rightmost_node

  def _strategy_2(
    problematic_node: p_data_structures.DuoGlotNode,
    context_tree: p_data_structures.PirelTree,
    orig_text: str,
    nodes_can_be_simplified_dict: Dict[int, Dict[int, bool]],
    pot_simplifiable_nodes: Dict[int, p_data_structures.DuoGlotNode],
  ) -> Tuple[str, int]:
    '''
    Go over nodes for which all siblings can be simplified and
    problematic node is one of the siblings
    in this case, we remove all simplifiable nodes except the problematic node
    there should be no more than one such node

    RETURN
    1. simplified code with this strategy
    2. updated problematic node id

    NOTE modifies `nodes_can_be_simplified_dict`
    '''

    logger.debug('Starting context simplification using strategy 2')

    # ~~~ collect container nodes children of which contain `problematic_node`
    leftmost_node, rightmost_node = None, None
    siblings_can_be_removed_node_id = _all_siblings_can_be_simplified_prob_yes(
      nodes_can_be_simplified_dict,
      problematic_node.get_id()
    )
    if siblings_can_be_removed_node_id is not None:
      leftmost_node, rightmost_node = _process_all_siblings_can_be_simplified_node_prob_yes(
        siblings_can_be_removed_node_id,
        nodes_can_be_simplified_dict,
        pot_simplifiable_nodes
      )

    # simplification is not applicable
    else:
      return orig_text, problematic_node.get_id()

    # ~~~ do the actual simplification
    # TODO HACK do not simplify if problematic_node is a child of argument_list
    if problematic_node.get_parent().get_ts_node_type() == 'argument_list':
      logger.debug(f'Not simplifying context node using strategy 2 (hack) for parent of: {problematic_node}')
      return orig_text, problematic_node.get_id()

    logger.debug(f'Simplifying context using strategy 2 for parent of: {problematic_node}')
    start_point = context_tree.annotation[leftmost_node.get_id()][0]
    end_point = context_tree.annotation[rightmost_node.get_id()][1]
    replacement_code = context_tree.get_node_with_id(problematic_node.get_id()).get_text()
    orig_text = orig_text[:start_point] + replacement_code + orig_text[end_point:]

    upd_prob_nid = leftmost_node.get_id()
    return orig_text, upd_prob_nid

  # STRATEGY 3
  def _get_individually_simplifiable_nodes(
    problematic_node_id: int,
    nodes_can_be_simplified_dict: Dict[int, Dict[int, bool]],
    pot_simplifiable_nodes: Dict[int, p_data_structures.DuoGlotNode]
  ) -> List[p_data_structures.DuoGlotNode]:
    '''
    Remove all nodes that could be processed by strategy 1 and 2, and
    return the remaining nodes.

    NOTE writes to `nodes_can_be_simplified_dict`
    '''
    # ~~~ collect container nodes children of which are removed
    while True:
      siblings_can_be_removed_node_id = _all_siblings_can_be_simplified_prob_no(
        nodes_can_be_simplified_dict,
        problematic_node_id
      )
      if siblings_can_be_removed_node_id is None:
        break
      parent_node_of_simpl_nodes = _process_all_siblings_can_be_simplified_node_prob_no(
        siblings_can_be_removed_node_id,
        nodes_can_be_simplified_dict,
        pot_simplifiable_nodes
      )
      nodes_can_be_simplified_dict.pop(parent_node_of_simpl_nodes.get_id(), None)

    # ~~~ collect container nodes children of which contain `problematic_node`
    leftmost_node, rightmost_node = None, None
    siblings_can_be_removed_node_id = _all_siblings_can_be_simplified_prob_yes(
      nodes_can_be_simplified_dict,
      problematic_node_id
    )
    if siblings_can_be_removed_node_id is not None:
      leftmost_node, rightmost_node = _process_all_siblings_can_be_simplified_node_prob_yes(
        siblings_can_be_removed_node_id,
        nodes_can_be_simplified_dict,
        pot_simplifiable_nodes
      )
      nodes_can_be_simplified_dict.pop(leftmost_node.get_id(), None)
      nodes_can_be_simplified_dict.pop(rightmost_node.get_id(), None)

    # ~~~ remaining nodes are what we need
    individually_simplifiable_nodes = [pot_simplifiable_nodes[nid] for nid in nodes_can_be_simplified_dict.keys()]
    return individually_simplifiable_nodes

  def _strategy_3(
    problematic_node: p_data_structures.DuoGlotNode,
    context_tree: p_data_structures.PirelTree,
    orig_text: str,
    individually_simplifiable_nodes: List[p_data_structures.DuoGlotNode],
    template_dict: dict,
    grammar: p_grammar.TreeSitterGrammar,
    is_simplify_nodes_before_prob_node: bool = False,
    is_simplify_nodes_after_prob_node: bool = False
  ) -> Tuple[str, int]:
    '''
    Process nodes in reverse pre-order fashion to not mess up annotation marks,
    since we rely on string replacement. Obviously, not the best solution.
    Instead, we can try using top-down approach, which will make it more efficient.
    TODO left this as a later work.

    RETURN
    1. simplified code with this strategy
    2. updated problematic node id (in case of simplifying nodes before prob. node)

    PARAM is_simplify_nodes_before_prob_node - controls whether or not nodes
    that appear before the problematic node are simplified. Why is it important to
    set this flag to `False`? Because, if we simplify nodes before the problematic
    node and after that use the simplified code to generate a partial program,
    then we may not be able to use previously learned translation rules, and end up
    generating an invalid partial program.

    PARAM is_simplify_nodes_after_prob_node - controls whether or not nodes
    that appear after the problematic node are simplified. Why is it important to
    set this flag to `False`? The reason is the same as for
    `is_simplify_nodes_before_prob_node`.
    '''

    logger.debug('Starting context simplification using strategy 3')

    def __simplify_node(
      orig_text: str,
      node: p_data_structures.DuoGlotNode,
      context_tree: p_data_structures.PirelTree,
      individually_simplifiable_nodes: List[p_data_structures.DuoGlotNode],
      template_dict: dict,
      grammar: p_grammar.TreeSitterGrammar
    ) -> Optional[Tuple[str, dict]]:
      '''
      RETURN None if
      1. simplification produces SyntaxError
      2. generated simplified code is not simpler than the existing code

      NOTE writes to `context_tree.annotation`
      TODO this function uses bottom-up apprach, optimize it to use top-down approach
      '''
      # generate simplified code candidate
      simplified_node_code = _gen_code_for_node_type(node.get_ts_node_type(), grammar)
      start_point = context_tree.annotation[node.get_id()][0]
      end_point = context_tree.annotation[node.get_id()][1]
      simplified_code = orig_text[:start_point] + simplified_node_code + orig_text[end_point:]

      # check for parse errors
      has_parse_error = p_utils.does_have_parse_error(simplified_code, template_dict['src_lang'])
      if has_parse_error:
        return None

      # check if the generated code is simpler than the existing code
      num_nt_nodes_before = _get_num_nt_nodes(orig_text, template_dict['src_lang'])
      num_nt_nodes_after = _get_num_nt_nodes(simplified_code, template_dict['src_lang'])
      if num_nt_nodes_before <= num_nt_nodes_after:
        return None

      # NOTE annotations of ancestor nodes of `node` should be updated
      # to reflect the changes in the code
      annotation_copy = copy.deepcopy(context_tree.annotation)
      for pot_ancestor in individually_simplifiable_nodes:
        if pot_ancestor.get_id() == node.get_id():
          continue
        if pot_ancestor.is_ancestor(node):
          anc_end_point = annotation_copy[pot_ancestor.get_id()][1]
          node_text_size_before = end_point - start_point
          node_text_size_after = len(simplified_node_code)
          node_text_size_diff = node_text_size_before - node_text_size_after
          anc_new_end_point = anc_end_point - node_text_size_diff
          annotation_copy[pot_ancestor.get_id()][1] = anc_new_end_point

      return simplified_code, annotation_copy

    # sort in reverse so we do not mess up the annotation marks
    individually_simplifiable_nodes.sort(key=lambda node: node.get_id(), reverse=True)
    upd_prob_nid = problematic_node.get_id()

    for node in individually_simplifiable_nodes:
      node_simpl_res = __simplify_node(orig_text, node, context_tree, individually_simplifiable_nodes, template_dict, grammar)

      # skip `node` which we can't simplify
      if node_simpl_res is None:
        logger.debug(f'Context simplification using strategy 3 not possible for (syntax error): {node}')
        continue

      simplified_code, annotation_copy = node_simpl_res

      # `node` appears before the `problematic_node`
      # need to adjust the `problematic_node_id`
      if node.get_id() < problematic_node.get_id():
        if not is_simplify_nodes_before_prob_node:
          logger.debug(f'Context simplification using strategy 3 not possible for (appears before prob.node): {node}')
          continue

        # the difference in the number of non-terminal nodes tells us
        # how much node id of the problematic node has shifted
        num_nt_nodes_before = _get_num_nt_nodes(orig_text, template_dict['src_lang'])
        num_nt_nodes_after = _get_num_nt_nodes(simplified_code, template_dict['src_lang'])
        upd_prob_nid -= (num_nt_nodes_before - num_nt_nodes_after)

      # `node` appears after the `problematic_node`
      if node.get_id() > problematic_node.get_id():
        if not is_simplify_nodes_after_prob_node:
          if node.get_ts_node_type() not in p_consts.BODY_NODE_TYPES[template_dict['src_lang']]:
            logger.debug(f'Context simplification using strategy 3 not possible for (appears after prob.node): {node}')
            continue

      orig_text = simplified_code
      context_tree.annotation = annotation_copy

    return orig_text, upd_prob_nid

  logger.debug('~~~ Starting p_grammar.simplify_template')

  template_origin = template_dict['template_origin']
  src_lang = template_dict['src_lang']
  problematic_node_path = template_dict['problematic_node_path']

  grobj = p_consts.GRAMMAR_DICT_READONLY[src_lang]
  grammar = TreeSitterGrammar.from_dict(grobj)

  # ~~~ prepare artifacts for strategy 1
  ctx_node_strat1, prob_node_strat1, ctx_tree_strat1 = _get_context_problematic_nodes_context_tree(
    template_origin, src_lang, problematic_node_path=problematic_node_path
  )

  pot_simplifiable_nodes_strat1, nodes_can_be_simplified_dict_strat1 = _get_simplification_metadata(
    ctx_node_strat1,
    prob_node_strat1,
    template_dict,
    grammar
  )
  p_utils.log_json_time(f'{subject.name}_nodes_can_be_simplified_dict_strat1.json', nodes_can_be_simplified_dict_strat1)

  # ~~~ simplify using strategy 1
  upd_text_strat1, upd_prob_nid_strat1 = _strategy_1(
    prob_node_strat1,
    ctx_tree_strat1,
    template_origin,
    nodes_can_be_simplified_dict_strat1,
    pot_simplifiable_nodes_strat1,
    grammar,
    strat1_num_children_nodes_threshold=5
  )
  logger.debug(f'before simplification using strategy 1:\n{template_origin}')
  logger.debug(f'after simplification using strategy 1:\n{upd_text_strat1}')

  # ~~~ prepare artifacts for strategy 2
  ctx_node_strat2, prob_node_strat2, ctx_tree_strat2 = _get_context_problematic_nodes_context_tree(
    upd_text_strat1, src_lang, problematic_node_id=upd_prob_nid_strat1
  )
  assert prob_node_strat1.get_type() == prob_node_strat2.get_type(), 'sanity check'

  pot_simplifiable_nodes_strat2, nodes_can_be_simplified_dict_strat2 = _get_simplification_metadata(
    ctx_node_strat2,
    prob_node_strat2,
    template_dict,
    grammar
  )
  p_utils.log_json_time(f'{subject.name}_nodes_can_be_simplified_dict_strat2.json', nodes_can_be_simplified_dict_strat2)

  # ~~~ simplify using strategy 2
  upd_text_strat2, upd_prob_nid_strat2 = _strategy_2(
    prob_node_strat2,
    ctx_tree_strat2,
    upd_text_strat1,
    nodes_can_be_simplified_dict_strat2,
    pot_simplifiable_nodes_strat2
  )
  logger.debug(f'before simplification using strategy 2:\n{upd_text_strat1}')
  logger.debug(f'after simplification using strategy 2:\n{upd_text_strat2}')

  # ~~~ prepare artifacts for strategy 3
  ctx_node_strat3, prob_node_strat3, ctx_tree_strat3 = _get_context_problematic_nodes_context_tree(
    upd_text_strat2, src_lang, problematic_node_id=upd_prob_nid_strat2
  )
  assert prob_node_strat2.get_type() == prob_node_strat3.get_type(), 'sanity check'

  pot_simplifiable_nodes_strat3, nodes_can_be_simplified_dict_strat3 = _get_simplification_metadata(
    ctx_node_strat3,
    prob_node_strat3,
    template_dict,
    grammar
  )
  p_utils.log_json_time(f'{subject.name}_nodes_can_be_simplified_dict_strat3.json', nodes_can_be_simplified_dict_strat3)

  # ~~~ simplify using strategy 3
  individually_simplifiable_nodes = _get_individually_simplifiable_nodes(
    prob_node_strat3.get_id(),
    nodes_can_be_simplified_dict_strat3,
    pot_simplifiable_nodes_strat3
  )
  upd_text_strat3, upd_prob_nid_strat3 = _strategy_3(
    prob_node_strat3,
    ctx_tree_strat3,
    upd_text_strat2,
    individually_simplifiable_nodes,
    template_dict,
    grammar,
    is_simplify_nodes_before_prob_node=False,
    is_simplify_nodes_after_prob_node=False
  )
  logger.debug(f'before simplification using strategy 3:\n{upd_text_strat2}')
  logger.debug(f'after simplification using strategy 3:\n{upd_text_strat3}')

  # ~~~ prepare artifacts for strategy 4 (if any)
  ctx_node_strat4, prob_node_strat4, ctx_tree_strat4 = _get_context_problematic_nodes_context_tree(
    upd_text_strat3, src_lang, problematic_node_id=upd_prob_nid_strat3
  )
  assert prob_node_strat3.get_type() == prob_node_strat4.get_type(), 'sanity check'

  template_dict['template_origin_before_simplification'] = template_dict['template_origin']
  template_dict['template_origin'] = upd_text_strat3
  template_dict['problematic_node_id'] = upd_prob_nid_strat3
  template_dict['problematic_node_path'] = ctx_node_strat4.get_path_to_child(prob_node_strat4)

  return template_dict

def _get_potential_simplifiable_nodes(
  context_node: p_data_structures.DuoGlotNode,
  problematic_node: p_data_structures.DuoGlotNode,
  template_dict: dict
) -> Dict[int, p_data_structures.DuoGlotNode]:
  '''
  RETURN a sequence of nodes that can "potentially" be simplified/removed
  from the program. It is emphasized that not all the nodes in the
  resulting sequence can be actually simplified, hence "potentially".
  '''

  def __is_potential_simplifiable_node(
    node: p_data_structures.DuoGlotNode,
    problematic_node: p_data_structures.DuoGlotNode,
    template_dict: dict
  ) -> bool:
    if node.is_terminal():
      return False
    # ancestors of problematic node cannot be simplified
    if node.is_ancestor(problematic_node):
      return False
    # cannot simplify `problematic_node` itself
    if node == problematic_node:
      return False
    # NOTE e.g. `d = {'a': 1, 'b': 2, 'c': 3}` -> `problematic_node` of `expression_statement`
    # that is assignment with `dictionary` on the right hand side.
    # In this case, we would want to simplify `dictionary`.
    if problematic_node.is_ancestor(node):
      # TODO what is the difference between `block`, `list`, `dict`
      # from the perspective of "body" or "blocky" or "container" node types?
      # if node.get_ts_node_type() in p_consts.BODY_NODE_TYPES[template_dict['src_lang']]:
      if node.get_ts_node_type() in ['block']:
        return True
      return False
    return True

  def __rec_pre_order_collect_potential_simplifiable_nodes(
    at_node: p_data_structures.DuoGlotNode,
    context_node: p_data_structures.DuoGlotNode,
    problematic_node: p_data_structures.DuoGlotNode,
    template_dict: dict,
    container: dict
  ):
    '''
    Writes to `container`
    '''
    if __is_potential_simplifiable_node(at_node, problematic_node, template_dict):
      container[at_node.get_id()] = at_node
    for child in at_node.get_children():
      __rec_pre_order_collect_potential_simplifiable_nodes(child, context_node, problematic_node, template_dict, container)

  simplifiable_nodes = {}
  __rec_pre_order_collect_potential_simplifiable_nodes(
    context_node,
    context_node,
    problematic_node,
    template_dict,
    simplifiable_nodes
  )
  return simplifiable_nodes

def _process_potential_simplifiable_node_w_grammar(
  pot_simplifiable_node: p_data_structures.DuoGlotNode,
  grammar: TreeSitterGrammar
) -> Optional[Dict[int, bool]]:
  '''
  Return a dict that contains whether the following nodes can be simplified:
  1. potential simplifiable node
  2. potential simplifiable node's non-terminal siblings (as defined in mapper algorithm)
  '''

  def __child_node_can_be_simplified(
    parent_node: p_data_structures.DuoGlotNode,
    child_node: p_data_structures.DuoGlotNode,
    production_path: List[str],  # ['_right_hand_side', 'expression', 'primary_expression']
    grammar: TreeSitterGrammar
  ) -> bool:
    '''
    Can we remove `child_node` from `parent_node` without breaking the grammar?
    We can remove optionals and repeats.
    '''

    def ___rule_path_allows_node_removal(
      rule_path: List[str]
    ) -> bool:
      '''
      Tells us whether this rule path allows node removal
      '''
      if 'optional' in rule_path or 'repeat' in rule_path:
        return True
      return False

    def ___production_pair_allows_node_removal(
      production_pair: Tuple[str, str],  # ('_right_hand_side', 'expression')
      grammar: TreeSitterGrammar
    ) -> bool:
      parent, child = production_pair
      assert not grammar.is_external(parent), 'sanity check'
      par_rule = grammar.rules[parent]
      rule_paths = par_rule.get_rule_seq_to_symbol_rule(child, grammar)
      if all(map(___rule_path_allows_node_removal, rule_paths)):
        return True
      return False

    par_ntype = parent_node.get_ts_node_type()
    ch_ntype = child_node.get_ts_node_type()

    production_path.insert(0, par_ntype)
    production_path.append(ch_ntype)

    production_pairs = list(zip(production_path[:-1], production_path[1:]))
    if any(map(lambda pp: ___production_pair_allows_node_removal(pp, grammar), production_pairs)):
      return True
    return False

  par_simpl_node = pot_simplifiable_node.parent
  par_simpl_ntype = par_simpl_node.get_ts_node_type()

  assert par_simpl_node.is_nonterminal(), 'sanity check: non-terminal node expected'
  assert not grammar.is_external(par_simpl_ntype), 'sanity check'
  par_rule = grammar.rules[par_simpl_ntype]

  # ~~~ obtain mappings of
  # potential simplifiable node's siblings (including itself) and grammar
  siblings_simpl_node = par_simpl_node.get_children()
  # grammar matcher cannot handle comments at the moment
  siblings_simpl_node = [n for n in siblings_simpl_node if n.node_type != 'py.comment']
  nt_siblings_simpl_node = [n for n in siblings_simpl_node if n.is_nonterminal()]
  assert len(nt_siblings_simpl_node) > 0, 'sanity check'
  try:
    mappings = par_rule.get_ast_mapping(siblings_simpl_node, grammar)
  except AM_UnmappableError:
    return None

  # ~~~ process mappings
  # can potential simplifiable node be simplified?
  # can all non-terminal siblings of potential simplifiable node be simplified?
  can_be_simplified_dict : Dict[int, bool] = {}
  for mapping in mappings:
    sibling_simpl_node, mapped_rule, production_path = mapping
    can_be_simplified = __child_node_can_be_simplified(par_simpl_node, sibling_simpl_node, production_path, grammar)
    can_be_simplified_dict[sibling_simpl_node.get_id()] = can_be_simplified

  assert pot_simplifiable_node.get_id() in can_be_simplified_dict, 'sanity check: simplifiable node must be present'
  return can_be_simplified_dict

def _get_simplification_metadata(
  context_node: p_data_structures.DuoGlotNode,
  problematic_node: p_data_structures.DuoGlotNode,
  template_dict: dict,
  grammar: TreeSitterGrammar
) -> Tuple[Dict[int, p_data_structures.DuoGlotNode], Dict[int, Dict[int, bool]]]:
  '''
  RETURN
  1. potential simplifiable nodes
  2. a sequence of nodes that can actually be simplified
  '''

  def _update_can_be_simplified_dict(
    can_be_simplified_dict: Dict[int, bool],
    pot_simplifiable_nodes: Dict[int, p_data_structures.DuoGlotNode]
  ) -> Dict[int, bool]:
    '''
    WHY DO WE NEED THIS FUNCTION?
    Since `_process_potential_simplifiable_node` tells whether a node can be simplified
    from the grammar perspective only, it does not necessarily mean that the node can
    actually be simplified. For example, this applies for a case when we have a
    `li = [(1, 'a'), (2, 'b'), (3, 'c')]` with `'a'` being the problematic node.
    We can clearly say that `(1, 'a')` cannot be simplified, when grammar says that it can be.

    NOTE writes to can_be_simplified_dict
    '''
    for nid, cbs in can_be_simplified_dict.items():
      # reset the flag if node cannot be potentially simplified
      if nid not in pot_simplifiable_nodes:
        can_be_simplified_dict[nid] = False
    return can_be_simplified_dict

  # ~~~ artifact 1
  pot_simplifiable_nodes = _get_potential_simplifiable_nodes(context_node, problematic_node, template_dict)

  # ~~~ artifact 2
  nodes_can_be_simplified_dict : Dict[int, Dict[int, bool]] = {}
  for snid, pot_simpl_node in pot_simplifiable_nodes.items():
    _can_be_simplified_dict = _process_potential_simplifiable_node_w_grammar(pot_simpl_node, grammar)
    if _can_be_simplified_dict is not None:
      _can_be_simplified_dict = _update_can_be_simplified_dict(_can_be_simplified_dict, pot_simplifiable_nodes)
      nodes_can_be_simplified_dict[pot_simpl_node.get_id()] = _can_be_simplified_dict

  return pot_simplifiable_nodes, nodes_can_be_simplified_dict


# API for TSP generation
def get_alternative_starting_node_types(
  problematic_node: p_data_structures.DuoGlotNode,
  grammar: TreeSitterGrammar,
) -> List[Tuple[p_data_structures.DuoGlotNode, List[str]]]:
  '''
  NOTE There might be cases when there is no alternative to N. In such cases,
  we might have to find alternatives to children of N. TODO Let's consider it later.

  RETURN a list of tuples, where each tuple contains a `mapped_node` and
         all its possible alternative node types including `mapped_node.get_ts_node_type()`

  TODO update docs
  '''

  problematic_node_type = problematic_node.get_ts_node_type()

  assert problematic_node.is_nonterminal(), 'non-terminal node expected'
  assert not grammar.is_external(problematic_node_type), f'{problematic_node_type} is an external rule and is not supported'

  rule = grammar.rules[problematic_node_type]

  children = problematic_node.get_children()
  # grammar matcher cannot handle comments at the moment
  children = [n for n in children if n.node_type != 'py.comment']
  assert len(children) > 0, '`problematic_node` should have at least one non-terminal child'

  # match children nodes with (symbol|alias) rules that parsed them
  # TODO raises AM_UnmappableError
  # TODO do we need to reset `Rule.stack_ast_mapping`?
  mappings = rule.get_ast_mapping(children, grammar)

  nt_children = [n for n in children if n.is_nonterminal()]
  assert len(mappings) == len(nt_children), 'each non-terminal child should be mapped to a symbol'

  all_alt_node_types : List[Tuple[p_data_structures.DuoGlotNode, List[str]]] = []
  for mapped_node, mapped_rule, path_to_rule in mappings:
    try:
      alt_node_types = get_alternative_starting_node_type(problematic_node, mapped_node, mapped_rule, path_to_rule, grammar)
      all_alt_node_types.append((mapped_node, alt_node_types))
    except API_NoAlternativeError:
      all_alt_node_types.append((mapped_node, [mapped_node.get_ts_node_type()]))

  return all_alt_node_types


def get_alternative_starting_node_type(
  problematic_node: p_data_structures.DuoGlotNode,
  child_node: p_data_structures.DuoGlotNode,
  mapped_rule: Rule,
  path_to_rule: List[str],
  grammar: TreeSitterGrammar,
) -> List[str]:
  '''
  A mapping has a connection between problematic node's child node
  and a symbol rule associated with it. The goal of this function
  is to find alternative symbol rules that can be associated with
  the child of the problematic node. At one of these symbol rules
  we will start generation of a random AST (program) to later use
  it as a substitute to the child node. To achieve this, we need to
  check the parents of `mapped_rule`.

  RETURN A list of all possible alternatives including type of child node.
  RAISE API_NoAlternativeError, RuntimeError

  NOTE This is a recursive function.
  '''

  def _get_choices_of_supertype(rule_name: str, grammar: TreeSitterGrammar, cycle_detection_list: list = []) -> List[str]:
    ''''''
    assert grammar.is_supertype(rule_name), f'"{rule_name}" is not a supertype'

    # avoid cycles
    if rule_name in cycle_detection_list:
      return []
    cycle_detection_list.append(rule_name)

    rule = grammar.rules[rule_name]
    assert isinstance(rule, ChoiceRule), f'"{rule_name}" is not a ChoiceRule'
    assert all(map(lambda m: isinstance(m, SymbolRule), rule.members)), f'Every member of "{rule_name}" must be a SymbolRule'
    members_str = list(map(lambda m: m.name, rule.members))

    # a rule in `members_str` can be a supertype
    # e.g. `primary_expression` under `expression`
    # recursively replace each member with its choices if it's a supertype
    checked_members_str = []
    for member_str in members_str:
      if grammar.is_supertype(member_str):
        member_supertype_choices = _get_choices_of_supertype(member_str, grammar, cycle_detection_list)
        checked_members_str.extend(member_supertype_choices)
      else:
        checked_members_str.append(member_str)

    return checked_members_str

  assert isinstance(mapped_rule, (SymbolRule, AliasRule, FieldRule, RepeatRule)), \
    'mapped rule must be one of SymbolRule, AliasRule, FieldRule, RepeatRule'

  is_sep1_res = grammar.is_sep1(mapped_rule.parent)
  is_optional_res = grammar.is_optional(mapped_rule.parent)
  prob_node_type = problematic_node.get_ts_node_type()
  ch_node_type = child_node.get_ts_node_type()

  # 1 `mapped_rule` itself is an AliasRule
  if isinstance(mapped_rule, AliasRule):
    # don't really know what to do in this case
    raise API_NoAlternativeError

  # 2 OPTIONAL: parent is optional. Optional is a ChoiceRule,
  # but not all ChoiceRules are optional, thus this case appears before the next.
  if is_optional_res is not None:
    # expect optionals to be directly under the production rule for the problematic node
    assert len(path_to_rule) == 0, f'"{mapped_rule}" is expected to be directly inside production rule for {prob_node_type}'
    # we can't do anything at this point, there are no alternatives
    raise API_NoAlternativeError

  # 3 CHOICE: parent is a ChoiceRule.
  # The simplest case is when a `rule` is an option of a ChoiceRule.
  # In this case, we select one of the alternatives to `rule`.
  # The alternative choice should not be external, SymbolRule(node_type)
  elif isinstance(mapped_rule.parent, ChoiceRule):
    alternatives : List[str] = []
    for alt in mapped_rule.parent.members:
      # alternative rule can only be a SymbolRule
      # TODO can it be something that contains a SymbolRule?
      if not isinstance(alt, SymbolRule):
        continue
      # alternative cannot be an external rule (we cannot generate such nodes)
      if grammar.is_external(alt.name):
        continue
      # NOTE leaving if statement below for reference
      # alternative must be different than the ch_node_type
      # if alt.name == ch_node_type:
      #   continue
      # NOTE if `alt` is a supertype rule (e.g. `primary_expression`) then we should expand it to its choices
      # https://tree-sitter.github.io/tree-sitter/using-parsers#static-node-types
      if grammar.is_supertype(alt.name):
        supertype_choices = _get_choices_of_supertype(alt.name, grammar)
        alternatives.extend(supertype_choices)
      else:
        alternatives.append(alt.name)

    if len(alternatives) == 0:
      raise API_NoAlternativeError

    # choose a node that reaches a terminal the fastest
    alternatives = _rank_node_types(alternatives, grammar)
    return alternatives

  # 4 SEP1: parent is sep1 rule. Cannot have any other options.
  elif bool(is_sep1_res):
    # expect sep1 to be directly under the production rule for the problematic node
    assert len(path_to_rule) == 0, f'"{mapped_rule}" is expected to be directly inside production rule for "{prob_node_type}"'
    # we can't do anything at this point, there are no alternatives
    raise API_NoAlternativeError

  # 5 FIELD: parent is a FieldRule, check grandparent.
  elif isinstance(mapped_rule.parent, FieldRule):
    return get_alternative_starting_node_type(problematic_node, child_node, mapped_rule.parent, path_to_rule, grammar)

  # 6 SEQ: parent is SeqRule. Cannot do anything.
  elif isinstance(mapped_rule.parent, SeqRule):
    raise API_NoAlternativeError('need to consider children of the node')

  # 7 REP: parent is RepeatRule, check grandparent
  elif isinstance(mapped_rule.parent, RepeatRule):
    return get_alternative_starting_node_type(problematic_node, child_node, mapped_rule.parent, path_to_rule, grammar)

  # NOTE be vocal on new errors so new cases can be added above
  else:
    raise RuntimeError(f'rule.parent is {mapped_rule.parent.__class__.__name__}')


def _rank_node_types(node_types: List[str], grammar: TreeSitterGrammar) -> List[str]:
  '''
  Sort node types in ascending order.
  Node types that reach to literal tokens faster appear first.
  '''
  def __get_min_distance_optimized(from_node: str, to_node: str) -> Union[int, float]:
    '''
    Author: Jinwoo Choi
    '''
    nonlocal grammar
    queue = deque([(from_node, 0)])
    visited = set()

    while queue:
      cur_node, dist = queue.popleft()

      if cur_node == to_node:
        return dist

      if cur_node in visited:
        continue

      visited.add(cur_node)

      if not grammar.is_hidden(cur_node):
        dist += 1

      children = grammar.get_symbols_under(cur_node)
      for child in children:
        queue.append((child, dist))
    else:
      return float('inf')

  assert len(node_types) == len(set(node_types)), '`node_types` list contains duplicates (should not happen)'

  reachable_nodes = list(PY_GEN.keys())  # NOTE a bit hacky
  min_dists : List[Tuple[Tuple[str, str], int|float]] = []
  for node_type in node_types:
    for reachable_node in reachable_nodes:
      min_dist = __get_min_distance_optimized(node_type, reachable_node)
      min_dists.append(((node_type, reachable_node), min_dist))
  min_dists.sort(key=lambda min_dist: min_dist[1])
  ranked = [min_dist[0][0] for min_dist in min_dists]
  ranked = list(dict.fromkeys(ranked))  # remove duplicate while preserving order
  return ranked


# AST-GRAMMAR MATCH USAGE
def match_ast_usage() -> None:
  '''
  given an AST, match the grammar to it
  '''
  def _find_alternative_nodes(
    prob_node: p_data_structures.DuoGlotNode,
    ch_node: p_data_structures.DuoGlotNode,
    rule: Rule,
    path_to_rule: List[str],
    grammar: TreeSitterGrammar
  ) -> None:
    '''
    This is a recursive function.
    '''

    print(f'PROBLEMATIC NODE: <{prob_node}>')
    print(f'      CHILD NODE: <{ch_node}>')
    print(f'       RULE PATH: {path_to_rule}')
    print(f'            RULE: {rule}')
    print(f'     RULE.PARENT: {rule.parent}', end='\n')

    assert isinstance(rule, SymbolRule), 'should not happen?'

    # A mapping has a connection between problematic node's child node
    # and a symbol rule associated with it. The goal of this function
    # is to find alternative symbol rules that can be associated with
    # the child of the problematic node. At one of these symbol rules
    # we will start generation of a random AST (program) to later use
    # it as a substitute to the child node. To achieve this, we need to
    # check the parents of `rule`.

    is_sep1_res = grammar.is_sep1(rule.parent)
    is_optional_res = grammar.is_optional(rule.parent)
    prob_node_type = prob_node.get_ts_node_type()
    ch_node_type = ch_node.get_ts_node_type()

    # 1 OPTIONAL: optional is a ChoiceRule, but not all ChoiceRules are
    if is_optional_res is not None:
      # expect optionals to be directly under the production rule for the problematic node
      assert len(path_to_rule) == 0, f'"{rule}" is expected to be directly inside production rule for {prob_node_type}'

      # we can't do anything at this point, there are no alternatives
      print('~~~ OPTIONAL')
      print('no alternatives for associated SymbolRule')

    # 2 CHOICE: The simplest case is when a `rule` is an option of a ChoiceRule.
    # In this case, we select one of the alternatives to `rule`.
    # The alternative choice should not be external, SymbolRule(node_type)
    elif isinstance(rule.parent, ChoiceRule):
      alternatives = []
      for alt in rule.parent.members:
        if isinstance(alt, SymbolRule) and alt.name == ch_node_type:
          continue
        if isinstance(alt, SymbolRule) and grammar.is_external(alt.name):
          continue
        alternatives.append(alt)

      print('~~~ CHOICE')
      print(f'alternatives are (choose one):')
      print(alternatives)

    # 3 SEP1: cannot have any other options
    elif bool(is_sep1_res):
      # expect sep1 to be directly under the production rule
      # for the problematic node
      assert len(path_to_rule) == 0, f'"{rule}" is expected to be directly inside production rule for {prob_node_type}'

      print(f'~~~ SEP1')
      print(f'no alternatives: its parent is a sep1 rule')

    # 4 FIELD: parent is a field, check grandparent
    elif isinstance(rule.parent, FieldRule):
      print(f'~~~ FIELD')
      print('Parent is a FieldRule: need to check parent of FieldRule (recursive call):')
      _find_alternative_nodes(prob_node, ch_node, rule.parent, path_to_rule, grammar)

    # 5 SEQ: cannot do anything
    elif isinstance(rule.parent, SeqRule):
      print(f'~~~ SEQ')
      print('no alternatives for this node')

    else:
      raise RuntimeError(f'rule.parent is {rule.parent.__class__.__name__}')

    print()

  def _do_sth_with_mapping(
    prob_node: p_data_structures.DuoGlotNode,
    mappings: List[Tuple[p_data_structures.DuoGlotNode, Rule, List[str]]],
    grammar: TreeSitterGrammar
  ) -> None:
    ''''''
    for node, rule, path in mappings:
      _find_alternative_nodes(prob_node, node, rule, path, grammar)

  def _match_node_with_rule(node: p_data_structures.DuoGlotNode, rule: Rule, grammar: TreeSitterGrammar) -> None:
    assert node.is_nonterminal(), 'non-terminal node expected'

    children = node.get_children()
    # grammar matcher cannot handle comments at the moment
    children = [n for n in children if n.node_type != 'py.comment']
    nt_children = [n for n in children if n.is_nonterminal()]

    mapping = rule.get_ast_mapping(children, grammar)
    _do_sth_with_mapping(node, mapping, grammar)
    assert len(mapping) == len(nt_children), 'each non-terminal child should be mapped to a symbol'
    print()
    print('=' * 100)
    print('\n')

  # INPUTS
  grobj = p_utils.read_json('temporary_python-grammar.json')
  grammar = TreeSitterGrammar.from_dict(grobj)

  code = \
'''
### findMedianSortedArrays
import math
from math import inf
from typing import *
def f_gold(nums1: List[int], nums2: List[int]) -> float:
    def findKth(i, j, k):
        if i >= m:
            return nums2[j + k - 1]
        if j >= n:
            return nums1[i + k - 1]
        if k == 1:
            return min(nums1[i], nums2[j])
        midVal1 = nums1[i + k // 2 - 1] if i + k // 2 - 1 < m else float('inf')
        midVal2 = nums2[j + k // 2 - 1] if j + k // 2 - 1 < n else float('inf')
        if midVal1 < midVal2:
            return findKth(i + k // 2, j, k - k // 2)

        # this part is added to test some features
        elif True:
            for i in range(10):
                pass
            else:
                pass
        else:
            with open('hi.txt', 'r') as fin:
                fin.read()

        return findKth(i, j + k // 2, k - k // 2)
    m, n = len(nums1), len(nums2)
    left, right = (m + n + 1) // 2, (m + n + 2) // 2
    return (findKth(0, 0, left) + findKth(0, 0, right)) / 2
'''.strip()
  lang = 'py'
  ast, ann = d_ast_parse.parse_text_dbg(code, lang, keep_text=False)
  tree = p_data_structures.DuoGlotTree(ast)

  # p_utils.write_json('temporary_ast.json', ast)

  # ALGORITHM
  # for problematic_node_id in range(257):  # all
  # for problematic_node_id in [158]:  # single
  for problematic_node_id in range(14, 257):  # range
    prob_node = tree.get_node_with_id(problematic_node_id)
    prob_node_type = prob_node.get_ts_node_type()

    # skip certain nodes
    if prob_node_type in ['integer', 'identifier', 'string', 'string_content', 'comment', 'float']:
      continue
    # skip externals
    if grammar.is_external(prob_node_type):
      continue

    _match_node_with_rule(prob_node, grammar.rules[prob_node_type], grammar)


# AST GENERATION USAGE
def generate_usage() -> None:
  # INPUTS
  grobj = p_utils.read_json('temporary_python-grammar.json')
  grammar = TreeSitterGrammar.from_dict(grobj)

  # for start_node in ['_compound_statement']:
  # for start_node in ['list_splat_pattern']:
  # for start_node in ['expression']:
  # for start_node in ['string']:
  for start_node in ['if_statement']:
  # for start_node in ['while_statement']:
  # for start_node in ['for_statement']:
  # for start_node in ['class_definition']:
  # for start_node in ['function_definition']:
  # for start_node in ['block']:
  # for start_node in ['_statement']:
  # for start_node in ['_simple_statements']:
  # for start_node in ['_suite']:
  # for start_node in ['_simple_statement']:
  # for start_node in ['integer', 'identifier', 'true', 'primary_expression', 'parameter', 'expression', '_simple_statement']:
    gen_ast = grammar.generate_simplest_ast(start_node)
    p_utils.write_json('temporary_gen_ast.json', gen_ast)
    print(gen_ast)


# VISITOR GENERATOR
def visitor_generate_helper():
  '''
  Function to generate visitor pattern related classes and node classes
  for a tree-sitter grammar.
  '''

  def _node_type_title_case(node_type: str) -> str:
    '''given a node type in lowercase return a title case version'''
    swus = node_type.startswith('_')
    words = [word.capitalize() for word in node_type.split('_') if word != '']
    titled = ('_' if swus else '') + ''.join(words)
    return titled

  VISITOR_INTERFACE = \
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Union
import p_consts
import p_utils
import d_ast_parse
import tree_sitter


class Visitor(ABC):
  '''
  This is the Visitor interface for ASTs generated from parsing Python code.
  Should add an abstract method for each node type.

  NOTE
  This class changes only if the Tree-Sitter node types change for Python.
  '''
""".strip()

  METHOD_TEMPLATE = \
"""
@abstractmethod
def visit_{node_type}_node(self, node: {NodeType}Node) -> None:
  raise NotImplementedError
""".strip()

  ABSTRACT_NODE_CLASS = \
"""
class AbstractNode(ABC):
  '''
  This is the base class for node classes.
  All node classes should inherit from this class.

  INV1 self.parent is not None
  INV2 self.is_root_node() and self.parent == self
  '''
  def __init__(self, node_type: str) -> None:
    self.node_type = node_type
    self.children: List[AbstractNode] = []
    self.parent = None

  def __repr__(self) -> str:
    return self.node_type

  def add_child(self, child: AbstractNode):
    self.children.append(child)

  def get_children(self) -> List[AbstractNode]:
    return self.children

  def set_parent(self, parent: AbstractNode) -> None:
    self.parent = parent

  def get_parent(self) -> AbstractNode:
    assert self.parent is not None, 'class invariant is broken'
    return self.parent

  def get_root_node(self) -> AbstractNode:
    '''
    Return root_node of the tree that `self` belongs to
    According to class invariant INV2, root_node's parent is itself.
    '''
    cursor = self
    while cursor != cursor.parent:
      cursor = cursor.parent
    return cursor

  def get_path_to_self(self) -> List[int]:
    '''
    return path to `self` from the `root_node` of tree that `self` belongs to
    '''
    root_node = self.get_root_node()
    return root_node.get_path_to_child(self)

  def get_nt_children(self) -> List[AbstractNode]:
    '''
    Return a list of non-terminal children of `self`.
    '''
    return list(filter(lambda node: not isinstance(node, TerminalNode), self.children))

  def is_ancestor_or_itself(self, other_node: AbstractNode) -> bool:
    def _recurse(descendant: AbstractNode, other_node: AbstractNode) -> bool:
      if id(descendant) == id(other_node):
        return True
      for child_node in descendant.get_children():
        child_res = _recurse(child_node, other_node)
        if child_res:
          return True
      return False
    return _recurse(self, other_node)

  def get_path_to_child(self, child_node: AbstractNode) -> List[int]:
    '''return path to a node under self as a list of int indices'''
    assert self.is_ancestor_or_itself(child_node)
    def _rec_pre_order(path: List[int], node: AbstractNode) -> Union[None, List[int]]:
      nonlocal child_node
      if node == child_node:
        return path
      for i, nd in enumerate(node.get_children()):
        child_result = _rec_pre_order(path + [i], nd)
        if child_result is not None:
          return child_result
      return None
    path = _rec_pre_order([], self)
    assert path is not None, 'should not happen'
    return path

  def get_child_by_path(self, rel_path: List[int]) -> Union[AbstractNode, None]:
    '''return a child node by a relative path from self, None if not found'''
    try:
      child_node = self
      for child_idx in rel_path:
        child_node = child_node.get_children()[child_idx]
      return child_node
    except IndexError:
      return None

  @abstractmethod
  def accept(self, visitor: Visitor) -> None:
    pass
""".strip()

  NODE_CLASS_TEMPLATE = \
"""
class {NodeType}Node(AbstractNode):
  def accept(self, visitor: Visitor) -> Any:
    return visitor.visit_{node_type}_node(self)
""".strip()

  NODE_TYPES_CLASSES_DICT = \
"""
NODE_TYPES_CLASSES: Dict[str, AbstractNode] = {{
{pairs}
}}
""".strip()

  PAIR = """'{node_type}': {NodeType}Node,"""

  TREE_CLASS = \
"""
class Tree:
  '''
  Class that represents an AST that was generated by p_grammar.generate
  '''
  def __init__(self, root_node: AbstractNode) -> None:
    self.root_node: AbstractNode = root_node

  def __repr__(self) -> str:
    return f'Tree({self.root_node.node_type})'

  @classmethod
  def from_gen_ast(cls, ast: list) -> Tree:
    '''
    Construct a Tree from a structure generated by p_grammar.generate
    '''
    def _rec_construct_at(parent_node: AbstractNode, node: Union[list, str]) -> None:
      # base case: `node` is terminal
      if isinstance(node, str):
        new_node = TerminalNode(node)
        parent_node.add_child(new_node)
        new_node.set_parent(parent_node)
        return
      node_type, children = node[0], node[1:]
      NodeCls = NODE_TYPES_CLASSES[node_type]
      new_node = NodeCls(node_type)
      parent_node.add_child(new_node)
      new_node.set_parent(parent_node)
      for child in children:
        _rec_construct_at(new_node, child)

    root_node_type, children = ast[0], ast[1:]
    RootNodeCls = NODE_TYPES_CLASSES[root_node_type]
    root_node = RootNodeCls(root_node_type)
    root_node.set_parent(root_node)
    for child in children:
      _rec_construct_at(root_node, child)
    tree = Tree(root_node)
    return tree


if __name__ == '__main__':
  ast = p_utils.read_json('temporary_gen_ast.json')
  tree = Tree.from_gen_ast(ast)
  print(tree)
""".strip()

  # INPUTS
  grobj = p_utils.read_json('temporary_python-grammar.json')
  grammar = TreeSitterGrammar.from_dict(grobj)

  # manually add a class for terminal nodes
  # as they are not present in grammar
  NODE_TYPES = ['terminal'] + sorted(grammar.rules.keys())

  # Visitor interface
  code = ''
  code += VISITOR_INTERFACE
  code += '\n\n'
  for node_type in NODE_TYPES:
    titled = _node_type_title_case(node_type)
    code += p_utils.indent(METHOD_TEMPLATE.format(node_type=node_type, NodeType=titled), 2)
    code += '\n\n'
  code += '\n'

  # Node classes
  code += ABSTRACT_NODE_CLASS
  code += '\n\n'
  for node_type in NODE_TYPES:
    titled = _node_type_title_case(node_type)
    code += NODE_CLASS_TEMPLATE.format(node_type=node_type, NodeType=titled)
    code += '\n\n'
  code += '\n'

  # Node types classes dictionary
  pairs = ''
  for node_type in NODE_TYPES:
    titled = _node_type_title_case(node_type)
    pairs += PAIR.format(node_type=node_type, NodeType=titled)
    pairs += '\n'
  pairs = p_utils.indent(pairs.strip(), 2)
  code += NODE_TYPES_CLASSES_DICT.format(pairs=pairs)
  code += '\n\n\n'

  # Tree class
  code += TREE_CLASS
  code += '\n'

  # p_utils.write_text('temporary_visitor.py', code)
  return code


# PROGRAM SIMPLIFICATION USAGE
def simplify_program_context_usage() -> None:
  '''
  WHAT DO WE NEED?
  We need a list of nodes that we can remove from the AST.

  We have two ways of simplification:
  1. Remove the simplifiable node
  2. IF all of the non-terminal children of a node can be simplified
     AND problematic node is one of those child nodes, THEN
     remove everything EXCEPT the problematic node.
  3.

  NOTE
  Current implementation is not complete. Not all nodes that are
  classified to be simplified, can in fact be simplified. For
  example, we cannot handle the case of `type` in `function_definition`.
  `type` is optional, but it comes with a terminal `->`, and if
  we remove `type` we will keep `->` and this way we get a syntax error.
  '''

  def _is_simplifiable_node(
    node: p_data_structures.DuoGlotNode,
    problematic_node: p_data_structures.DuoGlotNode
  ) -> bool:
    if node.is_terminal():
      return False
    if node.is_ancestor_or_itself(problematic_node):
      return False
    return True

  def _rec_pre_order_collect_potential_simplifiable_nodes(
    at_node: p_data_structures.DuoGlotNode,
    context_node: p_data_structures.DuoGlotNode,
    problematic_node: p_data_structures.DuoGlotNode,
    container: dict
  ):
    if at_node == problematic_node:
      return
    if _is_simplifiable_node(at_node, problematic_node):
      # container[at_node.get_id()] = context_node.get_path_to_child(at_node)
      container[at_node.get_id()] = at_node
    for child in at_node.get_children():
      _rec_pre_order_collect_potential_simplifiable_nodes(child, context_node, problematic_node, container)

  def _get_simplifiable_nodes(
    context_node: p_data_structures.DuoGlotNode,
    problematic_node: p_data_structures.DuoGlotNode
  ) -> Dict[int, p_data_structures.DuoGlotNode]:
    simplifiable_nodes = {}
    _rec_pre_order_collect_potential_simplifiable_nodes(
      context_node,
      context_node,
      problematic_node,
      simplifiable_nodes
    )
    return simplifiable_nodes

  def _child_node_can_be_simplified(
    parent_node: p_data_structures.DuoGlotNode,
    child_node: p_data_structures.DuoGlotNode,
    production_path: List[str],  # ['_right_hand_side', 'expression', 'primary_expression']
    grammar: TreeSitterGrammar
  ) -> bool:

    def __rule_path_allows_node_removal(
      rule_path: List[str]
    ) -> bool:
      '''
      Tells us whether this rule path allows node removal
      '''
      if 'optional' in rule_path or 'repeat' in rule_path:
        return True
      return False

    def __production_pair_allows_node_removal(
      production_pair: Tuple[str, str],  # ('_right_hand_side', 'expression')
      grammar: TreeSitterGrammar
    ) -> bool:
      parent, child = production_pair
      assert not grammar.is_external(parent), 'sanity check'
      par_rule = grammar.rules[parent]
      rule_paths = par_rule.get_rule_seq_to_symbol_rule(child, grammar)
      if all(map(__rule_path_allows_node_removal, rule_paths)):
        return True
      return False

    par_ntype = parent_node.get_ts_node_type()
    ch_ntype = child_node.get_ts_node_type()

    production_path.insert(0, par_ntype)
    production_path.append(ch_ntype)

    production_pairs = list(zip(production_path[:-1], production_path[1:]))
    if any(map(lambda pp: __production_pair_allows_node_removal(pp, grammar), production_pairs)):
      return True
    return False

  def _process_simplifiable_node(
    simplifiable_node: p_data_structures.DuoGlotNode,
    grammar: TreeSitterGrammar
  ) -> Dict[int, bool]:

    par_simpl_node = simplifiable_node.parent
    par_simpl_ntype = par_simpl_node.get_ts_node_type()

    assert par_simpl_node.is_nonterminal(), 'non-terminal node expected'

    print(f'~~           SIMPLIFIABLE NODE: <{simplifiable_node}>')
    print(f'~~ PARENT OF SIMPLIFIABLE NODE: <{par_simpl_node}>')
    print('`' * 50)

    assert not grammar.is_external(par_simpl_ntype)
    par_rule = grammar.rules[par_simpl_ntype]

    # ~~~ obtain mappings
    siblings_simpl_node = par_simpl_node.get_children()
    # grammar matcher cannot handle comments at the moment
    siblings_simpl_node = [n for n in siblings_simpl_node if n.node_type != 'py.comment']
    nt_siblings_simpl_node = [n for n in siblings_simpl_node if n.is_nonterminal()]
    assert len(nt_siblings_simpl_node) > 0, 'sanity check'
    try:
      mappings = par_rule.get_ast_mapping(siblings_simpl_node, grammar)
    except AM_UnmappableError:
      print('unmappable node')
      return {}

    # ~~~ process mappings
    # can simplifiable node be simplified?
    # can all non-terminal siblings of simplifiable node be simplified?
    can_be_simplified_dict : Dict[int, bool] = {}
    for mapping in mappings:
      mapped_node, mapped_rule, production_path = mapping
      print(f'               SIMPLIFIABLE NODE SIBLING: <{mapped_node}>')
      print(f'     PARENT OF SIMPLIFIABLE NODE SIBLING: <{par_simpl_node}>')
      print(f'PATH PARENT -> SIMPLIFIABLE NODE SIBLING: {production_path}')
      print(f'                             MAPPED RULE: {mapped_rule}')

      can_be_simplified = _child_node_can_be_simplified(par_simpl_node, mapped_node, production_path, grammar)
      can_be_simplified_dict[mapped_node.get_id()] = can_be_simplified
      print(f'                       CAN BE SIMPLIFIED: {can_be_simplified}')
      print('-' * 100)

    assert simplifiable_node.get_id() in can_be_simplified_dict, 'sanity check: simplifiable node must be present'

    print(f'                SIMPLIFIABLE NODE CAN BE SIMPLIFIED: {can_be_simplified_dict[simplifiable_node.get_id()]}')
    print(f'ALL SIBLINGS OF SIMPLIFIABLE NODE CAN BE SIMPLIFIED: {all(can_be_simplified_dict.values())}')
    print()

    return can_be_simplified_dict

  def _process_can_be_simplified_dict(
    nodes_can_be_simplified: Dict[int, Dict[int, bool]],
    problematic_node: p_data_structures.DuoGlotNode,
    simpl_nodes_dict: Dict[int, p_data_structures.DuoGlotNode]
  ):
    '''
    1. if all siblings can be simplified
      a. problematic node is one of the siblings -> leave only the problematic node
      b. problematic node is not one of the sibligns -> remove all the nodes
    2. if all siblings cannot be simplified, only the node itself can be simplified
      a. remove the node (if removing it does not induce syntax errors as in return type annotation)
    3. node cannot be simplified -> do not do anything
    '''

    def __all_siblings_can_be_simplified_prob_no(
      nodes_can_be_simplified_copy: Dict[int, Dict[int, bool]],
      problematic_node_id: int
    ) -> Optional[int]:
      '''
      Return the smallest `node_id` (either parent or previous sibling)
      for which all siblings can be simplified and problematic node is not one of the siblings
      '''
      for nid in sorted(nodes_can_be_simplified_copy):
        can_be_simplified_values = nodes_can_be_simplified_copy[nid]
        if all(can_be_simplified_values.values()) and problematic_node_id not in can_be_simplified_values:
          return nid
      return None

    def __all_siblings_can_be_simplified_prob_yes(
      nodes_can_be_simplified_copy: Dict[int, Dict[int, bool]],
      problematic_node_id: int
    ) -> Optional[int]:
      '''
      Return the smallest `node_id` (either parent or previous sibling)
      for which all siblings can be simplified and problematic node is one of the siblings
      NOTE this function should return a value no more than once
      '''
      for nid in sorted(nodes_can_be_simplified_copy):
        can_be_simplified_values = nodes_can_be_simplified_copy[nid]
        if all(can_be_simplified_values.values()) and problematic_node_id in can_be_simplified_values:
          return nid
      return None

    def __process_all_siblings_can_be_simplified_node_prob_no(
      siblings_can_be_removed_node_id: int,
      nodes_can_be_simplified_copy: Dict[int, Dict[int, bool]],
      simpl_nodes_dict: Dict[int, p_data_structures.DuoGlotNode]
    ) -> p_data_structures.DuoGlotNode:
      '''
      modifies `nodes_can_be_simplified_copy`
      Return a reference to a node whose all non-terminal children
      can be simplified. In other words, return a reference to a
      parent node of a node whose all siblings can be simplified.
      '''
      # get the parent node of siblings that can all be simplified
      parent_node = simpl_nodes_dict[siblings_can_be_removed_node_id].get_parent()

      # remove `siblings_can_be_removed_node_id` and its descendants
      siblings_can_be_simplified_nids = list(nodes_can_be_simplified_copy[siblings_can_be_removed_node_id].keys())
      for sibling_can_be_simplified_nid in sorted(siblings_can_be_simplified_nids):
        sibling_can_be_simplified = simpl_nodes_dict[sibling_can_be_simplified_nid]
        # remove the descendants in reverse order (why?)
        descendants = sibling_can_be_simplified.get_nonterminal_descendants()
        descendants.sort(key=lambda node: node.get_id(), reverse=True)
        for descendant in descendants:
          if descendant.get_id() in nodes_can_be_simplified_copy:
            nodes_can_be_simplified_copy.pop(descendant.get_id())
        # remove the node itself
        nodes_can_be_simplified_copy.pop(sibling_can_be_simplified_nid)

      return parent_node

    def __process_all_siblings_can_be_simplified_node_prob_yes(
      siblings_can_be_removed_node_id: int,
      nodes_can_be_simplified_copy: Dict[int, Dict[int, bool]],
      simpl_nodes_dict: Dict[int, p_data_structures.DuoGlotNode]
    ) -> Tuple[p_data_structures.DuoGlotNode, p_data_structures.DuoGlotNode]:
      '''
      modifies `nodes_can_be_simplified_copy`

      `siblings_can_be_removed_node_id` is a `node_id` of the problematic node
      whose all siblings can be removed.

      What do we do?
      1. get the leftmost non-terminal sibling (L)
      2. get the rightmost non-terminal sibling (R)
      3. remove everything between (L) and (R) but keep the problematic node itself

      We can remove non-terminal nodes by using annotation marks in `ann` dictionary
      provided by `d_ast_parse.parse_text_dbg` function.

      How about terminal nodes?
      We can get the annotations for the terminal nodes by traversing the
      tree that we obtained by parsing the program by tree-sitter

      What do we return?
      Reference to the leftmost, and the rightmost non-terminal nodes.
      '''
      # get the leftmost and rightmost siblings of problematic node
      node_can_be_simplified_dict = nodes_can_be_simplified_copy[siblings_can_be_removed_node_id]
      assert all(node_can_be_simplified_dict.values()), 'sanity check'
      node_ids = node_can_be_simplified_dict.keys()
      leftmost_node = simpl_nodes_dict[min(node_ids)]
      rightmost_node = simpl_nodes_dict[max(node_ids)]

      siblings_can_be_simplified_nids = list(nodes_can_be_simplified_copy[siblings_can_be_removed_node_id].keys())
      for sibling_can_be_simplified_nid in sorted(siblings_can_be_simplified_nids):
        sibling_can_be_simplified = simpl_nodes_dict[sibling_can_be_simplified_nid]
        # remove the descendants in reverse order (why?)
        descendants = sibling_can_be_simplified.get_nonterminal_descendants()
        descendants.sort(key=lambda node: node.get_id(), reverse=True)
        for descendant in descendants:
          if descendant.get_id() in nodes_can_be_simplified_copy:
            nodes_can_be_simplified_copy.pop(descendant.get_id())
        # remove the node itself
        nodes_can_be_simplified_copy.pop(sibling_can_be_simplified_nid)

      return leftmost_node, rightmost_node

    # ~~~ artifacts
    all_children_can_be_simplified_nodes_list : List[p_data_structures.DuoGlotNode] = []
    leftmost_rightmost_siblings_problematic_node : Optional[Tuple[p_data_structures.DuoGlotNode, p_data_structures.DuoGlotNode]] = None

    nodes_can_be_simplified_copy = copy.deepcopy(nodes_can_be_simplified)

    print()
    print('~~~ _process_can_be_simplified_dict')
    # ~~~ phase 1: go over nodes for which all siblings can be simplified and
    # problematic node is not one of the siblings
    # in this case, we remove all simplifiable nodes
    while True:
      siblings_can_be_removed_node_id = __all_siblings_can_be_simplified_prob_no(
        nodes_can_be_simplified_copy,
        problematic_node.get_id()
      )
      if siblings_can_be_removed_node_id is None:
        break
      parent_node_of_simpl_nodes = __process_all_siblings_can_be_simplified_node_prob_no(
        siblings_can_be_removed_node_id,
        nodes_can_be_simplified_copy,
        simpl_nodes_dict
      )
      all_children_can_be_simplified_nodes_list.append(parent_node_of_simpl_nodes)

    print('children of these nodes can all be simplified')
    print(json.dumps(all_children_can_be_simplified_nodes_list, indent=2, default=str))
    print('nodes_can_be_simplified_copy')
    print(json.dumps(nodes_can_be_simplified_copy, indent=2, default=str))

    # ~~~ phase 2: go over nodes for which all siblings can be simplified and
    # problematic node is one of the siblings
    # in this case, we remove all simplifiable nodes except the problematic node
    # there should be no more than one such node
    siblings_can_be_removed_node_id = __all_siblings_can_be_simplified_prob_yes(
      nodes_can_be_simplified_copy,
      problematic_node.get_id()
    )
    if siblings_can_be_removed_node_id is not None:
      leftmost_rightmost_siblings_problematic_node = __process_all_siblings_can_be_simplified_node_prob_yes(
        siblings_can_be_removed_node_id,
        nodes_can_be_simplified_copy,
        simpl_nodes_dict
      )

    # ~~~ phase 3: go over nodes which can be simplified on their own
    # leave this as a future work TODO

    return all_children_can_be_simplified_nodes_list, leftmost_rightmost_siblings_problematic_node

  def _simplify_context(
    all_children_can_be_simplified_nodes_list: List[p_data_structures.DuoGlotNode],
    leftmost_rightmost_siblings_problematic_node : Optional[Tuple[p_data_structures.DuoGlotNode, p_data_structures.DuoGlotNode]],
    problematic_node: p_data_structures.DuoGlotNode,
    template_dict: dict,
    grammar: p_grammar.TreeSitterGrammar
  ) -> str:
    '''
    Actual context simplification happens here.
    We need to go over the nodes in reverse pre-order fashion.
    '''
    def __gen_code_for_node_type(node_type: str, grammar: p_grammar.TreeSitterGrammar):
      ast = grammar.generate_simplest_ast(node_type)
      ast_tree = p_visitor_py.Tree.from_gen_ast(ast)
      code = p_visitor_py.PrettyPrinterForGeneratedCode().visit(ast_tree.root_node)
      return code

    def __process_parent_nodes(
      parent_nodes: List[p_data_structures.DuoGlotNode],
      context_tree: p_data_structures.PirelTree,
      orig_text: str,
      grammar: p_grammar.TreeSitterGrammar
    ):
      parent_nodes.sort(key=lambda n: n.get_id(), reverse=True)
      for parent_node in parent_nodes:
        replacement_code = __gen_code_for_node_type(parent_node.get_ts_node_type(), grammar)
        start_point = context_tree.annotation[parent_node.get_id()][0]
        end_point = context_tree.annotation[parent_node.get_id()][1]
        orig_text = orig_text[:start_point] + replacement_code + orig_text[end_point:]
      return orig_text

    def __process_problematic_node(
      leftmost_node: p_data_structures.DuoGlotNode,
      rightmost_node: p_data_structures.DuoGlotNode,
      problematic_node: p_data_structures.DuoGlotNode,
      context_tree: p_data_structures.PirelTree,
      context_node: p_data_structures.PirelNode,
      orig_text: str,
      template_dict: dict
    ):
      '''
      writes to `template_dict`
      '''
      start_point = context_tree.annotation[leftmost_node.get_id()][0]
      end_point = context_tree.annotation[rightmost_node.get_id()][1]
      replacement_code = context_tree.get_node_with_id(problematic_node.get_id()).get_text()
      orig_text = orig_text[:start_point] + replacement_code + orig_text[end_point:]

      # update problematic node's info in `template_dict`
      updated_problematic_node = context_tree.get_node_with_id(leftmost_node.get_id())
      template_dict['problematic_node_id'] = updated_problematic_node.get_id()
      template_dict['problematic_node_path'] = context_node.get_path_to_child(updated_problematic_node)

      return orig_text

    template_origin = template_dict['template_origin']
    src_lang = template_dict['src_lang']

    context_ast_text, context_annotation = d_ast_parse.parse_text_dbg(template_origin, lang=src_lang, keep_text=True)
    context_tree = p_data_structures.PirelTree(context_ast_text, annotation=context_annotation)
    context_tree._fix_indentation()
    context_node = context_tree.get_root_node().get_children()[0]
    orig_text = context_node.get_text()

    # split `all_children_can_be_simplified_nodes_list` into nodes
    # that appear before and after problematic node
    pre_accbs_nodes_list = []
    post_accbs_nodes_list = []
    if leftmost_rightmost_siblings_problematic_node is not None:
      leftmost_node = leftmost_rightmost_siblings_problematic_node[0]
      rightmost_node = leftmost_rightmost_siblings_problematic_node[1]
      pre_accbs_nodes_list = [n for n in all_children_can_be_simplified_nodes_list if n.get_id() < leftmost_node.get_id()]
      post_accbs_nodes_list = [n for n in all_children_can_be_simplified_nodes_list if n.get_id() > rightmost_node.get_id()]
    else:
      pre_accbs_nodes_list = [n for n in all_children_can_be_simplified_nodes_list if n.get_id() < problematic_node.get_id()]
      post_accbs_nodes_list = [n for n in all_children_can_be_simplified_nodes_list if n.get_id() > problematic_node.get_id()]

    # simplify parent nodes that appear after problematic node
    orig_text = __process_parent_nodes(post_accbs_nodes_list, context_tree, orig_text, grammar)

    # simplify problematic node's siblings
    if leftmost_rightmost_siblings_problematic_node is not None:
      orig_text = __process_problematic_node(
        leftmost_rightmost_siblings_problematic_node[0],
        leftmost_rightmost_siblings_problematic_node[1],
        problematic_node,
        context_tree,
        context_node,
        orig_text,
        template_dict
      )

    # simplify parent nodes that appear before problematic node
    # NOTE commented out, because this changes the problematic node's id
    # orig_text = __process_parent_nodes(pre_accbs_nodes_list, context_tree, orig_text, grammar)

    return orig_text

  config_fpath = p_utils.read_json('temporary_simplify_program_context_config.json')
  template_dict = p_utils.read_json(config_fpath['template_dict_fpath'])

  template_origin = template_dict['template_origin']
  src_lang = template_dict['src_lang']
  problematic_node_path = template_dict['problematic_node_path']

  ast, ann = d_ast_parse.parse_text_dbg(template_origin, src_lang, keep_text=False)
  # p_utils.write_json('temporary_ast.json', ast)
  tree = p_data_structures.DuoGlotTree(ast)
  root_node = tree.root_node
  assert len(root_node.get_children()) == 1, 'sanity check: root node must have exactly one child'

  # ~~~ these are the main artifacts
  context_node = root_node.get_children()[0]
  problematic_node = context_node.get_child_by_path(problematic_node_path)
  simplifiable_nodes = _get_simplifiable_nodes(context_node, problematic_node)

  print(f'~~~       CONTEXT NODE: <{context_node}>')
  print(f'~~~   PROBLEMATIC NODE: <{problematic_node}>')
  sn_str = '\n'.join(map(lambda sn: f'<{str(sn)}>', simplifiable_nodes.values()))
  print(f'~~~ SIMPLIFIABLE NODES:\n{sn_str}\n')

  grobj = p_utils.read_json('temporary_python-grammar.json')
  grammar = TreeSitterGrammar.from_dict(grobj)

  # ~~~ check which nodes can be simplified
  nodes_can_be_simplified_dict : Dict[int, Dict[int, bool]] = {}
  simpl_nodes_dict : Dict[int, p_data_structures.DuoGlotNode] = {}
  for snid, simpl_node in simplifiable_nodes.items():
    can_be_simplified_dict = _process_simplifiable_node(simpl_node, grammar)
    nodes_can_be_simplified_dict[simpl_node.get_id()] = can_be_simplified_dict
    simpl_nodes_dict[simpl_node.get_id()] = simpl_node

  print(json.dumps(nodes_can_be_simplified_dict, indent=2, default=str))

  # ~~~ process nodes that can be simplified
  all_children_can_be_simplified_nodes_list, leftmost_rightmost_siblings_problematic_node = _process_can_be_simplified_dict(
    nodes_can_be_simplified_dict,
    problematic_node,
    simpl_nodes_dict
  )

  # ~~~ simplify the context
  simplified_code = _simplify_context(
    all_children_can_be_simplified_nodes_list,
    leftmost_rightmost_siblings_problematic_node,
    problematic_node,
    template_dict,
    grammar
  )

  print('simplified code:')
  print(simplified_code)
  print('updated template dict:')
  print(json.dumps(template_dict, indent=2, default=str))


# FINDING WHETHER A PRODUCTION IS OPTIONAL (USAGE)
def run_optional_production_usage():
  grobj = p_utils.read_json('temporary_python-grammar.json')
  grammar = TreeSitterGrammar.from_dict(grobj)

  start_rule_name = 'assignment'
  end_rule_name = '_left_hand_side'
  end_rule_name = '_right_hand_side'
  start_rule_name = input('start: ')
  end_rule_name = input('end: ')

  rule = grammar.rules[start_rule_name]
  rule_paths = rule.get_rule_seq_to_symbol_rule(end_rule_name, grammar)
  print(json.dumps(rule_paths, indent=2))


# TEST HARNESSES
def _test_simplify_template():
  test_harness_config:dict = p_utils.read_json('temporary_p_grammar_test_simplify_template_config.json')
  template_dict = p_utils.read_json(test_harness_config['template_dict_fpath'])
  kwargs = {
    'subject_name': 'test_simplify_template',
  }
  updated_template_dict = simplify_template(template_dict, **kwargs)
  print('\nsimplified context:')
  print(updated_template_dict['template_origin'])
  print('\nupdated template_dict:')
  print(json.dumps(updated_template_dict, indent=2))
  p_utils.write_json('temporary_test_simplify_template.json', updated_template_dict)


def _test_get_alternative_starting_node_types():
  config_dict = p_utils.read_json('temporary_test_get_alternative_starting_node_types_config.json')
  src_code = config_dict['src_code']
  src_lang = config_dict['src_lang']
  problematic_node_id = config_dict['problematic_node_id']

  ast, ann = d_ast_parse.parse_text_dbg(src_code, src_lang, keep_text=False)
  tree = p_data_structures.DuoGlotTree(ast)
  problematic_node = tree.get_node_with_id(problematic_node_id)

  grobj = p_consts.GRAMMAR_DICT_READONLY[src_lang]
  grammar = TreeSitterGrammar.from_dict(grobj)

  alt_start_node_types = get_alternative_starting_node_types(problematic_node, grammar)
  print(alt_start_node_types)


if __name__ == '__main__':
  # AST-grammar matching
  # match_ast_usage()

  # AST generation
  # generate_usage()

  # Visitor generator
  # visitor_generate_helper()

  # program/template simplification
  # simplify_program_context_usage()

  # removing optional productions (program simplification)
  # run_optional_production_usage()

  # _test_simplify_template()
  _test_get_alternative_starting_node_types()
