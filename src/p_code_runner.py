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


# the following snippets of code are inserted
# into `tar_program` to log input and output to the program under test
# `MYLOG_IMPL_XX` is for `src_program`
# `MYLOG_MATCH_IMPL_XX` is for `tar_program`
# TODO those starting with underscore are not implemented yet
_MYLOG_IMPL_JS = '''
"use strict";
function mylog_obj_to_comp(arg) {
  let typearg = typeof arg;
  if (arg === true || arg === false) return ["bool", arg];
  else if (typearg === "number") return ["num", arg];
  else if (typearg === "string") return ["string", arg.length, arg.length < 10 ? arg : arg.slice(0,10)];
  else if (Array.isArray(arg)) return ["list", arg.length, arg.length > 0 ? mylog_obj_to_comp(arg[0]) : "EMPTY", arg.length > 1 ? mylog_obj_to_comp(arg[1]) : "EMPTY"];
  else if (arg === null || arg === undefined) return ["none"];
  else return ["Unknown"];
}
function mylog() {
  let info_list = ["MYLOG:" + arguments[0]];
  for (let i = 1; i < arguments.length; i++) {
    info_list.push(mylog_obj_to_comp(arguments[i]));
  }
  console.log("\\n" + JSON.stringify(info_list));
}
function myexactlog() {
  mylog(...arguments);
}
'''

MYLOG_MATCH_IMPL_JS = '''
"use strict";
const SKIP_LOGGING = false;
const MYLOG_LIST = {MYLOG_LIST};
let _console_log = console.log;
let mylog_callcount = 0;
function _list_compare(ls1, ls2) {
  if (ls1.length !== ls2.length) return false;
  if (ls1.length > 0 && ls1[0] === "num" && ls2.length > 0 && ls2[0] === "num") {
    if (ls1[1] === ls2[1]) return true;
    else {
      try {
        if (Math.abs(ls1[1]) > 1e-6 && Math.abs(ls2[1]) > 1e-6) {
          if (Math.abs(ls1[1]) > 2 * Math.abs(ls2[1])) return false;
          else if (2 * Math.abs(ls1[1]) < Math.abs(ls2[1])) return false;
          else if (Math.abs(Math.abs(ls1[1] / ls2[1]) - 1) > 1e-6) return false;
          else return true;
        }
        else if (Math.abs(ls1[1]) <= 1e-6 && Math.abs(ls2[1]) <= 1e-6) return true;
        else return false;
      } catch (e) {
        throw Error("MyLogError _list_compare num error: " + ls1 + " <==> " + ls2 + " " + e);
      }
    }
  }
  else if (ls1.length > 0 && ls1[0] === "string" && ls2.length > 0 && ls2[0] === "Unknown") {
    return ls1[2] === ls2[2];
  }
  let anyDiff = false;
  for (let i = 0; i < ls1.length; i++) {
    let ls1e = ls1[i], ls2e = ls2[i];
    if (Array.isArray(ls1e) && Array.isArray(ls2e)) {
      let elem_anydiff = !_list_compare(ls1e, ls2e);
      anyDiff = anyDiff || elem_anydiff;
    }
    else anyDiff = anyDiff || (ls1e !== ls2e);
    if (anyDiff) break;
  }
  return !anyDiff;
}
function mylog_obj_to_comp(is_exact, arg) {
  let typearg = typeof arg;
  if (arg === true || arg === false) return ["bool", arg];
  else if (typearg === "number") return ["num", arg];
  else if (typearg === "string") {
    if (is_exact) return ["string", arg.length, arg];
    else return ["string", arg.length, arg.length < 10 ? arg : arg.slice(0,10)];
  }
  else if (Array.isArray(arg)) {
    if (is_exact) return ["list", arg.length, arg.map(x => mylog_obj_to_comp(is_exact, x))];
    else return ["list", arg.length, arg.length > 0 ? mylog_obj_to_comp(is_exact, arg[0]) : "EMPTY", arg.length > 1 ? mylog_obj_to_comp(is_exact, arg[1]) : "EMPTY"];
  }
  else if (arg === null || arg === undefined) return ["none"];
  else {
    let str_result = String(arg);
    return ["Unknown", str_result.length, str_result];
  }
}
function sortKeysReplacer(key, value) {
  if (value && typeof value === "object" && !Array.isArray(value)) {
    return Object.keys(value)
      .sort() // Sort the keys alphabetically
      .reduce((sortedObj, sortedKey) => {
        sortedObj[sortedKey] = value[sortedKey];
        return sortedObj;
      }, {});
  }
  return value; // Return the value as-is for non-objects
}
function _mylog() {
  let is_exact = arguments[0];
  let prefix = is_exact ? "MYLOGEX:" : "MYLOGAP:";
  let info_list = [prefix + JSON.stringify(arguments[1], sortKeysReplacer)];
  if (SKIP_LOGGING === true && arguments[1] === -1) return;
  for (let i = 2; i < arguments.length; i++) {
    info_list.push(mylog_obj_to_comp(is_exact, arguments[i]));
  }
  _console_log("\\n" + JSON.stringify(info_list));
  while (SKIP_LOGGING === true && mylog_callcount < MYLOG_LIST.length && MYLOG_LIST[mylog_callcount][0].endsWith(":-1")) {
    mylog_callcount += 1;
  }
  if (mylog_callcount >= MYLOG_LIST.length) {
    throw Error("MyLogError MYLOG_LENGTH_EXCEEDED COUNT:" + String(mylog_callcount) + " CALL_ID:" + String(arguments[0]));
  }
  else {
    if (_list_compare(info_list, MYLOG_LIST[mylog_callcount])) {
      mylog_callcount += 1;
      return;
    } else {
      throw Error("MyLogError MISMATCH CALL_ID:" + String(arguments[1])
        + " MISMATCH_IDX:" + String(mylog_callcount)
        + " OBSERVED:" + JSON.stringify(info_list)
        + " EXPECTED:" + JSON.stringify(MYLOG_LIST[mylog_callcount]));
    }
  }
}
function mylog() {
  _mylog(false, ...arguments);
}
function myexactlog() {
  _mylog(true, ...arguments);
}
console.log = function () {
  myexactlog(-1, [...arguments]);
  _console_log(...arguments);
}
'''

MYLOG_IMPL_PY = '''
import json
_default_print = print
def mylog_obj_to_comp(is_exact, arg):
  if isinstance(arg, bool): return ["bool", arg]
  elif isinstance(arg, str):
    if is_exact:
      return ["string", len(arg), arg]
    else:
      return ["string", len(arg), arg if len(arg) < 10 else arg[0:10]]
  elif isinstance(arg, int) or isinstance(arg, float): return ["num", arg]
  elif isinstance(arg, list) or isinstance(arg, tuple):
    if is_exact:
      return ["list", len(arg), [mylog_obj_to_comp(is_exact, x) for x in arg]]
    else:
      return ["list", len(arg), mylog_obj_to_comp(is_exact, arg[0]) if len(arg) > 0 else "EMPTY", mylog_obj_to_comp(is_exact, arg[1]) if len(arg) > 1 else "EMPTY"]
  elif arg is None: return ["none"]
  else:
    str_result = str(arg)
    return ["Unknown", len(str_result), str_result]
def _mylog(is_exact, *args):
  prefix = "MYLOGEX:" if is_exact else "MYLOGAP:"
  info_list = [prefix + json.dumps(args[0], sort_keys=True, separators=(',', ':'))]
  for arg in args[1:]:
    info_list.append(mylog_obj_to_comp(is_exact, arg))
  _default_print("\\n" + json.dumps(info_list))
def mylog(*args):
  _mylog(False, *args)
def myexactlog(*args):
  _mylog(True, *args)
def print(*args, **kargs):
  myexactlog(-1, args)
  return _default_print(*args, **kargs)
'''

_MYLOG_MATCH_IMPL_PY = '''
MYLOG_LIST = {MYLOG_LIST}
import json
mylog_callcount = 0
def _list_compare(ls1, ls2):
  raise NotImplementedError
def mylog_obj_to_comp(arg):
  if isinstance(arg, bool): return ["bool", arg]
  elif isinstance(arg, str): return ["string", len(arg), arg if len(arg) < 10 else arg[0:10]]
  elif isinstance(arg, int) or isinstance(arg, float): return ["num", arg]
  elif isinstance(arg, list) or isinstance(arg, tuple): return ["list", len(arg), mylog_obj_to_comp(arg[0]) if len(arg) > 0 else "EMPTY", mylog_obj_to_comp(arg[1]) if len(arg) > 1 else "EMPTY"]
  elif arg is None: return ["none"]
  else: return ["Unknown"]
def mylog(*args):
  info_list = ["MYLOG:" + str(args[0])]
  for arg in args[1:]:
    info_list.append(mylog_obj_to_comp(arg))
  print("\\n" + json.dumps(info_list))
  if _list_compare(info_list, MYLOG_LIST[mylog_callcount]):
    mylog_callcount += 1
    return
  else:
    raise Exception("MyLogError CALL_ID:" + str(args[0]) + " MISMATCH_IDX:" + str(mylog_callcount))
def myexactlog(*args):
  mylog(*args)
'''

MYLOG_IMPL = {
  'py': MYLOG_IMPL_PY
}

MYLOG_MATCH_IMPL = {
  'js': MYLOG_MATCH_IMPL_JS,
}


CODE_RUN_COMMANDS = {
  'py': 'python {filename}',
  'js': 'node {filename}'
}

TMP_DIR = Path('/tmp/pirel_code_runner')
TMP_DIR.mkdir(exist_ok=True)


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
  return stdout, stderr


def comment_out_tester_ph(code: str, lang: str) -> str:
  logger.debug('Starting p_code_runner.comment_out_tester_ph')
  assert lang in p_consts.LANG_DICT, f'Unsupported language: {lang}'

  _SPLITTER = '\n"+++++++++++++++++"\n'

  if lang == 'py':
    splits = code.split(_SPLITTER)
    if len(splits) == 1:
      return code
    assert len(splits) == 2
    to_comment_out, rest = splits
    commented_out = '\n'.join(['# ' + line for line in to_comment_out.split('\n')])
    return commented_out + _SPLITTER + rest

  if lang == 'js':
    splits = code.split(_SPLITTER)
    if len(splits) == 1:
      return code
    assert len(splits) == 2
    to_comment_out, rest = splits
    commented_out = '\n'.join(['// ' + line for line in to_comment_out.split('\n')])
    return commented_out + _SPLITTER + rest


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

  assert subject.src_lang in MYLOG_IMPL, f'mylog for {subject.src_lang} is not implemented.'
  src_program_run = MYLOG_IMPL[subject.src_lang] + comment_out_tester_ph(src_program_instr, subject.src_lang)

  p_utils.log_file_time(f'{subject.name}_src_program_run.{subject.src_lang}', src_program_run)
  stdout, stderr = _run_code(src_program_run, subject.src_lang)

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
  logger.debug('Starting p_code_runner.run_tar_program_until_mylog_mismatch')

  assert subject.tar_lang in MYLOG_MATCH_IMPL, f'mylog (match) for {subject.tar_lang} is not implemented.'
  concode_prepart = MYLOG_MATCH_IMPL[subject.tar_lang].replace('{MYLOG_LIST}', json.dumps(src_log))
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
