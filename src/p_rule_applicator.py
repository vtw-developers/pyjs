import asyncio
import json
import re
from typing import Dict, List, Optional, Tuple

import d_grammar_expand
import p_code_runner
import p_consts
import p_ext_rule_chooser
import p_pirel
import p_subject
import p_utils


logger = p_utils.setup_logger(__name__)


class UnknownTypeInTracesError(RuntimeError): pass
class SrcTestScriptRunError(RuntimeError): pass
class TarTestScriptRunError(RuntimeError):
  def __init__(self, tar_error_dict: dict):
    super().__init__('Error running tar test script')
    self.tar_error_dict = tar_error_dict
  def __str__(self):
    return f'TarTestScriptRunError: {json.dumps(self.tar_error_dict, indent=2)}'
class TraceMismatchError(RuntimeError):
  def __init__(self, error_lines: dict):
    super().__init__('Trace mismatch between src and tar test scripts')
    self.error_lines = error_lines
  def __str__(self):
    return f'TraceMismatchError: {json.dumps(self.error_lines, indent=2)}'
class SrcTestScriptProblematicNodeError(RuntimeError):
  '''
  This error is raised when there is a translation error
  when translating src_main_code.
  '''
  def __init__(self, *args):
    super().__init__(*args)
    self.src_main_code : Optional[str] = None
    self.choices : Optional[dict] = None
    self.translation_rules_main_code : Optional[str] = None
    self.problematic_node_id : Optional[int] = None
    self.problematic_node_type : Optional[str] = None


# INTERNAL API
def are_traces_equal_rec(
  src_trace: list,
  tar_trace: list
) -> bool:
  '''
  Compare the traces from the source and target programs.
  This is a recursive function.
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

  # base case: types are hash
  if type1 == 'hash':
    len1, len2 = src_trace[1], tar_trace[1]
    hash1, hash2 = src_trace[2], tar_trace[2]
    return len1 == len2 and hash1 == hash2

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
      child_res = are_traces_equal_rec(ch1, ch2)
      if not child_res:
        return False
    return True

  if type1 == 'unknown':
    logger.warning('are_traces_equal_rec: unknown type')
    len1, len2 = src_trace[1], tar_trace[1]
    str1, str2 = src_trace[2], tar_trace[2]
    return len1 == len2 and str1 == str2

  raise UnknownTypeInTracesError(f'Unknown type in are_traces_equal_rec: "{type1}"')


def is_valid_trace(
  trace: list
) -> bool:
  '''
  Check if the trace is valid.
  A valid trace is a list with exactly 3 elements:
  - type of the trace is a string "list"
  - length of the trace
  - list of trace entries
  '''
  if not isinstance(trace, list):
    return False
  if len(trace) != 3:
    return False

  trace_type = trace[0]
  trace_size = trace[1]
  trace_entries = trace[2]

  if not isinstance(trace_type, str):
    return False
  if trace_type != 'list':
    return False

  if not isinstance(trace_size, int):
    return False
  if trace_size < 0:
    return False

  if not isinstance(trace_entries, list):
    return False
  if len(trace_entries) != trace_size:
    return False

  return True


def is_valid_trace_entry(
  trace_entry: list
) -> bool:
  '''
  Check if the trace entry is valid.
  A valid trace entry is a list with exactly 3 elements:
  - type of the trace entry is a string "list"
  - length of the trace entry (corresponds to the number of arguments)
  - list of trace entry arguments
  '''
  if not isinstance(trace_entry, list):
    return False
  if len(trace_entry) != 3:
    return False

  te_type = trace_entry[0]
  te_size = trace_entry[1]
  te_args = trace_entry[2]

  if not isinstance(te_type, str):
    return False
  if te_type != 'list':
    return False

  '''
  Size of the trace entry must be at least 2:
  1. the first argument is the index of the log statement
  2. the second and subsequent arguments are the actual logged values
  '''
  if not isinstance(te_size, int):
    return False
  if te_size < 2:
    return False

  if not isinstance(te_args, list):
    return False
  if len(te_args) != te_size:
    return False

  return True


def is_trace_subsumed(
  shorter_trace: list,
  longer_trace: list
) -> bool:
  '''
  Check if the longer trace subsumes the shorter trace.
  '''
  assert is_valid_trace(shorter_trace), 'shorter_trace must be a valid trace'
  assert is_valid_trace(longer_trace), 'longer_trace must be a valid trace'

  shorter_tes = shorter_trace[2]
  longer_tes = longer_trace[2]
  assert len(longer_tes) > len(shorter_tes), 'longer_trace must be strictly longer than shorter_trace'

  # zip truncates the longer trace to the length of the shorter trace
  for idx, (shorter_te, longer_te) in enumerate(zip(shorter_tes, longer_tes)):
    assert is_valid_trace_entry(shorter_te), 'shorter_trace entry must be valid'
    assert is_valid_trace_entry(longer_te), 'longer_trace entry must be valid'
    trace_entries_identical = are_traces_equal_rec(shorter_te, longer_te)
    if not trace_entries_identical:
      return False

  return True


def does_trace_subsume_another(
  trace1: list,
  trace2: list
) -> bool:
  '''
  Check if one trace subsumes the second trace.
  '''
  assert is_valid_trace(trace1), 'trace1 must be a valid trace'
  assert is_valid_trace(trace2), 'trace2 must be a valid trace'
  trace1_len = trace1[1]
  trace2_len = trace2[1]
  if trace1_len < trace2_len:
    return is_trace_subsumed(trace1, trace2)
  elif trace2_len < trace1_len:
    return is_trace_subsumed(trace2, trace1)
  else:
    return are_traces_equal_rec(trace1, trace2)


def _get_trace_mismatch_idx(
  src_trace: list,
  tar_trace: list
) -> int:
  '''
  Given two traces, find the first index where they differ.
  If they are identical, return None. Index is 0-based.
  PRE: traces are not identical.
  RAISE: RuntimeError if traces are identical.
  '''
  def __get_trace_mismatch_idx_len_equal(src_trace_entries: list, tar_trace_entries: list) -> int:
    '''
    This function is used when the source trace and target trace are of the same length.
    '''
    for idx, (src_te, tar_te) in enumerate(zip(src_trace_entries, tar_trace_entries)):
      assert is_valid_trace_entry(src_te), 'source trace entry must be valid'
      assert is_valid_trace_entry(tar_te), 'target trace entry must be valid'
      trace_entries_identical = are_traces_equal_rec(src_te, tar_te)
      if not trace_entries_identical:
        return idx
    # if we reach here, it means that all entries are identical
    raise RuntimeError('Traces must be different')

  def __get_trace_mismatch_idx_tar_trace_larger(src_trace_entries: list, tar_trace_entries: list) -> int:
    '''
    This function is used when the source trace is shorter than the target trace.
    '''
    for idx, (src_te, tar_te) in enumerate(zip(src_trace_entries, tar_trace_entries)):
      assert is_valid_trace_entry(src_te), 'source trace entry must be valid'
      assert is_valid_trace_entry(tar_te), 'target trace entry must be valid'
      trace_entries_identical = are_traces_equal_rec(src_te, tar_te)
      if not trace_entries_identical:
        return idx
    # if we reach here, it means that src trace is subsumed by target trace
    raise RuntimeError('Source trace is subsumed by target trace. Target trace has more iterations?')

  def __get_trace_mismatch_idx_src_trace_larger(src_trace_entries: list, tar_trace_entries: list) -> int:
    '''
    This function is used when the source trace is longer than the target trace.
    '''
    for idx, (src_te, tar_te) in enumerate(zip(src_trace_entries, tar_trace_entries)):
      assert is_valid_trace_entry(src_te), 'source trace entry must be valid'
      assert is_valid_trace_entry(tar_te), 'target trace entry must be valid'
      trace_entries_identical = are_traces_equal_rec(src_te, tar_te)
      if not trace_entries_identical:
        return idx
    # if we reach here, it means that tar trace is subsumed by src trace
    raise RuntimeError('Target trace is subsumed by source trace. Target trace needs more iterations?')

  src_trace_type = src_trace[0]
  tar_trace_type = tar_trace[0]
  assert src_trace_type == 'list' and tar_trace_type == 'list', 'traces must be lists'
  src_trace_len = src_trace[1]
  tar_trace_len = tar_trace[1]
  src_trace_entries = src_trace[2]
  tar_trace_entries = tar_trace[2]

  # both traces are of the same length
  if src_trace_len == tar_trace_len:
    return __get_trace_mismatch_idx_len_equal(src_trace_entries, tar_trace_entries)

  # source trace is shorter than target trace
  elif src_trace_len < tar_trace_len:
    return __get_trace_mismatch_idx_tar_trace_larger(src_trace_entries, tar_trace_entries)

  # source trace is longer than target trace
  else:
    return __get_trace_mismatch_idx_src_trace_larger(src_trace_entries, tar_trace_entries)


def _get_log_statement_idx(
  src_trace: list,
  tar_trace: list,
  trace_idx: int
) -> int:
  '''
  Given two traces and a trace index, find the log statement index under that trace index.
  Log statement indices are 1-based. trace_idx is 0-based.

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

  assert trace_idx < len(src_trace_entries), 'trace index must be less than src trace entries length'
  assert trace_idx < len(tar_trace_entries), 'trace index must be less than tar trace entries length'

  src_trace_entry = src_trace_entries[trace_idx]
  tar_trace_entry = tar_trace_entries[trace_idx]

  src_trace_entry_type = src_trace_entry[0]
  tar_trace_entry_type = tar_trace_entry[0]
  assert src_trace_entry_type == 'list' and tar_trace_entry_type == 'list', \
    'trace entries must be lists'

  src_trace_arg_len = src_trace_entry[1]
  tar_trace_arg_len = tar_trace_entry[1]
  assert src_trace_arg_len >= 2 and tar_trace_arg_len >= 2, \
    'trace entries must have at least 2 arguments logged'

  src_trace_args = src_trace_entry[2]
  tar_trace_args = tar_trace_entry[2]
  src_trace_arg1 = src_trace_args[0]
  tar_trace_arg1 = tar_trace_args[0]
  src_trace_arg1_type = src_trace_arg1[0]
  tar_trace_arg1_type = tar_trace_arg1[0]
  assert src_trace_arg1_type == 'number' and tar_trace_arg1_type == 'number', \
    'trace entry first argument must be a number'

  src_trace_arg1_value = src_trace_arg1[1]
  tar_trace_arg1_value = tar_trace_arg1[1]
  assert isinstance(src_trace_arg1_value, int) and isinstance(tar_trace_arg1_value, int), \
    'trace entry first argument must be an int'

  src_trace_arg2 = src_trace_args[1]
  tar_trace_arg2 = tar_trace_args[1]

  if src_trace_arg1_value != tar_trace_arg1_value:
    logger.warning(
      f'Expected log statement #{src_trace_arg1_value}, got #{tar_trace_arg1_value}.\n'
      f'src_trace_entry: {src_trace_entry}\n'
      f'tar_trace_entry: {tar_trace_entry}\n'
      f'trace_idx: {trace_idx}')
  else:
    logger.warning(
      f'Expected "{src_trace_arg2}" at log statement #{src_trace_arg1_value}, got "{tar_trace_arg2}".\n'
      f'src_trace_entry: {src_trace_entry}\n'
      f'tar_trace_entry: {tar_trace_entry}\n'
      f'trace_idx: {trace_idx}')

  return tar_trace_arg1_value


def _get_log_statement_idx_subsumed(
  src_trace: list,
  tar_trace: list
) -> int:
  '''
  Return a log statement index that caused the trace mismatch
  given that one trace is subsumed by another.
  '''
  assert does_trace_subsume_another(src_trace, tar_trace), 'one trace must subsume another'
  assert is_valid_trace(src_trace), 'src_trace must be a valid trace'
  assert is_valid_trace(tar_trace), 'tar_trace must be a valid trace'

  src_trace_entries = src_trace[2]
  tar_trace_entries = tar_trace[2]

  assert len(src_trace_entries) != len(tar_trace_entries), 'traces must be of different lengths'
  shorter_trace_len = min(len(src_trace_entries), len(tar_trace_entries))
  longer_trace_entries = tar_trace_entries if len(tar_trace_entries) > len(src_trace_entries) else src_trace_entries

  trace_entry = longer_trace_entries[shorter_trace_len]
  assert is_valid_trace_entry(trace_entry), 'trace entry must be valid'

  trace_entry_type = trace_entry[0]
  assert trace_entry_type == 'list', 'trace entry must be a list'

  trace_entry_len = trace_entry[1]
  assert trace_entry_len >= 2, 'trace entry must have at least 2 arguments logged'

  trace_entry_args = trace_entry[2]
  trace_arg1 = trace_entry_args[0]
  trace_arg1_type = trace_arg1[0]
  assert trace_arg1_type == 'number', 'trace entry first argument must be a number'

  trace_arg1_value = trace_arg1[1]
  assert isinstance(trace_arg1_value, int), 'trace entry first argument must be an int'

  logger.warning(f'Looks like an extra or missing loop iteration caused by log statement #{trace_arg1_value}')
  return trace_arg1_value


def _get_mismatched_log_statement_idx(
  src_trace: list,
  tar_trace: list
) -> int:

  if not does_trace_subsume_another(src_trace, tar_trace):
    '''
    A trace mismatch index is a 0-based index in the traces where the entries differ.
    Using this index, we can find which log statement caused the trace mismatch.
    '''
    trace_mismatch_idx = _get_trace_mismatch_idx(src_trace, tar_trace)

    '''
    A mismatched log statement index is an index of the log statement that caused
    the trace mismatch. Log statement indices are 1-based.
    trace_mismatch_idx is 0-based.
    '''
    mismatched_log_stat_idx = _get_log_statement_idx(src_trace, tar_trace, trace_mismatch_idx)

    return mismatched_log_stat_idx

  else:
    '''
    If one trace subsumes another, it means that there is a missing or extra loop iteration.
    '''
    mismatched_log_stat_idx = _get_log_statement_idx_subsumed(src_trace, tar_trace)
    return mismatched_log_stat_idx


def _get_error_lines(
  tar_program_instr: str,
  mismatched_log_stat_idx: int
) -> Dict[int, str]:
  '''
  Given a tar_program_instr (instrumented tar program) and a mismatched log statement index,
  return the line numbers right before the mismatched log statement.
  RETURN a dictionary with line numbers as keys and lines as values:
  {
    12: "        n += 'n';"
  }
  NOTE line numbers are 0-based indices of lines in `tar_program_instr`.
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

  def __is_log_stat_before_return_stat(stripped_lines: List[str], mismatched_log_stat_idx: int):
    '''
    The idea is to find the line that starts with `myexactlog(mismatched_log_stat_idx)`
    and check if the next line starts with `return `.
    '''
    assert mismatched_log_stat_idx >= 1, 'mismatched_log_stat_idx must be >= 1'
    myexactlog_idx = __find_text(stripped_lines, f'myexactlog({mismatched_log_stat_idx}')
    next_idx = myexactlog_idx + 1
    if stripped_lines[next_idx].startswith('return '):
      logger.debug(f'Log statement {mismatched_log_stat_idx} appears right before return statement.')
      return True
    return False

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

  '''
  We need to check whether log statement with index mismatch_line_idx_before
  appears right before the return statement. If it does, then the error line
  is at the return statement, and we need to overwrite the values of
  mismatch_line_idx and mismatch_line_idx_before.
  '''
  if __is_log_stat_before_return_stat(stripped_lines, mismatched_log_stat_idx):
    # return statement is in between these two lines
    mismatch_line_idx_before = mismatch_line_idx
    mismatch_line_idx = mismatch_line_idx + 2

  assert mismatch_line_idx != -1, \
    f'mismatched_log_stat_idx {mismatched_log_stat_idx} not found in stripped lines'
  assert mismatch_line_idx_before != -1, \
    f'mismatched_log_stat_idx {mismatched_log_stat_idx - 1} not found in stripped lines'

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
  Error lines is a dictionary where keys are line numbers (0-based) and values
  are the lines of the tar program that caused the trace mismatch.
  '''
  mismatched_log_stat_idx = _get_mismatched_log_statement_idx(src_trace, tar_trace)
  error_lines = _get_error_lines(tar_program_instr, mismatched_log_stat_idx)

  return error_lines


async def _run_tests(
  src_program_instr: str,
  tar_program_instr: str,
  subject: p_subject.PirelSubject
) -> None:
  '''
  RAISE `SrcTestScriptRunError` if there is an error when running src test script.
  RAISE `TarTestScriptRunError` if there is an error when running tar test script.
  RAISE `TraceMismatchError` if there is a trace mismatch between src and tar test scripts.
  '''
  p_utils.log_json_time(f'args-run_tests.json', locals())
  logger.debug('~~~ Starting to run source and target test scripts.')

  # 1. run `src_program_instr` and collect output trace
  src_trace, src_stderr = await p_code_runner.run_src_test_script(src_program_instr, subject)
  assert is_valid_trace(src_trace), 'src_trace must be a valid trace'

  # there is an error in running src test script
  if src_stderr != '':
    msg = f'SHOULD NOT HAPPEN! Error running src test script: {src_stderr}'
    logger.critical(msg)
    raise SrcTestScriptRunError(msg)
  else:
    logger.debug('GOOD No errors running src test script.')

  # 2. run `tar_program_instr` and collect output trace
  tar_trace, tar_std_error = await p_code_runner.run_tar_test_script(tar_program_instr, subject)
  assert is_valid_trace(tar_trace), 'tar_trace must be a valid trace'

  '''
  At this point, we have all the necessary data to decide whether to
  1. finish running tests without any errors
  2. raise TraceMismatchError if there is a trace mismatch
  3. raise TarTestScriptRunError if there is an error in running tar test script

  NOTE Trace categories (relative to each other)
  src and tar traces may fall into one of the following 6 categories:
  1. len(src_trace) < len(tar_trace) - src trace is shorter than tar trace
     a. is_trace_subsumed(src_trace, tar_trace)
        - there is a semantic error in tar test script due to
          possibly extra loop iterations
     b. not is_trace_subsumed(src_trace, tar_trace)
        - there is a semantic error due to trace mismatch
  2. len(src_trace) > len(tar_trace) - src trace is longer than tar trace
     a. is_trace_subsumed(tar_trace, src_trace)
        - there is a semantic error in tar test script due to
          possibly missing loop iterations
     b. not is_trace_subsumed(tar_trace, src_trace)
        - there is a semantic error due to trace mismatch
  3. len(src_trace) == len(tar_trace) - src trace and tar trace are of the same length
     a. are_traces_equal_rec(src_trace, tar_trace)
        - there is no semantic error
     b. not are_traces_equal_rec(src_trace, tar_trace)
        - there is a semantic error due to trace mismatch

  NOTE Error categories
  Regarding what error to raise:
  1. raise TarTestScriptRunError iff
     a. (tar_std_error != '') and is_trace_subsumed(tar_trace, src_trace)
        - case 2a
        - cases 1a, 3a are not supported yet
  2. raise TraceMismatchError iff
     a. (tar_std_error == '') and does_trace_subsume_another(src_trace, tar_trace)
        - cases 1b, 2b, 3b
        - cases 1a, 2a, 3a are not supported yet
     b. (tar_std_error != '') and does_trace_subsume_another(src_trace, tar_trace)
        - cases 1b, 2b, 3b
        - cases 1a, 2a, 3a are not supported yet
  '''

  # there is an error in running tar test script
  if tar_std_error != '':
    logger.debug(f'BAD Error running tar test script:\n{tar_std_error.strip()}')
    '''
    Sometimes, it might be the case that at the time an error occurs in tar test script,
    there already is a trace mismatch between src and tar traces. This suggests that the
    tar test script error occured due to an invalid rule chosen earlier. In this case,
    we should ensure that at the time of tar test script error, the src and tar traces
    are identical by choosing the correct translation rule.
    '''
    if not does_trace_subsume_another(src_trace, tar_trace):
      logger.debug('Trace mismatch between src and tar traces at the time of tar test script error.')
      error_lines = _extract_err_lines_from_trace_mismatch(src_trace, tar_program_instr, tar_trace)
      logger.debug(f'Trace mismatch error lines:\n{json.dumps(error_lines, indent=2)}')
      raise TraceMismatchError(error_lines)

    '''
    At this point, we know that one of the traces subsumes the other.
    If the src trace subsumes the tar trace, it is ok, because up to the point of
    tar test script error, the src and tar traces match.
    If the tar trace subsumes the src trace, it is not ok, because this case is not
    considered yet.
    '''
    src_trace_size = src_trace[1]
    tar_trace_size = tar_trace[1]
    assert src_trace_size > tar_trace_size, \
      'NOT SUPPORTED: src_trace must be strictly longer than tar_trace'

    tar_error_dict = p_code_runner.extract_err_from_stderr_JS(tar_std_error, subject.tar_lang)
    raise TarTestScriptRunError(tar_error_dict)
  else:
    logger.debug('GOOD No errors running tar test script.')

  # 3. compare traces
  are_traces_identical = are_traces_equal_rec(src_trace, tar_trace)
  if not are_traces_identical:
    error_lines = _extract_err_lines_from_trace_mismatch(src_trace, tar_program_instr, tar_trace)
    logger.debug(
      f'Traces are not identical. There is a semantic error in translation.\n'
      f'error_lines:\n{json.dumps(error_lines, indent=2)}')
    raise TraceMismatchError(error_lines)


def _get_tar_test_code(
  src_test_code: Optional[str],
  subject: p_subject.PirelSubject
) -> Optional[str]:
  '''
  Ideally, this function is run only once.
  '''
  if not subject.is_three_split:
    assert src_test_code is None, 'sanity check'
    return None

  # translate `src_test_code` using `translation_rules_test_code`
  duoglot_translate_result = p_pirel.duoglot_translate_wrapper(
    src_code=src_test_code,
    src_lang=subject.src_lang,
    tar_lang=subject.tar_lang,
    trans_rules=subject.translation_rules_test_code,
    auto_backward=subject.auto_backward,
    choices=subject.choices,
    skip_template_extraction=True
  )
  tar_test_code = duoglot_translate_result['tar_code']
  return tar_test_code


def _get_tar_test_call_code(
  src_test_call_code: str
) -> str:
  '''
  For the moment, just use `src_test_call_code` as `tar_test_call_code`,
  because Python and JavaScript function call syntax is the same.
  '''
  return src_test_call_code


def _get_tar_main_code_instr(
  src_main_code: str,
  choices: dict,
  subject: p_subject.PirelSubject
) -> Tuple[str, Dict[int, List[dict]], List[dict]]:
  '''
  Translate `src_main_code` using `translation_rules_main_code` and `choices`.
  RAISE SrcTestScriptProblematicNodeError
  '''
  logger.debug('Translating src_main_code_instr to get tar_main_code_instr.')

  assert subject.translation_rules_main_code is not None, \
    'translation rules for main code must be provided'

  try:
    duoglot_translate_result = p_pirel.duoglot_translate_wrapper(
      src_code=src_main_code,
      src_lang=subject.src_lang,
      tar_lang=subject.tar_lang,
      trans_rules=subject.translation_rules_main_code,
      auto_backward=subject.auto_backward,
      choices=choices,
      skip_template_extraction=True
    )
  except d_grammar_expand.TranslationRuleNotFoundException as exc:
    templates_dict = exc.get_templates_dict()
    logger.warning(f'Caught TranslationRuleNotFoundException when translating src_main_code: {exc}')
    err_obj = SrcTestScriptProblematicNodeError(
      f'There is a problematic node in src_main_code:\n'
      f'problematic_node_type = "{templates_dict["problematic_node_type"]}", '
      f'problematic_node_id = {templates_dict["problematic_node_id"]}')
    err_obj.src_main_code = src_main_code
    err_obj.choices = choices
    err_obj.translation_rules_main_code = subject.translation_rules_main_code
    err_obj.problematic_node_id = templates_dict['problematic_node_id']
    err_obj.problematic_node_type = templates_dict['problematic_node_type']
    raise err_obj

  tar_main_code = duoglot_translate_result['tar_code']
  map_to_exid = duoglot_translate_result['map_to_exid']
  translate_dbg_history = duoglot_translate_result['dbg_history']
  return tar_main_code, map_to_exid, translate_dbg_history


def _program_parts_concatenate(
  test_code: Optional[str],
  main_code: str,
  test_call_code: Optional[str],
  subject: p_subject.PirelSubject
) -> str:
  '''
  Combine `test_code`, `main_code`, and `test_call_code` into a single string.
  '''
  if not subject.is_three_split:
    assert test_code is None, 'sanity check'
    assert test_call_code is None, 'sanity check'
    return main_code
  assert test_code is not None, 'sanity check'
  assert test_call_code is not None, 'sanity check'
  return f'\n{p_consts.TEST_MAIN_CALL_DELIMITER}\n'.join([test_code, main_code, test_call_code])


def _program_parts_split(
  program: str,
  subject: p_subject.PirelSubject
) -> Tuple[Optional[str], str, Optional[str]]:
  '''
  Split `program` into test, main, and test call code snippets.
  If `subject.is_three_split` is False, return None for test and test call code snippets.
  '''
  if not subject.is_three_split:
    assert p_consts.TEST_MAIN_CALL_DELIMITER not in program, 'sanity check'
    return None, program, None

  chunks = program.split(p_consts.TEST_MAIN_CALL_DELIMITER)
  assert len(chunks) == 3, 'sanity check: program should be split into 3 parts'
  src_test_code, src_main_code, src_test_call_code = chunks
  return src_test_code, src_main_code, src_test_call_code


# API
async def apply_translation_rules(
  subject: p_subject.PirelSubject
) -> str:
  '''
  Apply the translation rules to the source program.
  Equivalent to index_bench.js::runBenchmarkHandler
  RETURN a str tar_program_instr

  Raised or propagated exceptions:
  - SrcTestScriptRunError
  - RuleCombinationsExhaustedError
  - SrcTestScriptProblematicNodeError

  NOTE subject.src_program must be instrumented.
  '''

  p_utils.log_json_time(f'args-apply_translation_rules.json', locals())
  logger.info('rule-app: starting rule applicator')

  src_program_instr = subject.src_program
  src_test_code, src_main_code_instr, src_test_call_code = \
    _program_parts_split(src_program_instr, subject)

  # 2 get corresponding instrumented test code and test call code
  tar_test_code = _get_tar_test_code(src_test_code, subject)
  tar_test_call_code = _get_tar_test_call_code(src_test_call_code)

  '''
  This is a stack of choice options for each error line.
  '''
  choices_list_stack = []

  '''
  This is an object that is passed to the translator that tells it
  which rules to choose at given AST nodes.
  '''
  current_choices = subject.choices
  assert current_choices['type'] == 'ASTNODE', f'unsupported choices type "{current_choices["type"]}"'

  # 3 loop to get exhaustive translation of main code
  logger.debug(
    'Starting a loop to exhaustively translate `src_program_instr` '
    'with different combinations of translation rules')
  iteration = 0
  while True:
    logger.debug(f'rule-app: iteration {iteration} starts')
    iteration += 1

    tar_main_code_instr, map_to_exid, translate_dbg_history = \
      _get_tar_main_code_instr(src_main_code_instr, current_choices, subject)
    tar_program_instr = _program_parts_concatenate(tar_test_code, tar_main_code_instr, tar_test_call_code, subject)

    try:
      await _run_tests(src_program_instr, tar_program_instr, subject)
      return tar_program_instr

    except SrcTestScriptRunError as err:
      logger.critical('There is an error in running src test script. This normally should not happen')
      raise

    except TarTestScriptRunError as err:
      logger.warning(
        'There is an error in running tar test script. '
        'Depending on the location of the error, will attempt to find a new '
        'translation rules combination.')
      tar_error_dict = err.tar_error_dict

      # May raise
      # 1. RuleCombinationsExhaustedError
      proposed_choices = p_ext_rule_chooser.get_proposed_choices_compile_error(
        tar_program_instr,
        tar_main_code_instr,
        tar_error_dict,
        choices_list_stack,
        map_to_exid,
        translate_dbg_history,
        subject.readonly_choices_list
      )

      current_choices = proposed_choices

    except TraceMismatchError as err:
      logger.critical('There is a trace mismatch between src and tar test scripts.')
      error_lines = err.error_lines

      # May raise
      # 1. RuleCombinationsExhaustedError
      proposed_choices = p_ext_rule_chooser.get_proposed_choices_semantic_error(
        tar_program_instr,
        tar_main_code_instr,
        error_lines,
        choices_list_stack,
        map_to_exid,
        translate_dbg_history,
        subject.readonly_choices_list
      )

      current_choices = proposed_choices

    logger.debug(f'rule-app: iteration {iteration} ended')


# USAGE
def usage_apply_translation_rules():
  subject_config = p_subject.PirelSubject.from_file_config(p_consts.ROOT_DIR / 'conf' / 'pirel-subject' / 'test.yaml')
  tar_program_plausible = asyncio.run(apply_translation_rules(subject_config))
  logger.debug(f'Plausible target program:\n{tar_program_plausible}')


# TEST HARNESSES
def _test_apply_translation_rules():
  '''
  async def apply_translation_rules(subject: p_subject.PirelSubject) -> str:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_apply_translation_rules_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  subject = p_subject.PirelSubject.from_dict(json.loads(args_dict['subject']))
  tar_program_deinstr = asyncio.run(apply_translation_rules(subject))
  print(f'Plausible target program:\n{tar_program_deinstr}')


def _test_run_tests():
  '''
  async def _run_tests(
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
  subject = p_subject.PirelSubject.from_dict(json.loads(args_dict['subject']))

  asyncio.run(_run_tests(src_program_instr, tar_program_instr, subject))


if __name__ == '__main__':
  # usage_apply_translation_rules()
  _test_apply_translation_rules()
  # _test_run_tests()
