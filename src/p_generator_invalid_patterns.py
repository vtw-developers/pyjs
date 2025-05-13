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
