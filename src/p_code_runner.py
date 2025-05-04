import json
import os
import signal
import subprocess
from pathlib import Path
from typing import Optional, Tuple

import d_utils
import p_consts
import p_subject
import p_utils


logger = p_utils.setup_logger(__name__)


CODE_RUN_COMMANDS = {
  'py': 'python {filename}',
  'js': 'node {filename}'
}

TMP_DIR = Path('/tmp/pirel_code_runner')
TMP_DIR.mkdir(exist_ok=True)


def get_mylog_implementation(lang: str) -> str:
  '''
  Get the mylog implementation for the given language.
  '''
  assert lang in p_consts.LANG_DICT, f'Unsupported language: {lang}'
  mylog_fpath = p_consts.MYLOG_DEFINITIONS_DIR / lang / f'mylog.{lang}'
  assert mylog_fpath.exists(), f'Mylog implementation not found for {lang}'
  return p_utils.read_text(mylog_fpath)


def get_mylog_match_implementation(lang: str) -> str:
  '''
  Get the mylog match implementation for the given language.
  '''
  assert lang in p_consts.LANG_DICT, f'Unsupported language: {lang}'
  mylog_match_fpath = p_consts.MYLOG_DEFINITIONS_DIR / lang / f'mylog_match.{lang}'
  assert mylog_match_fpath.exists(), f'Mylog match implementation not found for {lang}'
  return p_utils.read_text(mylog_match_fpath)


def _get_temp_filename(text: str, lang: str) -> str:
  hexhash = d_utils.string_sha256(text)[:8]
  return TMP_DIR / f'{hexhash}.{lang}'


def _command_execute(command: str, timeout=10) -> None:
  try:
    logger.debug(f'Executing command: {command}')
    proc = subprocess.Popen(command, cwd=os.path.dirname(__file__), shell=True, preexec_fn=os.setsid)
    proc.wait(timeout)
  except Exception as exc:
    logger.debug(f'Error executing command: {command}')
    logger.debug(f'Error: {exc}')
    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    raise exc


def _extract_log_list_from_stdout(stdout: str, lang: str) -> list:
  mylog_lines = [line for line in stdout.split('\n') if line.startswith('["MYLOG')]
  return [json.loads(line) for line in mylog_lines]


def _extract_err_from_stderr(stderr: str, lang: str) -> Optional[dict]:
  logger.debug('Starting p_code_runner._extract_err_from_stderr')
  logger.debug('stderr: ' + stderr)

  _SPLITTERS_JS = [
    'SyntaxError:',
    'ReferenceError:',
    'Error: MyLogError',
    'Error: MyAssertError',
    'Error: MyTraceError',
    'TypeError:',
    'RangeError:',
    'Error: Cannot find module',
  ]

  assert lang in p_consts.LANG_DICT, f'Unsupported language: {lang}'

  if lang == 'js' and str(TMP_DIR) in stderr:
    # find the splitter
    splitter = None
    for s in _SPLITTERS_JS:
      if s in stderr:
        splitter = s
        break
    assert splitter is not None, f'Unknown error type in stderr: {stderr}'

    splitted = stderr.split(splitter)
    assert len(splitted) == 2, f'Unexpected error format in stderr: {stderr}'

    pos_lines = splitted[0].strip().split('\n')
    if pos_lines[0].startswith(str(TMP_DIR)):
      line_num_raw = pos_lines[0].split(':')
      assert len(line_num_raw) == 2
      line_num = [line_num_raw[0], int(line_num_raw[1])]
      line_content = pos_lines[1].strip()
    else:
      line_num = [pos_lines[0], -1] # not accurate
      line_content = 'NOT_IMPLEMENTED_DONT_KNOW'

    errorlines = splitted[1].strip().split('\n')
    error_msg = errorlines[0]
    return {
      'error_type': splitter,
      'error_msg': error_msg,
      'line_num': line_num,
      'line_content': line_content
    }

  if lang == 'py' and str(TMP_DIR) in stderr:
    raise NotImplementedError('Python error extraction is not implemented yet')


def _run_code(code: str, lang: str) -> Tuple[str, str]:
  '''
  Run the code and return stdout and stderr
  '''
  logger.debug('Starting p_code_runner._run_code')

  assert lang in p_consts.LANG_DICT, f'Unsupported language: {lang}'
  temp_filename = _get_temp_filename(code, lang)
  p_utils.write_text(temp_filename, code)

  runner_command = CODE_RUN_COMMANDS[lang].format(filename=temp_filename)
  redirect_suffix = f' >{temp_filename}.stdout 2>{temp_filename}.stderr'
  _command_execute(runner_command + redirect_suffix)

  stdout = p_utils.read_text(f'{temp_filename}.stdout')
  stderr = p_utils.read_text(f'{temp_filename}.stderr')

  logger.debug(f'stdout: "\n{stdout.strip()}\n"')
  logger.debug(f'stderr: "\n{stderr.strip()}\n"')
  logger.debug('Finished p_code_runner._run_code')

  return stdout, stderr


def comment_out_tester_ph(code: str, lang: str) -> str:
  assert lang in p_consts.LANG_DICT, f'Unsupported language: {lang}'

  _SPLITTER = '"+++++++++++++++++"'

  if lang == 'py':
    splits = code.split(_SPLITTER)
    if len(splits) == 1:
      return code
    assert len(splits) == 2
    to_comment_out, rest = splits
    commented_out = '\n'.join(['# ' + line for line in to_comment_out.split('\n') if line.strip() != ''])
    return commented_out + f'\n\n{_SPLITTER}\n\n' + rest

  if lang == 'js':
    splits = code.split(_SPLITTER)
    if len(splits) == 1:
      return code
    assert len(splits) == 2
    to_comment_out, rest = splits
    commented_out = '\n'.join(['// ' + line for line in to_comment_out.split('\n') if line.strip() != ''])
    return commented_out + f'\n\n{_SPLITTER}\n\n' + rest


_last_run_cached = None
def run_src_program_with_mylog(src_program_instr: str, subject: p_subject.PirelSubject) -> Tuple[list, Optional[dict]]:
  '''
  This function runs the source program with mylog and returns the log list and error if any.
  '''
  logger.debug('Starting p_code_runner.run_src_program_with_mylog')

  # check the cache first
  global _last_run_cached
  if _last_run_cached is not None and _last_run_cached[0] == src_program_instr and _last_run_cached[1] == subject.src_lang:
    logger.debug('run_src_program_with_mylog: using cached result')
    return _last_run_cached[2], _last_run_cached[3]

  mylog_implementation = get_mylog_implementation(subject.src_lang)
  src_program_run = mylog_implementation + comment_out_tester_ph(src_program_instr, subject.src_lang)

  p_utils.log_file_time(f'{subject.name}_src_program_run.{subject.src_lang}', src_program_run)
  stdout, stderr = _run_code(src_program_run, subject.src_lang)

  if stderr != '':
    logger.error('Test script in src_lang should run without errors.')

  src_log = _extract_log_list_from_stdout(stdout, subject.src_lang)
  src_error = _extract_err_from_stderr(stderr, subject.src_lang)

  _last_run_cached = (src_program_instr, subject.src_lang, src_log, src_error)

  return src_log, src_error


def run_tar_program_until_mylog_mismatch(
  tar_program_instr: str,
  subject: p_subject.PirelSubject,
  src_log: list,
  is_dry_run: bool
) -> Tuple[str, list, Optional[dict]]:
  '''
  This function runs the target program until the log list mismatch
  and returns the concatenated code, log list, and error if any.
  '''
  # commented to be used when necessary, actual args can be obtained
  # from running `p_rule_applicator.apply_translation_rules()`.
  # p_utils.log_json_time(f'{subject.name}_args-run_tar_program_until_mylog_mismatch.json', locals())
  logger.debug('Starting p_code_runner.run_tar_program_until_mylog_mismatch')

  mylog_match_implementation = get_mylog_match_implementation(subject.tar_lang)
  concode_prepart = mylog_match_implementation.replace('{MYLOG_LIST}', json.dumps(src_log))
  tar_program_run = concode_prepart + comment_out_tester_ph(tar_program_instr, subject.tar_lang)

  if is_dry_run:
    return tar_program_run, None, None

  p_utils.log_file_time(f'{subject.name}_tar_program_run.{subject.tar_lang}', tar_program_run)
  stdout, stderr = _run_code(tar_program_run, subject.tar_lang)

  tar_log = _extract_log_list_from_stdout(stdout, subject.tar_lang)
  tar_error = _extract_err_from_stderr(stderr, subject.tar_lang)

  if tar_error is not None and 'line_num' in tar_error:
    prepart_linecount = len(concode_prepart.split('\n')) - 1
    tar_error['line_num'][1] -= prepart_linecount

  return tar_program_run, tar_log, tar_error


# TEST HARNESSES
def _test_run_tar_program_until_mylog_mismatch():
  '''
  def run_tar_program_until_mylog_mismatch(
    tar_program_instr: str,
    subject: p_subject.PirelSubject,
    src_log: list,
    is_dry_run: bool
  ) -> Tuple[str, list, Optional[dict]]:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_run_tar_program_until_mylog_mismatch_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  tar_program_instr = args_dict['tar_program_instr']
  subject = p_subject.PirelSubject.from_dict_config(json.loads(args_dict['subject']))
  src_log = args_dict['src_log']
  is_dry_run = args_dict['is_dry_run']

  result = run_tar_program_until_mylog_mismatch(tar_program_instr, subject, src_log, is_dry_run)
  print(json.dumps(result, indent=2))


if __name__ == '__main__':
  _test_run_tar_program_until_mylog_mismatch()
