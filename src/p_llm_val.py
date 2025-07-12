'''
Class diagram:

                                         BaseValidationResult
                                          │       │       │
                                          │       │       │
                                          │       │       │
                                          │       │       │
                                          │       │       │
                         ◄────────────────┘       ▼       └───────────────────►
SimplifyTemplateValidationResult       TranslateSP1ValidationResult       TranslateSP2ValidationResult
'''

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import d_ast_parse
import p_consts
import p_data_structures as pds
import p_utils


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


class SimplifyTemplateValidationResult(BaseValidationResult):
  def __init__(self, validation_result):
    super().__init__(validation_result)
    self.st_cands : List[str] = validation_result['simplified_template_cands']
    self.success : bool = validation_result['success']
    self.does_need_simplification : bool = validation_result['does_need_simplification']
    self.simplified_templates : List[dict] = validation_result['simplified_templates']
    self.st_cands_stats : List[dict] = validation_result['simplified_template_cands_stats']

  # BOOLEAN METHODS
  def all_exceed_depth_threshold(self) -> bool:
    flags = list(map(self.ad_are_depths_at_templatized_nodes_within_limit, self.st_cands_stats))
    return not any(flags)

  def all_change_parts_outside_holes(self) -> bool:
    '''
    LLM is supposed to fill in only the holes in a template.
    It should not change other parts of the template.
    '''
    flags = list(map(self.ad_is_type_isomorphic_to_template_origin, self.st_cands_stats))
    return not any(flags)

  # ADAPTER METHODS TO `st_cands_stats` (have `ad` prefix)
  def ad_simplified_template_cand(self, st_stat: dict) -> str:
    return st_stat['simplified_template_cand']

  def ad_template_origin(self, st_stat: dict) -> str:
    return st_stat['template_origin']

  def ad_success(self, st_stat: dict) -> bool:
    return st_stat['success'] is True

  def ad_has_parse_error(self, st_stat: dict) -> bool:
    return st_stat['has_parse_error'] is True

  def ad_is_type_isomorphic_to_template_origin(self, st_stat: dict) -> bool:
    return st_stat['is_type_isomorphic_to_template_origin'] is True

  def ad_root_node_has_multiple_children(self, st_stat: dict) -> bool:
    return st_stat['root_node_has_multiple_children'] is True

  def ad_are_depths_at_templatized_nodes_within_limit(self, st_stat: dict) -> bool:
    return st_stat['are_depths_at_templatized_nodes_within_limit'] is True

  def ad_simplified_template(self, st_stat: dict) -> str:
    return st_stat['simplified_template']

  def ad_simplified_template_origin(self, st_stat: dict) -> str:
    return st_stat['simplified_template_origin']

  def ad_templatized_nodes_depths_sum(self, st_stat: dict) -> int:
    return st_stat['templatized_nodes_depths_sum']

  # ABSTRACT METHOD IMPLEMENTATIONS
  def get_data(self) -> Dict[str, str]:
    simplified_templates = self.validation_result['simplified_templates']
    depth_sum = lambda st: st['templatized_nodes_depths_sum']
    best_st = min(simplified_templates, key=depth_sum)
    return best_st


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

  # ADAPTER METHODS TO `ref_trans_cands_stats` (have `ad` prefix)
  def ad_ref_trans_cand(self, ref_trans_cand_stat: dict) -> str:
    return ref_trans_cand_stat['ref_trans_cand']

  def ad_success(self, ref_trans_cand_stat: dict) -> bool:
    return ref_trans_cand_stat['success'] is True

  def ad_has_parse_error(self, ref_trans_cand_stat: dict) -> bool:
    return ref_trans_cand_stat['has_parse_error'] is True

  # ABSTRACT METHOD IMPLEMENTATIONS
  def get_data(self) -> List[str]:
    return self.ref_translations


# VALIDATE SIMPLIFIED TEMPLATE CANDIDATES
def val_simplified_template_candidates(st_cands: List[str], template_dict: dict, **kwargs) -> SimplifyTemplateValidationResult:
  '''
  Simplified templates should satisfy the following criteria:
  1. Should be parseable
  2. Everything except templatized nodes should be identical to template origin
  3. Simplest AST at templatized nodes.
  How do we measure simplicity? Should not exceed depth N.
  '''
  p_utils.log_json_time(f'{kwargs["subject_name"]}_args-val_simplified_template_candidates.json', locals())
  logger.debug(f'~~~ Starting validation of {len(st_cands)} "Simplified Template" candidates')

  return_dict = {}
  return_dict['simplified_template_cands'] = st_cands
  return_dict['success'] = False
  return_dict['does_need_simplification'] = True
  return_dict['simplified_templates'] = []
  return_dict['simplified_template_cands_stats'] = []

  assert len(template_dict['templatized_node_ids_context']) > 0, 'sanity check'

  simplified_templates = []
  for idx, st_cand in enumerate(st_cands, start=1):
    logger.debug(f'Checking if simplified template candidate ({idx}/{len(st_cands)}) satisfies our criteria')
    st_cand_stats = _simplified_template_cand_gather_stats(st_cand, template_dict)
    return_dict['simplified_template_cands_stats'].append(st_cand_stats)
    success = st_cand_stats['success']

    if success:
      simplified_templates.append({
        'simplified_template': st_cand_stats['simplified_template'],
        'simplified_template_origin': st_cand_stats['simplified_template_origin'],
        'templatized_nodes_depths_sum': st_cand_stats['templatized_nodes_depths_sum'],
      })

  if len(simplified_templates) == 0:
    logger.warning(f'BAD no simplified templates were formed from {len(st_cands)} simpl.template candidates')
    return SimplifyTemplateValidationResult(return_dict)

  return_dict['success'] = True
  return_dict['simplified_templates'] = simplified_templates
  logger.debug(f'GOOD end of simplified template candidates validation')
  return SimplifyTemplateValidationResult(return_dict)


def _simplified_template_cand_gather_stats(st_cand: str, template_dict: dict) -> dict:
  src_lang = template_dict['src_lang']
  template_origin = template_dict['template_origin']
  templatized_node_ids_context : dict = template_dict['templatized_node_ids_context']
  template_context_str_replace : str = template_dict['template_context_str_replace']

  return_dict = {}
  return_dict['simplified_template_cand'] = st_cand
  return_dict['template_origin'] = template_origin
  return_dict['success'] = None
  return_dict['has_parse_error'] = None
  return_dict['is_type_isomorphic_to_template_origin'] = None
  return_dict['root_node_has_multiple_children'] = None
  return_dict['are_depths_at_templatized_nodes_within_limit'] = None
  return_dict['simplified_template'] = None
  return_dict['simplified_template_origin'] = None
  return_dict['templatized_nodes_depths_sum'] = None

  # criteria #1 - parse error
  has_parse_error = p_utils.does_have_parse_error(st_cand, src_lang)
  if has_parse_error:
    logger.debug(f'BAD: simplified template candidate has a parse error')
    return_dict['success'] = False
    return_dict['has_parse_error'] = True
    return return_dict

  # criteria #2 - type isomorphism with template
  tn_paths = list(templatized_node_ids_context.values())
  st_cand_ast_text, _ = d_ast_parse.parse_text_dbg(st_cand, src_lang, keep_text=True)
  template_origin_ast_text, _ = d_ast_parse.parse_text_dbg(template_origin, src_lang, keep_text=True)
  st_cand_tree = pds.PirelTree(st_cand_ast_text)
  template_origin_tree = pds.PirelTree(template_origin_ast_text)

  is_type_isomorphic_to_template_origin = _is_generated_code_type_isomorphic_to_shallow_template(
    st_cand_tree,
    template_origin_tree,
    tn_paths
  )

  if not is_type_isomorphic_to_template_origin:
    logger.debug(f'BAD: simplified template candidate is not type isomorphic to template origin')
    return_dict['success'] = False
    return_dict['has_parse_error'] = False
    return_dict['is_type_isomorphic_to_template_origin'] = False
    return return_dict

  # criteria #4 - number of children at root node
  st_cand_tree._fix_indentation()
  st_cand_root_node = st_cand_tree.get_root_node()

  if len(st_cand_root_node.get_children()) != 1:
    logger.debug(f'BAD: simplified template candidate\'s root node has multiple children')
    return_dict['success'] = False
    return_dict['has_parse_error'] = False
    return_dict['is_type_isomorphic_to_template_origin'] = True
    return_dict['root_node_has_multiple_children'] = True
    return return_dict

  # criteria #4 - depths at templatized nodes
  st_cand_context_node = st_cand_root_node.get_children()[0]
  tns_depths = []
  tns_texts = []
  for templatized_node_path in tn_paths:
    st_cand_tn = st_cand_context_node.get_child_by_path(templatized_node_path)
    tn_depth = st_cand_tn.get_depth()
    tn_text = st_cand_tn.get_text()
    tns_depths.append(tn_depth)
    tns_texts.append(tn_text)

  if not all(map(lambda depth: depth <= p_consts.LLM_VAL_TS_MAX_DEPTH, tns_depths)):
    logger.debug(f'BAD: one of templatized nodes of simplified template candidate exceeds depth threshold')
    return_dict['success'] = False
    return_dict['has_parse_error'] = False
    return_dict['is_type_isomorphic_to_template_origin'] = True
    return_dict['root_node_has_multiple_children'] = False
    return_dict['are_depths_at_templatized_nodes_within_limit'] = False
    return return_dict

  # SUCCESS - prepare simplified template
  for tn_text in tns_texts:
    template_context_str_replace = template_context_str_replace.replace(p_consts.CONTEXT_PH_TEXT, tn_text, 1)

  logger.debug(f'GOOD: simplified template candidate passed the validation step.')
  return_dict['success'] = True
  return_dict['has_parse_error'] = False
  return_dict['is_type_isomorphic_to_template_origin'] = True
  return_dict['root_node_has_multiple_children'] = False
  return_dict['are_depths_at_templatized_nodes_within_limit'] = True
  return_dict['simplified_template'] = template_context_str_replace
  return_dict['simplified_template_origin'] = st_cand
  return_dict['templatized_nodes_depths_sum'] = sum(tns_depths)

  return return_dict


# VALIDATE TP1 CANDIDATES (SP1-TP1 ~ PROGRAM PAIRS)
def val_tp1_candidates(tp1_cands: List[str], sp1: str, template_dict: dict, **kwargs) -> TranslateSP1ValidationResult:
  '''
  This function is invoked to check if the translation of the first
  program in source language is valid or not.

  CRITERIA:
  1. translation has no parse errors
  2. translation contains at least one context

  RETURN program pairs that satisfy criteria
  '''
  p_utils.log_json_time(f'{kwargs["subject_name"]}_args-val_tp1_candidates.json', locals())
  logger.debug(f'~~~ Starting validation of {len(tp1_cands)} TP1 candidates')

  tp1_cands_uniq = p_utils.deduplicate(tp1_cands)
  if len(tp1_cands_uniq) != len(tp1_cands):
    logger.warning(f'WARNING: {len(tp1_cands) - len(tp1_cands_uniq)} duplicate TP1 candidates were found')
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
    tp1_cand_stats = _tp1_cand_gather_stats(tp1_cand, sp1, template_dict, **kwargs)
    return_dict['tp1_cands_stats'].append(tp1_cand_stats)
    success = tp1_cand_stats['success']

    if success:
      program_pairs.append({'source': sp1, 'target': tp1_cand})

    logger.debug(f'TP1 candidate satisfies our criteria => ({success})')
    logger.debug(f'The number of good program pairs so far is {len(program_pairs)}/{len(tp1_cands)}')

  if len(program_pairs) == 0:
    _ = {'sp1': sp1, 'tp1_cands': tp1_cands}
    logger.warning(f'BAD: no program pairs were formed with {len(tp1_cands)} TP1 candidates:\n{json.dumps(_, indent=2)}')
    return TranslateSP1ValidationResult(return_dict)

  return_dict['success'] = True
  return_dict['program_pairs'] = program_pairs
  logger.debug(f'GOOD End of TP1 candidates validation.')
  logger.debug(f'The number of good program pairs is {len(program_pairs)}/{len(tp1_cands)}')
  return TranslateSP1ValidationResult(return_dict)


def _tp1_cand_gather_stats(tp1_cand: str, sp1: str, template_dict: dict, **kwargs) -> dict:
  contexts = template_dict['contexts']
  src_lang = template_dict['src_lang']
  tar_lang = template_dict['tar_lang']

  return_dict = {
    'sp1': sp1,
    'tp1_cand': tp1_cand,
    'success': None,
    'has_parse_error': None,
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

  # criteria 2
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
    return_dict['has_context'] = False
    return return_dict

  logger.debug('GOOD: TP1 candidate satisfies our criteria')
  return_dict['success'] = True
  return_dict['has_parse_error'] = False
  return_dict['has_context'] = True
  return return_dict


# VALIDATE TP2 CANDIDATES (SP1-TP1, SP2-TP2 ~ TRANSLATION PAIRS)
def val_tp2_candidates(tp2_cands: List[str], sp1: str, sp2: str, tp1_cand: str, template_dict: dict, **kwargs) -> TranslateSP2ValidationResult:
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
  p_utils.log_json_time(f'{kwargs["subject_name"]}_args-val_tp2_candidates.json', locals())
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
    tp2_cand_stat = _tp2_cand_gather_stats(sp1, sp2, tp1_cand, tp2_cand, template_dict, **kwargs)
    return_dict['tp2_cands_stats'].append(tp2_cand_stat)
    success = tp2_cand_stat['success']

    if success:
      translation_pairs.append(({'source': sp1, 'target': tp1_cand}, {'source': sp2, 'target': tp2_cand}))

  if len(translation_pairs) == 0:
    _ = {'sp1': sp1, 'sp2': sp2, 'tp1': tp1_cand, 'tp2_cands': tp2_cands}
    logger.warning(f'BAD: no translation pairs were formed with {len(tp2_cands)} TP2 candidates:\n{json.dumps(_, indent=2)}')
    return TranslateSP2ValidationResult(return_dict)

  return_dict['success'] = True
  return_dict['translation_pairs'] = translation_pairs
  logger.debug(f'GOOD End of TP2 candidates validation.')
  logger.debug(f'The number of good translation pairs is {len(translation_pairs)}/{len(tp2_cands)}')
  return TranslateSP2ValidationResult(return_dict)


def _tp2_cand_gather_stats(sp1: str, sp2: str, tp1_cand: str, tp2_cand: str, template_dict: dict, **kwargs) -> dict:
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
    src_lang,
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
  src_lang: str,
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


def _get_type_ahu_ter_x_ident_lit_encoding(tree: pds.DuoGlotTree) -> str:
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


def _get_type_ahu_encoding_x_ident(tree: pds.DuoGlotTree) -> str:
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
  f_gold_function: str,
  template_dict: dict,
  **kwargs
) -> GenTestFunctionValidationResult:
  '''
  This function is invoked to check if the generated test function candidates
  are valid or not.

  CRITERIA:
  1. generated test function candidates have no parse errors
  '''
  p_utils.log_json_time(f'{kwargs["subject_name"]}_args-val_gen_test_function_candidates.json', locals())
  logger.debug(f'~~~ Starting validation of {len(gen_test_fn_cands)} generated test function candidates')

  return_dict = {}
  return_dict['gen_test_fn_cands'] = gen_test_fn_cands
  return_dict['test_functions'] = []
  return_dict['success'] = False
  return_dict['gen_test_fn_cands_stats'] = []

  test_functions = []
  for idx, gen_test_fn_cand in enumerate(gen_test_fn_cands, start=1):
    logger.debug(f'Checking if generated test function candidate ({idx}/{len(gen_test_fn_cands)}) satisfies our criteria')
    gen_test_fn_cand_stats = _gen_test_fn_cand_gather_stats(gen_test_fn_cand, f_gold_function, template_dict)
    return_dict['gen_test_fn_cands_stats'].append(gen_test_fn_cand_stats)
    success = gen_test_fn_cand_stats['success']

    if success:
      test_functions.append(gen_test_fn_cand)

    logger.debug(f'Generated test function candidate satisfies our criteria => ({success})')
    logger.debug(f'The number of good test functions so far is {len(test_functions)}/{len(gen_test_fn_cands)}')

  if len(test_functions) == 0:
    _ = {'gen_test_fn_cands': gen_test_fn_cands}
    logger.warning(f'BAD: no test functions were formed with {len(gen_test_fn_cands)} generated test function candidates:\n{json.dumps(_, indent=2)}')
    return GenTestFunctionValidationResult(return_dict)

  return_dict['success'] = True
  return_dict['test_functions'] = test_functions
  logger.debug(f'GOOD: End of generated test function candidates validation.')
  logger.debug(f'The number of good test functions is {len(test_functions)}/{len(gen_test_fn_cands)}')
  return GenTestFunctionValidationResult(return_dict)


def _gen_test_fn_cand_gather_stats(gen_test_fn_cand: str, f_gold_function: str, template_dict: dict) -> dict:
  return_dict = {
    'gen_test_fn_cand': gen_test_fn_cand,
    'success': None,
    'has_parse_error': None,
    'has_single_fn_def_test': None,
  }

  logger.debug(f'Checking if generated test function candidate satisfies our criteria')
  logger.debug(f'\ngen_test_fn_cand:\n{repr(gen_test_fn_cand)}')

  # criteria 1
  if p_utils.does_have_parse_error(gen_test_fn_cand, template_dict['src_lang']):
    logger.debug(f'BAD: generated test function candidate has a parse error')
    return_dict['success'] = False
    return_dict['has_parse_error'] = True
    return return_dict

  # criteria 2
  # generated test function candidate should have:
  # 1. only one function definition
  # 2. and that function definition should be `def test()`
  ast, _ = d_ast_parse.parse_text_dbg(gen_test_fn_cand, template_dict['src_lang'])
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
  template_dict: dict,
  **kwargs
):
  '''
  This function is invoked to check if the reference translation candidates
  are valid or not.

  CRITERIA:
  1. reference translation candidates have no parse errors
  '''
  p_utils.log_json_time(f'{kwargs["subject_name"]}_args-val_get_ref_trans_candidates.json', locals())
  logger.debug(f'~~~ Starting validation of {len(ref_trans_cands)} reference translation candidates')

  return_dict = {}
  return_dict['ref_trans_cands'] = ref_trans_cands
  return_dict['ref_translations'] = []
  return_dict['success'] = False
  return_dict['ref_trans_cands_stats'] = []

  ref_translations = []
  for idx, ref_trans_cand in enumerate(ref_trans_cands, start=1):
    logger.debug(f'Checking if reference translation candidate ({idx}/{len(ref_trans_cands)}) satisfies our criteria')
    ref_trans_cand_stats = _get_ref_trans_cand_gather_stats(ref_trans_cand, template_dict)
    return_dict['ref_trans_cands_stats'].append(ref_trans_cand_stats)
    success = ref_trans_cand_stats['success']

    if success:
      ref_translations.append(ref_trans_cand)

    logger.debug(f'Reference translation candidate satisfies our criteria => ({success})')
    logger.debug(f'The number of reference translations so far is {len(ref_translations)}/{len(ref_trans_cands)}')

  if len(ref_translations) == 0:
    _ = {'ref_trans_cands': ref_trans_cands}
    logger.warning(
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
  template_dict: dict
):
  return_dict = {
    'ref_trans_cand': ref_trans_cand,
    'success': None,
    'has_parse_error': None,
  }

  logger.debug(f'Checking if generated reference translation candidate satisfies our criteria')
  logger.debug(f'\nref_trans_cand:\n{repr(ref_trans_cand)}')

  # criteria 1
  if p_utils.does_have_parse_error(ref_trans_cand, template_dict['tar_lang']):
    logger.debug(f'BAD: generated reference translation candidate has a parse error')
    return_dict['success'] = False
    return_dict['has_parse_error'] = True
    return return_dict

  logger.debug(f'GOOD: generated reference translation candidate passed the validation step.')
  return_dict['success'] = True
  return_dict['has_parse_error'] = False
  return return_dict


# COMMONLY USED FUNCTIONS IN THIS MODULE
def _is_generated_code_type_isomorphic_to_shallow_template(
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
def _test_val_simplified_template_candidates():
  template_fpath = Path('/code/repo-duoglot/backend/duoglotcore-server/pirel-logs/02-08-04-56-15.842895-TEMPLATE_p_pirel.json')
  simplified_template_candidates_fpath = Path('/code/repo-duoglot/backend/duoglotcore-server/pirel-logs/02-08-04-56-39.368370-st-cand-code-blocks.json')

  template_dict = p_utils.read_json(template_fpath)
  st_cands = p_utils.read_json(simplified_template_candidates_fpath)

  src_lang = template_dict['src_lang']
  template_origin = template_dict['template_origin']
  templatized_node_ids_context = template_dict['templatized_node_ids_context']

  kwargs = {
    'subject_name': 'test-templ-cands'
  }

  val_result_dict = val_simplified_template_candidates(src_lang, template_origin, templatized_node_ids_context, st_cands, **kwargs)
  p_utils.write_json('temporary_test_val_simplified_template_candidates.json', val_result_dict)

def _test_val_tp1_candidates():
  test_harness_config:dict = p_utils.read_json('temporary_test_val_tp1_candidates_config.json')
  args_dict = p_utils.read_json(test_harness_config['args_dict_fpath'])

  tp1_cands = args_dict['tp1_cands']
  sp1 = args_dict['sp1']
  template_dict = args_dict['template_dict']
  kwargs = args_dict['kwargs']

  val_result_dict = val_tp1_candidates(tp1_cands, sp1, template_dict, **kwargs)
  print(json.dumps(val_result_dict, indent=2, default=str))
  p_utils.write_json(f'temporary_test_val_tp1_candidates.json', val_result_dict)

def _test_val_translation_pair_candidates():
  test_harness_config:dict = p_utils.read_json('temporary_test_val_translation_pair_candidates_config.json')
  args_dict = p_utils.read_json(test_harness_config['args_dict_fpath'])

  tp2_cands = args_dict['tp2_cands']
  sp1 = args_dict['sp1']
  sp2 = args_dict['sp2']
  tp1_cand = args_dict['tp1_cand']
  template_dict = args_dict['template_dict']
  kwargs = args_dict['kwargs']

  val_result_dict = val_tp2_candidates(tp2_cands, sp1, sp2, tp1_cand, template_dict, **kwargs)
  p_utils.write_json('temporary_test_val_translation_pair_candidates.json', val_result_dict)

if __name__ == '__main__':
  # _test_val_translation_pair_candidates()
  _test_val_tp1_candidates()
