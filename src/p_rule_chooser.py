import json
from typing import List, Dict, Set, Tuple

import p_utils


logger = p_utils.setup_logger(__name__)


class NoUniqueChoicesError(RuntimeError): pass


def are_choices_lists_equal_astnode(
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


def are_choices_list_equal_step(
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


def has_been_chosen_before(
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
      if are_choices_list_equal_step(choices_list, choices_list_hist_elem):
        return True

    elif choice_type == 'ASTNODE':
      if are_choices_lists_equal_astnode(choices_list, choices_list_hist_elem):
        return True

  return False


def get_updated_choices_list_astnode(
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


def get_updated_choices_list_step(
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


def get_next_unique_choices(
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
        updated_choices_list = get_updated_choices_list_step(current_choices_list, rel_alt_step, new_choice_idx)
        new_choices = {
          'type': 'STEP',
          'choices_list': updated_choices_list
        }
        is_in_history = has_been_chosen_before(new_choices, choices_history)
        if not is_in_history:
          return new_choices
    raise NoUniqueChoicesError('No unique choices found')

  elif choice_type == 'ASTNODE':
    for info_dict in rel_alt_step_infos.values():
      rel_next_choices_count = info_dict['next_choices_count']
      rel_current_choice_idx = info_dict['current_choose_idx']
      rel_current_range_info = info_dict['current_range_info']

      new_choice_idxs = list(range(rel_next_choices_count))
      for new_choice_idx in new_choice_idxs:
        if new_choice_idx == rel_current_choice_idx:
          continue
        updated_choices_list = get_updated_choices_list_astnode(current_choices_list, rel_current_range_info, new_choice_idx)
        new_choices = {
          'type': 'ASTNODE',
          'choices_list': updated_choices_list
        }
        is_in_history = has_been_chosen_before(new_choices, choices_history)
        if not is_in_history:
          return new_choices
    raise NoUniqueChoicesError('No unique choices found')


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
  assert line_content in expected_line, "Expected line doesn't contain error line content."

  return err_line_idx


def get_proposed_choices_compile_error(
  tar_program_instr: str,
  tar_main_code: str,
  tar_error_dict: dict,
  current_choices: dict,
  choices_history: List[dict],
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

  NOTE
  <choices_history> -> List[<choices>]
  <choices> -> {
    'type': {"STEP", "ASTNODE"},
    'choices_list': <choices_list>
  }
  <choices_list> -> List[<choice_elem>]
  <choices_list>: (list of mappings of AST nodes to rules to translate them)
  <choice_elem> -> Tuple(
    <node_identifier>,
    <choice_idx>
  )
  <node_identifier> -> OR(<range_info>, <alt_step>)
  <range_info> -> Tuple(
    (AST node id),
    (start index of AST range),
    (end index of AST range)
  )
  <alt_step>: (id of alt object that was created for expansion)
  <choice_idx>: (index of a rule to choose at that node)
  aliases(choices, current_choices, proposed_choices, subject.choices, new_choices)
  aliases(choices_list, updated_choices_list, new_choices_list)
  '''

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

  msg = (
    f'there was an error running `tar_program_instr`\n'
    f'{error_type} "{error_msg}" on line {err_line_idx + 1} of "{line_content}"\n')
  logger.debug(msg)

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
  _RELATED_WINDOW_SIZE = 1
  exids_err_line : List[int] = list(sorted(line_idx_to_exids[err_line_idx]))
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
        'ex_id': mod_dbg_history[rel_alt_step]['ex_id'],
        'current_rule_id': mod_dbg_history[rel_alt_step]['current_rule_id'],
        'current_range_info': mod_dbg_history[rel_alt_step]['current_range_info']
      }

  new_choices = get_next_unique_choices(rel_alt_step_infos, current_choices, choices_history)
  return new_choices
