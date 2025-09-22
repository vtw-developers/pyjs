import json
from pathlib import Path

import d_grammar
from tree_sitter import Language, Parser

################################################################################################
#################################### DIRECTORIES ###############################################
################################################################################################
SRC_DIR = Path(__file__).parent
ROOT_DIR = SRC_DIR.parent

BENCHMARKS_DIR = ROOT_DIR / 'benchmarks'
BUILD_DIR = ROOT_DIR / 'build'
CONFIGS_DIR = ROOT_DIR / 'conf'
EXPERIMENTS_DIR = ROOT_DIR / 'experiments'
LOGS_DIR = ROOT_DIR / 'logs'
MYLOG_DEFINITIONS_DIR = ROOT_DIR / 'mylog-definitions'
TEST_ARTIFACTS_DIR = ROOT_DIR / 'test-artifacts'
TMP_DIR = ROOT_DIR / 'tmp'
TRANSLATION_RULES_DIR = ROOT_DIR / 'translation-rules'
TREE_SITTER_GRAMMARS_DIR = ROOT_DIR / 'tree-sitter-util'

DUOGLOT_LOGS_DIR = LOGS_DIR / 'duoglot'
LEARN_RULES_LOGS_DIR = LOGS_DIR / 'learn-rules'
PIREL_LOGS_DIR = LOGS_DIR / 'pirel'

LEARN_APPLY_RULES_CONFIGS_DIR = CONFIGS_DIR / 'p-learn-apply-rules'
PIREL_SUBJECT_CONFIGS_DIR = CONFIGS_DIR / 'pirel-subject'


################################################################################################
#################################### ENVIRONMENT ###############################################
################################################################################################
ENV_FILE = ROOT_DIR / '.env.json'


################################################################################################
#################################### TREESITTER RELATED ########################################
################################################################################################
_language_paths = [
  TREE_SITTER_GRAMMARS_DIR / 'tree-sitter-javascript',
  TREE_SITTER_GRAMMARS_DIR / 'tree-sitter-python'
]
Language.build_library(BUILD_DIR / 'my-languages.so', _language_paths)

_py_language = Language(BUILD_DIR / 'my-languages.so', 'python')
_js_language = Language(BUILD_DIR / 'my-languages.so', 'javascript')

_py_parser = Parser()
_js_parser = Parser()

_py_parser.set_language(_py_language)
_js_parser.set_language(_js_language)

PARSER_DICT = {
  'py': _py_parser,
  'js': _js_parser
}


################################################################################################
#################################### GRAMMAR RELATED ###########################################
################################################################################################
with open(_language_paths[1] / 'src' / 'grammar.json') as fin:
  grammar_contents = fin.read()
  _py_grammar = json.loads(grammar_contents)
  _py_grammar_readonly = json.loads(grammar_contents)
with open(_language_paths[0] / 'src' / 'grammar.json') as fin:
  grammar_contents = fin.read()
  _js_grammar = json.loads(grammar_contents)
  _js_grammar_readonly = json.loads(grammar_contents)

d_grammar.grm_preprocess('py', _py_grammar)
d_grammar.grm_preprocess('js', _js_grammar)

GRAMMAR_DICT = {
  'py': _py_grammar,
  'js': _js_grammar
}

GRAMMAR_DICT_READONLY = {
  'py': _py_grammar_readonly,
  'js': _js_grammar_readonly
}

PY_NOT_INLINED_NTS = d_grammar.grm_get_all_not_inlined_NTs(_py_grammar)
JS_NOT_INLINED_NTS = d_grammar.grm_get_all_not_inlined_NTs(_js_grammar)

NT_DICT = {
  'py': PY_NOT_INLINED_NTS,
  'js': JS_NOT_INLINED_NTS
}


################################################################################################
#################################### PIREL CONFIGS #############################################
################################################################################################
GENERIC_SECRET_FN = 'secret_fun_4071'
GENERIC_SECRET_FN_INVOCATION = GENERIC_SECRET_FN + '()'
PAR_PROG_PROB_NODE_REPLACE = 'pirel_replace_var'
PAR_PROG_DUMMY_IDENTIFIER = 'pirel_dummy_var'

# Maximum number of TSPs from which some rules are learned
MAX_NUM_USEFUL_TSPS = 1

# Maximum number of AST node groups fuzzed for TSP generation
MAX_FUZZ_GROUP_LEN = 1000

# Maximum number of concurrent subjects to learn rules for
MAX_CONCURRENT_SUBJECTS = 1000

# When comparing traces, max percentage difference between two numbers
# to be considered equal
EPS_PERCENTAGE = 0.01


################################################################################################
############################# TSP GENERATION ###################################################
################################################################################################
BODY_NODE_TYPES = {
  'py': ['block', 'list', 'dictionary']
}
ENABLE_SPECIAL_TREATMENT_FOR_BODY_NODE_TYPES = True
SPECIAL_TREATMENT_BODY_NODE_TYPES = {
  'py': {
    'block': GENERIC_SECRET_FN_INVOCATION,
    'list': '[' + GENERIC_SECRET_FN_INVOCATION + ']',
    'dictionary': '{' + f'foo: {GENERIC_SECRET_FN_INVOCATION}' + '}'
  }
}

BASIC_NODE_TYPES = {
  'py': ['identifier', 'integer', 'float']
}

# When set to True, the generator will generate `identifier` node
# if the `mapped_node` is of type `identifier`.
IS_FORCE_IDENTIFIERS = True

NON_DESCENDABLE_NODES = {
  'py': ['string']
}

FN_NAMES_WITH_NON_EMPTY_ARGUMENT_LIST = {
  'py': [
    'abs', 'all', 'any', 'chr', 'divmod', 'enumerate', 'float', 'len',
    'min', 'max','ord', 'pow', 'range', 'reversed', 'round', 'sorted', 'sum'
    ]
}

REMOVE_FROM_FUZZ_NODE_GROUPS_NODE_TYPES = {
  'py': ['call', 'keyword_argument'],
}

# For the following node types we include (`template_origin`, `template_origin`)
# as a TSP. This allows us to learn the most overfitted translation rules for them,
# and avoid errors. This is applicable in such case:
# `problematic_node` is `string` and `template_origin` is `dfs(0, 0, '')`
# Translation rules for empty strings and non-empty strings are different.
# However, the generator generates non-empty strings, and this does not let us
# learn the translation rule for empty strings.
# This is a workaround to avoid such issues.
DO_NOT_GENERATE_TSPS_FOR_NODE_TYPES = {
  'py': ['string', 'slice']
}

PY_BUILT_IN_FUNCTIONS = {
  'abs', 'aiter', 'all', 'anext', 'any', 'ascii', 'bin', 'bool', 'breakpoint',
  'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex',
  'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'filter',
  'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help',
  'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'list',
  'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open',
  'ord', 'pow', 'print', 'property', 'range', 'repr', 'reversed', 'round', 'set',
  'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple',
  'type', 'vars', 'zip'
}

PY_BUILT_IN_MODULES = {
  '__future__', '__main__', '_thread', '_tkinter', 'abc', 'aifc', 'argparse', 'array',
  'ast', 'asynchat', 'asyncio', 'asyncore', 'atexit', 'audioop', 'base64', 'bdb',
  'binascii', 'bisect', 'builtins', 'bz2', 'calendar', 'cgi', 'cgitb', 'chunk',
  'cmath', 'cmd', 'code', 'codecs', 'codeop', 'collections', 'collections.abc',
  'colorsys', 'compileall', 'concurrent.futures', 'configparser', 'contextlib',
  'contextvars', 'copy', 'copyreg', 'cProfile', 'crypt', 'csv', 'ctypes', 'curses',
  'curses.ascii', 'curses.panel', 'curses.textpad', 'dataclasses', 'datetime',
  'dbm', 'dbm.dumb', 'dbm.gnu', 'dbm.ndbm', 'dbm.sqlite3', 'decimal', 'difflib',
  'dis', 'distutils', 'doctest', 'email', 'email.charset', 'email.contentmanager',
  'email.encoders', 'email.errors', 'email.generator', 'email.header',
  'email.headerregistry', 'email.iterators', 'email.message', 'email.mime',
  'email.mime.application', 'email.mime.audio', 'email.mime.base',
  'email.mime.image', 'email.mime.message', 'email.mime.multipart',
  'email.mime.nonmultipart', 'email.mime.text', 'email.parser', 'email.policy',
  'email.utils', 'encodings.idna', 'encodings.mbcs', 'encodings.utf_8_sig',
  'ensurepip', 'enum', 'errno', 'faulthandler', 'fcntl', 'filecmp', 'fileinput',
  'fnmatch', 'fractions', 'ftplib', 'functools', 'gc', 'getopt', 'getpass',
  'gettext', 'glob', 'graphlib', 'grp', 'gzip', 'hashlib', 'heapq', 'hmac',
  'html', 'html.entities', 'html.parser', 'http', 'http.client', 'http.cookiejar',
  'http.cookies', 'http.server', 'idlelib', 'imaplib', 'imghdr', 'imp', 'importlib',
  'importlib.abc', 'importlib.machinery', 'importlib.metadata',
  'importlib.resources', 'importlib.resources.abc', 'importlib.util', 'inspect',
  'io', 'ipaddress', 'itertools', 'json', 'json.tool', 'keyword', 'linecache',
  'locale', 'logging', 'logging.config', 'logging.handlers', 'lzma', 'mailbox',
  'mailcap', 'marshal', 'math', 'mimetypes', 'mmap', 'modulefinder', 'msilib',
  'msvcrt', 'multiprocessing', 'multiprocessing.connection', 'multiprocessing.dummy',
  'multiprocessing.managers', 'multiprocessing.pool', 'multiprocessing.shared_memory',
  'multiprocessing.sharedctypes', 'netrc', 'nis', 'nntplib', 'numbers', 'operator',
  'optparse', 'os', 'os.path', 'ossaudiodev', 'pathlib', 'pdb', 'pickle',
  'pickletools', 'pipes', 'pkgutil', 'platform', 'plistlib', 'poplib', 'posix',
  'pprint', 'profile', 'pstats', 'pty', 'pwd', 'py_compile', 'pyclbr', 'pydoc',
  'queue', 'quopri', 'random', 're', 'readline', 'reprlib', 'resource',
  'rlcompleter', 'runpy', 'sched', 'secrets', 'select', 'selectors', 'shelve',
  'shlex', 'shutil', 'signal', 'site', 'sitecustomize', 'smtpd', 'smtplib',
  'sndhdr', 'socket', 'socketserver', 'spwd', 'sqlite3', 'ssl', 'stat', 'statistics',
  'string', 'stringprep', 'struct', 'subprocess', 'sunau', 'symtable', 'sys',
  'sys.monitoring', 'sysconfig', 'syslog', 'tabnanny', 'tarfile', 'telnetlib',
  'tempfile', 'termios', 'test', 'test.regrtest', 'test.support',
  'test.support.bytecode_helper', 'test.support.import_helper',
  'test.support.os_helper', 'test.support.script_helper',
  'test.support.socket_helper', 'test.support.threading_helper',
  'test.support.warnings_helper', 'textwrap', 'threading', 'time', 'timeit',
  'tkinter', 'tkinter.colorchooser', 'tkinter.commondialog', 'tkinter.dnd',
  'tkinter.filedialog', 'tkinter.font', 'tkinter.messagebox', 'tkinter.scrolledtext',
  'tkinter.simpledialog', 'tkinter.ttk', 'token', 'tokenize', 'tomllib', 'trace',
  'traceback', 'tracemalloc', 'tty', 'turtle', 'turtledemo', 'types', 'typing',
  'unicodedata', 'unittest', 'unittest.mock', 'urllib', 'urllib.error',
  'urllib.parse', 'urllib.request', 'urllib.response', 'urllib.robotparser',
  'usercustomize', 'uu', 'uuid', 'venv', 'warnings', 'wave', 'weakref',
  'webbrowser', 'winreg', 'winsound', 'wsgiref', 'wsgiref.handlers', 'wsgiref.headers',
  'wsgiref.simple_server', 'wsgiref.types', 'wsgiref.util', 'wsgiref.validate',
  'xdrlib', 'xml', 'xml.dom', 'xml.dom.minidom', 'xml.dom.pulldom',
  'xml.etree.ElementInclude', 'xml.etree.ElementTree', 'xml.parsers.expat',
  'xml.parsers.expat.errors', 'xml.parsers.expat.model', 'xml.sax',
  'xml.sax.handler', 'xml.sax.saxutils', 'xml.sax.xmlreader', 'xmlrpc',
  'xmlrpc.client', 'xmlrpc.server', 'zipapp', 'zipfile', 'zipimport', 'zlib', 'zoneinfo'
}


################################################################################################
#################################### LLM CONFIGS ###############################################
################################################################################################
DEFAULT_MODEL_PARAMS = {
  'model_name': 'gpt-5',
  # 'model_name': 'gpt-5-nano',
  'temperature': 1.0,
  'max_completion_tokens': 16384,
  'request_timeout': None,
  'max_retries': 2,
}

TRANSLATION_SP1_MAX_RETRIES = 2
TRANSLATION_SP2_MAX_RETRIES = 2

TRANSLATION_SP1_MAX_FEEDBACKS = 2
TRANSLATION_SP2_MAX_FEEDBACKS = 2

# The number of attempts to learn translation rules from a single TSP
TSP_NUM_ATTEMPTS = 2


################################################################################################
#################################### BENCHMARKS ################################################
################################################################################################
TEST_MAIN_CALL_DELIMITER = '"-----------------"'
STARTING_RULESET_FPATH = TRANSLATION_RULES_DIR / 'starting-ruleset.snart'

GFG_BENCHMARK_DIR = BENCHMARKS_DIR / 'gfg' / 'py'
GFG_TRULES_MAIN_FPATH = TRANSLATION_RULES_DIR / 'main' / 'gfg.snart'
GFG_TRULES_TEST_FPATH = TRANSLATION_RULES_DIR / 'test' / 'gfg.snart'

BENCHMARK_CONFIGS = {
  'gfg': {
    'benchmark_dir': GFG_BENCHMARK_DIR,
    'translation_rules_main_code_fpath': GFG_TRULES_MAIN_FPATH,
    'translation_rules_test_code_fpath': GFG_TRULES_TEST_FPATH,
  },
  'skel': {
    'benchmark_dir': BENCHMARKS_DIR / 'skel',
    'translation_rules_main_code_fpath': GFG_TRULES_MAIN_FPATH,
    'translation_rules_test_code_fpath': GFG_TRULES_TEST_FPATH,
  },
}


################################################################################################
############################# TRANSLATION RULE VALIDATION ######################################
################################################################################################
PIREL_LOG_OBJ_FN_NAME = 'myexactlog'
TEST_SCRIPT_TEMPLATE = (
  '{test_code}\n'
  f'{TEST_MAIN_CALL_DELIMITER}\n'
  '{main_code}\n'
  f'{TEST_MAIN_CALL_DELIMITER}\n'
  '{test_call_code}'
)
LOG_STAT_RULE_FPATH = TRANSLATION_RULES_DIR / 'log-statement.snart'
RULE_VAL_EXTRA_RULES_FPATH = TRANSLATION_RULES_DIR / 'rule-validation-extra.snart'

PRE_CTX_SPEC_IDENT = 'pirel_pre_ctx_spec_identifier'
PRE_CTX_INSERT_BREAK_IN_LOOPS = True

GEN_TEST_FN_LLM_NUM_ATTEMPTS = 3
GEN_TEST_FN_LLM_FEEDBACKS = 3

GET_REF_TRANS_LLM_NUM_ATTEMPTS = 3
GET_REF_TRANS_LLM_FEEDBACKS = 3


################################################################################################
#################################### GENERAL CONFIGS ###########################################
################################################################################################
LANG_DICT = {
  'py': 'Python',
  'js': 'JavaScript'
}
