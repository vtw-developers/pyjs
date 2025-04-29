'''
Contains classes that store all the relevant information (log) about the
translation of a subject from source to target language.
The information is stored in a tree-like structure.
'''


from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import d_utils


##################################################################
###################### COMMON CLASSES ############################
##################################################################

@dataclass
class TRule:
  hash: str
  rule: str
  syntax_val_res: Optional['TRuleSyntaxValRes'] = None
  test_based_val_res: Optional['TRuleTestBasedValRes'] = None
  @classmethod
  def from_str(cls, rule: str) -> 'TRule':
    hash = d_utils.string_sha256(rule)
    return cls(hash=hash, rule=rule)

@dataclass
class TransPair:
  hash: str
  sp1: str
  sp2: str
  tp1: str
  tp2: str
  contexts: List['Context'] = field(default_factory=list)
  num_inferred_rules: int = 0
  @classmethod
  def from_tuple(cls, translation_pair: Tuple[Dict[str, str], Dict[str, str]]) -> 'TransPair':
    sp1 = translation_pair[0]['source']
    tp1 = translation_pair[0]['target']
    sp2 = translation_pair[1]['source']
    tp2 = translation_pair[1]['target']
    hash = d_utils.string_sha256(f'{sp1}{tp1}{sp2}{tp2}')
    return cls(hash=hash, sp1=sp1, tp1=tp1, sp2=sp2, tp2=tp2)

@dataclass
class Sp1Tp1Cand:
  hash: str
  sp1: str
  tp1_cand: str
  @classmethod
  def from_dict(cls, sp1_tp1_cand: Dict[str, str]) -> 'Sp1Tp1Cand':
    sp1 = sp1_tp1_cand['source']
    tp1_cand = sp1_tp1_cand['target']
    hash = d_utils.string_sha256(f'{sp1}{tp1_cand}')
    return cls(hash=hash, sp1=sp1, tp1_cand=tp1_cand)

##################################################################
############### TRANSLATION RULE VALIDATION ######################
##################################################################

@dataclass
class TRuleSyntaxValRes:
  is_valid: Optional[bool] = None
  reason: Optional[str] = None

@dataclass
class TRuleTestBasedValRes:
  snippet_under_test: Optional[str] = None
  paramable_ids: Optional[List[str]] = None
  f_gold_for_pynguin: Optional[str] = None
  is_valid: Optional[bool] = None
  reason: Optional[str] = None
  num_generated_tests: Optional[int] = None
  num_pynguin_attempts: Optional[int] = None
  pynguin_generated_tests: List[str] = field(default_factory=list)
  generated_test_that_is_used: Optional[str] = None
  test_script: Optional[str] = None

@dataclass
class PRuleValLog:
  translation_rules: List[TRule] = field(default_factory=list)

##################################################################
################ TRANSLATION RULE INFERENCE ######################
##################################################################

@dataclass
class RuleInfComb:
  largest_and_ignore: Optional[List[bool]] = None
  translation_rule: Optional[TRule] = None
  reason: Optional[str] = None
  num_inferred_rules: int = 0

@dataclass
class Context:
  id: int
  source_context: List[str]
  target_context: List[str]
  num_inferred_rules: int = 0
  combinations: List[RuleInfComb] = field(default_factory=list)

@dataclass
class PRuleInfLog:
  translation_pairs: List[TransPair] = field(default_factory=list)
  num_inferred_rules: int = 0

##################################################################
################## TRANSLATION PAIR GENERATION ###################
##################################################################

@dataclass
class Feedback:
  id: int
  code_blocks: List[str] = field(default_factory=list)
  success: bool = False
  reason: Optional[str] = None

@dataclass
class TaskIteration:
  id: int
  starting_code_blocks: List[str] = field(default_factory=list)
  feedbacks: List[Feedback] = field(default_factory=list)
  success: bool = False
  reason: Optional[str] = None

@dataclass
class TaskLoop:
  task_name: str
  task_iterations: List[TaskIteration] = field(default_factory=list)
  success: bool = False
  reason: Optional[str] = None

@dataclass
class BaseTrans:
  task_loop: Optional[TaskLoop] = None

@dataclass
class TransSP2(BaseTrans):
  id: Optional[int] = None
  sp1_tp1_cand: Optional[Sp1Tp1Cand] = None
  sp2: Optional[str] = None
  sp1_sp2_are_identical: bool = False
  success: bool = False
  reason: Optional[str] = None
  translation_pairs: List[TransPair] = field(default_factory=list)

@dataclass
class TransSP1(BaseTrans):
  sp1: Optional[str] = None
  success: bool = False
  reason: Optional[str] = None
  sp1_tp1_cands: List[Sp1Tp1Cand] = field(default_factory=list)

@dataclass
class PLLMGenLog:
  trans_sp1: Optional[TransSP1] = None
  trans_sp2s: List[TransSP2] = field(default_factory=list)
  success: bool = False
  reason: Optional[str] = None

##################################################################
################## PiREL RULE LEARNING PHASE #####################
##################################################################

@dataclass
class TRuleLearnAttempt:
  id: int
  num_trules: Optional[int] = None
  success: bool = False
  reason: Optional[str] = None
  p_llm_gen_log: Optional[PLLMGenLog] = None  # get_translation_pairs_from_tsp()
  p_rule_inferencer_log: Optional[PRuleInfLog] = None  # infer_translation_rules()
  p_rule_validator_log: Optional[PRuleValLog] = None  # filter_translation_rules()

@dataclass
class TSP:
  id: int
  sp1: str
  sp2: str
  sp3: str
  success: bool = False
  reason: Optional[str] = None
  trans_rule_learn_attempts: List[TRuleLearnAttempt] = field(default_factory=list)
  learned_translation_rules: List[TRule] = field(default_factory=list)

@dataclass
class ProbNode:
  node_id: int
  node_type: str
  template_origin: Optional[str] = None
  success: bool = False
  reason: Optional[str] = None
  tsps: List[TSP] = field(default_factory=list)

@dataclass
class TransIteration:
  id: int
  success: bool = False
  reason: Optional[str] = None
  problematic_node: Optional[ProbNode] = None

@dataclass
class RuleLearnPhase:
  translation_iterations: List[TransIteration] = field(default_factory=list)
  start_time: Optional[int] = None
  end_time: Optional[int] = None
  success: bool = False
  reason: Optional[str] = None

@dataclass
class RuleApplicationPhase:
  plausible_target_program: Optional[str] = None
  start_time: Optional[int] = None
  end_time: Optional[int] = None
  success: bool = False
  reason: Optional[str] = None

@dataclass
class Subject:
  subject_name: str
  id: Optional[int] = None
  rule_learn_phase: Optional[RuleLearnPhase] = None
  rule_application_phase: Optional[RuleApplicationPhase] = None
  success: bool = False
  reason: Optional[str] = None
  def get_total_time(self) -> str:
    assert self.rule_learn_phase.start_time is not None, 'Start time must be set'
    assert self.rule_learn_phase.end_time is not None, 'End time must be set'
    # only rule learn phase ran
    start_time = self.rule_learn_phase.start_time
    end_time = self.rule_learn_phase.end_time
    # if rule application phase ran, end time is the end time of the rule application phase
    if self.rule_application_phase is not None:
      assert self.rule_application_phase.start_time is not None, 'Start time must be set'
      assert self.rule_application_phase.end_time is not None, 'End time must be set'
      end_time = self.rule_application_phase.end_time
    total_sec = end_time - start_time
    if total_sec < 60:
      return f'{total_sec}s'
    total_min, total_sec = divmod(total_sec, 60)
    total_hr, total_min = divmod(total_min, 60)
    if total_hr == 0:
      return f'{total_min}m{total_sec}s'
    return f'{total_hr}h{total_min}m{total_sec}s'

@dataclass
class Benchmark:
  benchmark_name: str
  sample_size: Optional[int] = None
  subjects: List[Subject] = field(default_factory=list)
