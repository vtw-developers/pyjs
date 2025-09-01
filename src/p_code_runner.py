import asyncio
import json
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


def _extract_err_from_stderr_JS(stderr: str, lang: str) -> dict:
  '''
  Parse the error message from the stderr of the JS code.

  Sample stderr:
  ```
  /tmp/pirel_code_runner/706fcc78.js:177
      if (id_px.has(id_shcx)) {
                ^

  TypeError: id_px.has is not a function
      at f_gold (/tmp/pirel_code_runner/706fcc78.js:177:15)
      at test (/tmp/pirel_code_runner/706fcc78.js:172:9)
      at Object.<anonymous> (/tmp/pirel_code_runner/706fcc78.js:184:1)
      at Module._compile (node:internal/modules/cjs/loader:1375:14)
      at Module._extensions..js (node:internal/modules/cjs/loader:1434:10)
      at Module.load (node:internal/modules/cjs/loader:1206:32)
      at Module._load (node:internal/modules/cjs/loader:1022:12)
      at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:142:12)
      at node:internal/main/run_main_module:28:49

  Node.js v21.5.0
  ```
  '''

  def __get_error_type(stderr: str) -> str:
    # works in conjuction with `p_ext_rule_chooser.get_proposed_choices_compile_error()`
    _SUPPORTED_ERROR_TYPES_JS = [
      'SyntaxError:',
      'ReferenceError:',
      'TypeError:'
    ]

    error_type = None
    for _et in _SUPPORTED_ERROR_TYPES_JS:
      if _et in stderr:
        error_type = _et
        break

    # new error type identified
    if error_type is None:
      msg = f'_extract_err_from_stderr_JS: Unknown error type in stderr: {stderr}'
      logger.error(msg)
      raise RuntimeError(msg)

    return error_type

  logger.debug('Starting p_code_runner._extract_err_from_stderr')
  assert lang == 'js', f'Unsupported language: {lang}'
  assert str(TMP_DIR) in stderr, f'Expected "{TMP_DIR}" in stderr: {stderr}'

  error_type = __get_error_type(stderr)
  splits = stderr.split(error_type)
  assert len(splits) == 2, f'Unexpected error format in stderr: {stderr}'
  error_loc_lines = splits[0].strip().split('\n')

  if error_loc_lines[0].startswith(str(TMP_DIR)):

    fpath_and_line_num = error_loc_lines[0].split(':')
    line_content = error_loc_lines[1].strip()
    assert len(fpath_and_line_num) == 2
    file_path = fpath_and_line_num[0]
    # line number in stderr is 1-based
    line_num = int(fpath_and_line_num[1])

    mylog_impl = get_mylog_impl(lang)
    line_num_shift = len(mylog_impl.split('\n')) - 1
    line_num = line_num - line_num_shift

  else:
    raise RuntimeError('Error location not found in stderr')

  error_lines = splits[1].strip().split('\n')
  error_msg = error_lines[0]
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
  try:
    proc = await asyncio.create_subprocess_exec(
      command, temp_filename, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
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
    p_utils.log_file_time(f'{lang}-stdout.txt', stdout)
    logger.debug(f'{lang} stderr: "\n{stderr.strip()}\n"')
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

  p_utils.log_file_time(f'{subject.name}_src_program_run.{subject.src_lang}', src_program_run)
  stdout, stderr = await _run_code(src_program_run, subject.src_lang)
  src_trace = _extract_trace_from_stdout(stdout)

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
  subject = p_subject.PirelSubject.from_dict(json.loads(args_dict['subject']))

  result = await run_src_test_script(src_program_instr, subject)
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
  subject = p_subject.PirelSubject.from_dict(json.loads(args_dict['subject']))

  result = await run_tar_test_script(tar_program_instr, subject)
  print(json.dumps(result, indent=2))


if __name__ == '__main__':
  asyncio.run(_test_run_src_test_script())
  # asyncio.run(_test_run_tar_test_script())
