import json
from typing import List, Dict, Optional, Set, Tuple

import p_utils


logger = p_utils.setup_logger(__name__)


class NoUniqueChoicesError_deprecated(RuntimeError): pass
class RuleCombinationsExhaustedError(RuntimeError): pass


def are_choices_lists_equal_astnode_deprecated(
  choices_list: List[tuple],
  choices_list_hist_elem: List[tuple]
) -> bool:
  '''
  INV: choices_list does not contain duplicate entries for the same range_info.
  '''
  range_info_to_choice_idx : Dict[str, int] = {}

  # populate choices_range2chidx
  for range_info, choice_idx in choices_list:
    ni, si, ei = range_info
    range_info_str = f'{ni}-{si}-{ei}'

    # sanity check: no duplicate range_info choice in choices_list
    if range_info_str in range_info_to_choice_idx:
      raise ValueError(f'duplicate entry in: {range_info_to_choice_idx}')

    # choices with choice_idx == 0 are not considered
    if choice_idx != 0:
      range_info_to_choice_idx[range_info_str] = choice_idx

  for range_info_hist_elem, choice_idx_hist_elem in choices_list_hist_elem:
    nic, sic, eic = range_info_hist_elem
    range_info_str_hist_elem = f'{nic}-{sic}-{eic}'

    if range_info_str_hist_elem in range_info_to_choice_idx:
      if range_info_to_choice_idx[range_info_str_hist_elem] == choice_idx_hist_elem:
        range_info_to_choice_idx[range_info_str_hist_elem] = -1
        continue
      return False

    # ignore range_info's with choice_idx == 0
    if choice_idx_hist_elem == 0:
      continue

    return False

  for range_info_str in range_info_to_choice_idx:
    if range_info_to_choice_idx[range_info_str] != -1:
      return False

  return True


def are_choices_list_equal_step_deprecated(
  choices_list: List[Tuple[int, int]],
  choices_list_hist_elem: List[Tuple[int, int]]
) -> bool:
  ''''''
  step_to_choice_idx : Dict[int, int] = {}

  for alt_step, choice_idx in choices_list:

    # sanity check: no duplicate alt_step choice in choices_list
    if alt_step in step_to_choice_idx:
      raise ValueError(f'duplicate entry in: {step_to_choice_idx}')

    if choice_idx != 0:
      step_to_choice_idx[alt_step] = choice_idx

  for alt_step_hist_elem, choice_idx_hist_elem in choices_list_hist_elem:
    if alt_step_hist_elem in step_to_choice_idx:
      if step_to_choice_idx[alt_step_hist_elem] == choice_idx_hist_elem:
        step_to_choice_idx[alt_step_hist_elem] = -1
        continue
      return False

    if choice_idx_hist_elem == 0:
      continue

    return False

  for alt_step in step_to_choice_idx:
    if step_to_choice_idx[alt_step] != -1:
      return False

  return True


def has_been_chosen_before_deprecated(
  new_choices: dict,
  choices_history: List[dict]
):
  '''
  Compare new_choices with each element in choices_history.
  If any element in choices_history is equal to new_choices, return True.
  Otherwise, return False.
  '''
  choice_type = new_choices['type']
  choices_list = new_choices['choices_list']

  for choices_hist_elem in choices_history:
    choice_type_hist_elem = choices_hist_elem['type']
    choices_list_hist_elem = choices_hist_elem['choices_list']
    assert choice_type == choice_type_hist_elem, 'sanity check: choice types must be same'
    assert choice_type in ['STEP', 'ASTNODE'], f'unknown choice type: "{choice_type}"'

    if choice_type == 'STEP':
      if are_choices_list_equal_step_deprecated(choices_list, choices_list_hist_elem):
        return True

    elif choice_type == 'ASTNODE':
      if are_choices_lists_equal_astnode_deprecated(choices_list, choices_list_hist_elem):
        return True

  return False


def get_updated_choices_list_astnode_deprecated(
  current_choices_list: List[Tuple[Tuple[int], int]],
  rel_current_range_info: Tuple[int],
  new_choice_idx: int
) -> List[Tuple[Tuple[int], int]]:
  '''
  rel_current_range_info is a tuple of (node_id, start_idx, end_idx)
  '''
  new_choices_list = []
  is_current_node_set = False
  cni, csi, cei = rel_current_range_info

  for current_choice in current_choices_list:
    ni, si, ei = current_choice[0]

    # choice in choices_list points to the same AST node
    if cni == ni and csi == si and cei == ei:
      is_current_node_set = True
      if new_choice_idx != 0:
        new_choices_list.append((rel_current_range_info, new_choice_idx))
      continue

    # choice in choices_list points to a different AST node
    # we keep it as is
    new_choices_list.append(current_choice)

  if not is_current_node_set and new_choice_idx != 0:
    new_choices_list.append((rel_current_range_info, new_choice_idx))

  return new_choices_list


def get_updated_choices_list_step_deprecated(
  current_choices_list: List[Tuple[int, int]],
  rel_alt_step: int,
  new_choice_idx: int
) -> List[Tuple[int, int]]:
  ''''''
  new_choices_list = []
  is_current_step_set = False

  for current_choice in current_choices_list:
    alt_step = current_choice[0]

    # choice in choices_list points to the same alt_step
    if alt_step == rel_alt_step:
      is_current_step_set = True
      if new_choice_idx != 0:
        new_choices_list.append((rel_alt_step, new_choice_idx))
      continue

    # choice in choices_list points to a alt_step
    # we keep it as is
    if alt_step <= rel_alt_step:
      new_choices_list.append(current_choice)

  if not is_current_step_set and new_choice_idx != 0:
    new_choices_list.append((rel_alt_step, new_choice_idx))

  return new_choices_list


def get_next_unique_choices_deprecated(
  rel_alt_step_infos: Dict[int, dict],
  current_choices: dict,
  choices_history: List[dict]
) -> dict:
  logger.debug('Starting p_rule_chooser.get_next_unique_choices')

  choice_type = current_choices['type']
  current_choices_list : list = current_choices['choices_list']
  assert choice_type in ['STEP', 'ASTNODE'], f'unsupported choice type: "{choice_type}"'

  if choice_type == 'STEP':
    for rel_alt_step, info_dict in rel_alt_step_infos.items():
      rel_next_choices_count = info_dict['next_choices_count']
      rel_current_choice_idx = info_dict['current_choose_idx']

      new_choice_idxs = list(range(rel_next_choices_count))
      for new_choice_idx in new_choice_idxs:
        if new_choice_idx == rel_current_choice_idx:
          continue
        updated_choices_list = get_updated_choices_list_step_deprecated(current_choices_list, rel_alt_step, new_choice_idx)
        new_choices = {
          'type': 'STEP',
          'choices_list': updated_choices_list
        }
        is_in_history = has_been_chosen_before_deprecated(new_choices, choices_history)
        if not is_in_history:
          return new_choices
    raise NoUniqueChoicesError_deprecated('No unique choices found')

  elif choice_type == 'ASTNODE':
    for info_dict in rel_alt_step_infos.values():
      rel_next_choices_count = info_dict['next_choices_count']
      rel_current_choice_idx = info_dict['current_choose_idx']
      rel_current_range_info = info_dict['current_range_info']

      new_choice_idxs = list(range(rel_next_choices_count))
      for new_choice_idx in new_choice_idxs:
        if new_choice_idx == rel_current_choice_idx:
          continue
        updated_choices_list = get_updated_choices_list_astnode_deprecated(current_choices_list, rel_current_range_info, new_choice_idx)
        new_choices = {
          'type': 'ASTNODE',
          'choices_list': updated_choices_list
        }
        is_in_history = has_been_chosen_before_deprecated(new_choices, choices_history)
        if not is_in_history:
          return new_choices
    raise NoUniqueChoicesError_deprecated('No unique choices found')


def are_choices_lists_equal(
  gen_choices_list: List[tuple],
  actual_choices_list: List[tuple]
) -> bool:
  '''
  An actual choices list may be longer, because a new choice may
  create new choice nodes down the line. For example,
  [
    ((11, 3, 5), 0),
    ((19, 4, 5), 1)
  ]
  we choose "1" in (19, 4, 5), and this is the actual choices after applying it:
  [
    ((11, 3, 5), 0),
    ((19, 4, 5), 1),
    ((23, 2, 3), 0),
    ((24, 3, 4), 0)
  ]
  As you see, (23, 2, 3) and (24, 3, 4) are new nodes at which we can make new choices.
  '''

  # The following assertion does not hold for all cases.
  # Refer to "debug-35-gfg20-rate-14" / G0001.
  # assert len(actual_choices_list) >= len(gen_choices_list), \
  #   'sanity check: actual choices list must be longer or equal to generated choices list'

  if len(actual_choices_list) > len(gen_choices_list):
    for choice in actual_choices_list[len(gen_choices_list):]:
      range_info, choice_idx = choice
      assert choice_idx == 0, 'sanity check: actual choices list must contain only 0 choice_idx for new nodes'

  '''
  In case actuall list is longer, the new nodes are not considered.
  '''
  for choice_a, choice_b in zip(gen_choices_list, actual_choices_list):
    range_info_a, choice_idx_a = choice_a
    range_info_b, choice_idx_b = choice_b
    if range_info_a != range_info_b:
      return False
    if choice_idx_a != choice_idx_b:
      return False
  return True


def choices_stack_list_to_choices_list(
  choices_list_stack: List[List[Tuple[Tuple[int], int]]]
) -> List[Tuple[Tuple[int], int]]:
  '''
  Convert a stack of choices lists to a single choices list.
  The stack is a list of lists, where each inner list is a choices list.
  The function returns a single choices list that contains all the choices
  from the stack, preserving the order of choices.
  '''
  choices_list = []
  for choices in choices_list_stack:
    for choice in choices:
      assert choice not in choices_list, f'duplicate choice found: {choice}'
      choices_list.append(choice)
  return choices_list


def get_next_unique_choices(
  rel_alt_step_infos: Dict[int, dict],
  choices_list_stack: list
) -> dict:
  '''
  Updated and fixed version. Exhaustively checks all possible choices.
  '''

  '''
  `rel_alt_step_infos` contains information about all the possible
  translation rules that can be applied to obtain a different translation.
  '''
  rasis_values = list(rel_alt_step_infos.values())

  '''
  `choices_list` contains current choices of rules at certain AST nodes.
  The fact that we are inside this function tells that these choices
  were invalid and must be replaced.
  '''
  choices_list = [
    (info['current_range_info'], info['current_choose_idx'])
    for info in rasis_values
  ]

  '''
  This is done only once (to bootstrap the stack).
  '''
  if len(choices_list_stack) == 0:
    choices_list_stack.append(choices_list)

  '''
  This makes sure that we pop the invalid choices_list from the stack.
  '''
  if are_choices_lists_equal(choices_list_stack[-1], choices_list):
    choices_list_stack.pop()

  new_choices_list = _get_new_choices_list_rec(rasis_values)
  if new_choices_list is None:
    raise RuleCombinationsExhaustedError('Exhaustively checked all possible choices')
  choices_list_stack.append(new_choices_list)

  all_choices_list = choices_stack_list_to_choices_list(choices_list_stack)
  return {'type': 'ASTNODE', 'choices_list': all_choices_list}


def _get_new_choices_list_rec(rasis_values: List[dict]) -> Optional[list]:
  '''
  PARAM rasis_values: a list of dictionaries, each dictionary contains:
    - 'next_choices_count': number of rules that can be applied
    - 'current_choose_idx': index of the chosen rule
    - 'current_range_info': range_info of the current alt object
  '''

  '''
  The idea is to choose the next combination at the lower level.
  If there are no more choices at the lower level, choose the next
  combination one level up.
  '''
  rasis_value = rasis_values[0]
  next_choices_count = rasis_value['next_choices_count']
  current_choose_idx = rasis_value['current_choose_idx']
  current_range_info = rasis_value['current_range_info']

  # base case
  if len(rasis_values) == 1:
    if current_choose_idx + 1 == next_choices_count:
      return None
    node_choice = (current_range_info, current_choose_idx + 1)
    return [node_choice]

  # recursive call
  choices_down_the_line = _get_new_choices_list_rec(rasis_values[1:])
  if choices_down_the_line is None:
    if current_choose_idx + 1 == next_choices_count:
      return None
    node_choice = (current_range_info, current_choose_idx + 1)
    return [node_choice]
  else:
    node_choice = (current_range_info, current_choose_idx)
    return [node_choice] + choices_down_the_line


def get_char_line_col_idxs(main_code_lines: List[str]) -> Tuple[List[int], List[int]]:
  '''
  Given the code split into lines, return the line and column indices of each character.
  The column index is -1 for the newline character.
  '''
  line_idxs = []
  col_idxs = []
  for i, line in enumerate(main_code_lines):
    for j, _ in enumerate(line):
      line_idxs.append(i)
      col_idxs.append(j)
    # the newline char
    line_idxs.append(i)
    col_idxs.append(-1)
  return line_idxs, col_idxs


def get_err_line_idx_in_tar_main_code(
  line_content: str,
  err_line_tpi: int,
  tar_program_instr: str,
  tar_main_code: str
) -> int:
  '''
  Get the index of the line in `tar_main_code` that corresponds to the error line.
  PARAM tar_program_instr: instrumented target program (test, main, test call)
  PARAM tar_main_code: main code of the target program (main)
  PARAM err_line_tpi: line number in `tar_program_instr` where the error occurred (1 indexed)
  PARAM line_content: content of the line where the error occurred in `tar_program_instr`
  '''
  tpi_chunks = tar_program_instr.split(tar_main_code)
  assert len(tpi_chunks) == 2, 'sanity check: tar_main_code should appear exactly once in wrapper'

  pre_main_code = tpi_chunks[0]
  pre_main_code_line_count = len(pre_main_code.split('\n'))

  err_line_idx = err_line_tpi - pre_main_code_line_count
  main_code_lines = tar_main_code.split('\n')
  assert err_line_idx < len(main_code_lines), 'sanity check: err_line_idx should be within main_code_lines'

  expected_line = main_code_lines[err_line_idx]
  assert line_content in expected_line, \
    (f'Expected line does not contain error line content.\n'
     f'Expected: "{expected_line}"\n'
     f'Actual: "{line_content}"\n')

  return err_line_idx


def get_proposed_choices_based_on_line_idxs(
  tar_main_code: str,
  err_line_idxs: List[int],
  choices_list_stack: list,
  map_to_exid: Dict[int, List[dict]],
  translate_dbg_history: List[dict],
):
  '''
  PARAM tar_main_code: main code (f_gold) of the target program.
  PARAM err_line_idxs: a list of 0-based indices of the lines in
  `tar_main_code` where the error occurred.
  '''

  '''
  The following function returns the line indices of every character
  in tar_main_code.
  '''
  main_code_lines = tar_main_code.split('\n')
  line_idxs, col_idxs = get_char_line_col_idxs(main_code_lines)

  '''
  The following loop creates `line_idx_to_exids` - a mapping of
  line indices to expansion ids that are present at the line.
  '''
  line_idx_to_exids : Dict[int, Set[int]] = {}
  for exid, tokens_by_ex in map_to_exid.items():
    for token_by_ex in tokens_by_ex:
      # token in tar_main_code and its range
      token = token_by_ex['str']
      token_range = token_by_ex['range']
      _si, _ei = token_range  # start and end indices of the token in tar_main_code
      assert tar_main_code[_si:_ei] == token, f'sanity check: discrepancy in token range'
      line_si : int = line_idxs[_si]
      line_ei : int = line_idxs[_ei]
      assert line_si == line_ei, 'sanity check: token spans multiple lines'
      assert token in main_code_lines[line_si], f'sanity check: token not found in tar_main_code'
      line_idx_to_exids.setdefault(line_si, set()).add(exid)

  '''
  Create two objects:
  1. mod_dbg_history - a modified version of `translate_dbg_history` that contains
     only the necessary information for the rule chooser.
  2. exid_to_mod_dbg_history_elem - a mapping of expansion ids to the corresponding
     elements in `mod_dbg_history`.
  This is used to quickly access the debug history element for a given expansion id.
  '''
  mod_dbg_history : Dict[int, dict] = {}
  exid_to_mod_dbg_history_elem : Dict[int, dict] = {}
  for elem in translate_dbg_history:
    alt_step = elem['alt_step']
    exid = elem['dbg_info']['ex_id']
    # the assertion below ensures that the dbg_history elements
    # come in the order of alt_step starting from 1.
    assert alt_step - 1 == len(mod_dbg_history), 'sanity check: dbg history elems should come in order'
    mod_dbg_history_elem = {
      'alt_step': alt_step,
      'next_choices_count': elem['next_choices_status']['count'],
      'next_choices_all_known': elem['next_choices_status']['done'],
      'ex_id': exid,
      'current_choose_idx': elem['dbg_info']['notes']['choose_idx'],
      'current_rule_id': elem['dbg_info']['notes']['rule_id'],
      'current_range_info': elem['range_info']
    }
    mod_dbg_history[alt_step] = mod_dbg_history_elem
    exid_to_mod_dbg_history_elem[exid] = mod_dbg_history_elem

  '''
  INVARIANT: `alt_step` starts from 1
  Iterate over expansions on the error line, and for each expansion:
  1. Get the `mod_dbg_history_elem` for the expansion (alt object).
  2. For the given alt object, get the previous `_RELATED_WINDOW_SIZE` elements
  3. From the selected alt objects, keep only those that have more than
     one rule that can be applied at that alt object.
  '''
  _RELATED_WINDOW_SIZE = 0
  exids_err_line : List[int] = list(sorted(set(
    [exid for err_line_idx in err_line_idxs for exid in line_idx_to_exids[err_line_idx]]
  )))
  rel_alt_step_infos : Dict[int, dict] = {}

  for exid_err_line in exids_err_line:
    mod_dbg_history_elem = exid_to_mod_dbg_history_elem[exid_err_line]
    alt_step : int = mod_dbg_history_elem['alt_step']

    # previous _RELATED_WINDOW_SIZE elements + alt_step itself
    rel_alt_steps = list(range(alt_step - _RELATED_WINDOW_SIZE, alt_step + 1))
    for rel_alt_step in rel_alt_steps:
      # because we use `rel_alt_step - 1` below
      if rel_alt_step - 1 < 1:
        continue
      # keep only if number of rules at that step is greater than 1
      if mod_dbg_history[rel_alt_step - 1]['next_choices_count'] <= 1:
        continue
      rel_alt_step_infos[rel_alt_step] = {
        'next_choices_count': mod_dbg_history[rel_alt_step - 1]['next_choices_count'],
        'current_choose_idx': mod_dbg_history[rel_alt_step]['current_choose_idx'],
        # 'ex_id': mod_dbg_history[rel_alt_step]['ex_id'],  # not used
        # 'current_rule_id': mod_dbg_history[rel_alt_step]['current_rule_id'],  # not used
        'current_range_info': mod_dbg_history[rel_alt_step]['current_range_info']
      }

  if len(rel_alt_step_infos) == 0:
    raise RuleCombinationsExhaustedError('No alternative rules found for the error line')

  new_choices = get_next_unique_choices(rel_alt_step_infos, choices_list_stack)
  return new_choices


def get_proposed_choices_compile_error(
  tar_program_instr: str,
  tar_main_code: str,
  tar_error_dict: dict,
  choices_list_stack: list,
  map_to_exid: Dict[int, List[dict]],
  translate_dbg_history: List[dict],
) -> dict:
  '''
  NOTE PARAM map_to_exid:
  <map_to_exid> -> Dict[<exid>, List[<token_info>]]
  <map_to_exid>: (id of expansion: list of all tokens that were created by this expansion)
  <token_info> -> {
    'ex_id': (id of expansion this token belongs to),
    'str': (token in tar_main_code),
    'range': (range of token in tar_main_code)
  }
  In informal words, map_to_exid contains expansion ids and all tokens that
  were created by this expansion + ranges of every token.
  map_to_exid is created by `d_ast_pretty.ast_to_code()` function.
  The function `d_ast_pretty.ast_to_code()` is called in `p_pirel.duoglot_translate_wrapper()`.

  NOTE PARAM translate_dbg_history:
  <translate_dbg_history> -> List[<history_elem>]
  <history_elem> -> {
    'alt_step' -> (translation step id),
    'range_info' -> (source AST to which the rule was mapped),
    'next_choices_status' -> <next_choices_status>,
    'dbg_info' -> <dbg_info>
  }
  <next_choices_status> -> {
    'count' -> (number of rules that matched a source AST),
    'done' -> (next_choices_all_known?)
  }
  <dbg_info> -> {
    'ex_id' -> (expansion.ex_id, id of expansion that was created from source AST),
    'corres_slot_id' -> (expansion.corres_slot_id, id of slot in source AST),
    'src_matching_node_ids' -> (expansion.matching_node_ids),
    'slot_src_matching_node_ids' -> ([_get_node_ids_from_range_cursor(x) for x in expansion.src_slot_cursors]),
    'notes' -> <notes>,
    'slot_names' -> (expansion.slot_names),
    'slot_ids' -> ([(x.slot_id if x is not None else None) for x in expansion.slots]),
    'outcome' -> (AC, RE, or ER),
    'elem_list_info_id' -> (self._optional_dbg_info_func((self._tail_stack, len(self._tail_stack)), _tail_stack_length_to_elem_list)),
    'loop_count' -> (DelimitedParser._loop_idx)
  }
  <notes> -> {
    'choose_idx': (index of rule from a list of matched rules),
    'rule_id': (id of the rule in the ruleset)
  }
  <notes>: (expansion.notes)
  This object is created in `d_grammar_expand.TransSession._get_alt_debug_history()`
  and is passed to `p_pirel.duoglot_translate_wrapper()`.
  <dbg_info> is a dictionary that is created by
  `d_grammar_dlmparser.DelimitedParser.add_expansion_parse_until_stuck()`,
  which in turn is called by `d_grammar_expand.TransSession._ensure_parser_result()`.
  '''

  p_utils.log_json_time(f'args-get_proposed_choices_compile_error.json', locals())
  logger.debug('Starting p_rule_chooser.get_proposed_choices_compile_error')

  # Unpack `tar_error_dict`. "tpi" stands for "tar_program_instr"
  error_msg = tar_error_dict['error_msg']  # e.g. 'SyntaxError: invalid syntax'
  error_type = tar_error_dict['error_type']  # e.g. 'SyntaxError'
  line_content = tar_error_dict['line_content']  # code snippet at the line of error in `tar_program_instr`
  file_path = tar_error_dict['file_path']  # absolute path to the file where the error occurred
  err_line_tpi = tar_error_dict['line_num']  # line number in the file where the error occurred (0 indexed)

  '''
  Current implementation of `get_proposed_choices_compile_error()` can propose choices
  only on the basis of errors in "tar_program_run.js". And the following
  are the errors that are supported.
  '''
  _SUPPORTED_ERROR_TYPES_JS = ['SyntaxError:', 'ReferenceError:', 'TypeError:']
  assert error_type in _SUPPORTED_ERROR_TYPES_JS, f'unsupported error type {error_type}'

  '''
  The following function returns the error line number in tar_main_code.
  We need to do this because the `err_line_tpi` points to the line number
  in "tar_program_run.js", which is the wrapper code that runs the main code.
  err_line_idx is 0-based.
  '''
  err_line_idx = get_err_line_idx_in_tar_main_code(line_content, err_line_tpi, tar_program_instr, tar_main_code)

  logger.debug(
    f'there was an error running `tar_program_instr`\n'
    f'{error_type} "{error_msg}" on line {err_line_idx + 1} of "{line_content}"\n')

  new_choices = get_proposed_choices_based_on_line_idxs(
    tar_main_code,
    [err_line_idx],
    choices_list_stack,
    map_to_exid,
    translate_dbg_history
  )
  return new_choices


def get_proposed_choices_semantic_error(
  tar_program_instr: str,
  tar_main_code: str,
  error_lines: dict,
  choices_list_stack: list,
  map_to_exid: Dict[int, List[dict]],
  translate_dbg_history: List[dict],
) -> dict:
  '''
  Propose new choices based on a semantic error. A semantic error occurs
  when traces of src and tar test scripts do not match.

  PARAM error_lines: a dictionary where keys are line numbers (0-based) and values
  are the content of the lines that caused the semantic error. Sample:
  {
    12: "    while (x && m) {"
  }
  '''

  p_utils.log_json_time(f'args-get_proposed_choices_semantic_error.json', locals())
  logger.debug('Starting p_rule_chooser.get_proposed_choices_compile_error')
  logger.debug(
    f'There are {len(error_lines)} error lines in the semantic error\n'
    f'{json.dumps(error_lines, indent=2)}\n')

  assert len(error_lines) > 0, 'there must be at least one semantic error line'
  error_line_nums = list(error_lines.keys())
  error_line_num = error_line_nums[0]
  error_line_content = error_lines[error_line_num]

  '''
  error_line_num is 0-based line index of a trace mismatch in
  tar_program_instr, we need to get the 0-based line index in tar_main_code.
  '''
  err_line_idx = get_err_line_idx_in_tar_main_code(error_line_content, error_line_num + 1, tar_program_instr, tar_main_code)

  '''
  Depending on the locations of log statements (myexactlog), we may end up
  in a situation where there are multiple lines in `error_lines`. For example:
  {
    21: "        break;",
    22: "    }",
    23: "    var x = (x && !m) || (!x && m);"
  }
  taken from:
  ```js
          // ...
          myexactlog(4, m);
          break;
      }
      var x = (x && !m) || (!x && m);
      myexactlog(5, x);  // trace mismatch occurs here
      // ...
  ```
  In this case, we pass all error lines to get_proposed_choices_based_on_line_idxs.
  '''
  err_line_idxs = list(range(err_line_idx, err_line_idx + len(error_lines)))

  new_choices = get_proposed_choices_based_on_line_idxs(
    tar_main_code,
    err_line_idxs,
    choices_list_stack,
    map_to_exid,
    translate_dbg_history
  )
  return new_choices
