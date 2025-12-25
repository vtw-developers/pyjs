import json
from functools import reduce
from random import sample
from typing import Dict, List, Optional, Set, Tuple, Union

import d_ast_parse
import p_consts
import p_data_structures as pds
import p_grammar
import p_utils
import p_visitor_py as pvpy


logger = p_utils.setup_logger(__name__)


class _CannotGenerateProgramPairError(RuntimeError): pass


def is_invalid_pattern_before_gen_mapped_node_PY(
  node_type: str,
  mapped_node: pds.DuoGlotNode,
  template_dict: dict,
) -> bool:
  '''
  Given a node type for which to generate the simplest AST,
  and a mapped node which is replaced with the simplest AST,
  check the node type matches one of the invalid patterns.
  '''
  def _pattern_1_block_without_secret_fn_turned_on(mapped_node: pds.DuoGlotNode, template_dict: dict) -> bool:
    '''
    exclude cases where need to generate a body node type,
    but `is_insert_secret_fn` is False
    '''
    # is_insert_secret_fn must be turned off
    if template_dict['is_insert_secret_fn']:
      return False
    # mapped_node must be a block node
    node_type = mapped_node.get_ts_node_type()
    if node_type != 'block':
      return False
    logger.debug(f'Invalid pattern detected: generating `block` with is_insert_secret_fn turned off')
    return True

  def _pattern_2_argument_list_for_fn(mapped_node: pds.DuoGlotNode, fnname: str) -> bool:
    '''
    exclude such cases `range( )`
    '''
    # mapped_node must be an argument_list
    if mapped_node.get_ts_node_type() != 'argument_list':
      return False
    parent = mapped_node.get_parent()
    # parent must be a call node
    if parent.get_ts_node_type() != 'call':
      return False
    # parent must have two non-terminal children
    if len(parent.get_nt_children()) != 2:
      return False
    # first child must be identifier
    first_child = parent.get_children()[0]
    if first_child.get_ts_node_type() != 'identifier':
      return False
    # function name must be `fnname`
    terminal = first_child.get_children()[0].node_type
    if terminal != fnname:
      return False
    logger.debug(f'Invalid pattern detected: generating argument_list for "{fnname}"')
    return True

  def _pattern_3_keyword_argument(mapped_node: pds.DuoGlotNode) -> bool:
    '''
    Exclude cases such as `print(a, id_xyz='')`, to avoid
    generating a keyword argument with an invalid key.
    '''
    # mapped_node must be a keyword_argument
    if mapped_node.get_ts_node_type() != 'keyword_argument':
      return False
    logger.debug(f'Invalid pattern detected: generating keyword_argument')
    return True

  def _pattern_4_pattern_list(mapped_node: pds.DuoGlotNode) -> bool:
    '''
    Exclude cases such as `id_alic , = 5674` to avoid
    generating a pattern_list with a single element.
    '''
    # mapped_node must be a pattern_list
    if mapped_node.get_ts_node_type() != 'pattern_list':
      return False
    logger.debug(f'Invalid pattern detected: generating pattern_list')
    return True

  def _pattern_5_subscript(mapped_node: pds.DuoGlotNode) -> bool:
    '''
    Exclude generating a subscript as LHS of an assignment.
    '''
    # mapped_node must be a subscript
    if mapped_node.get_ts_node_type() != 'subscript':
      return False
    parent = mapped_node.get_parent()
    assert parent is not None, 'subscript must have a parent'
    if parent.get_ts_node_type() not in ['assignment', 'augmented_assignment']:
      return False
    idx_self = parent.children.index(mapped_node)
    if idx_self != 0:
      return False
    logger.debug(f'Invalid pattern detected: generating subscript as LHS of an assignment')
    return True

  def _pattern_6_rhs_in_comparison_operator(node_type: str, mapped_node: pds.DuoGlotNode) -> bool:
    '''
    Exclude cases such as `return 4394 in 3487`
                                          ^^^^
    '''
    # parent of mapped_node must be a comparison_operator
    parent = mapped_node.get_parent()
    if parent.get_ts_node_type() != 'comparison_operator':
      return False
    # mapped_node is the last child of parent
    if parent.children[-1] != mapped_node:
      return False
    operator = parent.children[1]
    if operator.get_type() not in ['in', 'not in']:
      return False
    if node_type != 'integer':
      return False
    logger.debug(
      f'Invalid pattern detected: generating integer as rhs of `in` comparison operator'
      f'"{mapped_node.children[0].node_type}"')
    return True

  pattern_callbacks = [
    lambda: _pattern_1_block_without_secret_fn_turned_on(mapped_node, template_dict),
    lambda: _pattern_3_keyword_argument(mapped_node),
    lambda: _pattern_4_pattern_list(mapped_node),
    lambda: _pattern_5_subscript(mapped_node),
    lambda: _pattern_6_rhs_in_comparison_operator(node_type, mapped_node),
  ]
  for ntype in p_consts.FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST[template_dict['src_lang']]:
    pattern_callbacks.append(lambda ntype=ntype: _pattern_2_argument_list_for_fn(mapped_node, ntype))

  for pattern_callback in pattern_callbacks:
    if pattern_callback():
      return True
  return False


def is_force_identifiers_PY(
  mapped_node: pds.DuoGlotNode,
) -> bool:
  '''
  These are the cases where we want to generate identifiers
  irregardless of the alternative node types. For example,
  grammar rule for `call` allows integers as function names.
  We will check such cases and force using identifiers only.

  NOTE be cautious when adding new patterns here, e.g.
  `if 4394 in 3487:` feels tempting to replace `3487` with an identifier,
  but if replaced, the rule won't match the original
  `if arr[i] in Hash.keys():`.
  '''
  def _pattern_1_mapped_node_is_identifier(mapped_node: pds.DuoGlotNode) -> bool:
    if mapped_node.get_ts_node_type() != 'identifier':
      return False
    logger.debug(
      f'Forcing identifiers: mapped_node is an identifier: '
      f'"{mapped_node.children[0].node_type}"')
    return True

  def _pattern_2_call_attribute(mapped_node: pds.DuoGlotNode) -> bool:
    '''
    When generating an attribute for a call, always use identifiers.
    For example, grammar rule for `call` allows integers as function names.
    Use identifiers instead.
    '''
    # mapped_node must be an attribute
    if mapped_node.get_ts_node_type() != 'attribute':
      return False
    # parent of mapped_node must be call
    parent = mapped_node.get_parent()
    if parent.get_ts_node_type() != 'call':
      return False
    logger.debug(
      f'Forcing identifiers: mapped_node is an attribute of a call'
      f'"{mapped_node.children[0].node_type}"')
    return True

  def _pattern_3_int_as_value_of_subscript(mapped_node: pds.DuoGlotNode) -> bool:
    '''
    Exclude cases such as retval_1 = 3740[id_jubr]
                                     ^^^^
    '''
    # parent of mapped_node must be a subscript
    parent = mapped_node.get_parent()
    if parent.get_ts_node_type() != 'subscript':
      return False
    # mapped_node is the first child of parent
    if parent.children[0] != mapped_node:
      return False
    logger.debug(
      f'Forcing identifiers: mapped_node is the value of a subscript'
      f'"{mapped_node.children[0].node_type}"')
    return True

  def _pattern_4_rhs_for_in_clause(mapped_node: pds.DuoGlotNode) -> bool:
    '''
    Exclude cases such as `dp = [6169 for id_nwi in 848]`
                                                    ^^^
    '''
    # parent of mapped_node must be an for_in_clause
    parent = mapped_node.get_parent()
    if parent.get_ts_node_type() != 'for_in_clause':
      return False
    # mapped_node is the last child of parent
    if parent.children[-1] != mapped_node:
      return False
    logger.debug(
      f'Forcing identifiers: mapped_node is the rhs of a for_in_clause'
      f'"{mapped_node.children[0].node_type}"')
    return True

  def _pattern_5_fn_single_arg(mapped_node: pds.DuoGlotNode) -> bool:
    '''
    Exclude cases such as `ord(123)`
                               ^^^
    '''
    # parent of mapped_node must be an argument_list
    parent = mapped_node.get_parent()
    if parent.get_ts_node_type() != 'argument_list':
      return False
    # parent must have one non-terminal child
    if len(parent.get_nt_children()) != 1:
      return False
    # previous sibling of parent must be an identifier
    prevs = parent.get_left_sibling()
    if prevs.get_ts_node_type() != 'identifier':
      return False
    # function name is `ord`
    fnname = prevs.children[0].node_type
    if fnname not in p_consts.FN_NAMES_FORCE_SINGLE_ARG_TO_IDENTIFIER['py']:
      return False
    logger.debug(
      f'Forcing identifiers: mapped_node is an argument of a builtin function `ord`'
      f'"{mapped_node.children[0].node_type}"')
    return True

  def _pattern_6_arg_str_join(mapped_node: pds.DuoGlotNode) -> bool:
    '''
    Exclude cases such as `" ".join(123)`
                                    ^^^
    '''
    # parent of mapped_node must be an argument_list
    parent = mapped_node.get_parent()
    if parent.get_ts_node_type() != 'argument_list':
      return False
    # parent must have one non-terminal child
    if len(parent.get_nt_children()) != 1:
      return False
    # previous sibling of parent must be an attribute
    prevs = parent.get_left_sibling()
    if prevs.get_ts_node_type() != 'attribute':
      return False
    # last non-terminal child of prevs must be an identifier
    lnt_child = prevs.get_nt_children()[-1]
    if lnt_child.get_ts_node_type() != 'identifier':
      return False
    # function name is `join`
    fnname = lnt_child.children[0].node_type
    if fnname != 'join':
      return False
    logger.debug(
      f'Forcing identifiers: mapped_node is an argument of a str method `join`'
      f'"{mapped_node.children[0].node_type}"')
    return True

  pattern_callbacks = [
    lambda: _pattern_1_mapped_node_is_identifier(mapped_node),
    lambda: _pattern_2_call_attribute(mapped_node),
    lambda: _pattern_3_int_as_value_of_subscript(mapped_node),
    lambda: _pattern_4_rhs_for_in_clause(mapped_node),
    lambda: _pattern_5_fn_single_arg(mapped_node),
    lambda: _pattern_6_arg_str_join(mapped_node),
  ]

  for pattern_callback in pattern_callbacks:
    if pattern_callback():
      return True
  return False


def is_do_not_change_identifier_PY(
  mapped_node: pds.DuoGlotNode
) -> bool:
  '''
  These are the cases where we do not want to change identifiers
  '''

  def _pattern_1_is_fn_name_PY(mapped_node: pds.DuoGlotNode) -> bool:
    '''
    Check if `mapped_node` is a function name (identifier).
    For example, `enumerate(nums)`, `findKth(i, j, k)
                  ^^^^^^^^^          ^^^^^^^
    '''
    # mapped node must be an identifier
    if mapped_node.get_ts_node_type() != 'identifier':
      return False
    # mapped node must be a child of a call node
    if mapped_node.get_parent().get_ts_node_type() != 'call':
      return False
    # mapped node must be the first child of a call node
    if mapped_node.get_parent().children[0] != mapped_node:
      return False
    logger.debug(
      f'Do not change identifier: mapped_node is a function name: '
      f'{mapped_node.children[0].node_type}')
    return True

  def _pattern_2_is_call_attribute_PY(mapped_node: pds.DuoGlotNode) -> bool:
    '''
    Return true, if `mapped_node` is an attribute of a call node (identifier).
    For example, `chars.remove(c)`
                        ^^^^^^
    '''
    # mapped node must be an identifier
    if mapped_node.get_ts_node_type() != 'identifier':
      return False
    # mapped node must be a child of an attribute node
    attribute_node = mapped_node.get_parent()
    if attribute_node.get_ts_node_type() != 'attribute':
      return False
    # mapped node must be the last node of the attribute node
    if attribute_node.children[-1] != mapped_node:
      return False
    # attribute node must be a child of a call node
    call_node = attribute_node.get_parent()
    if call_node.get_ts_node_type() != 'call':
      return False
    logger.debug(
      f'Do not change identifier: mapped_node is an attribute of a call: '
      f'{mapped_node.children[0].node_type}')
    return True

  def _pattern_3_is_keyword_argument_of_call_PY(mapped_node: pds.DuoGlotNode) -> bool:
    '''
    Return true, if `mapped_node` is a keyword argument of a call node (identifier).
    For example, `print(a, end='')`
                           ^^^
    '''
    # mapped node must be an identifier
    if mapped_node.get_ts_node_type() != 'identifier':
      return False
    # mapped node must be a child of a keyword_argument node
    kwarg_node = mapped_node.get_parent()
    if kwarg_node.get_ts_node_type() != 'keyword_argument':
      return False
    # mapped node must be the first child of a keyword_argument node
    if kwarg_node.children[0] != mapped_node:
      return False
    # kwarg node must be a child of an argument_list node
    arg_list_node = kwarg_node.get_parent()
    if arg_list_node.get_ts_node_type() != 'argument_list':
      return False
    # arg_list node must be a child of a call node
    call_node = arg_list_node.get_parent()
    if call_node.get_ts_node_type() != 'call':
      return False
    logger.debug(
      f'Do not change identifier: mapped_node is a keyword argument of a call: '
      f'{mapped_node.children[0].node_type}')
    return True

  def _pattern_4_builtin_module_PY(mapped_node: pds.DuoGlotNode) -> bool:
    '''
    Return true, if `mapped_node` is a builtin module name (identifier).
    For example, `math.pi`
                  ^^^^
    '''
    # mapped node must be an identifier
    if mapped_node.get_ts_node_type() != 'identifier':
      return False
    # mapped node must be a child of an attribute node
    attribute_node = mapped_node.get_parent()
    if attribute_node.get_ts_node_type() != 'attribute':
      return False
    # mapped node must be the first node of the attribute node
    if attribute_node.children[0] != mapped_node:
      return False
    id_literal = mapped_node.children[0].node_type
    if id_literal not in p_consts.PY_BUILT_IN_MODULES:
      return False
    logger.debug(
      f'Do not change identifier: mapped_node is a builtin module name: '
      f'{mapped_node.children[0].node_type}')
    return True

  def _pattern_5_builtin_module_attribute_PY(mapped_node: pds.DuoGlotNode) -> bool:
    '''
    Return true, if `mapped_node` is an attribute of a builtin module (identifier).
    For example, `math.pi`, `sys.maxsize`
                       ^^        ^^^^^^^
    '''
    # mapped node must be an identifier
    if mapped_node.get_ts_node_type() != 'identifier':
      return False
    # mapped node must be a child of an attribute node
    attribute_node = mapped_node.get_parent()
    if attribute_node.get_ts_node_type() != 'attribute':
      return False
    # mapped node must be the last node of the attribute node
    if attribute_node.children[-1] != mapped_node:
      return False
    # first child of attribute_node must be an identifier
    first_child = attribute_node.children[0]
    if first_child.get_ts_node_type() != 'identifier':
      return False
    id_literal = first_child.children[0].node_type
    if id_literal not in p_consts.PY_BUILT_IN_MODULES:
      return False
    logger.debug(
      f'Do not change identifier: mapped_node is an attribute of a builtin module: '
      f'{mapped_node.children[0].node_type}')
    return True

  pattern_callbacks = [
    lambda: _pattern_1_is_fn_name_PY(mapped_node),
    lambda: _pattern_2_is_call_attribute_PY(mapped_node),
    lambda: _pattern_3_is_keyword_argument_of_call_PY(mapped_node),
    lambda: _pattern_4_builtin_module_PY(mapped_node),
    lambda: _pattern_5_builtin_module_attribute_PY(mapped_node),
  ]

  for pattern_callback in pattern_callbacks:
    if pattern_callback():
      return True
  return False


def generate_tsps_manually_PY(
  template_dict: dict
) -> Optional[List[Tuple[str, str]]]:

  # case 1: add (`template_origin`, `template_origin`) as a TSP for some cases such as `string`, `int`, etc.
  if template_dict['problematic_node_type'] in p_consts.DO_NOT_GENERATE_TSPS_FOR_NODE_TYPES[template_dict['src_lang']]:
    logger.debug(f'problematic_node_type is "{template_dict["problematic_node_type"]}": manual TSP generation')
    tsps = [(template_dict['template_origin'], template_dict['template_origin'])]
    logger.debug(f'Using `(template_origin, template_origin)` as a TSP: {json.dumps(tsps, indent=2)}')
    return tsps

  return None


def generate_tsps_with_generator(template_dict: dict) -> List[Tuple[str, str]]:
  r'''
  We have `template_origin`, `problematic_node`, `context_node`.
  `context_node` is the only child of a `root_node` of `template_origin`s AST.
  In the case, where the context is null, `context_node` == `problematic_node`.
  We generate code under `problematic_node`. The two ASTs generated at
  `problematic_node` should produce a matcher (when unified) that matches
  the corresponding node in the AST of `template_origin`.

  AST for ```m = (core + core) * pi```

               expression_statement
                        |
                    assignment
            /            |         \
  identifier1           "="              binary_operator1
       |                                /     |      \
      "m"        parenthesized_expression    "*"    identifier2
                /           |           \               |
              "("    binary_operator2   ")"            "pi"
                      /     |       \
             identifier3   "+"    identifier4
                 |                     |
              "core"                "core"

  This function is expected to generate a pair of programs (TSP)
  no matter what. In the worst case, the generated programs can be
  type-isomorphic to `template_origin`, whereby we learn an overfitted rule.
  An overfitted rule can be used to translate code of the same structure
  as `template_origin` (type-isomorphic).

  Fuzz node groups:
  [
    [expression_statement],  # replace(assignment)
    [assignment],  # basic(identifier1), replace(binary_operator1)
    [identifier1, binary_operator1],  # basic_itself(identifier1), replace(parenthesized_expression), basic(identifier2)
    [identifier1, parenthesized_expression, identifier2],  # replace(binary_operator2), basic_itself(identifier1), basic_itself(identifier2)
    [identifier1, binary_operator2, identifier2],  # basic_itself(identifier1), basic_itself(identifier2), basic(identifier3), basic(identifier4)
    [identifier1, identifier3, identifier4, identifier2],  # basic_itself(identifier1), basic_itself(identifier2), basic_itself(identifier3), basic_itself(identifier4)
  ]

  NOTE this function should be vocal about important errors
  NOTE `template_dict` must include:
  - template_origin: str
  - src_lang: str
  - problematic_node_path: List[int]
  - problematic_node_type: str
  - is_insert_secret_fn: bool
  '''

  p_utils.log_json_time('args-generate_tsps_with_generator.json', locals())

  def _init_problematic_node(template_dict: dict) -> pds.DuoGlotNode:
    '''
    Parse `template_origin` and return a reference to the `problematic_node`.
    '''
    # We need the `problematic_node`, which will be passed to the generator.
    # Since `template_origin` is already simplified, we use it to get the `problematic_node`.
    template_origin = template_dict['template_origin']
    lang = template_dict['src_lang']
    ast, ann = d_ast_parse.parse_text_dbg(template_origin, lang, keep_text=False)

    tree = pds.DuoGlotTree(ast)
    # `root_node` of `tree` should have only a single child, which is a `context_node`
    root_node = tree.get_root_node()
    assert len(root_node.get_children()) == 1, 'Root node of template origin must have just a single child'
    context_node = root_node.get_children()[0]
    problematic_node_path = template_dict['problematic_node_path']
    problematic_node = context_node.get_child_by_path(problematic_node_path)

    problematic_node_str = d_ast_parse.range_cursor_pretty_print(
      d_ast_parse.get_range_cursor(ast, problematic_node.get_id()),
      ann, template_origin
    )
    logger.info(f'Problematic node is "{problematic_node}".')
    logger.info(f'Context code is ({context_node.get_ts_node_type()}):\n{template_origin}')
    logger.info(f'Problematic code is ({problematic_node.get_ts_node_type()}):\n{problematic_node_str}')

    return problematic_node

  def _is_valid_fuzz_node(node: pds.DuoGlotNode, template_dict: dict, grammar: p_grammar.TreeSitterGrammar) -> bool:
    '''
    RETURN True if `node` can be passed to `p_grammar.get_alternative_starting_node_types`
    In other words, it tells us whether we can generate alternative nodes for children of `node`.
    Unlike, for example, an `integer` node. `integer` cannot be a fuzz
    node, because it itself is templatized, i.e. it is a child of a fuzz node.

    NOTE writes to `template_dict`.
    '''
    # a valid fuzz node has to be non-terminal
    if node.is_terminal():
      return False

    # a valid fuzz node must not be external
    if grammar.is_external(node.get_ts_node_type()):
      return False

    # a valid fuzz node has to have at least one non-terminal child
    if node.get_num_nt_children() == 0:
      return False

    # a valid fuzz node cannot be of a "body node type"
    if node.get_ts_node_type() in p_consts.BODY_NODE_TYPES[template_dict['src_lang']]:
      # NOTE turn the flag on iff there is a non-terminal node
      # e.g. for empty `list`s and `dictionary`s it will stay `False`
      if node.get_num_nt_children() > 0:
        template_dict['is_insert_secret_fn'] = True
      return False

    return True

  def _gen_seq_fuzz_node_groups(problematic_node: pds.DuoGlotNode, template_dict: dict) -> List[List[pds.DuoGlotNode]]:
    r'''
    Given an initial `problematic_node`, generate a sequence of node groups
    which will be later passed to `p_grammar.get_alternative_starting_node_types`.

    What is a fuzz node group?
    A fuzz node group is a list of one or more nodes each of which:
    1. Will be passed to `p_grammar.get_alternative_starting_node_types`
    2. Will be a parent node of nodes at which
       alternative ASTs will be generated (a.k.a. templatized nodes).

    Why do we need this?
    Generating an alternative AST right under the `problematic_node` might not
    work in some cases. To solve this issue, we can try going one level down.

    Let's say that `expression_statement` is a `problematic_node` in ```core = 1```:

        expression_statement
               |
           assignment
          /     |    \
    identifier  "="   integer
         |               |
      "core"            "1"

    Then, generating an AST with `expression_statement` at its root may not work
    as in the case of ```id_foo```:

     expression_statement
              |
          identifier
              |
          "id_foo"

    Both of the ASTs have `expression_statement` at their root, but their
    translations to JavaScript may not allow us to learn a translation rule
    for `expression_statement`, since they can be not type-isomorphic.

    If we go down one level, and generate an AST with a root at `assignment`,
    then we have higher chances to get correct JavaScript translations, and
    thus learn a working translation rule.

    [[expression_statement], [assignment], [identifier, integer]] would be
    a good candidate for "fuzz node groups".

    NOTE Another example
    AST for ```m = (core + core) * pi```

                  expression_statement
                          |
                      assignment
              /            |         \
    identifier1            "="              binary_operator1
          |                                /     |      \
        "m"        parenthesized_expression    "*"    identifier2
                  /           |           \               |
                "("    binary_operator2    ")"            "pi"
                        /     |       \
                identifier3    "+"    identifier4
                    |                     |
                "core"                "core"

    [
      [expression_statement],  # assignment
      [assignment],  # identifier1, binary_operator1
      [identifier1, binary_operator1],  # parenthesized_expression, identifier2
      [identifier1, parenthesized_expression, identifier2],  # binary_operator2
      ...
    ]

    NOTE
    1. When a node reaches Python 'block' node, it stops (just like at `identifier`, `integer`, etc.).
       This allows us to use custom generation strategies for `block` nodes.
    2. Generates almost all possible fuzz node group combinations.
       Sometimes, especially when the expression is complex, the number of combinations
       can be huge. In that case, we randomly sample a subset of combinations.
       The number of combinations is controlled by `p_consts.MAX_FUZZ_GROUP_LEN`.
    3. This function is language specific (hacky).
    4. A fuzz node group may contain both valid fuzz nodes AND nodes like `integer`, `float`, etc.
    '''

    def __can_descend(node: pds.DuoGlotNode, template_dict: dict) -> bool:
      '''
      Base conditions to stop descending down the tree.
      '''
      # controls depth of recursion
      if node.get_ts_node_type() in p_consts.NON_DESCENDABLE_NODES[template_dict['src_lang']]:
        return False

      # nodes like `block`. `block` is treated specially during program generation
      if node.get_ts_node_type() in p_consts.BODY_NODE_TYPES[template_dict['src_lang']]:
        return False

      return True

    def __rec_descend(
      start_node: pds.DuoGlotNode,
      template_dict: dict
    ) -> Optional[List[List[pds.DuoGlotNode]]]:
      '''
      Recursively get fuzz node group combinations for children nodes,
      make their cartesian product, add the node itself, and return.
      '''
      # base case: ignore terminal nodes
      if start_node.is_terminal():
        return None

      # base case: cannot descend further
      if not __can_descend(start_node, template_dict):
        return [[start_node]]

      # recursive case: collect children groups
      children_generations = []
      for child in start_node.get_nt_children():
        child_generation = __rec_descend(child, template_dict)
        if child_generation is not None:
          children_generations.append(child_generation)

      # base case: no children groups
      if len(children_generations) == 0:
        return [[start_node]]

      # add start_node itself, and then add cartesian product of children
      all_generations = [[start_node]]

      image_norm = reduce(int.__mul__, map(len, children_generations))
      if image_norm > p_consts.MAX_FUZZ_GROUP_LEN:
        indices = sample(range(image_norm), p_consts.MAX_FUZZ_GROUP_LEN)
        logger.warning(
          f'Number of combinations of fuzz node groups is {image_norm}, '
          f'randomly sampling {p_consts.MAX_FUZZ_GROUP_LEN} combinations')
      else:
        indices = range(image_norm)
      for d in indices:
        generation = []
        for dimension in children_generations:
          d, m = divmod(d, len(dimension))
          generation.extend(dimension[m])
        all_generations.append(generation)

      return all_generations

    def __max_depth(group: List[pds.DuoGlotNode]) -> Union[int, float]:
      '''
      RETURN given the distances from nodes in `group` to the root node, return the maximum.
      '''
      max_depth = -1
      for node in group:
        node_depth = node.get_dist_root()
        if node_depth > max_depth:
          max_depth = node_depth
      return max_depth

    def __min_depth(group: List[pds.DuoGlotNode]) -> Union[int, float]:
      '''
      RETURN given the distances from nodes in `group` to the root node, return the minimum.
      '''
      min_depth = float('inf')
      for node in group:
        node_depth = node.get_dist_root()
        if node_depth < min_depth:
          min_depth = node_depth
      return min_depth

    def __is_within_max_span(group: List[pds.DuoGlotNode], max_span: int) -> bool:
      '''
      RETURN True if the max and min distances are within a certain threshold.
      '''
      return abs(__min_depth(group) - __max_depth(group)) <= max_span

    def __remove_terminals(group: List[pds.DuoGlotNode]) -> List[pds.DuoGlotNode]:
      '''
      Remove terminal nodes from `group`.
      '''
      return [node for node in group if not node.is_terminal()]

    def __remove_subgroups(groups: List[List[pds.DuoGlotNode]]) -> List[List[pds.DuoGlotNode]]:
      '''
      Remove subgroups from `group`.
      PRE: `groups` is a list of unique groups.
      '''
      result = []
      for i, group in enumerate(groups):
        is_subgroup = False
        for j, other_group in enumerate(groups):
          if i == j:
            continue
          if __is_subgroup_of(group, other_group):
            is_subgroup = True
            break
        if not is_subgroup:
          result.append(group)
      return result

    def __is_subgroup_of(subgroup: List[pds.DuoGlotNode], main_group: List[pds.DuoGlotNode]) -> bool:
      '''
      Check if `subgroup` is a subsequence of `main_group`.
      '''
      if len(subgroup) > len(main_group):
        return False
      for node in subgroup:
        if node not in main_group:
          return False
      return True

    def __remove_nts_with_single_nt_child(group: List[pds.DuoGlotNode], template_dict: dict) -> List[pds.DuoGlotNode]:
      '''
      Remove nodes that have a single child which is a non-terminal.
      e.g. ... -> expression_statement -> assignment -> (identifier, "=", integer)
      "expression_statement" which is an "assignment"

      NOTE the loop works in reverse: instead of removing undesirable nodes,
      we keep the desirable ones.
      '''
      nodes = []
      for node in group:
        # keep nodes with multiple children
        if len(node.get_children()) != 1:
          nodes.append(node)
          continue
        # at this point, we know that `node` has a single child
        assert len(node.get_children()) == 1, ''
        # keep nodes if their only child is terminal
        child = node.get_children()[0]
        if child.is_terminal():
          nodes.append(node)
          continue
        # at this point, we know that the only `child` is non-terminal
        assert not child.is_terminal()
        # keep nodes whose only child that is non-terminal,
        # if these nodes are of body node types.
        # they can potentially have single non-terminal child like in case of
        # `block` -> `return_statement`
        ts_node_type = node.get_ts_node_type()
        if ts_node_type in p_consts.BODY_NODE_TYPES[template_dict['src_lang']]:
          nodes.append(node)
      return nodes

    def __remove_special_nodes(group: List[pds.DuoGlotNode], template_dict: dict) -> List[pds.DuoGlotNode]:
      '''
      Remove special nodes from fuzz node groups.
      '''
      keep = lambda node: node.get_ts_node_type() not in \
        p_consts.REMOVE_FROM_FUZZ_NODE_GROUPS_NODE_TYPES[template_dict['src_lang']]
      return [node for node in group if keep(node)]

    _MAX_SPAN = 2
    # all combinations
    groups = __rec_descend(problematic_node, template_dict)
    # keep groups within certain span
    groups = [group for group in groups if __is_within_max_span(group, _MAX_SPAN)]
    # remove terminal nodes from groups
    groups = [__remove_terminals(group) for group in groups]
    # remove nodes that have a single child which is a non-terminal
    groups = [__remove_nts_with_single_nt_child(group, template_dict) for group in groups]
    # remove special nodes from fuzz node groups
    groups = [__remove_special_nodes(group, template_dict) for group in groups]
    # remove empty groups
    groups = [group for group in groups if len(group) > 0]
    # remove subgroups
    groups = __remove_subgroups(groups)
    # sort ascending by distance to root
    groups.sort(key=__max_depth)
    return groups

  _get_alt_starting_ntypes_cache = {}
  def _get_alt_starting_ntypes_cached(node: pds.DuoGlotNode, grammar: p_grammar.TreeSitterGrammar) -> List[Tuple[pds.DuoGlotNode, List[str]]]:
    nonlocal _get_alt_starting_ntypes_cache
    if node.get_id() in _get_alt_starting_ntypes_cache:
      return _get_alt_starting_ntypes_cache[node.get_id()]
    alt_starting_nodes = p_grammar.get_alternative_starting_node_types(node, grammar)
    _get_alt_starting_ntypes_cache[node.get_id()] = alt_starting_nodes
    return alt_starting_nodes

  def _gen_code_for_node_type(
    node_type: str,
    mapped_node: pds.DuoGlotNode,
    template_dict: dict,
    grammar: p_grammar.TreeSitterGrammar
  ) -> str:
    '''NOTE the generated code may have semantic errors'''

    if is_invalid_pattern_before_gen_mapped_node_PY(node_type, mapped_node, template_dict):
      raise _CannotGenerateProgramPairError('Invalid pattern detected')

    if p_consts.ENABLE_SPECIAL_TREATMENT_FOR_BODY_NODE_TYPES and template_dict['is_insert_secret_fn']:
      spec_treatment_map = p_consts.SPECIAL_TREATMENT_BODY_NODE_TYPES[template_dict['src_lang']]
      if node_type in spec_treatment_map:
        return spec_treatment_map[node_type]

    if is_do_not_change_identifier_PY(mapped_node):
      return mapped_node.children[0].node_type

    ast = grammar.generate_simplest_ast(node_type)
    ast_tree = pvpy.Tree.from_gen_ast(ast)
    code = pvpy.PrettyPrinterForGeneratedCode().visit(ast_tree.root_node)
    return code

  def _gen_code_pair_for_node_with_check(
    mapped_node: pds.DuoGlotNode,
    alt_node_types: List[str],
    template_dict: dict,
    grammar: p_grammar.TreeSitterGrammar
  ) -> Tuple[str, str]:
    '''
    RETURN pair of "valid" programs or raise an exception.
    NOTE Additionally, return a third generated snippet for trans.rule validation.
    '''

    def __choose_ranked(basic_ntypes_subset: Set[str], template_dict: dict) -> str:
      '''
      Return a node type from `basic_ntypes_subset` that is ranked higher
      in the list of basic node types.
      '''
      basic_ntypes = p_consts.BASIC_NODE_TYPES[template_dict['src_lang']]
      assert set(basic_ntypes).issuperset(basic_ntypes_subset), 'sanity check failed'

      for ntype in basic_ntypes:
        if ntype in basic_ntypes_subset:
          return ntype

      raise RuntimeError('should not reach here')

    def __get_alt_node_types(
      mapped_node: pds.DuoGlotNode,
      alt_node_types: List[str],
      template_dict: dict,
    ) -> Tuple[str, str]:
      '''
      Given a mapped node and a list of alternative node types,
      return two alternative node types that can be used to generate
      alternative ASTs.
      NOTE first two alternatives are for TSP, the third is for a program
      snippet that is used for translation rule validation.
      TODO is this always True -> `mapped_node.get_ts_node_type() in alt_node_types`
      '''
      mapped_ntype = mapped_node.get_ts_node_type()
      basic_ntypes = set(p_consts.BASIC_NODE_TYPES[template_dict['src_lang']])
      alt_ntypes = set(alt_node_types)

      # alternatives from basic node types including mapped_ntype
      basic_alts = basic_ntypes.intersection(alt_ntypes)

      # case 1: mapped_node has a basic type
      if mapped_ntype in basic_ntypes:
        # alternatives from basic node types excluding mapped_ntype
        # {identifier, integer, float}, {identifier, integer}, {identifier} -> {integer}
        pure_alts = basic_alts.difference({mapped_ntype})

        # for the second alternative node type
        # choose alternative basic type if possible (mapped_ntype, alt_ntype)
        if len(pure_alts) > 0:
          alt_ntype1 = mapped_ntype
          alt_ntype2 = __choose_ranked(pure_alts, template_dict)
          return alt_ntype1, alt_ntype2

        # otherwise fall back to the mapped_ntype (mapped_ntype, mapped_ntype)
        else:
          alt_ntype1 = mapped_ntype
          alt_ntype2 = mapped_ntype
          return alt_ntype1, alt_ntype2

      # case 2: mapped_node is not a basic type, but
      # can choose both alternatives from basic types
      if len(basic_alts) >= 2:
        # choose two different basic types from the intersection
        alt_ntype1 = __choose_ranked(basic_alts, template_dict)
        basic_alts.remove(alt_ntype1)
        alt_ntype2 = __choose_ranked(basic_alts, template_dict)
        return alt_ntype1, alt_ntype2

      # case 3: mapped_node is not a basic type, but
      # can choose one alternative from basic types
      elif len(basic_alts) == 1:
        # choose the only basic type from the intersection
        alt_ntype1 = list(basic_alts)[0]
        alt_ntype2 = mapped_ntype
        return alt_ntype1, alt_ntype2

      # case 4: no basic types in the intersection: use mapped_ntype itself
      elif len(basic_alts) == 0:
        alt_ntype1 = mapped_ntype
        alt_ntype2 = mapped_ntype
        return alt_ntype1, alt_ntype2

      raise RuntimeError('should not reach here')

    if p_consts.IS_FORCE_IDENTIFIERS and is_force_identifiers_PY(mapped_node):
      alt_ntype1, alt_ntype2 = 'identifier', 'identifier'
    else:
      alt_ntype1, alt_ntype2 = __get_alt_node_types(mapped_node, alt_node_types, template_dict)

    if mapped_node.get_ts_node_type() in p_consts.DO_NOT_GENERATE_TSPS_FOR_NODE_TYPES[template_dict['src_lang']]:
      existing = d_ast_parse.node_id_pretty_print(
        template_dict['template_origin'], template_dict['src_lang'], mapped_node.get_id())
      return existing, existing

    # NOTE TODO no check is performed on the generated code
    code1 = _gen_code_for_node_type(alt_ntype1, mapped_node, template_dict, grammar)
    code2 = _gen_code_for_node_type(alt_ntype2, mapped_node, template_dict, grammar)
    return code1, code2

  def _apply_alt_codes(alternative_codes: Dict[int, str], template_dict: dict) -> str:
    '''
    Given alternative codes (code blocks) for particular nodes,
    return an updated code with alternative codes applied.

    PARAM alternative_code: keys are `node_id`s, values are alternative codes.
    '''
    assert len(alternative_codes) > 0, 'sanity check: alternative_codes must not be empty'
    # We need PirelTree as it supports `text` attribute that we rely on.
    template_origin = template_dict['template_origin']
    lang = template_dict['src_lang']
    ast_text, ann = d_ast_parse.parse_text_dbg(template_origin, lang, keep_text=True)
    tree = pds.PirelTree(ast_text, annotation=ann)
    tree._fix_indentation()
    # `root_node` of `tree` should have only a single child, which is a `context_node`
    root_node = tree.get_root_node()
    assert len(root_node.get_children()) == 1, 'Root node of template origin must have just a single child'
    context_node = root_node.get_children()[0]
    # Original text that will be replaced by alternative codes at each mapped node.
    # Need to replace starting from the end of the string so that indices in `ann`
    # do not get shifted.
    orig_text = context_node.get_text()
    templatized_node_ids = sorted(alternative_codes.keys(), reverse=True)
    for tni in templatized_node_ids:
      start_point = tree.annotation[tni][0]
      end_point = tree.annotation[tni][1]
      orig_text = orig_text[:start_point] + alternative_codes[tni] + orig_text[end_point:]
    return orig_text

  def _gen_program_pair(
    all_alt_starting_nodes: List[Tuple[pds.DuoGlotNode, List[str]]],
    grammar: p_grammar.TreeSitterGrammar,
    template_dict: dict
  ) -> Tuple[str, str]:
    ''''''
    # FOR EACH TEMPLATIZED NODE, GENERATE AN ALTERNATIVE AST
    alternative_codes_1 = {}
    alternative_codes_2 = {}

    # `alt_node_types` is a list of all alternative nodes including `mapped_node.get_type()`
    for mapped_node, alt_node_types in all_alt_starting_nodes:
      code_1, code_2 = _gen_code_pair_for_node_with_check(mapped_node, alt_node_types, template_dict, grammar)
      alternative_codes_1[int(mapped_node.get_id())] = code_1
      alternative_codes_2[int(mapped_node.get_id())] = code_2

    if len(alternative_codes_1) == 0 or len(alternative_codes_2) == 0:
      raise _CannotGenerateProgramPairError('Cannot generate program pair')

    # APPLY ALTERNATIVE CODES AT DESIGNATED LOCATIONS
    gen_src_prog_1 = _apply_alt_codes(alternative_codes_1, template_dict)
    gen_src_prog_2 = _apply_alt_codes(alternative_codes_2, template_dict)

    return gen_src_prog_1, gen_src_prog_2

  def _filter_program_pairs(program_pairs: List[Tuple[str, str]], template_dict: dict) -> List[Tuple[str, str]]:
    '''
    Given the final list of program pairs (TSPs),
    sanity check them, remove duplicate entries.

    Filter criteria:
    1. Parseable
    2. Keep only unique
    '''
    def __get_type_encoding_x_term(tree: pds.DuoGlotTree) -> str:
      '''
      Compute AHU encoding with
      1. type information
      2. terminals except literals (integer, float, identifier, etc.)
      for comparing tree for type-isomorphism
      https://www.baeldung.com/cs/isomorphic-trees#1-ahu-encoding
      '''
      def __rec_post_order(node: pds.DuoGlotNode):
        # base case
        if node.is_terminal():
          # literals do not have siblings
          if node.get_num_siblings() == 0:
            return '0'
          else:
            return node.get_type()
        children_encoding = ''
        for child in node.get_children():
          children_encoding += __rec_post_order(child) + ' '
        children_encoding = children_encoding.strip()
        return f'({node.get_type()} {children_encoding})'
      encoding = __rec_post_order(tree.get_root_node())
      return encoding

    def __get_tree(code: str, lang: str) -> pds.DuoGlotTree:
      '''
      In case of any error, treat `code` as non-parseable and return `None`.
      '''
      try:
        ast, ann = d_ast_parse.parse_text_dbg(code, lang, keep_text=False)
        tree = pds.DuoGlotTree(ast)
        return tree
      except:
        return None

    lang = template_dict['src_lang']
    filtered_program_pairs = []
    unique_pair_encodings = []
    for program_pair in program_pairs:
      # NOTE The third snippet in `program_pair` is used for translation rule validation.
      # We do not need to use it as a criteria for removing duplicate entries.
      tree1, tree2 = __get_tree(program_pair[0], lang), __get_tree(program_pair[1], lang)
      # skip if any of them has a parse error
      if tree1 is None or tree2 is None:
        continue
      # skip duplicates
      enc1, enc2 = __get_type_encoding_x_term(tree1), __get_type_encoding_x_term(tree2)
      enc1, enc2 = sorted([enc1, enc2])  # make encodings order insensitive
      pair_enc = enc1 + ' ' + enc2
      if pair_enc in unique_pair_encodings:
        continue
      unique_pair_encodings.append(pair_enc)
      # filtering step is over
      filtered_program_pairs.append(program_pair)
    return filtered_program_pairs

  def _special_treatment_if_statement(
    problematic_node: pds.DuoGlotNode,
    grammar: p_grammar.TreeSitterGrammar,
    template_dict: dict
  ) -> List[Tuple[str, str]]:
    '''
    Special treatment for `if_statement` nodes in Python.
    '''
    # alternative node types for conditions
    all_alt_starting_nodes : List[Tuple[pds.DuoGlotNode, List[str]]] = []
    nt_children = problematic_node.get_nt_children()
    all_alt_starting_nodes.append((nt_children[0], ['identifier', 'integer']))  # if condition
    all_alt_starting_nodes.append((nt_children[1], ['block']))  # if body
    for nt_child in nt_children[1:]:
      if nt_child.get_ts_node_type() == 'elif_clause':
        elif_nt_children = nt_child.get_nt_children()
        all_alt_starting_nodes.append((elif_nt_children[0], ['identifier', 'integer']))  # elif condition
        all_alt_starting_nodes.append((elif_nt_children[1], ['block']))  # elif body
      elif nt_child.get_ts_node_type() == 'else_clause':
        else_nt_children = nt_child.get_nt_children()
        all_alt_starting_nodes.append((else_nt_children[0], ['block']))  # else body
    # generate a program pair
    template_dict['is_insert_secret_fn'] = True
    gen_src_prog_1, gen_src_prog_2 = _gen_program_pair(all_alt_starting_nodes, grammar, template_dict)
    return [(gen_src_prog_1, gen_src_prog_2)]

  logger.info('gen-tsp: starting generator based TSP generation.')

  # INPUTS TO THE GENERATOR
  lang = template_dict['src_lang']
  grammar = p_grammar.TreeSitterGrammar.from_dict(p_consts.GRAMMAR_DICT_READONLY[lang])
  problematic_node = _init_problematic_node(template_dict)

  if problematic_node.get_ts_node_type() == 'if_statement':
    return _special_treatment_if_statement(problematic_node, grammar, template_dict)

  # before automatic generation, check if we can use manually generated TSPs
  # specific to Python
  manually_generated_tsps = generate_tsps_manually_PY(template_dict)
  if manually_generated_tsps is not None:
    logger.debug('Using manually generated TSPs')
    return manually_generated_tsps

  # `program_pairs` is a list of tuples, each tuple is a pair of programs
  program_pairs : List[Tuple[str, str]] = []

  # GROUPS OF NODES THAT CAN BE ROOTS OF ALTERNATIVE ASTs (similar to templatized nodes)
  fuzz_node_groups = _gen_seq_fuzz_node_groups(problematic_node, template_dict)
  logger.debug(f'There are {len(fuzz_node_groups)} fuzz node groups.')

  for group_idx, fuzz_node_group in enumerate(fuzz_node_groups):
    # NOTE EXPERIMENTAL resetting a flag in `template_dict`
    # it is set to `True` in `_is_valid_fuzz_node`
    template_dict['is_insert_secret_fn'] = False

    # contains a list of alternative starting nodes for
    # 1. each node under every node in `fuzz_node_group` OR
    # 2. the node itself.
    # We will generate ASTs to replace these nodes in the tree.
    all_alt_starting_nodes : List[Tuple[pds.DuoGlotNode, List[str]]] = []

    # FIND ALTERNATIVE STARTING NODE TYPES
    for node in fuzz_node_group:

      # do not generate AST for certain node types
      if node.get_ts_node_type() in p_consts.DO_NOT_GENERATE_TSPS_FOR_NODE_TYPES[template_dict['src_lang']]:
        continue

      # check if we can pass the node to `p_grammar.get_alternative_starting_node_types`
      if _is_valid_fuzz_node(node, template_dict, grammar):
        alt_starting_nodes = _get_alt_starting_ntypes_cached(node, grammar)
        all_alt_starting_nodes.extend(alt_starting_nodes)
      else:
        all_alt_starting_nodes.append((node, [node.get_ts_node_type()]))

    # APPLY ALTERNATIVE CODES AT DESIGNATED LOCATIONS
    # Since `fuzz_node_groups` are ordered from root nodes to leaf nodes,
    # `program_pairs` ends up containing the most abstract program pairs
    # first, and concrete program pairs next. That is, translation rule
    # inferred from first TSP would be the most abstract, and translation
    # rule inferred from last TSP would be the most concrete.
    try:
      gen_src_prog_1, gen_src_prog_2 = _gen_program_pair(all_alt_starting_nodes, grammar, template_dict)
      program_pairs.append((gen_src_prog_1, gen_src_prog_2))
    except _CannotGenerateProgramPairError:
      continue

  # remove duplicates, sanity check
  unique_tsps = _filter_program_pairs(program_pairs, template_dict)
  logger.debug(f'gen-tsp: generated {len(unique_tsps)} TSPs:\n{json.dumps(unique_tsps, indent=2)}')

  return unique_tsps


def simplify_template_with_generator(template_dict: dict) -> dict:
  '''
  Given a template_origin, problematic_node, and context_node,
  replace everything around problematic_node with a generated basic type
  wherever it is possible (according to grammar).

  Example,
  `m = c + d if a > b else e - f`
  can be simplified to
  `m = id1 if a > b else id2`
  where `a > b` is problematic.

  NOTE writes to `template_dict`.
  The following keys must be present:
  - `template_origin`
  - `src_lang`
  - `problematic_node_path`
  The following keys are updated/written:
  - `problematic_node_id`
  - `template_origin`
  The following keys are created:
  - `template_origin_before_simpl_w_gen`

  NOTE the idea is very similar to `generate_tsps_with_generator`.
  '''

  def _get_context_problematic_nodes(
    program_text: str,
    lang: str,
    problematic_node_path: List[int] = None,
  ) -> Tuple[pds.DuoGlotNode, pds.DuoGlotNode]:
    ast, _ = d_ast_parse.parse_text_dbg(program_text, lang, keep_text=False)
    tree = pds.DuoGlotTree(ast)
    root_node = tree.root_node
    assert len(root_node.get_children()) == 1, 'sanity check: root node must have exactly one child'
    context_node = root_node.get_children()[0]
    assert problematic_node_path is not None, 'sanity check'
    assert isinstance(problematic_node_path, list), 'sanity check'
    problematic_node = context_node.get_child_by_path(problematic_node_path)
    return context_node, problematic_node

  def _rec_collect_simplifiable_nodes(
    node: pds.DuoGlotNode,
    template_node: pds.DuoGlotNode,
    src_lang: str,
    is_simplify_nodes_before_prob_node: bool = False
  ) -> List[pds.DuoGlotNode]:
    '''
    Collect nodes that can be simplified.
    We need to collect all nodes that are not `problematic_node` itself,
    but are still children of `problematic_node`.

    PARAM is_simplify_nodes_before_prob_node - controls whether or not nodes
    that appear before the problematic node are simplifieid. Why is it important to
    set this flag to `False`? For example, let's say we are learned a rule for
    if_statement: `if r >= l:\n    pass\nelse:\n    pass`
    ```
    (match_expand
      (fragment ("py.if_statement" (str "if") ("py.comparison_operator" ("py.identifier" "_val_") (str ">=") ("py.identifier" "_val_")) (str ":") "*") "*")
      (fragment ("js.if_statement" (str "if") ("js.parenthesized_expression" (str "(") ("js.binary_expression" ("js.identifier" "_val1_") (str ">=") ("js.identifier" "_val2_")) (str ")")) "*1") "*2")
    )
    ```
    The next problematic node is `else_clause`. If we simplify `r >= l` to `id_xyz`,
    `if id_xyz:\n    pass\nelse:\n    pass`, then the previous rule will not match.
    That's why we should not simplify nodes that appear before the problematic node.
    '''
    # base case
    if node == template_node:
      return []
    if not is_simplify_nodes_before_prob_node:
      if node.get_id() < template_node.get_id():
        return []
    simplifiable_nodes = []
    if node.is_ancestor_or_itself(template_node):
      for child in node.get_nt_children():
        child_res = _rec_collect_simplifiable_nodes(child, template_node, src_lang)
        simplifiable_nodes.extend(child_res)
      return simplifiable_nodes
    if node.get_ts_node_type() not in p_consts.BASIC_NODE_TYPES[src_lang]:
      simplifiable_nodes.append(node)
    return simplifiable_nodes

  def _get_simplifiable_parents(simplifiable_nodes: List[pds.DuoGlotNode]) -> List[Tuple[pds.DuoGlotNode, List[pds.DuoGlotNode]]]:
    '''
    From the given list of simplifiable nodes, get their parents.
    We need the parents for `_get_alt_starting_ntypes`.
    '''
    parent_id_children = {}
    for node in simplifiable_nodes:
      parent_id_children.setdefault(node.get_parent().get_id(), []).append(node)
    result_dict = []
    for parent_id, children in parent_id_children.items():
      result_dict.append((children[0].get_parent(), children))
    return result_dict

  def _get_alt_ntypes_for_child(child: pds.DuoGlotNode, alt_starting_nodes: List[Tuple[pds.DuoGlotNode, List[str]]]) -> List[str]:
    for alt_starting_node in alt_starting_nodes:
      if child.get_id() == alt_starting_node[0].get_id():
        return alt_starting_node[1]
    raise RuntimeError('should not reach here')

  def _is_call_attribute_PY(mapped_node: pds.DuoGlotNode) -> bool:
    '''
    Return true, if `mapped_node` is an attribute of a call node.
    For example, `chars.remove(c)`
                  ^^^^^^^^^^^^
    '''
    # mapped node must be an attribute
    if mapped_node.get_ts_node_type() != 'attribute':
      return False
    # mapped node must be a child of a call node
    if mapped_node.get_parent().get_ts_node_type() != 'call':
      return False
    # mapped node must be the first child of the call node
    if mapped_node.get_parent().children[0] != mapped_node:
      return False
    return True

  def _gen_code_for_node_type(node_type: str, grammar: p_grammar.TreeSitterGrammar) -> str:
    '''NOTE the generated code may have semantic errors'''
    ast = grammar.generate_simplest_ast(node_type)
    ast_tree = pvpy.Tree.from_gen_ast(ast)
    code = pvpy.PrettyPrinterForGeneratedCode().visit(ast_tree.root_node)
    return code

  def _gen_code_for_node(
    mapped_node: pds.DuoGlotNode,
    alt_node_types: List[str],
    src_lang: str,
    grammar: p_grammar.TreeSitterGrammar
  ) -> Optional[str]:
    '''
    RETURN a simplified code, else None
    '''

    def __choose_ranked(basic_ntypes_subset: Set[str], src_lang: str) -> str:
      '''
      return a node type from `basic_ntypes_subset` that is ranked higher
      in the list of basic node types.
      '''
      basic_ntypes = p_consts.BASIC_NODE_TYPES[src_lang]
      assert set(basic_ntypes).issuperset(basic_ntypes_subset), 'sanity check failed'

      for ntype in basic_ntypes:
        if ntype in basic_ntypes_subset:
          return ntype

      raise RuntimeError('should not reach here')

    def __get_alt_node_types(mapped_node: pds.DuoGlotNode, alt_node_types: List[str], src_lang: str) -> Optional[str]:
      '''
      Given a mapped node and a list of alternative node types,
      return one alternative node type that can be used to generate
      an alternative AST.
      RETURN None if cannot simplify the `mapped_node`.
      TODO is this always True -> `mapped_node.get_ts_node_type() in alt_node_types`
      '''
      mapped_ntype = mapped_node.get_ts_node_type()
      basic_ntypes = set(p_consts.BASIC_NODE_TYPES[src_lang])
      alt_ntypes = set(alt_node_types)

      # alternatives from basic node types including mapped_ntype
      basic_alts = basic_ntypes.intersection(alt_ntypes)

      # case 1: mapped_node has a basic type: do not touch
      if mapped_ntype in basic_ntypes:
        return None

      # case 2: mapped_node is not a basic type, but
      # can choose an alternative from basic types
      if len(basic_alts) > 0:
        alt_ntype = __choose_ranked(basic_alts, src_lang)
        return alt_ntype

      # case 3: no basic types in the intersection: use mapped_ntype itself
      elif len(basic_alts) == 0:
        return None

      raise RuntimeError('should not reach here')

    # make sure that we do not simplify method calls on objects
    if _is_call_attribute_PY(mapped_node):
      return None

    alt_ntype = __get_alt_node_types(mapped_node, alt_node_types, src_lang)
    if alt_ntype is None:
      return None
    code = _gen_code_for_node_type(alt_ntype, grammar)
    return code

  def _apply_alt_codes(alternative_codes: Dict[int, str], template_origin: str, src_lang: str) -> str:
    '''
    Given alternative codes (code blocks) for particular nodes,
    return an updated code with alternative codes applied.

    PARAM alternative_code: keys are `node_id`s, values are alternative codes.
    '''
    # We need PirelTree as it supports `text` attribute that we rely on.
    ast_text, ann = d_ast_parse.parse_text_dbg(template_origin, src_lang, keep_text=True)
    tree = pds.PirelTree(ast_text, annotation=ann)
    tree._fix_indentation()
    # `root_node` of `tree` should have only a single child, which is a `context_node`
    root_node = tree.get_root_node()
    assert len(root_node.get_children()) == 1, 'Root node of template origin must have just a single child'
    context_node = root_node.get_children()[0]
    # Original text that will be replaced by alternative codes at each mapped node.
    # Need to replace starting from the end of the string so that indices in `ann`
    # do not get shifted.
    orig_text = context_node.get_text()
    templatized_node_ids = sorted(alternative_codes.keys(), reverse=True)
    for tni in templatized_node_ids:
      start_point = tree.annotation[tni][0]
      end_point = tree.annotation[tni][1]
      orig_text = orig_text[:start_point] + alternative_codes[tni] + orig_text[end_point:]
    return orig_text

  def _gen_program(
    all_alt_starting_nodes: List[Tuple[pds.DuoGlotNode, List[str]]],
    grammar: p_grammar.TreeSitterGrammar,
    template_origin: str,
    src_lang: str,
  ) -> str:
    alternative_codes = {}
    # `alt_node_types` is a list of all alternative nodes including `mapped_node.get_type()`
    for mapped_node, alt_node_types in all_alt_starting_nodes:
      code = _gen_code_for_node(mapped_node, alt_node_types, src_lang, grammar)
      # cannot/no need to simplify the `mapped_node`
      if code is None:
        continue
      alternative_codes[int(mapped_node.get_id())] = code
    gen_src_prog = _apply_alt_codes(alternative_codes, template_origin, src_lang)
    return gen_src_prog

  logger.debug('~~~ Starting generator based snippet simplification')
  grammar = p_grammar.TreeSitterGrammar.from_dict(p_consts.GRAMMAR_DICT_READONLY[template_dict['src_lang']])
  context_node, problematic_node = _get_context_problematic_nodes(
    template_dict['template_origin'],
    template_dict['src_lang'],
    template_dict['problematic_node_path']
  )
  simplifiable_nodes = _rec_collect_simplifiable_nodes(
    context_node,
    problematic_node,
    template_dict['src_lang'],
    is_simplify_nodes_before_prob_node=False
  )
  simplifiable_parents = _get_simplifiable_parents(simplifiable_nodes)

  all_alt_starting_nodes : List[Tuple[pds.DuoGlotNode, List[str]]] = []
  for parent, children in simplifiable_parents:
    alt_starting_nodes = p_grammar.get_alternative_starting_node_types(parent, grammar)
    for child in children:
      alt_ntypes = _get_alt_ntypes_for_child(child, alt_starting_nodes)
      all_alt_starting_nodes.append((child, alt_ntypes))

  simplified_template = _gen_program(all_alt_starting_nodes, grammar, template_dict['template_origin'], template_dict['src_lang'])

  # NOTE problematic_node_path must be the same, since we haven't removed any nodes
  upd_context_node, upd_problematic_node = _get_context_problematic_nodes(
    simplified_template,
    template_dict['src_lang'],
    template_dict['problematic_node_path']
  )

  assert context_node.get_id() == upd_context_node.get_id(), 'sanity check'
  assert problematic_node.get_type() == upd_problematic_node.get_type(), 'sanity check'
  assert problematic_node.debug_str() == upd_problematic_node.debug_str(), 'sanity check'

  template_dict['template_origin_before_simpl_w_gen'] = template_dict['template_origin']
  template_dict['template_origin'] = simplified_template
  template_dict['problematic_node_id'] = upd_problematic_node.get_id()

  return template_dict


# TEST HARNESSES
def _test_generate_tsps_with_generator():
  '''
  template_dict must include:
  - template_origin: str
  - src_lang: str
  - problematic_node_path: List[int]
  - problematic_node_type: str
  - is_insert_secret_fn: bool
  '''
  config_fpath = p_consts.TMP_DIR / 'test_generate_tsps_with_generator.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  template_dict = args_dict['template_dict']
  tsps = generate_tsps_with_generator(template_dict)

  print(template_dict['template_origin'])
  print()
  print(f'Generated {len(tsps)} TSPs:')
  for idx, tsp in enumerate(tsps, start=1):
    print(f'TSP {idx}:')
    print(f'{tsp[0]}')
    print(f'{tsp[1]}')
    print()
  template_dict['tsps'] = tsps
  print(json.dumps(template_dict))


if __name__ == '__main__':
  _test_generate_tsps_with_generator()
