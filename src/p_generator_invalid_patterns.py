import p_data_structures as pds


def pattern_1_has_integer_as_function_name(node: pds.DuoGlotNode) -> bool:
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


def pattern_2_has_range_with_empty_argument_list(node: pds.DuoGlotNode) -> bool:
  '''
  RETURN True if the snippet contains an empty argument list for `range` function.
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


def pattern_3_has_block_with_ret_stat_secretfn_flag_on(node: pds.DuoGlotNode, template_dict: dict) -> bool:
  '''
  RETURN True if the snippet contains a block with a return statement
  when is_insert_secret_fn flag is turned on.
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


def pattern_4_has_floatfn_with_empty_argument_list(node: pds.DuoGlotNode) -> bool:
  '''
  RETURN True if the snippet contains a float function with an empty argument list.
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
  # function name must be float
  fn_name = first_child.get_children()[0].node_type
  if fn_name != 'float':
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
