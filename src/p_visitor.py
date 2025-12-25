'''
This module provides base classes for visitors across multiple languages.

Classes:
  - Visitor: Base class for implementing the visitor pattern.
  - AbstractNode: Base class for implementing nodes in an AST.
  - TerminalNode: Base class for implementing terminal nodes in an AST.
'''


from __future__ import annotations

from abc import ABC
from typing import final, Any, List, Optional, Union


class Visitor(ABC):
  @final
  def visit(self, node: AbstractNode) -> Any:
    '''
    This is a dispatcher method that either calls `self.visit_<NodeClass>()`
    if it exists. Otherwise, falls back to `self.default_visit()`.
    <NodeClass> is a CamelCase class name for parameter `node`.
    NOTE this method is intended to be final, i.e. not be overridden.
    '''
    method_name = 'visit_' + node.__class__.__name__
    visit_method = getattr(self, method_name, self.default_visit)
    return visit_method(node)

  def default_visit(self, node: AbstractNode) -> None:
    '''
    Default visit method for all nodes.
    NOTE can be overridden in subclasses.
    '''
    for child in node.children:
      self.visit(child)


class AbstractNode(ABC):
  '''
  This is the base class for node classes.
  All node classes should inherit from this class.
  '''
  def __init__(self, node_type: str) -> None:
    self.node_type = node_type
    self.children: List[AbstractNode] = []
    self.parent = None

  def __repr__(self) -> str:
    return self.node_type

  def get_type(self) -> str:
    return self.node_type

  def add_child(self, child: AbstractNode):
    self.children.append(child)

  def get_children(self) -> List[AbstractNode]:
    return self.children

  def set_parent(self, parent: AbstractNode) -> None:
    self.parent = parent

  def get_parent(self) -> AbstractNode:
    return self.parent

  def next_sibling(self) -> Union[AbstractNode, None]:
    '''
    Return the next sibling of `self` if it exists, otherwise None.
    '''
    if self.parent is None:
      return None
    siblings = self.parent.get_children()
    idx = siblings.index(self)
    if idx + 1 < len(siblings):
      return siblings[idx + 1]
    return None

  def get_root_node(self) -> AbstractNode:
    '''
    Return root_node of the tree that `self` belongs to
    According to class invariant INV2, root_node's parent is itself.
    '''
    cursor = self
    while cursor.parent is not None:
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
    '''
    Check if `self` is an ancestor of `other_node` or if they are the same node.
    '''
    def _recurse(descendant: AbstractNode, other_node: AbstractNode) -> bool:
      if id(descendant) == id(other_node):
        return True
      for child_node in descendant.get_children():
        child_res = _recurse(child_node, other_node)
        if child_res:
          return True
      return False
    return _recurse(self, other_node)

  def is_ancestor(self, other_node: AbstractNode) -> bool:
    '''
    Check if `self` is a strict ancestor of `other_node`.
    '''
    if id(self) == id(other_node):
      return False
    return self.is_ancestor_or_itself(other_node)

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

  def is_terminal(self) -> bool:
    return isinstance(self, TerminalNode)

  def is_nonterminal(self) -> bool:
    return not self.is_terminal()

  def get_nid_node_map(self) -> dict[int, AbstractNode]:
    '''
    Get a mapping from node IDs to AST nodes.
    This function might be useful for connecting
    DuoGlot-style ASTs with ASTs represented by this class.
    NOTE Node IDs are assigned starting from 0 in a pre-order
    traversal starting from `self`. In order to get the
    right mapping for the whole tree, call this method
    on the root node of the tree.
    '''
    nid_node_map = {}
    nid_counter = 0

    def _traverse(node: AbstractNode) -> None:
      nonlocal nid_counter
      if node.is_terminal():
        return
      nid_node_map[nid_counter] = node
      nid_counter += 1
      for child in node.children:
        _traverse(child)

    _traverse(self)
    return nid_node_map

  def get_node_id(self) -> int:
    '''
    Get the node ID of `self` in the tree that `self` belongs to.
    This function might be useful for connecting
    DuoGlot-style ASTs with ASTs represented by this class.
    NOTE Node IDs are assigned starting from 0 in a pre-order
    traversal starting from the root node of the tree that `self` belongs to.
    '''
    root_node = self.get_root_node()
    nid_node_map = root_node.get_nid_node_map()
    for nid, node in nid_node_map.items():
      if id(node) == id(self):
        return nid
    raise ValueError('Node not found in its own tree, should not happen')

  def find_node_under_context(self, context: List[List[str]]) -> Optional[AbstractNode]:
    '''
    NOTE this method is copied from p_llm_val._context_exists()
    '''
    nt_children = self.get_nt_children()
    if len(nt_children) == 0:
      return None

    siblings_and_child = list(reversed(context[-1]))
    assert len(siblings_and_child) >= 1, 'sanity check'

    # base case
    if len(context) == 1:
      siblings = siblings_and_child[:-1]
      for i in range(len(siblings)):
        _sibi = siblings[i]
        _sibi = _sibi.split('.')[-1]  # remove lang prefix, i.e. "py.*"
        _ntci = nt_children[i]

        # NOTE `p_data_structures.PatternNode.get_path_to_root_source._get_path`
        # refer to the function above for more information on why check for `pirel_anynode`.
        # `pirel_anynode` refers to a "." placeholder in match fragment of a translation rule
        # that is not used in the expand fragment, and can match any non-terminal node.
        if _sibi == 'pirel_anynode':
          continue

        if _sibi != _ntci.get_type():
          return None
      return nt_children[len(siblings)]

    # for ntype in reversed(context_elem):
    for i in range(len(siblings_and_child)):
      _saci = siblings_and_child[i]
      _saci = _saci.split('.')[-1]  # remove lang prefix, i.e. "py.*"
      _ntci = nt_children[i]
      assert _saci != 'pirel_anynode', 'consider this case'

      if _saci != _ntci.get_type():
        return None
      # last matching element
      if i == len(siblings_and_child) - 1:
        result = _ntci.find_node_under_context(context[:-1])
        if result is None:
          return None
        else:
          return result

  def is_literal_node(self) -> bool:
    '''
    Literal nodes are terminal nodes that represent literals,
    e.g. string literals, numeric literals, boolean literals, etc.
    This method can be overridden in subclasses for more accuracy.
    As a default implementation, we consider all nodes with single
    terminal child as literal nodes.
    '''
    if self.is_terminal():
      return False
    if len(self.children) == 1 and self.children[0].is_terminal():
      return True
    return False

  def collect_literal_nodes(self) -> List[AbstractNode]:
    '''
    Collect all literal nodes under `self` (including `self` if it is a literal node).
    '''
    literal_nodes = []
    if self.is_literal_node():
      literal_nodes.append(self)
    for child in self.children:
      literal_nodes.extend(child.collect_literal_nodes())
    return literal_nodes


class TerminalNode(AbstractNode):
  def __repr__(self) -> str:
    return f'Terminal({repr(self.node_type)})'
