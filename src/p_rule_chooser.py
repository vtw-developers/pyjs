from typing import List, Dict, Tuple

import p_utils


logger = p_utils.setup_logger(__name__)


class NoUniqueChoicesError(RuntimeError): pass


def get_proposed_choices(
  tar_program_instr: str,
  tar_main_code: str,
  tar_error_dict: dict,
  current_choices: dict,
  choices_history: List[dict],
  map_to_exid: Dict[int, List[dict]],
  translate_dbg_history: List[dict],
) -> dict:

  def __get_err_line_idx_in_tar_main_code(
    line_content: str,
    err_line_tpi: int,
    tar_program_instr: str,
    tar_main_code: str
  ) -> int:
    '''
    Get the index of the line in `tar_main_code` that corresponds to the error line.
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

  def __get_char_pos_to_line_pos_map_lists(main_code_lines: List[str]) -> Tuple[List[int], List[int]]:
    line_map = []
    column_map = []
    for i, line in enumerate(main_code_lines):
      for j, _ in enumerate(line):
        line_map.append(i)
        column_map.append(j)
      # the newline char
      line_map.append(i)
      column_map.append(-1)
    return line_map, column_map

  def __find_next_unique_choices(
    related_alt_step_infos: Dict[int, tuple],
    current_choices: dict,
    choices_history: List[dict]
  ):

    def ___step_choices_list_update(
      choices_list: list,
      step: int,
      update_ch: int
    ):
      new_choices = []
      is_set = False
      for choice in choices_list:
        if choice[0] == step:
          is_set = True
          if update_ch != 0:
            new_choices.append([step, update_ch])
        else:
          if choice[0] > step:
            continue
          else:
            new_choices.append(choice)
      if not is_set and update_ch != 0:
        new_choices.append([step, update_ch])
      return new_choices

    def ___astnode_choices_list_update(
      choices_list: list,
      current_range_key: Tuple[int],
      update_ch: int
    ):
      new_choices = []
      is_set = False
      c_astid, c_start, c_end = current_range_key
      for choice in choices_list:
        astid, start, end = choice[0]
        if c_astid == astid and c_start == start and c_end == end:
          is_set = True
          if update_ch != 0:
            new_choices.append([current_range_key, update_ch])
        else:
          new_choices.append(choice)
      if not is_set and update_ch != 0:
        new_choices.append([current_range_key, update_ch])
      return new_choices

    def ___choices_any_duplicate(
      choices: list,
      choices_history: List[dict]
    ):
      type_ = choices['type']
      choices_list = choices['choices_list']
      for cmp_choices in choices_history:
        cmp_type = cmp_choices['type']
        assert cmp_type == type_, '___choices_any_duplicate boolean check FAILED. Choices are of different type.'
        cmp_choices_list = cmp_choices['choices_list']
        assert type_ in ['STEP', 'ASTNODE'], f'___choices_any_duplicate unknown type: {type_}'
        if type_ == 'STEP':
          if ___step_choices_list_compare(choices_list, cmp_choices_list):
            return True
        elif type_ == 'ASTNODE':
          if ___astnode_choices_list_compare(choices_list, cmp_choices_list):
            return True
      return False

    def ___step_choices_list_compare(
      choices_list1: list,
      choices_list2: list
    ):
      choices1_dict = {}
      for step, ch in choices_list1:
        assert step not in choices1_dict, f'___step_choices_list_compare invalid choices_list1: duplicated step: {choices1_dict}'
        if ch != 0:
          choices1_dict[step] = ch
      for step, ch in choices_list2:
        if step in choices1_dict:
          if choices1_dict[step] == ch:
            choices1_dict[step] = -1
            continue
          else:
            return False
        else:
          if ch == 0:
            continue
          else:
            return False
      for step in choices1_dict:
        if choices1_dict[step] != -1:
          return False
      return True

    def ___astnode_choices_list_compare(
      choices_list1: list,
      choices_list2: list
    ):
      choices1_dict = {}
      for range_key, ch in choices_list1:
        astid, start, end = range_key
        range_key_str = f'{astid}-{start}-{end}'
        if range_key_str in choices1_dict:
          raise ValueError(f'_astnode_choices_list_compare invalid choices_list1: duplicated range_key: {choices1_dict}')
        if ch != 0:
          choices1_dict[range_key_str] = ch
      for range_key, ch in choices_list2:
        astid, start, end = range_key
        range_key_str = f'{astid}-{start}-{end}'
        if range_key_str in choices1_dict:
          if choices1_dict[range_key_str] == ch:
            choices1_dict[range_key_str] = -1
            continue
          else:
            return False
        else:
          if ch == 0:
            continue
          else:
            return False
      for range_key_str in choices1_dict:
        if choices1_dict[range_key_str] != -1:
          return False
      return True

    logger.debug('Starting p_rule_chooser.get_proposed_choices.__find_next_unique_choices')

    type_ = current_choices['type']
    choices_list : list = current_choices['choices_list']
    assert type_ in ['STEP', 'ASTNODE'], f'__find_next_unique_choices unknown type: {type_}'

    if type_ == 'STEP':
      for alt_step, info in related_alt_step_infos.items():
        chcount, current_ch = info[:2]
        for i in range(chcount):
          if i == current_ch:
            continue
          updated_choices_list = ___step_choices_list_update(choices_list, int(alt_step), i)
          new_choices = {
            'type': 'STEP',
            'choices_list': updated_choices_list
          }
          if not ___choices_any_duplicate(new_choices, choices_history):
            return new_choices
    elif type_ == 'ASTNODE':
      for alt_step, info in related_alt_step_infos.items():
        chcount, current_ch = info[:2]
        current_range_key = info[5]
        for i in range(chcount):
          if i == current_ch:
            continue
          updated_choices_list = ___astnode_choices_list_update(choices_list, current_range_key, i)
          new_choices = {
            'type': 'ASTNODE',
            'choices_list': updated_choices_list
          }
          if not ___choices_any_duplicate(new_choices, choices_history):
            return new_choices

    raise NoUniqueChoicesError('No unique choices found')

  logger.debug('Starting p_rule_chooser.get_proposed_choices')

  error_msg = tar_error_dict['error_msg']  # e.g. 'SyntaxError: invalid syntax'
  error_type = tar_error_dict['error_type']  # e.g. 'SyntaxError'
  line_content = tar_error_dict['line_content']  # code snippet at the line of error in `tar_program_instr`
  err_file_tpi = tar_error_dict['line_num'][0]  # absolute path to the file where the error occurred
  err_line_tpi = tar_error_dict['line_num'][1]  # line number in the file where the error occurred

  SUPPORTED_ERROR_TYPES = ['SyntaxError:', 'ReferenceError:', 'TypeError:']
  assert error_type in SUPPORTED_ERROR_TYPES, f'unsupported error type {error_type}'

  logger.debug(f'there was an error running `tar_program_instr`:')
  logger.debug(f'on line {err_line_tpi} in file {err_file_tpi}')
  logger.debug(f'{error_type}: {error_msg}\n{line_content}')

  err_line_idx = __get_err_line_idx_in_tar_main_code(line_content, err_line_tpi, tar_program_instr, tar_main_code)
  logger.debug(f'tar_main_code:\n{tar_main_code}')
  logger.debug(f'Error: `{error_type}` at line {err_line_idx + 1} (idx={err_line_idx})')
  logger.debug(f'Buggy line: `{line_content}`')

  main_code_lines = tar_main_code.split('\n')
  line_map, column_map = __get_char_pos_to_line_pos_map_lists(main_code_lines)

  # populate `exids_by_line_idx`
  exids_by_line_idx : Dict[int, dict] = {}
  for exid_err_line, ranges_of_exid in map_to_exid.items():
    for range_of_exid in ranges_of_exid:
      ch_start_idx, ch_end_idx = range_of_exid['range']

      assert tar_main_code[ch_start_idx:ch_end_idx] == range_of_exid['str'], \
        f"code_map is wrong! {tar_main_code[ch_start_idx:ch_end_idx]} != {range_of_exid['str']}"

      line_start_idx : int = line_map[ch_start_idx]
      line_end_idx : int = line_map[ch_end_idx]

      assert line_start_idx == line_end_idx, 'unhandled case: a str across multiple lines'

      assert range_of_exid['str'] in main_code_lines[line_start_idx], \
        f"code_map processing code is wrong! {main_code_lines[line_start_idx]} does not contain {range_of_exid['str']}"

      exids_by_line_idx.setdefault(line_start_idx, {})[exid_err_line] = True

  # process `translate_dbg_history`
  alt_step_to_choices_exid : List[dict] = []
  exid_to_alt_step_choices : Dict[int, dict] = {}
  for elem in translate_dbg_history:
    assert elem['alt_step'] - 1 == len(alt_step_to_choices_exid), 'sanity check'
    push_obj = {
      'alt_step': elem['alt_step'],
      'next_choices_count': elem['next_choices_status']['count'],
      'next_choices_all_known': elem['next_choices_status']['done'],
      'ex_id': elem['dbg_info']['ex_id'],
      'current_choose_idx': elem['dbg_info']['notes']['choose_idx'],
      'current_rule_id': elem['dbg_info']['notes']['rule_id'],
      'current_range_key': elem['range_info']
    }
    alt_step_to_choices_exid.append(push_obj)
    exid_to_alt_step_choices[push_obj['ex_id']] = push_obj

  # implementation of this feature is skipped, because it is not used
  # by DuoGlot for default benchmark configurations.
  _can_skip_dict = {}

  exids_err_line : Dict[int, bool] = exids_by_line_idx[err_line_idx]
  related_alt_step_infos : Dict[int, tuple] = {}
  RELATED_WINDOW_SIZE = 1

  for exid_err_line in exids_err_line:
    alt_step_info = exid_to_alt_step_choices[exid_err_line]
    alt_step = alt_step_info['alt_step']

    for i in range(alt_step - 1 - RELATED_WINDOW_SIZE, alt_step):
      if i <= 0 or i >= len(alt_step_to_choices_exid):
        continue
      if alt_step_to_choices_exid[i-1]['next_choices_count'] > 1:
        related_alt_step_id = alt_step_to_choices_exid[i]['alt_step']
        rule_id = alt_step_to_choices_exid[i]['current_rule_id']
        is_skip_allowed = rule_id in _can_skip_dict
        related_alt_step_infos[related_alt_step_id] = (
          alt_step_to_choices_exid[i-1]['next_choices_count'],
          alt_step_to_choices_exid[i]['current_choose_idx'],
          alt_step_to_choices_exid[i]['ex_id'],
          rule_id,
          is_skip_allowed,
          alt_step_to_choices_exid[i]['current_range_key']
        )

  new_choices = __find_next_unique_choices(related_alt_step_infos, current_choices, choices_history)
  return new_choices
