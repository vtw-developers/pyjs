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

  @classmethod
  def from_str(cls, rule: str) -> 'TRule':
    hash = d_utils.string_sha256(rule)
    return cls(hash=hash, rule=rule)

  @classmethod
  def from_dict(cls, obj: dict) -> 'TRule':
    hash = obj['hash']
    rule = obj['rule']
    syntax_val_res = None
    if 'syntax_val_res' in obj:
      syntax_val_res = TRuleSyntaxValRes.from_dict(obj['syntax_val_res'])
    return cls(hash=hash, rule=rule, syntax_val_res=syntax_val_res)

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

  @classmethod
  def from_dict(cls, obj: dict) -> 'TransPair':
    hash = obj['hash']
    sp1 = obj['sp1']
    sp2 = obj['sp2']
    tp1 = obj['tp1']
    tp2 = obj['tp2']
    contexts = []
    for ctx_dict in obj.get('contexts', []):
      ctx_obj = Context.from_dict(ctx_dict)
      contexts.append(ctx_obj)
    num_inferred_rules = obj.get('num_inferred_rules', 0)
    return cls(hash=hash, sp1=sp1, sp2=sp2, tp1=tp1, tp2=tp2,
               contexts=contexts, num_inferred_rules=num_inferred_rules)

@dataclass
class Sp1Tp1Cand:
  hash: str
  sp1: str
  tp1_cand: str

  @classmethod
  def from_gen_cands(cls, sp1_tp1_cand: Dict[str, str]) -> 'Sp1Tp1Cand':
    sp1 = sp1_tp1_cand['source']
    tp1_cand = sp1_tp1_cand['target']
    hash = d_utils.string_sha256(f'{sp1}{tp1_cand}')
    return cls(hash=hash, sp1=sp1, tp1_cand=tp1_cand)

  @classmethod
  def from_dict(cls, obj: dict) -> 'Sp1Tp1Cand':
    hash = obj['hash']
    sp1 = obj['sp1']
    tp1_cand = obj['tp1_cand']
    return cls(hash=hash, sp1=sp1, tp1_cand=tp1_cand)

##################################################################
############### TRANSLATION RULE VALIDATION ######################
##################################################################

@dataclass
class TRuleSyntaxValRes:
  is_valid: Optional[bool] = None
  reason: Optional[str] = None

  @classmethod
  def from_dict(cls, obj: dict) -> 'TRuleSyntaxValRes':
    is_valid = obj.get('is_valid', None)
    reason = obj.get('reason', None)
    return cls(is_valid=is_valid, reason=reason)

@dataclass
class PRuleFilterLog:
  translation_rules: List[TRule] = field(default_factory=list)

  @classmethod
  def from_dict(cls, obj: dict) -> 'PRuleFilterLog':
    translation_rules = []
    for tr_dict in obj.get('translation_rules', []):
      tr_obj = TRule.from_dict(tr_dict)
      translation_rules.append(tr_obj)
    return cls(translation_rules=translation_rules)

##################################################################
################ TRANSLATION RULE INFERENCE ######################
##################################################################

@dataclass
class RuleInfComb:
  largest_and_ignore: Optional[List[bool]] = None
  translation_rule: Optional[TRule] = None
  reason: Optional[str] = None
  num_inferred_rules: int = 0

  @classmethod
  def from_dict(cls, obj: dict) -> 'RuleInfComb':
    largest_and_ignore = obj.get('largest_and_ignore', None)
    translation_rule = None
    if 'translation_rule' in obj:
      translation_rule = TRule.from_dict(obj['translation_rule'])
    reason = obj.get('reason', None)
    num_inferred_rules = obj.get('num_inferred_rules', 0)
    return cls(largest_and_ignore=largest_and_ignore,
               translation_rule=translation_rule,
               reason=reason, num_inferred_rules=num_inferred_rules)

@dataclass
class Context:
  id: int
  source_context: List[str]
  target_context: List[str]
  num_inferred_rules: int = 0
  combinations: List[RuleInfComb] = field(default_factory=list)

  @classmethod
  def from_dict(cls, obj: dict) -> 'Context':
    id_ = obj['id']
    source_context = obj['source_context']
    target_context = obj['target_context']
    num_inferred_rules = obj.get('num_inferred_rules', 0)
    combinations = []
    for comb_dict in obj.get('combinations', []):
      comb_obj = RuleInfComb.from_dict(comb_dict)
      combinations.append(comb_obj)
    return cls(id=id_, source_context=source_context,
               target_context=target_context,
               num_inferred_rules=num_inferred_rules,
               combinations=combinations)

@dataclass
class PRuleInfLog:
  translation_pairs: List[TransPair] = field(default_factory=list)
  num_inferred_rules: int = 0

  @classmethod
  def from_dict(cls, obj: dict) -> 'PRuleInfLog':
    translation_pairs = []
    for tp_dict in obj.get('translation_pairs', []):
      tp_obj = TransPair.from_dict(tp_dict)
      translation_pairs.append(tp_obj)
    num_inferred_rules = obj.get('num_inferred_rules', 0)
    return cls(translation_pairs=translation_pairs,
               num_inferred_rules=num_inferred_rules)

##################################################################
################## TRANSLATION PAIR GENERATION ###################
##################################################################

@dataclass
class Feedback:
  id: int
  code_blocks: List[str] = field(default_factory=list)
  success: bool = False
  reason: Optional[str] = None

  @classmethod
  def from_dict(cls, obj: dict) -> 'Feedback':
    id_ = obj['id']
    code_blocks = obj.get('code_blocks', [])
    success = obj.get('success', False)
    reason = obj.get('reason', False)
    return cls(id=id_, code_blocks=code_blocks,
               success=success, reason=reason)

@dataclass
class TaskIteration:
  id: int
  starting_code_blocks: List[str] = field(default_factory=list)
  feedbacks: List[Feedback] = field(default_factory=list)
  success: bool = False
  reason: Optional[str] = None

  @classmethod
  def from_dict(cls, obj: dict) -> 'TaskIteration':
    id_ = obj['id']
    starting_code_blocks = obj.get('starting_code_blocks', [])
    feedbacks = []
    for fb_dict in obj.get('feedbacks', []):
      fb_obj = Feedback.from_dict(fb_dict)
      feedbacks.append(fb_obj)
    success = obj.get('success', False)
    reason = obj.get('reason', False)
    return cls(id=id_, starting_code_blocks=starting_code_blocks,
               feedbacks=feedbacks, success=success,
               reason=reason)

@dataclass
class TaskLoop:
  task_name: str
  task_iterations: List[TaskIteration] = field(default_factory=list)
  success: bool = False
  reason: Optional[str] = None

  @classmethod
  def from_dict(cls, obj: dict) -> 'TaskLoop':
    task_name = obj['task_name']
    task_iterations = []
    for ti_dict in obj.get('task_iterations', []):
      ti_obj = TaskIteration.from_dict(ti_dict)
      task_iterations.append(ti_obj)
    success = obj.get('success', False)
    reason = obj.get('reason', False)
    return cls(task_name=task_name, task_iterations=task_iterations,
               success=success, reason=reason)

@dataclass
class BaseTask:  # abstract class
  task_loop: Optional[TaskLoop] = None

@dataclass
class GenTestFunction(BaseTask):
  f_gold_function: Optional[str] = None
  test_function: Optional[str] = None
  success: bool = False
  reason: Optional[str] = None

  @classmethod
  def from_dict(cls, obj: dict) -> 'GenTestFunction':
    # task_loop is from superclass
    task_loop = None
    if 'task_loop' in obj:
      task_loop = TaskLoop.from_dict(obj['task_loop'])
    f_gold_function = obj.get('f_gold_function', None)
    test_function = obj.get('test_function', None)
    success = obj.get('success', False)
    reason = obj.get('reason', None)
    return cls(task_loop=task_loop, f_gold_function=f_gold_function,
               test_function=test_function, success=success, reason=reason)

@dataclass
class TransSP2(BaseTask):
  id: Optional[int] = None
  sp1_tp1_cand: Optional[Sp1Tp1Cand] = None
  sp2: Optional[str] = None
  sp1_sp2_are_identical: bool = False
  success: bool = False
  reason: Optional[str] = None
  translation_pairs: List[TransPair] = field(default_factory=list)

  @classmethod
  def from_dict(cls, obj: dict) -> 'TransSP2':
    # task_loop is from superclass
    task_loop = None
    if 'task_loop' in obj:
      task_loop = TaskLoop.from_dict(obj['task_loop'])
    id_ = obj.get('id', None)
    sp1_tp1_cand = None
    if 'sp1_tp1_cand' in obj:
      sp1_tp1_cand = Sp1Tp1Cand.from_dict(obj['sp1_tp1_cand'])
    sp2 = obj.get('sp2', None)
    sp1_sp2_are_identical = obj.get('sp1_sp2_are_identical', False)
    success = obj.get('success', False)
    reason = obj.get('reason', None)
    translation_pairs = []
    for tp_dict in obj.get('translation_pairs', []):
      tp_obj = TransPair.from_dict(tp_dict)
      translation_pairs.append(tp_obj)
    return cls(task_loop=task_loop, id=id_, sp1_tp1_cand=sp1_tp1_cand,
               sp2=sp2, sp1_sp2_are_identical=sp1_sp2_are_identical,
               success=success, reason=reason,
               translation_pairs=translation_pairs)

@dataclass
class TransSP1(BaseTask):
  sp1: Optional[str] = None
  success: bool = False
  reason: Optional[str] = None
  sp1_tp1_cands: List[Sp1Tp1Cand] = field(default_factory=list)

  @classmethod
  def from_dict(cls, obj: dict) -> 'TransSP1':
    # task_loop is from superclass
    task_loop = None
    if 'task_loop' in obj:
      task_loop = TaskLoop.from_dict(obj['task_loop'])
    sp1 = obj.get('sp1', None)
    success = obj.get('success', False)
    reason = obj.get('reason', None)
    sp1_tp1_cands = []
    for sp1_tp1_cand_dict in obj.get('sp1_tp1_cands', []):
      sp1_tp1_cand_obj = Sp1Tp1Cand.from_dict(sp1_tp1_cand_dict)
      sp1_tp1_cands.append(sp1_tp1_cand_obj)
    return cls(task_loop=task_loop, sp1=sp1, success=success,
               reason=reason, sp1_tp1_cands=sp1_tp1_cands)

@dataclass
class PLLMGenLog:
  trans_sp1: Optional[TransSP1] = None
  trans_sp2s: List[TransSP2] = field(default_factory=list)
  success: bool = False
  reason: Optional[str] = None

  @classmethod
  def from_dict(cls, obj: dict) -> 'PLLMGenLog':
    trans_sp1 = None
    if 'trans_sp1' in obj:
      trans_sp1 = TransSP1.from_dict(obj['trans_sp1'])
    trans_sp2s = []
    for trans_sp2_dict in obj.get('trans_sp2s', []):
      trans_sp2_obj = TransSP2.from_dict(trans_sp2_dict)
      trans_sp2s.append(trans_sp2_obj)
    success = obj.get('success', False)
    reason = obj.get('reason', None)
    return cls(trans_sp1=trans_sp1, trans_sp2s=trans_sp2s,
               success=success, reason=reason)

##################################################################
################## PiREL RULE LEARNING PHASE #####################
##################################################################

@dataclass
class RuleApplicationPhase:
  plausible_target_program: Optional[str] = None
  start_time: Optional[int] = None
  end_time: Optional[int] = None
  success: bool = False
  reason: Optional[str] = None

  @classmethod
  def from_dict(cls, obj: dict) -> 'RuleApplicationPhase':
    plausible_target_program = obj.get('plausible_target_program', None)
    start_time = obj.get('start_time', None)
    end_time = obj.get('end_time', None)
    success = obj.get('success', False)
    reason = obj.get('reason', None)
    return cls(plausible_target_program=plausible_target_program,
               start_time=start_time, end_time=end_time,
               success=success, reason=reason)

@dataclass
class RulesValidationRecovery:
  success: bool = False
  reason: Optional[str] = None

  @classmethod
  def from_dict(cls, obj: dict) -> 'RulesValidationRecovery':
    success = obj.get('success', False)
    reason = obj.get('reason', None)
    return cls(success=success, reason=reason)

@dataclass
class TRuleLearnAttempt:
  id: int
  p_llm_gen_log: Optional[PLLMGenLog] = None  # get_translation_pairs_from_tsp()
  p_rule_inferencer_log: Optional[PRuleInfLog] = None  # infer_translation_rules()
  p_rule_filter_log: Optional[PRuleFilterLog] = None  # filter_translation_rules()
  success: bool = False
  reason: Optional[str] = None

  @classmethod
  def from_dict(cls, obj: dict) -> 'TRuleLearnAttempt':
    id_ = obj['id']
    p_llm_gen_log = None
    if 'p_llm_gen_log' in obj:
      p_llm_gen_log = PLLMGenLog.from_dict(obj['p_llm_gen_log'])
    p_rule_inferencer_log = None
    if 'p_rule_inferencer_log' in obj:
      p_rule_inferencer_log = PRuleInfLog.from_dict(obj['p_rule_inferencer_log'])
    p_rule_filter_log = None
    if 'p_rule_filter_log' in obj:
      p_rule_filter_log = PRuleFilterLog.from_dict(obj['p_rule_filter_log'])
    success = obj.get('success', False)
    reason = obj.get('reason', None)
    return cls(id=id_, p_llm_gen_log=p_llm_gen_log,
               p_rule_inferencer_log=p_rule_inferencer_log,
               p_rule_filter_log=p_rule_filter_log,
               success=success, reason=reason)

@dataclass
class TSP:
  id: int
  sp1: str
  sp2: str
  trans_rule_learn_attempts: List[TRuleLearnAttempt] = field(default_factory=list)
  success: bool = False
  reason: Optional[str] = None

  @classmethod
  def from_dict(cls, obj: dict) -> 'TSP':
    id_ = obj['id']
    sp1 = obj['sp1']
    sp2 = obj['sp2']
    trans_rule_learn_attempts = []
    for trla_dict in obj.get('trans_rule_learn_attempts', {}):
      trla_obj = TRuleLearnAttempt.from_dict(trla_dict)
      trans_rule_learn_attempts.append(trla_obj)
    success = obj.get('success', False)
    reason = obj.get('reason', None)
    return cls(id=id_, sp1=sp1, sp2=sp2, trans_rule_learn_attempts=trans_rule_learn_attempts,
               success=success, reason=reason)

@dataclass
class NodeTransIteration:
  id: int
  node_id: Optional[int] = None
  node_type: Optional[str] = None
  template_origin: Optional[str] = None
  tsps: List[TSP] = field(default_factory=list)
  unchecked_trules: List[TRule] = field(default_factory=list)
  success: bool = False
  reason: Optional[str] = None

  @classmethod
  def from_dict(cls, obj: dict) -> 'NodeTransIteration':
    id_ = obj['id']
    node_id = obj.get('node_id', None)
    node_type = obj.get('node_type', None)
    template_origin = obj.get('template_origin', None)
    tsps = []
    for tsp_dict in obj.get('tsps', []):
      tsp_obj = TSP.from_dict(tsp_dict)
      tsps.append(tsp_obj)
    unchecked_trules = []
    for trule_dict in obj.get('unchecked_trules', []):
      trule_obj = TRule.from_dict(trule_dict)
      unchecked_trules.append(trule_obj)
    success = obj.get('success', False)
    reason = obj.get('reason', None)
    return cls(id=id_, node_id=node_id, node_type=node_type,
               template_origin=template_origin, tsps=tsps,
               unchecked_trules=unchecked_trules, success=success, reason=reason)

@dataclass
class StatementNode:
  id: int
  node_id: Optional[int] = None
  node_text: Optional[str] = None
  simplified_node_text: Optional[str] = None
  node_trans_iterations: List[NodeTransIteration] = field(default_factory=list)
  unchecked_trules: List[TRule] = field(default_factory=list)
  validation_and_recovery: Optional[RulesValidationRecovery] = None

  @classmethod
  def from_dict(cls, obj: dict) -> 'StatementNode':
    id_ = obj['id']
    node_id = obj.get('node_id', None)
    node_text = obj.get('node_text', None)
    simplified_node_text = obj.get('simplified_node_text', None)
    node_trans_iterations = []
    for nti_dict in obj.get('node_trans_iterations', []):
      nti_obj = NodeTransIteration.from_dict(nti_dict)
      node_trans_iterations.append(nti_obj)
    unchecked_trules = []
    for trule_dict in obj.get('unchecked_trules', []):
      trule_obj = TRule.from_dict(trule_dict)
      unchecked_trules.append(trule_obj)
    validation_and_recovery = None
    if 'validation_and_recovery' in obj:
      validation_and_recovery = RulesValidationRecovery.from_dict(obj['validation_and_recovery'])
    return cls(id=id_, node_id=node_id, node_text=node_text,
               simplified_node_text=simplified_node_text,
               node_trans_iterations=node_trans_iterations,
               unchecked_trules=unchecked_trules,
               validation_and_recovery=validation_and_recovery)

@dataclass
class RuleLearnPhase:
  statement_nodes: List[StatementNode] = field(default_factory=list)
  start_time: Optional[int] = None
  end_time: Optional[int] = None
  success: bool = False
  reason: Optional[str] = None

  @classmethod
  def from_dict(cls, obj: dict) -> 'RuleLearnPhase':
    statement_nodes = []
    for node_dict in obj.get('statement_nodes', []):
      node_obj = StatementNode.from_dict(node_dict)
      statement_nodes.append(node_obj)
    start_time = obj.get('start_time', None)
    end_time = obj.get('end_time', None)
    success = obj.get('success', False)
    reason = obj.get('reason', None)
    return cls(statement_nodes=statement_nodes, start_time=start_time,
               end_time=end_time, success=success, reason=reason)

@dataclass
class Subject:
  subject_name: str
  code_text: Optional[str] = None
  id: Optional[int] = None
  rule_learn_phase: Optional[RuleLearnPhase] = None
  rule_application_phase: Optional[RuleApplicationPhase] = None
  success: bool = False
  reason: Optional[str] = None

  @classmethod
  def from_dict(cls, obj: dict) -> 'Subject':
    subject_name = obj['subject_name']
    code_text = obj.get('code_text', None)
    id_ = obj.get('id', None)
    rule_learn_phase = None
    if 'rule_learn_phase' in obj:
      rule_learn_phase = RuleLearnPhase.from_dict(obj['rule_learn_phase'])
    rule_application_phase = None
    if 'rule_application_phase' in obj:
      rule_application_phase = RuleApplicationPhase.from_dict(obj['rule_application_phase'])
    success = obj.get('success', False)
    reason = obj.get('reason', None)
    return cls(subject_name=subject_name, code_text=code_text, id=id_,
               rule_learn_phase=rule_learn_phase, rule_application_phase=rule_application_phase,
               success=success, reason=reason)

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

  @classmethod
  def from_dict(cls, obj: dict) -> 'Benchmark':
    benchmark_name = obj['benchmark_name']
    sample_size = obj.get('sample_size', None)
    subjects = []
    for subject_dict in obj.get('subjects', []):
      subject_obj = Subject.from_dict(subject_dict)
      subjects.append(subject_obj)
    return cls(benchmark_name=benchmark_name, sample_size=sample_size, subjects=subjects)
