'''
This module provides classes for working with JavaScript ASTs.

Classes:
  - *Node: classes that represent nodes in a JavaScript AST
  - Tree: represents a JavaScript AST
  - PrettyPrinter: a visitor class that prints a JavaScript AST in a readable format
  - LogStatementInserter: a visitor class that inserts print statements in a JavaScript AST

Constants:
  - NODE_TYPES_CLASSES: dictionary that maps node types to their respective classes
  - NODES_WITH_FIELDS: list of node types that have fields
'''


from __future__ import annotations

import jsbeautifier
import tree_sitter
from typing import Dict, List, Union

import p_consts
import p_utils
import p_visitor as pvis


class _AugmentedAssignmentLhsNode(pvis.AbstractNode): pass
class _CallSignatureNode(pvis.AbstractNode): pass
class _DestructuringPatternNode(pvis.AbstractNode): pass
class _ExpressionsNode(pvis.AbstractNode): pass
class _ForHeaderNode(pvis.AbstractNode): pass
class _FormalParameterNode(pvis.AbstractNode): pass
class _FromClauseNode(pvis.AbstractNode): pass
class _IdentifierNode(pvis.AbstractNode): pass
class _ImportExportSpecifierNode(pvis.AbstractNode): pass
class _InitializerNode(pvis.AbstractNode): pass
class _JsxAttributeNode(pvis.AbstractNode): pass
class _JsxAttributeNameNode(pvis.AbstractNode): pass
class _JsxAttributeValueNode(pvis.AbstractNode): pass
class _JsxChildNode(pvis.AbstractNode): pass
class _JsxElementNode(pvis.AbstractNode): pass
class _JsxElementNameNode(pvis.AbstractNode): pass
class _JsxIdentifierNode(pvis.AbstractNode): pass
class _LhsExpressionNode(pvis.AbstractNode): pass
class _PropertyNameNode(pvis.AbstractNode): pass
class _ReservedIdentifierNode(pvis.AbstractNode): pass
class _SemicolonNode(pvis.AbstractNode): pass
class ArgumentsNode(pvis.AbstractNode): pass
class ArrayNode(pvis.AbstractNode): pass
class ArrayPatternNode(pvis.AbstractNode): pass
class ArrowFunctionNode(pvis.AbstractNode): pass
class AssignmentExpressionNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.left : pvis.AbstractNode = None
    self.right : pvis.AbstractNode = None
class AssignmentPatternNode(pvis.AbstractNode): pass
class AugmentedAssignmentExpressionNode(pvis.AbstractNode): pass
class AwaitExpressionNode(pvis.AbstractNode): pass
class BinaryExpressionNode(pvis.AbstractNode): pass
class BreakStatementNode(pvis.AbstractNode): pass
class CallExpressionNode(pvis.AbstractNode): pass
class CatchClauseNode(pvis.AbstractNode): pass
class ClassNode(pvis.AbstractNode): pass
class ClassBodyNode(pvis.AbstractNode): pass
class ClassDeclarationNode(pvis.AbstractNode): pass
class ClassHeritageNode(pvis.AbstractNode): pass
class CommentNode(pvis.AbstractNode): pass
class ComputedPropertyNameNode(pvis.AbstractNode): pass
class ContinueStatementNode(pvis.AbstractNode): pass
class DebuggerStatementNode(pvis.AbstractNode): pass
class DeclarationNode(pvis.AbstractNode): pass
class DecoratorNode(pvis.AbstractNode): pass
class DecoratorCallExpressionNode(pvis.AbstractNode): pass
class DecoratorMemberExpressionNode(pvis.AbstractNode): pass
class DoStatementNode(pvis.AbstractNode): pass
class ElseClauseNode(pvis.AbstractNode): pass
class EmptyStatementNode(pvis.AbstractNode): pass
class EscapeSequenceNode(pvis.AbstractNode): pass
class ExportClauseNode(pvis.AbstractNode): pass
class ExportStatementNode(pvis.AbstractNode): pass
class ExpressionNode(pvis.AbstractNode): pass
class ExpressionStatementNode(pvis.AbstractNode): pass
class FalseNode(pvis.AbstractNode): pass
class FieldDefinitionNode(pvis.AbstractNode): pass
class FinallyClauseNode(pvis.AbstractNode): pass
class ForInStatementNode(pvis.AbstractNode): pass
class ForStatementNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.initializer : pvis.AbstractNode = None
    self.condition : pvis.AbstractNode = None
    self.increment : pvis.AbstractNode = None
    self.body : pvis.AbstractNode = None
class FormalParametersNode(pvis.AbstractNode): pass
class FunctionNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.name : pvis.AbstractNode = None
    self.parameters : pvis.AbstractNode = None
    self.body : pvis.AbstractNode = None
class FunctionDeclarationNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.name : pvis.AbstractNode = None
    self.parameters : pvis.AbstractNode = None
    self.body : pvis.AbstractNode = None
class GeneratorFunctionNode(pvis.AbstractNode): pass
class GeneratorFunctionDeclarationNode(pvis.AbstractNode): pass
class HashBangLineNode(pvis.AbstractNode): pass
class IdentifierNode(pvis.AbstractNode):
  def __init__(self, node_type: str):
    super().__init__(node_type)
  def __repr__(self) -> str:
    return f'ID({self.val()})'
  def val(self) -> str:
    assert len(self.children) == 1, 'sanity check'
    assert isinstance(self.children[0], pvis.TerminalNode), 'sanity check'
    return self.children[0].node_type
class IfStatementNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.condition : pvis.AbstractNode = None
    self.consequence : pvis.AbstractNode = None
    self.alternative : pvis.AbstractNode = None
class ImportNode(pvis.AbstractNode): pass
class ImportClauseNode(pvis.AbstractNode): pass
class ImportStatementNode(pvis.AbstractNode): pass
class JsxAttributeNode(pvis.AbstractNode): pass
class JsxClosingElementNode(pvis.AbstractNode): pass
class JsxElementNode(pvis.AbstractNode): pass
class JsxExpressionNode(pvis.AbstractNode): pass
class JsxFragmentNode(pvis.AbstractNode): pass
class JsxIdentifierNode(pvis.AbstractNode): pass
class JsxNamespaceNameNode(pvis.AbstractNode): pass
class JsxOpeningElementNode(pvis.AbstractNode): pass
class JsxSelfClosingElementNode(pvis.AbstractNode): pass
class JsxTextNode(pvis.AbstractNode): pass
class LabeledStatementNode(pvis.AbstractNode): pass
class LexicalDeclarationNode(pvis.AbstractNode): pass
class MemberExpressionNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.object : pvis.AbstractNode = None
    self.property : pvis.AbstractNode = None
class MetaPropertyNode(pvis.AbstractNode): pass
class MethodDefinitionNode(pvis.AbstractNode): pass
class NamedImportsNode(pvis.AbstractNode): pass
class NamespaceImportExportNode(pvis.AbstractNode): pass
class NestedIdentifierNode(pvis.AbstractNode): pass
class NewExpressionNode(pvis.AbstractNode): pass
class NullNode(pvis.AbstractNode): pass
class NumberNode(pvis.AbstractNode): pass
class ObjectNode(pvis.AbstractNode): pass
class ObjectAssignmentPatternNode(pvis.AbstractNode): pass
class ObjectPatternNode(pvis.AbstractNode): pass
class PairNode(pvis.AbstractNode): pass
class PairPatternNode(pvis.AbstractNode): pass
class ParenthesizedExpressionNode(pvis.AbstractNode): pass
class PatternNode(pvis.AbstractNode): pass
class PrimaryExpressionNode(pvis.AbstractNode): pass
class PrivatePropertyIdentifierNode(pvis.AbstractNode): pass
class ProgramNode(pvis.AbstractNode): pass
class RegexNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.pattern : pvis.AbstractNode = None
    self.flags : pvis.AbstractNode = None
class RegexFlagsNode(pvis.AbstractNode): pass
class RegexPatternNode(pvis.AbstractNode): pass
class RestPatternNode(pvis.AbstractNode): pass
class ReturnStatementNode(pvis.AbstractNode): pass
class SequenceExpressionNode(pvis.AbstractNode): pass
class SpreadElementNode(pvis.AbstractNode): pass
class StatementNode(pvis.AbstractNode): pass
class StatementBlockNode(pvis.AbstractNode): pass
class StringNode(pvis.AbstractNode): pass
class SubscriptExpressionNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.object : pvis.AbstractNode = None
    self.index : pvis.AbstractNode = None
class SuperNode(pvis.AbstractNode): pass
class SwitchBodyNode(pvis.AbstractNode): pass
class SwitchCaseNode(pvis.AbstractNode): pass
class SwitchDefaultNode(pvis.AbstractNode): pass
class SwitchStatementNode(pvis.AbstractNode): pass
class TemplateStringNode(pvis.AbstractNode): pass
class TemplateSubstitutionNode(pvis.AbstractNode): pass
class TernaryExpressionNode(pvis.AbstractNode): pass
class ThisNode(pvis.AbstractNode): pass
class ThrowStatementNode(pvis.AbstractNode): pass
class TrueNode(pvis.AbstractNode): pass
class TryStatementNode(pvis.AbstractNode): pass
class UnaryExpressionNode(pvis.AbstractNode): pass
class UndefinedNode(pvis.AbstractNode): pass
class UnescapedDoubleStringFragmentNode(pvis.AbstractNode): pass
class UnescapedSingleStringFragmentNode(pvis.AbstractNode): pass
class UpdateExpressionNode(pvis.AbstractNode): pass
class VariableDeclarationNode(pvis.AbstractNode): pass
class VariableDeclaratorNode(pvis.AbstractNode):
  def __init__(self, node_type):
    super().__init__(node_type)
    self.name : pvis.AbstractNode = None
    self.value : pvis.AbstractNode = None
class WhileStatementNode(pvis.AbstractNode): pass
class WithStatementNode(pvis.AbstractNode): pass
class YieldExpressionNode(pvis.AbstractNode): pass

# CLASSES FOR EXTERNAL NODES
class TemplateCharsNode(pvis.AbstractNode): pass


NODE_TYPES_CLASSES: Dict[str, pvis.AbstractNode] = {
  'terminal': pvis.TerminalNode,
  '_augmented_assignment_lhs': _AugmentedAssignmentLhsNode,
  '_call_signature': _CallSignatureNode,
  '_destructuring_pattern': _DestructuringPatternNode,
  '_expressions': _ExpressionsNode,
  '_for_header': _ForHeaderNode,
  '_formal_parameter': _FormalParameterNode,
  '_from_clause': _FromClauseNode,
  '_identifier': _IdentifierNode,
  '_import_export_specifier': _ImportExportSpecifierNode,
  '_initializer': _InitializerNode,
  '_jsx_attribute': _JsxAttributeNode,
  '_jsx_attribute_name': _JsxAttributeNameNode,
  '_jsx_attribute_value': _JsxAttributeValueNode,
  '_jsx_child': _JsxChildNode,
  '_jsx_element': _JsxElementNode,
  '_jsx_element_name': _JsxElementNameNode,
  '_jsx_identifier': _JsxIdentifierNode,
  '_lhs_expression': _LhsExpressionNode,
  '_property_name': _PropertyNameNode,
  '_reserved_identifier': _ReservedIdentifierNode,
  '_semicolon': _SemicolonNode,
  'arguments': ArgumentsNode,
  'array': ArrayNode,
  'array_pattern': ArrayPatternNode,
  'arrow_function': ArrowFunctionNode,
  'assignment_expression': AssignmentExpressionNode,
  'assignment_pattern': AssignmentPatternNode,
  'augmented_assignment_expression': AugmentedAssignmentExpressionNode,
  'await_expression': AwaitExpressionNode,
  'binary_expression': BinaryExpressionNode,
  'break_statement': BreakStatementNode,
  'call_expression': CallExpressionNode,
  'catch_clause': CatchClauseNode,
  'class': ClassNode,
  'class_body': ClassBodyNode,
  'class_declaration': ClassDeclarationNode,
  'class_heritage': ClassHeritageNode,
  'comment': CommentNode,
  'computed_property_name': ComputedPropertyNameNode,
  'continue_statement': ContinueStatementNode,
  'debugger_statement': DebuggerStatementNode,
  'declaration': DeclarationNode,
  'decorator': DecoratorNode,
  'decorator_call_expression': DecoratorCallExpressionNode,
  'decorator_member_expression': DecoratorMemberExpressionNode,
  'do_statement': DoStatementNode,
  'else_clause': ElseClauseNode,
  'empty_statement': EmptyStatementNode,
  'escape_sequence': EscapeSequenceNode,
  'export_clause': ExportClauseNode,
  'export_statement': ExportStatementNode,
  'expression': ExpressionNode,
  'expression_statement': ExpressionStatementNode,
  'false': FalseNode,
  'field_definition': FieldDefinitionNode,
  'finally_clause': FinallyClauseNode,
  'for_in_statement': ForInStatementNode,
  'for_statement': ForStatementNode,
  'formal_parameters': FormalParametersNode,
  'function': FunctionNode,
  'function_declaration': FunctionDeclarationNode,
  'generator_function': GeneratorFunctionNode,
  'generator_function_declaration': GeneratorFunctionDeclarationNode,
  'hash_bang_line': HashBangLineNode,
  'identifier': IdentifierNode,
  'if_statement': IfStatementNode,
  'import': ImportNode,
  'import_clause': ImportClauseNode,
  'import_statement': ImportStatementNode,
  'jsx_attribute': JsxAttributeNode,
  'jsx_closing_element': JsxClosingElementNode,
  'jsx_element': JsxElementNode,
  'jsx_expression': JsxExpressionNode,
  'jsx_fragment': JsxFragmentNode,
  'jsx_identifier': JsxIdentifierNode,
  'jsx_namespace_name': JsxNamespaceNameNode,
  'jsx_opening_element': JsxOpeningElementNode,
  'jsx_self_closing_element': JsxSelfClosingElementNode,
  'jsx_text': JsxTextNode,
  'labeled_statement': LabeledStatementNode,
  'lexical_declaration': LexicalDeclarationNode,
  'member_expression': MemberExpressionNode,
  'meta_property': MetaPropertyNode,
  'method_definition': MethodDefinitionNode,
  'named_imports': NamedImportsNode,
  'namespace_import_export': NamespaceImportExportNode,
  'nested_identifier': NestedIdentifierNode,
  'new_expression': NewExpressionNode,
  'null': NullNode,
  'number': NumberNode,
  'object': ObjectNode,
  'object_assignment_pattern': ObjectAssignmentPatternNode,
  'object_pattern': ObjectPatternNode,
  'pair': PairNode,
  'pair_pattern': PairPatternNode,
  'parenthesized_expression': ParenthesizedExpressionNode,
  'pattern': PatternNode,
  'primary_expression': PrimaryExpressionNode,
  'private_property_identifier': PrivatePropertyIdentifierNode,
  'program': ProgramNode,
  'regex': RegexNode,
  'regex_flags': RegexFlagsNode,
  'regex_pattern': RegexPatternNode,
  'rest_pattern': RestPatternNode,
  'return_statement': ReturnStatementNode,
  'sequence_expression': SequenceExpressionNode,
  'spread_element': SpreadElementNode,
  'statement': StatementNode,
  'statement_block': StatementBlockNode,
  'string': StringNode,
  'subscript_expression': SubscriptExpressionNode,
  'super': SuperNode,
  'switch_body': SwitchBodyNode,
  'switch_case': SwitchCaseNode,
  'switch_default': SwitchDefaultNode,
  'switch_statement': SwitchStatementNode,
  'template_string': TemplateStringNode,
  'template_substitution': TemplateSubstitutionNode,
  'ternary_expression': TernaryExpressionNode,
  'this': ThisNode,
  'throw_statement': ThrowStatementNode,
  'true': TrueNode,
  'try_statement': TryStatementNode,
  'unary_expression': UnaryExpressionNode,
  'undefined': UndefinedNode,
  'unescaped_double_string_fragment': UnescapedDoubleStringFragmentNode,
  'unescaped_single_string_fragment': UnescapedSingleStringFragmentNode,
  'update_expression': UpdateExpressionNode,
  'variable_declaration': VariableDeclarationNode,
  'variable_declarator': VariableDeclaratorNode,
  'while_statement': WhileStatementNode,
  'with_statement': WithStatementNode,
  'yield_expression': YieldExpressionNode,

  # aliases
  'property_identifier': IdentifierNode,
  'shorthand_property_identifier': IdentifierNode,
  'shorthand_property_identifier_pattern': IdentifierNode,
  'statement_identifier': IdentifierNode,
  'string_fragment': UnescapedDoubleStringFragmentNode,

  # externals
  'template_chars': TemplateCharsNode,
}

NODES_WITH_FIELDS = [
  'assignment_expression',
  'for_statement',
  'function',
  'function_declaration',
  'if_statement',
  'member_expression',
  'regex',
  'subscript_expression',
  'variable_declarator',
]


class Tree:
  '''
  Class that represents an JavaScript AST.
  This class is compatible with `pvis.Visitor` classes.
  '''
  def __init__(self, root_node: pvis.AbstractNode) -> None:
    self.root_node: pvis.AbstractNode = root_node

  def __repr__(self) -> str:
    return f'Tree({self.root_node.node_type})'

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

    def _create_node_with_field(ts_node: tree_sitter.Node) -> pvis.AbstractNode:
      '''
      Special treatment for some nodes in tree-sitter trees.
      What is special about these nodes? They have fields.
      Their fields must be registered as attributes in their respective
      classes (see `AssignmentNode` for example). This special treatment
      allows us to access fields of these classes as attributes.
      Check `NODES_WITH_FIELDS` for the list of special nodes.
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
        # NOTE can achieve the same result by using `child_by_field_id`
        # which fails to work in the current tree-sitter version
        # and is fixed in the latest version as of Mar 2025.
        # TODO what to do with multiple nodes under a single field name?
        for part_fld_name in ts_field_names:
          part_child_node = ts_node.child_by_field_name(part_fld_name)
          if part_child_node == ts_child:
            setattr(node_wfield, part_fld_name, child_node)

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


class PrettyPrinter(pvis.Visitor):
  # VISITOR METHODS
  def default_visit(self, node: pvis.AbstractNode, delimiter: str = ' ') -> str:
    code = ''
    for child in node.children:
      child_code = self.visit(child)
      code += child_code + delimiter
    return code.strip()

  def visit_ArgumentsNode(self, node: ArgumentsNode) -> str:
    assert node.children[0].is_terminal() and node.children[0].node_type == '(', 'sanity check: ( is terminal node'
    assert node.children[-1].is_terminal() and node.children[-1].node_type == ')', 'sanity check: ) is terminal node'
    arg_nodes = [ch for ch in node.children[1:-1] if ch.is_nonterminal() or ch.node_type in ['null', 'true', 'false']]
    args = ', '.join([self.visit(child) for child in arg_nodes])
    return f'({args})'

  def visit_CallExpressionNode(self, node: CallExpressionNode) -> str:
    return self.default_visit(node, delimiter='')

  def visit_MemberExpressionNode(self, node: MemberExpressionNode) -> str:
    obj = self.visit(node.object)
    assert node.children[1].is_terminal(), 'sanity check: property is terminal node'
    assert node.children[1].node_type in ['.', '?.'], 'sanity check: property is . or ?.'
    chaining_op = self.visit(node.children[1])
    prop = self.visit(node.property)
    return f'{obj}{chaining_op}{prop}'

  def visit_ProgramNode(self, node: ProgramNode) -> str:
    entire_code = self.default_visit(node, delimiter='\n')
    # delegate (almost) all pretty printing to jsbeautifier
    return jsbeautifier.beautify(entire_code)

  def visit_RegexNode(self, node: RegexNode) -> str:
    '''
    regex: $ => seq(
      '/',
      field('pattern', $.regex_pattern),
      token.immediate('/'),
      optional(field('flags', $.regex_flags))
    ),
    '''
    pattern = self.visit(node.pattern)
    flags = '' if node.flags is None else self.visit(node.flags)
    return f'/{pattern}/{flags}'

  def visit_StringNode(self, node: StringNode) -> str:
    return self.default_visit(node, delimiter='')

  def visit_SubscriptExpressionNode(self, node: SubscriptExpressionNode) -> str:
    '''
    NOTE As far as I remember, this whole implementation is written
    because the jsbeautifier library could not handle subscript expressions properly.

    subscript_expression: $ => prec.right('member', seq(
      field('object', choice($.expression, $.primary_expression)),
      optional('?.'),
      '[', field('index', $._expressions), ']'
    )),
    '''
    child_cursor = node.children[0]

    assert node.object == child_cursor, 'sanity check: object is the first child'
    obj = self.visit(node.object)

    child_cursor = child_cursor.next_sibling()
    chaining_op = ''
    if child_cursor.is_terminal() and child_cursor.node_type == '?.':
      chaining_op = self.visit(child_cursor)
      child_cursor = child_cursor.next_sibling()

    assert child_cursor.is_terminal() and child_cursor.node_type == '[', 'sanity check: [ is terminal node'

    child_cursor = child_cursor.next_sibling()
    index = self.visit(child_cursor)

    child_cursor = child_cursor.next_sibling()
    assert child_cursor.is_terminal() and child_cursor.node_type == ']', 'sanity check: ] is terminal node'
    return f'{obj}{chaining_op}[{index}]'

  def visit_TemplateCharsNode(self, node: TemplateCharsNode) -> str:
    assert len(node.children) == 1, 'sanity check: only one child'
    assert isinstance(node.children[0], pvis.TerminalNode), 'sanity check: child is terminal node'
    return node.children[0].node_type

  def visit_TemplateStringNode(self, node: TemplateStringNode) -> str:
    return self.default_visit(node, delimiter='')

  def visit_TemplateSubstitutionNode(self, node: TemplateSubstitutionNode) -> str:
    return self.default_visit(node, delimiter='')

  def visit_TerminalNode(self, node: pvis.TerminalNode) -> str:
    return node.node_type

  def visit_UnaryExpressionNode(self, node: UnaryExpressionNode) -> str:
    '''
    unary_expression: $ => prec.left('unary_void', seq(
      field('operator', choice('!', '~', '-', '+', 'typeof', 'void', 'delete')),
      field('argument', $.expression)
    )),
    '''
    # the following unary operators should be separated by a space
    if node.children[0].is_terminal() and node.children[0].node_type in ['delete', 'void', 'typeof']:
      return self.default_visit(node, delimiter=' ')
    return self.default_visit(node, delimiter='')

  def visit_UnescapedDoubleStringFragmentNode(self, node: UnescapedDoubleStringFragmentNode) -> str:
    assert node.children[0].is_terminal(), 'sanity check: child is terminal node'
    return node.children[0].node_type


class LogStatementInserter(pvis.Visitor):
  '''
  Assume that the LogStatementInserter works on a test script,
  which contains test function, tested function, and test function invocation.
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
  def build_CallExpressionNode(self, function: MemberExpressionNode, arguments: ArgumentsNode) -> CallExpressionNode:
    '''
    console.log(JSON.stringify(obj, null, 2));
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    call_expression
      function: <member_expression>
      arguments: <arguments>
    '''
    assert isinstance(function, MemberExpressionNode), 'function must be a MemberExpressionNode'
    assert isinstance(arguments, ArgumentsNode), 'arguments must be an ArgumentsNode'

    # level 0
    call_expression = CallExpressionNode('call_expression')

    # level 1
    call_expression.add_child(function)
    function.set_parent(call_expression)

    call_expression.add_child(arguments)
    arguments.set_parent(call_expression)

    return call_expression

  def build_MemberExpressionNode(self, obj: str, prop: str) -> MemberExpressionNode:
    '''
    console.log(JSON.stringify(obj, null, 2));
                ^^^^^^^^^^^^^^
    member_expression
      object: identifier 'JSON'
      '.'
      property: property_identifier 'stringify'

    NOTE property_identifier is an alias for identifier
    '''
    assert isinstance(obj, str), 'obj must be a string'
    assert isinstance(prop, str), 'prop must be a string'

    # level 0
    member_expression = MemberExpressionNode('member_expression')

    # level 1
    identifier = self.build_IdentifierNode(obj)
    member_expression.object = identifier
    member_expression.add_child(identifier)
    identifier.set_parent(member_expression)

    dot = pvis.TerminalNode('.')
    member_expression.add_child(dot)
    dot.set_parent(member_expression)

    property_identifier = self.build_IdentifierNode(prop)
    member_expression.property = property_identifier
    member_expression.add_child(property_identifier)
    property_identifier.set_parent(member_expression)

    return member_expression

  def build_IdentifierNode(self, val: str) -> IdentifierNode:
    assert isinstance(val, str), 'val must be a string'
    identifier = IdentifierNode('identifier')
    terminal = pvis.TerminalNode(val)
    identifier.add_child(terminal)
    terminal.set_parent(identifier)
    return identifier

  def build_NumberNode(self, val: Union[str, int, float]) -> NumberNode:
    assert isinstance(val, (str, int, float)), 'val must be a string, integer, or float'
    number = NumberNode('number')
    terminal = pvis.TerminalNode(val if isinstance(val, str) else str(val))
    number.add_child(terminal)
    terminal.set_parent(number)
    return number

  def build_StringNode(self, val: str) -> StringNode:
    assert isinstance(val, str), 'val must be a string'
    string = StringNode('string')
    terminal = pvis.TerminalNode(f"'{val}'")
    string.add_child(terminal)
    terminal.set_parent(string)
    return string

  def build_ArgumentsNode(self, args: List[pvis.AbstractNode]) -> ArgumentsNode:
    '''
    console.log(JSON.stringify(obj, null, 2));
                              ^^^^^^^^^^^^^^
    arguments
      '('
      <arg>
      ','
      <arg>
      ','
      <arg>
      ')'
    '''

    _SUPPORTED_ARG_TYPES = [
      'call_expression',
      'identifier',
      'null',
      'number',
      'string',
    ]
    for arg in args:
      assert arg.node_type in _SUPPORTED_ARG_TYPES, f'unsupported argument type: {arg.node_type}'

    # level 0
    arguments = ArgumentsNode('arguments')

    # level 1
    lparen = pvis.TerminalNode('(')
    arguments.add_child(lparen)
    lparen.set_parent(arguments)

    for idx, arg in enumerate(args):
      arguments.add_child(arg)
      arg.set_parent(arguments)

      if idx != len(args) - 1:
        comma = pvis.TerminalNode(',')
        arguments.add_child(comma)
        comma.set_parent(arguments)

    rparen = pvis.TerminalNode(')')
    arguments.add_child(rparen)
    rparen.set_parent(arguments)

    return arguments

  def build_ArrayNode(self, elements: List[pvis.AbstractNode]) -> ArrayNode:
    '''
    [1, 2, 3]

    array
      *
      *
    '''
    _SUPPORTED_ELEMENT_TYPES = [
      IdentifierNode,
      NumberNode,
    ]
    for elem in elements:
      assert isinstance(elem, tuple(_SUPPORTED_ELEMENT_TYPES)), f'Unsupported element type: {type(elem)}'

    # level 0
    array_node = ArrayNode('array')

    # level 1
    open_br = pvis.TerminalNode('[')
    array_node.add_child(open_br)
    open_br.set_parent(array_node)

    for idx, elem in enumerate(elements):
      array_node.add_child(elem)
      elem.set_parent(array_node)

      # add comma if not the last element
      if idx != len(elements) - 1:
        comma = pvis.TerminalNode(',')
        array_node.add_child(comma)
        comma.set_parent(array_node)

    clos_br = pvis.TerminalNode(']')
    array_node.add_child(clos_br)
    clos_br.set_parent(array_node)

    return array_node

  # LOG STATEMENT BUILDER METHOD
  def build_ArgLogStatement(self, arg: pvis.AbstractNode) -> ExpressionStatementNode:
    '''
    Build a print statement with the given argument where `arg`
    can be any `AbstractNode` instance (as long as it respects grammar).

    console.log(JSON.stringify(obj, null, 2));

    expression_statement
      call_expression1
        function: member_expression1
          object: identifier1 'console'
          '.'
          property: property_identifier1 'log'
        arguments: arguments1
          '('
          call_expression2
            function: member_expression2
              object: identifier2 'JSON'
              '.'
              property: property_identifier2 'stringify'
            arguments: arguments2
              '('
              identifier3 'obj'
              ','
              'null'
              ','
              number '2'
              ')'
          ')'
      ';'
    '''
    _SUPPORTED_TYPES = [
      IdentifierNode,
      NumberNode,
      StringNode,
    ]

    assert isinstance(arg, tuple(_SUPPORTED_TYPES)), f'unsupported argument type: {arg.node_type}'

    # build bottom-up
    arguments2 = self.build_ArgumentsNode([arg, pvis.TerminalNode('null'), self.build_NumberNode(2)])
    member_expression2 = self.build_MemberExpressionNode('JSON', 'stringify')
    call_expression2 = self.build_CallExpressionNode(member_expression2, arguments2)
    arguments1 = self.build_ArgumentsNode([call_expression2])
    member_expression1 = self.build_MemberExpressionNode('console', 'log')
    call_expression1 = self.build_CallExpressionNode(member_expression1, arguments1)

    expression_statement = ExpressionStatementNode('expression_statement')
    expression_statement.add_child(call_expression1)
    call_expression1.set_parent(expression_statement)

    semicolon = pvis.TerminalNode(';')
    expression_statement.add_child(semicolon)
    semicolon.set_parent(expression_statement)

    return expression_statement

  # VISIT METHODS
  def visit_ProgramNode(self, node: ProgramNode) -> None:
    '''
    Given a top-level `program` node, find the function definition
    with the name `self.function_name` and visit it.
    '''
    function_declarations = [child for child in node.children if isinstance(child, FunctionDeclarationNode)]
    assert len(function_declarations), 'no function declarations found'
    fgold_fns = [fn for fn in function_declarations if fn.name.val() == self.function_name]
    assert len(fgold_fns) > 0, 'broken precondition: f_gold function not found'
    assert len(fgold_fns) == 1, 'broken precondition: multiple f_gold functions found'
    fgold_fn = fgold_fns[0]
    self.visit(fgold_fn)

  def visit_ForStatementNode(self, node: ForStatementNode) -> None:
    '''
    Insert print statements at the beginning of the for statement.

    NOTE for both for and if statements, it is possible that the consequence/body
    is just a single statement, in which case parentheses are not required.
    If we are inserting a log statement, we need to wrap the statement in parentheses
    alongside with the log statement. TODO
    '''
    for child in node.get_nt_children():
      self.visit(child)
    log_statement = self.build_ArgLogStatement(self.build_StringNode(f'for #{self.for_counter}'))
    self.for_counter += 1
    node.body.children.insert(1, log_statement)

  def visit_FunctionDeclarationNode(self, node: FunctionDeclarationNode) -> None:
    '''
    Given a function declaration node, visit its body and insert print statements.
    '''
    self.visit(node.body)

  def visit_IfStatementNode(self, node: IfStatementNode) -> None:
    '''
    Insert print statements at the beginning of the if statement.
    '''
    for child in node.get_nt_children():
      self.visit(child)
    log_statement = self.build_ArgLogStatement(self.build_StringNode(f'if #{self.if_counter}'))
    self.if_counter += 1
    node.consequence.children.insert(1, log_statement)

  def visit_StatementBlockNode(self, node: StatementBlockNode) -> None:
    '''
    Insert log statements after assignment statements.
    Assignment appear only under block nodes (?)
    '''
    idx = 0
    while idx < len(node.children):
      child = node.children[idx]

      if child.is_terminal():
        idx += 1
        continue

      # visit the child
      self.visit(child)

      # check if child is a top-level node for assignment
      if not child.node_type in ['lexical_declaration', 'variable_declaration', 'expression_statement']:
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


class AssignedIdentifierExtractor(pvis.Visitor):
  '''
  Given a child node of a statement node, specifically
  lexical_declaration, variable_declaration, or expression_statement,
  extract all assigned identifiers from the node.
  '''
  '''TREE-SITTER GRAMMAR RULES ASSOCIATED WITH ASSIGNMENT:

  lexical_declaration: $ => seq(
    field('kind', choice('let', 'const')),
    commaSep1($.variable_declarator),
    $._semicolon
  ),

  variable_declaration: $ => seq(
    'var',
    commaSep1($.variable_declarator),
    $._semicolon
  ),

  variable_declarator: $ => seq(
    field('name', choice($.identifier, $._destructuring_pattern)),
    optional($._initializer)
  ),

  _destructuring_pattern: $ => choice(
    $.object_pattern,
    $.array_pattern
  ),

  _initializer: $ => seq(
    '=',
    field('value', $.expression)
  ),


  assignment_expression: $ => prec.right('assign', seq(
    field('left', choice($.parenthesized_expression, $._lhs_expression)),
    '=',
    field('right', $.expression)
  )),

  augmented_assignment_expression: $ => prec.right('assign', seq(
    field('left', $._augmented_assignment_lhs),
    field('operator', choice('+=', '-=', '*=', '/=', '%=', '^=', '&=', '|=', '>>=', '>>>=',
                              '<<=', '**=', '&&=', '||=', '??=')),
    field('right', $.expression)
  )),

  _lhs_expression: $ => choice(
    $.member_expression,
    $.subscript_expression,
    $._identifier,
    alias($._reserved_identifier, $.identifier),
    $._destructuring_pattern
  ),

  _augmented_assignment_lhs: $ => choice(
    $.member_expression,
    $.subscript_expression,
    alias($._reserved_identifier, $.identifier),
    $.identifier,
    $.parenthesized_expression,
  ),
  '''
  '''EXAMPLES:

  `let x = 10;`
  `const y = 30;`
  lexical_declaration
    kind: let|const
    variable_declarator
      name: identifier
      value: number

  `let [x, y] = [1, 2];`
  lexical_declaration
    kind: let
    variable_declarator
      name: array_pattern '[x, y]'
      value: array '[1, 2]'

  `let {name, age} = {name: "Alice", age: 30};`
  lexical_declaration
    kind: let
    variable_declarator
      name: object_pattern '{name, age}'
      value: object '{name: "Alice", age: 30}'

  `var z = 50;`
  variable_declaration
    var
    variable_declarator
      name: identifier 'z'
      value: number '50'

  `x = 20;`
  expression_statement
    assignment_expression
      left: identifier
      right: number

  `obj.age = 2;`
  expression_statement
    assignment_expression
      left: member_expression
        object: identifier
        .
        property: property_identifier
      =
      right: number
    ;

  `arr[0] = 100;`
  expression_statement
    assignment_expression
      left: subscript_expression
        object: identifier

        index: number
        ]
      =
      right: number
    ;

  `Object.assign(target, source);`
  expression_statement
    call_expression
      function: member_expression
        object: identifier
        .
        property: property_identifier
      arguments: arguments
        (
        identifier
        ,
        identifier
        )
    ;
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

  def visit_AssignmentExpressionNode(self, node: AssignmentExpressionNode) -> None:
    '''
    assignment_expression: $ => prec.right('assign', seq(
      field('left', choice($.parenthesized_expression, $._lhs_expression)),
      '=',
      field('right', $.expression)
    )),
    '''
    self.visit(node.left)

  def visit_ExpressionStatementNode(self, node: ExpressionStatementNode) -> None:
    '''
    Extract the assigned identifiers from the expression statement node.

    expression: $ => choice(
      $.primary_expression,
      $._jsx_element,
      $.jsx_fragment,
      $.assignment_expression,
      $.augmented_assignment_expression,
      $.await_expression,
      $.unary_expression,
      $.binary_expression,
      $.ternary_expression,
      $.update_expression,
      $.new_expression,
      $.yield_expression,
    ),
    '''
    _ASSIGNMENT_RELATED_NODES = [
      AssignmentExpressionNode,
      AugmentedAssignmentExpressionNode,
      UpdateExpressionNode,
    ]

    nt_children = node.get_nt_children()
    assert len(nt_children) == 1, 'sanity check: expression statement has one child'
    child = nt_children[0]

    # visit only the following children of expression_statement
    if isinstance(child, tuple(_ASSIGNMENT_RELATED_NODES)):
      self.visit(child)

  def visit_IdentifierNode(self, node: IdentifierNode) -> None:
    self.add_assigned_identifier(node.val())

  def visit_LexicalDeclarationNode(self, node: LexicalDeclarationNode) -> None:
    '''
    lexical_declaration: $ => seq(
      field('kind', choice('let', 'const')),
      commaSep1($.variable_declarator),
      $._semicolon
    ),
    '''
    var_declarators = [child for child in node.children if isinstance(child, VariableDeclaratorNode)]
    for var_declarator in var_declarators:
      self.visit(var_declarator)

  def visit_SubscriptExpressionNode(self, node: SubscriptExpressionNode) -> None:
    '''
    subscript_expression: $ => prec.right('member', seq(
      field('object', choice($.expression, $.primary_expression)),
      optional('?.'),
      '[', field('index', $._expressions), ']'
    )),
    '''
    self.visit(node.object)

  def visit_VariableDeclarationNode(self, node: VariableDeclarationNode) -> None:
    '''
    variable_declaration: $ => seq(
      'var',
      commaSep1($.variable_declarator),
      $._semicolon
    ),
    '''
    var_declarators = [child for child in node.children if isinstance(child, VariableDeclaratorNode)]
    for var_declarator in var_declarators:
      self.visit(var_declarator)

  def visit_VariableDeclaratorNode(self, node: VariableDeclaratorNode) -> None:
    '''
    variable_declarator: $ => seq(
      field('name', choice($.identifier, $._destructuring_pattern)),
      optional($._initializer)
    ),
    _destructuring_pattern: $ => choice(
      $.object_pattern,
      $.array_pattern
    ),
    _initializer: $ => seq(
      '=',
      field('value', $.expression)
    ),
    '''
    # just a variable declaration without initialization (e.g. `let x;`)
    if node.value is None:
      return
    self.visit(node.name)


# TEST HARNESSES
def _get_js_boilerplate_code():
  '''
  Generate boilerplate code for NODE_TYPES_CLASSES and NODES_WITH_FIELDS
  '''
  import p_grammar
  import p_consts

  lang = 'js'
  gr_obj = p_consts.GRAMMAR_DICT_READONLY[lang]
  grammar = p_grammar.TreeSitterGrammar.from_dict(gr_obj)

  cls_template = """class {clsname}(pvis.AbstractNode): pass"""
  ntcls_template = """  '{ntype}': {clsname},"""

  for rule in sorted(grammar.rules.keys()):
    ntype = rule
    clsname = p_utils.to_camel_case(ntype)
    print(cls_template.format(clsname=clsname))

  for rule in sorted(grammar.rules.keys()):
    ntype = rule
    clsname = p_utils.to_camel_case(ntype)
    print(ntcls_template.format(ntype=ntype, clsname=clsname))


def _test_pretty_printer():
  snippet = p_utils.read_tmp_text('test_pp.js')
  src_lang = 'js'

  parser = p_consts.PARSER_DICT[src_lang]
  ts_tree = parser.parse(bytes(snippet, 'utf8'))
  tree = Tree.from_ts_tree(ts_tree)

  pp = PrettyPrinter()
  code = pp.visit(tree.root_node)
  print(code)


def _test_log_statement_inserter():
  snippet = p_utils.read_tmp_text('test_inserter.js')
  src_lang = 'js'

  parser = p_consts.PARSER_DICT[src_lang]
  ts_tree = parser.parse(bytes(snippet, 'utf8'))
  tree = Tree.from_ts_tree(ts_tree)

  # first pass: insert print statements and modify AST
  psi = LogStatementInserter('f_gold')
  psi.visit(tree.root_node)

  # second pass: pretty print the modified AST
  pp = PrettyPrinter()
  code = pp.visit(tree.root_node)
  p_utils.write_tmp_text('test_script_instrumented.js', code)
  print(code)


if __name__ == '__main__':
  # _get_js_boilerplate_code()
  # _test_pretty_printer()
  _test_log_statement_inserter()
