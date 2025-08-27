'''
This module provides base classes for visitors across multiple languages.

Classes:
  - Visitor: Base class for implementing the visitor pattern.
  - AbstractNode: Base class for implementing nodes in an AST.
  - TerminalNode: Base class for implementing terminal nodes in an AST.
'''


from __future__ import annotations

from abc import ABC
from typing import final, Any, List, Union


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
    def _recurse(descendant: AbstractNode, other_node: AbstractNode) -> bool:
      if id(descendant) == id(other_node):
        return True
      for child_node in descendant.get_children():
        child_res = _recurse(child_node, other_node)
        if child_res:
          return True
      return False
    return _recurse(self, other_node)

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


class TerminalNode(AbstractNode):
  def __repr__(self) -> str:
    return f'Terminal({repr(self.node_type)})'
