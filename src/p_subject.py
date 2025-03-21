import json
from typing import Optional

import p_consts
import p_utils


logger = p_utils.setup_logger(__name__)


class PirelSubject:
  '''
  Instances of this class store configurations for a single subject in PiREL benchmarks.

  translation_rules_main_code - translation rules that were learned
  by PiREL from translating `src_program` to the target language.
  We want to validate and apply these rules.

  translation_rules_test_code - translation rules that are
  hand-written by DuoGlot authors to translate the test code.
  If `None`, then `src_program` does not have test code.

  translation_rules_instr_src - translation rules that are
  hand-written by DuoGlot authors to instrument the source program.

  translation_rules_instr_tar - translation rules that are
  hand-written by DuoGlot authors to de-instrument the target program.

  is_three_split - if `True`, then `src_program` is split into
  three parts: test code, main code, and test call code.
  Current `is_three_split` benhmarks are "GFG" and "Leetcode".

  is_mylog_inserted - if `True`, then `src_test_code` is already
  instrumented with `mylog` invocations. For this flag to work,
  `needs_instrumentation` must be `True`. If `needs_instrumentation`
  is `False`, then `is_mylog_inserted` has no effect. The only benchmark
  in `mylog` invocations are already present is "Leetcode".

  needs_instrumentation - if `True`, then `src_program` needs
  instrumentation. If `False`, then the subject already comes with
  necessary print statements or assertions that allow validation
  of the translation rules. The only benchmark that does not need
  instrumentation is "CTCI".
  '''
  def __init__(
    self,
    benchmark_name: str,  # leetcode | gfg | ctci
    name: str,  # L0001
    src_program: str,  # test_code + main_code + test_call_code | main_code
    src_lang: str,  # py
    tar_lang: str,  # js
  ):
    logger.debug('Initializing PirelSubject instance')
    assert benchmark_name in p_consts.BENCHMARK_CONFIGS

    # ATTRIBUTES PASSED BY CONSTRUCTOR
    self.benchmark_name = benchmark_name
    self.name = name
    self.src_program = src_program
    self.src_lang = src_lang
    self.tar_lang = tar_lang

    # ATTRIBUTES WITH DEFAULT VALUES (PER DUOGLOT)
    self.auto_backward = True
    self.choices = {'type': 'ASTNODE', 'choices_list': []}

    # ATTRIBUTES LOADED FROM CONFIGS
    self.translation_rules_test_code = self._load_tr_test_code(benchmark_name)
    self.translation_rules_instr_src = self._load_tr_instr_src(benchmark_name)
    self.translation_rules_instr_tar = self._load_tr_instr_tar(benchmark_name)

    self.is_three_split = p_consts.BENCHMARK_CONFIGS[benchmark_name]['is_three_split']
    self.is_mylog_inserted = p_consts.BENCHMARK_CONFIGS[benchmark_name]['is_mylog_inserted']
    self.needs_instrumentation = p_consts.BENCHMARK_CONFIGS[benchmark_name]['needs_instrumentation']

    # COMPUTED ATTRIBUTES
    self.is_long_requires_processing = self._get_is_long_requires_processing()
    if self.is_long_requires_processing:
      self._translation_rules_process_for_long_source()

    # src_program contains the entire subject code,
    # which may include test code, main code, and test call code.
    if self.is_three_split:
      assert self.src_program.count(p_consts.TEST_MAIN_CALL_DELIMITER) == 2
      _tmc_splits = self.src_program.split(p_consts.TEST_MAIN_CALL_DELIMITER)
      self.src_test_code = _tmc_splits[0]
      self.src_main_code = _tmc_splits[1]
      self.src_test_call_code = _tmc_splits[2]
    else:
      assert p_consts.TEST_MAIN_CALL_DELIMITER not in self.src_program
      self.src_test_code = None
      self.src_main_code = self.src_program
      self.src_test_call_code = None

    # this must be set to the translation rules learned by PiREL
    self.translation_rules_main_code = None

  def __str__(self) -> str:
    attrs = {
      'benchmark_name': self.benchmark_name,
      'name': self.name,
      'src_program': self.src_program,
      'src_lang': self.src_lang,
      'tar_lang': self.tar_lang,
    }
    return json.dumps(attrs)

  def __repr__(self) -> str:
    return f'PirelSubject({self.name})'

  def _load_tr_test_code(self, benchmark_name: str) -> Optional[str]:
    '''Load translation rules for the test code'''
    benchmark_conf = p_consts.BENCHMARK_CONFIGS[benchmark_name]
    translation_rules_test_code = p_utils.read_text_or_none(benchmark_conf['translation_rules_test_code_fpath'])
    return translation_rules_test_code

  def _load_tr_instr_src(self, benchmark_name: str) -> Optional[str]:
    '''Load translation rules for the source program instrumentation'''
    benchmark_conf = p_consts.BENCHMARK_CONFIGS[benchmark_name]
    translation_rules_instr_src = p_utils.read_text_or_none(benchmark_conf['translation_rules_instr_src_fpath'])
    return translation_rules_instr_src

  def _load_tr_instr_tar(self, benchmark_name: str) -> Optional[str]:
    '''Load translation rules for the target program de-instrumentation'''
    benchmark_conf = p_consts.BENCHMARK_CONFIGS[benchmark_name]
    translation_rules_instr_tar = p_utils.read_text_or_none(benchmark_conf['translation_rules_instr_tar_fpath'])
    return translation_rules_instr_tar

  def _has_all_translation_rules_set(self) -> bool:
    assert self.translation_rules_main_code is not None
    if self.translation_rules_instr_src is None:
      return False
    if self.translation_rules_test_code is None:
      return False
    if self.translation_rules_instr_tar is None:
      return False
    return True

  def _is_long_source(self) -> bool:
    if len(self.src_program) > p_consts.LONG_SRC_PROGRAM_THRESHOLD:
      return True
    return False

  def _get_is_long_requires_processing(self) -> bool:
    logger.debug('checking if `src_program` is long and subject needs special processing')
    if not self._is_long_source():
      logger.debug('`src_program` is not long: <= 5000 characters')
      return False
    if not self._has_all_translation_rules_set():
      logger.debug('some of the translation rules are not set')
      return False
    logger.debug('subject requires special processing')
    return True

  def _translation_rules_process_for_long_source(self) -> None:
    '''
    NOTE writes to some attributes of `self`
    '''
    logger.debug('subject is long and requires special processing')
    assert p_consts.PARAM_HACK_FLAG in self.translation_rules_instr_src, 't.r._instr_src does not support long files'
    assert p_consts.PARAM_HACK_FLAG in self.translation_rules_test_code, 't.r._test_code does not support long files'
    assert p_consts.PARAM_HACK_FLAG in self.translation_rules_instr_tar, 't.r._instr_tar does not support long files'
    self.translation_rules_instr_src = self.translation_rules_instr_src.replace(p_consts.PARAM_HACK_FLAG, '')
    self.translation_rules_test_code = self.translation_rules_test_code.replace(p_consts.PARAM_HACK_FLAG, '')
    self.translation_rules_instr_tar = self.translation_rules_instr_tar.replace(p_consts.PARAM_HACK_FLAG, '')
