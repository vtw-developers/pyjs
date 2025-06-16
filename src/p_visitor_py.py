'''
This module provides classes for working with Python ASTs.

Classes:
  - *Node: classes that represent nodes in a Python AST
  - Tree: represents a Python AST
  - PrettyPrinter: a visitor class that prints a Python AST in a readable format
  - ParametrizableVariablesCollector: a visitor class that collects parametrizable variables in a Python AST
  - LogStatementInserter: a visitor class that inserts print statements in a Python AST

Constants:
  - NODE_TYPES_CLASSES: dictionary that maps node types to their respective classes
  - NODES_WITH_FIELDS: list of node types that have fields
'''


from __future__ import annotations

import tree_sitter
from typing import Dict, List, Union

import p_consts
import p_utils
import p_visitor as pvis


class _CollectionElementsNode(pvis.AbstractNode): pass
class _CompoundStatementNode(pvis.AbstractNode): pass
class _ComprehensionClausesNode(pvis.AbstractNode): pass
class _ExpressionWithinForInClauseNode(pvis.AbstractNode): pass
class _ExpressionsNode(pvis.AbstractNode): pass
class _ImportListNode(pvis.AbstractNode): pass
class _LeftHandSideNode(pvis.AbstractNode): pass
class _ParametersNode(pvis.AbstractNode): pass
class _PatternsNode(pvis.AbstractNode): pass
class _RightHandSideNode(pvis.AbstractNode): pass
class _SimpleStatementNode(pvis.AbstractNode): pass
class _SimpleStatementsNode(pvis.AbstractNode): pass
class _StatementNode(pvis.AbstractNode): pass
class _SuiteNode(pvis.AbstractNode): pass
class AliasedImportNode(pvis.AbstractNode): pass
class ArgumentListNode(pvis.AbstractNode):
  @classmethod
  def build(self, arguments: List[pvis.AbstractNode]) -> ArgumentListNode:
    '''
    Build an argument list node from a list of arguments
    NOTE developer is responsible for ensuring grammatical correctness
    '''
    node = ArgumentListNode('argument_list')
    left_par = pvis.TerminalNode('(')
    node.add_child(left_par)
    left_par.set_parent(node)
    for idx, arg in enumerate(arguments):
      node.add_child(arg)
      arg.set_parent(node)
      if idx < len(arguments) - 1:
        comma = pvis.TerminalNode(',')
        node.add_child(comma)
        comma.set_parent(node)
    right_par = pvis.TerminalNode(')')
    node.add_child(right_par)
    right_par.set_parent(node)
    return node
class AssertStatementNode(pvis.AbstractNode): pass
class AssignmentNode(pvis.AbstractNode):
  def __init__(self, node_type: str):
    super().__init__(node_type)
    self.left : pvis.AbstractNode = None
    self.type : pvis.AbstractNode = None
    self.right : pvis.AbstractNode = None
class AttributeNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.object : pvis.AbstractNode = None
    self.attribute : pvis.AbstractNode = None
class AugmentedAssignmentNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.left : pvis.AbstractNode = None
    self.operator : pvis.AbstractNode = None
    self.right : pvis.AbstractNode = None
class AwaitNode(pvis.AbstractNode): pass
class BinaryOperatorNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.left : pvis.AbstractNode = None
    self.operator : pvis.AbstractNode = None
    self.right : pvis.AbstractNode = None
class BlockNode(pvis.AbstractNode): pass
class BooleanOperatorNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.left : pvis.AbstractNode = None
    self.operator : pvis.AbstractNode = None
    self.right : pvis.AbstractNode = None
class BreakStatementNode(pvis.AbstractNode): pass
class CallNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.function : pvis.AbstractNode = None
    self.arguments : pvis.AbstractNode = None
  @classmethod
  def build(self, function: IdentifierNode, arguments: ArgumentListNode) -> CallNode:
    '''
    Build a call node from a function and an argument list
    NOTE developer is responsible for ensuring grammatical correctness
    '''
    assert isinstance(function, IdentifierNode), 'function must be an IdentifierNode'
    assert isinstance(arguments, ArgumentListNode), 'arguments must be an ArgumentListNode'
    node = CallNode('call')
    node.function = function
    node.arguments = arguments
    node.add_child(function)
    function.set_parent(node)
    node.add_child(arguments)
    arguments.set_parent(node)
    return node
class ChevronNode(pvis.AbstractNode): pass
class ClassDefinitionNode(pvis.AbstractNode): pass
class CommentNode(pvis.AbstractNode): pass
class ComparisonOperatorNode(pvis.AbstractNode): pass
class ConcatenatedStringNode(pvis.AbstractNode): pass
class ConditionalExpressionNode(pvis.AbstractNode): pass
class ContinueStatementNode(pvis.AbstractNode): pass
class DecoratedDefinitionNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.definition : pvis.AbstractNode = None
class DecoratorNode(pvis.AbstractNode): pass
class DefaultParameterNode(pvis.AbstractNode): pass
class DeleteStatementNode(pvis.AbstractNode): pass
class DictionaryNode(pvis.AbstractNode): pass
class DictionaryComprehensionNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.body : pvis.AbstractNode = None
class DictionarySplatNode(pvis.AbstractNode): pass
class DictionarySplatPatternNode(pvis.AbstractNode): pass
class DottedNameNode(pvis.AbstractNode): pass
class ElifClauseNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.condition : pvis.AbstractNode = None
    self.consequence : pvis.AbstractNode = None
class EllipsisNode(pvis.AbstractNode): pass
class ElseClauseNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.body : pvis.AbstractNode = None
class EscapeInterpolationNode(pvis.AbstractNode): pass
class EscapeSequenceNode(pvis.AbstractNode): pass
class ExceptClauseNode(pvis.AbstractNode): pass
class ExecStatementNode(pvis.AbstractNode): pass
class ExpressionNode(pvis.AbstractNode): pass
class ExpressionListNode(pvis.AbstractNode): pass
class ExpressionStatementNode(pvis.AbstractNode):
  @classmethod
  def build(cls, child_node: pvis.AbstractNode) -> ExpressionStatementNode:
    '''
    Build an expression statement as a parent of `child_node`
    NOTE developer is responsible for ensuring grammatical correctness
    '''
    node = cls('expression_statement')
    node.add_child(child_node)
    child_node.set_parent(node)
    return node
class FalseNode(pvis.AbstractNode): pass
class FinallyClauseNode(pvis.AbstractNode): pass
class FloatNode(pvis.AbstractNode):
  def val(self) -> str:
    assert len(self.children) == 1, 'sanity check'
    assert isinstance(self.children[0], pvis.TerminalNode), 'sanity check'
    return self.children[0].node_type
class ForInClauseNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.left : pvis.AbstractNode = None
    self.right : pvis.AbstractNode = None
class ForStatementNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.left : pvis.AbstractNode = None
    self.right : pvis.AbstractNode = None
    self.body : pvis.AbstractNode = None
    self.alternative : pvis.AbstractNode = None
class FormatExpressionNode(pvis.AbstractNode): pass
class FormatSpecifierNode(pvis.AbstractNode): pass
class FunctionDefinitionNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.name : pvis.AbstractNode = None
    self.parameters : pvis.AbstractNode = None
    self.return_type : pvis.AbstractNode = None
    self.body : pvis.AbstractNode = None
class FutureImportStatementNode(pvis.AbstractNode): pass
class GeneratorExpressionNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.body : pvis.AbstractNode = None
class GlobalStatementNode(pvis.AbstractNode): pass
class IdentifierNode(pvis.AbstractNode):
  def __init__(self, node_type: str):
    super().__init__(node_type)
  def __repr__(self) -> str:
    return f'ID({self.val()})'
  def val(self) -> str:
    assert len(self.children) == 1, 'sanity check'
    assert isinstance(self.children[0], pvis.TerminalNode), 'sanity check'
    return self.children[0].node_type
  @classmethod
  def build(cls, name: str) -> IdentifierNode:
    '''Build an identifier node from a string'''
    node = cls('identifier')
    tnode = pvis.TerminalNode(name)
    node.add_child(tnode)
    tnode.set_parent(node)
    return node
class IfClauseNode(pvis.AbstractNode): pass
class IfStatementNode(pvis.AbstractNode):
  '''
  In tree-sitter AST, multiple nodes may appear under a single field `alternative`.
  Since a single attribute holds a single node,
  we use `alternatives` attribute to hold all nodes under `alternative`.
  '''
  def __init__(self, node_type):
    super().__init__(node_type)
    self.condition : pvis.AbstractNode = None
    self.consequence : pvis.AbstractNode = None
    self.alternatives : List[pvis.AbstractNode] = []
class ImportFromStatementNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.module_name : pvis.AbstractNode = None
class ImportPrefixNode(pvis.AbstractNode): pass
class ImportStatementNode(pvis.AbstractNode): pass
class IntegerNode(pvis.AbstractNode):
  def val(self) -> str:
    assert len(self.children) == 1, 'sanity check'
    assert isinstance(self.children[0], pvis.TerminalNode), 'sanity check'
    return self.children[0].node_type
class InterpolationNode(pvis.AbstractNode): pass
class KeywordArgumentNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.name : pvis.AbstractNode = None
    self.value : pvis.AbstractNode = None
class KeywordIdentifierNode(pvis.AbstractNode): pass
class LambdaNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.parameters : pvis.AbstractNode = None
    self.body : pvis.AbstractNode = None
class LambdaParametersNode(pvis.AbstractNode): pass
class LambdaWithinForInClauseNode(pvis.AbstractNode): pass
class ListNode(pvis.AbstractNode): pass
class ListComprehensionNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.body : pvis.AbstractNode = None
class ListPatternNode(pvis.AbstractNode): pass
class ListSplatNode(pvis.AbstractNode): pass
class ListSplatPatternNode(pvis.AbstractNode): pass
class ModuleNode(pvis.AbstractNode): pass
class NamedExpressionNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.name : pvis.AbstractNode = None
    self.value : pvis.AbstractNode = None
class NoneNode(pvis.AbstractNode): pass
class NonlocalStatementNode(pvis.AbstractNode): pass
class NotEscapeSequenceNode(pvis.AbstractNode): pass
class NotOperatorNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.argument : pvis.AbstractNode = None
class PairNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.key : pvis.AbstractNode = None
    self.value : pvis.AbstractNode = None
class ParameterNode(pvis.AbstractNode): pass
class ParametersNode(pvis.AbstractNode): pass
class ParenthesizedExpressionNode(pvis.AbstractNode): pass
class ParenthesizedListSplatNode(pvis.AbstractNode): pass
class PassStatementNode(pvis.AbstractNode):
  @classmethod
  def build(cls) -> PassStatementNode:
    '''Build a pass statement node'''
    node = cls('pass_statement')
    tnode = pvis.TerminalNode('pass')
    node.add_child(tnode)
    tnode.set_parent(node)
    return node
class PatternNode(pvis.AbstractNode): pass
class PatternListNode(pvis.AbstractNode): pass
class PrimaryExpressionNode(pvis.AbstractNode): pass
class PrintStatementNode(pvis.AbstractNode): pass
class RaiseStatementNode(pvis.AbstractNode): pass
class RelativeImportNode(pvis.AbstractNode): pass
class ReturnStatementNode(pvis.AbstractNode): pass
class SetNode(pvis.AbstractNode): pass
class SetComprehensionNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.body : pvis.AbstractNode = None
class SliceNode(pvis.AbstractNode): pass
class StringNode(pvis.AbstractNode):
  '''NOTE may not support all types of quoted strings'''
  def val(self) -> str:
    assert len(self.children) == 1, 'sanity check'
    assert isinstance(self.children[0], pvis.TerminalNode), 'sanity check'
    return self.children[0].node_type
class SubscriptNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.value : pvis.AbstractNode = None
    self.subscript : pvis.AbstractNode = None
class TrueNode(pvis.AbstractNode): pass
class TryStatementNode(pvis.AbstractNode): pass
class TupleNode(pvis.AbstractNode): pass
class TuplePatternNode(pvis.AbstractNode): pass
class TypeNode(pvis.AbstractNode): pass
class TypeConversionNode(pvis.AbstractNode): pass
class TypedDefaultParameterNode(pvis.AbstractNode): pass
class TypedParameterNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.type : pvis.AbstractNode = None
class UnaryOperatorNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.operator : pvis.AbstractNode = None
    self.argument : pvis.AbstractNode = None
class WhileStatementNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.condition : pvis.AbstractNode = None
    self.body : pvis.AbstractNode = None
    self.alternative : pvis.AbstractNode = None
class WildcardImportNode(pvis.AbstractNode): pass
class WithClauseNode(pvis.AbstractNode): pass
class WithItemNode(pvis.AbstractNode): pass
class WithStatementNode(pvis.AbstractNode): pass
class YieldNode(pvis.AbstractNode): pass


NODE_TYPES_CLASSES: Dict[str, pvis.AbstractNode] = {
  'terminal': pvis.TerminalNode,
  '_collection_elements': _CollectionElementsNode,
  '_compound_statement': _CompoundStatementNode,
  '_comprehension_clauses': _ComprehensionClausesNode,
  '_expression_within_for_in_clause': _ExpressionWithinForInClauseNode,
  '_expressions': _ExpressionsNode,
  '_import_list': _ImportListNode,
  '_left_hand_side': _LeftHandSideNode,
  '_parameters': _ParametersNode,
  '_patterns': _PatternsNode,
  '_right_hand_side': _RightHandSideNode,
  '_simple_statement': _SimpleStatementNode,
  '_simple_statements': _SimpleStatementsNode,
  '_statement': _StatementNode,
  '_suite': _SuiteNode,
  'aliased_import': AliasedImportNode,
  'argument_list': ArgumentListNode,
  'assert_statement': AssertStatementNode,
  'assignment': AssignmentNode,
  'attribute': AttributeNode,
  'augmented_assignment': AugmentedAssignmentNode,
  'await': AwaitNode,
  'binary_operator': BinaryOperatorNode,
  'block': BlockNode,
  'boolean_operator': BooleanOperatorNode,
  'break_statement': BreakStatementNode,
  'call': CallNode,
  'chevron': ChevronNode,
  'class_definition': ClassDefinitionNode,
  'comment': CommentNode,
  'comparison_operator': ComparisonOperatorNode,
  'concatenated_string': ConcatenatedStringNode,
  'conditional_expression': ConditionalExpressionNode,
  'continue_statement': ContinueStatementNode,
  'decorated_definition': DecoratedDefinitionNode,
  'decorator': DecoratorNode,
  'default_parameter': DefaultParameterNode,
  'delete_statement': DeleteStatementNode,
  'dictionary': DictionaryNode,
  'dictionary_comprehension': DictionaryComprehensionNode,
  'dictionary_splat': DictionarySplatNode,
  'dictionary_splat_pattern': DictionarySplatPatternNode,
  'dotted_name': DottedNameNode,
  'elif_clause': ElifClauseNode,
  'ellipsis': EllipsisNode,
  'else_clause': ElseClauseNode,
  'escape_interpolation': EscapeInterpolationNode,
  'escape_sequence': EscapeSequenceNode,
  'except_clause': ExceptClauseNode,
  'exec_statement': ExecStatementNode,
  'expression': ExpressionNode,
  'expression_list': ExpressionListNode,
  'expression_statement': ExpressionStatementNode,
  'false': FalseNode,
  'finally_clause': FinallyClauseNode,
  'float': FloatNode,
  'for_in_clause': ForInClauseNode,
  'for_statement': ForStatementNode,
  'format_expression': FormatExpressionNode,
  'format_specifier': FormatSpecifierNode,
  'function_definition': FunctionDefinitionNode,
  'future_import_statement': FutureImportStatementNode,
  'generator_expression': GeneratorExpressionNode,
  'global_statement': GlobalStatementNode,
  'identifier': IdentifierNode,
  'if_clause': IfClauseNode,
  'if_statement': IfStatementNode,
  'import_from_statement': ImportFromStatementNode,
  'import_prefix': ImportPrefixNode,
  'import_statement': ImportStatementNode,
  'integer': IntegerNode,
  'interpolation': InterpolationNode,
  'keyword_argument': KeywordArgumentNode,
  'keyword_identifier': KeywordIdentifierNode,
  'lambda': LambdaNode,
  'lambda_parameters': LambdaParametersNode,
  'lambda_within_for_in_clause': LambdaWithinForInClauseNode,
  'list': ListNode,
  'list_comprehension': ListComprehensionNode,
  'list_pattern': ListPatternNode,
  'list_splat': ListSplatNode,
  'list_splat_pattern': ListSplatPatternNode,
  'module': ModuleNode,
  'named_expression': NamedExpressionNode,
  'none': NoneNode,
  'nonlocal_statement': NonlocalStatementNode,
  'not_escape_sequence': NotEscapeSequenceNode,
  'not_operator': NotOperatorNode,
  'pair': PairNode,
  'parameter': ParameterNode,
  'parameters': ParametersNode,
  'parenthesized_expression': ParenthesizedExpressionNode,
  'parenthesized_list_splat': ParenthesizedListSplatNode,
  'pass_statement': PassStatementNode,
  'pattern': PatternNode,
  'pattern_list': PatternListNode,
  'primary_expression': PrimaryExpressionNode,
  'print_statement': PrintStatementNode,
  'raise_statement': RaiseStatementNode,
  'relative_import': RelativeImportNode,
  'return_statement': ReturnStatementNode,
  'set': SetNode,
  'set_comprehension': SetComprehensionNode,
  'slice': SliceNode,
  'string': StringNode,
  'subscript': SubscriptNode,
  'true': TrueNode,
  'try_statement': TryStatementNode,
  'tuple': TupleNode,
  'tuple_pattern': TuplePatternNode,
  'type': TypeNode,
  'type_conversion': TypeConversionNode,
  'typed_default_parameter': TypedDefaultParameterNode,
  'typed_parameter': TypedParameterNode,
  'unary_operator': UnaryOperatorNode,
  'while_statement': WhileStatementNode,
  'wildcard_import': WildcardImportNode,
  'with_clause': WithClauseNode,
  'with_item': WithItemNode,
  'with_statement': WithStatementNode,
  'yield': YieldNode,
}

NODES_WITH_FIELDS = [
  'attribute',
  'assignment',
  'augmented_assignment',
  'binary_operator',
  'boolean_operator',
  'call',
  'decorated_definition',
  'dictionary_comprehension',
  'elif_clause',
  'else_clause',
  'for_in_clause',
  'function_definition',
  'generator_expression',
  'import_from_statement',
  'lambda',
  'list_comprehension',
  'keyword_argument',
  'named_expression',
  'not_operator',
  'pair',
  'set_comprehension',
  'subscript',
  'typed_parameter',
  'unary_operator',
  'while_statement',
]


class Tree:
  '''
  Class that represents a Python AST.
  This class is compatible with `pvis.Visitor` classes.
  '''
  def __init__(self, root_node: pvis.AbstractNode) -> None:
    self.root_node: pvis.AbstractNode = root_node

  def __repr__(self) -> str:
    return f'Tree({self.root_node.node_type})'

  @classmethod
  def from_gen_ast(cls, ast: list) -> Tree:
    '''
    Construct a Tree from a structure generated by p_grammar.TreeSitterGrammar.generate_simplest_ast
    '''
    def _rec_construct_at(parent_node: pvis.AbstractNode, node: Union[list, str]) -> None:
      # base case: `node` is terminal
      if isinstance(node, str):
        new_node = pvis.TerminalNode(node)
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
    for child in children:
      _rec_construct_at(root_node, child)
    tree = Tree(root_node)
    return tree

  @classmethod
  def from_ts_tree(cls, ts_tree: tree_sitter.Tree) -> Tree:
    '''
    Construct a Tree from a parsed tree-sitter tree
    NOTE we can also use `text` attribute of `ts_tree`

    PARAM nodes_with_fields: list of node types that have fields.
    Special treatment for some nodes.
    These nodes have fields that we want to access as attributes.
    Check `_create_node_with_field` for more details.
    '''

    def _create_StringNode(ts_node: tree_sitter.Node) -> StringNode:
      '''
      Special treatment for `string` nodes in tree-sitter trees.
      We want `string` to be a literal node in our AST. However,
      in tree-sitter trees, `string` nodes are not literal nodes.
      '''
      node = StringNode('string')
      string_content_node = pvis.TerminalNode(ts_node.text.decode('utf-8'))
      node.add_child(string_content_node)
      string_content_node.set_parent(node)
      return node

    def _create_IfStatementNode(ts_node: tree_sitter.Node) -> IfStatementNode:
      '''
      This is a workaround for a bug in the current tree-sitter version.
      The bug: `else_clause` is parsed as a `consequence` field,
      but should be parsed as `alternative` field according to grammar.
      '''
      if_statement_node = IfStatementNode('if_statement')

      # according to grammar, first four children are:
      # 'if', 'condition', ':', 'consequence'
      # and all four must be present
      assert len(ts_node.children) >= 4, 'per grammar: if_statement must have at least 4 children'
      for idx, ts_child in enumerate(ts_node.children[:4]):
        child_node = _rec_build_tree(ts_child)
        if idx == 1:
          if_statement_node.condition = child_node
        elif idx == 3:
          if_statement_node.consequence = child_node
        if_statement_node.add_child(child_node)
        child_node.set_parent(if_statement_node)

      # remaining nodes are `alternative` fields
      # NOTE alternative fields are added to `alternatives` attribute
      for ts_child in ts_node.children[4:]:
        child_node = _rec_build_tree(ts_child)
        if_statement_node.add_child(child_node)
        child_node.set_parent(if_statement_node)
        if_statement_node.alternatives.append(child_node)

      return if_statement_node

    def _create_ForStatementNode(ts_node: tree_sitter.Node) -> ForStatementNode:
      '''
      This is a workaround for a bug in the current tree-sitter version.
      The bug:  `for_statement`s `else_clause` is parsed as
      `body` field. It should be parsed as `alternative`
      according to the grammar.

      TODO async is not supported
      '''
      assert ts_node.children[0].type != 'async', 'async is not supported'
      assert ts_node.children[0].type == 'for', 'sanity check'

      for_statement_node = ForStatementNode('for_statement')

      # according to grammar, first six children are:
      # 'for', 'left', 'in', 'right', ':', 'body'
      for idx, ts_child in enumerate(ts_node.children[:6]):
        child_node = _rec_build_tree(ts_child)
        if idx == 1:
          for_statement_node.left = child_node
        elif idx == 3:
          for_statement_node.right = child_node
        elif idx == 5:
          for_statement_node.body = child_node
        for_statement_node.add_child(child_node)
        child_node.set_parent(for_statement_node)

      # no else_clause
      if len(ts_node.children) == 6:
        return for_statement_node

      # else_clause is present
      # NOTE else_clause is added to `alternative` attribute
      else_clause_node = _rec_build_tree(ts_node.children[6])
      for_statement_node.add_child(else_clause_node)
      else_clause_node.set_parent(for_statement_node)
      for_statement_node.alternative = else_clause_node
      return for_statement_node

    def _create_node_with_field(ts_node: tree_sitter.Node) -> pvis.AbstractNode:
      '''
      Special treatment for some nodes in tree-sitter trees.
      What is special about these nodes? They have fields.
      Their fields must be registered as attributes in their respective
      classes (see `AssignmentNode` for example). This special treatment
      allows us to access fields of these classes as attributes.
      Check `NODES_WITH_FIELDS` for the list of special nodes.

      NOTE TODO in `if_statement`, there are multiple nodes under a single
      field `alternative`. Current implementation does not support it, as it
      will save the last node under `alternative` as an attribute.
      The same issue is true for `comparison_operator`
      and its `operators` field.

      NOTE TODO in order to fix the issue above, we can use the method
      `children_by_field_name`, `child_by_field_name` to set multiple
      nodes under the same field name into a single attribute
      that is a list.
      '''
      # instantiate a special node
      ntype = ts_node.type
      NodeCls = NODE_TYPES_CLASSES[ntype]
      node_wfield = NodeCls(ntype)

      # field names of the special node
      ts_field_names = [ts_node.field_name_for_child(i) for i in range(len(ts_node.children))]
      ts_field_names = [fn for fn in ts_field_names if fn is not None]

      # add children to the node with field
      # register nodes as attributes using `setattr`
      for idx, ts_child in enumerate(ts_node.children):
        child_node = _rec_build_tree(ts_child)
        node_wfield.add_child(child_node)
        child_node.set_parent(node_wfield)

        # set attributes of the special node
        ts_child_field_name = ts_node.field_name_for_child(idx)
        if ts_child_field_name in ts_field_names:
          setattr(node_wfield, ts_child_field_name, child_node)

      return node_wfield

    def _rec_build_tree(ts_node: tree_sitter.Node) -> pvis.AbstractNode:
      '''Construct a tree from a tree-sitter node recursively'''
      # base case: leaf node
      # might be a terminal node, literal node
      if len(ts_node.children) == 0:
        text : str = ts_node.text.decode('utf-8')
        type_ : str = ts_node.type

        # terminal node
        if type_ == text:
          return pvis.TerminalNode(text)

        # literal node
        NodeCls = NODE_TYPES_CLASSES[type_]
        literal_node = NodeCls(type_)
        tnode = pvis.TerminalNode(text)
        literal_node.add_child(tnode)
        tnode.set_parent(literal_node)
        return literal_node

      # special case: string node
      if ts_node.type == 'string':
        string_node = _create_StringNode(ts_node)
        return string_node

      # special case: if_statement node
      if ts_node.type == 'if_statement':
        if_statement_node = _create_IfStatementNode(ts_node)
        return if_statement_node

      # special case: for_statement node
      if ts_node.type == 'for_statement':
        for_statement_node = _create_ForStatementNode(ts_node)
        return for_statement_node

      # special case: nodes with fields
      # NOTE might as well do this for all nodes
      if ts_node.type in NODES_WITH_FIELDS:
        spec_node = _create_node_with_field(ts_node)
        return spec_node

      # general case: non-terminal node
      NodeCls = NODE_TYPES_CLASSES[ts_node.type]
      ntnode = NodeCls(ts_node.type)

      for ts_child in ts_node.children:
        child_node = _rec_build_tree(ts_child)
        ntnode.add_child(child_node)
        child_node.set_parent(ntnode)

      return ntnode

    ts_root_node = ts_tree.root_node
    assert not ts_root_node.has_error, 'tree-sitter tree has error'

    RootNodeCls = NODE_TYPES_CLASSES[ts_root_node.type]
    root_node = RootNodeCls(ts_root_node.type)

    for child in ts_root_node.children:
      child_node = _rec_build_tree(child)
      root_node.add_child(child_node)
      child_node.set_parent(root_node)

    tree = Tree(root_node)
    return tree

  @classmethod
  def from_str(cls, code: str) -> Tree:
    '''
    Construct a Tree from a string
    '''
    parser = p_consts.PARSER_DICT['py']
    ts_tree = parser.parse(bytes(code, 'utf8'))
    tree = Tree.from_ts_tree(ts_tree)
    return tree


class PrettyPrinterForGeneratedCode(pvis.Visitor):
  '''
  Pretty printer that is used for trees generated by
  `p_grammar.TreeSitterGrammar.generate_simplest_ast`.
  `PrettyPrinter` can also be used to pretty print these
  generated trees, but respective `visit_*` methods must be
  implemented in `PrettyPrinter`. The generated trees
  contain hidden nodes as well (e.g. `_suite`, `_statement`).
  '''
  def __init__(self) -> None:
    super().__init__()
    self.indentation_level : int = 0
    self.indentation_size : int = 2

  def indent(self, text: str) -> str:
    self.indentation_level += 1
    code = p_utils.indent(text, self.indentation_level * self.indentation_size)
    self.indentation_level -= 1
    return code

  def default_visit(self, node: pvis.AbstractNode, delimeter: str = ' ') -> str:
    code = ''
    for child in node.children:
      child_code = self.visit(child)
      code += (child_code + delimeter)
    return code.strip()

  def visit_TerminalNode(self, node: pvis.TerminalNode) -> str:
    return node.node_type

  def visit__SuiteNode(self, node: _SuiteNode) -> str:
    code = self.default_visit(node, delimeter='\n')
    code = self.indent(code)
    return '\n' + code


class PrettyPrinter(pvis.Visitor):
  def __init__(self, indent_with: str = '  ') -> None:
    super().__init__()
    # e.g. two spaces
    self.indent_with = indent_with

    # current indentation level
    self.level = 0

    # accumulate lines of generated code
    self.lines : List[str] = []

  def indent(self) -> str:
    '''Return the current indentation string'''
    return self.indent_with * self.level

  def write_line(self, line: str) -> None:
    '''Write a line of code to the output'''
    self.lines.append(self.indent() + line)

  # VISIT METHODS
  def default_visit(self, node: pvis.AbstractNode) -> None:
    print('\n'.join(self.lines))
    raise NotImplementedError(f'visit_{node.__class__.__name__} not implemented')

  def visit_ArgumentListNode(self, node: ArgumentListNode) -> str:
    arguments = ', '.join([self.visit(child) for child in node.get_nt_children()])
    return arguments

  def visit_AssignmentNode(self, node: AssignmentNode) -> str:
    left = self.visit(node.left)
    right = self.visit(node.right)
    return f'{left} = {right}'

  def visit_AttributeNode(self, node: AttributeNode) -> str:
    object_ = self.visit(node.object)
    attribute = self.visit(node.attribute)
    return f'{object_}.{attribute}'

  def visit_AugmentedAssignmentNode(self, node: AugmentedAssignmentNode) -> str:
    left = self.visit(node.left)
    operator = self.visit(node.operator)
    right = self.visit(node.right)
    return f'{left} {operator} {right}'

  def visit_BinaryOperatorNode(self, node: BinaryOperatorNode) -> str:
    left = self.visit(node.left)
    operator = self.visit(node.operator)
    right = self.visit(node.right)
    return f'{left} {operator} {right}'

  def visit_BlockNode(self, node: BlockNode) -> None:
    for stmt in node.children:
      self.visit(stmt)

  def visit_BooleanOperatorNode(self, node: BooleanOperatorNode) -> str:
    left = self.visit(node.left)
    operator = self.visit(node.operator)
    right = self.visit(node.right)
    return f'{left} {operator} {right}'

  def visit_BreakStatementNode(self, node: BreakStatementNode) -> None:
    self.write_line('break')

  def visit_CallNode(self, node: CallNode) -> str:
    function = self.visit(node.function)
    arguments = self.visit(node.arguments)
    return f'{function}({arguments})'

  def visit_ClassDefinitionNode(self, node: ClassDefinitionNode) -> None:
    signature = 'class '
    # according to grammar, first child is `name`
    # and the last child is `body`
    for child in node.children[1:-1]:
      signature += self.visit(child)
    self.write_line(signature)
    self.level += 1
    self.visit(node.children[-1])
    self.level -= 1

  def visit_CommentNode(self, node: CommentNode) -> None:
    self.write_line(f'{node.children[0].node_type}')

  def visit_ComparisonOperatorNode(self, node: ComparisonOperatorNode) -> str:
    '''
    NOTE `comparison_operator` uses a field `operators`.
    There might be multiple comparison operators in a single node.
    In this implementation, we are not using this field.
    '''
    left_node = node.children[0]
    assert left_node.is_nonterminal(), 'left node is expected to be non-terminal'
    left = self.visit(left_node)

    # NOTE operator may span two terminal nodes as in `not in` and `is not`
    rem_ch_queue = node.children[1:]
    while len(rem_ch_queue) > 0:
      operator, right = '', ''

      # at least one operator token is always present
      op_node_first = rem_ch_queue.pop(0)
      assert op_node_first.is_terminal(), 'operator node is expected to be terminal'
      operator = self.visit(op_node_first)

      # second operator token is not always present
      op_node_second = rem_ch_queue.pop(0)
      if op_node_second.is_terminal():
        assert (op_node_first.node_type, op_node_second.node_type) in [('not', 'in'), ('is', 'not')], \
          'operator is expected to be `not in` or `is not`'
        operator += f' {self.visit(op_node_second)}'
        right_node = rem_ch_queue.pop(0)
      else:
        right_node = op_node_second

      assert right_node.is_nonterminal(), 'right node is expected to be non-terminal'

      right = self.visit(right_node)

      # append to the right
      left = f'{left} {operator} {right}'

    return left

  def visit_ConditionalExpressionNode(self, node: ConditionalExpressionNode) -> str:
    assert len(node.get_children()) == 5, 'per grammar: sanity check'
    assert len(node.get_nt_children()) == 3, 'per grammar: sanity check'
    consequence = self.visit(node.get_nt_children()[0])
    condition = self.visit(node.get_nt_children()[1])
    alternative = self.visit(node.get_nt_children()[2])
    return f'{consequence} if {condition} else {alternative}'

  def visit_ContinueStatementNode(self, node: ContinueStatementNode) -> None:
    self.write_line('continue')

  def visit_DecoratedDefinitionNode(self, node: DecoratedDefinitionNode) -> None:
    '''
    According to grammar, `definition` is the last child.
    '''
    assert all(child.is_nonterminal() for child in node.children), 'all children must be non-terminal'
    assert node.definition is node.children[-1], 'per grammar: definition is the last child'
    for dec_node in node.children[:-1]:
      decorator = self.visit(dec_node)
      self.write_line(decorator)
    self.visit(node.definition)

  def visit_DecoratorNode(self, node: DecoratorNode) -> str:
    return f'@{self.visit(node.children[1])}'

  def visit_DeleteStatementNode(self, node: DeleteStatementNode) -> None:
    targets = ', '.join([self.visit(child) for child in node.get_nt_children()])
    self.write_line(f'del {targets}')

  def visit_DictionaryComprehensionNode(self, node: DictionaryComprehensionNode) -> str:
    '''
    Similar to `list_comprehension`
    '''
    nt_children = node.get_nt_children()
    assert len(nt_children) >= 2, 'per grammar: there must be at least two non-terminal children'
    body = self.visit(node.body)
    assert nt_children[0] is node.body, 'per grammar: first non-terminal child is the body'
    clauses = ' '.join([self.visit(child) for child in nt_children[1:]])
    return f'{{{body} {clauses}}}'

  def visit_DictionaryNode(self, node: DictionaryNode) -> str:
    pairs = ', '.join([self.visit(child) for child in node.get_nt_children()])
    return f'{{{pairs}}}'

  def visit_DottedNameNode(self, node: DottedNameNode) -> str:
    return '.'.join([self.visit(child) for child in node.children])

  def visit_ElifClauseNode(self, node: ElifClauseNode) -> None:
    assert len(node.get_nt_children()) == 2, 'per grammar: there must be exactly two non-terminal children'
    cond = self.visit(node.condition)
    self.write_line(f'elif {cond}:')
    self.level += 1
    self.visit(node.consequence)
    self.level -= 1

  def visit_ElseClauseNode(self, node: ElseClauseNode) -> None:
    assert len(node.get_nt_children()) == 1, 'per grammar: there must be exactly one non-terminal child'
    self.write_line('else:')
    self.level += 1
    self.visit(node.body)
    self.level -= 1

  def visit_ExpressionListNode(self, node: ExpressionListNode) -> str:
    expressions = ', '.join([self.visit(child) for child in node.get_nt_children()])
    return expressions

  def visit_ExpressionStatementNode(self, node: ExpressionStatementNode) -> None:
    assert len(node.children) == 1, 'sanity check'
    code = self.visit(node.children[0])
    self.write_line(code)

  def visit_FalseNode(self, node: FalseNode) -> str:
    return 'False'

  def visit_FloatNode(self, node: FloatNode) -> str:
    return node.val()

  def visit_ForInClauseNode(self, node: ForInClauseNode) -> str:
    '''
    TODO async is not supported
    '''
    left = self.visit(node.left)
    right = self.visit(node.right)
    return f'for {left} in {right}'

  def visit_ForStatementNode(self, node: ForStatementNode) -> None:
    '''
    TODO async is not supported
    TODO alternative is not supported
    '''
    left = self.visit(node.left)
    right = self.visit(node.right)
    self.write_line(f'for {left} in {right}:')
    self.level += 1
    self.visit(node.body)
    self.level -= 1
    if node.alternative:
      self.visit(node.alternative)

  def visit_FunctionDefinitionNode(self, node: FunctionDefinitionNode) -> None:
    '''
    TODO `async` is not supported
    '''
    name = self.visit(node.name)
    params = self.visit(node.parameters)
    # return type annotation is optional
    if node.return_type:
      return_type = self.visit(node.return_type)
      self.write_line(f'def {name}{params} -> {return_type}:')
    else:
      self.write_line(f'def {name}{params}:')
    self.level += 1
    self.visit(node.body)
    self.level -= 1

  def visit_GeneratorExpressionNode(self, node: GeneratorExpressionNode) -> str:
    nt_children = node.get_nt_children()
    assert len(nt_children) >= 2, 'per grammar: there must be at least two non-terminal children'
    body = self.visit(node.body)
    assert nt_children[0] is node.body, 'per grammar: first non-terminal child is the body'
    clauses = ' '.join([self.visit(child) for child in nt_children[1:]])
    return f'({body} {clauses})'

  def visit_IdentifierNode(self, node: IdentifierNode) -> str:
    return node.val()

  def visit_IfClauseNode(self, node: IfClauseNode) -> str:
    cond = self.visit(node.children[1])
    return f'if {cond}'

  def visit_IfStatementNode(self, node: IfStatementNode) -> None:
    '''
    Access `alternative` fields by child index.
    Better way to do this is to use field names as attributes (really?)
    '''
    cond = self.visit(node.condition)
    self.write_line(f'if {cond}:')
    self.level += 1
    self.visit(node.consequence)
    self.level -= 1

    # alternatives are the third and later children
    if len(node.get_nt_children()) <= 2:
      return
    for alt in node.get_nt_children()[2:]:
      self.visit(alt)

  def visit_ImportFromStatementNode(self, node: ImportFromStatementNode) -> None:
    module_name = self.visit(node.module_name)
    imports : str = ', '.join([self.visit(child) for child in node.get_nt_children()[1:]])
    code = f'from {module_name} import {imports}'
    self.write_line(code)

  def visit_ImportStatementNode(self, node: ImportStatementNode) -> None:
    nt_children = node.get_nt_children()
    assert len(nt_children) == 1, 'per grammar: there must be exactly one non-terminal child'
    import_list : str = self.visit(nt_children[0])
    self.write_line(f'import {import_list}')

  def visit_IntegerNode(self, node: IntegerNode) -> str:
    return node.val()

  def visit_KeywordArgumentNode(self, node: KeywordArgumentNode) -> str:
    name = self.visit(node.name)
    value = self.visit(node.value)
    return f'{name}={value}'

  def visit_LambdaNode(self, node: LambdaNode) -> str:
    '''
    lambda parameters are optional according to grammar
    '''
    if node.parameters is None:
      params = ''
    else:
      params = f' {self.visit(node.parameters)}'
    body = self.visit(node.body)
    return f'lambda{params}: {body}'

  def visit_LambdaParametersNode(self, node: LambdaParametersNode) -> str:
    params = ', '.join([self.visit(child) for child in node.get_nt_children()])
    return f'{params}'

  def visit_ListComprehensionNode(self, node: ListComprehensionNode) -> str:
    '''
    According to grammar, first and last children are brackets.
    First non-terminal child is the body of the list comprehension.
    Remaining non-terminal children are comprehension clauses.
    '''
    nt_children = node.get_nt_children()
    assert len(nt_children) >= 2, 'per grammar: there must be at least two non-terminal children'
    body = self.visit(node.body)
    assert nt_children[0] is node.body, 'per grammar: first non-terminal child is the body'
    clauses = ' '.join([self.visit(child) for child in nt_children[1:]])
    return f'[{body} {clauses}]'

  def visit_ListNode(self, node: ListNode) -> str:
    elements = ', '.join([self.visit(child) for child in node.get_nt_children() if not isinstance(child, CommentNode)])
    return f'[{elements}]'

  def visit_ListSplatNode(self, node: ListSplatNode) -> str:
    return f'*{self.visit(node.children[1])}'

  def visit_ModuleNode(self, node: ModuleNode) -> str:
    for stmt in node.children:
      self.visit(stmt)
    return '\n'.join(self.lines)

  def visit_NamedExpressionNode(self, node: NamedExpressionNode) -> str:
    name = self.visit(node.name)
    value = self.visit(node.value)
    return f'{name} := {value}'

  def visit_NoneNode(self, node: NoneNode) -> str:
    return 'None'

  def visit_NonlocalStatementNode(self, node: NonlocalStatementNode) -> None:
    names = ', '.join([self.visit(child) for child in node.get_nt_children()])
    self.write_line(f'nonlocal {names}')

  def visit_NotOperatorNode(self, node: NotOperatorNode) -> str:
    argument = self.visit(node.argument)
    return f'not {argument}'

  def visit_PairNode(self, node: PairNode) -> str:
    key = self.visit(node.key)
    value = self.visit(node.value)
    return f'{key}: {value}'

  def visit_ParametersNode(self, node: ParametersNode) -> str:
    params = ', '.join([self.visit(child) for child in node.get_nt_children()])
    return f'({params})'

  def visit_ParenthesizedExpressionNode(self, node: ParenthesizedExpressionNode) -> str:
    assert len(node.children) == 3, 'per grammar: parenthesized expression has 3 children'
    assert node.children[1].is_nonterminal(), 'per grammar: second child is non-terminal'
    return f'({self.visit(node.children[1])})'

  def visit_PassStatementNode(self, node: PassStatementNode) -> None:
    self.write_line('pass')

  def visit_PatternListNode(self, node: PatternListNode) -> str:
    pattern_list = ', '.join([self.visit(child) for child in node.get_nt_children()])
    return f'{pattern_list}'

  def visit_ReturnStatementNode(self, node: ReturnStatementNode) -> None:
    if len(node.get_nt_children()) == 0:
      self.write_line('return')
      return
    assert len(node.get_nt_children()) == 1, 'there must be exactly one return value node'
    return_value = self.visit(node.get_nt_children()[0])
    self.write_line(f'return {return_value}')

  def visit_SetComprehensionNode(self, node: SetComprehensionNode) -> str:
    '''
    Similar to `list_comprehension` and `dictionary_comprehension`
    '''
    nt_children = node.get_nt_children()
    assert len(nt_children) >= 2, 'per grammar: there must be at least two non-terminal children'
    body = self.visit(node.body)
    assert nt_children[0] is node.body, 'per grammar: first non-terminal child is the body'
    clauses = ' '.join([self.visit(child) for child in nt_children[1:]])
    return f'{{{body} {clauses}}}'

  def visit_SetNode(self, node: SetNode) -> str:
    elements = ', '.join([self.visit(child) for child in node.get_nt_children()])
    return f'{{{elements}}}'

  def visit_SliceNode(self, node: SliceNode) -> str:
    '''
    Very tricky one :)
    Need to use `:` as anchors.
    '''
    # first colon is always present
    first_colon_idx = -1
    for idx, child in enumerate(node.children):
      if child.node_type == ':':
        first_colon_idx = idx
        break
    assert first_colon_idx in [0, 1], 'sanity check: first colon is always present'

    # second colon is optional
    second_colon_idx = -1
    for idx, child in enumerate(node.children[first_colon_idx + 1:], start=first_colon_idx + 1):
      if child.node_type == ':':
        second_colon_idx = idx
        break

    # all three are optional
    start, stop, step = '', '', ''

    # start optional is present
    if first_colon_idx == 1:
      assert node.children[0].is_nonterminal(), 'sanity check: start is non-terminal'
      start = self.visit(node.children[0])

    # second colon is missing
    if second_colon_idx == -1:
      # stop optional is present
      if len(node.children) == first_colon_idx + 2:
        assert node.children[first_colon_idx + 1].is_nonterminal(), 'sanity check: stop is non-terminal'
        stop = self.visit(node.children[first_colon_idx + 1])
      return f'{start}:{stop}'

    # second colon is present
    assert second_colon_idx > first_colon_idx, 'sanity check: second colon is after the first colon'

    # stop optional is present
    if second_colon_idx == first_colon_idx + 2:
      assert node.children[first_colon_idx + 1].is_nonterminal(), 'sanity check: stop is non-terminal'
      stop = self.visit(node.children[first_colon_idx + 1])

    # step optional is present
    if len(node.children) == second_colon_idx + 2:
      assert node.children[second_colon_idx + 1].is_nonterminal(), 'sanity check: step is non-terminal'
      step = self.visit(node.children[second_colon_idx + 1])

    return f'{start}:{stop}:{step}'

  def visit_StringNode(self, node: StringNode) -> str:
    return node.val()

  def visit_SubscriptNode(self, node: SubscriptNode) -> str:
    value = self.visit(node.value)
    subscript = self.visit(node.subscript)
    return f'{value}[{subscript}]'

  def visit_TerminalNode(self, node: pvis.TerminalNode) -> str:
    return node.node_type

  def visit_TrueNode(self, node: TrueNode) -> str:
    return 'True'

  def visit_TupleNode(self, node: TupleNode) -> str:
    # tuple with one element
    if len(node.get_nt_children()) == 1:
      return f'({self.visit(node.get_nt_children()[0])},)'
    elements = ', '.join([self.visit(child) for child in node.get_nt_children()])
    return f'({elements})'

  def visit_TuplePatternNode(self, node: TuplePatternNode) -> str:
    patterns = ', '.join([self.visit(child) for child in node.get_nt_children()])
    return f'({patterns})'

  def visit_TypeNode(self, node: TypeNode) -> str:
    return self.visit(node.children[0])

  def visit_TypedParameterNode(self, node: TypedParameterNode) -> str:
    type_ = self.visit(node.type)
    name = self.visit(node.children[0])
    return f'{name}: {type_}'

  def visit_UnaryOperatorNode(self, node: UnaryOperatorNode) -> str:
    operator = self.visit(node.operator)
    operand = self.visit(node.argument)
    return f'{operator}{operand}'

  def visit_WhileStatementNode(self, node: WhileStatementNode) -> None:
    cond = self.visit(node.condition)
    self.write_line(f'while {cond}:')
    self.level += 1
    self.visit(node.body)
    self.level -= 1
    if node.alternative:
      self.visit(node.alternative)

  def visit_WildcardImportNode(self, node: WildcardImportNode) -> str:
    return '*'


class ParametrizableVariablesCollector(pvis.Visitor):
  '''
  Assume that the generated snippet will be a body of a function definition.
  This visitor collects all identifiers that are parametrizable for that function.
  '''

  def __init__(self) -> None:
    super().__init__()

    # list of identifiers that are parametrizable
    self.parametrizable_identifiers : List[str] = []

    # list of all identifiers
    self.all_identifiers : List[str] = []

    # list of identifiers that were assigned a value
    self.initialized_identifiers : List[str] = []

    # context stack
    self.ctx : List[str] = []

  def add_parametrizable_identifier(self, node: IdentifierNode) -> None:
    self.parametrizable_identifiers.append(node.val())

  def add_identifier(self, node: IdentifierNode) -> None:
    self.all_identifiers.append(node.val())

  def add_initialized_identifier(self, node: IdentifierNode) -> None:
    self.initialized_identifiers.append(node.val())

  def is_first_time_seeing(self, node: IdentifierNode) -> bool:
    return node.val() not in self.all_identifiers

  def get_parametrizable_identifiers(self) -> List[str]:
    return self.parametrizable_identifiers

  def is_identifier_built_in_function(self, node: IdentifierNode) -> bool:
    # not a built-in function if appears as an argument
    # L0388: `i, n = (0, len(input))` (input is a built-in function)
    # L0049: how about `chars = defaultdict(list)`
    # L0126: how about `prev = defaultdict(set)`
    if self.ctx and self.ctx[-1] == 'call.arguments':
      return False
    # L0749: idx = boundaries.index(max(boundaries, key=len))
    #                                                   ^^^
    if self.ctx and self.ctx[-1] == 'keyword_argument.value':
      # the value of a keyword argument might be a generated identifier
      # such as `id_evw`
      if node.val().startswith('id_'):
        return False
      # by default, all values are considered as built-in or defined function names
      return True
    return node.val() in p_consts.PY_BUILT_IN_FUNCTIONS

  def is_identifier_built_in_module(self, node: IdentifierNode) -> bool:
    # not a built-in module if appears as an argument
    # L0167: `i, j = 1, len(numbers)` (numbers is a built-in module)
    if self.ctx and self.ctx[-1] == 'call.arguments':
      return False
    # L0681: `s = {c for c in time if c != ':'}` (time is a built-in module)
    if self.ctx and self.ctx[-1] == 'for_in_clause.right':
      return False
    return node.val() in p_consts.PY_BUILT_IN_MODULES

  # VISIT METHODS
  def visit_IdentifierNode(self, node: IdentifierNode) -> None:
    # if we already have seen this identifier, skip
    # because we already have decided what to do with this identifier
    if not self.is_first_time_seeing(node):
      return

    # add to all identifiers list
    self.add_identifier(node)

    # check if the identifier is a variable that is being assigned a value
    # i.e. it appears on the left-hand side of an assignment
    if self.ctx and self.ctx[-1] == 'assignment.left':
      self.add_initialized_identifier(node)
      return
    # similar to assignment
    if self.ctx and self.ctx[-1] == 'named_expression.name':
      self.add_initialized_identifier(node)
      return
    # `for a in nums: pass` - `a` is initialized
    if self.ctx and self.ctx[-1] == 'for_statement.left':
      self.add_initialized_identifier(node)
      return
    # `[None for a in nums]` - `a` is initialized
    if self.ctx and self.ctx[-1] == 'for_in_clause.left':
      self.add_initialized_identifier(node)
      return
    # this in an inner function, and all of its parameters are initialized
    if self.ctx and self.ctx[-1] == 'function_definition.parameters':
      self.add_initialized_identifier(node)
      return
    # lambda fn is similar to inner fn, and all of its parameters are initialized
    if self.ctx and self.ctx[-1] == 'lambda.parameters':
      self.add_initialized_identifier(node)
      return
    # whatever is inside `defaultdict` is initialized
    # L1722: `mp = defaultdict(Counter)`
    if self.ctx and self.ctx[-1] == 'defaultdict.arguments':
      self.add_initialized_identifier(node)
      return
    # fixes L0049: `chars = defaultdict(list)`
    if self.is_identifier_built_in_function(node):
      self.add_initialized_identifier(node)
      return
    if self.is_identifier_built_in_module(node):
      self.add_initialized_identifier(node)
      return

    # an identifier is parametrizable
    # 1. seeing it for the first time
    # 2. if it is not being assigned a value
    self.add_parametrizable_identifier(node)

  def visit_AttributeNode(self, node: AttributeNode) -> None:
    '''
    Do not visit `node.attribute`:
    1. it is a method name (this is actually handled by self.visit_CallNode)
    '''
    self.ctx.append('attribute.object')
    self.visit(node.object)
    self.ctx.pop()

  def visit_AssignmentNode(self, node: AssignmentNode) -> None:
    self.ctx.append('assignment.right')
    self.visit(node.right)
    self.ctx.pop()

    self.ctx.append('assignment.left')
    self.visit(node.left)
    self.ctx.pop()

  def visit_CallNode(self, node: CallNode) -> None:
    '''
    Both of these examples are CallNode's:
    1. max(a,b)
    2. a.max(b)

    In (1), we assume `max` is defined in the global scope.
    That's why we care about the parameters of `max` only.

    In (2), we assume `max` is defined in the object `a`.
    We consider both `a` and `b` as parametrizable variables.
    '''
    if isinstance(node.function, IdentifierNode):
      if node.function.val() == 'defaultdict':
        self.ctx.append('defaultdict.arguments')
        self.visit(node.arguments)
        self.ctx.pop()
      elif node.function.val() == 'map':
        self.ctx.append('map.arguments')
        self.visit(node.arguments)
        self.ctx.pop()
      else:
        self.ctx.append('call.arguments')
        self.visit(node.arguments)
        self.ctx.pop()
    elif isinstance(node.function, AttributeNode):
      self.visit(node.function)
      self.visit(node.arguments)
    else:
      raise ValueError('unknown function type')

  def visit_DecoratorNode(self, node: DecoratorNode) -> None:
    '''Do not visit anything'''

  def visit_DictionaryComprehensionNode(self, node: DictionaryComprehensionNode) -> None:
    '''
    Treat identical to ListComprehensionNode
    '''
    # we will modify this list, that's why we need a slice
    clauses = node.get_nt_children()[:]
    # keep only the clauses in the parsed order
    clauses.remove(node.body)

    # clauses are visited in sequence
    for clause in clauses:
      self.ctx.append('dictionary_comprehension.clause')
      self.visit(clause)
      self.ctx.pop()

    # body is visited last
    self.ctx.append('dictionary_comprehension.body')
    self.visit(node.body)
    self.ctx.pop()

  def visit_ForInClauseNode(self, node: ForInClauseNode) -> None:
    self.ctx.append('for_in_clause.right')
    self.visit(node.right)
    self.ctx.pop()

    self.ctx.append('for_in_clause.left')
    self.visit(node.left)
    self.ctx.pop()

  def visit_ForStatementNode(self, node: ForStatementNode) -> None:
    self.ctx.append('for_statement.left')
    self.visit(node.left)
    self.ctx.pop()

    self.ctx.append('for_statement.right')
    self.visit(node.right)
    self.ctx.pop()

    self.ctx.append('for_statement.body')
    self.visit(node.body)
    self.ctx.pop()

  def visit_FunctionDefinitionNode(self, node: FunctionDefinitionNode) -> None:
    '''
    Inner functions may use parametrized variables as in L0022.
    '''
    self.ctx.append('function_definition.parameters')
    self.visit(node.parameters)
    self.ctx.pop()

    self.ctx.append('function_definition.body')
    self.visit(node.body)
    self.ctx.pop()

  def visit_GeneratorExpressionNode(self, node: GeneratorExpressionNode) -> None:
    '''
    Treat identical to ListComprehensionNode
    '''
    # we will modify this list, that's why we need a slice
    clauses = node.get_nt_children()[:]
    # keep only the clauses in the parsed order
    clauses.remove(node.body)

    # clauses are visited in sequence
    for clause in clauses:
      self.ctx.append('generator_expression.clause')
      self.visit(clause)
      self.ctx.pop()

    # body is visited last
    self.ctx.append('generator_expression.body')
    self.visit(node.body)
    self.ctx.pop()

  def visit_ImportFromStatementNode(self, node: ImportFromStatementNode) -> None:
    '''Do not visit anything'''

  def visit_ImportStatementNode(self, node: ImportStatementNode) -> None:
    '''Do not visit anything'''

  def visit_KeywordArgumentNode(self, node: KeywordArgumentNode) -> None:
    '''Do not visit `name`'''
    self.ctx.append('keyword_argument.value')
    self.visit(node.value)
    self.ctx.pop()

  def visit_LambdaNode(self, node: LambdaNode) -> None:
    '''
    Treat as an inner function.
    '''
    # lambda parameters are optional per grammar
    if node.parameters is not None:
      self.ctx.append('lambda.parameters')
      self.visit(node.parameters)
      self.ctx.pop()

    self.ctx.append('lambda.body')
    self.visit(node.body)
    self.ctx.pop()

  def visit_ListComprehensionNode(self, node: ListComprehensionNode) -> None:
    '''
    This is very tricky. The following implementation is based on intuition
    and some hand testing. It might not be correct. Refer to
    https://docs.python.org/3/reference/expressions.html#displays-for-lists-sets-and-dictionaries
    for more details on how list comprehensions are executed.

    One thing for sure is that the body is executed last.
    Remaining `if` and `for` clauses are executed in "some" order.
    Currently, we are visiting the clauses in the order they appear in the code.
    '''
    # we will modify this list, that's why we need a slice
    clauses = node.get_nt_children()[:]
    # keep only the clauses in the parsed order
    clauses.remove(node.body)

    # clauses are visited in sequence
    for clause in clauses:
      self.ctx.append('list_comprehension.clause')
      self.visit(clause)
      self.ctx.pop()

    # body is visited last
    self.ctx.append('list_comprehension.body')
    self.visit(node.body)
    self.ctx.pop()

  def visit_ModuleNode(self, node: ModuleNode) -> None:
    '''
    We want to visit the `function_definition` nodes last,
    since they might use variables out of their scope.

    `decorated_definition` are function definitions with a decorator.
    '''
    # we will modify this list, that's why we need a slice
    children = node.get_nt_children()[:]

    # Separate function_definition nodes from other nodes
    fn_dfns = [ch for ch in children
               if isinstance(ch, (FunctionDefinitionNode, DecoratedDefinitionNode))]
    other_nodes = [ch for ch in children
                   if not isinstance(ch, (FunctionDefinitionNode, DecoratedDefinitionNode))]

    # Concatenate other nodes with function_definition nodes at the end
    children = other_nodes + fn_dfns

    for child in children:
      self.visit(child)

  def visit_NamedExpressionNode(self, node: NamedExpressionNode) -> None:
    '''Similar to `AssignmentNode`'''
    self.ctx.append('named_expression.value')
    self.visit(node.value)
    self.ctx.pop()

    self.ctx.append('named_expression.name')
    self.visit(node.name)
    self.ctx.pop()

  def visit_SetComprehensionNode(self, node: SetComprehensionNode) -> None:
    '''
    Treat identical to ListComprehensionNode
    '''
    # we will modify this list, that's why we need a slice
    clauses = node.get_nt_children()[:]
    # keep only the clauses in the parsed order
    clauses.remove(node.body)

    # clauses are visited in sequence
    for clause in clauses:
      self.ctx.append('set_comprehension.clause')
      self.visit(clause)
      self.ctx.pop()

    # body is visited last
    self.ctx.append('set_comprehension.body')
    self.visit(node.body)
    self.ctx.pop()

  def visit_SubscriptNode(self, node: SubscriptNode) -> None:
    self.ctx.append('subscript.subscript')
    self.visit(node.subscript)
    self.ctx.pop()

    self.ctx.append('subscript.value')
    self.visit(node.value)
    self.ctx.pop()

  def visit_TypedParameterNode(self, node: TypedParameterNode) -> None:
    '''
    Do not visit the field `type`.
    Visit just the identifier, which is the first child according to grammar.
    '''
    self.visit(node.children[0])

  # API
  @classmethod
  def get_paramable_ids(cls, snippet: str) -> List[str]:
    '''
    Get all identifiers that are parametrizable for the given snippet.
    The snippet is expected to be a body of a function definition.
    '''
    src_parser = p_consts.PARSER_DICT['py']
    ts_tree = src_parser.parse(bytes(snippet, 'utf-8'))
    tree = Tree.from_ts_tree(ts_tree)
    param_collector = cls()
    param_collector.visit(tree.root_node)
    parametrizable_identifiers = param_collector.get_parametrizable_identifiers()
    return parametrizable_identifiers


class LogStatementInserter(pvis.Visitor):
  '''
  Assume that the LogStatementInserter works on a test script,
  which contains a test function, a tested function (f_gold), and a test function invocation.
  The LogStatementInserter works on the tested function (f_gold).
  '''

  def __init__(self, function_name: str):
    super().__init__()

    # name of the function that we are inserting print statements into
    # this function must appear at the top level of the script
    self.function_name = function_name

    # counters for control-flow statements
    self.if_counter = 0
    self.elif_counter = 0
    self.else_counter = 0
    self.for_counter = 0
    self.while_counter = 0

  # NODE BUILDER METHODS
  def build_ArgumentListNode(self, args: List[pvis.AbstractNode]) -> ArgumentListNode:
    '''
    print(json.dumps(arg, indent=2))
                    ^^^^^^^^^^^^^^^
    argument_list
      *
      *
    '''

    _SUPPORTED_ARG_TYPES = [
      BinaryOperatorNode,
      CallNode,
      ExpressionListNode,
      FloatNode,
      IdentifierNode,
      IntegerNode,
      KeywordArgumentNode,
      ListNode,
      StringNode,
      SubscriptNode,
      UnaryOperatorNode,
    ]
    for arg in args:
      assert isinstance(arg, tuple(_SUPPORTED_ARG_TYPES)), f'Unsupported argument type: {type(arg)}'

    # level 0
    argument_list = ArgumentListNode('argument_list')

    # level 1
    open_par = pvis.TerminalNode('(')
    argument_list.add_child(open_par)
    open_par.set_parent(argument_list)

    for idx, arg in enumerate(args):
      argument_list.add_child(arg)
      arg.set_parent(argument_list)

      # add comma if not the last argument
      if idx != len(args) - 1:
        comma = pvis.TerminalNode(',')
        argument_list.add_child(comma)
        comma.set_parent(argument_list)

    clos_par = pvis.TerminalNode(')')
    argument_list.add_child(clos_par)
    clos_par.set_parent(argument_list)

    return argument_list

  def build_AttributeNode(self, obj: str, attr: str) -> AttributeNode:
    '''
    print(json.dumps(arg, indent=2))
          ^^^^^^^^^^

    attribute
      object: identifier1 'json'
      attribute: identifier2 'dumps'
    '''
    assert isinstance(obj, str), 'obj must be a string'
    assert isinstance(attr, str), 'attr must be a string'

    # level 0
    attribute = AttributeNode('attribute')

    # level 1
    identifier1 = self.build_IdentifierNode(obj)
    attribute.object = identifier1
    attribute.add_child(identifier1)
    identifier1.set_parent(attribute)

    identifier2 = self.build_IdentifierNode(attr)
    attribute.attribute = identifier2
    attribute.add_child(identifier2)
    identifier2.set_parent(attribute)

    return attribute

  def build_CallNode(self, fname: pvis.AbstractNode, argument_list: ArgumentListNode) -> CallNode:
    '''
    call
      function: *
      arguments: *
    '''
    assert isinstance(fname, (IdentifierNode, AttributeNode)), f'unsupported function name type {type(fname)}'
    assert isinstance(argument_list, ArgumentListNode), 'argument_list must be an ArgumentListNode'

    # level 0
    call = CallNode('call')

    # level 1
    call.function = fname
    call.add_child(fname)
    fname.set_parent(call)

    call.arguments = argument_list
    call.add_child(argument_list)
    argument_list.set_parent(call)

    return call

  def build_IdentifierNode(self, val: str) -> IdentifierNode:
    assert isinstance(val, str), 'val must be a string'
    identifier = IdentifierNode('identifier')
    terminal = pvis.TerminalNode(val)
    identifier.add_child(terminal)
    terminal.set_parent(identifier)
    return identifier

  def build_IntegerNode(self, val: Union[str, int]) -> IntegerNode:
    assert isinstance(val, (str, int)), 'val must be a string or an integer'
    integer = IntegerNode('integer')
    terminal = pvis.TerminalNode(val if isinstance(val, str) else str(val))
    integer.add_child(terminal)
    terminal.set_parent(integer)
    return integer

  def build_ImportStatementNode(self, module_name: str) -> ImportStatementNode:
    '''
    import json

    import_statement
      name: dotted_name
        identifier 'json'
    '''
    assert isinstance(module_name, str), 'module_name must be a string'

    # level 0
    import_statement = ImportStatementNode('import_statement')

    # level 1
    dotted_name = DottedNameNode('dotted_name')
    # imp_statement.name = dotted_name  # not required
    import_statement.add_child(dotted_name)
    dotted_name.set_parent(import_statement)

    # level 2
    identifier = self.build_IdentifierNode(module_name)
    dotted_name.add_child(identifier)
    identifier.set_parent(dotted_name)

    return import_statement

  def build_KeywordArgumentNode(self, name: str, value: pvis.AbstractNode) -> KeywordArgumentNode:
    '''
    print(json.dumps(arg, indent=2))
                          ^^^^^^^^
    keyword_argument
      name: identifier
      value: integer
    '''

    _SUPPORTED_VALUE_TYPES = [
      IntegerNode,
      TrueNode,
    ]

    assert isinstance(name, str), 'name must be a string'
    assert isinstance(value, tuple(_SUPPORTED_VALUE_TYPES)), f'Unsupported value type: {type(value)}'

    # level 0
    keyword_argument = KeywordArgumentNode('keyword_argument')

    # level 1
    identifier = self.build_IdentifierNode(name)
    keyword_argument.name = identifier
    keyword_argument.add_child(identifier)
    identifier.set_parent(keyword_argument)

    keyword_argument.value = value
    keyword_argument.add_child(value)
    value.set_parent(keyword_argument)

    return keyword_argument

  def build_ListNode(self, elements: List[pvis.AbstractNode]) -> ListNode:
    '''
    [1, 2, 3]

    list
      *
      *
    '''
    _SUPPORTED_ELEMENT_TYPES = [
      IdentifierNode,
      IntegerNode,
    ]
    for elem in elements:
      assert isinstance(elem, tuple(_SUPPORTED_ELEMENT_TYPES)), f'Unsupported element type: {type(elem)}'

    # level 0
    list_node = ListNode('list')

    # level 1
    open_br = pvis.TerminalNode('[')
    list_node.add_child(open_br)
    open_br.set_parent(list_node)

    for idx, elem in enumerate(elements):
      list_node.add_child(elem)
      elem.set_parent(list_node)

      # add comma if not the last element
      if idx != len(elements) - 1:
        comma = pvis.TerminalNode(',')
        list_node.add_child(comma)
        comma.set_parent(list_node)

    clos_br = pvis.TerminalNode(']')
    list_node.add_child(clos_br)
    clos_br.set_parent(list_node)

    return list_node

  def build_StringNode(self, val: str) -> StringNode:
    assert isinstance(val, str), 'val must be a string'
    string = StringNode('string')
    terminal = pvis.TerminalNode(f"'{val}'")
    string.add_child(terminal)
    terminal.set_parent(string)
    return string

  def build_TrueNode(self) -> TrueNode:
    true = TrueNode('true')
    terminal = pvis.TerminalNode('True')
    true.add_child(terminal)
    terminal.set_parent(true)
    return true

  # LOG STATEMENT BUILDER METHOD
  def build_ArgLogStatement(self, arg: pvis.AbstractNode) -> ExpressionStatementNode:
    '''
    Build a print statement with the given argument where `arg`
    can be any `AbstractNode` instance (as long as it respects grammar).

    PIREL_LOG_OBJ_FN_NAME(arg)

    expression_statement
      call
        function: identifier 'PIREL_LOG_OBJ_FN_NAME'
        arguments: argument_list
          'arg'
    '''
    _SUPPORTED_TYPES = [
      BinaryOperatorNode,
      CallNode,
      ExpressionListNode,
      FloatNode,
      IdentifierNode,
      IntegerNode,
      ListNode,
      StringNode,
      SubscriptNode,
      UnaryOperatorNode,
    ]

    assert isinstance(arg, tuple(_SUPPORTED_TYPES)), f'Unsupported argument type: {type(arg)}'

    # build bottom-up
    argument_list = self.build_ArgumentListNode([arg])
    call = self.build_CallNode(self.build_IdentifierNode(p_consts.PIREL_LOG_OBJ_FN_NAME), argument_list)

    expression_statement = ExpressionStatementNode('expression_statement')
    expression_statement.add_child(call)
    call.set_parent(expression_statement)

    return expression_statement

  # VISIT METHODS
  def visit_BlockNode(self, node: BlockNode) -> None:
    '''
    Insert log statements after assignment statements.
    Assignment appear only under block nodes.
    '''
    idx = 0
    while idx < len(node.children):
      child = node.children[idx]

      if child.is_terminal():
        idx += 1
        continue

      # insert log statement before return_statement
      if isinstance(child, ReturnStatementNode):

        # no return value
        if len(child.children) == 1:
          assert child.children[0].is_terminal(), 'return statement has one child'
          assert child.children[0].node_type == 'return', 'return statement has one child'
          idx += 1
          continue

        # return value
        assert len(child.children) == 2, 'return statement has two children'
        assert child.children[0].is_terminal(), 'first child is terminal'
        assert child.children[0].node_type == 'return', 'first child is terminal `return`'
        assert child.children[1].is_nonterminal(), 'second child is non-terminal'
        return_val = child.children[1]

        # NOTE ideally make a deepcopy of return_val
        # but since pretty printer just needs references to children,
        # we can just use the reference
        log_statement = self.build_ArgLogStatement(return_val)
        node.children.insert(idx, log_statement)

        # since we are not doing a deepcopy, setting the parent
        # will break the tree structure
        # log_statement.set_parent(node)
        idx += 2
        continue

      # visit the child
      self.visit(child)

      # check if child is a top-level node for assignment
      if not isinstance(child, ExpressionStatementNode):
        idx += 1
        continue

      aie = AssignedIdentifierExtractor()
      aie.visit(child)
      assigned_identifiers = aie.get_assigned_identifiers()
      assert len(assigned_identifiers) <= 1, 'currently support only one assigned identifier'

      if len(assigned_identifiers) == 0:
        idx += 1
        continue

      ai = assigned_identifiers[0]

      # build and insert log statement
      arg = self.build_IdentifierNode(ai)
      log_statement = self.build_ArgLogStatement(arg)
      node.children.insert(idx + 1, log_statement)
      log_statement.set_parent(node)
      idx += 1

  def visit_ElifClauseNode(self, node: ElifClauseNode) -> None:
    '''
    Insert print statements at the beginning of the elif statement.
    '''
    for child in node.get_nt_children():
      self.visit(child)
    log_statement = self.build_ArgLogStatement(self.build_IntegerNode(self.elif_counter))
    self.elif_counter += 1
    node.consequence.children.insert(0, log_statement)

  def visit_ElseClauseNode(self, node: ElseClauseNode) -> None:
    '''
    Insert print statements at the beginning of the else statement.
    '''
    for child in node.get_nt_children():
      self.visit(child)
    log_statement = self.build_ArgLogStatement(self.build_IntegerNode(self.else_counter))
    self.else_counter += 1
    node.body.children.insert(0, log_statement)

  def visit_ForStatementNode(self, node: ForStatementNode) -> None:
    '''
    Insert print statements at the beginning of the for statement.
    '''
    for child in node.get_nt_children():
      self.visit(child)
    log_statement = self.build_ArgLogStatement(self.build_IntegerNode(self.for_counter))
    self.for_counter += 1
    node.body.children.insert(0, log_statement)

  def visit_FunctionDefinitionNode(self, node: FunctionDefinitionNode) -> None:
    '''
    Insert import statement at the beginning of the function.
    Ideally, this visit method is executed only once.
    '''
    self.visit(node.body)

  def visit_IfStatementNode(self, node: IfStatementNode) -> None:
    '''
    Insert print statements at the beginning of the if statement.
    '''
    for child in node.get_nt_children():
      self.visit(child)
    log_statement = self.build_ArgLogStatement(self.build_IntegerNode(self.if_counter))
    self.if_counter += 1
    node.consequence.children.insert(0, log_statement)

  def visit_ModuleNode(self, node: ModuleNode) -> None:
    '''
    Given a top-level `module` node, find the function definition
    with the name `self.function_name` and visit it.
    '''
    function_definitions = [child for child in node.children if isinstance(child, FunctionDefinitionNode)]
    assert len(function_definitions), 'no function definitions found'
    fgold_fns = [fn for fn in function_definitions if fn.name.val() == self.function_name]
    assert len(fgold_fns) > 0, 'broken precondition: f_gold function not found'
    assert len(fgold_fns) == 1, 'broken precondition: multiple f_gold functions found'
    fgold_fn = fgold_fns[0]
    self.visit(fgold_fn)

  def visit_WhileStatementNode(self, node: WhileStatementNode) -> None:
    '''
    Insert print statements at the beginning of the while statement.
    '''
    for child in node.get_nt_children():
      self.visit(child)
    log_statement = self.build_ArgLogStatement(self.build_IntegerNode(self.while_counter))
    self.while_counter += 1
    node.body.children.insert(0, log_statement)

  @classmethod
  def insert_log_statements(cls, test_script_str: str) -> str:
    '''
    Insert log statements into the test script.
    The test script is expected to be a body of a function definition.
    '''
    src_parser = p_consts.PARSER_DICT['py']
    ts_tree = src_parser.parse(bytes(test_script_str, 'utf-8'))
    tree = Tree.from_ts_tree(ts_tree)
    inserter = cls(function_name='f_gold')
    inserter.visit(tree.root_node)
    pretty_printer = PrettyPrinter(indent_with='    ')
    code = pretty_printer.visit(tree.root_node)
    return code.strip()


class LogStatementsIndexer(pvis.Visitor):
  '''
  Index all invocations of myexactlog() and print()
  by adding an index as a first argument to the function call.
  This is used for precisely locating statements that are
  responsible for semantic errors.
  '''
  def __init__(self, function_name: str):
    super().__init__()

    # name of the function that contains the functions that we need
    # this function must appear at the top level of the script
    self.function_name = function_name

    # log statements counter
    self.counter = 1

  # NODE BUILDER METHODS
  def build_IntegerNode(self, val: Union[str, int]) -> IntegerNode:
    assert isinstance(val, (str, int)), 'val must be a string or an integer'
    integer = IntegerNode('integer')
    terminal = pvis.TerminalNode(val if isinstance(val, str) else str(val))
    integer.add_child(terminal)
    terminal.set_parent(integer)
    return integer

  # VISIT METHODS
  def visit_ArgumentListNode(self, node: ArgumentListNode) -> None:
    '''
    Visit the argument list and add an index as the first argument.
    '''
    # parent must be CallNode
    parent = node.get_parent()
    if not isinstance(parent, CallNode):
      return

    # function name must be IdentifierNode
    function_name = parent.function
    if not isinstance(function_name, IdentifierNode):
      return

    # function name must be one of ['myexactlog', 'print']
    fname_ter = function_name.get_children()[0].node_type
    if fname_ter not in ['myexactlog', 'print']:
      return

    # build the index argument
    index_arg = self.build_IntegerNode(self.counter)
    self.counter += 1

    # insert the index argument at the beginning of the list
    # NOTE actually, also need to insert a comma,
    # but the PrettyPrinter can handle this.
    node.children.insert(1, index_arg)
    index_arg.set_parent(node)

  def visit_ModuleNode(self, node: ModuleNode) -> None:
    '''
    Given a top-level `module` node, find the function definition
    with the name `self.function_name` and visit it.
    '''
    function_definitions = [child for child in node.children if isinstance(child, FunctionDefinitionNode)]
    assert len(function_definitions), 'no function definitions found'
    fgold_fns = [fn for fn in function_definitions if fn.name.val() == self.function_name]
    assert len(fgold_fns) > 0, 'broken precondition: f_gold function not found'
    assert len(fgold_fns) == 1, 'broken precondition: multiple f_gold functions found'
    fgold_fn = fgold_fns[0]
    self.visit(fgold_fn)

  @classmethod
  def index_log_statements(cls, test_script_str: str) -> str:
    '''
    Index log statements in the test script.
    '''
    src_parser = p_consts.PARSER_DICT['py']
    ts_tree = src_parser.parse(bytes(test_script_str, 'utf-8'))
    tree = Tree.from_ts_tree(ts_tree)
    indexer = cls(function_name='f_gold')
    indexer.visit(tree.root_node)
    pretty_printer = PrettyPrinter(indent_with='    ')
    code = pretty_printer.visit(tree.root_node)
    return code.strip()


class AssignedIdentifierExtractor(pvis.Visitor):
  '''
  Given the left hand side of an assignment statement, this visitor
  extracts the identifiers that were assigned a value.
  '''
  def __init__(self):
    super().__init__()
    self.assigned_identifiers : List[str] = []

  def add_assigned_identifier(self, lit: str) -> None:
    self.assigned_identifiers.append(lit)

  def get_assigned_identifiers(self) -> List[str]:
    return self.assigned_identifiers

  # VISIT METHODS
  def default_visit(self, node):
    raise NotImplementedError(f'visit_{node.__class__.__name__} is not implemented')

  def visit_AssignmentNode(self, node: AssignmentNode) -> None:
    '''
    We care only about the left hand side.
    '''
    self.visit(node.left)

  def visit_AttributeNode(self, node: AttributeNode) -> None:
    '''
    chars.remove(s[i])
    ^^^^^
    '''
    assert isinstance(node.object, IdentifierNode), 'sanity check'
    self.add_assigned_identifier(node.object.val())

  def visit_AugmentedAssignmentNode(self, node: AugmentedAssignmentNode) -> None:
    '''
    We care only about the left hand side.
    '''
    self.visit(node.left)

  def visit_CallNode(self, node: CallNode) -> None:
    '''
    chars.remove(s[i])
    ^^^^^
    '''
    if isinstance(node.function, AttributeNode):
      self.visit(node.function)

  def visit_ExpressionStatementNode(self, node: ExpressionStatementNode) -> None:
    '''
    Extract the assigned identifiers from the expression statement node.

    expression_statement: $ => choice(
      $.expression,
      seq(commaSep1($.expression), optional(',')),
      $.assignment,
      $.augmented_assignment,
      $.yield
    ),
    '''
    _ASSIGNMENT_RELATED_NODES = [
      AssignmentNode,
      AugmentedAssignmentNode,
      CallNode,
    ]

    nt_children = node.get_nt_children()
    assert len(nt_children) == 1, 'sanity check: expression statement has one child'
    child = nt_children[0]

    # visit only the following children of expression_statement
    if isinstance(child, tuple(_ASSIGNMENT_RELATED_NODES)):
      self.visit(child)

  def visit_IdentifierNode(self, node: IdentifierNode) -> None:
    self.add_assigned_identifier(node.val())

  def visit_SubscriptNode(self, node: SubscriptNode) -> None:
    # base case: if the subscript is an identifier
    if isinstance(node.value, IdentifierNode):
      self.add_assigned_identifier(node.value.val())
      return
    self.visit(node.value)


class BreakStatementInserter(pvis.Visitor):
  '''
  Insert a break statement at the end of each loop.
  This visitor is used in pre-context extraction.
  '''
  # VISIT METHODS
  def visit_WhileStatementNode(self, node: WhileStatementNode) -> None:
    # visit the body
    self.visit(node.body)

    # insert break statement
    break_statement = BreakStatementNode('break_statement')
    node.body.children.append(break_statement)
    break_statement.set_parent(node.body)

  def visit_ForStatementNode(self, node: ForStatementNode) -> None:
    # visit the body
    self.visit(node.body)

    # insert break statement
    break_statement = BreakStatementNode('break_statement')
    node.body.children.append(break_statement)
    break_statement.set_parent(node.body)


class StatementNodeSimplifier(pvis.Visitor):
  '''
  This visitor simplifies the statement nodes.
  If a statement node is a compound statement (involves BlockNode as a child),
  then replace all children under its block with a PassStatementNode.
  '''
  # VISIT METHODS
  def visit_BlockNode(self, node: BlockNode) -> None:
    # replace all children with a pass statement
    pass_statement_node = PassStatementNode.build()
    node.children = [pass_statement_node]
    pass_statement_node.set_parent(node)


class DefinedFunctionNameExtractor(pvis.Visitor):
  '''
  Given a Python script, extracts all names of the functions
  that are defined in it.
  '''
  def __init__(self):
    super().__init__()
    self.defined_fn_names : List[str] = []

  def add_function_name(self, name: str) -> None:
    '''
    Add a function name to the list of defined function names.
    '''
    if name not in self.defined_fn_names:
      self.defined_fn_names.append(name)

  # VISIT METHODS
  def visit_FunctionDefinitionNode(self, node: FunctionDefinitionNode) -> None:
    '''
    Extract the name of the function definition.
    '''
    assert isinstance(node.name, IdentifierNode), 'function name must be an IdentifierNode'
    self.add_function_name(node.name.val())
    for child in node.children:
      self.visit(child)

  @classmethod
  def get_defined_function_names(cls, snippet: str) -> List[str]:
    '''
    Get all defined function names from the given snippet.
    The snippet is expected to be a body of a Python script.
    '''
    src_parser = p_consts.PARSER_DICT['py']
    ts_tree = src_parser.parse(bytes(snippet, 'utf-8'))
    tree = Tree.from_ts_tree(ts_tree)
    extractor = cls()
    extractor.visit(tree.root_node)
    return extractor.defined_fn_names


class FunctionInvocationReplacer(pvis.Visitor):
  '''
  Replace a list of given function invocations with `secret_fun_4071()`
  For example, if the following script:
  ```
  def f_gold(a, b):
      if a > b:
          return f_gold(a - 1, b)
      return 0
  ```
  can be replaced with:
  ```
  def f_gold(a, b):
      if a > b:
          return secret_fun_4071()
      return 0
  ```
  This visitor is used in rule validation.
  '''
  def __init__(self, function_names: List[str]):
    super().__init__()
    self.function_names = function_names

  # VISIT METHODS
  def visit_CallNode(self, node: CallNode) -> None:
    '''
    If there is a list of nested calls, consider the outermost one.
    '''
    fn_name_id = node.function

    # function name must be an IdentifierNode (i.e. not a method call)
    if not isinstance(fn_name_id, IdentifierNode):
      return

    # function name must be in the list of function names
    if fn_name_id.val() not in self.function_names:
      return

    # replace the function name with `secret_fun_4071()`
    secret_fn_name = IdentifierNode.build(p_consts.GENERIC_SECRET_FN)
    secret_fn_args = ArgumentListNode.build([])  # no arguments
    node.function = secret_fn_name
    node.arguments = secret_fn_args
    node.children = [secret_fn_name, secret_fn_args]
    secret_fn_name.set_parent(node)
    secret_fn_args.set_parent(node)

  @classmethod
  def replace_function_invocations(cls, snippet: str, function_names: List[str]) -> str:
    '''
    Replace function invocations in the given snippet with `secret_fun_4071()`.
    The snippet is expected to be a body of a Python script.
    '''
    src_parser = p_consts.PARSER_DICT['py']
    ts_tree = src_parser.parse(bytes(snippet, 'utf-8'))
    tree = Tree.from_ts_tree(ts_tree)
    replacer = cls(function_names)
    replacer.visit(tree.root_node)
    pretty_printer = PrettyPrinter(indent_with='    ')
    code = pretty_printer.visit(tree.root_node)
    return code.strip()


# TEST HARNESSES
def _test_pretty_printer():
  snippet = p_utils.read_tmp_text('test_pp.py')
  src_lang = 'py'

  parser = p_consts.PARSER_DICT[src_lang]
  ts_tree = parser.parse(bytes(snippet, 'utf8'))
  tree = Tree.from_ts_tree(ts_tree)

  pp = PrettyPrinter()
  code = pp.visit(tree.root_node)
  print(code)


def _test_parametrizable_variables_collector():
  snippet = p_utils.read_tmp_text('test_params.py')
  src_lang = 'py'

  parser = p_consts.PARSER_DICT[src_lang]
  ts_tree = parser.parse(bytes(snippet, 'utf8'))
  tree = Tree.from_ts_tree(ts_tree)

  pvc = ParametrizableVariablesCollector()
  pvc.visit(tree.root_node)
  print(pvc.parametrizable_identifiers)


def _test_log_statement_inserter():
  snippet = p_utils.read_tmp_text('test_inserter.py')
  src_lang = 'py'

  parser = p_consts.PARSER_DICT[src_lang]
  ts_tree = parser.parse(bytes(snippet, 'utf8'))
  tree = Tree.from_ts_tree(ts_tree)

  # first pass: insert print statements and modify AST
  psi = LogStatementInserter('f_gold')
  psi.visit(tree.root_node)

  # second pass: pretty print the modified AST
  pp = PrettyPrinter(indent_with='    ')
  code = pp.visit(tree.root_node)
  p_utils.write_tmp_text('test_script_instrumented.py', code)
  print(code)


def _test_classmethod_insert_log_statements():
  snippet = p_utils.read_tmp_text('test_inserter.py')
  output = LogStatementInserter.insert_log_statements(snippet)
  print(output)


if __name__ == '__main__':
  # _test_pretty_printer()
  # _test_tree_from_ts_tree()
  # _test_parametrizable_variables_collector()
  # _test_log_statement_inserter()
  _test_classmethod_insert_log_statements()
