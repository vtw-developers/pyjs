import json
from typing import Dict, List, Tuple

import d_ast_parse
import p_consts
import p_data_structures as pds
import p_grammar
import p_utils
import p_visitor_py as pvpy


logger = p_utils.setup_logger(__name__)


ARTIF_CTX_TEMPLATE = 'return {}'
ARTIF_PROB_NPATH = [1]
ARTIF_CTX_NTYPE = 'return_statement'
ARTIF_CTX_NID = 1
ARTIF_PARPROG = f'return {p_consts.PAR_PROG_PROB_NODE_REPLACE};'


def _apply_alt_codes(
  alternative_codes: Dict[int, str],
  template_origin: str,
  src_lang: str,
) -> str:
  if len(alternative_codes) == 0:
    return template_origin
  tree = pds.PirelTree.from_code_str(template_origin, src_lang)
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


def _process_ctx_prob_nodes_diff(
  cursor_prob_node: pds.DuoGlotNode,
  context_node: pds.DuoGlotNode,
  template_dict: dict,
  grammar: p_grammar.TreeSitterGrammar,
) -> Tuple[List[Tuple[str, str]], dict]:
  '''
  problematic_node and context_node are different nodes
  PRE1: artif_template_origin has no parse error
  PRE2: problematic node under artif_context is similar to cursor_prob_node
  RETURN generated TSPs, updated template_dict
  '''

  '''
  Create two alternative snippets by replacing replacable nodes
  under `cursor_prob_node` with alternative identifiers.
  '''
  template_origin = template_dict['template_origin']
  src_lang = template_dict['src_lang']

  prob_nid = cursor_prob_node.get_id()
  prob_nstr = d_ast_parse.node_id_pretty_print(template_origin, src_lang, prob_nid)
  artif_template_origin = ARTIF_CTX_TEMPLATE.format(prob_nstr)

  # PRE1: check parse error under artificial context
  assert not p_utils.does_have_parse_error(artif_template_origin, src_lang), \
    'PRE1 broken: artificial context template has parse error'

  # PRE2: check similarity of problematic node under artificial context
  artif_tree = pds.DuoGlotTree.from_code_str(artif_template_origin, src_lang)
  assert len(artif_tree.root_node.get_children()) == 1
  artif_ctx_node = artif_tree.root_node.get_children()[0]
  artif_prob_node = artif_ctx_node.get_child_by_path(ARTIF_PROB_NPATH)
  assert cursor_prob_node.is_similar_to_rec(artif_prob_node), \
    'PRE2 broken: problematic node under artificial context is not similar to cursor_prob_node'

  template_dict['is_insert_secret_fn'] = False  # reset first
  artif_template_origin = pvpy.SecretFunInserter.insert_secret_functions(artif_template_origin)
  if p_consts.GENERIC_SECRET_FN_INVOCATION in artif_template_origin:
    template_dict['is_insert_secret_fn'] = True

  replacable_nodes = _get_replacable_nodes(artif_prob_node, artif_ctx_node, grammar)
  replacable_nodes = _check_exclude_nodes(replacable_nodes)

  alternative_codes1 = {}
  alternative_codes2 = {}
  for idx, mapped_node in enumerate(replacable_nodes, start=1):
    alt_code1 = f'var{idx}'
    alt_code2 = f'pirel_var{idx}'
    assert alt_code1 not in artif_template_origin, f'Collision: {alt_code1} already in artif_template_origin'
    assert alt_code2 not in artif_template_origin, f'Collision: {alt_code2} already in artif_template_origin'
    alternative_codes1[int(mapped_node.get_id())] = alt_code1
    alternative_codes2[int(mapped_node.get_id())] = alt_code2

  snippet1 = _apply_alt_codes(alternative_codes1, artif_template_origin, src_lang)
  snippet2 = _apply_alt_codes(alternative_codes2, artif_template_origin, src_lang)

  artif_contexts = [
    {
      'source_context': [
        [
          cursor_prob_node.get_type()
        ],
        [
          'py.return_statement'
        ]
      ],
      'target_context': [
        [
          'unknown'
        ],
        [
          'js.return_statement'
        ]
      ]
    }
  ]

  artif_template_dict = {
    'template_id': template_dict['template_id'],
    'src_lang': template_dict['src_lang'],
    'tar_lang': template_dict['tar_lang'],
    'template_origin': snippet1,
    'context_node_type': ARTIF_CTX_NTYPE,
    'context_node_id': ARTIF_CTX_NID,
    'problematic_node_type': cursor_prob_node.get_ts_node_type(),
    'problematic_node_id': cursor_prob_node.get_id(),
    'problematic_node_path': ARTIF_PROB_NPATH,
    'is_valid_template': template_dict['is_valid_template'],
    'is_insert_secret_fn': template_dict['is_insert_secret_fn'],
    'contexts': artif_contexts,
    'partial_program': ARTIF_PARPROG,
  }

  return [(snippet1, snippet2)], artif_template_dict


def _process_ctx_prob_nodes_same(
  cursor_prob_node: pds.DuoGlotNode,
  context_node: pds.DuoGlotNode,
  template_dict: dict,
  grammar: p_grammar.TreeSitterGrammar,
) -> Tuple[List[Tuple[str, str]], dict]:
  '''
  problematic_node and context_node are the same node
  RETURN generated TSPs, updated template_dict
  '''

  '''
  For certain node types, TSPs are template_origin itself
  '''
  if context_node.get_ts_node_type() in ['raise_statement']:
    template_dict['partial_program'] = p_consts.PAR_PROG_PROB_NODE_REPLACE + ';'
    return [(template_dict['template_origin'], template_dict['template_origin'])], template_dict

  '''
  Create two alternative snippets by replacing replacable nodes
  under `cursor_prob_node` with alternative identifiers.
  '''
  template_origin = template_dict['template_origin']
  template_origin = pvpy.SecretFunInserter.insert_secret_functions(template_origin)
  template_dict['is_insert_secret_fn'] = False  # reset first
  if p_consts.GENERIC_SECRET_FN_INVOCATION in template_origin:
    template_dict['is_insert_secret_fn'] = True

  # new tree since template_origin may have changed
  tree = pds.DuoGlotTree.from_code_str(template_origin, template_dict['src_lang'])
  root_node = tree.get_root_node()
  assert len(root_node.get_children()) == 1, 'Root node of template origin must have just a single child'
  new_ctx_node = root_node.get_children()[0]
  new_prob_node = new_ctx_node.get_child_by_path(template_dict['problematic_node_path'])
  assert new_prob_node is new_ctx_node, 'cursor_prob_node must be the same as problematic_node'

  replacable_nodes = _get_replacable_nodes(new_prob_node, new_ctx_node, grammar)
  replacable_nodes = _check_exclude_nodes(replacable_nodes)

  alternative_codes1 = {}
  alternative_codes2 = {}
  for idx, mapped_node in enumerate(replacable_nodes, start=1):
    alt_code1 = f'var{idx}'
    alt_code2 = f'pirel_var{idx}'
    assert alt_code1 not in template_origin, f'Collision: {alt_code1} already in template_origin'
    assert alt_code2 not in template_origin, f'Collision: {alt_code2} already in template_origin'
    alternative_codes1[int(mapped_node.get_id())] = alt_code1
    alternative_codes2[int(mapped_node.get_id())] = alt_code2

  src_lang = template_dict['src_lang']
  snippet1 = _apply_alt_codes(alternative_codes1, template_origin, src_lang)
  snippet2 = _apply_alt_codes(alternative_codes2, template_origin, src_lang)

  empty_context = [
    {
      'source_context': [
        [
          context_node.get_type()
        ]
      ],
      'target_context': [
        [
          'unknown'
        ]
      ]
    }
  ]

  template_dict = {
    'template_id': template_dict['template_id'],
    'src_lang': template_dict['src_lang'],
    'tar_lang': template_dict['tar_lang'],
    'template_origin': snippet1,
    'context_node_type': template_dict['context_node_type'],
    'context_node_id': template_dict['context_node_id'],
    'problematic_node_type': cursor_prob_node.get_ts_node_type(),
    'problematic_node_id': cursor_prob_node.get_id(),
    'problematic_node_path': context_node.get_path_to_child(cursor_prob_node),
    'is_valid_template': template_dict['is_valid_template'],
    'is_insert_secret_fn': template_dict['is_insert_secret_fn'],
    'contexts': empty_context,
    'partial_program': p_consts.PAR_PROG_PROB_NODE_REPLACE + ';',
  }

  return [(snippet1, snippet2)], template_dict


def _check_exclude_nodes(
  nodes: List[pds.DuoGlotNode],
) -> List[pds.DuoGlotNode]:
  '''
  Exclude nodes that are not suitable for replacement.
  '''

  def _pattern_1_builtin_module_accessed_dot_not(node: pds.DuoGlotNode) -> bool:
    '''
    Pattern 1: builtin module is accessed with dot notation, e.g., `math.pi`
                                                                    ^^^^
    '''
    # ANCHOR
    if node.is_terminal():
      return False
    if node.get_ts_node_type() != 'identifier':
      return False
    parent = node.get_parent()
    assert parent is not None, 'parent cannot be None'
    if parent.get_ts_node_type() != 'attribute':
      return False
    node_idx = parent.get_children().index(node)
    if node_idx != 0:
      return False
    # CHECK
    text = node.children[0].get_type()
    if text not in p_consts.PY_BUILT_IN_MODULES:
      return False
    logger.debug(f'Excluding node {node.get_id()}: built-in module')
    return True

  def _pattern_2_attribute_of_builtin_module(node: pds.DuoGlotNode) -> bool:
    '''
    Pattern 2: attribute of built-in module, e.g., `math.pi`
                                                         ^^
    '''
    # ANCHOR
    if node.is_terminal():
      return False
    if node.get_ts_node_type() != 'identifier':
      return False
    parent = node.get_parent()
    assert parent is not None, 'parent cannot be None'
    if parent.get_ts_node_type() != 'attribute':
      return False
    # must be the last child of parent
    if parent.get_children()[-1] is not node:
      return False
    # module
    first_child = parent.get_children()[0]
    if first_child.get_ts_node_type() != 'identifier':
      return False
    # CHECK
    text = first_child.children[0].get_type()
    if text not in p_consts.PY_BUILT_IN_MODULES:
      return False
    logger.debug(f'Excluding node {node.get_id()}: attribute of built-in module')
    return True

  def _pattern_3_builtin_fn_call(node: pds.DuoGlotNode) -> bool:
    '''
    Pattern 3: built-in function call, e.g., `len(s)`
                                              ^^^
    '''
    # ANCHOR
    if node.is_terminal():
      return False
    if node.get_ts_node_type() != 'identifier':
      return False
    parent = node.get_parent()
    assert parent is not None, 'parent cannot be None'
    if parent.get_ts_node_type() != 'call':
      return False
    node_idx = parent.get_children().index(node)
    if node_idx != 0:
      return False
    # CHECK
    text = node.children[0].get_type()
    if text not in p_consts.PY_BUILT_IN_FUNCTIONS:
      return False
    logger.debug(f'Excluding node {node.get_id()}: built-in function call')
    return True

  def _pattern_4_parent_is_list(node: pds.DuoGlotNode) -> bool:
    '''
    Pattern 4: parent is a list literal, e.g., `[a, b, c]`
                                                 ^  ^  ^
    '''
    parent = node.get_parent()
    if parent is None:
      return False
    if parent.get_ts_node_type() == 'list':
      logger.debug(f'Excluding node {node.get_id()}: parent is list node')
      return True
    return False

  patterns = [
    lambda n: _pattern_1_builtin_module_accessed_dot_not(n),
    lambda n: _pattern_2_attribute_of_builtin_module(n),
    lambda n: _pattern_3_builtin_fn_call(n),
    lambda n: _pattern_4_parent_is_list(n),
  ]

  result = []
  for node in nodes:
    if any(pattern(node) for pattern in patterns):
      continue
    result.append(node)
  return result


def _get_replacable_nodes(
  node: pds.DuoGlotNode,
  context_node: pds.DuoGlotNode,
  grammar: p_grammar.TreeSitterGrammar,
) -> List[pds.DuoGlotNode]:
  '''
  Get list of nodes under `node` that can be replaced with `identifier`.
  '''

  # base case: no non-terminal children
  if len(node.get_nt_children()) == 0:
    return []

  # base case: single non-terminal child
  if len(node.get_children()) == len(node.get_nt_children()) == 1:
    return _get_replacable_nodes(node.get_children()[0], context_node, grammar)

  # special case: call node with attribute as first child
  # do not recurse into the object of the attribute
  # e.g., s.strip().lower() --> do not recurse into s.strip()
  if node.get_ts_node_type() == 'call':
    first_child = node.get_children()[0]  # function
    second_child = node.get_children()[1]  # arguments
    if first_child.get_ts_node_type() == 'attribute':
      _first_child = first_child.get_children()[0]
      return [_first_child] + _get_replacable_nodes(second_child, context_node, grammar)

  result = []
  alt_starting_nodes = p_grammar.get_alternative_starting_node_types(node, grammar)
  assert len(alt_starting_nodes) == len(node.get_nt_children()), 'number of alternative starting nodes must equal number of non-terminal children'

  for alt_node, alt_node_types in alt_starting_nodes:
    # special case: keyword_argument node
    # only recurse into the value, not the key
    if alt_node.get_ts_node_type() == 'keyword_argument':
      value_child = alt_node.get_children()[-1]
      result.append(value_child)
      continue

    # special case: pattern_list node under for_statement
    # do not recurse into pattern_list
    if alt_node.get_ts_node_type() == 'pattern_list' and context_node.get_ts_node_type() == 'for_statement':
      result.extend(alt_node.get_nt_children())
      continue

    # special case: do not recurse into block node
    if alt_node.get_ts_node_type() == 'block':
      continue

    if 'identifier' in alt_node_types:
      result.append(alt_node)
      continue

    result.extend(_get_replacable_nodes(alt_node, context_node, grammar))

  return result


def _process_problematic_node(
  problematic_node: pds.DuoGlotNode,
  context_node: pds.DuoGlotNode,
  template_dict: dict,
  grammar: p_grammar.TreeSitterGrammar,
) -> Tuple[List[Tuple[str, str]], dict]:
  '''
  RETURN generated TSPs, updated template_dict
  '''

  template_origin = template_dict['template_origin']
  src_lang = template_dict['src_lang']

  '''
  Set the cursor to the problematic node, and move up the tree until we hit
  1. the context node, or
  2. a node that has the same AST under the artificial context.
  '''
  cursor_prob_node = problematic_node
  iter_count = 0
  while cursor_prob_node is not context_node:
    iter_count += 1

    prob_nid = cursor_prob_node.get_id()
    prob_nstr = d_ast_parse.node_id_pretty_print(template_origin, src_lang, prob_nid)
    artif_template_origin = ARTIF_CTX_TEMPLATE.format(prob_nstr)

    if p_utils.does_have_parse_error(artif_template_origin, src_lang):
      cursor_prob_node = cursor_prob_node.get_parent()
      continue

    artif_tree = pds.DuoGlotTree.from_code_str(artif_template_origin, src_lang)
    assert len(artif_tree.root_node.get_children()) == 1
    artif_ctx_node = artif_tree.root_node.get_children()[0]
    artif_prob_node = artif_ctx_node.get_child_by_path(ARTIF_PROB_NPATH)
    if not cursor_prob_node.is_similar_to_rec(artif_prob_node):
      cursor_prob_node = cursor_prob_node.get_parent()
      continue

    break

  if cursor_prob_node is context_node:
    return _process_ctx_prob_nodes_same(
      cursor_prob_node,
      context_node,
      template_dict,
      grammar,
    )
  else:
    return _process_ctx_prob_nodes_diff(
      cursor_prob_node,
      context_node,
      template_dict,
      grammar,
    )


def _debug_log(
  template_origin: str,
  src_lang: str,
  problematic_node: pds.DuoGlotNode,
  tsps: List[Tuple[str, str]],
) -> None:
  _, dgann = d_ast_parse.parse_text_dbg(template_origin, src_lang)
  lines = template_origin.split('\n')
  _, _, start, end = dgann[problematic_node.get_id()]
  strow, stcol = start
  enrow, encol = end
  if strow == enrow:
    lines.insert(strow + 1, ' ' * stcol + '^' * (encol - stcol))
  template_origin_highlighted = '\n'.join(lines)
  logger.debug(f'Template Origin with Problematic Node Highlighted:\n{template_origin_highlighted}')
  logger.debug(f'Generated TSPs:\n{json.dumps(tsps, indent=2)}')


def generate_tsps_lightweight(
  template_dict: dict
) -> Tuple[List[Tuple[str, str]], dict]:
  '''
  RETURN generated TSPs, updated template_dict

  NOTE template_dict must contain:
  - template_id
  - template_origin
  - src_lang
  - tar_lang
  - context_node_type
  - context_node_id
  - problematic_node_path
  - is_valid_template
  - is_insert_secret_fn

  NOTE the following fields are added/updated in the returned template_dict:
  - template_origin
  - context_node_type
  - context_node_id
  - problematic_node_type
  - problematic_node_id
  - problematic_node_path
  - is_insert_secret_fn
  - contexts
  - partial_program
  '''
  p_utils.log_json_time('args-generate-tsps-lightweight.json', locals())

  src_lang = template_dict['src_lang']
  template_origin = template_dict['template_origin']
  problematic_node_path = template_dict['problematic_node_path']
  grammar = p_grammar.TreeSitterGrammar.from_dict(p_consts.GRAMMAR_DICT_READONLY[src_lang])

  tree = pds.DuoGlotTree.from_code_str(template_origin, src_lang)
  root_node = tree.get_root_node()
  assert len(root_node.get_children()) == 1, 'root_node must have a single child'
  context_node = root_node.get_children()[0]
  problematic_node = context_node.get_child_by_path(problematic_node_path)

  tsps, template_dict = _process_problematic_node(
    problematic_node,
    context_node,
    template_dict,
    grammar,
  )
  _debug_log(template_origin, src_lang, problematic_node, tsps)

  return tsps, template_dict


# TEST HARNESSES
def _test_generate_tsps_lightweight():
  '''
  def generate_tsps_lightweight(
    template_dict: dict
  ) -> Tuple[Tuple[str, str], dict]:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_generate_tsps_lightweight_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  template_dict = args_dict['template_dict']

  tsp, updated_template_dict = generate_tsps_lightweight(template_dict)

  data = {
    'tsps': tsp,
    'template_dict': template_dict,
    'updated_template_dict': updated_template_dict,
  }
  print(f'Updated Template Dict: \n{json.dumps(updated_template_dict, indent=2)}\n')
  print(f'Template Dict: \n{json.dumps(template_dict, indent=2)}\n')
  print(json.dumps(data) + '\n')
  print(f'Generated TSPs: \n{json.dumps(tsp, indent=2)}')


if __name__ == '__main__':
  _test_generate_tsps_lightweight()
