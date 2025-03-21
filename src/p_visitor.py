from __future__ import annotations

import tree_sitter
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

import p_consts
import p_utils


class Visitor(ABC):
  @abstractmethod
  def visit(self, node: AbstractNode) -> Any:
    pass


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

  def accept(self, visitor: Visitor) -> None:
    return visitor.visit(self)

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
class AssignmentNode(AbstractNode): pass
class AttributeNode(AbstractNode): pass
class AugmentedAssignmentNode(AbstractNode): pass
class AwaitNode(AbstractNode): pass
class BinaryOperatorNode(AbstractNode): pass
class BlockNode(AbstractNode): pass
class BooleanOperatorNode(AbstractNode): pass
class BreakStatementNode(AbstractNode): pass
class CallNode(AbstractNode): pass
class ChevronNode(AbstractNode): pass
class ClassDefinitionNode(AbstractNode): pass
class CommentNode(AbstractNode): pass
class ComparisonOperatorNode(AbstractNode): pass
class ConcatenatedStringNode(AbstractNode): pass
class ConditionalExpressionNode(AbstractNode): pass
class ContinueStatementNode(AbstractNode): pass
class DecoratedDefinitionNode(AbstractNode): pass
class DecoratorNode(AbstractNode): pass
class DefaultParameterNode(AbstractNode): pass
class DeleteStatementNode(AbstractNode): pass
class DictionaryNode(AbstractNode): pass
class DictionaryComprehensionNode(AbstractNode): pass
class DictionarySplatNode(AbstractNode): pass
class DictionarySplatPatternNode(AbstractNode): pass
class DottedNameNode(AbstractNode): pass
class ElifClauseNode(AbstractNode): pass
class EllipsisNode(AbstractNode): pass
class ElseClauseNode(AbstractNode): pass
class EscapeInterpolationNode(AbstractNode): pass
class EscapeSequenceNode(AbstractNode): pass
class ExceptClauseNode(AbstractNode): pass
class ExecStatementNode(AbstractNode): pass
class ExpressionNode(AbstractNode): pass
class ExpressionListNode(AbstractNode): pass
class ExpressionStatementNode(AbstractNode): pass
class FalseNode(AbstractNode): pass
class FinallyClauseNode(AbstractNode): pass
class FloatNode(AbstractNode): pass
class ForInClauseNode(AbstractNode): pass
class ForStatementNode(AbstractNode): pass
class FormatExpressionNode(AbstractNode): pass
class FormatSpecifierNode(AbstractNode): pass
class FunctionDefinitionNode(AbstractNode): pass
class FutureImportStatementNode(AbstractNode): pass
class GeneratorExpressionNode(AbstractNode): pass
class GlobalStatementNode(AbstractNode): pass
class IdentifierNode(AbstractNode): pass
class IfClauseNode(AbstractNode): pass
class IfStatementNode(AbstractNode): pass
class ImportFromStatementNode(AbstractNode): pass
class ImportPrefixNode(AbstractNode): pass
class ImportStatementNode(AbstractNode): pass
class IntegerNode(AbstractNode): pass
class InterpolationNode(AbstractNode): pass
class KeywordArgumentNode(AbstractNode): pass
class KeywordIdentifierNode(AbstractNode): pass
class LambdaNode(AbstractNode): pass
class LambdaParametersNode(AbstractNode): pass
class LambdaWithinForInClauseNode(AbstractNode): pass
class ListNode(AbstractNode): pass
class ListComprehensionNode(AbstractNode): pass
class ListPatternNode(AbstractNode): pass
class ListSplatNode(AbstractNode): pass
class ListSplatPatternNode(AbstractNode): pass
class ModuleNode(AbstractNode): pass
class NamedExpressionNode(AbstractNode): pass
class NoneNode(AbstractNode): pass
class NonlocalStatementNode(AbstractNode): pass
class NotEscapeSequenceNode(AbstractNode): pass
class NotOperatorNode(AbstractNode): pass
class PairNode(AbstractNode): pass
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
class SetComprehensionNode(AbstractNode): pass
class SliceNode(AbstractNode): pass
class StringNode(AbstractNode): pass
class SubscriptNode(AbstractNode): pass
class TrueNode(AbstractNode): pass
class TryStatementNode(AbstractNode): pass
class TupleNode(AbstractNode): pass
class TuplePatternNode(AbstractNode): pass
class TypeNode(AbstractNode): pass
class TypeConversionNode(AbstractNode): pass
class TypedDefaultParameterNode(AbstractNode): pass
class TypedParameterNode(AbstractNode): pass
class UnaryOperatorNode(AbstractNode): pass
class WhileStatementNode(AbstractNode): pass
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
  Class that represents an AST that was generated by p_grammar.TreeSitterGrammar.generate_simplest_ast
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

    def _create_string_node(ts_node: tree_sitter.Node) -> StringNode:
      '''Special treatment for `string` nodes in tree-sitter trees'''
      node = StringNode('string')
      string_content_node = TerminalNode(ts_node.text.decode('utf-8'))
      node.add_child(string_content_node)
      string_content_node.set_parent(node)
      return node

    def _rec_construct_at(parent_node: AbstractNode, ts_node: tree_sitter.Node) -> None:
      '''Recursively construct the tree from a tree-sitter node'''

      # base case: leaf node
      # might be a terminal node, literal node
      if len(ts_node.children) == 0:
        text : str = ts_node.text.decode('utf-8')
        type : str = ts_node.type

        # terminal node
        if type == text:
          terminal_node = TerminalNode(ts_node.text.decode('utf-8'))
          parent_node.add_child(terminal_node)
          terminal_node.set_parent(parent_node)
          return

        # literal node
        NodeCls = NODE_TYPES_CLASSES[ts_node.type]
        literal_node = NodeCls(ts_node.type)
        parent_node.add_child(literal_node)
        literal_node.set_parent(parent_node)

        terminal_node = TerminalNode(ts_node.text.decode('utf-8'))
        literal_node.add_child(terminal_node)
        terminal_node.set_parent(literal_node)
        return

      # base case: string node
      if ts_node.type == 'string':
        terminal_node = _create_string_node(ts_node)
        parent_node.add_child(terminal_node)
        terminal_node.set_parent(parent_node)
        return

      # general case: non-terminal node
      NodeCls = NODE_TYPES_CLASSES[ts_node.type]
      terminal_node = NodeCls(ts_node.type)
      parent_node.add_child(terminal_node)
      terminal_node.set_parent(parent_node)

      for child in ts_node.children:
        _rec_construct_at(terminal_node, child)

    ts_root_node = ts_tree.root_node
    assert not ts_root_node.has_error, 'tree-sitter tree has error'

    RootNodeCls = NODE_TYPES_CLASSES[ts_root_node.type]
    root_node = RootNodeCls(ts_root_node.type)

    for child in ts_root_node.children:
      _rec_construct_at(root_node, child)

    tree = Tree(root_node)
    return tree


class PrettyPrinter(Visitor):
  def __init__(self) -> None:
    super().__init__()
    self.indentation_level : int = 0
    self.indentation_size : int = 2

  def visit(self, node: AbstractNode) -> str:
    method_name = 'visit_' + node.__class__.__name__
    visit_method = getattr(self, method_name, self.default_visit)
    return visit_method(node)

  def indent(self, text: str) -> str:
    self.indentation_level += 1
    code = p_utils.indent(text, self.indentation_level * self.indentation_size)
    self.indentation_level -= 1
    return code

  def default_visit(self, node: AbstractNode, delimiter: str = ' ') -> str:
    code = ''
    for child in node.children:
      child_code = child.accept(self)
      code += (child_code + delimiter)
    return code.strip()

  def visit_TerminalNode(self, node: TerminalNode) -> str:
    return node.node_type

  def visit__SuiteNode(self, node: _SuiteNode) -> str:
    code = self.default_visit(node, delimiter='\n')
    code = self.indent(code)
    return '\n' + code


# TEST HARNESSES
def _test_pretty_printer():
  snippet = p_utils.read_tmp_text('L0001_TwoSum.py')
  src_lang = 'py'

  parser = p_consts.PARSER_DICT[src_lang]
  ts_tree = parser.parse(bytes(snippet, 'utf8'))
  tree = Tree.from_ts_tree(ts_tree)

  pp = PrettyPrinter()
  code = pp.visit(tree.root_node)
  print(code)


def _test_tree_from_ts_tree():
  snippet = p_utils.read_tmp_text('L0001_TwoSum.py')
  src_lang = 'py'

  # logic
  parser = p_consts.PARSER_DICT[src_lang]
  ts_tree = parser.parse(bytes(snippet, 'utf8'))
  tree = Tree.from_ts_tree(ts_tree)
  print()


if __name__ == '__main__':
  _test_pretty_printer()
  # _test_tree_from_ts_tree()
