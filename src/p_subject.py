from __future__ import annotations

import json
from pathlib import Path
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

    assert benchmark_name is not None, 'benchmark_name is None'
    assert name is not None, 'name is None'
    assert src_program is not None, 'src_program is None'
    assert src_lang is not None, 'src_lang is None'
    assert tar_lang is not None, 'tar_lang is None'
    assert isinstance(benchmark_name, str), f'benchmark_name must be a string: {benchmark_name}'
    assert isinstance(name, str), f'name must be a string: {name}'
    assert isinstance(src_program, str), f'src_program must be a string: {src_program}'
    assert isinstance(src_lang, str), f'src_lang must be a string: {src_lang}'
    assert isinstance(tar_lang, str), f'tar_lang must be a string: {tar_lang}'
    assert src_lang in p_consts.LANG_DICT, f'src_lang is not supported: {src_lang}'
    assert tar_lang in p_consts.LANG_DICT, f'tar_lang is not supported: {tar_lang}'

    # ATTRIBUTES PASSED BY CONSTRUCTOR
    self.benchmark_name = benchmark_name
    self.name = name
    self.src_program = src_program
    self.src_lang = src_lang
    self.tar_lang = tar_lang

    # explicitly setting all attributes to none
    # to avoid using uninitialized attributes
    self.auto_backward = None
    self.choices = None
    self.translation_rules_test_code = None
    self.translation_rules_instr_src = None
    self.translation_rules_instr_tar = None
    self.is_three_split = None
    self.is_mylog_inserted = None
    self.needs_instrumentation = None
    self.is_long_requires_processing = None
    self.src_test_code = None
    self.src_main_code = None
    self.src_test_call_code = None
    self.translation_rules_main_code = None  # must be set to trans.rules learned by PiREL

    # ATTRIBUTES WITH DEFAULT VALUES (PER DUOGLOT)
    self.auto_backward = True
    self.choices = {'type': 'ASTNODE', 'choices_list': []}

    # if benchmark_name is not in the configs, then
    # the remaining attributes must be set manually
    if self.benchmark_name not in p_consts.BENCHMARK_CONFIGS:
      logger.warning(f'benchmark_name "{self.benchmark_name}" not in benchmark configs')
      logger.warning('all attributes must be set manually')
      return

    logger.debug(f'benchmark_name "{self.benchmark_name}" in benchmark configs')
    logger.debug(f'loading benchmark configs for "{self.benchmark_name}" from p_consts module')

    # ATTRIBUTES LOADED FROM CONFIGS
    self.translation_rules_test_code = self._load_tr_test_code(benchmark_name)
    self.translation_rules_instr_src = self._load_tr_instr_src(benchmark_name)
    self.translation_rules_instr_tar = self._load_tr_instr_tar(benchmark_name)

    self.is_three_split = p_consts.BENCHMARK_CONFIGS[benchmark_name]['is_three_split']
    self.is_mylog_inserted = p_consts.BENCHMARK_CONFIGS[benchmark_name]['is_mylog_inserted']
    self.needs_instrumentation = p_consts.BENCHMARK_CONFIGS[benchmark_name]['needs_instrumentation']

    # ATTRIBUTES THAT ARE COMPUTED BASED ON PREVIOUS ATTRIBUTES
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

  def __str__(self) -> str:
    return self.to_json_str()

  def to_json_str(self) -> str:
    '''
    Convert the PirelSubject instance to a JSON string.
    '''
    return json.dumps(self.__dict__, sort_keys=True)

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

  @classmethod
  def from_file_config(cls, conf_fpath: Path) -> PirelSubject:
    assert conf_fpath.exists(), f'Config file does not exist: {conf_fpath}'
    assert conf_fpath.is_file(), f'Config file is not a file: {conf_fpath}'
    assert conf_fpath.is_absolute(), f'Config file is not an absolute path: {conf_fpath}'
    assert conf_fpath.suffix == '.yaml', f'Config file is not a YAML file: {conf_fpath}'
    logger.debug(f'Loading subject from config file: {conf_fpath}')
    conf : dict = p_utils.read_yaml(conf_fpath)
    return cls.from_dict_config(conf)

  @classmethod
  def from_dict_config(cls, conf: dict) -> PirelSubject:
    '''
    Create a PirelSubject instance from a dictionary config.
    '''

    # main attributes
    attr_benchmark_name = conf.get('benchmark_name', 'custom')
    attr_name = conf['name']
    attr_src_lang = conf['src_lang']
    attr_tar_lang = conf['tar_lang']

    attr_src_program = None
    if 'src_program' in conf:
      attr_src_program = conf['src_program']
    elif 'src_program_fpath' in conf:
      src_program_fpath = p_utils.make_abs(conf['src_program_fpath'], p_consts.ROOT_DIR)
      assert src_program_fpath.exists(), f'Source program file does not exist: {src_program_fpath}'
      attr_src_program = p_utils.read_text(src_program_fpath)
    else:
      raise ValueError('Either `src_program` or `src_program_fpath` must be provided in the config')

    pirel_subject = PirelSubject(
      benchmark_name=attr_benchmark_name,
      name=attr_name,
      src_program=attr_src_program,
      src_lang=attr_src_lang,
      tar_lang=attr_tar_lang
    )

    # PirelSubject instance for a benchmark has an entry in the benchmark configs
    if attr_benchmark_name in p_consts.BENCHMARK_CONFIGS:
      if 'translation_rules_main_code' in conf:
        pirel_subject.translation_rules_main_code = conf['translation_rules_main_code']
      return pirel_subject

    # create a custom PirelSubject instance from the config file
    logger.debug('Creating custom PirelSubject instance from config file')

    pirel_subject.auto_backward = conf.get('auto_backward', True)
    pirel_subject.choices = conf.get('choices', {'type': 'ASTNODE', 'choices_list': []})

    # translation_rules_main_code
    if 'translation_rules_main_code' in conf:
      _trmc = conf['translation_rules_main_code']
    elif 'translation_rules_main_code_fpath' in conf:
      _trmcp = p_utils.make_abs(conf['translation_rules_main_code_fpath'], p_consts.ROOT_DIR)
      assert _trmcp.exists(), f'Translation rules main code file does not exist: {_trmcp}'
      _trmc = p_utils.read_text(_trmcp)
    else:
      _trmc = p_utils.read_text(p_consts.STARTING_RULESET_FPATH)
    assert _trmc is not None, 'translation_rules_main_code is None'
    assert isinstance(_trmc, str), f'translation_rules_main_code must be a string: {_trmc}'
    assert _trmc != '', 'translation_rules_main_code is empty'
    pirel_subject.translation_rules_main_code = _trmc

    # translation_rules_test_code
    _trtc = None
    if 'translation_rules_test_code' in conf:
      _trtc = conf['translation_rules_test_code']
    elif 'translation_rules_test_code_fpath' in conf:
      _trtcp = p_utils.make_abs(conf['translation_rules_test_code_fpath'], p_consts.ROOT_DIR)
      assert _trtcp.exists(), f'Translation rules test code file does not exist: {_trtcp}'
      _trtc = p_utils.read_text(_trtcp)
    pirel_subject.translation_rules_test_code = _trtc

    translation_rules_instr_src_fpath = conf.get('translation_rules_instr_src_fpath', None)
    pirel_subject.translation_rules_instr_src = None if translation_rules_instr_src_fpath is None else \
      p_utils.read_text_or_none(p_consts.ROOT_DIR / translation_rules_instr_src_fpath)

    translation_rules_instr_tar_fpath = conf.get('translation_rules_instr_tar_fpath', None)
    pirel_subject.translation_rules_instr_tar = None if translation_rules_instr_tar_fpath is None else \
      p_utils.read_text_or_none(p_consts.ROOT_DIR / translation_rules_instr_tar_fpath)

    pirel_subject.is_three_split = conf.get('is_three_split', True)
    pirel_subject.is_mylog_inserted = conf.get('is_mylog_inserted', True)
    pirel_subject.needs_instrumentation = conf.get('needs_instrumentation', True)

    # attributes that are computed based on previous attributes
    pirel_subject.is_long_requires_processing = pirel_subject._get_is_long_requires_processing()
    if pirel_subject.is_long_requires_processing:
      pirel_subject._translation_rules_process_for_long_source()

    if pirel_subject.is_three_split:
      assert pirel_subject.src_program.count(p_consts.TEST_MAIN_CALL_DELIMITER) == 2
      _tmc_splits = pirel_subject.src_program.split(p_consts.TEST_MAIN_CALL_DELIMITER)
      pirel_subject.src_test_code = _tmc_splits[0]
      pirel_subject.src_main_code = _tmc_splits[1]
      pirel_subject.src_test_call_code = _tmc_splits[2]
    else:
      assert p_consts.TEST_MAIN_CALL_DELIMITER not in pirel_subject.src_program
      pirel_subject.src_test_code = None
      pirel_subject.src_main_code = pirel_subject.src_program
      pirel_subject.src_test_call_code = None

    return pirel_subject

  @classmethod
  def from_json_str(cls, json_str: str) -> PirelSubject:
    '''
    Create a PirelSubject instance from a JSON string.
    '''
    conf = json.loads(json_str)
    return cls.from_dict_config(conf)
