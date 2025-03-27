from __future__ import annotations

import tree_sitter
from abc import ABC
from typing import final, Any, Dict, List, Union

import p_consts
import p_utils


class Visitor(ABC):
  @final
  def visit(self, node: AbstractNode) -> Any:
    '''
    This is a dispatcher method that either calls `self.visit_<NodeClass>()`
    if it exists. Otherwise, falls back to `self.default_visit()`.
    <NodeClass> is a CamelCase class name for parameter `node`.
    NOTE this method is intended to be final, i.e. not be overridden.
    '''
    method_name = 'visit_' + node.__class__.__name__
    visit_method = getattr(self, method_name, self.default_visit)
    return visit_method(node)

  def default_visit(self, node: AbstractNode) -> None:
    '''
    Default visit method for all nodes.
    NOTE can be overridden in subclasses.
    '''
    for child in node.children:
      self.visit(child)


class AbstractNode(ABC):
  '''
  This is the base class for node classes.
  All node classes should inherit from this class.
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
    return self.parent

  def get_root_node(self) -> AbstractNode:
    '''
    Return root_node of the tree that `self` belongs to
    According to class invariant INV2, root_node's parent is itself.
    '''
    cursor = self
    while cursor.parent is not None:
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

  def is_terminal(self) -> bool:
    return isinstance(self, TerminalNode)

  def is_nonterminal(self) -> bool:
    return not self.is_terminal()

class TerminalNode(AbstractNode):
  def __repr__(self) -> str:
    return f'Terminal({repr(self.node_type)})'
class _CollectionElementsNode(AbstractNode): pass
class _CompoundStatementNode(AbstractNode): pass
class _ComprehensionClausesNode(AbstractNode): pass
class _ExpressionWithinForInClauseNode(AbstractNode): pass
class _ExpressionsNode(AbstractNode): pass
class _ImportListNode(AbstractNode): pass
class _LeftHandSideNode(AbstractNode): pass
class _ParametersNode(AbstractNode): pass
class _PatternsNode(AbstractNode): pass
class _RightHandSideNode(AbstractNode): pass
class _SimpleStatementNode(AbstractNode): pass
class _SimpleStatementsNode(AbstractNode): pass
class _StatementNode(AbstractNode): pass
class _SuiteNode(AbstractNode): pass
class AliasedImportNode(AbstractNode): pass
class ArgumentListNode(AbstractNode): pass
class AssertStatementNode(AbstractNode): pass
class AssignmentNode(AbstractNode):
  def __init__(self, node_type: str):
    super().__init__(node_type)
    self.left : AbstractNode = None
    self.type : AbstractNode = None
    self.right : AbstractNode = None
class AttributeNode(AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.object : AbstractNode = None
    self.attribute : AbstractNode = None
class AugmentedAssignmentNode(AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.left : AbstractNode = None
    self.operator : AbstractNode = None
    self.right : AbstractNode = None
class AwaitNode(AbstractNode): pass
class BinaryOperatorNode(AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.left : AbstractNode = None
    self.operator : AbstractNode = None
    self.right : AbstractNode = None
class BlockNode(AbstractNode): pass
class BooleanOperatorNode(AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.left : AbstractNode = None
    self.operator : AbstractNode = None
    self.right : AbstractNode = None
class BreakStatementNode(AbstractNode): pass
class CallNode(AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.function : AbstractNode = None
    self.arguments : AbstractNode = None
class ChevronNode(AbstractNode): pass
class ClassDefinitionNode(AbstractNode): pass
class CommentNode(AbstractNode): pass
class ComparisonOperatorNode(AbstractNode): pass
class ConcatenatedStringNode(AbstractNode): pass
class ConditionalExpressionNode(AbstractNode): pass
class ContinueStatementNode(AbstractNode): pass
class DecoratedDefinitionNode(AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.definition : AbstractNode = None
class DecoratorNode(AbstractNode): pass
class DefaultParameterNode(AbstractNode): pass
class DeleteStatementNode(AbstractNode): pass
class DictionaryNode(AbstractNode): pass
class DictionaryComprehensionNode(AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.body : AbstractNode = None
class DictionarySplatNode(AbstractNode): pass
class DictionarySplatPatternNode(AbstractNode): pass
class DottedNameNode(AbstractNode): pass
class ElifClauseNode(AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.condition : AbstractNode = None
    self.consequence : AbstractNode = None
class EllipsisNode(AbstractNode): pass
class ElseClauseNode(AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.body : AbstractNode = None
class EscapeInterpolationNode(AbstractNode): pass
class EscapeSequenceNode(AbstractNode): pass
class ExceptClauseNode(AbstractNode): pass
class ExecStatementNode(AbstractNode): pass
class ExpressionNode(AbstractNode): pass
class ExpressionListNode(AbstractNode): pass
class ExpressionStatementNode(AbstractNode): pass
class FalseNode(AbstractNode): pass
class FinallyClauseNode(AbstractNode): pass
class FloatNode(AbstractNode):
  def val(self) -> str:
    assert len(self.children) == 1, 'sanity check'
    assert isinstance(self.children[0], TerminalNode), 'sanity check'
    return self.children[0].node_type
class ForInClauseNode(AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.left : AbstractNode = None
    self.right : AbstractNode = None
class ForStatementNode(AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.left : AbstractNode = None
    self.right : AbstractNode = None
    self.body : AbstractNode = None
    self.alternative : AbstractNode = None
class FormatExpressionNode(AbstractNode): pass
class FormatSpecifierNode(AbstractNode): pass
class FunctionDefinitionNode(AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.name : AbstractNode = None
    self.parameters : AbstractNode = None
    self.return_type : AbstractNode = None
    self.body : AbstractNode = None
class FutureImportStatementNode(AbstractNode): pass
class GeneratorExpressionNode(AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.body : AbstractNode = None
class GlobalStatementNode(AbstractNode): pass
class IdentifierNode(AbstractNode):
  def __init__(self, node_type: str):
    super().__init__(node_type)
  def __repr__(self) -> str:
    return f'ID({self.val()})'
  def val(self) -> str:
    assert len(self.children) == 1, 'sanity check'
    assert isinstance(self.children[0], TerminalNode), 'sanity check'
    return self.children[0].node_type
class IfClauseNode(AbstractNode): pass
class IfStatementNode(AbstractNode):
  '''
  In tree-sitter AST, multiple nodes may appear under a single field `alternative`.
  Since a single attribute holds a single node,
  we use `alternatives` attribute to hold all nodes under `alternative`.
  '''
  def __init__(self, node_type):
    super().__init__(node_type)
    self.condition : AbstractNode = None
    self.consequence : AbstractNode = None
    self.alternatives : List[AbstractNode] = []
class ImportFromStatementNode(AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.module_name : AbstractNode = None
class ImportPrefixNode(AbstractNode): pass
class ImportStatementNode(AbstractNode): pass
class IntegerNode(AbstractNode):
  def val(self) -> str:
    assert len(self.children) == 1, 'sanity check'
    assert isinstance(self.children[0], TerminalNode), 'sanity check'
    return self.children[0].node_type
class InterpolationNode(AbstractNode): pass
class KeywordArgumentNode(AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.name : AbstractNode = None
    self.value : AbstractNode = None
class KeywordIdentifierNode(AbstractNode): pass
class LambdaNode(AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.parameters : AbstractNode = None
    self.body : AbstractNode = None
class LambdaParametersNode(AbstractNode): pass
class LambdaWithinForInClauseNode(AbstractNode): pass
class ListNode(AbstractNode): pass
class ListComprehensionNode(AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.body : AbstractNode = None
class ListPatternNode(AbstractNode): pass
class ListSplatNode(AbstractNode): pass
class ListSplatPatternNode(AbstractNode): pass
class ModuleNode(AbstractNode): pass
class NamedExpressionNode(AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.name : AbstractNode = None
    self.value : AbstractNode = None
class NoneNode(AbstractNode): pass
class NonlocalStatementNode(AbstractNode): pass
class NotEscapeSequenceNode(AbstractNode): pass
class NotOperatorNode(AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.argument : AbstractNode = None
class PairNode(AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.key : AbstractNode = None
    self.value : AbstractNode = None
class ParameterNode(AbstractNode): pass
class ParametersNode(AbstractNode): pass
class ParenthesizedExpressionNode(AbstractNode): pass
class ParenthesizedListSplatNode(AbstractNode): pass
class PassStatementNode(AbstractNode): pass
class PatternNode(AbstractNode): pass
class PatternListNode(AbstractNode): pass
class PrimaryExpressionNode(AbstractNode): pass
class PrintStatementNode(AbstractNode): pass
class RaiseStatementNode(AbstractNode): pass
class RelativeImportNode(AbstractNode): pass
class ReturnStatementNode(AbstractNode): pass
class SetNode(AbstractNode): pass
class SetComprehensionNode(AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.body : AbstractNode = None
class SliceNode(AbstractNode): pass
class StringNode(AbstractNode):
  '''NOTE may not support all types of quoted strings'''
  def val(self) -> str:
    assert len(self.children) == 1, 'sanity check'
    assert isinstance(self.children[0], TerminalNode), 'sanity check'
    return self.children[0].node_type
class SubscriptNode(AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.value : AbstractNode = None
    self.subscript : AbstractNode = None
class TrueNode(AbstractNode): pass
class TryStatementNode(AbstractNode): pass
class TupleNode(AbstractNode): pass
class TuplePatternNode(AbstractNode): pass
class TypeNode(AbstractNode): pass
class TypeConversionNode(AbstractNode): pass
class TypedDefaultParameterNode(AbstractNode): pass
class TypedParameterNode(AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.type : AbstractNode = None
class UnaryOperatorNode(AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.operator : AbstractNode = None
    self.argument : AbstractNode = None
class WhileStatementNode(AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.condition : AbstractNode = None
    self.body : AbstractNode = None
    self.alternative : AbstractNode = None
class WildcardImportNode(AbstractNode): pass
class WithClauseNode(AbstractNode): pass
class WithItemNode(AbstractNode): pass
class WithStatementNode(AbstractNode): pass
class YieldNode(AbstractNode): pass


NODE_TYPES_CLASSES: Dict[str, AbstractNode] = {
  'terminal': TerminalNode,
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


class Tree:
  '''
  Class that represents an AST that was generated by p_grammar.TreeSitterGrammar.generate_simplest_ast.
  This class is compatible with `Visitor` classes.
  '''
  def __init__(self, root_node: AbstractNode) -> None:
    self.root_node: AbstractNode = root_node

  def __repr__(self) -> str:
    return f'Tree({self.root_node.node_type})'

  @classmethod
  def from_gen_ast(cls, ast: list) -> Tree:
    '''
    Construct a Tree from a structure generated by p_grammar.TreeSitterGrammar.generate_simplest_ast
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
    for child in children:
      _rec_construct_at(root_node, child)
    tree = Tree(root_node)
    return tree

  @classmethod
  def from_ts_tree(cls, ts_tree: tree_sitter.Tree) -> Tree:
    '''
    Construct a Tree from a parsed tree-sitter tree
    NOTE we can also use `text` attribute of `ts_tree`
    '''

    # special treatment for some nodes
    # these nodes have fields that we want to access as attributes
    # check `_create_special_node` for more details.
    _NODES_WITH_FIELDS = [
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

    def _create_StringNode(ts_node: tree_sitter.Node) -> StringNode:
      '''
      Special treatment for `string` nodes in tree-sitter trees.
      We want `string` to be a literal node in our AST. However,
      in tree-sitter trees, `string` nodes are not literal nodes.
      '''
      node = StringNode('string')
      string_content_node = TerminalNode(ts_node.text.decode('utf-8'))
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

    def _create_node_with_field(ts_node: tree_sitter.Node) -> AbstractNode:
      '''
      Special treatment for some nodes in tree-sitter trees.
      What is special about these nodes? They have fields.
      Their fields must be registered as attributes in their respective
      classes (see `AssignmentNode` for example). This special treatment
      allows us to access fields of these classes as attributes.
      Check `_NODES_WITH_FIELDS` for the list of special nodes.

      NOTE TODO in `if_statement`, there are multiple nodes under a single
      field `alternative`. Current implementation does not support it, as it
      will save the last node under `alternative` as an attribute.
      The same issue is true for `comparison_operator`
      and its `operators` field.
      '''
      # instantiate a special node
      ntype = ts_node.type
      NodeCls = NODE_TYPES_CLASSES[ntype]
      node_wfield = NodeCls(ntype)

      # field names of the special node
      ts_field_names = [ts_node.field_name_for_child(i) for i in range(len(ts_node.children))]
      ts_field_names = [fn for fn in ts_field_names if fn is not None]

      # add children to the special node
      for idx, ts_child in enumerate(ts_node.children):
        child_node = _rec_build_tree(ts_child)
        node_wfield.add_child(child_node)
        child_node.set_parent(node_wfield)

        # set attributes of the special node
        ts_child_field_name = ts_node.field_name_for_child(idx)
        if ts_child_field_name in ts_field_names:
          setattr(node_wfield, ts_child_field_name, child_node)

      return node_wfield

    def _rec_build_tree(ts_node: tree_sitter.Node) -> AbstractNode:
      '''Construct a tree from a tree-sitter node recursively'''
      # base case: leaf node
      # might be a terminal node, literal node
      if len(ts_node.children) == 0:
        text : str = ts_node.text.decode('utf-8')
        type_ : str = ts_node.type

        # terminal node
        if type_ == text:
          return TerminalNode(text)

        # literal node
        NodeCls = NODE_TYPES_CLASSES[type_]
        literal_node = NodeCls(type_)
        tnode = TerminalNode(text)
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
      if ts_node.type in _NODES_WITH_FIELDS:
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


class PrettyPrinter(Visitor):
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
  def default_visit(self, node: AbstractNode) -> None:
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
    elements = ', '.join([self.visit(child) for child in node.get_nt_children()])
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

  def visit_TerminalNode(self, node: TerminalNode) -> str:
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


class ParametrizableVariablesCollector(Visitor):
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
    if self.ctx and self.ctx[-1] == 'keyword_argument.value':
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


if __name__ == '__main__':
  # _test_pretty_printer()
  # _test_tree_from_ts_tree()
  _test_parametrizable_variables_collector()
