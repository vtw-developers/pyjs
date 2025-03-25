from __future__ import annotations

import tree_sitter
from abc import ABC, abstractmethod
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
class AugmentedAssignmentNode(AbstractNode): pass
class AwaitNode(AbstractNode): pass
class BinaryOperatorNode(AbstractNode): pass
class BlockNode(AbstractNode): pass
class BooleanOperatorNode(AbstractNode): pass
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
class GeneratorExpressionNode(AbstractNode): pass
class GlobalStatementNode(AbstractNode): pass
class IdentifierNode(AbstractNode):
  def __init__(self, node_type: str):
    super().__init__(node_type)
  def val(self) -> str:
    assert len(self.children) == 1, 'sanity check'
    assert isinstance(self.children[0], TerminalNode), 'sanity check'
    return self.children[0].node_type
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
class ListComprehensionNode(AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.body : AbstractNode = None
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
    _SPECIAL_NODES_WITH_FIELDS = [
      'attribute',
      'assignment',
      'call',
      'for_in_clause',
      'for_statement',
      'function_definition',
      'list_comprehension',
      'subscript',
      'typed_parameter',
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

    def _create_node_with_field(ts_node: tree_sitter.Node) -> AbstractNode:
      '''
      Special treatment for some nodes in tree-sitter trees.
      What is special about these nodes? They have fields.
      Their fields must be registered as attributes in their respective
      classes (see `AssignmentNode` for example). This special treatment
      allows us to access fields of these classes as attributes.
      Check `_SPECIAL_NODES_WITH_FIELDS` for the list of special nodes.
      '''
      # instantiate a special node
      ntype = ts_node.type
      NodeCls = NODE_TYPES_CLASSES[ntype]
      special_node = NodeCls(ntype)

      # field names of the special node
      field_names = [ts_node.field_name_for_child(i) for i in range(len(ts_node.children))]
      field_names = [fn for fn in field_names if fn is not None]

      # add children to the special node
      for idx, ts_child in enumerate(ts_node.children):
        child_node = _rec_build_tree(ts_child)
        special_node.add_child(child_node)
        child_node.set_parent(special_node)

        # set attributes of the special node
        ts_child_field_name = ts_node.field_name_for_child(idx)
        if ts_child_field_name in field_names:
          setattr(special_node, ts_child_field_name, child_node)

      return special_node

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

      # special case: nodes with fields
      # NOTE might as well do this for all nodes
      if ts_node.type in _SPECIAL_NODES_WITH_FIELDS:
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
  def __init__(self) -> None:
    super().__init__()
    self.indentation_level : int = 0
    self.indentation_size : int = 2

  def indent(self, text: str) -> str:
    self.indentation_level += 1
    code = p_utils.indent(text, self.indentation_level * self.indentation_size)
    self.indentation_level -= 1
    return code

  def default_visit(self, node: AbstractNode, delimiter: str = ' ') -> str:
    code = ''
    for child in node.children:
      child_code = self.visit(child)
      code += (child_code + delimiter)
    return code.strip()

  def visit_TerminalNode(self, node: TerminalNode) -> str:
    return node.node_type

  def visit__SuiteNode(self, node: _SuiteNode) -> str:
    code = self.default_visit(node, delimiter='\n')
    code = self.indent(code)
    return '\n' + code


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

  # VISIT METHODS
  def default_visit(self, node: AbstractNode) -> None:
    for child in node.children:
      self.visit(child)

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
    Do not visit `node.function`:
    1. it is a function name
    '''
    self.ctx.append('call.arguments')
    self.visit(node.arguments)
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

  def visit_ImportFromStatementNode(self, node: ImportFromStatementNode) -> None:
    '''Do not visit anything'''

  def visit_ImportStatementNode(self, node: ImportStatementNode) -> None:
    '''Do not visit anything'''

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
    '''
    # we will modify this list, that's why we need a slice
    children = node.get_nt_children()[:]

    # Separate function_definition nodes from other nodes
    function_definitions = [child for child in children if isinstance(child, FunctionDefinitionNode)]
    other_nodes = [child for child in children if not isinstance(child, FunctionDefinitionNode)]

    # Concatenate other nodes with function_definition nodes at the end
    children = other_nodes + function_definitions

    for child in children:
      self.visit(child)

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
