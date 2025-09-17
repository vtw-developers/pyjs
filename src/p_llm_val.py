'''
Class diagram:
- BaseValidationResult
  - TranslateSP1ValidationResult
  - TranslateSP2ValidationResult
  - GenTestFunctionValidationResult
  - GetRefTransValidationResult
'''

import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union

import d_ast_parse
import p_consts
import p_data_structures as pds
import p_utils
import p_visitor_js as pvjs


logger = p_utils.setup_logger(__name__)


class BaseValidationResult(ABC):
  '''Adapter class for validation results returned by validator functions in this module'''

  def __init__(self, validation_result: dict):
    self.validation_result = validation_result

  def __repr__(self) -> str:
    return f'{self.__class__.__name__}({self.is_successful()})'

  def get_val_result(self) -> dict:
    return self.validation_result

  def is_successful(self) -> bool:
    return self.validation_result['success']

  @abstractmethod
  def get_data(self) -> Any:
    pass


class TranslateSP1ValidationResult(BaseValidationResult):
  def __init__(self, validation_result: dict):
    super().__init__(validation_result)
    self.tp1_cands : List[str] = validation_result['tp1_cands']
    self.sp1 : str = validation_result['sp1']
    self.program_pairs : List[Dict[str, str]] = validation_result['program_pairs']
    self.success : bool = validation_result['success']
    self.tp1_cands_stats : List[dict] = validation_result['tp1_cands_stats']

  def get_all_no_parse_error(self) -> List[str]:
    '''RETURN all tp1_cands that do not have parse error'''
    npe_tp1_cands = [self.ad_tp1_cand(tp1_stat) for tp1_stat in self.tp1_cands_stats if not self.ad_has_parse_error(tp1_stat)]
    return npe_tp1_cands

  # BOOLEAN METHODS
  def has_no_tp1_cands(self) -> bool:
    return len(self.tp1_cands) == 0

  def all_have_parse_error(self) -> bool:
    flags = list(map(self.ad_has_parse_error, self.tp1_cands_stats))
    return all(flags)

  def all_are_comment_only(self) -> bool:
    flags = list(map(self.ad_is_comment_only, self.tp1_cands_stats))
    return all(flags)

  def all_miss_context(self) -> bool:
    '''
    c1, c2, ..., ci
    !(c1 || c2 || ... || ci) == !c1 && !c2 && ... && !ci
    '''
    flags = list(map(self.ad_has_context, self.tp1_cands_stats))
    return not any(flags)

  def all_violate_partial_program_affix(self, prefix: str, suffix: str) -> bool:
    flags = list(map(lambda tp2_stat: self.ad_is_parprog_affix_preserved(tp2_stat, prefix, suffix), self.tp1_cands_stats))
    return not any(flags)

  # ADAPTER METHODS TO `tp1_cands_stats` (have `ad` prefix)
  def ad_is_parprog_affix_preserved(self, tp2_stat: dict, prefix: str, suffix: str) -> bool:
    '''Check tp1_cand's affix'''
    prefix_ok = self.ad_tp1_cand(tp2_stat).startswith(prefix)
    suffix_ok = self.ad_tp1_cand(tp2_stat).endswith(suffix)
    return prefix_ok and suffix_ok

  def ad_tp1_cand(self, tp1_stat: dict) -> str:
    return tp1_stat['tp1_cand']

  def ad_success(self, tp1_stat: dict) -> bool:
    return tp1_stat['success'] is True

  def ad_has_parse_error(self, tp1_stat: dict) -> bool:
    return tp1_stat['has_parse_error'] is True

  def ad_is_comment_only(self, tp1_stat: dict) -> bool:
    return tp1_stat['is_comment_only'] is True

  def ad_has_context(self, tp1_stat: dict) -> bool:
    return tp1_stat['has_context'] is True

  # ABSTRACT METHOD IMPLEMENTATIONS
  def get_data(self) -> List[Dict[str, str]]:
    return self.program_pairs


class TranslateSP2ValidationResult(BaseValidationResult):
  def __init__(self, validation_result: dict):
    super().__init__(validation_result)
    # TODO how to treat cases with 0 cands?
    # assert len(validation_result['tp2_cands']) != 0, 'sanity check'
    self.tp2_cands : List[str] = validation_result['tp2_cands']
    self.sp1 : str = validation_result['sp1']
    self.sp2 : str = validation_result['sp2']
    self.tp1_cand : str = validation_result['tp1_cand']
    self.translation_pairs : List[Tuple[Dict[str, str], Dict[str, str]]] = validation_result['translation_pairs']
    self.success : bool = validation_result['success']
    self.tp2_cands_stats : List[dict] = validation_result['tp2_cands_stats']

  # BOOLEAN METHODS
  def has_no_tp2_cands(self) -> bool:
    return len(self.tp2_cands) == 0

  def all_have_parse_error(self) -> bool:
    flags = list(map(self.ad_has_parse_error, self.tp2_cands_stats))
    return all(flags)

  def all_miss_context(self) -> bool:
    flags = list(map(self.ad_has_context, self.tp2_cands_stats))
    return not any(flags)

  def all_are_not_type_isomorphic(self) -> bool:
    flags = list(map(self.ad_is_type_isomorphic, self.tp2_cands_stats))
    return not any(flags)

  def all_violate_partial_program_affix(self, prefix: str, suffix: str) -> bool:
    flags = list(map(lambda tp2_stat: self.ad_is_parprog_affix_preserved(tp2_stat, prefix, suffix), self.tp2_cands_stats))
    return not any(flags)

  # ADAPTER METHODS TO `tp2_cands_stats` (have `ad` prefix)
  def ad_is_parprog_affix_preserved(self, tp2_stat: dict, prefix: str, suffix: str) -> bool:
    '''Check tp2_cand's affix'''
    prefix_ok = self.ad_tp2_cand(tp2_stat).startswith(prefix)
    suffix_ok = self.ad_tp2_cand(tp2_stat).endswith(suffix)
    return prefix_ok and suffix_ok

  def ad_tp2_cand(self, tp2_stat: dict) -> str:
    return tp2_stat['tp2_cand']

  def ad_success(self, tp2_stat: dict) -> bool:
    return tp2_stat['success'] is True

  def ad_has_parse_error(self, tp2_stat: dict) -> bool:
    return tp2_stat['has_parse_error'] is True

  def ad_has_context(self, tp2_stat: dict) -> bool:
    return tp2_stat['has_context'] is True

  def ad_is_type_isomorphic(self, tp2_stat: dict) -> bool:
    return tp2_stat['is_type_isomorphic_to_tp1_cand'] is True

  # ABSTRACT METHOD IMPLEMENTATIONS
  def get_data(self) -> List[Tuple[Dict[str, str], Dict[str, str]]]:
    return self.translation_pairs


class GenTestFunctionValidationResult(BaseValidationResult):
  def __init__(self, validation_result: dict):
    super().__init__(validation_result)
    self.gen_test_fn_cands : List[str] = validation_result['gen_test_fn_cands']
    self.test_functions : List[str] = validation_result['test_functions']
    self.success : bool = validation_result['success']
    self.gen_test_fn_cands_stats : List[dict] = validation_result['gen_test_fn_cands_stats']

  # BOOLEAN METHODS
  def has_no_gen_test_fn_cands(self) -> bool:
    return len(self.gen_test_fn_cands) == 0

  def all_have_parse_error(self) -> bool:
    flags = list(map(self.ad_has_parse_error, self.gen_test_fn_cands_stats))
    return all(flags)

  def not_a_single_fn_def_test(self) -> bool:
    flags = list(map(self.ad_has_single_fn_def_test, self.gen_test_fn_cands_stats))
    return not any(flags)

  # ADAPTER METHODS TO `gen_test_fn_cands_stats` (have `ad` prefix)
  def ad_gen_test_fn_cand(self, gen_test_fn_stat: dict) -> str:
    return gen_test_fn_stat['gen_test_fn_cand']

  def ad_success(self, gen_test_fn_stat: dict) -> bool:
    return gen_test_fn_stat['success'] is True

  def ad_has_parse_error(self, gen_test_fn_stat: dict) -> bool:
    return gen_test_fn_stat['has_parse_error'] is True

  def ad_has_single_fn_def_test(self, gen_test_fn_stat: dict) -> bool:
    return gen_test_fn_stat['has_single_fn_def_test'] is True

  # ABSTRACT METHOD IMPLEMENTATIONS
  def get_data(self) -> List[str]:
    return self.test_functions


class GetRefTransValidationResult(BaseValidationResult):
  def __init__(self, validation_result: dict):
    super().__init__(validation_result)
    self.ref_trans_cands : List[str] = validation_result['ref_trans_cands']
    self.ref_translations : List[str] = validation_result['ref_translations']
    self.success : bool = validation_result['success']
    self.ref_trans_cands_stats : List[dict] = validation_result['ref_trans_cands_stats']

  # BOOLEAN METHODS
  def has_no_ref_trans_cands(self) -> bool:
    return len(self.ref_trans_cands) == 0

  def all_have_parse_error(self) -> bool:
    flags = list(map(self.ad_has_parse_error, self.ref_trans_cands_stats))
    return all(flags)

  def all_are_comment_only(self) -> bool:
    flags = list(map(self.ad_is_comment_only, self.ref_trans_cands_stats))
    return all(flags)

  def all_have_many_statements(self) -> bool:
    flags = list(map(self.ad_has_many_statements, self.ref_trans_cands_stats))
    return all(flags)

  def all_comp_stat_no_curly_braces(self) -> bool:
    flags = list(map(self.ad_comp_stat_no_curly_braces, self.ref_trans_cands_stats))
    return all(flags)

  # ADAPTER METHODS TO `ref_trans_cands_stats` (have `ad` prefix)
  def ad_ref_trans_cand(self, ref_trans_cand_stat: dict) -> str:
    return ref_trans_cand_stat['ref_trans_cand']

  def ad_success(self, ref_trans_cand_stat: dict) -> bool:
    return ref_trans_cand_stat['success'] is True

  def ad_has_parse_error(self, ref_trans_cand_stat: dict) -> bool:
    return ref_trans_cand_stat['has_parse_error'] is True

  def ad_is_comment_only(self, ref_trans_cand_stat: dict) -> bool:
    return ref_trans_cand_stat['is_comment_only'] is True

  def ad_has_many_statements(self, ref_trans_cand_stat: dict) -> bool:
    return ref_trans_cand_stat['has_many_statements'] is True

  def ad_comp_stat_no_curly_braces(self, ref_trans_cand_stat: dict) -> bool:
    return ref_trans_cand_stat['comp_stat_no_curly_braces'] is True

  # ABSTRACT METHOD IMPLEMENTATIONS
  def get_data(self) -> List[str]:
    return self.ref_translations


# VALIDATE TP1 CANDIDATES (SP1-TP1 ~ PROGRAM PAIRS)
def val_tp1_candidates(
  tp1_cands: List[str],
  sp1: str,
  template_dict: dict
) -> TranslateSP1ValidationResult:
  '''
  This function is invoked to check if the translation of the first
  program in source language is valid or not.

  CRITERIA:
  1. translation has no parse errors
  2. translation contains at least one context

  RETURN program pairs that satisfy criteria
  '''
  p_utils.log_json_time(f'args-val_tp1_candidates.json', locals())
  logger.debug(f'~~~ Starting validation of {len(tp1_cands)} TP1 candidates')

  tp1_cands_uniq = p_utils.deduplicate(tp1_cands)
  if len(tp1_cands_uniq) != len(tp1_cands):
    logger.debug(f'{len(tp1_cands) - len(tp1_cands_uniq)} duplicate TP1 candidates were found')
    tp1_cands = tp1_cands_uniq

  return_dict = {}
  return_dict['tp1_cands'] = tp1_cands
  return_dict['sp1'] = sp1
  return_dict['program_pairs'] = []
  return_dict['success'] = False
  return_dict['tp1_cands_stats'] = []

  program_pairs = []
  for idx, tp1_cand in enumerate(tp1_cands, start=1):
    logger.debug(f'Checking if TP1 candidate ({idx}/{len(tp1_cands)}) satisfies our criteria')
    tp1_cand_stats = _tp1_cand_gather_stats(tp1_cand, sp1, template_dict)
    return_dict['tp1_cands_stats'].append(tp1_cand_stats)
    success = tp1_cand_stats['success']

    if success:
      program_pairs.append({
        'source': tp1_cand_stats['sp1'],
        'target': tp1_cand_stats['tp1_cand']
      })

    logger.debug(f'TP1 candidate satisfies our criteria => ({success})')
    logger.debug(f'The number of good program pairs so far is {len(program_pairs)}/{len(tp1_cands)}')

  if len(program_pairs) == 0:
    _ = {'sp1': sp1, 'tp1_cands': tp1_cands}
    logger.debug(f'BAD: no program pairs were formed with {len(tp1_cands)} TP1 candidates:\n{json.dumps(_, indent=2)}')
    return TranslateSP1ValidationResult(return_dict)

  return_dict['success'] = True
  return_dict['program_pairs'] = program_pairs
  logger.debug(f'GOOD End of TP1 candidates validation.')
  logger.debug(f'The number of good program pairs is {len(program_pairs)}/{len(tp1_cands)}')
  return TranslateSP1ValidationResult(return_dict)


def _tp1_cand_gather_stats(
  tp1_cand: str,
  sp1: str,
  template_dict: dict
) -> dict:
  contexts = template_dict['contexts']
  src_lang = template_dict['src_lang']
  tar_lang = template_dict['tar_lang']

  return_dict = {
    'sp1': sp1,
    'tp1_cand': tp1_cand,
    'success': None,
    'has_parse_error': None,
    'is_comment_only': None,
    'has_context': None,
  }

  logger.debug(f'Checking if TP1 candidate satisfies our criteria')
  logger.debug(f'\nsp1:\n{repr(sp1)}\ntp1_cand:\n{repr(tp1_cand)}')

  # criteria 1
  if p_utils.does_have_parse_error(tp1_cand, tar_lang):
    logger.debug(f'BAD: TP1 candidate has a parse error')
    return_dict['success'] = False
    return_dict['has_parse_error'] = True
    return return_dict

  # actually remove comments from tp1_cand after checking for parse errors
  tp1_cand = pvjs.CommentsRemover.remove_comments(tp1_cand).strip()
  return_dict['tp1_cand'] = tp1_cand

  # criteria 2
  # the TP1 candidate should not be a comment-only string
  if tp1_cand == '':
    logger.debug(f'BAD: generated TP1 candidate is a comment-only string')
    return_dict['success'] = False
    return_dict['has_parse_error'] = False
    return_dict['is_comment_only'] = True
    return return_dict

  # criteria 3
  sp1_ast, _ = d_ast_parse.parse_text_dbg(sp1, src_lang)
  sp1_tree = pds.DuoGlotTree(sp1_ast)
  tp1_cand_ast, _ = d_ast_parse.parse_text_dbg(tp1_cand, tar_lang)
  tp1_cand_tree = pds.DuoGlotTree(tp1_cand_ast)

  # TODO how about checking sp1 and tp1_cand separately?
  all_contained_contexts = _get_all_contexts_contained(
    [sp1_tree],
    [tp1_cand_tree],
    contexts
  )

  if len(all_contained_contexts) == 0:
    logger.debug(f'BAD: None of the contexts are found in both SP1 and TP1 candidate')
    return_dict['success'] = False
    return_dict['has_parse_error'] = False
    return_dict['is_comment_only'] = False
    return_dict['has_context'] = False
    return return_dict

  logger.debug('GOOD: TP1 candidate satisfies our criteria')
  return_dict['success'] = True
  return_dict['has_parse_error'] = False
  return_dict['is_comment_only'] = False
  return_dict['has_context'] = True
  return return_dict


# VALIDATE TP2 CANDIDATES (SP1-TP1, SP2-TP2 ~ TRANSLATION PAIRS)
def val_tp2_candidates(
  tp2_cands: List[str],
  sp1: str,
  sp2: str,
  tp1_cand: str,
  template_dict: dict
) -> TranslateSP2ValidationResult:
  '''
  This function is invoked to check if the translation pair
  is valid

  CRITERIA:
  1. translation candidate of SP2 has no parse errors
  2. translation candidates of SP1 and SP2 are type-isomorphic
  except at identifiers and literals
  3. translation candidate of SP2 contains the same context as SP1

  RETURN
  All candidate translations that satisfy criteria
  '''
  p_utils.log_json_time(f'args-val_tp2_candidates.json', locals())
  logger.debug(f'~~~ Starting validation of {len(tp2_cands)} TP2 candidates')

  return_dict = {}
  return_dict['tp2_cands'] = tp2_cands
  return_dict['sp1'] = sp1
  return_dict['sp2'] = sp2
  return_dict['tp1_cand'] = tp1_cand
  return_dict['translation_pairs'] = []
  return_dict['success'] = False
  return_dict['tp2_cands_stats'] = []

  translation_pairs = []
  for idx, tp2_cand in enumerate(tp2_cands, start=1):
    logger.debug(f'Checking if TP2 candidate ({idx}/{len(tp2_cands)}) satisfies our criteria')
    tp2_cand_stat = _tp2_cand_gather_stats(sp1, sp2, tp1_cand, tp2_cand, template_dict)
    return_dict['tp2_cands_stats'].append(tp2_cand_stat)
    success = tp2_cand_stat['success']

    if success:
      translation_pairs.append(({'source': sp1, 'target': tp1_cand}, {'source': sp2, 'target': tp2_cand}))

  if len(translation_pairs) == 0:
    _ = {'sp1': sp1, 'sp2': sp2, 'tp1': tp1_cand, 'tp2_cands': tp2_cands}
    logger.debug(f'BAD: no translation pairs were formed with {len(tp2_cands)} TP2 candidates:\n{json.dumps(_, indent=2)}')
    return TranslateSP2ValidationResult(return_dict)

  return_dict['success'] = True
  return_dict['translation_pairs'] = translation_pairs
  logger.debug(f'GOOD End of TP2 candidates validation.')
  logger.debug(f'The number of good translation pairs is {len(translation_pairs)}/{len(tp2_cands)}')
  return TranslateSP2ValidationResult(return_dict)


def _tp2_cand_gather_stats(
  sp1: str,
  sp2: str,
  tp1_cand: str,
  tp2_cand: str,
  template_dict: dict
) -> dict:

  contexts = template_dict['contexts']
  src_lang = template_dict['src_lang']
  tar_lang = template_dict['tar_lang']

  return_dict = {
    'sp1': sp1,
    'sp2': sp2,
    'tp1_cand': tp1_cand,
    'tp2_cand': tp2_cand,
    'success': None,
    'has_parse_error': None,
    'has_context': None,
    'is_type_isomorphic_to_tp1_cand': None,
  }

  logger.debug(f'Checking if TP2 candidate satisfies our criteria')
  logger.debug(f'\ntp1_cand:\n{repr(tp1_cand)}\ntp2:\n{repr(tp2_cand)}')

  # criteria 1
  if p_utils.does_have_parse_error(tp2_cand, tar_lang):
    logger.debug(f'BAD: TP2 candidate has a parse error')
    return_dict['success'] = False
    return_dict['has_parse_error'] = True
    return return_dict

  # criteria 2
  source_trees : List[pds.DuoGlotTree] = []
  for source in [sp1, sp2]:
    source_ast, _ = d_ast_parse.parse_text_dbg(source, src_lang)
    source_tree = pds.DuoGlotTree(source_ast)
    source_trees.append(source_tree)
  target_trees : List[pds.DuoGlotTree] = []
  for target in [tp1_cand, tp2_cand]:
    target_ast, _ = d_ast_parse.parse_text_dbg(target, tar_lang)
    target_tree = pds.DuoGlotTree(target_ast)
    target_trees.append(target_tree)

  contexts_contained = _get_all_contexts_contained(source_trees, target_trees, contexts)
  if len(contexts_contained) == 0:
    logger.debug(f'BAD: SP1-TP1 and SP2-TP2 do not contain any of the contexts')
    return_dict['success'] = False
    return_dict['has_parse_error'] = False
    return_dict['has_context'] = False
    return return_dict

  # criteria 3
  are_targets_type_isomorphic = _are_translations_identical_except_identifiers(
    tp1_cand,
    tp2_cand,
    tar_lang
  )
  if not are_targets_type_isomorphic:
    logger.debug(f'BAD: TP1 and TP2 are not type-isomorphic.')
    return_dict['success'] = False
    return_dict['has_parse_error'] = False
    return_dict['has_context'] = True
    return_dict['is_type_isomorphic_to_tp1_cand'] = False
    return return_dict

  logger.debug(f'GOOD: TP2 candidate passed the validation step.')
  return_dict['success'] = True
  return_dict['has_parse_error'] = False
  return_dict['is_type_isomorphic_to_tp1_cand'] = True
  return_dict['has_context'] = True
  return return_dict


def _are_translations_identical_except_identifiers(
  trans1: str,
  trans2: str,
  tar_lang: str
) -> bool:
  '''
  Two translations (programs in the target language) are identical iff
  1. The trees are type isomorphic.
  2. All terminals EXCEPT identifiers and literals are identical.

  PRE1: trans1 does not have parse errors
  PRE2: trans2 does not have parse errors
  '''

  trans1_ast, _ = d_ast_parse.parse_text_dbg(trans1, tar_lang)
  trans2_ast, _ = d_ast_parse.parse_text_dbg(trans2, tar_lang)
  trans1_tree = pds.DuoGlotTree(trans1_ast)
  trans2_tree = pds.DuoGlotTree(trans2_ast)

  trans1_enc = _get_type_ahu_ter_x_ident_lit_encoding(trans1_tree)
  trans2_enc = _get_type_ahu_ter_x_ident_lit_encoding(trans2_tree)

  logger.debug(f'Encoding of TP1:\n{trans1_enc}')
  logger.debug(f'Encoding of TP2:\n{trans2_enc}')

  are_compatible = trans1_enc == trans2_enc

  return are_compatible


def _get_type_ahu_ter_x_ident_lit_encoding(
  tree: pds.DuoGlotTree
) -> str:
  '''
  Compute AHU encoding with
  1. type information
  2. terminals except identifiers
  3. terminals except literals
  for comparing tree for type-isomorphism
  https://www.baeldung.com/cs/isomorphic-trees#1-ahu-encoding
  '''
  def __rec_post_order(node: pds.DuoGlotNode):
    # base case (terminal node)
    if node.is_terminal():
      return node.get_type()
    # base case: non-terminal with a single terminal child
    if len(node.get_children()) == 1 and node.get_children()[0].is_terminal():
      return '0'
    children_encoding = ''
    for child in node.get_children():
      children_encoding += __rec_post_order(child) + ' '
    children_encoding = children_encoding.strip()
    return f'({node.get_type()} {children_encoding})'
  encoding = __rec_post_order(tree.get_root_node())
  return encoding


def _get_type_ahu_encoding_x_ident_deprecated(
  tree: pds.DuoGlotTree
) -> str:
  '''
  Compute AHU encoding with
  1. type information
  2. all terminals except identifier and literal terminals
  for removing duplicates of TSP candidates
  https://www.baeldung.com/cs/isomorphic-trees#1-ahu-encoding
  '''
  def __rec_post_order(node: pds.DuoGlotNode) -> str:
    if node.is_terminal():
      if node.get_num_siblings() == 0:  # identifier or literal
        return '0'
      else:
        return node.get_type()
    children_encoding = ''
    for child in node.get_children():
      children_encoding += __rec_post_order(child)
    return f'({node.get_type()} {children_encoding})'

  return __rec_post_order(tree.get_root_node())


# VALIDATE GENERATED TEST FUNCTION CANDIDATES
def val_gen_test_function_candidates(
  gen_test_fn_cands: List[str],
  src_lang: str
) -> GenTestFunctionValidationResult:
  '''
  This function is invoked to check if the generated test function candidates
  are valid or not.

  CRITERIA:
  1. generated test function candidates have no parse errors
  '''
  p_utils.log_json_time(f'args-val_gen_test_function_candidates.json', locals())
  logger.debug(f'~~~ Starting validation of {len(gen_test_fn_cands)} generated test function candidates')

  return_dict = {}
  return_dict['gen_test_fn_cands'] = gen_test_fn_cands
  return_dict['test_functions'] = []
  return_dict['success'] = False
  return_dict['gen_test_fn_cands_stats'] = []

  test_functions = []
  for idx, gen_test_fn_cand in enumerate(gen_test_fn_cands, start=1):
    logger.debug(f'Checking if generated test function candidate ({idx}/{len(gen_test_fn_cands)}) satisfies our criteria')
    gen_test_fn_cand_stats = _gen_test_fn_cand_gather_stats(gen_test_fn_cand, src_lang)
    return_dict['gen_test_fn_cands_stats'].append(gen_test_fn_cand_stats)
    success = gen_test_fn_cand_stats['success']

    if success:
      test_functions.append(gen_test_fn_cand)

    logger.debug(f'Generated test function candidate satisfies our criteria => ({success})')
    logger.debug(f'The number of good test functions so far is {len(test_functions)}/{len(gen_test_fn_cands)}')

  if len(test_functions) == 0:
    _ = {'gen_test_fn_cands': gen_test_fn_cands}
    logger.debug(f'BAD: no test functions were formed with {len(gen_test_fn_cands)} generated test function candidates:\n{json.dumps(_, indent=2)}')
    return GenTestFunctionValidationResult(return_dict)

  return_dict['success'] = True
  return_dict['test_functions'] = test_functions
  logger.debug(f'GOOD: End of generated test function candidates validation.')
  logger.debug(f'The number of good test functions is {len(test_functions)}/{len(gen_test_fn_cands)}')
  return GenTestFunctionValidationResult(return_dict)


def _gen_test_fn_cand_gather_stats(
  gen_test_fn_cand: str,
  src_lang: str
) -> dict:

  return_dict = {
    'gen_test_fn_cand': gen_test_fn_cand,
    'success': None,
    'has_parse_error': None,
    'has_single_fn_def_test': None,
  }

  logger.debug(f'Checking if generated test function candidate satisfies our criteria')
  logger.debug(f'\ngen_test_fn_cand:\n{repr(gen_test_fn_cand)}')

  # criteria 1
  if p_utils.does_have_parse_error(gen_test_fn_cand, src_lang):
    logger.debug(f'BAD: generated test function candidate has a parse error')
    return_dict['success'] = False
    return_dict['has_parse_error'] = True
    return return_dict

  # criteria 2
  # generated test function candidate should have:
  # 1. only one function definition
  # 2. and that function definition should be `def test()`
  ast, _ = d_ast_parse.parse_text_dbg(gen_test_fn_cand, src_lang)
  tree = pds.DuoGlotTree(ast)
  root_node = tree.get_root_node()
  if root_node.get_num_nt_children() != 1:
    logger.debug(f'BAD: generated test function candidate has multiple non-terminal children at root node')
    return_dict['success'] = False
    return_dict['has_parse_error'] = False
    return_dict['has_single_fn_def_test'] = False
    return return_dict
  fn_defn_node = root_node.get_nt_children()[0]
  if fn_defn_node.get_ts_node_type() != 'function_definition':
    logger.debug(f'BAD: generated test function candidate is not a function definition')
    return_dict['success'] = False
    return_dict['has_parse_error'] = False
    return_dict['has_single_fn_def_test'] = False
    return return_dict
  if 'def test():' not in gen_test_fn_cand:
    logger.debug(f'BAD: generated test function candidate is not a test function definition')
    return_dict['success'] = False
    return_dict['has_parse_error'] = False
    return_dict['has_single_fn_def_test'] = False
    return return_dict

  logger.debug(f'GOOD: generated test function candidate passed the validation step.')
  return_dict['success'] = True
  return_dict['has_parse_error'] = False
  return_dict['has_single_fn_def_test'] = True
  return return_dict


# VALIDATE REFERENCE TRANSLATION
def val_get_ref_trans_candidates(
  ref_trans_cands: List[str],
  tar_lang: str,
) -> GetRefTransValidationResult:
  '''
  This function is invoked to check if the reference translation candidates
  are valid or not.

  CRITERIA:
  1. reference translation candidates have no parse errors
  '''
  p_utils.log_json_time(f'args-val_get_ref_trans_candidates.json', locals())
  logger.debug(f'~~~ Starting validation of {len(ref_trans_cands)} reference translation candidates')

  return_dict = {}
  return_dict['ref_trans_cands'] = ref_trans_cands
  return_dict['ref_translations'] = []
  return_dict['success'] = False
  return_dict['ref_trans_cands_stats'] = []

  ref_translations = []
  for idx, ref_trans_cand in enumerate(ref_trans_cands, start=1):
    logger.debug(f'Checking if reference translation candidate ({idx}/{len(ref_trans_cands)}) satisfies our criteria')
    ref_trans_cand_stats = _get_ref_trans_cand_gather_stats(ref_trans_cand, tar_lang)
    return_dict['ref_trans_cands_stats'].append(ref_trans_cand_stats)
    success = ref_trans_cand_stats['success']

    if success:
      ref_translations.append(ref_trans_cand_stats['ref_trans_cand'])

    logger.debug(f'Reference translation candidate satisfies our criteria => ({success})')
    logger.debug(f'The number of reference translations so far is {len(ref_translations)}/{len(ref_trans_cands)}')

  if len(ref_translations) == 0:
    _ = {'ref_trans_cands': ref_trans_cands}
    logger.debug(
      f'BAD: no reference translations were formed with {len(ref_trans_cands)} '
      f'reference translation candidates:\n{json.dumps(_, indent=2)}')
    return GetRefTransValidationResult(return_dict)

  return_dict['success'] = True
  return_dict['ref_translations'] = ref_translations
  logger.debug(f'GOOD: End of reference translation candidates validation.')
  logger.debug(f'The number of good reference translations is {len(ref_translations)}/{len(ref_trans_cands)}')
  return GetRefTransValidationResult(return_dict)


def _get_ref_trans_cand_gather_stats(
  ref_trans_cand: str,
  tar_lang: str
) -> dict:

  return_dict = {
    'ref_trans_cand': ref_trans_cand,
    'success': None,
    'has_parse_error': None,
    'is_comment_only': None,
    'has_many_statements': None,
    'comp_stat_no_curly_braces': None,
  }

  logger.debug(f'Checking if generated reference translation candidate satisfies our criteria')
  logger.debug(f'\nref_trans_cand:\n{repr(ref_trans_cand)}')

  # criteria 1
  if p_utils.does_have_parse_error(ref_trans_cand, tar_lang):
    logger.debug(f'BAD: generated reference translation candidate has a parse error')
    return_dict['success'] = False
    return_dict['has_parse_error'] = True
    return return_dict

  # actually remove comments from ref_trans_cand after checking for parse errors
  ref_trans_cand = pvjs.CommentsRemover.remove_comments(ref_trans_cand).strip()
  return_dict['ref_trans_cand'] = ref_trans_cand

  # criteria 2
  # the reference translation should not be a comment-only string
  if ref_trans_cand == '':
    logger.debug(f'BAD: generated reference translation candidate is a comment-only string')
    return_dict['success'] = False
    return_dict['has_parse_error'] = False
    return_dict['is_comment_only'] = True
    return return_dict

  # criteria 3
  tree = pds.DuoGlotTree.from_code_str(ref_trans_cand, tar_lang)
  root_node = tree.get_root_node()
  if root_node.get_num_nt_children() > 1:
    logger.debug(f'BAD: generated reference translation candidate has multiple non-terminal children at root node')
    return_dict['success'] = False
    return_dict['has_parse_error'] = False
    return_dict['is_comment_only'] = False
    return_dict['has_many_statements'] = True
    return return_dict

  # criteria 4
  # if the reference translation is a compound statement,
  # it must use curly braces
  if tar_lang == 'js':
    context_node = root_node.get_children()[0]
    if context_node.get_ts_node_type() in [
      'if_statement',
      'switch_statement',
      'for_statement',
      'for_in_statement',
      'while_statement',
      'do_statement',
      'try_statement',
      'with_statement',
    ]:
      # statement_block must be one of direct children
      statement_block_nodes = list(filter(
        lambda node: node.is_nonterminal() and node.get_ts_node_type() == 'statement_block',
        context_node.get_children()
      ))
      if not statement_block_nodes:
        logger.debug(f'BAD: generated reference translation candidate has a compound statement without curly braces')
        return_dict['success'] = False
        return_dict['has_parse_error'] = False
        return_dict['is_comment_only'] = False
        return_dict['has_many_statements'] = False
        return_dict['comp_stat_no_curly_braces'] = True
        return return_dict

  logger.debug(f'GOOD: generated reference translation candidate passed the validation step.')
  return_dict['success'] = True
  return_dict['has_parse_error'] = False
  return_dict['is_comment_only'] = False
  return_dict['has_many_statements'] = False
  return_dict['comp_stat_no_curly_braces'] = False
  return return_dict


# COMMONLY USED FUNCTIONS IN THIS MODULE
def _is_generated_code_type_isomorphic_to_shallow_template_deprecated(
  gen_tree: pds.DuoGlotTree,
  template_tree: pds.DuoGlotTree,
  templatized_node_paths: List[List[int]]
) -> bool:
  '''
  everything except templatized nodes (holes) is the same
  templatized nodes can be arbitrarily different
  NOTE refer to notes or update this doc
  TODO what does `shallow template` mean?
  '''

  gen_type_enc = _get_tree_encoding_except_templatized_nodes(gen_tree, templatized_node_paths)
  if gen_type_enc is None:
    return False
  template_type_enc = _get_tree_encoding_except_templatized_nodes(template_tree, templatized_node_paths)
  assert template_type_enc is not None, 'should not happen: templatized_node_ids are invalid'

  return gen_type_enc == template_type_enc


def _get_tree_encoding_except_templatized_nodes(
  tree: pds.DuoGlotTree,
  templatized_node_paths: List[List[int]]
) -> Union[str, None]:
  '''
  Get string encoding of a tree
  Return None if any of templatized nodes is missing from tree
  TODO update this doc
  '''
  def __rec_post_order(node: pds.DuoGlotNode):
    nonlocal templatized_nodes
    if node in templatized_nodes:
      return '__'
    if isinstance(node, pds.TNode):
      return node.get_type()
    children_encoding = ''
    for child in node.get_children():
      children_encoding += __rec_post_order(child)
    return f'{node.get_type()} ({children_encoding})'

  root_node = tree.get_root_node()

  # get_child_by_path() relative to context node
  # context node should be the only child when its text is parsed as it is
  # TODO this may need refactoring
  if len(root_node.get_children()) != 1:
    return None

  context_node = root_node.get_children()[0]
  templatized_nodes = [context_node.get_child_by_path(path) for path in templatized_node_paths]

  if any(map(lambda node: node is None, templatized_nodes)):
    return None

  return __rec_post_order(tree.get_root_node())


def _get_all_contexts_contained(
  source_trees: List[pds.DuoGlotTree],
  target_trees: List[pds.DuoGlotTree],
  contexts: list,
) -> list:
  ''''''
  contexts_contained = []
  for context in contexts:
    ctx_exists = _context_exists(source_trees, target_trees, context['source_context'], context['target_context'])
    if ctx_exists:
      contexts_contained.append(context)
  return contexts_contained


def _context_exists(
  src_trees: List[pds.DuoGlotTree],
  tar_trees: List[pds.DuoGlotTree],
  source_context: list,
  target_context: list,
) -> bool:
  '''
  Implementation of this function is similar to p_rule_postprocessor.TranslationRule.trim_context()
  '''

  def __rec_pre_order_find_node_under_context(
    node: pds.DuoGlotNode,
    context: List[List[str]]
  ) -> Optional[pds.DuoGlotNode]:
    ''''''
    nt_children = node.get_nt_children()
    if len(nt_children) == 0:
      return None

    siblings_and_child = list(reversed(context[-1]))
    assert len(siblings_and_child) >= 1, 'sanity check'

    # base case
    if len(context) == 1:
      siblings = siblings_and_child[:-1]
      for i in range(len(siblings)):
        _sibi = siblings[i]
        _ntci = nt_children[i]

        # NOTE `p_data_structures.PatternNode.get_path_to_root_source._get_path`
        # refer to the function above for more information on why check for `pirel_anynode`.
        # `pirel_anynode` refers to a "." placeholder in match fragment of a translation rule
        # that is not used in the expand fragment, and can match any non-terminal node.
        if _sibi == 'pirel_anynode':
          continue

        if _sibi != _ntci.get_type().strip('"'):
          return None
      return nt_children[len(siblings)]

    # for ntype in reversed(context_elem):
    for i in range(len(siblings_and_child)):
      _saci = siblings_and_child[i]
      _ntci = nt_children[i]
      assert _saci != 'pirel_anynode', 'consider this case'

      if _saci != _ntci.get_type().strip('"'):
        return None
      # last matching element
      if i == len(siblings_and_child) - 1:
        result = __rec_pre_order_find_node_under_context(_ntci, context[:-1])
        if result is None:
          return None
        else:
          return result

  # all `src_trees` should contain `source_context`
  for src_tree in src_trees:
    try:
      src_problematic_node = __rec_pre_order_find_node_under_context(src_tree.get_root_node(), source_context)
    except IndexError:
      return False
    if src_problematic_node is None:
      return False

  # all `tar_trees` should contain `target_context`
  for tar_tree in tar_trees:
    try:
      tar_problematic_node = __rec_pre_order_find_node_under_context(tar_tree.get_root_node(), target_context)
    except IndexError:
      return False
    if tar_problematic_node is None:
      return False

  return True


# TEST HARNESSES
def _test_val_tp1_candidates():
  '''
  def val_tp1_candidates(
    tp1_cands: List[str],
    sp1: str,
    template_dict: dict
  ) -> TranslateSP1ValidationResult:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_val_tp1_candidates_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  tp1_cands = args_dict['tp1_cands']
  sp1 = args_dict['sp1']
  template_dict = args_dict['template_dict']

  val_result_dict = val_tp1_candidates(tp1_cands, sp1, template_dict)
  print(json.dumps(val_result_dict.get_val_result(), indent=2, default=str))


def _test_val_translation_pair_candidates():
  test_harness_config:dict = p_utils.read_json('temporary_test_val_translation_pair_candidates_config.json')
  args_dict = p_utils.read_json(test_harness_config['args_dict_fpath'])

  tp2_cands = args_dict['tp2_cands']
  sp1 = args_dict['sp1']
  sp2 = args_dict['sp2']
  tp1_cand = args_dict['tp1_cand']
  template_dict = args_dict['template_dict']

  val_result_dict = val_tp2_candidates(tp2_cands, sp1, sp2, tp1_cand, template_dict)
  p_utils.write_json('temporary_test_val_translation_pair_candidates.json', val_result_dict)


def _test_val_get_ref_trans_candidates():
  '''
  def val_get_ref_trans_candidates(
    ref_trans_cands: List[str],
    tar_lang: str,
  ):
  '''
  config_fpath = p_consts.TMP_DIR / 'test_val_get_ref_trans_candidates_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  ref_trans_cands = args_dict['ref_trans_cands']
  tar_lang = args_dict['tar_lang']

  val_result = val_get_ref_trans_candidates(
    ref_trans_cands,
    tar_lang,
  )

  print(json.dumps(val_result.get_val_result(), indent=2, default=str))


if __name__ == '__main__':
  # _test_val_tp1_candidates()
  # _test_val_translation_pair_candidates()
  _test_val_get_ref_trans_candidates()
