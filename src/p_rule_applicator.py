import json
import re
from typing import Dict, List, Optional, Tuple

import d_grammar_expand
import p_code_runner
import p_consts
import p_pirel
import p_subject
import p_utils


logger = p_utils.setup_logger(__name__)


# INTERNAL API
def _postprocess_src_program(translated_code: str, src_code: str, src_ann: dict) -> str:
  '''
  This function is used only for subjects that are long and require processing.
  Processing is done only after the `src_program` is instrumented by adding
  `mylog` function invocations to it. This is the case for GFG benchmark so far.
  Some subjects have really long parameters, which may slow down the instrumentation (?).
  That is why the `translation_rules_instr_src` includes a hacky translation rule
  that translates `param = *` exclusively, where `*` is a fairly large construct.
  For an example, check `GFG_ROW_WISE_COMMON_ELEMENTS_TWO_DIAGONALS_SQUARE_MATRIX.py`.
  After the translation (instrumentation) is complete, `*` should be placed back
  to the instrumented code, which is accomplished by this function.
  '''
  logger.debug('Starting p_rule_applicator._postprocess_src_program')

  regexp = re.compile(r'SOURCE_AST_IDX\((\d+)\)')
  all_matches : List[str] = regexp.findall(translated_code)
  restored_code = translated_code

  for match in all_matches:
    replaced_token = f'SOURCE_AST_IDX({match})'
    assert translated_code.count(replaced_token) == 1, f'{replaced_token} must appear once'

    ast_ann = src_ann[int(match)]
    start_point, end_point = ast_ann[:2]
    replacing_token = src_code[start_point:end_point]

    restored_code = restored_code.replace(replaced_token, replacing_token)

  return restored_code


def _postprocess_tar_program(translated_code: str, src_code: str, src_ann: dict) -> str:
  '''
  The intention of this function is similar to that of `_postprocess_src_program`.
  Please refer to that function.
  '''
  logger.debug('Starting p_rule_applicator._postprocess_tar_program')

  regexp = re.compile(r'SOURCE_AST_IDX\((\d+)\)')
  all_matches = regexp.findall(translated_code)
  restored_code = translated_code

  for match in all_matches:
    replaced_token = f'SOURCE_AST_IDX({match})'
    assert translated_code.count(replaced_token) == 1, f'{replaced_token} must appear once'

    ast_ann = src_ann[int(match)]
    start_point, end_point = ast_ann[:2]
    replacing_token = src_code[start_point:end_point]

    # transform py nested list-tuple to js array
    trans_chars = []
    is_in_string = False
    is_escaping = False
    for rep_token_char in replacing_token:
      if is_in_string:
        if rep_token_char == '\\':
          is_escaping = True
        elif is_escaping:
          is_escaping = False
        elif rep_token_char == '"':
          is_in_string = False
      else:
        if rep_token_char == '(':
          trans_chars.append('[')
          continue
        if rep_token_char == ')':
          trans_chars.append(']')
          continue
      trans_chars.append(rep_token_char)

    assert len(trans_chars) == len(replacing_token), 'py_array_to_js_array string length mismatch'

    new_replacing_token = ''.join(trans_chars)
    restored_code = restored_code.replace(replaced_token, new_replacing_token)

  return restored_code


def _run_tests(
  src_program_instr: str,
  tar_program_instr: str,
  subject: p_subject.PirelSubject,
  is_dry_run: bool
) -> Optional[dict]:
  '''
  RETURN `tar_error` - None if no error, else a dict containing error information.
  '''
  logger.debug('Starting p_rule_applicator._run_tests')

  src_log, src_error = p_code_runner.run_src_program_with_mylog(
    src_program_instr,
    subject
  )
  assert src_error is None, 'sanity check: error in running source program'
  tar_program_run, tar_log, tar_error = p_code_runner.run_tar_program_until_mylog_mismatch(
    tar_program_instr,
    subject,
    src_log,
    is_dry_run
  )
  return tar_error


def _get_instrumented_src_program(subject: p_subject.PirelSubject) -> str:
  '''
  In `src_program_instr` only the `src_test_code` is instrumented.
  "Instrumented" means that `mylog` invocations are added to the code.
  '''

  logger.debug('Starting p_rule_applicator._get_instrumented_src_program')

  if not subject.needs_instrumentation:
    logger.debug('program does not need instrumentation')
    logger.debug('will use `src_program` as `src_program_instr`')
    assert subject.translation_rules_instr_src is None, 'sanity check'
    assert subject.translation_rules_instr_tar is None, 'sanity check'
    return subject.src_program

  if subject.is_mylog_inserted:
    logger.debug('program needs instrumentation, but it already is instrumented')
    logger.debug('will use `src_program` as `src_program_instr`')
    assert subject.translation_rules_instr_src is None, 'sanity check'
    assert subject.translation_rules_instr_tar is None, 'sanity check'
    return subject.src_program

  logger.debug('program needs instrumentation, starting it now.')

  assert subject.translation_rules_instr_src is not None, 'sanity check'
  assert subject.translation_rules_instr_tar is not None, 'sanity check'

  # 1 translate `src_program` with `translation_rules_instr_src`
  # actions of this operations must be restored by postprocessing function
  # refer to `paramhack` and `_postprocess_src_program`
  duoglot_translate_result = p_pirel.duoglot_translate_wrapper(
    src_code=subject.src_program,
    src_lang=subject.src_lang,
    tar_lang=subject.src_lang,
    trans_rules=subject.translation_rules_instr_src,
    auto_backward=subject.auto_backward,
    choices=subject.choices,
    subject_name=subject.name,
    skip_template_extraction=True
  )
  src_program_instr_raw = duoglot_translate_result['tar_code']
  src_program_ann = duoglot_translate_result['src_ann']

  # 2 restore `param` in `src_program_instr_raw` (if needed)
  if subject.is_long_requires_processing:
    logger.debug('src_program is long and requires processing')
    src_program_instr_raw = _postprocess_src_program(src_program_instr_raw, subject.src_program, src_program_ann)

  # 3 replace each MYLOG_COUNTER with ints in range(0,)
  _spir_chunks = src_program_instr_raw.split('MYLOG_COUNTER')
  _interleaved_list = []
  for i in range(len(_spir_chunks)):
    _interleaved_list.append(_spir_chunks[i])
    if i < len(_spir_chunks) - 1:
      _interleaved_list.append(str(i))
  src_program_instr_raw_2 = ''.join(_interleaved_list)

  # 4 split the program into test, main, test call code snippets
  _spir2_chunks = src_program_instr_raw_2.split(p_consts.TEST_MAIN_CALL_DELIMITER)
  # NOTE this is an unexpected assertion
  assert len(_spir2_chunks) == 3, 'sanity check: src_program_instr should be 3 parts'
  src_test_code_instr_raw, src_main_code_instr_raw, src_test_call_code_raw = _spir2_chunks

  # 5 replace `mylog` invocations with `myexactlog`
  src_test_code_instr = src_test_code_instr_raw.replace('mylog(2', 'myexactlog(2')
  src_test_code_instr = src_test_code_instr.replace('mylog(1', 'myexactlog(1')
  src_test_code_instr = src_test_code_instr.replace('mylog(3', 'myexactlog(3')

  # 5 remove lines starting with 'mylog' from `src_main_code_raw`
  # this is done to remove instrumentation from `src_main_code`
  src_main_code = '\n'.join([line for line in src_main_code_instr_raw.split('\n') if not line.strip().startswith('mylog')])
  logger.debug("INFO: removed 'mylog' instrumentation in goldfunc (if any).")

  src_program_instr = f'\n{p_consts.TEST_MAIN_CALL_DELIMITER}\n'.join([src_test_code_instr, src_main_code, src_test_call_code_raw])
  return src_program_instr


def _get_instrumented_tar_program_plausible(src_program_instr: str, subject: p_subject.PirelSubject) -> str:
  ''''''
  logger.debug('Starting p_rule_applicator._get_instrumented_tar_program_plausible')

  # 1 split `src_program_instr` into test, main, test call code snippets
  src_test_code_instr, src_main_code, src_test_call_code = None, None, None
  if subject.is_three_split:
    logger.debug('`src_program` is three split')
    _spi_chunks = src_program_instr.split(p_consts.TEST_MAIN_CALL_DELIMITER)
    assert len(_spi_chunks) == 3, 'sanity check: src_program_instr should be 3 parts'
    src_test_code_instr = _spi_chunks[0]
    src_main_code = _spi_chunks[1]
    src_test_call_code = _spi_chunks[2]
  else:
    logger.debug('`src_program` is not three split, will use `src_program_instr` as `src_main_code`')
    logger.debug('`src_test_code_instr` is None and `src_test_call_code` is None')
    src_main_code = src_program_instr

  # 2 get corresponding instrumented test code and test call code
  tar_test_code_instr = _get_instrumented_tar_test_code(src_test_code_instr, subject)
  tar_test_call_code = _get_tar_test_call_code(src_test_call_code)

  # 3 loop to get exhaustive translation of main code
  choices_history = []
  current_choices = subject.choices
  iteration = 1

  logger.debug(
    'Starting a loop to exhaustively translate `src_program_instr` '
    'with different combinations of translation rules'
  )

  while True:
    logger.debug(f'_get_instrumented_tar_program_plausible.iteration {iteration}')
    iteration += 1

    tar_main_code, map_to_exid, translate_dbg_history = _get_tar_main_code(src_main_code, current_choices, subject)
    tar_program_instr = _concatenate_tar_snippets(tar_test_code_instr, tar_main_code, tar_test_call_code, subject)
    tar_error = _run_tests(src_program_instr, tar_program_instr, subject, is_dry_run=False)

    if tar_error is None:
      logger.debug('GOOD: no error in running tests')
      break
    logger.debug('BAD: error in running tests')

    proposed_choices = _get_proposed_choices(
      tar_program_instr,
      tar_main_code,
      tar_error,
      current_choices,
      choices_history,
      map_to_exid,
      translate_dbg_history
    )

    logger.debug(f'proposed choices: {json.dumps(proposed_choices, indent=2)}')

    choices_history.append(proposed_choices)
    current_choices = proposed_choices

  return tar_program_instr


def _get_deinstrumented_tar_program_plausible(src_program_instr: str, subject: p_subject.PirelSubject) -> str:
  logger.debug('Starting p_rule_applicator._get_deinstrumented_tar_program')
  tar_program_plausible_instr = _get_instrumented_tar_program_plausible(src_program_instr, subject)

  if not subject.needs_instrumentation:
    logger.debug('program does not need deinstrumentation')
    assert subject.translation_rules_instr_src is None, 'sanity check'
    assert subject.translation_rules_instr_tar is None, 'sanity check'
    return tar_program_plausible_instr

  if subject.is_mylog_inserted:
    logger.debug('program needs instrumentation, but it already is instrumented')
    assert subject.translation_rules_instr_src is None, 'sanity check'
    assert subject.translation_rules_instr_tar is None, 'sanity check'
    return tar_program_plausible_instr

  assert subject.translation_rules_instr_src is not None, 'sanity check'
  assert subject.translation_rules_instr_tar is not None, 'sanity check'

  # 1 translate `tar_program_plausible_instr` with `translation_rules_instr_tar`
  logger.debug('deinstrumenting `tar_program_plausible_instr`')
  duoglot_translate_result = p_pirel.duoglot_translate_wrapper(
    src_code=tar_program_plausible_instr,
    src_lang=subject.tar_lang,
    tar_lang=subject.tar_lang,
    trans_rules=subject.translation_rules_instr_tar,
    auto_backward=subject.auto_backward,
    choices=subject.choices,
    subject_name=subject.name,
    skip_template_extraction=True
  )
  tar_program_plausible_deinstr = duoglot_translate_result['tar_code']
  tar_program_plausible_instr_ann = duoglot_translate_result['src_ann']

  # 2 restore `param` in `tar_program_plausible_deinstr` (if needed)
  if subject.is_long_requires_processing:
    logger.debug('tar_program_plausible is long and requires processing')
    tar_program_plausible_deinstr = _postprocess_tar_program(
      tar_program_plausible_deinstr,
      tar_program_plausible_instr,
      tar_program_plausible_instr_ann
    )

  return tar_program_plausible_deinstr


def _get_instrumented_tar_test_code(src_test_code_instr: Optional[str], subject: p_subject.PirelSubject) -> Optional[str]:
  '''
  Ideally, this function is run only once.
  '''
  logger.debug(f'Starting p_rule_applicator._get_instrumented_tar_test_code')

  if not subject.is_three_split:
    logger.debug('`src_program` is not three split: tar_test_code is None')
    assert src_test_code_instr is None, 'sanity check'
    return None

  # translate `src_test_code_instr` using `translation_rules_test_code`
  duoglot_translate_result = p_pirel.duoglot_translate_wrapper(
    src_code=src_test_code_instr,
    src_lang=subject.src_lang,
    tar_lang=subject.tar_lang,
    trans_rules=subject.translation_rules_test_code,
    auto_backward=subject.auto_backward,
    choices=subject.choices,
    subject_name=subject.name,
    skip_template_extraction=True
  )
  tar_test_code_instr = duoglot_translate_result['tar_code']
  src_test_code_instr_ann = duoglot_translate_result['src_ann']

  if subject.is_long_requires_processing:
    logger.debug('src_program is long and requires processing')
    tar_test_code_instr = _postprocess_tar_program(tar_test_code_instr, src_test_code_instr, src_test_code_instr_ann)

  return tar_test_code_instr


def _get_tar_test_call_code(src_test_call_code: str) -> str:
  '''
  For the moment, just use `src_test_call_code` as `tar_test_call_code`,
  because Python and JavaScript function call syntax is the same.
  '''
  return src_test_call_code


def _get_tar_main_code(src_main_code: str, choices: dict, subject: p_subject.PirelSubject) -> Tuple[str, Dict[int, List[dict]], List[dict]]:
  '''
  Translate `src_main_code` using `translation_rules_main_code` and `choices`.
  '''
  logger.debug('Starting p_rule_applicator._get_tar_main_code')
  logger.debug('translating `src_main_code` to target language using choices:')
  logger.debug(json.dumps(choices, indent=2))

  assert subject.translation_rules_main_code is not None, \
    'translation rules for main code must be provided'

  # TODO consider a case when `choices` leads to a problematic slot.
  # i.e. a slot for which we don't have a translation rule.
  try:
    duoglot_translate_result = p_pirel.duoglot_translate_wrapper(
      src_code=src_main_code,
      src_lang=subject.src_lang,
      tar_lang=subject.tar_lang,
      trans_rules=subject.translation_rules_main_code,
      auto_backward=subject.auto_backward,
      choices=choices,
      subject_name=subject.name,
      skip_template_extraction=True
    )
  except d_grammar_expand.TranslationRuleNotFoundException as exc:
    templates_dict = exc.get_templates_dict()
    logger.warning(f'Caught TranslationRuleNotFoundException: {exc}')
    logger.warning(f'templates_dict: {json.dumps(templates_dict, indent=2)}')
    raise

  tar_main_code = duoglot_translate_result['tar_code']
  map_to_exid = duoglot_translate_result['map_to_exid']
  translate_dbg_history = duoglot_translate_result['dbg_history']
  return tar_main_code, map_to_exid, translate_dbg_history


def _concatenate_tar_snippets(
  tar_test_code_instr: Optional[str],
  tar_main_code: str,
  tar_test_call_code: Optional[str],
  subject: p_subject.PirelSubject
) -> str:
  '''
  Combine `tar_test_code_instr`, `tar_main_code`, and `tar_test_call_code`
  into a single string.
  '''
  if not subject.is_three_split:
    assert tar_test_code_instr is None, 'sanity check'
    assert tar_test_call_code is None, 'sanity check'
    return tar_main_code
  assert tar_test_code_instr is not None, 'sanity check'
  assert tar_test_call_code is not None, 'sanity check'
  return f'\n{p_consts.TEST_MAIN_CALL_DELIMITER}\n'.join([tar_test_code_instr, tar_main_code, tar_test_call_code])


def _get_proposed_choices(
  tar_program_instr: str,
  tar_main_code: str,
  tar_error: dict,
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

    logger.debug('Starting p_rule_applicator._get_proposed_choices.__find_next_unique_choices')

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

    raise RuntimeError('No unique choices found')

  logger.debug('Starting p_rule_applicator._get_proposed_choices')

  error_msg = tar_error['error_msg']  # e.g. 'SyntaxError: invalid syntax'
  error_type = tar_error['error_type']  # e.g. 'SyntaxError'
  line_content = tar_error['line_content']  # code snippet at the line of error in `tar_program_instr`
  err_file_tpi = tar_error['line_num'][0]  # absolute path to the file where the error occurred
  err_line_tpi = tar_error['line_num'][1]  # line number in the file where the error occurred

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


# API
def apply_translation_rules(subject: p_subject.PirelSubject) -> str:
  '''
  Apply the translation rules to the source program.
  Equivalent to index_bench.js::runBenchmarkHandler

  RETURN `tar_program_deinstr` - the target program that is deinstrumented.
  '''
  p_utils.log_json_time(f'{subject.name}_args-apply_translation_rules.json', locals())
  logger.info('Starting p_rule_applicator.apply_translation_rules (a la DuoGlot)')

  src_program_instr = _get_instrumented_src_program(subject)
  tar_program_deinstr = _get_deinstrumented_tar_program_plausible(src_program_instr, subject)

  return tar_program_deinstr


# USAGE
def usage_apply_translation_rules():
  subject_config = p_subject.PirelSubject.from_file_config(p_consts.ROOT_DIR / 'conf' / 'pirel-subject' / 'test.yaml')
  tar_program_plausible = apply_translation_rules(subject_config)
  logger.info(f'Plausible target program:\n{tar_program_plausible}')


# TEST HARNESSES
def _test_apply_translation_rules():
  '''
  def apply_translation_rules(subject: p_subject.PirelSubject) -> str:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_apply_translation_rules_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  subject = p_subject.PirelSubject.from_dict_config(json.loads(args_dict['subject']))
  tar_program_deinstr = apply_translation_rules(subject)
  print(f'Plausible target program:\n{tar_program_deinstr}')


def _test_postprocess_src_program():
  translated_code = p_utils.read_text('temporary_validator_translated_code.py')
  src_code = p_utils.read_text('temporary_validator_src_code.py')
  src_ann : dict = p_utils.read_json('temporary_validator_src_ann.json')
  # Convert all keys of src_ann from str to int
  src_ann = {int(k): v for k, v in src_ann.items()}
  result = _postprocess_src_program(translated_code, src_code, src_ann)
  print(result)


if __name__ == '__main__':
  # usage_apply_translation_rules()
  _test_apply_translation_rules()
  # _test_postprocess_src_program()
