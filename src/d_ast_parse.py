import json
from typing import Dict, Tuple, Union

import d_consts
import p_consts
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


def get_nid_ntype_map(ast: list) -> Dict[int, str]:
  '''
  Get mapping of node IDs to their types of trees obtained
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
