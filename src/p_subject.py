from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional, Tuple

import p_consts
import p_utils
import p_visitor_py as pvpy


logger = p_utils.setup_logger(__name__)


class PirelSubject:
  '''
  This class represents a subject for PiREL.
  It holds all the necessary attributes of a program that is
  going to be translated by PiREL.

  translation_rules_main_code - translation rules that were learned
  by PiREL from translating `src_program` to the target language.

  translation_rules_test_code - translation rules that are
  hand-written by DuoGlot authors to translate the test code.

  is_three_split - if `True`, then `src_program` is split into
  three parts: test code, main code, and test call code.
  '''

  def __init__(
    self,
    benchmark_name: str,  # gfg
    name: str,  # G0001
    src_program: str,  # test_code + main_code + test_call_code | main_code
    src_lang: str,  # py
    tar_lang: str,  # js
    is_three_split: bool,
  ):
    # all attributes are listed here
    self.benchmark_name = benchmark_name
    self.name = name
    self.src_program = src_program
    self.src_lang = src_lang
    self.tar_lang = tar_lang
    self.is_three_split = is_three_split
    self.translation_rules_main_code = None
    self.translation_rules_test_code = None
    self.auto_backward = True
    self.choices = {'type': 'ASTNODE', 'choices_list': []}
    self.readonly_choices_list: List[Tuple[Tuple[int, int, int], int]] = []

    # some additional checks and initializations
    if benchmark_name in p_consts.BENCHMARK_CONFIGS:
      self.translation_rules_test_code = self._load_translation_rules_test_code(benchmark_name)

    if self.is_three_split:
      assert self.src_program.count(p_consts.TEST_MAIN_CALL_DELIMITER) == 2, (
        f'Expected exactly two occurrences of the delimiter '
        f'`{p_consts.TEST_MAIN_CALL_DELIMITER}` in the source program '
        f'for a three-split subject, but found '
        f'{self.src_program.count(p_consts.TEST_MAIN_CALL_DELIMITER)}'
      )

  def __str__(self) -> str:
    return self.to_json_str()

  def __repr__(self) -> str:
    return f'{self.__class__.__name__}({self.name})'

  def _split_src_program(self) -> Tuple[Optional[str], str, Optional[str]]:
    '''
    Split the source program into test code, main code, and test call code.
    Returns a tuple of (test_code, main_code, and test_call_code).
    If the subject does not have test code or test call code,
    the corresponding values will be None.
    '''
    if self.is_three_split:
      assert self.src_program.count(p_consts.TEST_MAIN_CALL_DELIMITER) == 2
      parts = self.src_program.split(p_consts.TEST_MAIN_CALL_DELIMITER)
      return parts[0], parts[1], parts[2]
    else:
      assert self.is_three_split is not None, 'is_three_split is not set'
      return None, self.src_program, None

  def get_src_test_code(self) -> Optional[str]:
    '''
    Get the test code of the subject.
    Returns None if the subject does not have test code.
    '''
    test, main, test_call = self._split_src_program()
    return test.strip() if test is not None else None

  def get_src_main_code(self) -> str:
    '''
    Get the main code of the subject.
    This is the code that will be translated by PiREL.
    '''
    test, main, test_call = self._split_src_program()
    return main.strip() if main is not None else None

  def get_src_test_call_code(self) -> Optional[str]:
    '''
    Get the test call code of the subject.
    Returns None if the subject does not have test call code.
    '''
    test, main, test_call = self._split_src_program()
    return test_call.strip() if test_call is not None else None

  def _load_translation_rules_test_code(self, benchmark_name: str) -> str:
    benchmark_conf = p_consts.BENCHMARK_CONFIGS[benchmark_name]
    translation_rules_test_code = p_utils.read_text_or_none(benchmark_conf['translation_rules_test_code_fpath'])
    return translation_rules_test_code

  def to_json_str(self) -> str:
    '''
    Convert the PirelSubject instance to a JSON string.
    '''
    return json.dumps(self.__dict__, sort_keys=True)

  @classmethod
  def from_dict(cls, obj: dict) -> PirelSubject:
    '''
    Precedence:
    1. obj
    2. configs in p_consts
    '''

    # name, src_lang, tar_lang are required
    assert 'name' in obj, 'name is not provided in the config'
    assert 'src_lang' in obj, 'src_lang is not provided in the config'
    assert 'tar_lang' in obj, 'tar_lang is not provided in the config'
    benchmark_name = obj.get('benchmark_name', 'N/A')
    name = obj['name']
    src_lang = obj['src_lang']
    tar_lang = obj['tar_lang']

    # src_program or src_program_fpath is required
    src_program = None
    if 'src_program' in obj:
      src_program = obj['src_program']
    elif 'src_program_fpath' in obj:
      src_program_fpath = p_utils.make_abs(obj['src_program_fpath'], p_consts.ROOT_DIR)
      assert src_program_fpath.exists(), f'Source program file does not exist: {src_program_fpath}'
      src_program = p_utils.read_text(src_program_fpath)
    else:
      raise ValueError('Either `src_program` or `src_program_fpath` must be provided in the config')

    # create a pirel subject instance using configs in p_consts
    pirel_subject = PirelSubject(
      benchmark_name=benchmark_name,
      name=name,
      src_program=src_program,
      src_lang=src_lang,
      tar_lang=tar_lang,
      is_three_split=obj.get('is_three_split', False),
    )

    # override the default values with values from obj
    # translation_rules_main_code
    if 'translation_rules_main_code' in obj:
      pirel_subject.translation_rules_main_code = obj['translation_rules_main_code']
    elif 'translation_rules_main_code_fpath' in obj:
      fpath = p_utils.make_abs(obj['translation_rules_main_code_fpath'], p_consts.ROOT_DIR)
      pirel_subject.translation_rules_main_code = p_utils.read_text(fpath)

    # translation_rules_test_code
    if 'translation_rules_test_code' in obj:
      pirel_subject.translation_rules_test_code = obj['translation_rules_test_code']
    elif 'translation_rules_test_code_fpath' in obj:
      fpath = p_utils.make_abs(obj['translation_rules_test_code_fpath'], p_consts.ROOT_DIR)
      pirel_subject.translation_rules_test_code = p_utils.read_text(fpath)

    # auto_backward
    if 'auto_backward' in obj:
      pirel_subject.auto_backward = obj['auto_backward']

    # choices
    if 'choices' in obj:
      pirel_subject.choices = obj['choices']

    return pirel_subject

  @classmethod
  def from_file_config(cls, conf_fpath: Path) -> PirelSubject:
    assert conf_fpath.exists(), f'Config file does not exist: {conf_fpath}'
    assert conf_fpath.is_file(), f'Config file is not a file: {conf_fpath}'
    assert conf_fpath.is_absolute(), f'Config file is not an absolute path: {conf_fpath}'
    assert conf_fpath.suffix == '.yaml', f'Config file is not a YAML file: {conf_fpath}'
    logger.debug(f'Loading a PiREL subject from a config file: {conf_fpath}')
    conf : dict = p_utils.read_yaml(conf_fpath)
    return cls.from_dict(conf)

  @classmethod
  def from_json_str(cls, json_str: str) -> PirelSubject:
    '''
    Create a PirelSubject instance from a JSON string.
    '''
    conf = json.loads(json_str)
    return cls.from_dict(conf)
