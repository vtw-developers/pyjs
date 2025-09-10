'''
Contains classes that store all the relevant information (log) about the
translation of a subject from source to target language.
The information is stored in a tree-like structure.
'''


from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import d_utils


##################################################################
######################## BASE CLASSES ############################
##################################################################
@dataclass
class BaseLogNode(ABC):
  '''
  ATTRIBUTES (stms, etms, success, reason)
  '''
  stms: Optional[int] = None  # start time in milliseconds
  etms: Optional[int] = None  # end time in milliseconds
  success: Optional[bool] = None
  reason: Optional[str] = None

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


@dataclass
class LLMQueryStat:
  stms: Optional[int] = None  # start time in milliseconds
  etms: Optional[int] = None  # end time in milliseconds
  num_tokens_prompt: Optional[int] = None  # input tokens
  num_tokens_completion: Optional[int] = None  # output tokens
  num_tokens_total: Optional[int] = None  # total tokens

  @classmethod
  def from_dict(cls, obj: dict) -> 'LLMQueryStat':
    stms = obj['stms']
    etms = obj['etms']
    num_tokens_prompt = obj['num_tokens_prompt']
    num_tokens_completion = obj['num_tokens_completion']
    num_tokens_total = obj['num_tokens_total']
    return cls(stms=stms, etms=etms,
               num_tokens_prompt=num_tokens_prompt,
               num_tokens_completion=num_tokens_completion,
               num_tokens_total=num_tokens_total)

##################################################################
################# TRANSLATION RULE FILTERING #####################
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
class PRuleFilterLog(BaseLogNode):
  trules_all: List[TRule] = field(default_factory=list)
  trules_syn_valid: List[TRule] = field(default_factory=list)
  # stms: Optional[int] = None  # in BaseLogNode
  # etms: Optional[int] = None  # in BaseLogNode
  # success: Optional[bool] = None  # in BaseLogNode
  # reason: Optional[str] = None  # in BaseLogNode

  @classmethod
  def from_dict(cls, obj: dict) -> 'PRuleFilterLog':
    trules_all = []
    for tr_dict in obj.get('trules_all', []):
      tr_obj = TRule.from_dict(tr_dict)
      trules_all.append(tr_obj)
    trules_syn_valid = []
    for tr_dict in obj.get('trules_syn_valid', []):
      tr_obj = TRule.from_dict(tr_dict)
      trules_syn_valid.append(tr_obj)
    # BaseLogNode
    stms = obj.get('stms', None)
    etms = obj.get('etms', None)
    success = obj.get('success', None)
    reason = obj.get('reason', None)
    return cls(trules_all=trules_all,
               trules_syn_valid=trules_syn_valid,
               stms=stms, etms=etms,
               success=success, reason=reason)

##################################################################
################## TRANSLATION RULE INFERENCE ####################
##################################################################

@dataclass
class RuleInfComb:
  largest_and_ignore: List[bool] = field(default_factory=list)
  translation_rule: Optional[TRule] = None
  reason: Optional[str] = None
  num_inferred_rules: int = 0

  @classmethod
  def from_dict(cls, obj: dict) -> 'RuleInfComb':
    largest_and_ignore = obj.get('largest_and_ignore', [])
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
    id_ = obj.get('id', None)
    source_context = obj.get('source_context', [])
    target_context = obj.get('target_context', [])
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
class PRuleInfLog(BaseLogNode):
  translation_pairs: List[TransPair] = field(default_factory=list)
  num_inferred_rules: int = 0
  # stms: Optional[int] = None  # in BaseLogNode
  # etms: Optional[int] = None  # in BaseLogNode
  # success: Optional[bool] = None  # in BaseLogNode
  # reason: Optional[str] = None  # in BaseLogNode

  @classmethod
  def from_dict(cls, obj: dict) -> 'PRuleInfLog':
    translation_pairs = []
    for tp_dict in obj.get('translation_pairs', []):
      tp_obj = TransPair.from_dict(tp_dict)
      translation_pairs.append(tp_obj)
    num_inferred_rules = obj.get('num_inferred_rules', 0)
    # BaseLogNode
    stms = obj.get('stms', None)
    etms = obj.get('etms', None)
    success = obj.get('success', None)
    reason = obj.get('reason', None)
    return cls(translation_pairs=translation_pairs,
               num_inferred_rules=num_inferred_rules,
               stms=stms, etms=etms,
               success=success, reason=reason)

##################################################################
################## TRANSLATION PAIR GENERATION ###################
##################################################################

@dataclass
class Feedback(BaseLogNode):
  id: Optional[int] = None
  code_blocks: List[str] = field(default_factory=list)
  # stms: Optional[int] = None  # in BaseLogNode
  # etms: Optional[int] = None  # in BaseLogNode
  # success: Optional[bool] = None  # in BaseLogNode
  # reason: Optional[str] = None  # in BaseLogNode

  @classmethod
  def from_dict(cls, obj: dict) -> 'Feedback':
    id_ = obj.get('id', None)
    code_blocks = obj.get('code_blocks', [])
    # BaseLogNode
    stms = obj.get('stms', None)
    etms = obj.get('etms', None)
    success = obj.get('success', None)
    reason = obj.get('reason', None)
    return cls(id=id_, code_blocks=code_blocks,
               stms=stms, etms=etms,
               success=success, reason=reason)


@dataclass
class TaskIteration(BaseLogNode):
  id: Optional[int] = None
  starting_code_blocks: List[str] = field(default_factory=list)
  feedbacks: List[Feedback] = field(default_factory=list)
  # stms: Optional[int] = None  # in BaseLogNode
  # etms: Optional[int] = None  # in BaseLogNode
  # success: Optional[bool] = None  # in BaseLogNode
  # reason: Optional[str] = None  # in BaseLogNode

  @classmethod
  def from_dict(cls, obj: dict) -> 'TaskIteration':
    id_ = obj.get('id', None)
    starting_code_blocks = obj.get('starting_code_blocks', [])
    feedbacks = []
    for fb_dict in obj.get('feedbacks', []):
      fb_obj = Feedback.from_dict(fb_dict)
      feedbacks.append(fb_obj)
    # BaseLogNode
    stms = obj.get('stms', None)
    etms = obj.get('etms', None)
    success = obj.get('success', None)
    reason = obj.get('reason', None)
    return cls(id=id_, starting_code_blocks=starting_code_blocks,
               feedbacks=feedbacks, stms=stms, etms=etms,
               success=success, reason=reason)


@dataclass
class TaskLoop(BaseLogNode):
  task_name: Optional[str] = None
  task_iterations: List[TaskIteration] = field(default_factory=list)
  # stms: Optional[int] = None  # in BaseLogNode
  # etms: Optional[int] = None  # in BaseLogNode
  # success: Optional[bool] = None  # in BaseLogNode
  # reason: Optional[str] = None  # in BaseLogNode

  @classmethod
  def from_dict(cls, obj: dict) -> 'TaskLoop':
    task_name = obj.get('task_name', None)
    task_iterations = []
    for ti_dict in obj.get('task_iterations', []):
      ti_obj = TaskIteration.from_dict(ti_dict)
      task_iterations.append(ti_obj)
    # BaseLogNode
    stms = obj.get('stms', None)
    etms = obj.get('etms', None)
    success = obj.get('success', None)
    reason = obj.get('reason', None)
    return cls(task_name=task_name, task_iterations=task_iterations,
               stms=stms, etms=etms,
               success=success, reason=reason)


@dataclass
class BaseTask(BaseLogNode, ABC):
  task_loop: Optional[TaskLoop] = None
  # stms: Optional[int] = None  # in BaseLogNode
  # etms: Optional[int] = None  # in BaseLogNode
  # success: Optional[bool] = None  # in BaseLogNode
  # reason: Optional[str] = None  # in BaseLogNode


@dataclass
class GetRefTrans(BaseTask):
  statement_str: Optional[str] = None
  ref_translations: List[str] = field(default_factory=list)
  llm_query_stats: List[LLMQueryStat] = field(default_factory=list)
  # task_loop: Optional[TaskLoop] = None  # in BaseTask
  # stms: Optional[int] = None  # in BaseLogNode (via BaseTask)
  # etms: Optional[int] = None  # in BaseLogNode (via BaseTask)
  # success: Optional[bool] = None  # in BaseLogNode (via BaseTask)
  # reason: Optional[str] = None  # in BaseLogNode (via BaseTask)

  @classmethod
  def from_dict(cls, obj: dict) -> 'GetRefTrans':
    statement_str = obj.get('statement_str', None)
    ref_translations = obj.get('ref_translations', [])
    llm_query_stats = []
    for stats_dict in obj.get('llm_query_stats', []):
      stats_obj = LLMQueryStat.from_dict(stats_dict)
      llm_query_stats.append(stats_obj)
    # BaseTask
    task_loop = None
    if 'task_loop' in obj:
      task_loop = TaskLoop.from_dict(obj['task_loop'])
    # BaseLogNode
    stms = obj.get('stms', None)
    etms = obj.get('etms', None)
    success = obj.get('success', None)
    reason = obj.get('reason', None)
    return cls(statement_str=statement_str, ref_translations=ref_translations,
               llm_query_stats=llm_query_stats,
               task_loop=task_loop,
               stms=stms, etms=etms, success=success, reason=reason)


@dataclass
class GenTestFn_deprecated(BaseTask):
  f_gold_function: Optional[str] = None
  test_function: Optional[str] = None
  llm_query_stats: List[LLMQueryStat] = field(default_factory=list)
  # task_loop: Optional[TaskLoop] = None  # in BaseTask
  # stms: Optional[int] = None  # in BaseLogNode (via BaseTask)
  # etms: Optional[int] = None  # in BaseLogNode (via BaseTask)
  # success: Optional[bool] = None  # in BaseLogNode (via BaseTask)
  # reason: Optional[str] = None  # in BaseLogNode (via BaseTask)

  @classmethod
  def from_dict_deprecated(cls, obj: dict) -> 'GenTestFn_deprecated':
    f_gold_function = obj.get('f_gold_function', None)
    test_function = obj.get('test_function', None)
    llm_query_stats = []
    for stats_dict in obj.get('llm_query_stats', []):
      stats_obj = LLMQueryStat.from_dict(stats_dict)
      llm_query_stats.append(stats_obj)
    # BaseTask
    task_loop = None
    if 'task_loop' in obj:
      task_loop = TaskLoop.from_dict(obj['task_loop'])
    # BaseLogNode
    stms = obj.get('stms', None)
    etms = obj.get('etms', None)
    success = obj.get('success', None)
    reason = obj.get('reason', None)
    return cls(f_gold_function=f_gold_function, test_function=test_function,
               llm_query_stats=llm_query_stats,
               task_loop=task_loop,
               stms=stms, etms=etms, success=success, reason=reason)

@dataclass
class TransSP2(BaseTask):
  id: Optional[int] = None
  sp1_tp1_cand: Optional[Sp1Tp1Cand] = None
  sp2: Optional[str] = None
  sp1_sp2_are_identical: Optional[bool] = None
  translation_pairs: List[TransPair] = field(default_factory=list)
  llm_query_stats: List[LLMQueryStat] = field(default_factory=list)
  # task_loop: Optional[TaskLoop] = None  # in BaseTask
  # stms: Optional[int] = None  # in BaseLogNode (via BaseTask)
  # etms: Optional[int] = None  # in BaseLogNode (via BaseTask)
  # success: Optional[bool] = None  # in BaseLogNode (via BaseTask)
  # reason: Optional[str] = None  # in BaseLogNode (via BaseTask)

  @classmethod
  def from_dict(cls, obj: dict) -> 'TransSP2':
    id_ = obj.get('id', None)
    sp1_tp1_cand = None
    if 'sp1_tp1_cand' in obj:
      sp1_tp1_cand = Sp1Tp1Cand.from_dict(obj['sp1_tp1_cand'])
    sp2 = obj.get('sp2', None)
    sp1_sp2_are_identical = obj.get('sp1_sp2_are_identical', None)
    translation_pairs = []
    for tp_dict in obj.get('translation_pairs', []):
      tp_obj = TransPair.from_dict(tp_dict)
      translation_pairs.append(tp_obj)
    llm_query_stats = []
    for stats_dict in obj.get('llm_query_stats', []):
      stats_obj = LLMQueryStat.from_dict(stats_dict)
      llm_query_stats.append(stats_obj)
    # BaseTask
    task_loop = None
    if 'task_loop' in obj:
      task_loop = TaskLoop.from_dict(obj['task_loop'])
    # BaseLogNode
    stms = obj.get('stms', None)
    etms = obj.get('etms', None)
    success = obj.get('success', None)
    reason = obj.get('reason', None)
    return cls(id=id_, sp1_tp1_cand=sp1_tp1_cand,
               sp2=sp2, sp1_sp2_are_identical=sp1_sp2_are_identical,
               translation_pairs=translation_pairs,
               llm_query_stats=llm_query_stats,
               task_loop=task_loop,
               stms=stms, etms=etms, success=success, reason=reason)


@dataclass
class TransSP1(BaseTask):
  sp1: Optional[str] = None
  sp1_tp1_cands: List[Sp1Tp1Cand] = field(default_factory=list)
  llm_query_stats: List[LLMQueryStat] = field(default_factory=list)
  # task_loop: Optional[TaskLoop] = None  # in BaseTask
  # stms: Optional[int] = None  # in BaseLogNode (via BaseTask)
  # etms: Optional[int] = None  # in BaseLogNode (via BaseTask)
  # success: Optional[bool] = None  # in BaseLogNode (via BaseTask)
  # reason: Optional[str] = None  # in BaseLogNode (via BaseTask)

  @classmethod
  def from_dict(cls, obj: dict) -> 'TransSP1':
    sp1 = obj.get('sp1', None)
    sp1_tp1_cands = []
    for sp1_tp1_cand_dict in obj.get('sp1_tp1_cands', []):
      sp1_tp1_cand_obj = Sp1Tp1Cand.from_dict(sp1_tp1_cand_dict)
      sp1_tp1_cands.append(sp1_tp1_cand_obj)
    llm_query_stats = []
    for stats_dict in obj.get('llm_query_stats', []):
      stats_obj = LLMQueryStat.from_dict(stats_dict)
      llm_query_stats.append(stats_obj)
    # BaseTask
    task_loop = None
    if 'task_loop' in obj:
      task_loop = TaskLoop.from_dict(obj['task_loop'])
    # BaseLogNode
    stms = obj.get('stms', None)
    etms = obj.get('etms', None)
    success = obj.get('success', None)
    reason = obj.get('reason', None)
    return cls(sp1=sp1, sp1_tp1_cands=sp1_tp1_cands,
               llm_query_stats=llm_query_stats,
               task_loop=task_loop,
               stms=stms, etms=etms, success=success, reason=reason)


@dataclass
class PLLMGenLog(BaseLogNode):
  trans_sp1: Optional[TransSP1] = None
  trans_sp2s: List[TransSP2] = field(default_factory=list)
  # stms: Optional[int] = None  # in BaseLogNode
  # etms: Optional[int] = None  # in BaseLogNode
  # success: Optional[bool] = None  # in BaseLogNode
  # reason: Optional[str] = None  # in BaseLogNode

  @classmethod
  def from_dict(cls, obj: dict) -> 'PLLMGenLog':
    trans_sp1 = None
    if 'trans_sp1' in obj:
      trans_sp1 = TransSP1.from_dict(obj['trans_sp1'])
    trans_sp2s = []
    for trans_sp2_dict in obj.get('trans_sp2s', []):
      trans_sp2_obj = TransSP2.from_dict(trans_sp2_dict)
      trans_sp2s.append(trans_sp2_obj)
    # BaseLogNode
    stms = obj.get('stms', None)
    etms = obj.get('etms', None)
    success = obj.get('success', None)
    reason = obj.get('reason', None)
    return cls(trans_sp1=trans_sp1, trans_sp2s=trans_sp2s,
               stms=stms, etms=etms,
               success=success, reason=reason)

##################################################################
################## PiREL RULE LEARNING PHASE #####################
##################################################################

@dataclass
class RuleApplicationPhase(BaseLogNode):
  tar_main_code_plausible: Optional[str] = None
  # stms: Optional[int] = None  # in BaseLogNode
  # etms: Optional[int] = None  # in BaseLogNode
  # success: Optional[bool] = None  # in BaseLogNode
  # reason: Optional[str] = None  # in BaseLogNode

  @classmethod
  def from_dict(cls, obj: dict) -> 'RuleApplicationPhase':
    tar_main_code_plausible = obj.get('tar_main_code_plausible', None)
    # BaseLogNode
    stms = obj.get('stms', None)
    etms = obj.get('etms', None)
    success = obj.get('success', None)
    reason = obj.get('reason', None)
    return cls(tar_main_code_plausible=tar_main_code_plausible,
               stms=stms, etms=etms,
               success=success, reason=reason)


@dataclass
class RuleLearnRec(BaseLogNode):
  get_ref_trans: Optional[GetRefTrans] = None
  # stms: Optional[int] = None  # in BaseLogNode
  # etms: Optional[int] = None  # in BaseLogNode
  # success: Optional[bool] = None  # in BaseLogNode
  # reason: Optional[str] = None  # in BaseLogNode

  @classmethod
  def from_dict(cls, obj: dict) -> 'RuleLearnRec':
    get_ref_trans = None
    if 'get_ref_trans' in obj:
      get_ref_trans = GetRefTrans.from_dict(obj['get_ref_trans'])
    # BaseLogNode
    stms = obj.get('stms', None)
    etms = obj.get('etms', None)
    success = obj.get('success', None)
    reason = obj.get('reason', None)
    return cls(get_ref_trans=get_ref_trans,
               stms=stms, etms=etms,
               success=success, reason=reason)


@dataclass
class TRuleLearnAttempt(BaseLogNode):
  id: Optional[int] = None
  p_llm_gen_log: Optional[PLLMGenLog] = None
  p_rule_inferencer_log: Optional[PRuleInfLog] = None
  p_rule_filter_log: Optional[PRuleFilterLog] = None
  # stms: Optional[int] = None  # in BaseLogNode
  # etms: Optional[int] = None  # in BaseLogNode
  # success: Optional[bool] = None  # in BaseLogNode
  # reason: Optional[str] = None  # in BaseLogNode

  @classmethod
  def from_dict(cls, obj: dict) -> 'TRuleLearnAttempt':
    id_ = obj.get('id', None)
    p_llm_gen_log = None
    if 'p_llm_gen_log' in obj:
      p_llm_gen_log = PLLMGenLog.from_dict(obj['p_llm_gen_log'])
    p_rule_inferencer_log = None
    if 'p_rule_inferencer_log' in obj:
      p_rule_inferencer_log = PRuleInfLog.from_dict(obj['p_rule_inferencer_log'])
    p_rule_filter_log = None
    if 'p_rule_filter_log' in obj:
      p_rule_filter_log = PRuleFilterLog.from_dict(obj['p_rule_filter_log'])
    # BaseLogNode
    stms = obj.get('stms', None)
    etms = obj.get('etms', None)
    success = obj.get('success', None)
    reason = obj.get('reason', None)
    return cls(id=id_, p_llm_gen_log=p_llm_gen_log,
               p_rule_inferencer_log=p_rule_inferencer_log,
               p_rule_filter_log=p_rule_filter_log,
               success=success, reason=reason,
               stms=stms, etms=etms)


@dataclass
class TSP(BaseLogNode):
  id: Optional[int] = None
  sp1: Optional[str] = None
  sp2: Optional[str] = None
  trule_learn_attempts: List[TRuleLearnAttempt] = field(default_factory=list)
  # stms: Optional[int] = None  # in BaseLogNode
  # etms: Optional[int] = None  # in BaseLogNode
  # success: Optional[bool] = None  # in BaseLogNode
  # reason: Optional[str] = None  # in BaseLogNode

  @classmethod
  def from_dict(cls, obj: dict) -> 'TSP':
    id_ = obj.get('id', None)
    sp1 = obj.get('sp1', None)
    sp2 = obj.get('sp2', None)
    trule_learn_attempts = []
    for trla_dict in obj.get('trule_learn_attempts', []):
      trla_obj = TRuleLearnAttempt.from_dict(trla_dict)
      trule_learn_attempts.append(trla_obj)
    # BaseLogNode
    stms = obj.get('stms', None)
    etms = obj.get('etms', None)
    success = obj.get('success', None)
    reason = obj.get('reason', None)
    return cls(id=id_, sp1=sp1, sp2=sp2, trule_learn_attempts=trule_learn_attempts,
               success=success, reason=reason, stms=stms, etms=etms)


@dataclass
class NodeTransIter(BaseLogNode):
  id: Optional[int] = None
  node_id: Optional[int] = None
  node_type: Optional[str] = None
  template_origin: Optional[str] = None
  tsps: List[TSP] = field(default_factory=list)
  # stms: Optional[int] = None  # in BaseLogNode
  # etms: Optional[int] = None  # in BaseLogNode
  # success: Optional[bool] = None  # in BaseLogNode
  # reason: Optional[str] = None  # in BaseLogNode

  @classmethod
  def from_dict(cls, obj: dict) -> 'NodeTransIter':
    id_ = obj.get('id', None)
    node_id = obj.get('node_id', None)
    node_type = obj.get('node_type', None)
    template_origin = obj.get('template_origin', None)
    tsps = []
    for tsp_dict in obj.get('tsps', []):
      tsp_obj = TSP.from_dict(tsp_dict)
      tsps.append(tsp_obj)
    # BaseLogNode
    stms = obj.get('stms', None)
    etms = obj.get('etms', None)
    success = obj.get('success', None)
    reason = obj.get('reason', None)
    return cls(id=id_, node_id=node_id, node_type=node_type,
               template_origin=template_origin, tsps=tsps,
               success=success, reason=reason,
               stms=stms, etms=etms)


@dataclass
class RuleLearnStd(BaseLogNode):
  node_trans_iters: List[NodeTransIter] = field(default_factory=list)
  # stms: Optional[int] = None  # in BaseLogNode
  # etms: Optional[int] = None  # in BaseLogNode
  # success: Optional[bool] = None  # in BaseLogNode
  # reason: Optional[str] = None  # in BaseLogNode

  @classmethod
  def from_dict(cls, obj: dict) -> 'RuleLearnStd':
    node_trans_iters = []
    for nti_dict in obj.get('node_trans_iters', []):
      nti_obj = NodeTransIter.from_dict(nti_dict)
      node_trans_iters.append(nti_obj)
    # BaseLogNode
    stms = obj.get('stms', None)
    etms = obj.get('etms', None)
    success = obj.get('success', None)
    reason = obj.get('reason', None)
    return cls(node_trans_iters=node_trans_iters,
               success=success, reason=reason,
               stms=stms, etms=etms)


@dataclass
class StatNodeVal(BaseLogNode):
  v1_enough_rules: Optional[bool] = None
  v2_expr_valid_ok: Optional[bool] = None
  v2_expr_valid_stms: Optional[int] = None
  v2_expr_valid_etms: Optional[int] = None
  v3_rule_apply_ok: Optional[bool] = None
  v3_rule_apply_stms: Optional[int] = None
  v3_rule_apply_etms: Optional[int] = None
  # stms: Optional[int] = None  # in BaseLogNode
  # etms: Optional[int] = None  # in BaseLogNode
  # success: Optional[bool] = None  # in BaseLogNode
  # reason: Optional[str] = None  # in BaseLogNode

  @classmethod
  def from_dict(cls, obj: dict) -> 'StatNodeVal':
    v1_enough_rules = obj.get('v1_enough_rules', None)
    v2_expr_valid_ok = obj.get('v2_expr_valid_ok', None)
    v2_expr_valid_stms = obj.get('v2_expr_valid_stms', None)
    v2_expr_valid_etms = obj.get('v2_expr_valid_etms', None)
    v3_rule_apply_ok = obj.get('v3_rule_apply_ok', None)
    v3_rule_apply_stms = obj.get('v3_rule_apply_stms', None)
    v3_rule_apply_etms = obj.get('v3_rule_apply_etms', None)
    # BaseLogNode
    stms = obj.get('stms', None)
    etms = obj.get('etms', None)
    success = obj.get('success', None)
    reason = obj.get('reason', None)
    return cls(v1_enough_rules=v1_enough_rules,
               v2_expr_valid_ok=v2_expr_valid_ok,
               v2_expr_valid_stms=v2_expr_valid_stms,
               v2_expr_valid_etms=v2_expr_valid_etms,
               v3_rule_apply_ok=v3_rule_apply_ok,
               v3_rule_apply_stms=v3_rule_apply_stms,
               v3_rule_apply_etms=v3_rule_apply_etms,
               stms=stms, etms=etms,
               success=success, reason=reason)

@dataclass
class StatNodeIter(BaseLogNode):
  id: Optional[int] = None
  stat_node_val: Optional[StatNodeVal] = None
  stat_node_learn_std: Optional[RuleLearnStd] = None
  stat_node_learn_rec: Optional[RuleLearnRec] = None
  # stms: Optional[int] = None  # in BaseLogNode
  # etms: Optional[int] = None  # in BaseLogNode
  # success: Optional[bool] = None  # in BaseLogNode
  # reason: Optional[str] = None  # in BaseLogNode

  @classmethod
  def from_dict(cls, obj: dict) -> 'StatNodeIter':
    id_ = obj.get('id', None)
    stat_node_val = None
    if 'stat_node_val' in obj:
      stat_node_val = StatNodeVal.from_dict(obj['stat_node_val'])
    stat_node_learn_std = None
    if 'stat_node_learn_std' in obj:
      stat_node_learn_std = RuleLearnStd.from_dict(obj['stat_node_learn_std'])
    stat_node_learn_rec = None
    if 'stat_node_learn_rec' in obj:
      stat_node_learn_rec = RuleLearnRec.from_dict(obj['stat_node_learn_rec'])
    # BaseLogNode
    stms = obj.get('stms', None)
    etms = obj.get('etms', None)
    success = obj.get('success', None)
    reason = obj.get('reason', None)
    return cls(id=id_, stat_node_val=stat_node_val,
               stat_node_learn_std=stat_node_learn_std,
               stat_node_learn_rec=stat_node_learn_rec,
               stms=stms, etms=etms,
               success=success, reason=reason)


@dataclass
class StatNode(BaseLogNode):
  id: Optional[int] = None
  node_id: Optional[int] = None
  node_text: Optional[str] = None
  pre_context: Optional[str] = None
  simple_ntext: Optional[str] = None
  stat_node_iters: List[StatNodeIter] = field(default_factory=list)
  # stms: Optional[int] = None  # in BaseLogNode
  # etms: Optional[int] = None  # in BaseLogNode
  # success: Optional[bool] = None  # in BaseLogNode
  # reason: Optional[str] = None  # in BaseLogNode

  @classmethod
  def from_dict(cls, obj: dict) -> 'StatNode':
    id_ = obj.get('id', None)
    node_id = obj.get('node_id', None)
    node_text = obj.get('node_text', None)
    pre_context = obj.get('pre_context', None)
    simple_ntext = obj.get('simple_ntext', None)
    stat_node_iters = []
    for sni_dict in obj.get('stat_node_iters', []):
      sni_obj = StatNodeIter.from_dict(sni_dict)
      stat_node_iters.append(sni_obj)
    # BaseLogNode
    stms = obj.get('stms', None)
    etms = obj.get('etms', None)
    success = obj.get('success', False)
    reason = obj.get('reason', None)
    return cls(id=id_, node_id=node_id, node_text=node_text,
               pre_context=pre_context, simple_ntext=simple_ntext,
               stat_node_iters=stat_node_iters,
               stms=stms, etms=etms, success=success, reason=reason)


@dataclass
class RuleLearnPhase(BaseLogNode):
  num_stat_nodes: Optional[int] = None
  stat_nodes: List[StatNode] = field(default_factory=list)
  # stms: Optional[int] = None  # in BaseLogNode
  # etms: Optional[int] = None  # in BaseLogNode
  # success: Optional[bool] = None  # in BaseLogNode
  # reason: Optional[str] = None  # in BaseLogNode

  @classmethod
  def from_dict(cls, obj: dict) -> 'RuleLearnPhase':
    num_stat_nodes = obj.get('num_stat_nodes', None)
    stat_nodes = []
    for sn_dict in obj.get('stat_nodes', []):
      sn_obj = StatNode.from_dict(sn_dict)
      stat_nodes.append(sn_obj)
    # BaseLogNode
    stms = obj.get('stms', None)
    etms = obj.get('etms', None)
    success = obj.get('success', None)
    reason = obj.get('reason', None)
    return cls(num_stat_nodes=num_stat_nodes, stat_nodes=stat_nodes,
               stms=stms, etms=etms,
               success=success, reason=reason)


@dataclass
class Subject():
  id: Optional[int] = None
  subject_name: Optional[str] = None
  src_main_code: Optional[str] = None
  rule_learn_phase: Optional[RuleLearnPhase] = None
  rule_application_phase: Optional[RuleApplicationPhase] = None

  def get_primitive_stats(self) -> tuple:
    return (
      self.rule_learn_phase.success if self.rule_learn_phase else None,
      self.rule_application_phase.success if self.rule_application_phase else None
    )

  @classmethod
  def from_dict(cls, obj: dict) -> 'Subject':
    id_ = obj.get('id', None)
    subject_name = obj.get('subject_name', None)
    src_main_code = obj.get('src_main_code', None)
    rule_learn_phase = None
    if 'rule_learn_phase' in obj:
      rule_learn_phase = RuleLearnPhase.from_dict(obj['rule_learn_phase'])
    rule_application_phase = None
    if 'rule_application_phase' in obj:
      rule_application_phase = RuleApplicationPhase.from_dict(obj['rule_application_phase'])
    return cls(id=id_, subject_name=subject_name,
               src_main_code=src_main_code,
               rule_learn_phase=rule_learn_phase,
               rule_application_phase=rule_application_phase)


@dataclass
class Benchmark:
  benchmark_name: Optional[str] = None
  sample_size: Optional[int] = None
  subjects: List[Subject] = field(default_factory=list)

  def get_primitive_stats(self) -> List[dict]:
    stats = []
    for subject in self.subjects:
      stats.append(subject.get_primitive_stats())
    return stats

  @classmethod
  def from_dict(cls, obj: dict) -> 'Benchmark':
    benchmark_name = obj.get('benchmark_name', None)
    sample_size = obj.get('sample_size', None)
    subjects = []
    for subject_dict in obj.get('subjects', []):
      subject_obj = Subject.from_dict(subject_dict)
      subjects.append(subject_obj)
    return cls(benchmark_name=benchmark_name, sample_size=sample_size, subjects=subjects)
