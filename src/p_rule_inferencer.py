import json
from typing import Callable, Dict, List, Tuple

import d_ast_match
import d_ast_parse
import d_utils
import p_consts
import p_rule_postprocessor as prpp
import p_subject
import p_tree_log as ptlog
import p_utils


logger = p_utils.setup_logger(__name__)


class ContextNotFoundError(RuntimeError): pass


# INTERNAL FUNCTIONS
def get_segments_marks(segments: List[str], is_ignore_semicolor: bool) -> List[List[int]]:
  '''
  Given a list of program segments,
  return a list of begin/end marks for each segment.
  Since we pass all blocks of code joined together with a `\n`,
  the marks for blocks[1:] are calculated relative to blocks[0].
  '''
  def _begin_row_ith_segment(i: int, segments_lines: List[List[str]]):
    '''Begin row of i-th segment -> sum of number of lines of all previous segments'''
    nlines_prev_segs = 0
    for j in range(i):
      nlines_prev_segs += len(segments_lines[j])
    return nlines_prev_segs

  segments_lines = list(map(lambda segment: segment.split('\n'), segments))
  marks = []
  for i in range(0, len(segments_lines)):
    begin_col = 0
    begin_row = _begin_row_ith_segment(i, segments_lines)
    end_col = len(segments_lines[i][-1])  # length of last line of i-th segment

    # NOTE HACK this is a javascript specific hack, ignore semicolon at the end of segment
    # if it's a one-line segment
    if is_ignore_semicolor and len(segments_lines[i]) == 1:
      if segments_lines[i][-1].endswith(';'):
        end_col -= 1

    end_row = begin_row + len(segments_lines[i]) - 1  # of lines of i-th segment
    marks.append([begin_row, begin_col, end_row, end_col])
  return marks


def get_node_ids_to_node_asts_dict(ast):
  ''''''
  def _rec(ast_node, mutable_dict):
    # skip terminals
    if not isinstance(ast_node, list): return
    # skip string anno
    if len(ast_node) >= 1 and ast_node[0] == 'anno': return

    assert len(ast_node) > 2, 'Non-terminal AST node should have at least one child: debug'
    node_id = ast_node[1]
    mutable_dict[node_id] = ast_node
    # recurse children
    for i in range(2, len(ast_node)):
      _rec(ast_node[i], mutable_dict)
  result_dict = {}
  _rec(ast, result_dict)
  return result_dict


def query_range(ann, ast, marks):
  '''
  For each mark (#marks == #source-programs == #pairs)
  find nodes that contain that mark entirely (i.e. nodes that subsume the marked region)
  The output follows this structure:
  [
    [
      mark1,
      [
        [node_id, node, node_ann],
        [node_id, node, node_ann],
        ...
      ]
    ],
    [
      mark2,
      [
        [node_id, node, node_ann],
        [node_id, node, node_ann],
        ...
      ]
    ],
    ...
  ]

  p** - parent
  c** - child
  *s* - start
  *e* - end
  **l - line
  **c - character

  TODO what if there are multiple nodes spanning a mark?
  '''
  def _is_included(parent_range, child_range):
    psl, psc, pel, pec = parent_range
    csl, csc, cel, cec = child_range
    if (csl > psl or (csl == psl and csc >= psc)) and (cel < pel or (cel == pel and cec <= pec)):
      return True
    return False

  # tighter version of _is_included
  def _is_exact(parent_range, child_range):
    psl, psc, pel, pec = parent_range
    csl, csc, cel, cec = child_range
    if csl == psl and csc == psc and cel == pel and cec == pec:
      return True
    return False

  node_ids_to_node_asts_dict = get_node_ids_to_node_asts_dict(ast)
  result = []
  for mark in marks:
    included_range_info = []
    for node_id in ann:
      node_ann = ann[node_id]
      node_range = node_ann[2] + node_ann[3]
      # `node` contains `mark` entirely
      if _is_exact(node_range, mark):
        included_range_info.append([node_id, node_ids_to_node_asts_dict[node_id], node_ann])

    if len(included_range_info) == 0:
      logger.warning('The boundaries of source code did not match any AST nodes. '
                     'It might be due to multiple AST nodes under a root node. '
                     'For example, multiple `expression_statement` nodes under `module` node.')

    result.append([mark, included_range_info])
  return result


def ast_to_s_expr(node: list, depth_val: int, is_ignore_str: bool):
  '''
  node: DuoGlot-style AST node
  depth_val: ?
  is_ignore_str: ?
  '''

  def _hacky_should_insert_nostr_after_strs(node_type):
    '''
    hacky function for js used in `_ruleInfInternal_ns.astToSExpr`
    previous function name: SHOULD_INSERT_NOSTR_AFTER_STRS
    TODO generalize?
    '''
    if node_type == 'js.arrow_function':
      return True
    if node_type == 'js.method_definition':
      # NOTE this branch contains a reference to suspicious variable
      # refer to the original source file index_editrule.js in original-duoglot branch
      raise RuntimeError('should not happen')
    return False

  def _hacky_is_parent_name_valchild(node_type: str):
    '''
    hacky function used in `_ruleInfInternal_ns.astToSExpr`
    previous function name: IS_PARNAME_VALCHILD
    TODO generalize?
    '''
    if 'py.comment' in node_type:
      return True
    if 'py.string_content' in node_type:
      return True
    if 'identifier' in node_type:
      return True
    if 'string_fragment' in node_type:
      return True
    if 'number' in node_type:
      return True
    if 'integer' in node_type:
      return True
    if 'regex_pattern' in node_type:
      return True
    if 'regex_flags' in node_type:
      return True
    if node_type == 'py.float':
      return True
    return False

  def _s_expr_rec(_node, _parent_name: str, _current_depth: int):
    assert _current_depth < depth_val, 'too deep AST: check the original source code'

    # `_node` is non-terminal
    if isinstance(_node, list):
      _node_type = _node[0]

      # fragment node (top-most node)
      if _node_type == 'fragment':
        ret_arr = ['fragment']
        # there is only one child actually
        for i in range(1, len(_node)):
          child_res = _s_expr_rec(_node[i], _node_type, _current_depth + 1)
          ret_arr.append(child_res)
        return ret_arr

      # string annotation node
      elif _node_type == 'anno':
        ret_arr = ['anno ']
        # children
        for i in range(1, len(_node)):
          _child_type = _node[i][0]
          _child_value = _node[i][1]
          ret_arr.append([_child_type, _child_value])
        return ret_arr

      # all remaining node types (NT & T)
      else:
        ret_arr = ['"' + _node_type + '"']
        nostr_tbd = _hacky_should_insert_nostr_after_strs(_node_type)
        # iterate children, skip node_id
        for i in range(2, len(_node)):
          # special treatment for js: nostr
          if nostr_tbd and not isinstance(_node[i], str):
            ret_arr.append(['nostr'])
            nostr_tbd = False
          child_res = _s_expr_rec(_node[i], _node_type, _current_depth + 1)
          ret_arr.append(child_res)
        if nostr_tbd:
          raise RuntimeError('Should not happen. Check the original source code')
        return ret_arr

    # should not happen in proper AST's
    elif isinstance(_node, int):
      logger.warning(f'unexpected int node: {_node}')

    # `node` is terminal
    else:
      if _hacky_is_parent_name_valchild(_parent_name):
        return ['val', _node]
      else:
        if is_ignore_str:
          logger.warning(f'str node (ignored): {_node}')
          return ''
        return ['str', _node]

  assert node is not None, 'input node should not be None'
  result = _s_expr_rec(node, _parent_name=node[0], _current_depth=0)
  return result


def unify_ast_fragments(
  asts,
  mutable_phs,
  mutable_tuple_phs,
  wildcard_ph_func: Callable,
  are_source_segments: bool
):
  '''
  `asts`: AST's that are to be unified

  `fragment`:
  ["fragment" ast]

  `sExpr`:
  AST-like structure (refer to logs)
  '''
  fragments = list(map(lambda ast: ['fragment', ast], asts))
  s_exprs = list(map(lambda fragment: ast_to_s_expr(fragment, depth_val=100, is_ignore_str=False), fragments))

  # log (uncomment for debugging)
  for i in range(0, len(s_exprs)):
    segment_text = 'source' if are_source_segments else 'target'
    # p_utils.log_json_time(f'{segment_text}-ast-to-s-expr-logs-seg{i}.json', s_expr_log_results[i][1])
    # p_utils.log_json_time(f'{segment_text}-ast-to-unify-seg{i}.json', fragments[i])
    # p_utils.log_json_time(f'{segment_text}-s-expression-seg{i}.json', s_exprs[i])

  # the main unifying recursive function
  def _common_root_tree(s_exprs):
    _node_types = list(map(lambda x: x[0], s_exprs))
    # node types for all `s_exprs` have to be identical
    for name in _node_types:
      if name != _node_types[0]:
        return ['ERROR_DIFF_NAME']
    # at this point, node types are identical
    _common_node_type = _node_types[0]
    # common node type is `str`
    if _common_node_type == 'str':
      common_val = s_exprs[0][1]
      for s_expr in s_exprs:
        if len(s_expr) != 2:
          return ['ERROR_STR_NODE_LENGTH']
        if s_expr[1] != common_val:
          return wildcard_ph_func('_str_', s_exprs, mutable_phs, mutable_tuple_phs)
      return ['str', common_val]
    # common node type is `val`
    elif _common_node_type == 'val':
      common_val = s_exprs[0][1]
      for s_expr in s_exprs:
        if len(s_expr) != 2:
          return ['ERROR_VAL_NODE_LENGTH']
        if str(s_expr[1]) != str(common_val):
          return wildcard_ph_func('_val_', s_exprs, mutable_phs, mutable_tuple_phs)
      return ['val', common_val]
    # common node type is neither `str` nor `val`
    else:
      _is_nonterminal = lambda node_type: node_type.startswith('"') and node_type.find('.') > 0
      is_nt = _is_nonterminal(_common_node_type)
      is_fragment = _common_node_type == 'fragment'
      is_nostr = _common_node_type == 'nostr'

      # @satbek: unify string `anno`s
      # NOTE potentially buggy: unifies different types of strings (i.e. r'' with b'', etc.)
      # NOTE experimental: might be problematic with programs with complex strings
      is_anno = _common_node_type.strip() == 'anno'
      if is_anno:
        return None

      if not is_nt and not is_fragment and not is_nostr:
        return ['ERROR_NT_OR_FRAGMENT_EXPECTED']

      common_root = [_common_node_type]
      i = 0
      while True:
        i += 1
        # the expression `(x[i:i+1] or [None])[0]`
        # returns the element if it exists in the list, None otherwise
        # https://stackoverflow.com/questions/2492087/how-to-get-the-nth-element-of-a-python-list-or-a-default-if-not-available
        ith_children = list(map(lambda x: (x[i:i+1] or [None])[0], s_exprs))
        # the types of i-th children may differ
        # fix on the i-th child of the first segment
        s_expr_ith_child_segment1 = ith_children[0]
        if s_expr_ith_child_segment1 is None:
          if any(map(lambda x: x is not None, ith_children)):
            common_root.append(wildcard_ph_func('*', s_exprs, mutable_phs, mutable_tuple_phs))
          break
        # i-th child has to be a list
        if isinstance(s_expr_ith_child_segment1, (str, int)):
          common_root.append('ERROR_UNEXPECTED_STRING_OR_NUMBER')
          return common_root
        if not isinstance(s_expr_ith_child_segment1, list):
          common_root.append('ERROR_UNEXPECTED_NON_ARRAY_CHILD')
          return common_root
        # compare i-th child of the first segment
        # to the i-th children of the remaining segments
        to_be_common_is_nt = _is_nonterminal(s_expr_ith_child_segment1[0])
        to_be_common_node_type = s_expr_ith_child_segment1[0]
        name_diff_found = False
        all_nt = to_be_common_is_nt
        # iterate over i-th children of the remaining segments (j -> 1 ..)
        for j in range(1, len(ith_children)):
          s_expr_ith_child_segment_j = ith_children[j]
          # i-th child has to be an array
          if not isinstance(s_expr_ith_child_segment_j, list):
            common_root.append('ERROR_UNEXPECTED_NON_ARRAY_CHILD')
            return common_root
          # types of i-th children are different (thus need to be made into holes)
          if to_be_common_node_type != s_expr_ith_child_segment_j[0]:
            name_diff_found = True
          # all of the i-th children are non-terminals (need for distinguishing b/w `.` and '*)
          if to_be_common_is_nt and not _is_nonterminal(s_expr_ith_child_segment_j[0]):
            all_nt = False
        # i-th children are non-terminals (recurse down)
        if all_nt:
          if name_diff_found:
            common_root.append(wildcard_ph_func('.', ith_children, mutable_phs, mutable_tuple_phs))
          else:
            common_root_tree_var = _common_root_tree(ith_children)

            # @satbek: None check due to `anno` check above
            # should not result in regression errors
            if common_root_tree_var is not None:
              common_root.append(common_root_tree_var)
        # i-th children are a mix of non-terminals and terminals (recurse right)
        else:
          if name_diff_found:
            common_root.append(wildcard_ph_func('*', s_exprs, mutable_phs, mutable_tuple_phs))
            break
          else:
            common_root_tree_var = _common_root_tree(ith_children)

            # @satbek: None check due to `anno` check above
            # should not result in regression errors
            if common_root_tree_var is not None:
              common_root.append(common_root_tree_var)
      return common_root

  unified = _common_root_tree(s_exprs)
  unified.append(wildcard_ph_func('*', 'TAIL', mutable_phs, mutable_tuple_phs))
  return unified


def src_wildcard_ph_func(
  x,
  diffing_s_exprs,
  mutable_src_phs,
  mutable_src_tuple_phs
):
  '''
  POST1: `srcPhs` is mutated
  POST2: `srcTuplePhs` is mutated
  '''
  if x == '.' or x == '*':
    mutable_src_phs.append(['x', diffing_s_exprs])
  elif x in mutable_src_tuple_phs:
    mutable_src_tuple_phs[x].append([x, diffing_s_exprs])
  else:
    raise RuntimeError('Should not happen. Please refer to the original code')
  # unreachable return? TODO debug
  return '"' + x + '"'


def tar_wildcard_ph_func(
  x,
  diffing_s_exprs,
  mutable_tar_phs,
  mutable_tar_tuple_phs
):
  '''
  POST1: `tarPhs` is mutated
  POST2: `tarTuplePhs` is mutated
  '''
  if x == '.' or x == '*':
    mutable_tar_phs.append([x, diffing_s_exprs])
    return '"' + x + f'PH{len(mutable_tar_phs)}"'
  elif x in mutable_tar_tuple_phs:
    mutable_tar_tuple_phs[x].append([x, diffing_s_exprs])
    return f'"_strPH{len(mutable_tar_tuple_phs[x])}_"' if x == '_str_' else f'"_valPH{len(mutable_tar_tuple_phs[x])}_"'
  else:
    # TODO debug this case
    raise RuntimeError('Should not happen. Please refer to the original code')
    return '"' + x + '"'


def compute_tree_distance(trees1, trees2, algo_name):
  ''''''
  dists = []
  for i in range(len(trees2)):
    rowdist = []
    for j in range(len(trees1)):
      rowdist.append(d_ast_match.distance_of_AST_frags(trees2[i], trees1[j], algo_name))
    dists.append(rowdist)
  return dists


def get_min_idxes(dist_matrix):
  ''''''
  result = []
  for i in range(0, len(dist_matrix)):
    row = dist_matrix[i]
    min_val = float('inf')
    min_idx = -1
    for j in range(0, len(row)):
      if row[j] < min_val:
        min_val = row[j]
        min_idx = j
    result.append(min_idx)
  return result


def set_ph(pattern, search_ph, replace_ph):
  if isinstance(pattern, list):
    return list(map(lambda x: set_ph(x, search_ph, replace_ph), pattern))
  if not isinstance(pattern, str):
    raise RuntimeError('set_ph expect nested string or array')
  if pattern == search_ph:
    return replace_ph
  return pattern


def pretty_s_expr_tree_like(s_expr, indent_size=2, global_indent='  '):
  '''
  This function is a supplementary to `_ruleInfInternal_ns.prettySExpr`
  Allows printing translation rules as tree-like that might be used for debugging.
  This function has no functional importance for Pirel.
  The default `_ruleInfInternal_ns.prettySExpr` is enough.

  `globalIndent`: custom prefix for all lines of the output
  '''
  def _rec(s_expr, indent_level, indent_size, global_indent):
    # base cases
    if isinstance(s_expr, str):
      return global_indent + (' ' * (indent_size * indent_level)) + s_expr
    if isinstance(s_expr, list) and len(s_expr) == 2 and isinstance(s_expr[0], str) and isinstance(s_expr[1], str):
      return global_indent + (' ' * (indent_size * indent_level)) + s_expr[0] + ' ' + s_expr[1]

    result = global_indent + (' ' * (indent_size * indent_level)) + '('
    result += s_expr[0]
    for i in range(1, len(s_expr)):
      result += '\n' + _rec(s_expr[i], indent_level+1, indent_size, global_indent)
    result += '\n' + global_indent + (' ' * (indent_size * indent_level)) + ')'
    return result
  result = _rec(s_expr, 0, indent_size, global_indent)
  return result


def pretty_s_expr(s_expr):
  '''
  `sExpr` has a very similar structure to DuoGlot style AST's.
  This function returns a string version of it which is THE version
  that is parsed by the DuoGlot transpiler.
  '''
  if isinstance(s_expr, list):
    result = ['(']
    for i in range(0, len(s_expr)):
      result.append(pretty_s_expr(s_expr[i]))
      if i < len(s_expr) - 1:
        result.append(' ')
    result.append(')')
    return ''.join(result)
  else:
    return str(s_expr)


def pretty_rule(match, expand, tree_like):
  '''
  Pretty-prints a translation rule to the standard format.
  '''
  rule_type = 'match_expand'
  if tree_like:
    return \
      f'({rule_type}\n\n' \
      f'{pretty_s_expr_tree_like(match)}\n\n' \
      f'{pretty_s_expr_tree_like(expand)}\n\n)'
  return \
    f'({rule_type}\n' \
    f'  {pretty_s_expr(match)}\n' \
    f'  {pretty_s_expr(expand)}\n)'


def _is_context_empty(context: dict) -> bool:
  source_context = context['source_context']
  target_context = context['target_context']

  # source or parent context have a parent -> have context
  if len(source_context) > 1 or len(target_context) > 1:
    assert len(source_context) > 1, 'sanity check'
    assert len(target_context) > 1, 'sanity check'
    return False

  source_node_and_siblings = source_context[0]
  target_node_and_siblings = target_context[0]

  # source or parent context have a sibling -> have context
  if len(source_node_and_siblings) > 1 or len(target_node_and_siblings) > 1:
    assert len(source_node_and_siblings) > 1, 'sanity check'
    assert len(source_node_and_siblings) > 1, 'sanity check'
    return False

  assert target_node_and_siblings[0] == 'unknown', 'sanity check'

  return True


# API
def infer_translation_rule(
  translation_pair: dict,
  src_lang: str,
  tar_lang: str,
  context: dict,
  is_insert_secret_fn: bool,  # for post-processing
  choose_largest_node: bool,  # choose the largest/smallest node for a given mark
  is_ignore_semicolon: bool,  # update end column of a mark depending on semicolon
  pretty_print_tree_like: bool
):
  '''
  program_pairs: [{"source": str, "target": str}, ...]

  Given a list of source-target program pairs, infer a translation rule.

  PARAMS
  programPairs
  [{source: str, target: str}, {source: str, target: str}, ...]

  srcLang - 'py'
  tarLang - 'js'

  pyBlockReplaced
  whether or not the program pairs contain a secret
  function call which replaces a block node (py.block, js.statement_block)

  TODO this parameter might be unnecessary after introduction of context info
  isChooseLargestContainingNode
  whether or not to choose a largest node that has
  the same boundaries as srcMarks or tarMarks

  ppTreeLike
  return rule pretty-printed as a tree (for visual)
  '''

  # 1 split program_pairs into source and target lists
  src_segments = list(map(lambda elem: elem['source'], translation_pair))
  tar_segments = list(map(lambda elem: elem['target'], translation_pair))

  # 2 get marks
  src_marks = get_segments_marks(src_segments, is_ignore_semicolor=is_ignore_semicolon)
  tar_marks = get_segments_marks(tar_segments, is_ignore_semicolor=is_ignore_semicolon)

  # 3 parse
  src_ast, src_ann = d_ast_parse.parse_text_dbg('\n'.join(src_segments), src_lang)
  tar_ast, tar_ann = d_ast_parse.parse_text_dbg('\n'.join(tar_segments), tar_lang)

  # 4 query range
  src_query_results = query_range(src_ann, src_ast, src_marks)
  tar_query_results = query_range(tar_ann, tar_ast, tar_marks)

  # 5
  src_phs = []
  src_tpl_phs = {'_str_': [], '_val_': []}
  tar_phs = []
  tar_tpl_phs = {'_str_': [], '_val_': []}

  # 6 unify AST fragments
  src_smallest_containing_nodes_per_segment = list(map(lambda x: x[1][-1][1], src_query_results))
  src_largest_containing_nodes_per_segment = list(map(lambda x: x[1][0][1], src_query_results))
  src_containing_nodes_per_segment = \
    src_largest_containing_nodes_per_segment if choose_largest_node else src_smallest_containing_nodes_per_segment
  src_unified_pattern = unify_ast_fragments(
    src_containing_nodes_per_segment,
    src_phs,
    src_tpl_phs,
    src_wildcard_ph_func,
    are_source_segments=True
  )

  tar_smallest_containing_nodes_per_segment = list(map(lambda x: x[1][-1][1], tar_query_results))
  tar_largest_containing_nodes_per_segment = list(map(lambda x: x[1][0][1], tar_query_results))
  tar_containing_nodes_per_segment = \
    tar_largest_containing_nodes_per_segment if choose_largest_node else tar_smallest_containing_nodes_per_segment
  tar_unified_pattern = unify_ast_fragments(
    tar_containing_nodes_per_segment,
    tar_phs,
    tar_tpl_phs,
    tar_wildcard_ph_func,
    are_source_segments=False
  )

  # 7
  phs_compare = compute_tree_distance(src_phs, tar_phs, None)
  str_compare = compute_tree_distance(src_tpl_phs['_str_'], tar_tpl_phs['_str_'], 'EXACT')
  val_compare = compute_tree_distance(src_tpl_phs['_val_'], tar_tpl_phs['_val_'], 'EXACT')

  # 8
  phs_match_idxes = get_min_idxes(phs_compare)
  str_match_idxes = get_min_idxes(str_compare)
  val_match_idxes = get_min_idxes(val_compare)

  # 9
  for i in range(0, len(phs_match_idxes)):
    tar_unified_pattern = set_ph(
      tar_unified_pattern,
      '"*PH' + str(i + 1) + '"',
      '"*' + str(phs_match_idxes[i] + 1) + '"'
    )
    tar_unified_pattern = set_ph(
      tar_unified_pattern,
      '".PH' + str(i + 1) + '"',
      '".' + str(phs_match_idxes[i] + 1) + '"'
    )

  for i in range(0, len(str_match_idxes)):
    tar_unified_pattern = set_ph(
      tar_unified_pattern,
      '"_strPH' + str(i + 1) + '_"',
      '"_str' + str(str_match_idxes[i] + 1) + '_"'
    )

  for i in range(0, len(val_match_idxes)):
    tar_unified_pattern = set_ph(
      tar_unified_pattern,
      '"_valPH' + str(i + 1) + '_"',
      '"_val' + str(val_match_idxes[i] + 1) + '_"'
    )

  # log
  # p_utils.log_json_time('source-unified-pattern.json', src_unified_pattern)
  # p_utils.log_json_time('target-unified-pattern.json', tar_unified_pattern)

  # 10 post-process inferred rule
  # NOTE Creating an instance of `TranslationRule` might raise `pptr.RuleMappingError`
  # It is good to be vocal about errors in translation rules.
  translation_rule = prpp.TranslationRule(src_unified_pattern, tar_unified_pattern)
  if not _is_context_empty(context):
    result = translation_rule.trim_context(context)
    if result is None:
      logger.error('Context is not found')
      raise ContextNotFoundError('context not found')
    src_unified_pattern, tar_unified_pattern = result

  if is_insert_secret_fn:
    while True:
      try:
        logger.debug(f'Replacing secret identifier with `*` placeholder.')
        translation_rule = prpp.TranslationRule(src_unified_pattern, tar_unified_pattern)
        translation_rule.replace_secret_with_placeholder(p_consts.GENERIC_SECRET_FN)
        src_unified_pattern = translation_rule.src_as_s_expression()
        tar_unified_pattern = translation_rule.tar_as_s_expression()
      except prpp.SecretNodeNotFoundError as err:
        logger.warning(err)
        break

  # 11
  return pretty_rule(src_unified_pattern, tar_unified_pattern, pretty_print_tree_like)


def infer_translation_rule_wrapper(
  subject: p_subject.PirelSubject,
  translation_pair: dict,
  src_lang: str,
  tar_lang: str,
  context: dict,
  is_insert_secret_fn: bool,
  choose_largest_node: bool,
  is_ignore_semicolon: bool
) -> str:
  '''
  Infer a translation rule for a single translation pair.

  RAISE all incoming errors

  TODO consider option to choose the largest or smallest containing nodes.
  '''
  p_utils.log_json_time(f'{subject.name}_args-infer_translation_rule_wrapper.json', locals())

  logger.debug(f'Translation pair:\n{json.dumps(translation_pair, indent=2)}')
  logger.debug(f'Context:\n{json.dumps(context, indent=2)}')

  translation_rule = infer_translation_rule(
    translation_pair,
    src_lang,
    tar_lang,
    context,
    is_insert_secret_fn,
    choose_largest_node,
    is_ignore_semicolon,
    pretty_print_tree_like=False
  )

  logger.debug(
    f'Inferred translation rule:\n{translation_rule}\n'
    f'Rule hash value: {d_utils.string_sha256(translation_rule)}'
  )
  p_utils.log_file_time(f'{subject.name}_learned-translation-rule.snart', translation_rule)

  return translation_rule


def infer_translation_rules(
  subject: p_subject.PirelSubject,
  template_dict: dict,
  translation_pairs: List[Tuple[Dict[str, str], Dict[str, str]]],
  lprule_inf_log: ptlog.PRuleInfLog
) -> List[str]:
  '''
  Infer translation rules for multiple translation pairs.

  RAISE None. All exceptions are handled.
  '''
  p_utils.log_json_time(f'{subject.name}_args-infer_translation_rules.json', locals())

  contexts : List[Dict[str, List[List[str]]]] = template_dict['contexts']
  src_lang = template_dict['src_lang']
  tar_lang = template_dict['tar_lang']
  is_insert_secret_fn = template_dict['is_insert_secret_fn']

  logger.debug(
    f'Attempting to infer translation rules from '
    f'{len(translation_pairs)} translation pairs and {len(contexts)} contexts'
  )

  _pot_rule_idx = 0
  _num_pot_rules = len(translation_pairs) * len(contexts) * 2 * 2
  trules_list = []

  for i, translation_pair in enumerate(translation_pairs, start=1):
    ltrans_pair = ptlog.TransPair.from_tuple(translation_pair)
    lprule_inf_log.translation_pairs.append(ltrans_pair)

    for j, context in enumerate(contexts, start=1):
      lcontext = ptlog.Context(j, context['source_context'], context['target_context'])
      ltrans_pair.contexts.append(lcontext)

      for choose_largest_node in [True, False]:
        for is_ignore_semicolon in [True, False]:
          lrule_inf_comb = ptlog.RuleInfComb()
          lrule_inf_comb.largest_and_ignore = [choose_largest_node, is_ignore_semicolon]
          lcontext.combinations.append(lrule_inf_comb)

          _pot_rule_idx += 1
          logger.debug(
            f'infer translation rule for (permutation {_pot_rule_idx}/{_num_pot_rules}):\n'
            f'translation pair {i}/{len(translation_pairs)}, context {j}/{len(contexts)}, '
            f'choose_largest_node={choose_largest_node}, is_ignore_semicolon={is_ignore_semicolon}')

          # NOTE be graceful, and skip translation pairs from which we get errors.
          try:
            translation_rule = infer_translation_rule_wrapper(
              subject,
              translation_pair,
              src_lang,
              tar_lang,
              context,
              is_insert_secret_fn,
              choose_largest_node,
              is_ignore_semicolon
            )

            # do not store duplicate rules
            if translation_rule not in trules_list:
              trules_list.append(translation_rule)
              logger.debug(f'Added newly inferred translation rule to the list.')
              logger.debug(f'The number of translation rules so far is {len(trules_list)}')

              ltrule = ptlog.TRule.from_str(translation_rule)
              lrule_inf_comb.translation_rule = ltrule
              lrule_inf_comb.num_inferred_rules += 1
              lcontext.num_inferred_rules += 1
              ltrans_pair.num_inferred_rules += 1
              lprule_inf_log.num_inferred_rules += 1

            else:
              msg = 'This rule already exists in the list. Skipping.'
              logger.warning(msg)
              lrule_inf_comb.reason = msg

          except Exception as exc:
            msg = 'Error during rule inference. Skip this one\n'
            msg += p_utils.exception_to_str(exc)
            logger.error(msg)
            lrule_inf_comb.reason = msg

          logger.debug(f'the number of translation rules so far is {len(trules_list)}')

  return trules_list


# TEST HARNESS FUNCTIONS
# TODO paths should be updated (p_consts.CWD)
def _test_infer_translation_rules():
  import p_consts
  config_fpath = p_consts.CWD / 'temporary_test_infer_translation_rules_config.json'
  config = p_utils.read_json(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  template_dict = args_dict['template_dict']
  translation_pairs = args_dict['translation_pairs']
  kwargs = args_dict['kwargs']

  trules_list = infer_translation_rules(template_dict, translation_pairs, **kwargs)
  p_utils.write_text('temporary_test_infer_translation_rules.snart', '\n\n\n'.join(trules_list))

# TODO paths should be updated (p_consts.CWD)
def _test_infer_translation_rule_wrapper():
  import p_consts
  config_fpath = p_consts.CWD / 'temporary_test_infer_translation_rule_wrapper_config.json'
  config = p_utils.read_json(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  translation_pair = args_dict['translation_pair']
  src_lang = args_dict['src_lang']
  tar_lang = args_dict['tar_lang']
  context = args_dict['context']
  is_insert_secret_fn = args_dict['is_insert_secret_fn']
  choose_largest_node = args_dict['choose_largest_node']
  is_ignore_semicolon = args_dict['is_ignore_semicolon']
  kwargs = args_dict['kwargs']

  translation_rule = infer_translation_rule_wrapper(
    translation_pair,
    src_lang,
    tar_lang,
    context,
    is_insert_secret_fn,
    choose_largest_node,
    is_ignore_semicolon,
    **kwargs
  )
  p_utils.write_text('temporary_test_infer_translation_rule_wrapper.snart', translation_rule)


if __name__ == '__main__':
  # _test_infer_translation_rules()
  _test_infer_translation_rule_wrapper()
