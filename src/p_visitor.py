from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Union

import p_utils


class Visitor(ABC):
  '''
  This is the Visitor interface for ASTs generated from parsing Python code.
  Should add an abstract method for each node type.

  NOTE
  This class changes only if the Tree-Sitter node types change for Python.
  '''

  @abstractmethod
  def visit_terminal_node(self, node: TerminalNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit__collection_elements_node(self, node: _CollectionElementsNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit__compound_statement_node(self, node: _CompoundStatementNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit__comprehension_clauses_node(self, node: _ComprehensionClausesNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit__expression_within_for_in_clause_node(self, node: _ExpressionWithinForInClauseNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit__expressions_node(self, node: _ExpressionsNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit__import_list_node(self, node: _ImportListNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit__left_hand_side_node(self, node: _LeftHandSideNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit__parameters_node(self, node: _ParametersNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit__patterns_node(self, node: _PatternsNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit__right_hand_side_node(self, node: _RightHandSideNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit__simple_statement_node(self, node: _SimpleStatementNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit__simple_statements_node(self, node: _SimpleStatementsNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit__statement_node(self, node: _StatementNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit__suite_node(self, node: _SuiteNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_aliased_import_node(self, node: AliasedImportNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_argument_list_node(self, node: ArgumentListNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_assert_statement_node(self, node: AssertStatementNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_assignment_node(self, node: AssignmentNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_attribute_node(self, node: AttributeNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_augmented_assignment_node(self, node: AugmentedAssignmentNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_await_node(self, node: AwaitNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_binary_operator_node(self, node: BinaryOperatorNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_block_node(self, node: BlockNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_boolean_operator_node(self, node: BooleanOperatorNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_break_statement_node(self, node: BreakStatementNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_call_node(self, node: CallNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_chevron_node(self, node: ChevronNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_class_definition_node(self, node: ClassDefinitionNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_comment_node(self, node: CommentNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_comparison_operator_node(self, node: ComparisonOperatorNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_concatenated_string_node(self, node: ConcatenatedStringNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_conditional_expression_node(self, node: ConditionalExpressionNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_continue_statement_node(self, node: ContinueStatementNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_decorated_definition_node(self, node: DecoratedDefinitionNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_decorator_node(self, node: DecoratorNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_default_parameter_node(self, node: DefaultParameterNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_delete_statement_node(self, node: DeleteStatementNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_dictionary_node(self, node: DictionaryNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_dictionary_comprehension_node(self, node: DictionaryComprehensionNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_dictionary_splat_node(self, node: DictionarySplatNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_dictionary_splat_pattern_node(self, node: DictionarySplatPatternNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_dotted_name_node(self, node: DottedNameNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_elif_clause_node(self, node: ElifClauseNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_ellipsis_node(self, node: EllipsisNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_else_clause_node(self, node: ElseClauseNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_escape_interpolation_node(self, node: EscapeInterpolationNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_escape_sequence_node(self, node: EscapeSequenceNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_except_clause_node(self, node: ExceptClauseNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_exec_statement_node(self, node: ExecStatementNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_expression_node(self, node: ExpressionNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_expression_list_node(self, node: ExpressionListNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_expression_statement_node(self, node: ExpressionStatementNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_false_node(self, node: FalseNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_finally_clause_node(self, node: FinallyClauseNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_float_node(self, node: FloatNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_for_in_clause_node(self, node: ForInClauseNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_for_statement_node(self, node: ForStatementNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_format_expression_node(self, node: FormatExpressionNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_format_specifier_node(self, node: FormatSpecifierNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_function_definition_node(self, node: FunctionDefinitionNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_future_import_statement_node(self, node: FutureImportStatementNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_generator_expression_node(self, node: GeneratorExpressionNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_global_statement_node(self, node: GlobalStatementNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_identifier_node(self, node: IdentifierNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_if_clause_node(self, node: IfClauseNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_if_statement_node(self, node: IfStatementNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_import_from_statement_node(self, node: ImportFromStatementNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_import_prefix_node(self, node: ImportPrefixNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_import_statement_node(self, node: ImportStatementNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_integer_node(self, node: IntegerNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_interpolation_node(self, node: InterpolationNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_keyword_argument_node(self, node: KeywordArgumentNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_keyword_identifier_node(self, node: KeywordIdentifierNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_lambda_node(self, node: LambdaNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_lambda_parameters_node(self, node: LambdaParametersNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_lambda_within_for_in_clause_node(self, node: LambdaWithinForInClauseNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_list_node(self, node: ListNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_list_comprehension_node(self, node: ListComprehensionNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_list_pattern_node(self, node: ListPatternNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_list_splat_node(self, node: ListSplatNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_list_splat_pattern_node(self, node: ListSplatPatternNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_module_node(self, node: ModuleNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_named_expression_node(self, node: NamedExpressionNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_none_node(self, node: NoneNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_nonlocal_statement_node(self, node: NonlocalStatementNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_not_escape_sequence_node(self, node: NotEscapeSequenceNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_not_operator_node(self, node: NotOperatorNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_pair_node(self, node: PairNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_parameter_node(self, node: ParameterNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_parameters_node(self, node: ParametersNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_parenthesized_expression_node(self, node: ParenthesizedExpressionNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_parenthesized_list_splat_node(self, node: ParenthesizedListSplatNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_pass_statement_node(self, node: PassStatementNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_pattern_node(self, node: PatternNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_pattern_list_node(self, node: PatternListNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_primary_expression_node(self, node: PrimaryExpressionNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_print_statement_node(self, node: PrintStatementNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_raise_statement_node(self, node: RaiseStatementNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_relative_import_node(self, node: RelativeImportNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_return_statement_node(self, node: ReturnStatementNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_set_node(self, node: SetNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_set_comprehension_node(self, node: SetComprehensionNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_slice_node(self, node: SliceNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_string_node(self, node: StringNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_subscript_node(self, node: SubscriptNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_true_node(self, node: TrueNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_try_statement_node(self, node: TryStatementNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_tuple_node(self, node: TupleNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_tuple_pattern_node(self, node: TuplePatternNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_type_node(self, node: TypeNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_type_conversion_node(self, node: TypeConversionNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_typed_default_parameter_node(self, node: TypedDefaultParameterNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_typed_parameter_node(self, node: TypedParameterNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_unary_operator_node(self, node: UnaryOperatorNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_while_statement_node(self, node: WhileStatementNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_wildcard_import_node(self, node: WildcardImportNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_with_clause_node(self, node: WithClauseNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_with_item_node(self, node: WithItemNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_with_statement_node(self, node: WithStatementNode) -> None:
    raise NotImplementedError

  @abstractmethod
  def visit_yield_node(self, node: YieldNode) -> None:
    raise NotImplementedError


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

class TerminalNode(AbstractNode):
  def __repr__(self) -> str:
    return f'"{self.node_type}"'

  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_terminal_node(self)

class _CollectionElementsNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit__collection_elements_node(self)

class _CompoundStatementNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit__compound_statement_node(self)

class _ComprehensionClausesNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit__comprehension_clauses_node(self)

class _ExpressionWithinForInClauseNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit__expression_within_for_in_clause_node(self)

class _ExpressionsNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit__expressions_node(self)

class _ImportListNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit__import_list_node(self)

class _LeftHandSideNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit__left_hand_side_node(self)

class _ParametersNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit__parameters_node(self)

class _PatternsNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit__patterns_node(self)

class _RightHandSideNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit__right_hand_side_node(self)

class _SimpleStatementNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit__simple_statement_node(self)

class _SimpleStatementsNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit__simple_statements_node(self)

class _StatementNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit__statement_node(self)

class _SuiteNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit__suite_node(self)

class AliasedImportNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_aliased_import_node(self)

class ArgumentListNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_argument_list_node(self)

class AssertStatementNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_assert_statement_node(self)

class AssignmentNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_assignment_node(self)

class AttributeNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_attribute_node(self)

class AugmentedAssignmentNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_augmented_assignment_node(self)

class AwaitNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_await_node(self)

class BinaryOperatorNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_binary_operator_node(self)

class BlockNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_block_node(self)

class BooleanOperatorNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_boolean_operator_node(self)

class BreakStatementNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_break_statement_node(self)

class CallNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_call_node(self)

class ChevronNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_chevron_node(self)

class ClassDefinitionNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_class_definition_node(self)

class CommentNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_comment_node(self)

class ComparisonOperatorNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_comparison_operator_node(self)

class ConcatenatedStringNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_concatenated_string_node(self)

class ConditionalExpressionNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_conditional_expression_node(self)

class ContinueStatementNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_continue_statement_node(self)

class DecoratedDefinitionNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_decorated_definition_node(self)

class DecoratorNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_decorator_node(self)

class DefaultParameterNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_default_parameter_node(self)

class DeleteStatementNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_delete_statement_node(self)

class DictionaryNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_dictionary_node(self)

class DictionaryComprehensionNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_dictionary_comprehension_node(self)

class DictionarySplatNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_dictionary_splat_node(self)

class DictionarySplatPatternNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_dictionary_splat_pattern_node(self)

class DottedNameNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_dotted_name_node(self)

class ElifClauseNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_elif_clause_node(self)

class EllipsisNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_ellipsis_node(self)

class ElseClauseNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_else_clause_node(self)

class EscapeInterpolationNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_escape_interpolation_node(self)

class EscapeSequenceNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_escape_sequence_node(self)

class ExceptClauseNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_except_clause_node(self)

class ExecStatementNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_exec_statement_node(self)

class ExpressionNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_expression_node(self)

class ExpressionListNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_expression_list_node(self)

class ExpressionStatementNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_expression_statement_node(self)

class FalseNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_false_node(self)

class FinallyClauseNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_finally_clause_node(self)

class FloatNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_float_node(self)

class ForInClauseNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_for_in_clause_node(self)

class ForStatementNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_for_statement_node(self)

class FormatExpressionNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_format_expression_node(self)

class FormatSpecifierNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_format_specifier_node(self)

class FunctionDefinitionNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_function_definition_node(self)

class FutureImportStatementNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_future_import_statement_node(self)

class GeneratorExpressionNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_generator_expression_node(self)

class GlobalStatementNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_global_statement_node(self)

class IdentifierNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_identifier_node(self)

class IfClauseNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_if_clause_node(self)

class IfStatementNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_if_statement_node(self)

class ImportFromStatementNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_import_from_statement_node(self)

class ImportPrefixNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_import_prefix_node(self)

class ImportStatementNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_import_statement_node(self)

class IntegerNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_integer_node(self)

class InterpolationNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_interpolation_node(self)

class KeywordArgumentNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_keyword_argument_node(self)

class KeywordIdentifierNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_keyword_identifier_node(self)

class LambdaNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_lambda_node(self)

class LambdaParametersNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_lambda_parameters_node(self)

class LambdaWithinForInClauseNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_lambda_within_for_in_clause_node(self)

class ListNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_list_node(self)

class ListComprehensionNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_list_comprehension_node(self)

class ListPatternNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_list_pattern_node(self)

class ListSplatNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_list_splat_node(self)

class ListSplatPatternNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_list_splat_pattern_node(self)

class ModuleNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_module_node(self)

class NamedExpressionNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_named_expression_node(self)

class NoneNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_none_node(self)

class NonlocalStatementNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_nonlocal_statement_node(self)

class NotEscapeSequenceNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_not_escape_sequence_node(self)

class NotOperatorNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_not_operator_node(self)

class PairNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_pair_node(self)

class ParameterNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_parameter_node(self)

class ParametersNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_parameters_node(self)

class ParenthesizedExpressionNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_parenthesized_expression_node(self)

class ParenthesizedListSplatNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_parenthesized_list_splat_node(self)

class PassStatementNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_pass_statement_node(self)

class PatternNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_pattern_node(self)

class PatternListNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_pattern_list_node(self)

class PrimaryExpressionNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_primary_expression_node(self)

class PrintStatementNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_print_statement_node(self)

class RaiseStatementNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_raise_statement_node(self)

class RelativeImportNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_relative_import_node(self)

class ReturnStatementNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_return_statement_node(self)

class SetNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_set_node(self)

class SetComprehensionNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_set_comprehension_node(self)

class SliceNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_slice_node(self)

class StringNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_string_node(self)

class SubscriptNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_subscript_node(self)

class TrueNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_true_node(self)

class TryStatementNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_try_statement_node(self)

class TupleNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_tuple_node(self)

class TuplePatternNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_tuple_pattern_node(self)

class TypeNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_type_node(self)

class TypeConversionNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_type_conversion_node(self)

class TypedDefaultParameterNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_typed_default_parameter_node(self)

class TypedParameterNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_typed_parameter_node(self)

class UnaryOperatorNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_unary_operator_node(self)

class WhileStatementNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_while_statement_node(self)

class WildcardImportNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_wildcard_import_node(self)

class WithClauseNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_with_clause_node(self)

class WithItemNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_with_item_node(self)

class WithStatementNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_with_statement_node(self)

class YieldNode(AbstractNode):
  def accept(self, visitor: Visitor) -> None:
    return visitor.visit_yield_node(self)


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
    root_node.set_parent(root_node)
    for child in children:
      _rec_construct_at(root_node, child)
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

  def default_visit(self, node: AbstractNode, delimeter: str = ' ') -> str:
    code = ''
    for child in node.children:
      child_code = child.accept(self)
      code += (child_code + delimeter)
    return code.strip()

  def visit_terminal_node(self, node: TerminalNode) -> str:
    return node.node_type

  def visit__collection_elements_node(self, node: _CollectionElementsNode) -> str:
    return self.default_visit(node)

  def visit__compound_statement_node(self, node: _CompoundStatementNode) -> str:
    return self.default_visit(node)

  def visit__comprehension_clauses_node(self, node: _ComprehensionClausesNode) -> str:
    return self.default_visit(node)

  def visit__expression_within_for_in_clause_node(self, node: _ExpressionWithinForInClauseNode) -> str:
    return self.default_visit(node)

  def visit__expressions_node(self, node: _ExpressionsNode) -> str:
    return self.default_visit(node)

  def visit__import_list_node(self, node: _ImportListNode) -> str:
    return self.default_visit(node)

  def visit__left_hand_side_node(self, node: _LeftHandSideNode) -> str:
    return self.default_visit(node)

  def visit__parameters_node(self, node: _ParametersNode) -> str:
    return self.default_visit(node)

  def visit__patterns_node(self, node: _PatternsNode) -> str:
    return self.default_visit(node)

  def visit__right_hand_side_node(self, node: _RightHandSideNode) -> str:
    return self.default_visit(node)

  def visit__simple_statement_node(self, node: _SimpleStatementNode) -> str:
    return self.default_visit(node)

  def visit__simple_statements_node(self, node: _SimpleStatementsNode) -> str:
    return self.default_visit(node)

  def visit__statement_node(self, node: _StatementNode) -> str:
    return self.default_visit(node)

  def visit__suite_node(self, node: _SuiteNode) -> str:
    code = self.default_visit(node, delimeter='\n')
    code = self.indent(code)
    return '\n' + code

  def visit_aliased_import_node(self, node: AliasedImportNode) -> str:
    return self.default_visit(node)

  def visit_argument_list_node(self, node: ArgumentListNode) -> str:
    return self.default_visit(node)

  def visit_assert_statement_node(self, node: AssertStatementNode) -> str:
    return self.default_visit(node)

  def visit_assignment_node(self, node: AssignmentNode) -> str:
    return self.default_visit(node)

  def visit_attribute_node(self, node: AttributeNode) -> str:
    return self.default_visit(node)

  def visit_augmented_assignment_node(self, node: AugmentedAssignmentNode) -> str:
    return self.default_visit(node)

  def visit_await_node(self, node: AwaitNode) -> str:
    return self.default_visit(node)

  def visit_binary_operator_node(self, node: BinaryOperatorNode) -> str:
    return self.default_visit(node)

  def visit_block_node(self, node: BlockNode) -> str:
    return self.default_visit(node)

  def visit_boolean_operator_node(self, node: BooleanOperatorNode) -> str:
    return self.default_visit(node)

  def visit_break_statement_node(self, node: BreakStatementNode) -> str:
    return self.default_visit(node)

  def visit_call_node(self, node: CallNode) -> str:
    return self.default_visit(node)

  def visit_chevron_node(self, node: ChevronNode) -> str:
    return self.default_visit(node)

  def visit_class_definition_node(self, node: ClassDefinitionNode) -> str:
    return self.default_visit(node)

  def visit_comment_node(self, node: CommentNode) -> str:
    return self.default_visit(node)

  def visit_comparison_operator_node(self, node: ComparisonOperatorNode) -> str:
    return self.default_visit(node)

  def visit_concatenated_string_node(self, node: ConcatenatedStringNode) -> str:
    return self.default_visit(node)

  def visit_conditional_expression_node(self, node: ConditionalExpressionNode) -> str:
    return self.default_visit(node)

  def visit_continue_statement_node(self, node: ContinueStatementNode) -> str:
    return self.default_visit(node)

  def visit_decorated_definition_node(self, node: DecoratedDefinitionNode) -> str:
    return self.default_visit(node)

  def visit_decorator_node(self, node: DecoratorNode) -> str:
    return self.default_visit(node)

  def visit_default_parameter_node(self, node: DefaultParameterNode) -> str:
    return self.default_visit(node)

  def visit_delete_statement_node(self, node: DeleteStatementNode) -> str:
    return self.default_visit(node)

  def visit_dictionary_node(self, node: DictionaryNode) -> str:
    return self.default_visit(node)

  def visit_dictionary_comprehension_node(self, node: DictionaryComprehensionNode) -> str:
    return self.default_visit(node)

  def visit_dictionary_splat_node(self, node: DictionarySplatNode) -> str:
    return self.default_visit(node)

  def visit_dictionary_splat_pattern_node(self, node: DictionarySplatPatternNode) -> str:
    return self.default_visit(node)

  def visit_dotted_name_node(self, node: DottedNameNode) -> str:
    return self.default_visit(node)

  def visit_elif_clause_node(self, node: ElifClauseNode) -> str:
    return self.default_visit(node)

  def visit_ellipsis_node(self, node: EllipsisNode) -> str:
    return self.default_visit(node)

  def visit_else_clause_node(self, node: ElseClauseNode) -> str:
    return self.default_visit(node)

  def visit_escape_interpolation_node(self, node: EscapeInterpolationNode) -> str:
    return self.default_visit(node)

  def visit_escape_sequence_node(self, node: EscapeSequenceNode) -> str:
    return self.default_visit(node)

  def visit_except_clause_node(self, node: ExceptClauseNode) -> str:
    return self.default_visit(node)

  def visit_exec_statement_node(self, node: ExecStatementNode) -> str:
    return self.default_visit(node)

  def visit_expression_node(self, node: ExpressionNode) -> str:
    return self.default_visit(node)

  def visit_expression_list_node(self, node: ExpressionListNode) -> str:
    return self.default_visit(node)

  def visit_expression_statement_node(self, node: ExpressionStatementNode) -> str:
    return self.default_visit(node)

  def visit_false_node(self, node: FalseNode) -> str:
    return self.default_visit(node)

  def visit_finally_clause_node(self, node: FinallyClauseNode) -> str:
    return self.default_visit(node)

  def visit_float_node(self, node: FloatNode) -> str:
    return self.default_visit(node)

  def visit_for_in_clause_node(self, node: ForInClauseNode) -> str:
    return self.default_visit(node)

  def visit_for_statement_node(self, node: ForStatementNode) -> str:
    return self.default_visit(node)

  def visit_format_expression_node(self, node: FormatExpressionNode) -> str:
    return self.default_visit(node)

  def visit_format_specifier_node(self, node: FormatSpecifierNode) -> str:
    return self.default_visit(node)

  def visit_function_definition_node(self, node: FunctionDefinitionNode) -> str:
    return self.default_visit(node)

  def visit_future_import_statement_node(self, node: FutureImportStatementNode) -> str:
    return self.default_visit(node)

  def visit_generator_expression_node(self, node: GeneratorExpressionNode) -> str:
    return self.default_visit(node)

  def visit_global_statement_node(self, node: GlobalStatementNode) -> str:
    return self.default_visit(node)

  def visit_identifier_node(self, node: IdentifierNode) -> str:
    return self.default_visit(node)

  def visit_if_clause_node(self, node: IfClauseNode) -> str:
    return self.default_visit(node)

  def visit_if_statement_node(self, node: IfStatementNode) -> str:
    return self.default_visit(node)

  def visit_import_from_statement_node(self, node: ImportFromStatementNode) -> str:
    return self.default_visit(node)

  def visit_import_prefix_node(self, node: ImportPrefixNode) -> str:
    return self.default_visit(node)

  def visit_import_statement_node(self, node: ImportStatementNode) -> str:
    return self.default_visit(node)

  def visit_integer_node(self, node: IntegerNode) -> str:
    return self.default_visit(node)

  def visit_interpolation_node(self, node: InterpolationNode) -> str:
    return self.default_visit(node)

  def visit_keyword_argument_node(self, node: KeywordArgumentNode) -> str:
    return self.default_visit(node)

  def visit_keyword_identifier_node(self, node: KeywordIdentifierNode) -> str:
    return self.default_visit(node)

  def visit_lambda_node(self, node: LambdaNode) -> str:
    return self.default_visit(node)

  def visit_lambda_parameters_node(self, node: LambdaParametersNode) -> str:
    return self.default_visit(node)

  def visit_lambda_within_for_in_clause_node(self, node: LambdaWithinForInClauseNode) -> str:
    return self.default_visit(node)

  def visit_list_node(self, node: ListNode) -> str:
    return self.default_visit(node)

  def visit_list_comprehension_node(self, node: ListComprehensionNode) -> str:
    return self.default_visit(node)

  def visit_list_pattern_node(self, node: ListPatternNode) -> str:
    return self.default_visit(node)

  def visit_list_splat_node(self, node: ListSplatNode) -> str:
    return self.default_visit(node)

  def visit_list_splat_pattern_node(self, node: ListSplatPatternNode) -> str:
    return self.default_visit(node)

  def visit_module_node(self, node: ModuleNode) -> str:
    return self.default_visit(node, delimeter='\n')

  def visit_named_expression_node(self, node: NamedExpressionNode) -> str:
    return self.default_visit(node)

  def visit_none_node(self, node: NoneNode) -> str:
    return self.default_visit(node)

  def visit_nonlocal_statement_node(self, node: NonlocalStatementNode) -> str:
    return self.default_visit(node)

  def visit_not_escape_sequence_node(self, node: NotEscapeSequenceNode) -> str:
    return self.default_visit(node)

  def visit_not_operator_node(self, node: NotOperatorNode) -> str:
    return self.default_visit(node)

  def visit_pair_node(self, node: PairNode) -> str:
    return self.default_visit(node)

  def visit_parameter_node(self, node: ParameterNode) -> str:
    return self.default_visit(node)

  def visit_parameters_node(self, node: ParametersNode) -> str:
    return self.default_visit(node)

  def visit_parenthesized_expression_node(self, node: ParenthesizedExpressionNode) -> str:
    return self.default_visit(node)

  def visit_parenthesized_list_splat_node(self, node: ParenthesizedListSplatNode) -> str:
    return self.default_visit(node)

  def visit_pass_statement_node(self, node: PassStatementNode) -> str:
    return self.default_visit(node)

  def visit_pattern_node(self, node: PatternNode) -> str:
    return self.default_visit(node)

  def visit_pattern_list_node(self, node: PatternListNode) -> str:
    return self.default_visit(node)

  def visit_primary_expression_node(self, node: PrimaryExpressionNode) -> str:
    return self.default_visit(node)

  def visit_print_statement_node(self, node: PrintStatementNode) -> str:
    return self.default_visit(node)

  def visit_raise_statement_node(self, node: RaiseStatementNode) -> str:
    return self.default_visit(node)

  def visit_relative_import_node(self, node: RelativeImportNode) -> str:
    return self.default_visit(node)

  def visit_return_statement_node(self, node: ReturnStatementNode) -> str:
    return self.default_visit(node)

  def visit_set_node(self, node: SetNode) -> str:
    return self.default_visit(node)

  def visit_set_comprehension_node(self, node: SetComprehensionNode) -> str:
    return self.default_visit(node)

  def visit_slice_node(self, node: SliceNode) -> str:
    return self.default_visit(node)

  def visit_string_node(self, node: StringNode) -> str:
    return self.default_visit(node)

  def visit_subscript_node(self, node: SubscriptNode) -> str:
    return self.default_visit(node)

  def visit_true_node(self, node: TrueNode) -> str:
    return self.default_visit(node)

  def visit_try_statement_node(self, node: TryStatementNode) -> str:
    return self.default_visit(node)

  def visit_tuple_node(self, node: TupleNode) -> str:
    return self.default_visit(node)

  def visit_tuple_pattern_node(self, node: TuplePatternNode) -> str:
    return self.default_visit(node)

  def visit_type_node(self, node: TypeNode) -> str:
    return self.default_visit(node)

  def visit_type_conversion_node(self, node: TypeConversionNode) -> str:
    return self.default_visit(node)

  def visit_typed_default_parameter_node(self, node: TypedDefaultParameterNode) -> str:
    return self.default_visit(node)

  def visit_typed_parameter_node(self, node: TypedParameterNode) -> str:
    return self.default_visit(node)

  def visit_unary_operator_node(self, node: UnaryOperatorNode) -> str:
    return self.default_visit(node)

  def visit_while_statement_node(self, node: WhileStatementNode) -> str:
    return self.default_visit(node)

  def visit_wildcard_import_node(self, node: WildcardImportNode) -> str:
    return self.default_visit(node)

  def visit_with_clause_node(self, node: WithClauseNode) -> str:
    return self.default_visit(node)

  def visit_with_item_node(self, node: WithItemNode) -> str:
    return self.default_visit(node)

  def visit_with_statement_node(self, node: WithStatementNode) -> str:
    return self.default_visit(node)

  def visit_yield_node(self, node: YieldNode) -> str:
    return self.default_visit(node)


if __name__ == '__main__':
  ast = p_utils.read_json('temporary_gen_ast.json')
  tree = Tree.from_gen_ast(ast)
  pp = PrettyPrinter()
  code = tree.root_node.accept(pp)
  print(code)
