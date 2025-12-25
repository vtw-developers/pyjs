'''
A module for post-processing match patterns in DuoGlot.
Match pattern is an s-expression that matches either a source program, or a target program.
Match pattern is a return value of frontend/pirel/rule_inference.js::ruleInfAPI_ns.inferTranslationRule()
Match pattern is directly pretty-printed into a translation rule.

In simple words, this module is for manipulating translation rules.
'''
# Class hierarchy:
#                                       AbstractNode
#                                         /--  --\
#                                     /---        ---\
#                                 ---                ---
#                       NonTerminalNode             TerminalNode
#                                                   /------\
#                                           /-------        -----\
#                                       ----                      ---
#                               PlainTerminalNode                  PhNode
#                                                             ------------\
#                                             ---------------/             ------\
#                                   --------/                                    ----
#                             SourcePhNode                                       TargetPhNode
#                           --------\                                           --- |----\
#               -----------/   -/    ---\                                 -----/    \     -------\
#         ------/              /          ---                          ---/           |            -----
# SourceValPhNode   SourceStrPhNode   SourceDotStarPhNode    TargetValPhNode   TargetStrPhNode   TargetDotStarPhNode

# TODO add support for (nostr) nodes


import json
import re
from typing import Callable, List, Optional, Tuple, Union

import p_rule_inferencer
import p_utils


logger = p_utils.setup_logger(__name__)


class RuleMappingError(RuntimeError): pass
class SecretNodeNotFoundError(RuntimeError): pass


class AbstractNode:
  '''
  Abstract Node class for pattern tree node types.
  '''

  def __init__(self, node_type: str, parent: 'AbstractNode') -> None:
    '''
    node_type: e.g. 'py.identifier'
    parent: parent AbstractNode. None if self is root.
    children: List[AbstractNode].
    '''
    self.node_type : str = node_type
    self.parent : Union[AbstractNode, None] = parent
    self.children : List[AbstractNode] = []

  def get_type(self) -> str:
    return self.node_type

  def set_type(self, new_type: str) -> None:
    self.node_type = new_type

  def get_parent(self) -> Union['AbstractNode', None]:
    return self.parent

  def set_parent(self, new_parent: 'AbstractNode') -> None:
    self.parent = new_parent

  def get_children(self) -> List['AbstractNode']:
    return self.children

  def is_root_node(self) -> bool:
    return self.parent is None

  def has_parent(self) -> bool:
    return self.parent is not None

  def num_children(self) -> int:
    return len(self.children)

  def get_siblings_include_self(self) -> List['AbstractNode']:
    if not self.has_parent():
      return [self]
    return self.parent.children

  def get_siblings_to_the_left(self) -> List['AbstractNode']:
    siblings = self.get_siblings_include_self()
    self_idx = siblings.index(self)
    return siblings[:self_idx]

  def get_child_by_path(self, rel_path: List[int]) -> Union['AbstractNode', None]:
    '''
    Return a child node of self by a relative path
    PRE: rel_path exists in self
    '''
    try:
      child_node = self
      for child_idx in rel_path:
        child_node = child_node.get_children()[child_idx]
      return child_node
    except IndexError:
      return None

  def get_src_dotstar_ph_nodes_under(self) -> List['SourceDotStarPhNode']:
    ''''''
    nodes = []
    def _pre_order(node: 'AbstractNode'):
      nonlocal nodes
      if isinstance(node, SourceDotStarPhNode):
        nodes.append(node)
      for child in node.get_children():
        _pre_order(child)
    _pre_order(self)
    return nodes

  def get_nt_children(self) -> List['NonTerminalNode']:
    def _is_real_nt(node: AbstractNode) -> bool:
      if not isinstance(node, NonTerminalNode):
        return False
      if node.node_type[0] != '"':
        return False
      if node.node_type[-1] != '"':
        return False
      if '.' not in node.node_type:
        return False
      return True
    nt_children = [node for node in self.children if _is_real_nt(node)]
    return nt_children

  def __str__(self) -> str:
    return f'class={type(self).__name__}\n' + \
    f'type={self.node_type}\n' + \
    f'num_children={len(self.children)}'

  def debug_str(self) -> str:
    '''return str repr of AST rooted at this node in pre-order traversal'''
    def _pre_order(node: 'AbstractNode'):
      result = node.get_type()
      for child in node.get_children():
        result += ' ' + _pre_order(child)
      return result
    return _pre_order(self)

  # abstract methods
  def add_child(self, child: 'AbstractNode') -> None:
    raise NotImplementedError

  def add_child_at(self, child: 'AbstractNode', idx: int) -> None:
    raise NotImplementedError

  def set_children(self, children: Union[str, list]) -> None:
    raise NotImplementedError

  def is_terminal(self) -> bool:
    raise NotImplementedError

  def is_nonterminal(self) -> bool:
    raise NotImplementedError

  def get_index_as_child(self) -> int:
    '''get index of `self` in `self.parent.children`'''
    raise NotImplementedError

  def get_num_siblings(self) -> int:
    raise NotImplementedError

  def get_siblings_to_the_right(self) -> List['AbstractNode']:
    raise NotImplementedError

  def has_single_terminal_child(self) -> bool:
    raise NotImplementedError

  def str_node_has_single_terminal_child(self) -> bool:
    raise NotImplementedError


class NonTerminalNode(AbstractNode):
  '''
  Non-terminal node: works for any tree
  '''
  def __init__(self, node_type: str, parent: AbstractNode) -> None:
    super().__init__(node_type, parent)

  def __repr__(self) -> str:
    return f'NT({self.node_type})'

  # overridden methods
  def add_child(self, child: AbstractNode):
    self.children.append(child)

  def add_child_at(self, child: 'AbstractNode', idx: int) -> None:
    assert 0 <= idx <= len(self.children)
    self.children.insert(idx, child)

  def set_children(self, children: Union[str, list]) -> None:
    self.children = children

  def is_terminal(self) -> bool:
    return False

  def is_nonterminal(self) -> bool:
    return True

  def get_index_as_child(self) -> int:
    if self.is_root_node():
      return 0
    return self.get_parent().get_children().index(self)

  def get_num_siblings(self) -> int:
    if self.is_root_node():
      return 0
    return len(self.get_parent().get_children()) - 1

  def get_siblings_to_the_right(self) -> List['AbstractNode']:
    if self.is_root_node():
      return []
    return self.get_parent().get_children()[self.get_index_as_child()+1:]

  def has_single_terminal_child(self) -> bool:
    if self.num_children() == 1 and isinstance(self.children[0], TerminalNode):
      return True
    return False

  def str_node_has_single_terminal_child(self) -> bool:
    '''
    Terminal nodes for syntax elements such as `:`, `,`, `(`
    are represented under `str` node type in translation rule patterns.
    This method is for checking if a node is such.
    '''
    if self.has_single_terminal_child() and self.get_type() == 'str':
      return True
    return False


class TerminalNode(AbstractNode):
  '''
  Terminal node for pattern on source side.
  '''
  # overridden methods
  def add_child(self, child: AbstractNode) -> None:
    raise AttributeError('Cannot add a child to a terminal node.')

  def add_child_at(self, child: 'AbstractNode', idx: int) -> None:
    raise AttributeError('Cannot add a child to a terminal node.')

  def set_children(self, children: Union[str, list]) -> None:
    raise AttributeError('Cannot add a child to a terminal node.')

  def is_terminal(self) -> bool:
    return True

  def is_nonterminal(self) -> bool:
    return False

  def get_index_as_child(self) -> int:
    return 0

  def get_num_siblings(self) -> int:
    return 0

  def get_siblings_to_the_right(self) -> List['AbstractNode']:
    return []

  def has_single_terminal_child(self) -> bool:
    return False


class PlainTerminalNode(TerminalNode):
  '''
  Terminal node non-PH nodes.
  '''
  def __init__(self, node_type: str, parent: AbstractNode) -> None:
    super().__init__(node_type, parent)

  def __repr__(self):
    return f'T({self.node_type})'


class PhNode(TerminalNode):
  '''
  Terminal node for PH nodes.
  '''
  def __init__(self, node_type: str, parent: AbstractNode, phid: int) -> None:
    super().__init__(node_type, parent)
    self.phid = phid

  def get_phid(self) -> int:
    return self.phid

  def set_phid(self, phid: int) -> None:
    self.phid = phid


class SourcePhNode(PhNode):
  pass


class TargetPhNode(PhNode):
  pass


class SourceValPhNode(SourcePhNode):
  def __str__(self) -> str:
    return f'Source _val_ PH node id={self.get_phid()}'

  def __repr__(self):
    return f'SrcValPH({self.node_type} #{self.phid})'


class SourceStrPhNode(SourcePhNode):
  def __str__(self) -> str:
    return f'Source _str_ PH node id={self.get_phid()}'

  def __repr__(self):
    return f'SrcStrPH({self.node_type} #{self.phid})'


class SourceDotStarPhNode(SourcePhNode):
  def __str__(self) -> str:
    return f'Source .|* PH node id={self.get_phid()}'

  def __repr__(self):
    return f'SrcDotStarPH({self.node_type} #{self.phid})'


class TargetValPhNode(TargetPhNode):
  def __str__(self) -> str:
    return f'Target _val<d>_ PH node id={self.get_phid()}'

  def __repr__(self):
    return f'TarValPH({self.node_type} #{self.phid})'


class TargetStrPhNode(TargetPhNode):
  def __str__(self) -> str:
    return f'Target _str<d>_ PH node id={self.get_phid()}'

  def __repr__(self):
    return f'TarStrPH({self.node_type} #{self.phid})'


class TargetDotStarPhNode(TargetPhNode):
  def __str__(self) -> str:
    return f'Target .<d>|*<d> PH node id={self.get_phid()}'

  def __repr__(self):
    return f'TarDotStarPH({self.node_type} #{self.phid})'


class TranslationRule:
  '''
  A mutable tree representation of translation rule patterns.
  '''
  def __init__(self, src_pattern_s_expr, tar_pattern_s_expr) -> None:
    '''
    src_pattern_s_expr: DuoGlot-style pattern s-expression (srcUnifiedPattern in rule_inference.js)
    tar_pattern_s_expr: DuoGlot-style pattern s-expression (tarUnifiedPattern in rule_inference.js)

    TODO update this grammar
    *pattern_s_expr grammar:
      pattern: [node]
      node: [node_type_nt, children] | [node_type_t, terminal] | placeholder
      node_type_nt: "str"
      node_type_t: str
      placeholder: "*" | "."
      children: Sequence[node]
      terminal: "str"

    TERMS
    S - set of placeholders in source pattern
    T - set of placeholders in target pattern
    STmap_val, STmap_str, STmap_dotstar - mapping of placeholders from S to T (1 -> 0,1,2,...)
    TSmap_val, TSmap_str, TSmap_dotstar - mapping of placeholders from T to S (1 -> 1)
    '''

    # re objects used in parsing the input
    self._re_tar_dot_star_ph = re.compile(r'^"([\.\*])(\d+)"$')
    self._re_src_dot_star_ph = re.compile(r'^"([\.\*])"$')
    self._re_val_ph = re.compile(r'^"_val(\d+)_"$')
    self._re_str_ph = re.compile(r'^"_str(\d+)_"$')

    # src root node
    src_root_node_type : str = src_pattern_s_expr[0]
    self.src_root_node = NonTerminalNode(src_root_node_type, None)
    self.src_dot_star_next_phid = 1
    self.src_val_next_phid = 1
    self.src_str_next_phid = 1
    # recurse src children
    src_root_node_children = src_pattern_s_expr[1:]
    for child_s_expr in src_root_node_children:
      self._rec_construct_at(self.src_root_node, child_s_expr)

    # tar root node
    tar_root_node_type : str = tar_pattern_s_expr[0]
    self.tar_root_node = NonTerminalNode(tar_root_node_type, None)
    # recurse tar children
    tar_root_node_children = tar_pattern_s_expr[1:]
    for child_s_expr in tar_root_node_children:
      self._rec_construct_at(self.tar_root_node, child_s_expr)

    # set of placeholders S and T
    self._update_placeholder_sets()

    # mappings
    self.STmap_val, self.TSmap_val, \
      self.STmap_str, self.TSmap_str, \
        self.STmap_dotstar, self.TSmap_dotstar = \
          self._get_placeholder_mappings()

  def _rec_construct_at(self, parent_node: AbstractNode, s_expr) -> None:
    # base case: terminal node
    if isinstance(s_expr, str):
      # s_expr is a child of `str` node -> not PH
      if parent_node.get_type() in ['str', 'val']:
        node = PlainTerminalNode(s_expr, parent_node)
        parent_node.add_child(node)
        return
      # special treatment for strings, refer to d_ast_parse._anno_func_py_string()
      elif parent_node.get_parent() is not None and \
        parent_node.get_parent().get_type() == 'anno':
        node = PlainTerminalNode(s_expr, parent_node)
        parent_node.add_child(node)
        return

      if s_expr == '"."' or s_expr == '"*"':
        node = SourceDotStarPhNode(s_expr, parent_node, self.src_dot_star_next_phid)
        parent_node.add_child(node)
        self.src_dot_star_next_phid += 1
        return
      elif s_expr == '"_val_"':
        node = SourceValPhNode(s_expr, parent_node, self.src_val_next_phid)
        parent_node.add_child(node)
        self.src_val_next_phid += 1
        return
      elif s_expr == '"_str_"':
        node = SourceStrPhNode(s_expr, parent_node, self.src_str_next_phid)
        parent_node.add_child(node)
        self.src_str_next_phid += 1
        return

      dot_star_match = self._re_tar_dot_star_ph.match(s_expr)
      val_match = self._re_val_ph.match(s_expr)
      str_match = self._re_str_ph.match(s_expr)
      assert sum(list(map(bool, [dot_star_match, val_match, str_match]))) == 1
      if dot_star_match:
        node = TargetDotStarPhNode(s_expr, parent_node, int(dot_star_match.group(2)))
        parent_node.add_child(node)
        return
      elif val_match:
        node = TargetValPhNode(s_expr, parent_node, int(val_match.group(1)))
        parent_node.add_child(node)
        return
      elif str_match:
        node = TargetStrPhNode(s_expr, parent_node, int(str_match.group(1)))
        parent_node.add_child(node)
        return

      raise RuntimeError('Something is wrong. Should not reach this. Debugging needed.')

    # non-terminal node
    node_type = s_expr[0]
    node = NonTerminalNode(node_type, parent_node)
    parent_node.add_child(node)
    # recurse children
    s_expr_children = s_expr[1:]
    for s_expr_child in s_expr_children:
      self._rec_construct_at(node, s_expr_child)

  def _update_placeholder_sets(self) -> None:
    self.S = self._get_placeholders(self.src_root_node)
    self.T = self._get_placeholders(self.tar_root_node)
    assert all([isinstance(S_i, SourcePhNode) for S_i in self.S])
    assert all([isinstance(T_i, TargetPhNode) for T_i in self.T])
    self.Sfiltered_val = list(filter(lambda x: isinstance(x, SourceValPhNode), self.S))
    self.Sfiltered_str = list(filter(lambda x: isinstance(x, SourceStrPhNode), self.S))
    self.Sfiltered_dotstar = list(filter(lambda x: isinstance(x, SourceDotStarPhNode), self.S))
    self.Tfiltered_val = list(filter(lambda x: isinstance(x, TargetValPhNode), self.T))
    self.Tfiltered_str = list(filter(lambda x: isinstance(x, TargetStrPhNode), self.T))
    self.Tfiltered_dotstar = list(filter(lambda x: isinstance(x, TargetDotStarPhNode), self.T))

  def _get_placeholders(self, start_node: AbstractNode) -> List[PhNode]:
    '''return a list of placeholder nodes under `start_node`'''
    ph_nodes = []
    def visit(node: AbstractNode):
      nonlocal ph_nodes
      if isinstance(node, PhNode):
        ph_nodes.append(node)
    self._pre_order(visit, start_node)
    return ph_nodes

  def _get_placeholder_mappings(self):
    '''
    return a mapping of placeholders SOURCE->TARGET and TARGET->SOURCE

    S - set of placeholders in source pattern
    T - set of placeholders in target pattern
    STmap_val, STmap_str, STmap_dotstar - mapping of placeholders from S to T (1 -> 0,1,2,...)
    TSmap_val, TSmap_str, TSmap_dotstar - mapping of placeholders from T to S (1 -> 1)
    '''
    def _get_S_i_from_T_i(T_i: TargetPhNode, S: List[SourcePhNode]):
      for S_i in S:
        # for any placeholder type (val, str, dotstar) in T, there should be a
        # matching placeholder in S with the same placeholder id
        if T_i.get_phid() != S_i.get_phid():
          continue

        if isinstance(T_i, TargetValPhNode):
          assert isinstance(S_i, SourceValPhNode), 'sanity check failed: S_i should be a SourceValPhNode'
          return S_i

        if isinstance(T_i, TargetStrPhNode):
          assert isinstance(S_i, SourceStrPhNode), 'sanity check failed: S_i should be a SourceStrPhNode'
          return S_i

        if isinstance(T_i, TargetDotStarPhNode):
          assert isinstance(S_i, SourceDotStarPhNode), 'sanity check failed: S_i should be a SourceDotStarPhNode'
          # instead of returning S_i directly, we check their match regarding `.` and `*`
          tar_dot_star_match = self._re_tar_dot_star_ph.match(T_i.node_type)
          src_dot_star_match = self._re_src_dot_star_ph.match(S_i.node_type)
          assert tar_dot_star_match is not None, 'should not happen: regex did not match'
          assert src_dot_star_match is not None, 'should not happen: regex did not match'
          T_i_dotstar_type = tar_dot_star_match.group(1)
          S_i_dotstar_type = src_dot_star_match.group(1)
          if T_i_dotstar_type != S_i_dotstar_type:
            raise RuleMappingError('Placeholder id-s match, but `.` or `*` types do not')
          return S_i

      raise RuleMappingError('There has to be a matching placeholder in S for every placeholder in T.')

    STmap_val = dict()
    TSmap_val = dict()
    STmap_str = dict()
    TSmap_str = dict()
    STmap_dotstar = dict()
    TSmap_dotstar = dict()

    # iterate T, and find its pair in S
    for T_i in self.T:
      assert isinstance(T_i, (TargetPhNode)), 'self.T must have only placeholder nodes'
      T_i_id = T_i.get_phid()

      if isinstance(T_i, TargetValPhNode):
        S_i = _get_S_i_from_T_i(T_i, self.Sfiltered_val)
        TSmap_val[T_i_id] = S_i
        STmap_val.setdefault(S_i.get_phid(), []).append(T_i)

      elif isinstance(T_i, TargetStrPhNode):
        S_i = _get_S_i_from_T_i(T_i, self.Sfiltered_str)
        TSmap_str[T_i_id] = S_i
        STmap_str.setdefault(S_i.get_phid(), []).append(T_i)

      elif isinstance(T_i, TargetDotStarPhNode):
        S_i = _get_S_i_from_T_i(T_i, self.Sfiltered_dotstar)
        TSmap_dotstar[T_i_id] = S_i
        STmap_dotstar.setdefault(S_i.get_phid(), []).append(T_i)

      else:
        raise RuntimeError('should not happen')

    return STmap_val, TSmap_val, STmap_str, TSmap_str, STmap_dotstar, TSmap_dotstar

  def _get_mapping_of(self, node: PhNode) -> Union[List[PhNode], PhNode]:
    '''given ANY PhNode, whether source or target, returns its mapping'''
    assert isinstance(node, PhNode)

    if isinstance(node, SourceValPhNode):
      return self.STmap_val.get(node.get_phid(), [])
    elif isinstance(node, SourceStrPhNode):
      return self.STmap_str.get(node.get_phid(), [])
    elif isinstance(node, SourceDotStarPhNode):
      return self.STmap_dotstar.get(node.get_phid(), [])
    elif isinstance(node, TargetValPhNode):
      assert node.get_phid() in self.TSmap_val
      return self.TSmap_val[node.get_phid()]
    elif isinstance(node, TargetStrPhNode):
      assert node.get_phid() in self.TSmap_str
      return self.TSmap_str[node.get_phid()]
    elif isinstance(node, TargetDotStarPhNode):
      assert node.get_phid() in self.TSmap_dotstar
      return self.TSmap_dotstar[node.get_phid()]

    raise RuntimeError('Sanity check: Should not reach this. Debugging needed.')

  def src_as_s_expression(self) -> List:
    '''
    Construct s-expression from self.src_root_node (reverse of __init__())
    '''
    return self._rec_build_s_expression(self.src_root_node)

  def tar_as_s_expression(self) -> List:
    '''
    Construct s-expression from self.tar_root_node (reverse of __init__())
    '''
    return self._rec_build_s_expression(self.tar_root_node)

  def _rec_build_s_expression(self, node: AbstractNode) -> List:
    if node.is_terminal():
      return node.get_type()
    node_as_list = [node.get_type()]
    for child in node.get_children():
      node_as_list.append(self._rec_build_s_expression(child))
    return node_as_list

  def get_src_root_node(self) -> AbstractNode:
    return self.src_root_node

  def get_tar_root_node(self) -> AbstractNode:
    return self.tar_root_node

  def debug_print(self):
    def visit_fn(node: AbstractNode):
      print(str(node) + '\n')
    print('~~~ SOURCE PATTERN:')
    self._pre_order(visit_fn, self.src_root_node)
    print('\n\n\n~~~ TARGET PATTERN:')
    self._pre_order(visit_fn, self.tar_root_node)

  def _pre_order(self, visit_fn: Callable, start_node: AbstractNode) -> None:
    def _rec_pre_order(node: AbstractNode, visit_fn: Callable):
      visit_fn(node)
      for child in node.get_children():
        _rec_pre_order(child, visit_fn)
    _rec_pre_order(start_node, visit_fn)

  def __str__(self) -> str:
    return p_rule_inferencer.pretty_rule(
      self.src_as_s_expression(),
      self.tar_as_s_expression(),
      tree_like=False
    )

  # TODO re-implement hard-coded version
  def replace_secret_with_placeholder(self, secret_identifier: str) -> None:
    '''
    Given a 'secret' identifier (function name, or any other identifier),
    replace ONLY it with a placeholder `"*"`.
    As a convention, the function assumes that the 'secret' is a function call.

    IDEA
    Hacky for each language. Find the location of `secret` node,
    go up until (not including) `py.block` or 'js.statement_block` (a.k.a. stop node).
    Another idea is to leverage the template that was used to generate the pairs for this rule.

    TERMS
    SP - set of placeholder nodes in the source pattern that are under the nodes to-be-pruned
    SP_bar - set of placeholder nodes in the source pattern that are under the nodes NOT to-be-pruned
    TP - set of placeholder nodes in the target pattern that are under the nodes to-be-pruned
    TP_bar - set of placeholder nodes in the target pattern that are under the nodes NOT to-be-pruned
    '''

    # TODO HACK
    def _hack_parent_is_stop(node: 'AbstractNode'):
      assert node is not None, 'Did not find the secret node'
      if not node.has_parent():
        return False
      assert node.has_parent()
      if node.get_parent().get_type() in ['"py.block"', '"js.statement_block"']:
        return True
      if node.get_parent().get_type() in ['"py.list"', '"js.array"']:
        return True
      if node.get_parent().get_type() in ['"py.dictionary"', '"js.object"']:
        return True
      return False

    # 1 find the secret node
    src_secret_node = self._rec_find_secret_node(self.src_root_node, secret_identifier)
    tar_secret_node = self._rec_find_secret_node(self.tar_root_node, secret_identifier)
    if src_secret_node is None:
      raise SecretNodeNotFoundError(f'Secret node `{secret_identifier}` is not found in source pattern')
    if tar_secret_node is None:
      raise SecretNodeNotFoundError(f'Secret node `{secret_identifier}` is not found in target pattern')

    # 2 go up to the stop node (`py.block` or 'js.statement_block`)
    src_stop_node = src_secret_node
    while not _hack_parent_is_stop(src_stop_node):
      src_stop_node = src_stop_node.get_parent()
    src_stop_parent_node = src_stop_node.get_parent()

    tar_stop_node = tar_secret_node
    while not _hack_parent_is_stop(tar_stop_node):
      tar_stop_node = tar_stop_node.get_parent()
    tar_stop_parent_node = tar_stop_node.get_parent()

    # 3 determine siblings to the right
    src_siblings_right = src_stop_node.get_siblings_to_the_right()
    tar_siblings_right = tar_stop_node.get_siblings_to_the_right()

    # 4 identify placeholders SP, SP_bar, TP, TP_bar
    # need them to update placeholder mappings
    SP, TP = [], []
    for _node in [src_stop_node] + src_siblings_right:
      SP.extend(self._get_placeholders(_node))
    for _node in [tar_stop_node] + tar_siblings_right:
      TP.extend(self._get_placeholders(_node))
    SP_bar = [_node for _node in self.S if _node not in SP]
    TP_bar = [_node for _node in self.T if _node not in TP]

    # 5 assert precondition: all_mapped(SP, TP). Note that all_mapped(TP, SP) is not necessary
    # this check is needed to not prune placeholder nodes in SP that are used in TP_bar
    # TODO maybe raise an exception OR return null?
    for SP_i in SP:
      for T_i in self._get_mapping_of(SP_i):
        assert T_i in TP

    # 6 prune both source and target
    # NOTE we do the same way as in replace_secret_and_after_with_placeholder
    # since secret function call node is the only node (no previous nodes, so no need to worry about them)
    src_stop_node_idx_in_parent = src_stop_node.get_index_as_child()
    tar_stop_node_idx_in_parent = tar_stop_node.get_index_as_child()
    del src_stop_node.get_parent().get_children()[src_stop_node.get_index_as_child()]
    del tar_stop_node.get_parent().get_children()[tar_stop_node.get_index_as_child()]

    # 7 create a placeholder in both source and target and map them to each other
    # NOTE always replace with '*'
    src_placeholder_node = SourceDotStarPhNode('"*"', src_stop_parent_node, self.src_dot_star_next_phid)
    src_stop_parent_node.add_child_at(src_placeholder_node, src_stop_node_idx_in_parent)
    tar_placeholder_node = TargetDotStarPhNode(f'"*{self.src_dot_star_next_phid}"', tar_stop_parent_node, self.src_dot_star_next_phid)
    tar_stop_parent_node.add_child_at(tar_placeholder_node, tar_stop_node_idx_in_parent)

    # update placeholder mappings for newly created DotStarPhNode's
    self.STmap_dotstar[self.src_dot_star_next_phid] = [tar_placeholder_node]
    self.TSmap_dotstar[self.src_dot_star_next_phid] = src_placeholder_node
    self.src_dot_star_next_phid += 1

    # 8 remove mappings for nodes in pruned branches in both source and target
    for TP_i in TP:
      S_i = self._get_mapping_of(TP_i)
      if isinstance(TP_i, TargetValPhNode):
        self.STmap_val[S_i.get_phid()].remove(TP_i)  # may throw ValueError
        del self.TSmap_val[TP_i.get_phid()]
      if isinstance(TP_i, TargetStrPhNode):
        self.STmap_str[S_i.get_phid()].remove(TP_i)  # may throw ValueError
        del self.TSmap_str[TP_i.get_phid()]
      if isinstance(TP_i, TargetDotStarPhNode):
        self.STmap_dotstar[S_i.get_phid()].remove(TP_i)  # may throw ValueError
        del self.TSmap_dotstar[TP_i.get_phid()]

    # 9 pre-order source pattern, and update ph_id's incrementally
    self._recalculate_phids_and_remap(SP, TP)

    # 10
    self._update_placeholder_sets()

  def _rec_find_secret_node(self, start_node: AbstractNode, secret_keyword: str) -> Union[AbstractNode, None]:
    '''search for a node using pre-order traversal'''
    if start_node.get_type().strip('"') == secret_keyword:
      return start_node
    for child in start_node.get_children():
      child_res = self._rec_find_secret_node(child, secret_keyword)
      if child_res is not None:
        return child_res
    return None

  def _recalculate_phids_and_remap(self, SP: List[SourcePhNode], TP: List[TargetPhNode]) -> None:
    '''
    recalculate placeholder ids and update mappings after source and target patterns are modified
    SP: list of placeholder nodes that were pruned in source pattern
    TP: list of placeholder nodes that were pruned in target pattern
    '''
    self.src_dot_star_next_phid = 1
    self.src_val_next_phid = 1
    self.src_str_next_phid = 1

    STmap_val_new = dict()
    TSmap_val_new = dict()
    STmap_str_new = dict()
    TSmap_str_new = dict()
    STmap_dotstar_new = dict()
    TSmap_dotstar_new = dict()

    def _visit_update_phid(S_i: AbstractNode):
      nonlocal STmap_val_new
      nonlocal TSmap_val_new
      nonlocal STmap_str_new
      nonlocal TSmap_str_new
      nonlocal STmap_dotstar_new
      nonlocal TSmap_dotstar_new
      nonlocal SP, TP
      if isinstance(S_i, SourceValPhNode):
        T_i_list = self._get_mapping_of(S_i)
        # update mappings S->T
        STmap_val_new[self.src_val_next_phid] = [T_i for T_i in T_i_list if T_i not in TP]
        # update phid S_i
        S_i.set_phid(self.src_val_next_phid)
        for T_i in T_i_list:
          # update mappings T -> S
          TSmap_val_new[self.src_val_next_phid] = S_i
          # update phid T_i
          self._update_phid_tar_phnode(T_i, self.src_val_next_phid)
        self.src_val_next_phid += 1
      elif isinstance(S_i, SourceStrPhNode):
        T_i_list = self._get_mapping_of(S_i)
        # update mappings S->T
        STmap_str_new[self.src_str_next_phid] = [T_i for T_i in T_i_list if T_i not in TP]
        # update phid S_i
        S_i.set_phid(self.src_str_next_phid)
        for T_i in T_i_list:
          # update mappings T -> S
          TSmap_str_new[self.src_str_next_phid] = S_i
          # update phid T_i
          self._update_phid_tar_phnode(T_i, self.src_str_next_phid)
        self.src_str_next_phid += 1
      elif isinstance(S_i, SourceDotStarPhNode):
        T_i_list = self._get_mapping_of(S_i)
        # update mappings S->T
        STmap_dotstar_new[self.src_dot_star_next_phid] = [T_i for T_i in T_i_list if T_i not in TP]
        # update phid S_i
        S_i.set_phid(self.src_dot_star_next_phid)
        for T_i in T_i_list:
          # update mappings T -> S
          TSmap_dotstar_new[self.src_dot_star_next_phid] = S_i
          # update phid T_i
          self._update_phid_tar_phnode(T_i, self.src_dot_star_next_phid)
        self.src_dot_star_next_phid += 1

    self._pre_order(_visit_update_phid, self.src_root_node)

    self.STmap_val = STmap_val_new
    self.TSmap_val = TSmap_val_new
    self.STmap_str = STmap_str_new
    self.TSmap_str = TSmap_str_new
    self.STmap_dotstar = STmap_dotstar_new
    self.TSmap_dotstar = TSmap_dotstar_new

  def _update_phid_tar_phnode(self, tar_phnode: TargetPhNode, new_phid: int) -> None:
    '''update placeholder id for target node'''
    assert isinstance(tar_phnode, TargetPhNode)

    tar_phnode.set_phid(new_phid)
    if isinstance(tar_phnode, TargetValPhNode):
      tar_phnode.set_type(f'"_val{new_phid}_"')
    elif isinstance(tar_phnode, TargetStrPhNode):
      tar_phnode.set_type(f'"_str{new_phid}_"')
    else:
      dot_star_match = self._re_tar_dot_star_ph.match(tar_phnode.get_type())
      assert dot_star_match
      dot_or_star = dot_star_match.group(1)
      tar_phnode.set_type(f'"{dot_or_star}{new_phid}"')

  def trim_context(
    self,
    context: dict,
  ) -> Union[None, Tuple[list, list]]:
    '''
    Trim the given context from TranslationRule.
    This method is an API for server_trans.pirel_postprocess_translation_rule()

    POST: self is not mutated

    NOTE this method is a doppleganger of p_llm_val._context_exists()
    '''

    def _rec_pre_order_find_node_under_context(
      node: AbstractNode,
      context: List[List[str]]
    ) -> Optional[AbstractNode]:
      '''
      NOTE previously would return a list of nodes.
      Current implementation should return the only valid node.
      '''
      nt_children = node.get_nt_children()
      if len(nt_children) == 0:
        return None

      siblings_and_child = list(reversed(context[-1]))
      assert len(siblings_and_child) >= 1, 'sanity check'

      # base case
      if len(context) == 1:
        siblings = siblings_and_child[:-1]
        for i in range(len(siblings)):
          _sibi = siblings[i]
          _ntci = nt_children[i]

          # NOTE `p_data_structures.PatternNode.get_path_to_root_source._get_path`
          # refer to the function above for more information on why check for `pirel_anynode`.
          # `pirel_anynode` refers to a "." placeholder in match fragment of a translation rule
          # that is not used in the expand fragment, and can match any non-terminal node.
          if _sibi == 'pirel_anynode':
            continue

          if _sibi != _ntci.get_type().strip('"'):
            return None
        return nt_children[len(siblings)]

      # for ntype in reversed(context_elem):
      for i in range(len(siblings_and_child)):
        _saci = siblings_and_child[i]
        _ntci = nt_children[i]
        assert _saci != 'pirel_anynode', 'consider this case'

        if _saci != _ntci.get_type().strip('"'):
          return None
        # last matching element
        if i == len(siblings_and_child) - 1:
          result = _rec_pre_order_find_node_under_context(_ntci, context[:-1])
          if result is None:
            return None
          else:
            return result

    source_context = context['source_context']
    target_context = context['target_context']

    src_problematic_node = _rec_pre_order_find_node_under_context(self.src_root_node, source_context)
    tar_problematic_node = _rec_pre_order_find_node_under_context(self.tar_root_node, target_context)

    # context is not found
    if src_problematic_node is None or tar_problematic_node is None:
      return None

    # problematic node is 'fragment' if context is empty
    # TODO is there a better way to do this?
    is_src_context_empty = src_problematic_node.get_type() == 'fragment'
    is_tar_context_empty = tar_problematic_node.get_type() == 'fragment'

    # here we need to make src_problematic_node and tar_problematic_node
    # root nodes of their corresponding trees
    # 2 necessary condition for isolation is that
    # all placeholder nodes in tar are mapped under src
    src_ph_nodes = self._get_placeholders(src_problematic_node)
    tar_ph_nodes = self._get_placeholders(tar_problematic_node)
    tar_ph_nodes_mappings = [self._get_mapping_of(x) for x in tar_ph_nodes]
    for tar_ph_node_mapping in tar_ph_nodes_mappings:
      assert tar_ph_node_mapping in src_ph_nodes

    # 3 SP and TP are ph nodes under to-be-pruned trees
    all_src_ph_nodes = self._get_placeholders(self.src_root_node)
    all_tar_ph_nodes = self._get_placeholders(self.tar_root_node)
    SP = [phn for phn in all_src_ph_nodes if phn not in src_ph_nodes]
    TP = [phn for phn in all_tar_ph_nodes if phn not in tar_ph_nodes]

    # 4 make the problematic nodes roots
    # if context is empty, we don't need to modify the tree
    if not is_src_context_empty:
      self.src_root_node.set_children([src_problematic_node])
      src_problematic_node.set_parent(self.src_root_node)
    if not is_tar_context_empty:
      self.tar_root_node.set_children([tar_problematic_node])
      tar_problematic_node.set_parent(self.tar_root_node)

    # TODO when do we need to add ph node?
    if not is_src_context_empty and not is_tar_context_empty:
      # 5 add a star ph node
      src_placeholder_node = SourceDotStarPhNode('"*"', self.src_root_node, self.src_dot_star_next_phid)
      self.src_root_node.add_child(src_placeholder_node)
      tar_placeholder_node = TargetDotStarPhNode(f'"*{self.src_dot_star_next_phid}"', self.tar_root_node, self.src_dot_star_next_phid)
      self.tar_root_node.add_child(tar_placeholder_node)

      # 6 update placeholder mappings for newly created DotStarPhNode's
      self.STmap_dotstar[self.src_dot_star_next_phid] = [tar_placeholder_node]
      self.TSmap_dotstar[self.src_dot_star_next_phid] = src_placeholder_node
      self.src_dot_star_next_phid += 1

    # 7 remove mappings for nodes in pruned branches in both source and target
    for TP_i in TP:
      S_i = self._get_mapping_of(TP_i)
      if isinstance(TP_i, TargetValPhNode):
        self.STmap_val[S_i.get_phid()].remove(TP_i)  # may throw ValueError
        del self.TSmap_val[TP_i.get_phid()]
      if isinstance(TP_i, TargetStrPhNode):
        self.STmap_str[S_i.get_phid()].remove(TP_i)  # may throw ValueError
        del self.TSmap_str[TP_i.get_phid()]
      if isinstance(TP_i, TargetDotStarPhNode):
        self.STmap_dotstar[S_i.get_phid()].remove(TP_i)  # may throw ValueError
        del self.TSmap_dotstar[TP_i.get_phid()]

    # 8 do some final stuff
    self._recalculate_phids_and_remap(SP, TP)
    self._update_placeholder_sets()

    src_trimmed_pattern = self._rec_build_s_expression(self.src_root_node)
    tar_trimmed_pattern = self._rec_build_s_expression(self.tar_root_node)

    return src_trimmed_pattern, tar_trimmed_pattern

  def convert_ident_captures_to_dot_phs(self) -> Union[None, Tuple[list, list]]:
    '''
    Convert all identifier captures in both source and target patterns to dot placeholders.
    For example,
    (fragment ("py.expression_statement" ("py.assignment" ("py.identifier" "_val_") (str "=") ("py.identifier" "_val_"))) "*")
    becomes
    (fragment ("py.expression_statement" ("py.assignment" "."                       (str "=") "."                      )) "*")
    '''

    # TODO this is done on ALL identifier captures, might want to limit only to specific ones
    src_id_captures = [ph for ph in self.S if isinstance(ph, SourceValPhNode) and ph.get_parent().get_type() == '"py.identifier"']

    for src_id_capture in src_id_captures:
      tar_id_captures = self._get_mapping_of(src_id_capture)

      src_idnode = src_id_capture.get_parent()
      src_dot_ph_parent = src_idnode.get_parent()
      src_idnode_idx = src_idnode.get_index_as_child()
      src_idnode.set_parent(None)
      src_dot_ph = SourceDotStarPhNode('"."', src_dot_ph_parent, self.src_dot_star_next_phid)
      self.src_dot_star_next_phid += 1
      src_dot_ph_parent.get_children()[src_idnode_idx] = src_dot_ph

      for tar_id_capture in tar_id_captures:
        tar_idnode = tar_id_capture.get_parent()
        tar_dot_ph_parent = tar_idnode.get_parent()
        tar_idnode_idx = tar_idnode.get_index_as_child()
        tar_idnode.set_parent(None)
        tar_dot_ph = TargetDotStarPhNode(f'".{src_dot_ph.get_phid()}"', tar_dot_ph_parent, src_dot_ph.get_phid())
        tar_dot_ph_parent.get_children()[tar_idnode_idx] = tar_dot_ph

    self._update_placeholder_sets()
    self.STmap_val, self.TSmap_val, \
      self.STmap_str, self.TSmap_str, \
        self.STmap_dotstar, self.TSmap_dotstar = \
          self._get_placeholder_mappings()
    self._recalculate_phids_and_remap([], [])

    src_pattern = self._rec_build_s_expression(self.src_root_node)
    tar_pattern = self._rec_build_s_expression(self.tar_root_node)
    return src_pattern, tar_pattern
