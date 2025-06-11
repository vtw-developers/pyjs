import json
import re
from typing import Dict, List, Optional, Tuple

import d_grammar_expand
import p_code_runner
import p_consts
import p_pirel
import p_rule_chooser
import p_subject
import p_utils


logger = p_utils.setup_logger(__name__)


class UnknownTypeInTracesError(RuntimeError): pass
class SrcTestScriptError(RuntimeError): pass
class TarTestScriptError(RuntimeError):
  def __init__(self, tar_error_dict: dict):
    super().__init__('Error running tar test script')
    self.tar_error_dict = tar_error_dict
  def __str__(self):
    return f'TarTestScriptError: {json.dumps(self.tar_error_dict, indent=2)}'
class TraceMismatchError(RuntimeError):
  def __init__(self, error_lines: dict):
    super().__init__('Trace mismatch between src and tar test scripts')
    self.error_lines = error_lines
  def __str__(self):
    return f'TraceMismatchError: {json.dumps(self.error_lines, indent=2)}'
class TRuleNotFoundError(RuntimeError): pass


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


def _compare_traces(src_trace: list, tar_trace: list) -> bool:
  '''
  Compare the traces from the source and target programs.
  For more information, refer to
  1. run_src_test_script and run_tar_test_script in p_code_runner.py.
  2. myexactlog implementations for src and tar languages.
  '''

  # base case: lengths must be equal
  if len(src_trace) != len(tar_trace):
    return False

  # base case: types must be same
  type1, type2 = src_trace[0], tar_trace[0]
  if type1 != type2:
    return False

  assert type1 == type2, f'compare_traces: {type1} != {type2}'

  # base case: types are null
  if type1 == 'null':
    return True

  # base case: types are bool
  if type1 == 'bool':
    val1, val2 = src_trace[1], tar_trace[1]
    return val1 == val2

  # base case: types are string
  if type1 == 'string':
    len1, len2 = src_trace[1], tar_trace[1]
    str1, str2 = src_trace[2], tar_trace[2]
    return len1 == len2 and str1 == str2

  # base case: types are num
  if type1 == 'number':
    val1, val2 = src_trace[1], tar_trace[1]
    return p_utils.are_equal(val1, val2)

  # recurse
  if type1 in ['list', 'set', 'dict']:
    len1, len2 = src_trace[1], tar_trace[1]
    if len1 != len2:
      return False
    list1, list2 = src_trace[2], tar_trace[2]
    for ch1, ch2 in zip(list1, list2):
      child_res = _compare_traces(ch1, ch2)
      if not child_res:
        return False
    return True

  if type1 == 'unknown':
    logger.warning('_compare_traces: unknown type')
    len1, len2 = src_trace[1], tar_trace[1]
    str1, str2 = src_trace[2], tar_trace[2]
    return len1 == len2 and str1 == str2

  raise UnknownTypeInTracesError(f'Unknown type in _compare_traces: "{type1}"')


def _get_trace_mismatch_idx(src_trace: list, tar_trace: list) -> int:
  '''
  Given two traces, find the first index where they differ.
  If they are identical, return None.
  PRE: traces are not identical.
  RAISE: RuntimeError if traces are identical.
  '''
  src_trace_type = src_trace[0]
  tar_trace_type = tar_trace[0]
  assert src_trace_type == 'list' and tar_trace_type == 'list', 'traces must be lists'

  src_trace_len = src_trace[1]
  tar_trace_len = tar_trace[1]
  assert src_trace_len == tar_trace_len, 'traces of different lengths are not supported'

  src_trace_entries = src_trace[2]
  tar_trace_entries = tar_trace[2]

  for idx, (src_te, tar_te) in enumerate(zip(src_trace_entries, tar_trace_entries)):
    src_te_type = src_te[0]
    tar_te_type = tar_te[0]
    assert src_te_type == 'list' and tar_te_type == 'list', 'trace entries must be lists'

    '''
    Each entry in the traces must be a list of at least 2 elements.
    Why? In order to extract location of a semantic error (it causes
    a trace mismatch), each log statement (myexactlog, print) must
    have been indexed by being inserted its index as a first argument.
    That's why the trace entries must be at least 2 elements long.
    '''
    src_te_len = src_te[1]
    tar_te_len = tar_te[1]
    assert src_te_len >= 2 and tar_te_len >= 2, 'trace entries must have at least 2 elements'
    trace_entries_identical = _compare_traces(src_te, tar_te)
    if not trace_entries_identical:
      return idx

  # if we reach here, it means that all entries are identical
  raise RuntimeError('Traces must be different')


def _get_log_statement_idx(src_trace: list, tar_trace: list, trace_idx: int) -> int:
  '''
  Given two traces and a trace index, find the log statement index under that trace index.
  Log statement indices are 1-based.

  Sample trace:
  ["list", 1,
    [
      [
        "list", 2, [
          ["number", 5],
          ["number", 2]
        ]
      ]
    ]
  ]

  NOTE both src_trace and tar_trace are used to cross-check the log statement index.
  '''

  src_trace_entries = src_trace[2]
  tar_trace_entries = tar_trace[2]

  assert len(src_trace_entries) == len(tar_trace_entries), 'trace entries must be of the same length'
  assert trace_idx < len(src_trace_entries), 'trace index must be less than trace entries length'
  assert trace_idx < len(tar_trace_entries), 'trace index must be less than trace entries length'

  src_trace_entry = src_trace_entries[trace_idx]
  tar_trace_entry = tar_trace_entries[trace_idx]

  src_trace_entry_type = src_trace_entry[0]
  tar_trace_entry_type = tar_trace_entry[0]
  assert src_trace_entry_type == 'list' and tar_trace_entry_type == 'list', 'trace entries must be lists'

  src_trace_arg_len = src_trace_entry[1]
  tar_trace_arg_len = tar_trace_entry[1]
  assert src_trace_arg_len >= 2 and tar_trace_arg_len >= 2, 'trace entries must have at least 2 arguments logged'

  src_trace_args = src_trace_entry[2]
  tar_trace_args = tar_trace_entry[2]
  src_trace_arg1 = src_trace_args[0]
  tar_trace_arg1 = tar_trace_args[0]
  src_trace_arg1_type = src_trace_arg1[0]
  tar_trace_arg1_type = tar_trace_arg1[0]
  assert src_trace_arg1_type == 'number' and tar_trace_arg1_type == 'number', 'trace entry first argument must be a number'

  src_trace_arg1_value = src_trace_arg1[1]
  tar_trace_arg1_value = tar_trace_arg1[1]
  assert isinstance(src_trace_arg1_value, int) and isinstance(tar_trace_arg1_value, int), 'trace entry first argument must be an int'
  assert src_trace_arg1_value == tar_trace_arg1_value, 'trace entry first argument must be equal in both traces'

  # doesn't matter which trace we use, they are the same
  return src_trace_arg1_value


def _get_error_lines(tar_program_instr: str, mismatched_log_stat_idx: int) -> Dict[int, str]:
  '''
  Given a tar_program_instr (instrumented tar program) and a mismatched log statement index,
  return the line numbers right before the mismatched log statement.
  RETURN a dictionary with line numbers as keys and lines as values:
  {
    12: "        n += 'n';"
  }
  NOTE line numbers are 0-based.
  '''

  def __find_text(stripped_lines: List[str], text: str) -> int:
    '''
    RETURN -1 if not found.
    '''
    for idx, line in enumerate(stripped_lines):
      if line.startswith(text):
        return idx
    return -1

  def __find(stripped_lines: List[str], log_stat_idx: int) -> int:
    '''
    Return a 0-based index
    '''
    assert log_stat_idx >= 0, 'log_stat_idx must be >= 0'
    assert log_stat_idx < len(stripped_lines), 'log_stat_idx must be less than the number of stripped lines'

    # since log statement indices are 1-based, and requested
    # `log_stat_idx == 0`, we need to return the index of `function f_gold`
    if log_stat_idx == 0:
      fgold_def_idx = __find_text(stripped_lines, 'function f_gold')
      assert fgold_def_idx != -1, 'function f_gold definition must be present'
      return fgold_def_idx

    # either `console.log({log_stat_idx}` or `myexactlog({log_stat_idx}` must be searched
    myexactlog_idx = __find_text(stripped_lines, f'myexactlog({log_stat_idx}')
    print_idx = __find_text(stripped_lines, f'console.log({log_stat_idx}')
    if myexactlog_idx == -1 and print_idx == -1:
      return -1
    return myexactlog_idx if myexactlog_idx != -1 else print_idx

  assert mismatched_log_stat_idx >= 1, 'mismatched_log_stat_idx must be >= 1'

  # split into stripped lines
  lines = tar_program_instr.split('\n')
  stripped_lines = [line.strip() for line in lines]

  '''
  In order to find buggy lines not only we need the mismatched log statement index,
  but also the log statement right before it (the one at which there was no mismatch).
  Buggy lines would lie in between them two.
  '''
  mismatch_line_idx = __find(stripped_lines, mismatched_log_stat_idx)
  mismatch_line_idx_before = __find(stripped_lines, mismatched_log_stat_idx - 1)
  assert mismatch_line_idx != -1, f'mismatched_log_stat_idx {mismatched_log_stat_idx} not found in stripped lines'
  assert mismatch_line_idx_before != -1, f'mismatched_log_stat_idx {mismatched_log_stat_idx - 1} not found in stripped lines'

  error_line_idxs = list(range(mismatch_line_idx_before + 1, mismatch_line_idx))
  error_lines = {line_idx: lines[line_idx] for line_idx in error_line_idxs}

  return error_lines


def _extract_err_lines_from_trace_mismatch(
  src_trace: list,
  tar_program_instr: str,
  tar_trace: list
) -> dict:
  '''
  This function assumes that there is a trace mismatch betwenn
  src and tar test scripts. Trace mismatch points to a semantic error
  in the tar test script since we assume that src test script is correct.
  This function returns line numbers (0-based) and line contents
  at which a semantic error might have occured. By having this information,
  we can choose alternative translation rules to fix the semantic error.
  '''

  '''
  A trace mismatch index is an index in the traces where the entries differ.
  Using this index, we can find which log statement caused the trace mismatch.
  '''
  trace_mismatch_idx = _get_trace_mismatch_idx(src_trace, tar_trace)

  '''
  A mismatched log statement index is an index of the log statement that caused
  the trace mismatch. Log statement indices are 1-based.
  '''
  mismatched_log_stat_idx = _get_log_statement_idx(src_trace, tar_trace, trace_mismatch_idx)

  '''
  Error lines is a dictionary where keys are line numbers (0-based) and values
  are the lines of the tar program that caused the trace mismatch.
  '''
  error_lines = _get_error_lines(tar_program_instr, mismatched_log_stat_idx)

  return error_lines


def _run_tests(
  src_program_instr: str,
  tar_program_instr: str,
  subject: p_subject.PirelSubject
) -> None:
  '''
  RAISE `SrcTestScriptError` if there is an error when running src test script.
  RAISE `TarTestScriptError` if there is an error when running tar test script.
  RAISE `TraceMismatchError` if there is a trace mismatch between src and tar test scripts.
  '''
  p_utils.log_json_time(f'{subject.name}_args-run_tests.json', locals())
  logger.debug('Starting p_rule_applicator._run_tests')

  # 1. run `src_program_instr` and collect output trace
  src_trace, src_stderr = p_code_runner.run_src_test_script(src_program_instr, subject)

  # there is an error in running src test script
  if src_stderr != '':
    msg = f'Error running src test script: {src_stderr}'
    logger.error(msg)
    raise SrcTestScriptError(msg)

  # 2. run `tar_program_instr` and collect output trace
  tar_trace, tar_std_error = p_code_runner.run_tar_test_script(tar_program_instr, subject)

  # there is an error in running tar test script
  if tar_std_error != '':
    logger.error(f'Error running tar test script: {tar_std_error}')
    tar_error_dict = p_code_runner._extract_err_from_stderr_JS(tar_std_error, subject.tar_lang)
    raise TarTestScriptError(tar_error_dict)

  # 3. compare traces
  are_traces_identical = _compare_traces(src_trace, tar_trace)
  if not are_traces_identical:
    logger.error('Traces are not identical. There is a semantic error in translation.')
    error_lines = _extract_err_lines_from_trace_mismatch(src_trace, tar_program_instr, tar_trace)
    raise TraceMismatchError(error_lines)


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


def _get_instrumented_tar_program_plausible(
  src_program_instr: str,
  subject: p_subject.PirelSubject
) -> Tuple[str, List[List[int]]]:
  '''
  This function is responsible for obtaining a plausible translation of
  `src_program_instr` with `subject.translation_rules_main_code`.
  RETURN a tuple of:
  - `tar_program_instr` - the instrumented target program
  - `used_rule_ids_history` - a list of lists of used translation rule IDs
  '''

  def _get_used_translation_rule_ids(dbg_history: List[dict]) -> List[int]:
    used_rule_ids : List[int] = []
    for history_elem in dbg_history:
      dbg_info : dict = history_elem['dbg_info']
      notes : dict = dbg_info['notes']
      rule_id = notes['rule_id']
      used_rule_ids.append(rule_id)
    return used_rule_ids

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
  logger.debug(
    'Starting a loop to exhaustively translate `src_program_instr` '
    'with different combinations of translation rules')

  used_rule_ids_history = []
  choices_history = []
  current_choices = subject.choices
  iteration = 0
  while True:
    logger.debug(f'_get_instrumented_tar_program_plausible.iteration {iteration}')
    iteration += 1

    # May raise
    # 1. TRuleNotFoundError
    tar_main_code, map_to_exid, translate_dbg_history = _get_tar_main_code(src_main_code, current_choices, subject)
    used_rule_ids = _get_used_translation_rule_ids(translate_dbg_history)
    used_rule_ids_history.append(used_rule_ids)

    tar_program_instr = _concatenate_tar_snippets(tar_test_code_instr, tar_main_code, tar_test_call_code, subject)

    try:
      _run_tests(src_program_instr, tar_program_instr, subject)
      return tar_program_instr, used_rule_ids_history

    except SrcTestScriptError as err:
      logger.critical('There is an error in running src test script. This normally should not happen')
      raise

    except TarTestScriptError as err:
      logger.warning(
        'There is an error in running tar test script.\n'
        'Depending on the location of the error, will attempt to find a new '
        'translation rules combination.')
      tar_error_dict = err.tar_error_dict

      # May raise
      # 1. NoUniqueChoicesError
      proposed_choices = p_rule_chooser.get_proposed_choices_compile_error(
        tar_program_instr,
        tar_main_code,
        tar_error_dict,
        current_choices,
        choices_history,
        map_to_exid,
        translate_dbg_history
      )

      choices_history.append(proposed_choices)
      current_choices = proposed_choices

    except TraceMismatchError as err:
      logger.critical('There is a trace mismatch between src and tar test scripts.')
      error_lines = err.error_lines

      # May raise
      # 1. NoUniqueChoicesError
      proposed_choices = p_rule_chooser.get_proposed_choices_semantic_error(
        tar_program_instr,
        tar_main_code,
        error_lines,
        current_choices,
        choices_history,
        map_to_exid,
        translate_dbg_history
      )

      choices_history.append(proposed_choices)
      current_choices = proposed_choices


def _get_deinstrumented_tar_program_plausible(
  src_program_instr: str,
  subject: p_subject.PirelSubject
) -> Tuple[str, List[List[int]]]:

  logger.debug('Starting p_rule_applicator._get_deinstrumented_tar_program')
  tar_program_plausible_instr, used_rule_ids_history = _get_instrumented_tar_program_plausible(src_program_instr, subject)

  if not subject.needs_instrumentation:
    logger.debug('program does not need deinstrumentation')
    assert subject.translation_rules_instr_src is None, 'sanity check'
    assert subject.translation_rules_instr_tar is None, 'sanity check'
    return tar_program_plausible_instr, used_rule_ids_history

  if subject.is_mylog_inserted:
    logger.debug('program needs instrumentation, but it already is instrumented')
    assert subject.translation_rules_instr_src is None, 'sanity check'
    assert subject.translation_rules_instr_tar is None, 'sanity check'
    return tar_program_plausible_instr, used_rule_ids_history

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

  return tar_program_plausible_deinstr, used_rule_ids_history


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
  logger.debug(f'Starting p_rule_applicator._get_tar_test_call_code')
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
    raise TRuleNotFoundError('There is a problematic node in src_main_code')

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


# API
def apply_translation_rules(subject: p_subject.PirelSubject) -> Tuple[str, List[List[int]]]:
  '''
  Apply the translation rules to the source program.
  Equivalent to index_bench.js::runBenchmarkHandler

  RETURN `tar_program_deinstr` - the target program that is deinstrumented.
  '''
  p_utils.log_json_time(f'{subject.name}_args-apply_translation_rules.json', locals())
  logger.info('Starting p_rule_applicator.apply_translation_rules (a la DuoGlot)')

  src_program_instr = _get_instrumented_src_program(subject)
  tar_program_deinstr, used_rule_ids_history = _get_deinstrumented_tar_program_plausible(src_program_instr, subject)

  return tar_program_deinstr, used_rule_ids_history


# USAGE
def usage_apply_translation_rules():
  subject_config = p_subject.PirelSubject.from_file_config(p_consts.ROOT_DIR / 'conf' / 'pirel-subject' / 'test.yaml')
  tar_program_plausible, used_rule_ids_history = apply_translation_rules(subject_config)
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
  tar_program_deinstr, used_rule_ids_history = apply_translation_rules(subject)
  print(f'Plausible target program:\n{tar_program_deinstr}')
  print('Used rule IDs history:')
  for used_rule_ids in used_rule_ids_history:
    print(used_rule_ids)


def _test_run_tests():
  '''
  def _run_tests(
    src_program_instr: str,
    tar_program_instr: str,
    subject: p_subject.PirelSubject
  ) -> Optional[dict]:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_run_tests_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  src_program_instr = args_dict['src_program_instr']
  tar_program_instr = args_dict['tar_program_instr']
  subject = p_subject.PirelSubject.from_dict_config(json.loads(args_dict['subject']))

  result = _run_tests(src_program_instr, tar_program_instr, subject)
  print(json.dumps(result, indent=2))


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
  # _test_run_tests()
  # _test_postprocess_src_program()
