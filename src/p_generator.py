import itertools
import json
from typing import Dict, List, Set, Tuple, Union

import d_ast_parse
import p_consts
import p_data_structures as pds
import p_grammar
import p_utils
import p_visitor_py


logger = p_utils.setup_logger(__name__)


# ERROR CLASSES
class _CannotGenerateCorrectProgramError(RuntimeError): pass


# API FUNCTIONS
def simplify_template_init(template_dict: dict):
  '''
  What we want to achieve with this function is the following:
  p_templates.extract_templates prepares the following artifacts:
  1. templatized_node_ids_context  # this is to know exactly what nodes were simplified
  2. template_context_simplification  # this is sent to LLM for filling in
  3. template_context_str_replace  # this is used to prepare the final simplified template/program

  We want to prepare these artifacts using techniques from `generate_tsp_with_generator`.

  HOW?
  1. Collect nodes that should be simplified
  2. That's it

  WHAT ARTIFACTS DO WE USE?
  1. template_origin
  2. problematic_node_path
  3. src_lang

  NOTE copied and adapted from `p_templates.TemplateTree.get_template_dict_for_node_id`
  '''

  logger.debug('~~~ Starting p_generator.simplify_template_init')
  logger.debug('Preparing a template for program simplification')

  def _context_node_can_be_simplified(node: pds.PirelNode, template_node: pds.PirelNode) -> bool:
    '''
    RETURN True if this node in context can be simplified
    '''
    # terminals are already simple
    if node.is_terminal():
      return False
    assert node.is_nonterminal(), 'scope invariant'

    # cannot shadow the template node (a.k.a. problematic node)
    if node.is_ancestor_or_itself(template_node):
      return False
    assert not node.is_ancestor_or_itself(template_node), 'scope invariant'

    children = node.get_children()
    if len(children) == 1:
      only_child = children[0]

      # most literals and identifiers
      if only_child.is_terminal():
        return False
      assert only_child.is_nonterminal(), 'scope invariant'

      # TODO maybe should update to 'string of NT-NT-T of width 1'?
      return True

    assert len(children) > 1, 'scope invariant'
    if node.all_children_nonterminal():
      return True

    assert node.has_terminal_child()
    return False

  template_origin = template_dict['template_origin']
  src_lang = template_dict['src_lang']
  problematic_node_path = template_dict['problematic_node_path']

  context_ast_text, context_annotation = d_ast_parse.parse_text_dbg(template_origin, lang=src_lang, keep_text=True)
  context_tree = pds.PirelTree(context_ast_text, annotation=context_annotation)
  context_tree._fix_indentation()

  context_node = context_tree.get_root_node().get_children()[0]
  problematic_node = context_node.get_child_by_path(problematic_node_path)

  templatized_node_ids_context : dict = {}

  def _rec_collect_simplified_nodes_context_node(at_node: pds.PirelNode, template_node: pds.PirelNode, context_node: pds.PirelNode) -> None:
    '''modifies simplified_node_ids_context'''
    nonlocal templatized_node_ids_context
    # do not enter template node sub-ast
    if at_node == template_node:
      return
    if _context_node_can_be_simplified(at_node, template_node):
      templatized_node_ids_context[at_node.get_id()] = context_node.get_path_to_child(at_node)
      return
    for child_node in at_node.get_children():
      _rec_collect_simplified_nodes_context_node(child_node, template_node, context_node)

  _rec_collect_simplified_nodes_context_node(context_node, problematic_node, context_node)

  def _rec_templatize(node: pds.PirelNode, templatized_node_ids: List[int], placeholder_context: str) -> str:
    nonlocal context_tree
    orig_text = node.get_text()
    simplified_node_ids = sorted(templatized_node_ids, reverse=True)
    for snid in simplified_node_ids:
      start_point = context_tree.annotation[snid][0]
      end_point = context_tree.annotation[snid][1]
      orig_text = orig_text[:start_point] + placeholder_context + orig_text[end_point:]
    return orig_text

  template_context_simplification = _rec_templatize(context_node, list(templatized_node_ids_context.keys()), p_consts.PLACEHOLDER_TEXT)
  template_context_str_replace = _rec_templatize(context_node, list(templatized_node_ids_context.keys()), p_consts.CONTEXT_PH_TEXT)

  template_dict['template_context_simplification'] = template_context_simplification
  template_dict['template_context_str_replace'] = template_context_str_replace
  template_dict['templatized_node_ids_context'] = templatized_node_ids_context

  logger.debug(f'Template for program simplification looks like this:\n{template_context_simplification}')

  return template_dict


# DEPRECATED
def _deprecated_generate_tsps_with_generator_OLD(template_dict: dict) -> List[Tuple[str, str]]:
  '''
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
  identifier            "="              binary_operator
       |                                /     |      \
      "m"        parenthesized_expression    "*"    identifier
                /           |           \               |
              "("    binary_operator    ")"            "pi"
                      /     |       \
             identifier    "+"    identifier
                 |                     |
              "core"                "core"

  This function is expected to generate a pair of programs (TSP)
  no matter what. In the worst case, the generated programs can be
  type-isomorphic to `template_origin`, whereby we learn an overfitted rule.
  An overfitted rule can be used to translate code of the same structure
  as `template_origin` (type-isomorphic).

  NOTE this function should be vocal about important errors
  TODO consider cases where API_NoAlternativeError is raised
  '''

  def _init_problematic_node(template_dict: dict) -> pds.DuoGlotNode:
    '''
    Parse `template_origin` and return a reference to the `problematic_node`.
    '''
    # We need the `problematic_node`, which will be passed to the generator.
    # Since `template_origin` is already simplified, we use it to get the `problematic_node`.
    template_origin = template_dict['template_origin']
    lang = template_dict['src_lang']
    ast, _ = d_ast_parse.parse_text_dbg(template_origin, lang, keep_text=False)
    # p_utils.write_json('temporary_ast.json', ast)  # NOTE for debugging only
    tree = pds.DuoGlotTree(ast)
    # `root_node` of `tree` should have only a single child, which is a `context_node`
    root_node = tree.get_root_node()
    assert len(root_node.get_children()) == 1, 'Root node of template origin must have just a single child'
    context_node = root_node.get_children()[0]
    problematic_node_path = template_dict['problematic_node_path']
    problematic_node = context_node.get_child_by_path(problematic_node_path)
    return problematic_node

  def _is_valid_fuzz_node(node: pds.DuoGlotNode, template_dict: dict, grammar: p_grammar.TreeSitterGrammar) -> bool:
    '''
    RETURN True if `node` can be passed to `p_grammar.get_alternative_starting_node_types`
    In other words, it tells us whether we can generate alternative nodes for
    children of this node. Unlike, for example, an `integer` node. `integer` cannot be a fuzz
    node, because it itself is templatized, i.e. it is a child of a fuzz node.

    NOTE writes to `template_dict`.
    TODO should we reset "template_dict['is_insert_secret_fn']" to False?
    '''
    # has to be non-terminal
    if node.is_terminal():
      return False
    # must not be external
    if grammar.is_external(node.get_ts_node_type()):
      return False
    # cannot be `block`
    if node.get_ts_node_type() in p_consts.BODY_NODE_TYPES[template_dict['src_lang']]:
      # NOTE turn the flag on iff there is a non-terminal node
      # e.g. for empty `list`s and `dictionary`s it will stay `False`
      if node.get_num_nt_children() > 0:
        template_dict['is_insert_secret_fn'] = True
      return False
    # has to have at least one non-terminal child
    if node.get_num_nt_children() == 0:
      return False
    if not _can_be_fuzz_node_ancestor(node, template_dict):
      return False
    return True

  def _can_be_fuzz_node_ancestor(node: pds.DuoGlotNode, template_dict: dict) -> bool:
    '''
    These nodes can be added to fuzz node groups,
    but none of their children can.
    NOTE does not prevent a node from being added to a fuzz node group
    HACK this function is hacky
    '''
    # literal nodes like `integer`, `float`, etc.
    if node.has_single_terminal_child():
      return False
    # `string` is also a literal node, however it needs a special treatment unlike e.g. `integer`
    if node.get_ts_node_type() == 'string':
      return False
    # nodes like `block`. `block` is treated specially during program generation
    if node.get_ts_node_type() in p_consts.BODY_NODE_TYPES[template_dict['src_lang']]:
      return False
    return True

  def _can_be_added_to_fuzz_node_group(node_or_node_type: Union[pds.DuoGlotNode, str]) -> bool:
    '''
    If a node does not appear in a fuzz node group,
    then it will be kept intact. That is, it will not be fuzzed.
    For example, if we want to avoid having `string` nodes fuzzed, we can add it here.
    '''
    DO_NOT_GENERATE_ASTS_FOR = ['string', 'generator_expression']

    assert isinstance(node_or_node_type, (str, pds.DuoGlotNode)), 'sanity check failed'

    if isinstance(node_or_node_type, pds.DuoGlotNode):
      node_type = node_or_node_type.get_ts_node_type()
    elif isinstance(node_or_node_type, str):
      node_type = node_or_node_type

    if node_type in DO_NOT_GENERATE_ASTS_FOR:
      return False
    return True

  def _gen_seq_fuzz_node_groups_ALL(problematic_node: pds.DuoGlotNode, template_dict: dict, grammar: p_grammar.TreeSitterGrammar) -> List[List[pds.DuoGlotNode]]:
    '''
    Given an initial `problematic_node`, generate a sequence of node groups
    which will be later passed to `p_grammar.get_alternative_starting_node_types`.

    What is a fuzz node group?
    A fuzz node group is a list of one or more nodes each of which:
    1. Will be passed to `p_grammar.get_alternative_starting_node_types`
    2. Will be a parent node (not necessarily direct) of nodes at which
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
    ]

    NOTE This function works the same as `_gen_seq_fuzz_node_groups`, but
    1. When a node reaches Python 'block' node, it stops (just like at `identifier`, `integer`, etc.).
    This will allow using custom generation strategies for `block` nodes.
    2. Generates all possible fuzz node group combinations.

    NOTE This function is language specific (hacky).

    NOTE A fuzz node group may contain both valid fuzz nodes AND nodes like `integer`, `float`, etc.
    '''

    def __nodes_that_we_can_descend_to_from(node: pds.DuoGlotNode) -> List[pds.DuoGlotNode]:
      '''
      Returns list of non-terminal nodes of `node` that `__rec_descend` will descend to.
      That means that nodes returned by this function will be added to the
      fuzz node groups.
      '''
      # simplest case: return all non-terminal children
      # return node.get_nt_children()

      # more controlled version
      nodes = list(filter(_can_be_added_to_fuzz_node_group, node.get_nt_children()))
      return nodes

    def __rec_descend(start_node: pds.DuoGlotNode) -> List[List[pds.DuoGlotNode]]:
      '''
      Recursively get fuzz node group combinations for children nodes,
      make their cartesian product, add the node itself, and return.

      NOTE nodes that are `not _can_be_fuzz_node_ancestor` are added to the group
      '''

      nonlocal template_dict
      # base case: last node (node below which cannot descend)
      if not _can_be_fuzz_node_ancestor(start_node, template_dict):
        return [[start_node]]
      # collect children groups
      children_generations = []
      for ntchild in __nodes_that_we_can_descend_to_from(start_node):
        child_generation = __rec_descend(ntchild)
        children_generations.append(child_generation)
      # add start_node itself, and then add cartesian product of children
      all_generations = [[start_node]]
      for cart_prod in itertools.product(*children_generations):
        generation = []
        for child_generation in cart_prod:
          generation.extend(child_generation)
        all_generations.append(generation)
      return all_generations

    def __sort_key(group: List[pds.DuoGlotNode]) -> Union[int, float]:
      '''
      Sorting algorithm for fuzz node groups. Sort key:
      1. max depth is minimal
      '''
      max_depth = -1
      for node in group:
        node_depth = node.get_dist_root()
        if node_depth > max_depth:
          max_depth = node_depth
      return max_depth

    groups = __rec_descend(problematic_node)
    groups.sort(key=__sort_key)
    return groups

  def _gen_code_pair_for_node_with_check(
    mapped_node: pds.DuoGlotNode,
    alt_node_types: List[str],
    template_dict: dict,
    grammar: p_grammar.TreeSitterGrammar
  ) -> Tuple[str, str]:
    '''
    RETURN pair of "valid" programs or raise error
    RAISE `_CannotGenerateCorrectProgramError`
    '''

    def __choose_next_best_starting_node_type(alt_node_types: List[str], avoid_error: List[str], avoid_used: List[str]) -> Union[str, None]:
      '''
      PARAM avoid_error - avoid using these node types, as they result in an invalid code
      PARAM avoid_used - list of already used nodes, fall back to these if none can be chosen
      RETURN None if no valid choice left
      '''
      all_valid = [ntype for ntype in alt_node_types if ntype not in avoid_error]
      # worst case, no usable node types
      if len(all_valid) == 0:
        return None
      all_unused_valid = [ntype for ntype in all_valid if ntype not in avoid_used]
      if len(all_unused_valid) > 0:
        return all_unused_valid[0]
      # remaining node types are valid, but used
      if len(avoid_used) == 0:
        logger.warning('generate_tsp_with_generator._choose_best_starting_node_type: Should not happen')
        return None
      return avoid_used[0]

    def __hack_is_built_in_function_name_PY(mapped_node: pds.DuoGlotNode) -> bool:
      '''
      HACK for Python only
      '''
      # parent must be `call`
      if mapped_node.get_parent().get_ts_node_type() != 'call':
        return False
      # `mapped_node` must be a `identifier`
      if mapped_node.get_ts_node_type() != 'identifier':
        return False
      # `mapped_node` must be first child of `call`
      if mapped_node.get_parent().get_children()[0] != mapped_node:
        return False
      literal = mapped_node.get_children()[0].get_type()
      return literal in p_consts.PY_BUILT_IN_FUNCTIONS

    # HACK if the node is a built-in function, return it as is
    if __hack_is_built_in_function_name_PY(mapped_node):
      literal = mapped_node.get_children()[0].get_type()
      return literal, literal

    # TODO both lists below may end up containing duplicates
    avoid_error = []
    avoid_used = []
    code1 = None
    while True:
      alt_ntype1 = __choose_next_best_starting_node_type(alt_node_types, avoid_error, avoid_used)
      if alt_ntype1 is None:
        break
      code1 = _gen_code_for_node_type(alt_ntype1, template_dict, grammar)
      if not p_utils.does_have_parse_error(code1, template_dict['src_lang']):
      # if p_utils.compilable_py(code1):
        avoid_used.append(alt_ntype1)
        break
      avoid_error.append(alt_ntype1)

    if code1 is None:
      raise _CannotGenerateCorrectProgramError('Cannot generate `code1`')

    code2 = None
    while True:
      alt_ntype2 = __choose_next_best_starting_node_type(alt_node_types, avoid_error, avoid_used)
      if alt_ntype2 is None:
        break
      code2 = _gen_code_for_node_type(alt_ntype2, template_dict, grammar)
      if not p_utils.does_have_parse_error(code2, template_dict['src_lang']):
      # if p_utils.compilable_py(code2):
        avoid_used.append(alt_ntype2)
        break
      avoid_error.append(alt_ntype2)

    if code2 is None:
      raise _CannotGenerateCorrectProgramError('Cannot generate `code2`')

    return code1, code2

  def _gen_code_for_node_type(node_type: str, template_dict: dict, grammar: p_grammar.TreeSitterGrammar) -> str:
    '''
    NOTE the generated code may have semantic errors
    '''
    BLOCK_SPECIAL_TREATMENT = True
    if BLOCK_SPECIAL_TREATMENT and template_dict['is_insert_secret_fn']:
      if node_type == 'block':
        return p_consts.GENERIC_SECRET_FN_INVOCATION
      if node_type == 'list':
        return '[' + p_consts.GENERIC_SECRET_FN_INVOCATION + ']'
      if node_type == 'dictionary':
        return '{' + f'foo: {p_consts.GENERIC_SECRET_FN_INVOCATION}' + '}'

    ast = grammar.generate_simplest_ast(node_type)
    ast_tree = p_visitor_py.Tree.from_gen_ast(ast)
    # TODO fix type annotations for `accept` below as `code` is suggested to be `None`
    code = p_visitor_py.PrettyPrinterForGeneratedCode().visit(ast_tree.root_node)
    return code

  def _apply_alt_codes(alternative_codes: Dict[int, str], template_dict: dict) -> str:
    '''
    Given alternative codes (code blocks) for particular nodes,
    return an updated code with alternative codes applied.

    PARAM alternative_code: keys are `node_id`s, values are alternative codes.
    '''
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
    template_dict: dict,
    ignore_filter: bool
  ) -> Tuple[str, str]:
    '''
    PARAM ignore_filter: a boolean flag; when True, some nodes are filtered out
    with `__filter_alt_node_types` function.
    '''

    def __filter_alt_node_types(alt_node_types: List[str]) -> List[str]:
      filtered_list = []
      # remove duplicates (using sets messes up ranking)
      for alt_ntype in alt_node_types:
        if alt_ntype not in filtered_list:
          filtered_list.append(alt_ntype)
      # remove node types that we don't want to generate ASTs for
      filtered_list = [ntype for ntype in filtered_list if _can_be_added_to_fuzz_node_group(ntype)]
      return filtered_list

    # FOR EACH TEMPLATIZED NODE, GENERATE AN ALTERNATIVE AST
    alternative_codes_1 = {}
    alternative_codes_2 = {}

    # `alt_node_types` is a list of all alternative nodes including `mapped_node.get_type()`
    for mapped_node, alt_node_types in all_alt_starting_nodes:
      alt_node_types = alt_node_types if ignore_filter else __filter_alt_node_types(alt_node_types)
      code_1, code_2 = _gen_code_pair_for_node_with_check(mapped_node, alt_node_types, template_dict, grammar)
      alternative_codes_1[int(mapped_node.get_id())] = code_1
      alternative_codes_2[int(mapped_node.get_id())] = code_2

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

  _get_alt_starting_ntypes_cache = {}
  def _get_alt_starting_ntypes_cached(node: pds.DuoGlotNode, grammar: p_grammar.TreeSitterGrammar) -> List[Tuple[pds.DuoGlotNode, List[str]]]:
    ''''''
    nonlocal _get_alt_starting_ntypes_cache
    if node.get_id() in _get_alt_starting_ntypes_cache:
      return _get_alt_starting_ntypes_cache[node.get_id()]
    alt_starting_nodes = p_grammar.get_alternative_starting_node_types(node, grammar)
    _get_alt_starting_ntypes_cache[node.get_id()] = alt_starting_nodes
    return alt_starting_nodes

  logger.info('~~~ Starting API call to p_generator.generate_tsp_with_generator')

  # INPUTS TO THE GENERATOR
  lang = template_dict['src_lang']
  grammar = p_grammar.TreeSitterGrammar.from_dict(p_consts.GRAMMAR_DICT_READONLY[lang])
  problematic_node = _init_problematic_node(template_dict)
  logger.debug(f'Problematic node is "{problematic_node}"')

  # `program_pairs` is a list of tuples, each tuple is a pair of programs
  program_pairs : List[Tuple[str, str]] = []
  # _program_pairs_dbg : List[Tuple[str, str, str]] = []  # NOTE for debugging only

  # GROUPS OF NODES THAT CAN BE ROOTS OF ALTERNATIVE ASTs (similar to templatized nodes)
  fuzz_node_groups = _gen_seq_fuzz_node_groups_ALL(problematic_node, template_dict, grammar)
  logger.debug(f'There are {len(fuzz_node_groups)} fuzz node groups.')
  # p_utils.write_json('temporary_fuzz_node_groups.json', fuzz_node_groups)  # NOTE for debugging only

  for group_idx, fuzz_node_group in enumerate(fuzz_node_groups[:p_consts.MAX_NUM_FUZZ_NODE_GROUPS], start=1):
    # NOTE EXPERIMENTAL resetting a flag in `template_dict`
    # it is set to `True` in `_is_valid_fuzz_node`
    template_dict['is_insert_secret_fn'] = False

    # contains a list of alternative starting nodes for each node under
    # every node in `fuzz_node_group`,
    all_alt_starting_nodes : List[Tuple[pds.DuoGlotNode, List[str]]] = []

    # FIND ALTERNATIVE STARTING NODE TYPES
    for node in fuzz_node_group:
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
      # this is a special treatment of cases when a node type filtered out by
      # `__filter_alt_node_types` should be ignored, and not be filtered out.
      is_ignore_filter = len(fuzz_node_groups) == 1 and len(fuzz_node_group) == 1

      gen_src_prog_1, gen_src_prog_2 = _gen_program_pair(all_alt_starting_nodes, grammar, template_dict, ignore_filter=is_ignore_filter)
      program_pairs.append((gen_src_prog_1, gen_src_prog_2))
      # _program_pairs_dbg.append((gen_src_prog_1, gen_src_prog_2, str(fuzz_node_group)))  # NOTE for debugging only
    except _CannotGenerateCorrectProgramError as err:
      logger.warning(f'_gen_program_pair: {p_utils.exception_to_str(err)}')
      logger.debug(f'Cannot generate a TSP for this fuzz node group:\n{str(fuzz_node_group)}')
      continue

  # p_utils.write_json('temporary_gen_program_pairs.json', _program_pairs_dbg)  # NOTE for debugging only
  # remove duplicates, sanity check
  unique_tsps = _filter_program_pairs(program_pairs, template_dict)
  logger.debug(f'Generated {len(unique_tsps)} program pairs (TSPs):\n{json.dumps(unique_tsps, indent=2)}')

  return unique_tsps


# DEPRECATED
def _deprecated_generate_tsp_overfitted(template_dict: dict) -> Tuple[str, str]:
  '''
  Generate a TSP where literal nodes such as integer, float, identifier are fuzzed.
  '''

  def _is_literal_node(node: pds.PirelNode) -> bool:
    '''
    Return `True` if `node` has a single terminal child.

    NOTE `string` is also a literal node,
    however it needs a special treatment unlike e.g. `integer`
    '''
    if _hack_is_built_in_function_name_PY(node):
      return False
    if node.is_terminal():
      return False
    if len(node.get_children()) != 1:
      return False
    child = node.get_children()[0]
    if child.is_nonterminal():
      return False
    return True

  def _collect_literal_nodes(node: pds.PirelNode, literal_nodes: List[pds.PirelNode]) -> None:
    '''
    Collect all literal nodes in the AST.
    NOTE writes to `literal_nodes`
    '''
    if _is_literal_node(node):
      literal_nodes.append(node)
    for child in node.get_children():
      _collect_literal_nodes(child, literal_nodes)

  def _generate_code_for_literal_node(node: pds.PirelNode, grammar: p_grammar.TreeSitterGrammar) -> str:
    '''
    Generate code for a literal node.
    '''
    node_type = node.get_ts_node_type()
    ast = grammar.generate_simplest_ast(node_type)
    ast_tree = p_visitor_py.Tree.from_gen_ast(ast)
    code = p_visitor_py.PrettyPrinterForGeneratedCode().visit(ast_tree.root_node)
    return code

  def _generate_fuzzed_code_for_literal_nodes(
    literal_nodes: List[pds.PirelNode],
    context_node: pds.PirelNode,
    context_tree: pds.PirelTree,
    grammar: p_grammar.TreeSitterGrammar
  ) -> str:
    '''
    Generate code where all literal nodes are fuzzed.
    '''
    literal_nodes.sort(key=lambda node: node.get_id(), reverse=True)
    orig_text = context_node.get_text()
    for node in literal_nodes:
      code = _generate_code_for_literal_node(node, grammar)
      start_point = context_tree.annotation[node.get_id()][0]
      end_point = context_tree.annotation[node.get_id()][1]
      orig_text = orig_text[:start_point] + code + orig_text[end_point:]
    return orig_text

  def _hack_is_built_in_function_name_PY(node: pds.PirelNode) -> bool:
    '''
    HACK for Python only
    '''
    # parent must be `call`
    if node.get_parent().get_ts_node_type() != 'call':
      return False
    # `node` must be a `identifier`
    if node.get_ts_node_type() != 'identifier':
      return False
    # `node` must be first child of `call`
    if node.get_parent().get_children()[0] != node:
      return False
    literal = node.get_children()[0].get_type()
    return literal in p_consts.PY_BUILT_IN_FUNCTIONS

  logger.debug('~~~ Starting API call to p_generator.generate_tsp_overfitted')

  src_lang = template_dict['src_lang']
  problematic_node_path = template_dict['problematic_node_path']
  grammar = p_grammar.TreeSitterGrammar.from_dict(p_consts.GRAMMAR_DICT_READONLY[src_lang])

  template_origin = template_dict['template_origin']
  ast, ann = d_ast_parse.parse_text_dbg(template_origin, src_lang, keep_text=True)
  tree = pds.PirelTree(ast, ann)

  context_node = tree.get_root_node().get_children()[0]
  problematic_node = context_node.get_child_by_path(problematic_node_path)

  literal_nodes : List[pds.PirelNode] = []
  _collect_literal_nodes(problematic_node, literal_nodes)
  # filter out nodes types of which are external
  literal_nodes = [node for node in literal_nodes if not grammar.is_external(node.get_ts_node_type())]
  logger.debug(f'Literal nodes in the AST: {literal_nodes}')

  sp1 = template_origin
  sp2 = _generate_fuzzed_code_for_literal_nodes(literal_nodes, context_node, tree, grammar)
  tsp = (sp1, sp2)
  logger.debug(f'Generated overfitted TSP:\n{json.dumps(tsp, indent=2)}')

  return tsp


# NEW TSP GENERATION ALGORITHM
def generate_tsps_with_generator_new_algorithm(template_dict: dict) -> List[Tuple[str, str]]:
  '''
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
  '''

  def _init_problematic_node(template_dict: dict) -> pds.DuoGlotNode:
    '''
    Parse `template_origin` and return a reference to the `problematic_node`.
    '''
    # We need the `problematic_node`, which will be passed to the generator.
    # Since `template_origin` is already simplified, we use it to get the `problematic_node`.
    template_origin = template_dict['template_origin']
    lang = template_dict['src_lang']
    ast, _ = d_ast_parse.parse_text_dbg(template_origin, lang, keep_text=False)

    # p_utils.write_tmp_json('1ast.json', ast)  # NOTE for debugging only

    tree = pds.DuoGlotTree(ast)
    # `root_node` of `tree` should have only a single child, which is a `context_node`
    root_node = tree.get_root_node()
    assert len(root_node.get_children()) == 1, 'Root node of template origin must have just a single child'
    context_node = root_node.get_children()[0]
    problematic_node_path = template_dict['problematic_node_path']
    problematic_node = context_node.get_child_by_path(problematic_node_path)
    return problematic_node

  def _is_valid_fuzz_node(node: pds.DuoGlotNode, template_dict: dict, grammar: p_grammar.TreeSitterGrammar) -> bool:
    '''
    RETURN True if `node` can be passed to `p_grammar.get_alternative_starting_node_types`
    In other words, it tells us whether we can generate alternative nodes for children of `node`.
    Unlike, for example, an `integer` node. `integer` cannot be a fuzz
    node, because it itself is templatized, i.e. it is a child of a fuzz node.

    NOTE writes to `template_dict`.
    TODO should we reset "template_dict['is_insert_secret_fn']" to False?
    '''
    # a valid fuzz node has to be non-terminal
    if node.is_terminal():
      return False

    # a valid fuzz node must not be external
    if grammar.is_external(node.get_ts_node_type()):
      return False

    # a valid fuzz node cannot be of a "body node type"
    if node.get_ts_node_type() in p_consts.BODY_NODE_TYPES[template_dict['src_lang']]:
      # NOTE turn the flag on iff there is a non-terminal node
      # e.g. for empty `list`s and `dictionary`s it will stay `False`
      if node.get_num_nt_children() > 0:
        template_dict['is_insert_secret_fn'] = True
      return False

    # a valid fuzz node has to have at least one non-terminal child
    if node.get_num_nt_children() == 0:
      return False

    # a valid fuzz node must be a valid parent node for fuzz nodes
    if not _is_valid_fuzz_node_parent(node, template_dict):
      return False

    return True

  def _is_valid_fuzz_node_parent(node: pds.DuoGlotNode, template_dict: dict) -> bool:
    '''
    These nodes can be added to fuzz node groups, but none of their children can.
    NOTE does not prevent a node from being added to a fuzz node group
    '''
    assert _can_be_added_to_fuzz_node_group(node, template_dict), 'precondition failed'

    # literal nodes like `integer`, `float`, etc. cannot be fuzz node parents
    # they don't have non-terminal children
    if node.has_single_terminal_child():
      return False

    # `string` is also a literal node, however it needs a special treatment unlike e.g. `integer`
    if node.get_ts_node_type() == p_consts.NON_FUZZABLE_NODE_PARENTS_SPECIAL[template_dict['src_lang']]:
      return False

    # nodes like `block`. `block` is treated specially during program generation
    if node.get_ts_node_type() in p_consts.BODY_NODE_TYPES[template_dict['src_lang']]:
      return False

    return True

  def _can_be_added_to_fuzz_node_group(node_or_node_type: Union[pds.DuoGlotNode, str], template_dict: dict) -> bool:
    '''
    If a node does not appear in a fuzz node group, it will be kept intact.
    That is, a sub-tree with a root at this node will be unchanged.

    For example, if we want to avoid having `string` nodes fuzzed, we can add it here.
    '''

    assert isinstance(node_or_node_type, (str, pds.DuoGlotNode)), 'sanity check failed'

    if isinstance(node_or_node_type, pds.DuoGlotNode):
      node_type = node_or_node_type.get_ts_node_type()
    elif isinstance(node_or_node_type, str):
      node_type = node_or_node_type

    if node_type in p_consts.NON_FUZZABLE_NODES[template_dict['src_lang']]:
      return False

    return True

  def _gen_seq_fuzz_node_groups(problematic_node: pds.DuoGlotNode, template_dict: dict, grammar: p_grammar.TreeSitterGrammar) -> List[List[pds.DuoGlotNode]]:
    '''
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
    2. Generates all possible fuzz node group combinations.
    3. This function is language specific (hacky).
    4. A fuzz node group may contain both valid fuzz nodes AND nodes like `integer`, `float`, etc.
    '''

    def __get_descendable_children_fuzz_nodes(node: pds.DuoGlotNode, template_dict: dict) -> List[pds.DuoGlotNode]:
      '''
      Returns list of non-terminal nodes of `node` that `__rec_descend` will descend to.
      That means that nodes returned by this function will be added to fuzz node groups.
      '''
      # simplest case: return all non-terminal children
      # return node.get_nt_children()

      # more controlled version
      nodes = list(filter(lambda node: _can_be_added_to_fuzz_node_group(node, template_dict), node.get_nt_children()))
      return nodes

    def __rec_descend(start_node: pds.DuoGlotNode, template_dict: dict) -> List[List[pds.DuoGlotNode]]:
      '''
      Recursively get fuzz node group combinations for children nodes,
      make their cartesian product, add the node itself, and return.

      NOTE nodes that are `not _can_be_fuzz_node_ancestor` are added to the group
      '''
      # base case: last node (node from which cannot descend, a.k.a. "stop node")
      # if _is_stop_node(start_node, template_dict):  # `integer`, `float`, `identifier`, `block`, `string`
      if not _is_valid_fuzz_node_parent(start_node, template_dict):
        return [[start_node]]

      # collect children groups
      children_generations = []
      ch_fuzz_nodes = __get_descendable_children_fuzz_nodes(start_node, template_dict)
      for ntchild in ch_fuzz_nodes:
        child_generation = __rec_descend(ntchild, template_dict)
        children_generations.append(child_generation)

      # add start_node itself, and then add cartesian product of children
      all_generations = [[start_node]]

      # do not add a node if it has a single non-terminal child
      # e.g. ... -> expression_statement -> assignment -> (identifier, "=", integer)
      # "expression_statement" which is an "assignment"
      if len(start_node.get_children()) == 1 and start_node.get_children()[0].is_nonterminal():
        all_generations = []

      for cart_prod in itertools.product(*children_generations):
        generation = []
        for child_generation in cart_prod:
          generation.extend(child_generation)
        all_generations.append(generation)

      return all_generations

    def __sort_key(group: List[pds.DuoGlotNode]) -> Union[int, float]:
      '''
      Sorting algorithm for fuzz node groups.
      RETURN given the distances from nodes in `group` to the root node, return the maximum.
      '''
      max_depth = -1
      for node in group:
        node_depth = node.get_dist_root()
        if node_depth > max_depth:
          max_depth = node_depth
      return max_depth

    groups = __rec_descend(problematic_node, template_dict)
    groups.sort(key=__sort_key)
    return groups

  _get_alt_starting_ntypes_cache = {}
  def _get_alt_starting_ntypes_cached(node: pds.DuoGlotNode, grammar: p_grammar.TreeSitterGrammar) -> List[Tuple[pds.DuoGlotNode, List[str]]]:
    ''''''
    nonlocal _get_alt_starting_ntypes_cache
    if node.get_id() in _get_alt_starting_ntypes_cache:
      return _get_alt_starting_ntypes_cache[node.get_id()]
    alt_starting_nodes = p_grammar.get_alternative_starting_node_types(node, grammar)
    _get_alt_starting_ntypes_cache[node.get_id()] = alt_starting_nodes
    return alt_starting_nodes

  def _gen_code_for_node_type(node_type: str, template_dict: dict, grammar: p_grammar.TreeSitterGrammar) -> str:
    '''NOTE the generated code may have semantic errors'''

    if p_consts.ENABLE_SPECIAL_TREATMENT_FOR_BODY_NODE_TYPES and template_dict['is_insert_secret_fn']:
      spec_treatment_map = p_consts.SPECIAL_TREATMENT_BODY_NODE_TYPES[template_dict['src_lang']]
      if node_type in spec_treatment_map:
        return spec_treatment_map[node_type]

    ast = grammar.generate_simplest_ast(node_type)
    ast_tree = p_visitor_py.Tree.from_gen_ast(ast)
    code = p_visitor_py.PrettyPrinterForGeneratedCode().visit(ast_tree.root_node)
    return code

  def _gen_code_pair_for_node_with_check(
    mapped_node: pds.DuoGlotNode,
    alt_node_types: List[str],
    template_dict: dict,
    grammar: p_grammar.TreeSitterGrammar
  ) -> Tuple[str, str]:
    '''
    RETURN pair of "valid" programs or raise an exception.
    RAISE _CannotGenerateCorrectProgramError if both programs are `None`.
    '''

    def __pop_ranked(basic_ntypes_subset: Set[str], template_dict: dict) -> str:
      '''
      return a node type from `basic_ntypes_subset` that is ranked higher
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
      '''
      mapped_ntype = mapped_node.get_ts_node_type()
      basic_ntypes = set(p_consts.BASIC_NODE_TYPES[template_dict['src_lang']])
      alt_ntypes = set(alt_node_types)

      # case 1: mapped_node has a basic type
      if mapped_ntype in basic_ntypes:
        # {identifier, integer, float}, {identifier, integer}, {identifier} -> {integer}
        pure_alts = basic_ntypes.intersection(alt_ntypes).difference({mapped_ntype})

        # choose alternative basic type if possible (mapped_ntype, alt_ntype)
        if len(pure_alts) > 0:
          alt_ntype1 = mapped_ntype
          alt_ntype2 = __pop_ranked(pure_alts, template_dict)
          return alt_ntype1, alt_ntype2

        # otherwise fall back to the mapped_ntype (mapped_ntype, mapped_ntype)
        else:
          alt_ntype1 = mapped_ntype
          alt_ntype2 = mapped_ntype
          return alt_ntype1, alt_ntype2

      # case 2: can choose both alternatives from basic types
      in_both = basic_ntypes.intersection(alt_ntypes)
      if len(in_both) >= 2:
        # choose two different basic types from the intersection
        alt_ntype1 = __pop_ranked(in_both, template_dict)
        in_both.remove(alt_ntype1)
        alt_ntype2 = __pop_ranked(in_both, template_dict)
        return alt_ntype1, alt_ntype2

      # case 3: can choose only one alternative from basic types
      elif len(in_both) == 1:
        # choose the only basic type from the intersection
        alt_ntype1 = __pop_ranked(in_both, template_dict)
        alt_ntype2 = mapped_ntype
        return alt_ntype1, alt_ntype2

      # case 4: no basic types in the intersection: use mapped_ntype itself
      elif len(in_both) == 0:
        alt_ntype1 = mapped_ntype
        alt_ntype2 = mapped_ntype
        return alt_ntype1, alt_ntype2

      raise RuntimeError('should not reach here')

    alt_ntype1, alt_ntype2 = __get_alt_node_types(mapped_node, alt_node_types, template_dict)
    # NOTE TODO no check is performed on the generated code
    code1 = _gen_code_for_node_type(alt_ntype1, template_dict, grammar)
    code2 = _gen_code_for_node_type(alt_ntype2, template_dict, grammar)
    return code1, code2

  def _apply_alt_codes(alternative_codes: Dict[int, str], template_dict: dict) -> str:
    '''
    Given alternative codes (code blocks) for particular nodes,
    return an updated code with alternative codes applied.

    PARAM alternative_code: keys are `node_id`s, values are alternative codes.
    '''
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

  def _gen_program_pair_new_algorithm(
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

  # p_utils.write_tmp_json('1template_dict.json', template_dict)  # NOTE for debugging only

  logger.info('~~~ Starting API call to p_generator.generate_tsps_with_generator_new_algorithm')

  # INPUTS TO THE GENERATOR
  lang = template_dict['src_lang']
  grammar = p_grammar.TreeSitterGrammar.from_dict(p_consts.GRAMMAR_DICT_READONLY[lang])
  problematic_node = _init_problematic_node(template_dict)
  logger.debug(f'Problematic node is "{problematic_node}"')

  # `program_pairs` is a list of tuples, each tuple is a pair of programs
  program_pairs : List[Tuple[str, str]] = []
  _program_pairs_dbg = []  # NOTE for debugging only

  # GROUPS OF NODES THAT CAN BE ROOTS OF ALTERNATIVE ASTs (similar to templatized nodes)
  fuzz_node_groups = _gen_seq_fuzz_node_groups(problematic_node, template_dict, grammar)
  logger.debug(f'There are {len(fuzz_node_groups)} fuzz node groups.')

  # p_utils.write_tmp_json('1fuzz_node_groups.json', fuzz_node_groups)  # NOTE for debugging only

  for group_idx, fuzz_node_group in enumerate(fuzz_node_groups, start=1):
    # NOTE EXPERIMENTAL resetting a flag in `template_dict`
    # it is set to `True` in `_is_valid_fuzz_node`
    template_dict['is_insert_secret_fn'] = False

    # contains a list of alternative starting nodes for each node under
    # every node in `fuzz_node_group`,
    all_alt_starting_nodes : List[Tuple[pds.DuoGlotNode, List[str]]] = []

    # FIND ALTERNATIVE STARTING NODE TYPES
    for node in fuzz_node_group:
      if _is_valid_fuzz_node(node, template_dict, grammar):
        alt_starting_nodes = _get_alt_starting_ntypes_cached(node, grammar)
        all_alt_starting_nodes.extend(alt_starting_nodes)
      else:
        all_alt_starting_nodes.append((node, [node.get_ts_node_type()]))

    # p_utils.write_tmp_json(f'1fuzz_node_group_{group_idx}.json', all_alt_starting_nodes)  # NOTE for debugging only

    # APPLY ALTERNATIVE CODES AT DESIGNATED LOCATIONS
    # Since `fuzz_node_groups` are ordered from root nodes to leaf nodes,
    # `program_pairs` ends up containing the most abstract program pairs
    # first, and concrete program pairs next. That is, translation rule
    # inferred from first TSP would be the most abstract, and translation
    # rule inferred from last TSP would be the most concrete.
    try:
      gen_src_prog_1, gen_src_prog_2 = _gen_program_pair_new_algorithm(all_alt_starting_nodes, grammar, template_dict)
      program_pairs.append((gen_src_prog_1, gen_src_prog_2))
      _program_pairs_dbg.append((gen_src_prog_1, gen_src_prog_2, str(fuzz_node_group)))  # NOTE for debugging only
    except _CannotGenerateCorrectProgramError as err:
      logger.warning(f'_gen_program_pair_new_algorithm: {p_utils.exception_to_str(err)}')
      logger.debug(f'Cannot generate a TSP for this fuzz node group:\n{str(fuzz_node_group)}')
      continue

  # p_utils.write_tmp_json('1gen_program_pairs.json', _program_pairs_dbg)  # NOTE for debugging only

  # remove duplicates, sanity check
  unique_tsps = _filter_program_pairs(program_pairs, template_dict)
  logger.debug(f'Generated {len(unique_tsps)} program pairs (TSPs):\n{json.dumps(unique_tsps, indent=2)}')

  return unique_tsps


# TEST HARNESSES
def _test_simplify_template_init():
  test_harness_config:dict = p_utils.read_json('temporary_test_simplify_template_init_config.json')
  template_dict = p_utils.read_json(test_harness_config['template_dict_path'])
  kwargs = test_harness_config['kwargs']
  result_dict = simplify_template_init(template_dict, **kwargs)
  print(json.dumps(result_dict, indent=2))
  p_utils.write_json('temporary_test_simplify_template_init.json', result_dict)

def _test_generate_tsp_with_generator():
  test_harness_config:dict = p_utils.read_json('temporary_test_generate_tsp_with_generator_config.json')
  template_dict = p_utils.read_json(test_harness_config['template_dict_path'])
  kwargs = test_harness_config['kwargs']
  tsps = _deprecated_generate_tsps_with_generator_OLD(template_dict, **kwargs)
  p_utils.write_json('temporary_test_generate_tsp_with_generator.json', tsps)

def _test_generate_tsps_with_generator_new_algorithm():
  test_harness_config:dict = p_utils.read_tmp_json('test_generate_tsps_with_generator_new_algorithm_config.json')
  template_dict = p_utils.read_json(test_harness_config['template_dict_path'])
  tsps = generate_tsps_with_generator_new_algorithm(template_dict)
  p_utils.write_tmp_json('temporary_test_generate_tsps_with_generator_new_algorithm.json', tsps)

def _test_generate_tsp_overfitted():
  test_harness_config:dict = p_utils.read_json('temporary_test_generate_tsp_overfitted_config.json')
  template_dict = p_utils.read_json(test_harness_config['template_dict_path'])
  kwargs = {
    'subject_name': 'test_generate_tsp_overfitted'
  }
  tsp = _deprecated_generate_tsp_overfitted(template_dict, **kwargs)
  print(json.dumps(tsp, indent=2))
  p_utils.write_json('temporary_test_generate_tsp_overfitted.json', tsp)


if __name__ == '__main__':
  # _test_simplify_template_init()
  # _test_generate_tsp_with_generator()
  # _test_generate_tsp_overfitted()
  _test_generate_tsps_with_generator_new_algorithm()
