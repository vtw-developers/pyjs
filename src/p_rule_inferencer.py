import json
from typing import Callable, Dict, List, Optional, Tuple

import d_ast_match
import d_ast_parse
import d_grammar_rules
import d_utils
import p_consts
import p_rule_postprocessor as prpp
import p_tree_log as ptlog
import p_utils
from p_config import Config


logger = p_utils.setup_logger(__name__)


class ContextNotFoundError(RuntimeError): pass
class UnificationError(RuntimeError): pass


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
      logger.debug('The boundaries of source code did not match any AST nodes. '
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

  def _hacky_should_insert_nostr_after_strs_JS(node_type):
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
    Return True if a terminal node is a literal value, False otherwise (other terminals)
    hacky function used in `_ruleInfInternal_ns.astToSExpr`
    previous function name: IS_PARNAME_VALCHILD

    NOTE TODO can be generalized by checking the number of children of a parent.
    If a parent has a single terminal child, then should return True.
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
    if 'escape_sequence' in node_type:
      return True
    if node_type == 'js.template_chars':
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
        ret_arr = ['anno']
        # children
        for i in range(1, len(_node)):
          _child_type = _node[i][0]
          _child_value = _node[i][1]
          ret_arr.append([_child_type, _child_value])
        return ret_arr

      # all remaining node types (NT & T)
      else:
        ret_arr = ['"' + _node_type + '"']
        nostr_tbd = _hacky_should_insert_nostr_after_strs_JS(_node_type)
        # iterate children, skip node_id
        for i in range(2, len(_node)):
          # special treatment for js: nostr
          # inserts nostr before first non-terminal child
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
      logger.error(f'unexpected int node: {_node}')

    # `node` is terminal
    else:
      if _hacky_is_parent_name_valchild(_parent_name):
        return ['val', _node]
      else:
        if is_ignore_str:
          logger.debug(f'str node (ignored): {_node}')
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

  def _is_nonterminal(node_type: str) -> bool:
    return node_type.startswith('"') and node_type.find('.') > 0

  def _common_root_tree_rec(s_exprs: list) -> list:
    '''
    Goes over `s_exprs` in parallel.
    '''
    seg_all_ntypes = list(map(lambda x: x[0], s_exprs))
    seg_0_ntype = seg_all_ntypes[0]

    # base case: node types differ
    if any(nt != seg_0_ntype for nt in seg_all_ntypes):
      raise UnificationError('node types should be identical')

    assert all(seg_0_ntype == nt for nt in seg_all_ntypes), 'all node types should be identical here'

    # base case: common node type is `str`
    if seg_0_ntype == 'str':
      seg_0_str_val = s_exprs[0][1]
      for seg_i in s_exprs:
        if len(seg_i) != 2:
          raise UnificationError('str should have a single child')
        seg_i_str_val = seg_i[1]
        if seg_i_str_val != seg_0_str_val:
          return wildcard_ph_func('_str_', s_exprs, mutable_phs, mutable_tuple_phs)
      return ['str', seg_0_str_val]

    # base case: common node type is `val`
    if seg_0_ntype == 'val':
      seg_0_val_val = s_exprs[0][1]
      for seg_i in s_exprs:
        if len(seg_i) != 2:
          raise UnificationError('val should have a single child')
        seg_i_val_val = seg_i[1]
        if str(seg_i_val_val) != str(seg_0_val_val):
          return wildcard_ph_func('_val_', s_exprs, mutable_phs, mutable_tuple_phs)
      return ['val', seg_0_val_val]

    # base case: common node type is `anno`
    if seg_0_ntype == 'anno':
      ntypes = list(map(lambda x: x[0], s_exprs))
      stypes_0 = list(map(lambda x: x[1][0], s_exprs))
      stypes_1 = list(map(lambda x: x[1][1], s_exprs))
      quotes_0 = list(map(lambda x: x[2][0], s_exprs))
      quotes_1 = list(map(lambda x: x[2][1], s_exprs))
      assert all(nt == 'anno' for nt in ntypes), 'all node types should be anno here'
      assert all(st == '"stype"' for st in stypes_0), 'all stypes 1 should be stype here'
      assert all(qt == '"quote"' for qt in quotes_0), 'all quotes 1 should be quote here'
      seg_0_stype_val = s_exprs[0][1][1]
      if any(seg_0_stype_val != seg_i_stype_val for seg_i_stype_val in stypes_1):
        return UnificationError('string types differ in anno')
      seg_0_quote_val = s_exprs[0][2][1]
      if any(seg_0_quote_val != seg_i_quote_val for seg_i_quote_val in quotes_1):
        return UnificationError('quote types differ in anno')
      return ['anno', ['"stype"', seg_0_stype_val], ['"quote"', seg_0_quote_val]]

    # common node type must be one of: non-terminal, `fragment`, `nostr`
    if not (_is_nonterminal(seg_0_ntype) or seg_0_ntype == 'fragment' or seg_0_ntype == 'nostr'):
      raise UnificationError('common node type should be non-terminal, fragment, or nostr')

    common_root = [seg_0_ntype]
    i = 0
    while True:
      i += 1

      # the expression `(x[i:i+1] or [None])[0]`
      # returns the element if it exists in the list, None otherwise
      # https://stackoverflow.com/questions/2492087/how-to-get-the-nth-element-of-a-python-list-or-a-default-if-not-available
      ith_children = list(map(lambda x: (x[i:i+1] or [None])[0], s_exprs))
      assert all(isinstance(ith_child, list) or ith_child is None for ith_child in ith_children), \
        f'ith_children should be lists or None: {ith_children}'

      # the types of i-th children may differ
      # fix on the i-th child of the first segment
      seg_0_ith_child : Optional[list] = ith_children[0]

      # iteration is over for s_exprs[0]
      if seg_0_ith_child is None:
        # check if iteration is not over for other segments
        if any(map(lambda x: x is not None, ith_children)):
          common_root.append(wildcard_ph_func('*', s_exprs, mutable_phs, mutable_tuple_phs))
        break

      assert all(isinstance(ith_child, list) for ith_child in ith_children), \
        'ith_children should all be lists here'

      # compare i-th child of the first segment
      # to the i-th children of the remaining segments
      seg_0_ith_child_ntype = seg_0_ith_child[0]
      has_ntype_difference = any(seg_0_ith_child_ntype != ith_child[0] for ith_child in ith_children)
      are_all_nts = all(_is_nonterminal(ith_child[0]) for ith_child in ith_children)

      if are_all_nts:
        if has_ntype_difference:
          common_root.append(wildcard_ph_func('.', ith_children, mutable_phs, mutable_tuple_phs))
        else:
          common_root_tree_var = _common_root_tree_rec(ith_children)
          common_root.append(common_root_tree_var)
      else:
        if has_ntype_difference:
          common_root.append(wildcard_ph_func('*', s_exprs, mutable_phs, mutable_tuple_phs))
          break
        else:
          common_root_tree_var = _common_root_tree_rec(ith_children)
          common_root.append(common_root_tree_var)

    return common_root

  fragments = list(map(lambda ast: ['fragment', ast], asts))
  s_exprs = list(map( lambda fragment: ast_to_s_expr(fragment, depth_val=100, is_ignore_str=False), fragments))
  unified = _common_root_tree_rec(s_exprs)
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


def pretty_rule(match, expand, tree_like):
  '''
  Pretty-prints a translation rule to the standard format.
  '''
  rule_type = 'match_expand'
  if tree_like:
    return \
      f'({rule_type}\n\n' \
      f'{d_grammar_rules.pretty_s_expr_tree_like(match)}\n\n' \
      f'{d_grammar_rules.pretty_s_expr_tree_like(expand)}\n\n)'
  return \
    f'({rule_type}\n' \
    f'  {d_grammar_rules.pretty_s_expr(match)}\n' \
    f'  {d_grammar_rules.pretty_s_expr(expand)}\n)'


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


def remove_starting_rules_from_query_results(query_results: list, lang: str) -> None:
  '''
  PRE1 Just a single starting rule per language per grammar.
  NOTE This function is language specific. It should be reimplemented
  if a language has multiple top-level rules, or multi-level top-level rule.
  '''
  # we expect a single snippet per language -> single marks -> single query result
  assert len(query_results) == 1, 'query_results should contain a single element'
  assert lang in p_consts.LANG_DICT, f'lang {lang} is not supported'

  query_result = query_results[0]
  mark, ast_nodes = query_result

  for idx, (node_id, ast, _) in enumerate(ast_nodes[:]):
    # remove a node with id 0 (module for python, program for javascript)
    if node_id == 0:
      if lang == 'py':
        assert ast[0] == 'py.module', 'expected py.module as a starting rule'
      elif lang == 'js':
        assert ast[0] == 'js.program', 'expected js.program as a starting rule'
      del ast_nodes[idx]


# API
def infer_translation_rule(
  translation_pair: list,
  src_lang: str,
  tar_lang: str,
  context: dict,
  is_insert_secret_fn: bool,  # for post-processing
  choose_largest_node: bool,  # choose the largest/smallest node for a given mark
  is_ignore_semicolon: bool,  # update end column of a mark depending on semicolon
  pretty_print_tree_like: bool
) -> str:
  '''
  Given a list of source-target program pairs, infer a translation rule.

  PARAM translation_pair: [{"source": str, "target": str}, ...]
  PARAM srcLang - 'py'
  PARAM tarLang - 'js'
  PARAM context: [{'source_context': [['py.expression_statement]], 'target_context': [['unknown']]}]
  PARAM choose_largest_node: whether or not to choose a largest node that has
        the same boundaries as srcMarks or tarMarks
  PARAM pretty_print_tree_like: return rule pretty-printed as a tree (for visual)
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

  # in case when just a single program pair is provided,
  # remove starting rules for each language (e.g. `py.module` and `js.program`)
  # from each query result.
  if len(src_segments) == 1 and len(tar_segments) == 1:
    remove_starting_rules_from_query_results(src_query_results, src_lang)
    remove_starting_rules_from_query_results(tar_query_results, tar_lang)

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
  # NOTE Creating an instance of `TranslationRule` might raise `prpp.RuleMappingError`
  # It is good to be vocal about errors in translation rules.
  translation_rule = prpp.TranslationRule(src_unified_pattern, tar_unified_pattern)
  if Config.generator == 'lightweight':
    src_unified_pattern, tar_unified_pattern = translation_rule.convert_ident_captures_to_dot_phs()

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
        logger.debug(err)
        break

  # 11
  return pretty_rule(src_unified_pattern, tar_unified_pattern, pretty_print_tree_like)


def infer_translation_rule_wrapper(
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
  p_utils.log_json_time(f'args-infer_translation_rule_wrapper.json', locals())

  # logger.debug(f'Translation pair:\n{json.dumps(translation_pair, indent=2)}')
  # logger.debug(f'Context:\n{json.dumps(context, indent=2)}')

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
    f'Rule hash value: {d_utils.string_sha256(translation_rule)}')
  p_utils.log_file_time(f'learned-translation-rule.snart', translation_rule)

  return translation_rule


def infer_translation_rules(
  template_dict: dict,
  translation_pairs: List[Tuple[Dict[str, str], Dict[str, str]]],
  lprule_inf_log: Optional[ptlog.PRuleInfLog] = None
) -> List[str]:
  '''
  Infer translation rules for multiple translation pairs.
  RAISE None. All exceptions are handled.
  '''
  p_utils.log_json_time(f'args-infer_translation_rules.json', locals())
  lprule_inf_log = lprule_inf_log or ptlog.PRuleInfLog()
  lprule_inf_log.stms = p_utils.current_time_msec()

  contexts : List[Dict[str, List[List[str]]]] = template_dict['contexts']
  src_lang = template_dict['src_lang']
  tar_lang = template_dict['tar_lang']
  is_insert_secret_fn = template_dict['is_insert_secret_fn']

  logger.debug(
    f'rule-inf: attempting to infer translation rules from '
    f'{len(translation_pairs)} translation pairs and {len(contexts)} contexts')

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
              logger.debug(
                f'Added newly inferred translation rule to the list.\n'
                f'The number of translation rules so far is {len(trules_list)}')

              ltrule = ptlog.TRule.from_str(translation_rule)
              lrule_inf_comb.translation_rule = ltrule
              lrule_inf_comb.num_inferred_rules += 1
              lcontext.num_inferred_rules += 1
              ltrans_pair.num_inferred_rules += 1
              lprule_inf_log.num_inferred_rules += 1

            else:
              msg = 'This rule already exists in the list. Skipping.'
              logger.debug(msg)
              lrule_inf_comb.reason = msg

          except Exception as exc:
            msg = f'Error during rule inference. Skip this one: {exc}'
            logger.debug(msg)
            lrule_inf_comb.reason = msg

          logger.debug(f'the number of translation rules so far is --> {len(trules_list)}')

  lprule_inf_log.success = True
  lprule_inf_log.etms = p_utils.current_time_msec()
  if len(trules_list) == 0:
    logger.warning('No translation rules were inferred from the given translation pairs and contexts.')
  logger.debug(f'rule-inf: inferred {len(trules_list)} translation rules in total')
  return trules_list


# TEST HARNESS FUNCTIONS
def _test_infer_translation_rule_wrapper():
  '''
  def infer_translation_rule_wrapper(
    translation_pair: dict,
    src_lang: str,
    tar_lang: str,
    context: dict,
    is_insert_secret_fn: bool,
    choose_largest_node: bool,
    is_ignore_semicolon: bool
  ) -> str:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_infer_translation_rule_wrapper_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  translation_pair = args_dict['translation_pair']
  src_lang = args_dict['src_lang']
  tar_lang = args_dict['tar_lang']
  context = args_dict['context']
  is_insert_secret_fn = args_dict['is_insert_secret_fn']
  choose_largest_node = args_dict['choose_largest_node']
  is_ignore_semicolon = args_dict['is_ignore_semicolon']

  trule = infer_translation_rule_wrapper(
    translation_pair,
    src_lang,
    tar_lang,
    context,
    is_insert_secret_fn,
    choose_largest_node,
    is_ignore_semicolon
  )

  print(trule)


def _usage_infer_translation_rule():
  '''
  def infer_translation_rule(
    translation_pair: list,
    src_lang: str,
    tar_lang: str,
    context: dict,
    is_insert_secret_fn: bool,  # for post-processing
    choose_largest_node: bool,  # choose the largest/smallest node for a given mark
    is_ignore_semicolon: bool,  # update end column of a mark depending on semicolon
    pretty_print_tree_like: bool
  ):
  '''
  translation_pair = [
    {
      "source": "a = 'hi'",
      "target": "a = 'hi';"
    },
    {
      "source": "a = 'hello'",
      "target": "a = 'hello';"
    }
  ]

  src_lang = 'py'
  tar_lang = 'js'
  context = {
    'source_context': [['py.expression_statement']],
    'target_context': [['unknown']]
  }
  is_insert_secret_fn = False
  choose_largest_node = True
  is_ignore_semicolon = False
  pretty_print_tree_like = True

  trule = infer_translation_rule(
    translation_pair,
    src_lang,
    tar_lang,
    context,
    is_insert_secret_fn,
    choose_largest_node,
    is_ignore_semicolon,
    pretty_print_tree_like
  )

  print(trule)


if __name__ == '__main__':
  # _test_infer_translation_rule_wrapper()
  _usage_infer_translation_rule()
