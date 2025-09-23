import json
from typing import Dict, Iterable, Iterator, List, Optional, Tuple, Union

import d_consts
import p_consts
import p_data_structures as pds
from tree_sitter import Language, Node, Parser, Tree


def _anno_func_py_string(ann, context: str):
  startpos = ann[0]
  endpos = ann[1]
  subs = context[startpos:endpos]
  stype = ""
  if subs.startswith("f"): stype = "f"
  elif subs.startswith("r"): stype = "r"
  elif subs.startswith("b"): stype = "b"
  else:
    if not (subs.startswith('"') or subs.startswith("'")):
      print("_anno_func_py_string UNEXPECTED:", subs)
      assert "parse_error" == 0 or (subs.startswith('"') or subs.startswith("'"))
  quote = None
  if subs.endswith('\"\"\"'): quote = '\"\"\"'
  elif subs.endswith("\'\'\'"): quote = "\'\'\'"
  elif subs.endswith('\"'): quote = '\"'
  elif subs.endswith("\'"): quote = "\'"
  else: assert 0 == "py.string does not endswith ' or \""
  return ["anno", ['"stype"', f'"{stype}"'], ['"quote"', f'{json.dumps(quote)}']]


_ANNO_FUNC_DICT = {
  "py.string": _anno_func_py_string
}


def parse_text_dbg(text: str, lang: str, keep_text=False) -> Tuple[list, dict]:
  '''
  text: text of source code to parse
  lang: 'py', 'js', etc.
  keep_text: save TreeSitter generated .text attribute
  '''
  parser = p_consts.PARSER_DICT[lang]
  tree = parser.parse(bytes(text, "utf8"))

  current_node_idx = 0
  ann_info = {}

  extra_root = []
  ast_scope_stack = [extra_root]

  # does nothing at the moment
  def _fn_before(node: Node):
    if node.is_named == False: return
    if d_consts.DEBUG_VERBOSE > 0: print("(", end="")

  # does nothing at the moment
  def _fn_before_child(child: Node):
    if d_consts.DEBUG_VERBOSE > 0: print(" ", end="")

  def _fn_after(node: Node):
    if node.is_named == False: return
    ast_scope_stack.pop()
    if d_consts.DEBUG_VERBOSE > 0: print(")", end="")

  def _fn_visit(node: Node):
    def __add_id():
      nonlocal current_node_idx
      if d_consts.DEBUG_VERBOSE > 0: print(f" {current_node_idx}", end="")
      ann_info[current_node_idx] = [node.start_byte, node.end_byte, node.start_point, node.end_point]
      current_node_idx += 1
      return current_node_idx - 1

    if node.is_named:
      sub_ast_list = []
      ast_scope_stack[-1].append(sub_ast_list)
      ast_scope_stack.append(sub_ast_list)

      node_type = f'{lang}.{node.type}'  # pirel-style node type
      elem = [node_type, node.text.decode('utf-8')] if keep_text else node_type

      if d_consts.DEBUG_VERBOSE > 0: print(elem, end="")
      sub_ast_list.append(elem)

      new_id = __add_id()
      sub_ast_list.append(new_id)

      if node_type in _ANNO_FUNC_DICT:
        anno_func = _ANNO_FUNC_DICT[node_type]
        anno = anno_func(ann_info[new_id], text)
        if anno is not None:
          sub_ast_list.append(anno)

      if len(node.children) == 0:
        # named (typed), but no children. Should be an external symbol
        elem = json.dumps(text[node.start_byte:node.end_byte])
        if d_consts.DEBUG_VERBOSE > 0: print("", elem, end="")
        sub_ast_list.append(elem)
    else:
      # not named
      elem = json.dumps(node.type)
      if d_consts.DEBUG_VERBOSE > 0: print(elem, end="")
      ast_scope_stack[-1].append(elem)

  def _traverse(tree: Tree, fn_before, fn_visit, fn_before_child, fn_after):
    def __traverse_rec(node):
      fn_before(node)
      fn_visit(node)
      for child in node.children:
        fn_before_child(child)
        __traverse_rec(child)
      fn_after(node)
    __traverse_rec(tree.root_node)

  _traverse(tree, _fn_before, _fn_visit, _fn_before_child, _fn_after)

  assert len(ast_scope_stack) == 1
  assert len(extra_root) == 1
  return extra_root[0], ann_info


# AST AND RANGE CURSOR RELATED FUNCTIONS
def is_elem_non_terminal(elem) -> bool:
  '''
  Return True if the element is a non-terminal.
  '''
  if not isinstance(elem, list):
    return False
  if elem[0] == "anno":
    return False
  assert elem[0] != "fragment"
  assert isinstance(elem[1], int)
  return True


def get_nid_ntype_map(ast: list) -> Dict[int, str]:
  '''
  Get mapping of node IDs to their node types obtained
  from parse_text_dbg.
  '''
  nid_ntype_map = {}
  def _traverse(node) -> None:
    nonlocal nid_ntype_map
    # base case: terminal node
    if not isinstance(node, list):
      return
    assert len(node) >= 2, 'non-terminals are at least length 2'
    # if the second element is an int, it's an ID
    # unlike e.g. string nodes (check parsed ASTs to confirm)
    if isinstance(node[1], int):
      nid_ntype_map[node[1]] = node[0].split('.')[1]  # strip 'py.' prefix
    for child in node[2:]:
      _traverse(child)
  _traverse(ast)
  return nid_ntype_map


def parse_text_to_range_cursor(
  code: str,
  lang: str
) -> Tuple[Tuple[list, int, int], dict]:
  '''
  A range cursor is another way to represent ASTs in DuoGlot world.
  A structure of a range cursor is as follows:
  (AST of the parent node, start_idx, end_idx)
  start_idx and end_idx specify a range of nodes under a given
  parent node.
  NOTE Naturally, when using this function, it will not be able
  to reference the root node of the parsed tree, because range
  cursors require a parent node to be present. So this function
  returns references to the children of the root node.
  '''
  ast, ann = parse_text_dbg(code, lang)
  num_children = len(ast) - 2
  assert num_children >= 1, 'expected at least one child under the root node'
  range_cursor = (ast, 2, 2 + num_children)
  return range_cursor, ann


def get_range_cursor(ast: list, nid: int) -> Tuple[list, int, int]:
  '''
  Given an DuoGlot-style AST and a node id, return the range cursor to the node.
  Range cursor is a tuple of (list, start_idx, end_idx).
  RAISE ValueError if the node id is not found.
  '''
  def __is_child_that_we_need(child, nid: int) -> bool:
    # base case: child is terminal node
    if not isinstance(child, list):
      return False
    assert len(child) >= 2, 'non-terminals are at least length 2'
    # if the second element is an int, it's an ID
    child_nid = child[1]
    if not isinstance(child_nid, int):
      return False
    return child_nid == nid

  def __traverse(node, nid: int) -> Optional[Tuple[list, int, int]]:
    # base case: terminal node
    if not isinstance(node, list):
      return None
    assert len(node) >= 2, 'non-terminals are at least length 2'
    for idx, child in enumerate(node[2:], start=2):
      if __is_child_that_we_need(child, nid):
        return (node, idx, idx + 1)
      result = __traverse(child, nid)
      if result is not None:
        return result
    return None

  result = __traverse(ast, nid)
  if result is None:
    raise ValueError(f'Node id {nid} not found')
  return result


def deduplicate_range_cursors(
  range_cursors: list
) -> list:
  '''
  Deduplicate range cursors.
  '''
  seen = set()
  deduped = []
  for rc in range_cursors:
    rc_id = (id(rc[0]), rc[1], rc[2])
    if rc_id not in seen:
      deduped.append(rc)
      seen.add(rc_id)
  return deduped


def get_nt_children_as_range_cursors(nt_node: list) -> list:
  '''
  Given a duoglot-style AST node, return a list of non-terminal
  children as range cursors.
  POST: range cursors specify exactly one AST node.
  '''
  assert is_elem_non_terminal(nt_node), 'expected non-terminal node'
  result = []
  for i in range(2, len(nt_node)):
    if is_elem_non_terminal(nt_node[i]):
      result.append((nt_node, i, i + 1))
  return result


def range_cursor_seq_descending_from_ast(ast: list) -> list:
  '''
  Given a duoglot-style AST, generate a sequence of range cursors
  in pre-order traversal.
  POST: Sequence does not include the AST itself, only the subtrees.
  '''
  assert is_elem_non_terminal(ast), 'expected non-terminal node'
  result = []
  def _rec_pre_order(node: list):
    nonlocal result
    if not is_elem_non_terminal(node):
      return
    for child_range_cursor in get_nt_children_as_range_cursors(node):
      result.append(child_range_cursor)
      child_idx = child_range_cursor[1]
      child_ast = child_range_cursor[0][child_idx]
      _rec_pre_order(child_ast)
  _rec_pre_order(ast)
  return result


def get_all_range_cursors_under(
  range_cursor: Tuple[list, int, int],
) -> list:
  '''
  Need to add itself, because range_cursor_seq_descending_from_ast()
  will include only the subtrees. all_range_cursors are all possible
  range cursors under the range_cursor.
  '''
  choicable_ast = range_cursor_to_ast_node(range_cursor)
  all_range_cursors = [range_cursor]  # include itself
  choicable_range_cursor_children = range_cursor_seq_descending_from_ast(choicable_ast)
  all_range_cursors.extend(choicable_range_cursor_children)
  return all_range_cursors


def range_cursor_is_empty(range_cursor: tuple) -> bool:
  '''
  Return True if the range cursor is empty.
  An empty range cursor does not include any AST nodes.
  '''
  assert isinstance(range_cursor, tuple) and len(range_cursor) == 3
  assert isinstance(range_cursor[0], list)
  assert isinstance(range_cursor[1], int)
  assert isinstance(range_cursor[2], int)
  return range_cursor[1] == range_cursor[2]


def range_cursors_remove_empty(
  range_cursors: Iterable[tuple[list, int, int]],
) -> List[Tuple[list, int, int]]:
  '''
  Remove empty range cursors from the list.
  '''
  return [rc for rc in range_cursors if not range_cursor_is_empty(rc)]


def range_cursor_split(
  range_cursor: Tuple[list, int, int],
) -> Iterator[tuple[list, int, int]]:
  '''
  Split a range cursor into multiple range cursors, each specifying
  exactly one non-terminal AST node.
  '''
  assert isinstance(range_cursor, tuple) and len(range_cursor) == 3
  assert isinstance(range_cursor[0], list)
  assert isinstance(range_cursor[1], int)
  assert isinstance(range_cursor[2], int)
  parent_ast = range_cursor[0]
  start_idx = range_cursor[1]
  end_idx = range_cursor[2]

  # 2 is the index of the first child of a non-terminal node
  assert start_idx >= 2, 'range cursor start index must be >= 2'
  # start_idx == end_idx denotes an empty range cursor
  assert start_idx <= end_idx, 'range cursor start index must be <= end index'
  # end_idx > 2 means at least one child node is included
  assert end_idx > 2, 'range cursor end index must be > 2'
  # end_idx == len(parent_ast) means the range cursor includes the last child
  assert end_idx <= len(parent_ast), 'range cursor end index out of bounds'

  for idx in range(start_idx, end_idx):
    rc = (parent_ast, idx, idx + 1)
    ast = range_cursor_to_ast_node(rc)
    if is_elem_non_terminal(ast):
      yield rc


def range_cursor_to_ast_node(range_cursor: tuple) -> list:
  '''
  Convert a range cursor to an AST node.
  range_cursor: Tuple[ List[src_ast] , int , int ]
  PRE: range_cursor specifies exactly one AST node
  '''
  assert isinstance(range_cursor, tuple) and len(range_cursor) == 3
  assert isinstance(range_cursor[0], list)
  assert isinstance(range_cursor[1], int)
  assert isinstance(range_cursor[2], int)
  assert range_cursor[1] + 1 == range_cursor[2], 'range cursors specify exactly one AST node'

  # Convert the range cursor to an AST node
  parent_ast = range_cursor[0]
  child_ast_idx = range_cursor[1]
  child_ast = parent_ast[child_ast_idx]
  return child_ast


def range_cursor_to_choice_identifier(range_cursor: tuple) -> tuple:
  '''
  Choice identifier is a tuple of (node_id, start_idx, end_idx).
  It is used for identifying the node in the AST for which a rule
  choice is made. It is used in choices_list.
  '''
  node, start_idx, end_idx = range_cursor
  assert is_elem_non_terminal(node), 'sanity check'
  node_id = node[1]
  assert isinstance(node_id, int), 'sanity check'
  return (node_id, start_idx, end_idx)


def range_cursor_pretty_print(range_cursor: tuple, ann: dict, src_code: str) -> str:
  '''
  Pretty print the AST node specified by the range cursor.
  PARAM range_cursor: Tuple[ List[src_ast] , int , int ]
  PARAM ann: annotation dict from parse_text_dbg
  PARAM src_code: original source code
  '''
  ast = range_cursor_to_ast_node(range_cursor)
  if ast[0] == 'py.string_content':
    assert is_elem_non_terminal(ast), 'expected non-terminal node'
    assert len(ast) == 3, 'expected py.string_content to have 3 elements'
    assert isinstance(ast[2], str), 'expected py.string_content to have a string child'
    return ast[2]
  return ast_pretty_print(ast, ann, src_code)


def range_cursor_encode(range_cursor: tuple, ann: dict, src_code: str) -> str:
  '''
  Encode the AST node specified by the range cursor.
  PARAM range_cursor: Tuple[ List[src_ast] , int , int ]
  PARAM ann: annotation dict from parse_text_dbg
  PARAM src_code: original source code
  '''
  unparsed = range_cursor_pretty_print(range_cursor, ann, src_code)
  ast = range_cursor_to_ast_node(range_cursor)
  ast_encoded = ast_encode(ast)
  encoded = f'{unparsed}--{ast_encoded}'
  return encoded


def ast_pretty_print(ast: list, ann: dict, src_code: str) -> str:
  '''
  Pretty print the AST.
  PARAM ast: duoglot-style AST node
  PARAM ann: annotation dict from parse_text_dbg
  PARAM src_code: original source code
  '''
  assert isinstance(ast, list), 'expected list'
  assert len(ast) >= 2, 'expected at least 2 elements in ast'
  nid = ast[1]
  assert isinstance(nid, int), 'expected nid to be int'
  assert nid in ann, f'nid {nid} not in annotation dict'
  start_byte, end_byte, _, _ = ann[nid]
  return src_code[start_byte:end_byte].strip()


def node_id_pretty_print(src_code: str, src_lang: str, node_id: int) -> str:
  '''
  Pretty print the AST node specified by the node id.
  PARAM src_code: original source code
  PARAM node_id: node id
  '''
  tree = pds.PirelTree.from_code_str(src_code, src_lang)
  tree._fix_indentation()
  node = tree.get_node_with_id(node_id)
  assert node is not None, f'node id {node_id} not found in the AST'
  return node.get_text()


def are_nodes_equal(
  node1: Union[list, str],
  node2: Union[list, str],
  ignore_nids: bool = True
) -> bool:
  '''
  Recursively check if two AST nodes are equal.
  '''
  assert isinstance(node1, (list, str)), 'node1 is not list or str'
  assert isinstance(node2, (list, str)), 'node2 is not list or str'

  # both are terminals
  if isinstance(node1, str) and isinstance(node2, str):
    return node1 == node2

  # exactly one is non-terminal or terminal
  if type(node1) != type(node2):
    return False

  # both are non-terminals
  assert isinstance(node1, list), 'sanity check'
  assert isinstance(node2, list), 'sanity check'

  ntype1, ntype2 = node1[0], node2[0]
  assert isinstance(ntype1, str), 'sanity check'
  assert isinstance(ntype2, str), 'sanity check'

  # check if node types are equal
  if ntype1 != ntype2:
    return False

  # special case for string annotations
  if ntype1 == 'anno':
    assert len(node1) == 3, 'sanity check: anno has 3 elements'
    assert len(node2) == 3, 'sanity check: anno has 3 elements'
    if node1[1][1] != node2[1][1]:  # stype
      return False
    if node1[2][1] != node2[2][1]:  # quote
      return False
    return True

  # non-terminals have at least 3 elements
  assert len(node1) > 2, 'sanity check: ntype, nid, children'
  assert len(node2) > 2, 'sanity check: ntype, nid, children'

  nid1, nid2 = node1[1], node2[1]
  assert isinstance(nid1, int), 'sanity check'
  assert isinstance(nid2, int), 'sanity check'

  # check if node IDs are equal
  if not ignore_nids and nid1 != nid2:
    return False

  children1, children2 = node1[2:], node2[2:]
  if len(children1) != len(children2):
    return False

  for child1, child2 in zip(children1, children2):
    child_res = are_nodes_equal(child1, child2)
    if not child_res:
      return False
  return True


def ast_encode(
  ast: list,
  ignore_node_ids: bool = True,
  ignore_anno: bool = True
) -> str:
  '''
  Encode the AST as a string.
  PARAM ast: duoglot-style AST node
  '''
  def _pre_order(node: Union[list, str]) -> str:
    nonlocal ignore_anno
    # base case: terminal node
    if isinstance(node, str):
      return node
    # base case: anno nodes
    if node[0] == 'anno' and ignore_anno:
      return ''
    assert is_elem_non_terminal(node), 'expected non-terminal node'
    res = '[' + node[0]  # node type
    if not ignore_node_ids:
      res += f'_{node[1]}'  # node id
    for child in node[2:]:
      child_str = _pre_order(child)
      if child_str != '':
        res += f' {child_str}'
    return res + ']'

  assert ignore_anno, 'anno is not supported at the moment'
  return _pre_order(ast).strip()


def ast_to_dotgraph(
  text: str,
  lang: str,
  short_non_terminals: bool = False,
  short_non_terminals_len: int = 5,
  include_node_ids: bool = False,
  show_terminals: bool = True,
) -> None:
  '''
  Easy AST visualizer with https://dreampuf.github.io/GraphvizOnline
  PARAM short_non_terminals - shorten non-terminal labels
  PARAM short_non_terminals_len - number of characters to shorten to
  '''
  def _parse_node(astnode: list):
    '''PRE: astnode is non-terminal'''
    assert isinstance(astnode, list)
    node_type, node_id, children = astnode[0], astnode[1], astnode[2:]
    return node_type, node_id, children

  def _isnt(astnode: Union[list, str]):
    return isinstance(astnode, list)
  def _ist(astnode: Union[list, str]):
    return isinstance(astnode, str)

  def _nt_name(node_type: str, node_id: int) -> str:
    ts_node_type = node_type.split(".")[1]
    return f'{ts_node_type}{node_id}'
  def _nt_label(node_type: str, node_id: int) -> str:
    nonlocal short_non_terminals
    nonlocal short_non_terminals_len
    nonlocal include_node_ids
    ts_node_type = node_type.split(".")[1]
    if short_non_terminals:
      chunks = ts_node_type.split('_')
      chunks = [chunk[:short_non_terminals_len] for chunk in chunks]
      ts_node_type = '_'.join(chunks)
    if include_node_ids:
      ts_node_type = f'{node_id}-{ts_node_type}'
    return ts_node_type

  def _pre_order(node: list, depth=0):
    ''''''
    assert _isnt(node)
    nonlocal ntnldict, tnldict, edge_template
    nonlocal show_terminals

    ntype, nid, children = _parse_node(node)

    # skip `anno` node for py.string
    if ntype == 'py.string':
      children = ['`', children[2], '`']

    grnname = _nt_name(ntype, nid)
    grnlabel = _nt_label(ntype, nid)
    ntnldict[grnname] = grnlabel

    for chidx, child in enumerate(children):
      if _isnt(child):
        chtype, chid, chchildren = _parse_node(child)
        chgrnname = _nt_name(chtype, chid)
        chgrnlabel = _nt_label(chtype, chid)
        ntnldict[chgrnname] = chgrnlabel
        print(depth * indentsize * ' ', edge_template.format(grnname, chgrnname), sep='')
        _pre_order(child, depth + 1)
      elif _ist(child):
        chgrnname = f'term{nid}_{chidx}'
        chgrnlabel = child.strip('"')
        tnldict[chgrnname] = chgrnlabel
        if show_terminals:
          print(depth * indentsize * ' ', edge_template.format(grnname, chgrnname), sep='')
      else:
        raise RuntimeError('AST format error')

  edge_template = '{} -> {};'
  nt_template = '{} [label="{}"]'
  # nt_template = '{} [label="{}", style=filled, fillcolor={}]'
  t_template = '{} [label="{}", shape=square, color=red]'
  indentsize = 2

  ntnldict = {}
  tnldict = {}
  ast, ann = parse_text_dbg(text, lang)

  _pre_order(ast)
  for k, v in ntnldict.items():
    print(nt_template.format(k, v))
  if show_terminals:
    for k, v in tnldict.items():
      print(t_template.format(k, v))
