'''
Module for creating various LLM messages for prompting such as
starting messages and feedback messages
'''


import json
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

import p_consts
import p_data_structures as pds
import p_llm_templates
import p_llm_val
import p_subject
import p_utils
from langchain_core.messages.human import HumanMessage
from langchain_core.prompts.chat import HumanMessagePromptTemplate


logger = p_utils.setup_logger(__name__)


class FeedbackImpossibleError(RuntimeError): pass


class BaseMessageFactory(ABC):
  def __init__(self, template_dict: dict, subject: p_subject.PirelSubject):
    self.template_dict = template_dict
    self.subject = subject

    self.src_lang = self.subject.src_lang
    self.tar_lang = self.subject.tar_lang
    self.src_language = p_consts.LANG_DICT[self.src_lang]
    self.tar_language = p_consts.LANG_DICT[self.tar_lang]

  def __repr__(self) -> str:
    return f'MsgFactory_{self.__class__.__name__}'

  def _log(self, msg: str) -> None:
    logger.debug(f'{repr(self)}: {msg}')

  def log_args(self, **kwargs) -> None:
    log_data = {'template_dict': self.template_dict}
    log_data.update(kwargs)
    p_utils.log_file_time(f'{kwargs["subject_name"]}_{repr(self)}-args.json', json.dumps(log_data))

  def get_message_have_parse_error(self, cands_w_error: List[str]) -> HumanMessage:
    # cand_descs
    cand_descs = ''
    for cand_code in cands_w_error:
      cand_desc = p_llm_templates.TranslateAny.Feedback.ParseError.CAND_DESC.format(
        tar_language=self.tar_language,
        cand_code=cand_code
      )
      cand_descs += cand_desc + '\n\n\n'
    # MESSAGE
    feedback_message = HumanMessage(
      p_llm_templates.TranslateAny.Feedback.ParseError.MAIN.format(
        cand_descs=cand_descs
      )
    )
    return feedback_message

  def get_message_no_code_blocks(self) -> HumanMessage:
    return HumanMessage('Please provide code snippets in your response.')

  @abstractmethod
  def get_feedback_message(self) -> HumanMessage:
    pass


# TRANSLATE SP1
class BaseTranslateSP1Factory(BaseMessageFactory):
  def __init__(self, template_dict: dict, subject: p_subject.PirelSubject, val: p_llm_val.TranslateSP1ValidationResult):
    super().__init__(template_dict, subject)
    self.val = val

  def get_message_miss_context(self, tp1_cands_w_error: List[str], sp1: str) -> HumanMessage:
    def _get_tp1_cand_ast_desired() -> str:
      ''''''
      # NOTE TODO contexts is a list of contexts; which one should be selected?
      target_context = self.template_dict['contexts'][0]['target_context']
      result_str = 'program'  # TODO HACK
      for idx, parent_and_siblings in enumerate(reversed(target_context), start=1):
        siblings_and_parent = reversed(parent_and_siblings)
        for sap in siblings_and_parent:
          if sap == 'unknown':
            continue
          ntype = sap.strip('"').split('.')[-1]
          result_str += '\n'
          result_str += '  ' * idx + ntype
      return result_str

    # st_tp1_cand_descs
    st_tp1_cand_descs = ''
    for tp1c_err in tp1_cands_w_error:
      tp1_cand_ast_current = pds.DuoGlotTree.from_code_str(tp1c_err, self.tar_lang).tree_as_str()
      st_tp1_cand_desc = p_llm_templates.TranslateSP1.Feedback.MissingContext.ST_TP1_CAND_DESC.format(
        tar_language=self.tar_language,
        tp1_cand=tp1c_err,
        src_language=self.src_language,
        sp1=sp1,
        tp1_cand_ast_current=tp1_cand_ast_current
      )
      st_tp1_cand_descs += st_tp1_cand_desc + '\n\n\n'

    # st_grammar_cands_number
    if len(tp1_cands_w_error) > 1:
      st_grammar_cands_number = p_llm_templates.TranslateSP1.Feedback.MissingContext.StGrammar_CandsNumber.PLURAL.format(
        tar_language=self.tar_language
      )
    else:
      st_grammar_cands_number = p_llm_templates.TranslateSP1.Feedback.MissingContext.StGrammar_CandsNumber.SINGULAR.format(
        tar_language=self.tar_language
      )

    # tp1_cand_ast_desired
    # TODO HACK come back later
    tp1_cand_ast_desired = _get_tp1_cand_ast_desired()

    # MESSAGE
    feedback_message = HumanMessagePromptTemplate.from_template(
      p_llm_templates.TranslateSP1.Feedback.MissingContext.MAIN
    ).format(
      st_tp1_cand_descs=st_tp1_cand_descs,
      st_grammar_cands_number=st_grammar_cands_number,
      tp1_cand_ast_desired=tp1_cand_ast_desired
    )
    return feedback_message

  def check_common_cases(self) -> Optional[HumanMessage]:
    '''
    Should be the first statement in subclasses' `get_feedback_message` methods
    '''
    self._log('checking common feedback cases')
    self._log(f'the number of generated tp1_cands is {len(self.val.tp1_cands)}')
    self._log(f'here is the stats for them:\n{json.dumps(self.val.tp1_cands_stats, indent=2)}')

    # common case 1: checking for the presence of code blocks
    self._log('common case 1: checking for the presence of code blocks')
    if self.val.has_no_tp1_cands():
      self._log('no tp1_cands found')
      self._log('returning the feedback message')
      feedback_message = self.get_message_no_code_blocks()
      return feedback_message
    self._log('common case 1: tp1_cands found')

    # common case 2: checking if all tp1_cands have parse error
    self._log('common case 2: checking if all tp1_cands have parse error')
    if self.val.all_have_parse_error():
      self._log('all tp1_cands have parse error')
      self._log('returning the feedback message')
      feedback_message = self.get_message_have_parse_error(self.val.tp1_cands)
      return feedback_message
    self._log('common case 2: some/all tp1_cands do not have parse error')

    self._log('finished checking for common cases')


class SP1_DirectTransF(BaseTranslateSP1Factory):
  def get_feedback_message(self) -> HumanMessage:
    common_case_feedback_message = self.check_common_cases()
    if common_case_feedback_message is not None:
      return common_case_feedback_message

    self.log_args(val_dict=self.val.validation_result, subject_name=self.subject.name)
    raise NotImplementedError('new feedback case identified in SP1_DirectTrans')


class SP1_PartialProgramF(BaseTranslateSP1Factory):
  def get_feedback_message(self) -> HumanMessage:
    common_case_feedback_message = self.check_common_cases()
    if common_case_feedback_message is not None:
      return common_case_feedback_message

    # case 1 (parprog): checking if all tp1_cands violate the partial program prefix/suffix
    # that is, LLM put the translation of the `snippet_to_translate_src`
    # into `partial_program` by replacing `pirel_replace_var`
    partial_program = self.template_dict['partial_program']
    prefix, suffix = get_partial_program_affix(partial_program)
    self._log('case 1 (parprog): checking if all tp1_cands violate the partial program prefix/suffix')
    self._log(f'partial_program:\n{repr(partial_program)}\ntp1_cands:\n{json.dumps(self.val.tp1_cands, indent=2)}')
    self._log(f'prefix:\n{repr(prefix)}\nsuffix:\n{repr(suffix)}')
    if self.val.all_violate_partial_program_affix(prefix, suffix):
      self._log(f'all tp1_cands violate the partial program prefix/suffix')
      self._log(f'generating and returning a feedback prompt')
      feedback_prompt = HumanMessagePromptTemplate.from_template(
        p_llm_templates.TranslateAny.Feedback.PARPROG_AFFIX_VIOLATED
      ).format(
        tar_language=self.tar_language,
        partial_program=partial_program,
        variable_to_replace=p_consts.PAR_PROG_PROB_NODE_REPLACE
      )
      return feedback_prompt
    self._log('case 1 (parprog): some/all tp1_cands respect the partial program prefix/suffix')

    # case 2 (parprog): checking if all tp1_cands miss the target context(s)
    self._log('case 2 (parprog): checking if all tp1_cands miss the target context(s)')
    if self.val.all_miss_context():
      self._log('all tp1_cands miss the context(s)')
      self._log('returning the feedback message')

      # TODO this is a temporary solution, and should be addressed later
      npe_tp1_cands = self.val.get_all_no_parse_error()
      self._log('leaving out the tp1_cands with parse error')
      self._log(f'All:\n{json.dumps(self.val.tp1_cands, indent=2)}\nNo parse error:\n{json.dumps(npe_tp1_cands, indent=2)}')

      feedback_message = self.get_message_miss_context(npe_tp1_cands, self.val.sp1)
      return feedback_message
    self._log('case 2 (parprog): some/all tp1_cands contain the target context(s)')

    self.log_args(val_dict=self.val.validation_result, subject_name=self.subject.name)
    raise NotImplementedError('new feedback case identified in SP1_PartialProgram')


# TRANSLATE SP2
class BaseTranslateSP2Factory(BaseMessageFactory):
  def __init__(self, template_dict: dict, subject: p_subject.PirelSubject, val: p_llm_val.TranslateSP2ValidationResult):
    super().__init__(template_dict, subject)
    self.val = val

  def check_common_cases(self) -> Optional[HumanMessage]:
    '''
    Should be the first statement in subclasses' `get_feedback_message` methods
    '''
    self._log('checking common feedback cases')
    self._log(f'the number of generated tp2_cands is {len(self.val.tp2_cands)}')
    self._log(f'here is the stats for them:\n{json.dumps(self.val.tp2_cands_stats, indent=2)}')

    # common case 1: checking for the presence of code blocks
    self._log('common case 1: checking for the presence of code blocks')
    if self.val.has_no_tp2_cands():
      self._log('no tp2_cands found')
      self._log('returning the feedback message')
      feedback_message = self.get_message_no_code_blocks()
      return feedback_message
    self._log('common case 1: tp2_cands found')

    # common case 2: checking if all tp2_cands have parse error
    self._log('common case 2: checking if all tp2_cands have parse error')
    if self.val.all_have_parse_error():
      self._log('all tp2_cands have parse error')
      self._log('returning the feedback message')
      feedback_message = self.get_message_have_parse_error(self.val.tp2_cands)
      return feedback_message
    self._log('common case 2: some/all tp2_cands do not have parse error')

    self._log('finished checking for common cases')


class SP2_DirectTransF(BaseTranslateSP2Factory):
  def get_feedback_message(self) -> HumanMessage:
    common_case_feedback_message = self.check_common_cases()
    if common_case_feedback_message is not None:
      return common_case_feedback_message

    # case 1 (dirtrans): checking if all tp2_cands are not type-isomorphic to tp1_cand
    self._log('case 1 (dirtrans): checking if all tp2_cands are not type-isomorphic to tp1_cand')
    if self.val.all_are_not_type_isomorphic():
      msg = 'BAD: all tp2_cands are not type-isomorphic to tp1_cand. Cannot do anything for now.'
      self._log(msg)
      # TODO could try one more time
      raise FeedbackImpossibleError(msg)
    self._log('case 1 (dirtrans): some/all tp2_cands are type-isomorphic to tp1_cand')

    self.log_args(val_dict=self.val.validation_result, subject_name=self.subject.name)
    raise NotImplementedError('new feedback case identified in SP2_DirectTrans')


class SP2_PartialProgramF(BaseTranslateSP2Factory):
  def get_feedback_message(self) -> HumanMessage:
    common_case_feedback_message = self.check_common_cases()
    if common_case_feedback_message is not None:
      return common_case_feedback_message

    # case 1 (parprog): checking if all tp2_cands violate the partial program prefix/suffix
    # that is, LLM put the translation of the `snippet_to_translate_src`
    # into `partial_program` by replacing `pirel_replace_var`
    partial_program = self.template_dict['partial_program']
    prefix, suffix = get_partial_program_affix(partial_program)
    self._log('case 1 (parprog): checking if all tp2_cands violate the partial program prefix/suffix')
    self._log(f'partial_program:\n{repr(partial_program)}\ntp2_cands:\n{json.dumps(self.val.tp2_cands, indent=2)}')
    self._log(f'prefix:\n{repr(prefix)}\nsuffix:\n{repr(suffix)}')
    if self.val.all_violate_partial_program_affix(prefix, suffix):
      self._log(f'all tp2_cands violate the partial program prefix/suffix')
      self._log(f'generating and returning a feedback prompt')
      feedback_prompt = HumanMessagePromptTemplate.from_template(
        p_llm_templates.TranslateAny.Feedback.PARPROG_AFFIX_VIOLATED
      ).format(
        tar_language=self.tar_language,
        partial_program=partial_program,
        variable_to_replace=p_consts.PAR_PROG_PROB_NODE_REPLACE
      )
      return feedback_prompt
    self._log('case 1 (parprog): some/all tp2_cands respect the partial program prefix/suffix')

    # case 2 (parprog): checking if all tp2_cands are not type-isomorphic to tp1_cand
    self._log('case 2 (parprog): checking if all tp2_cands are not type-isomorphic to tp1_cand')
    if self.val.all_are_not_type_isomorphic():
      msg = 'BAD: all tp2_cands are not type-isomorphic to tp1_cand. Cannot do anything for now.'
      self._log(msg)
      # TODO could try one more time
      raise FeedbackImpossibleError(msg)
    self._log('case 2 (parprog): some/all tp2_cands are type-isomorphic to tp1_cand')

    self.log_args(val_dict=self.val.validation_result, subject_name=self.subject.name)
    raise NotImplementedError('new feedback case identified in SP2_PartialProgram')


# GENERATE TEST FUNCTION
class GenTestFunctionF(BaseMessageFactory):
  def __init__(
    self,
    template_dict: dict,
    subject: p_subject.PirelSubject,
    val: p_llm_val.GenTestFunctionValidationResult
  ):
    super().__init__(template_dict, subject)
    self.val = val

  def get_message_have_parse_error(self, cands_w_error: List[str]) -> HumanMessage:
    cands_str = ''
    for cand_code in cands_w_error:
      cands_str += f'```python\n{cand_code}\n```\n'
    return HumanMessage(f'All generated test functions have parse error. Here are the candidates:\n{cands_str}')

  def get_message_not_a_single_fn_defn_test(self) -> HumanMessage:
    return HumanMessage(
      f'Please make sure that the generated test function is a single function definition named `test()`.'
    )

  def get_feedback_message(self) -> HumanMessage:
    self._log(f'the number of generated test functions is {len(self.val.gen_test_fn_cands)}')
    self._log(f'here is the stats for them:\n{json.dumps(self.val.gen_test_fn_cands_stats, indent=2)}')

    # case 1: checking for the presence of code blocks
    self._log('case 1: checking for the presence of code blocks')
    if self.val.has_no_gen_test_fn_cands():
      self._log('no gen_test_fn_cands found')
      self._log('returning the feedback message')
      feedback_message = self.get_message_no_code_blocks()
      return feedback_message
    self._log('case 1: gen_test_fn_cands found')

    # case 2: checking if all gen_test_fn_cands have parse error
    self._log('case 2: checking if all gen_test_fn_cands have parse error')
    if self.val.all_have_parse_error():
      self._log('all gen_test_fn_cands have parse error')
      self._log('returning the feedback message')
      feedback_message = self.get_message_have_parse_error(self.val.gen_test_fn_cands)
      return feedback_message
    self._log('case 2: some/all gen_test_fn_cands do not have parse error')

    # case 3: checking if all gen_test_fn_cands have a single function defn `test()`
    self._log('case 3: checking if all gen_test_fn_cands have a single function defn `test()`')
    if self.val.not_a_single_fn_def_test():
      self._log('not a single generated test function is a single function defn `test()`')
      self._log('returning the feedback message')
      feedback_message = self.get_message_not_a_single_fn_defn_test()
      return feedback_message

    raise NotImplementedError('new feedback case identified in GenTestFunctionF')


# HELPER FUNCTIONS
def get_partial_program_affix(partial_program: str) -> Tuple[str, str]:
  '''
  function f_gold(pirel_replace_var, ) {
      pirel_dummy_var;
      pirel_dummy_var;
      pirel_dummy_var;
      pirel_dummy_var;
  }

  RETURN strings left to and right to `pirel_replace_var`
  '''
  kw = p_consts.PAR_PROG_PROB_NODE_REPLACE
  assert partial_program.count(kw) == 1, f'sanity check: "{kw}" should appear exactly once in partial program'
  start_idx = partial_program.index(kw)
  end_idx = start_idx + len(kw)

  prefix = partial_program[:start_idx]
  suffix = partial_program[end_idx:]
  return (prefix, suffix)


# TEST HARNESSES
def _test_SP2_PartialProgramF():
  test_harness_config:dict = p_utils.read_json('temporary_test_SP2_PartialProgramF_config.json')
  args_dict = p_utils.read_json(test_harness_config['args_dict_fpath'])
  template_dict = args_dict['template_dict']
  val_dict = args_dict['val_dict']

  val_obj = p_llm_val.TranslateSP2ValidationResult(val_dict)
  sp2_parprog_factory = SP2_PartialProgramF(template_dict, val_obj)
  fm = sp2_parprog_factory.get_feedback_message()
  fm.pretty_print()


if __name__ == '__main__':
  _test_SP2_PartialProgramF()
