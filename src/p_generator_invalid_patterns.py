import p_data_structures as pds


def pattern_1_has_integer_as_function_name(node: pds.DuoGlotNode) -> bool:
  '''
  RETURN True if the snippet contains an integer as function name.
  NOTE Generator can generate a function with an integer as function name.
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


def pattern_2_has_block_with_ret_stat_secretfn_flag_on(node: pds.DuoGlotNode, template_dict: dict) -> bool:
  '''
  RETURN True if the snippet contains a block with a return statement
  when is_insert_secret_fn flag is turned on.
  NOTE Generator may miss putting `secret_fn_4071()` in the `block` when it's necessary.
  '''
  # is_insert_secret_fn must be turned on
  if not template_dict['is_insert_secret_fn']:
    return False
  # node must be non-terminal
  if node.is_terminal():
    return False
  # node must be block
  if node.get_ts_node_type() != 'block':
    return False
  # must have a single non-terminal child
  if node.get_num_nt_children() != 1:
    return False
  # child must be an return_statement
  first_child = node.get_children()[0]
  if first_child.get_ts_node_type() != 'return_statement':
    return False
  return True


def pattern_3_has_fn_with_empty_argument_list(node: pds.DuoGlotNode, fnname: str) -> bool:
  '''
  RETURN True if the snippet contains a function with an empty argument list.
  For example, float(), range(), len(), min().
  NOTE The simplest argument_list generated is `()`.
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
  # function name must be `fnname`
  fn_name = first_child.get_children()[0].node_type
  if fn_name != fnname:
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
