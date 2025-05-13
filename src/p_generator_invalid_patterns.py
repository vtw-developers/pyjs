import d_ast_parse
import p_data_structures as pds


def pattern_1_has_integer_as_call_function(node: pds.DuoGlotNode) -> bool:
  '''
  RETURN True if the snippet contains an integer as function name.
  '''
  # node must be non-terminal
  if node.is_terminal():
    return False
  # node must be call
  if node.get_ts_node_type() != 'call':
    return False
  # first child must be non-terminal
  first_child = node.get_children()[0]
  assert first_child.is_nonterminal(), 'first child must be non-terminal'
  # first child must be an integer
  if first_child.get_ts_node_type() != 'integer':
    return False
  return True


def pattern_2_empty_arglist_for_range(node: pds.DuoGlotNode) -> bool:
  '''
  RETURN True if the snippet contains an empty argument list for range.
  '''
  # node must be non-terminal
  if node.is_terminal():
    return False
  # node must be call
  if node.get_ts_node_type() != 'call':
    return False
  # assert first child must be non-terminal
  first_child = node.get_children()[0]
  assert first_child.is_nonterminal(), 'first child must be non-terminal'
  # first child must be an identifier
  if first_child.get_ts_node_type() != 'identifier':
    return False
  # function name must be range
  fn_name = first_child.get_children()[0].node_type
  if fn_name != 'range':
    return False
  # assert second child must be non-terminal
  second_child = node.get_children()[1]
  assert second_child.is_nonterminal(), 'second child must be non-terminal'
  # second child must be an argument list
  if second_child.get_ts_node_type() != 'argument_list':
    return False
  # argument_list must have zero non-terminal children
  if second_child.get_num_nt_children() > 0:
    return False
  return True
