import asyncio
import json
import re
import sys
from pathlib import Path
from typing import Tuple

import d_utils
import p_consts
import p_subject
import p_utils


logger = p_utils.setup_logger(__name__)


CODE_RUN_COMMANDS = {'py': sys.executable, 'js': 'node'}
assert all(map(CODE_RUN_COMMANDS.__contains__, p_consts.LANG_DICT))

TMP_DIR = Path('/tmp/pirel_code_runner')
TMP_DIR.mkdir(exist_ok=True)


def get_mylog_impl(lang: str) -> str:
  '''
  Get the mylog implementation for the given language.
  '''
  assert lang in p_consts.LANG_DICT, f'Unsupported language: {lang}'
  mylog_fpath = p_consts.MYLOG_DEFINITIONS_DIR / lang / f'mylog_pirel.{lang}'
  assert mylog_fpath.exists(), f'Mylog implementation not found for {lang}'
  return p_utils.read_text(mylog_fpath)


def _get_temp_filename(text: str, lang: str) -> str:
  hexhash = d_utils.string_sha256(text)[:8]
  return TMP_DIR / f'{hexhash}.{lang}'


def _extract_trace_from_stdout(stdout: str) -> list:
  '''
  Parses whatever was produced by the `mylog` function

  sample stdout:
  ["MYLOGEX:", ["number", 0]]
  ["MYLOGEX:", ["number", 42]]
  89 ["MYLOGEX:",["number",1],["hash",64,"31258e253c85ed2fcf5c0c1df7817d48be55a95e1b90d9b4f201183cf6bf9afb"]]
  '''
  lines_str = stdout.split('\n')
  trace = []
  for line_str in lines_str:
    if line_str.startswith('["MYLOGEX:"'):
      line_obj = json.loads(line_str)
      trace.append(['list', len(line_obj) - 1, line_obj[1:]])

    # Cases where myexactlog output is not at the beginning of the line
    # e.g. '89 ["MYLOGEX:",["number",1],["hash",4,"8e25"]]'.
    # Happens in JS when process.stdout.write is used instead of console.log
    # as in G0004 in GFG benchmark.
    elif '["MYLOGEX:"' in line_str:
      begin_idx = line_str.index('["MYLOGEX:"')
      line_obj = json.loads(line_str[begin_idx:])
      trace.append(['list', len(line_obj) - 1, line_obj[1:]])

  return ['list', len(trace), trace]


def extract_err_from_stderr_JS(stderr: str, lang: str) -> dict:
  '''
  Parse the error message from the stderr of the JS code.
  Refer to tests for sample inputs and expected outputs.
  '''

  logger.debug('Starting p_code_runner._extract_err_from_stderr')
  assert lang == 'js', f'Unsupported language: {lang}'
  assert str(TMP_DIR) in stderr, f'Expected "{TMP_DIR}" in stderr: {stderr}'

  RE_FIRST_LINE = r'^(.+):(\d+)$'
  RE_AT_LINE = r'^at(.*) \(?(.+):(\d+):(\d+)\)?$'

  lines = [line.strip() for line in stderr.split('\n')]
  at_lines = [line for line in lines[5:]
              if line.startswith('at ') and str(TMP_DIR) in line]

  if len(at_lines) == 0:
    first_line = lines[0]
    match = re.match(RE_FIRST_LINE, first_line)
    assert match is not None, f'Expected match for first_line: {first_line}'
    file_path = match.group(1)
    line_num = int(match.group(2))
  else:
    at_line = at_lines[0]
    match = re.match(RE_AT_LINE, at_line)
    assert match is not None, f'Expected match for at_line: {at_line}'
    file_path = match.group(2)
    line_num = int(match.group(3))
  # adjust line_num to account for mylog implementation lines
  mylog_impl = get_mylog_impl(lang)
  line_num_shift = len(mylog_impl.split('\n')) - 1
  line_num = line_num - line_num_shift

  line_content = lines[1]
  assert lines[2].strip('^') == '', f'Expected one or more hats "^" on line #3: {lines[2]}'
  assert lines[3] == '', f'Expected nothing on line #4: {lines[3]}'

  error_type_msg = [ch.strip() for ch in lines[4].split(':')]
  assert len(error_type_msg) <= 2, f'Expected at most two chunks when splitting by ":": {lines[4]}'
  error_type = error_type_msg[0]
  assert error_type in p_consts.SUPPORTED_ERROR_TYPES_JS, f'Unsupported error type: {error_type}'
  error_msg = error_type_msg[1] if len(error_type_msg) == 2 else ''

  return {
    'error_type': error_type,
    'error_msg': error_msg,
    'file_path': file_path,
    'line_num': line_num,
    'line_content': line_content
  }


async def _run_code(code: str, lang: str,
                    timeout_sec: None | int | float = 100) -> tuple[str, str]:
  '''
  Run the code and return stdout and stderr
  '''
  assert lang in p_consts.LANG_DICT, f'Unsupported language: {lang}'
  command = CODE_RUN_COMMANDS[lang]
  temp_filename = _get_temp_filename(code, lang)
  p_utils.write_text(temp_filename, code)

  logger.debug(f'Executing command: {command} {temp_filename}')
  proc = await asyncio.create_subprocess_exec(
    command, temp_filename, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
  try:
    async with asyncio.timeout(timeout_sec):
      # await proc.communicate() sometimes create a zombie process,
      # which probably has something to do with improper pipe cleanup
      # at in asyncio.gather.  See also
      # https://github.com/python/cpython/issues/103847
      # and relevant issues mentioned in that thread.
      stdout = (await proc._read_stream(1)).decode()
      stderr = (await proc._read_stream(2)).decode()
  except Exception as exc:
    logger.debug(f'Error executing "{command} {temp_filename}": {exc}')
    proc.kill()
    raise
  else:
    return stdout, stderr


def comment_out_default_mylog_impls(code: str, lang: str) -> str:
  '''
  Leetcode benchmark subjects come with default values for
  `mylog` and `myexactlog` in the source code.
  This function comments out the lines between the
  `# ++++++ to be replaced by tester ++++++` and
  `# "+++++++++++++++++"` lines.
  '''

  assert lang in p_consts.LANG_DICT, f'Unsupported language: {lang}'

  _SPLITTER = '"+++++++++++++++++"'
  _LINE_COMMENT_FOR = {
    'py': '# ',
    'js': '// '
  }

  splits = code.split(_SPLITTER)
  if len(splits) == 1:
    return code
  assert len(splits) == 2
  to_comment_out, rest = splits
  commented_out = '\n'.join([_LINE_COMMENT_FOR[lang] + line for line in to_comment_out.split('\n')])
  return commented_out + f'{_SPLITTER}' + rest


_CACHE_RUN_SRC_TS = {}
_CACHE_RUN_SRC_TS_SIZE = 1000

async def run_src_test_script(
  src_program_instr: str,
  subject: p_subject.PirelSubject
) -> Tuple[list, str]:
  '''
  This function runs the source program with mylog and returns the log list and error.
  '''
  logger.debug('Running source test script')

  mylog_impl = get_mylog_impl(subject.src_lang)
  src_program_run = mylog_impl + comment_out_default_mylog_impls(src_program_instr, subject.src_lang)

  if src_program_run in _CACHE_RUN_SRC_TS:
    logger.debug('Cache hit: source test script found in cache')
    p_utils.log_file_time(f'{subject.name}_src_program_run.{subject.src_lang}', src_program_run)
    return _CACHE_RUN_SRC_TS[src_program_run]

  p_utils.log_file_time(f'{subject.name}_src_program_run.{subject.src_lang}', src_program_run)
  stdout, stderr = await _run_code(src_program_run, subject.src_lang)
  src_trace = _extract_trace_from_stdout(stdout)

  if len(_CACHE_RUN_SRC_TS) > _CACHE_RUN_SRC_TS_SIZE:
    logger.debug('Cache size exceeded, clearing cache')
    _CACHE_RUN_SRC_TS.clear()

  _CACHE_RUN_SRC_TS[src_program_run] = (src_trace, stderr)
  return src_trace, stderr


async def run_tar_test_script(
  tar_program_instr: str,
  subject: p_subject.PirelSubject,
) -> Tuple[list, str]:
  '''
  This function runs the target program until the log list mismatch
  and returns the concatenated code, log list, and error if any.
  '''
  logger.debug('Running target test script')

  mylog_impl = get_mylog_impl(subject.tar_lang)
  tar_program_run = mylog_impl + comment_out_default_mylog_impls(tar_program_instr, subject.tar_lang)

  p_utils.log_file_time(f'{subject.name}_tar_program_run.{subject.tar_lang}', tar_program_run)
  stdout, stderr = await _run_code(tar_program_run, subject.tar_lang)
  tar_trace = _extract_trace_from_stdout(stdout)

  return tar_trace, stderr


# TEST HARNESSES
async def _test_run_src_test_script():
  '''
  async def run_src_test_script(
    src_program_instr: str,
    subject: p_subject.PirelSubject
  ) -> Tuple[list, Optional[dict]]:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_run_src_test_script_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  src_program_instr = args_dict['src_program_instr']
  subject = p_subject.PirelSubject.from_dict(args_dict['subject'])

  result = asyncio.run(run_src_test_script(src_program_instr, subject))
  print(json.dumps(result, indent=2))


async def _test_run_tar_test_script():
  '''
  async def run_tar_program_until_mylog_mismatch(
    tar_program_instr: str,
    subject: p_subject.PirelSubject,
  ) -> Tuple[str, list, Optional[dict]]:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_run_tar_test_script_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  tar_program_instr = args_dict['tar_program_instr']
  subject = p_subject.PirelSubject.from_dict(args_dict['subject'])

  result = asyncio.run(run_tar_test_script(tar_program_instr, subject))
  print(json.dumps(result, indent=2))


if __name__ == '__main__':
  _test_run_src_test_script()
  # _test_run_tar_test_script()
