'''
This module is an attempt to generate translation rules statefully.

Class diagram
                                        BasePirelTask
                                        │     │    │
                                        │     │    │
                                        │     │    │
                                        │     │    │
                                        │     │    │
                                        │     │    │
                  ◄─────────────────────┘     ▼    └──────────────────────►
        SimplifyTemplateG              BaseTranslateSP1Task         BaseTranslateSP2Task
                                          │  │                            │     │
                                          │  │                            │     │
                                          │  │                            │     │
                                          │  │                            │     │
                                          │  │                            │     │
                                          │  │                            │     │
               ◄──────────────────────────┘  ▼                            ▼     └──────────────►
      SP1_DirectTransG            SP1_PartialProgramG            SP2_DirectTransG        SP2_PartialProgramG
'''


import copy
import json
import re
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union

import d_ast_parse
import p_consts
import p_data_structures as pds
import p_generator
import p_llm_messages
import p_llm_templates
import p_llm_val
import p_subject
import p_utils
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.base import BaseMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.system import SystemMessage
from langchain_core.prompts.chat import (HumanMessagePromptTemplate,
                                         SystemMessagePromptTemplate)
from langchain_openai import ChatOpenAI


logger = p_utils.setup_logger(__name__)


# ERROR CLASSES
class TemplateSimplificationRetryLimitError(RuntimeError): pass
class SP1TranslationRetryLimitError(RuntimeError): pass
class SP2TranslationRetryLimitError(RuntimeError): pass
class NoTransPairsFromTSPError(RuntimeError): pass
class LLMResponseFormatError(RuntimeError): pass


class BasePirelTask(ABC):
  '''
  Base class for PiREL LLM tasks.

  NOTE on `chat_history`:
  Starting messages
  - system message
  - few shot messages
  - starting prompt message
  Starting response
  - starting response
  Iteration 1
  - feedback 1
  - response 1
  ...
  Iteration N
  - feedback N
  - response N

  NOTE subclasses must have a corresponding adapter `BaseValidationResult` class.
  '''

  # error class for internal use
  class _TaskIterationFinishedError(RuntimeError): pass

  def __init__(self, task_name: str, subject: p_subject.PirelSubject, template_dict: dict):
    self.task_name : str = task_name
    self.chat_history : List[BaseMessage] = []
    self.code_blocks_history : List[List[str]] = []
    self.feedback_iteration_counter = 1
    self.task_iteration_counter = 1
    self.template_dict = template_dict
    self.subject = subject
    self.model_params = {}
    self._log(f'creating an in instance of "{task_name}"')

  def __repr__(self) -> str:
    return self.__class__.__name__

  # TASK LOOP
  def run(self) -> Any:
    '''
    Entry point. Not intended to be overridden.
    '''
    assert self.task_iteration_counter == 1, 'state error: task iteration counter'

    self._log('BasePirelTask.run: initializing the task')
    self.run_init()

    self._log('BasePirelTask.run: starting the task loop')
    while self.does_require_task_iteration():

      try:
        self._log(f'BasePirelTask.run: task loop (iteration #{self.task_iteration_counter})')
        data = self._run_task_once()

        self._log(f'BasePirelTask.run: SUCCESS task run successful. Ending.')
        return data

      except BasePirelTask._TaskIterationFinishedError:
        self._log(f'BasePirelTask.run: WARNING task run failed. Trying one more time.')
        self.task_iteration_counter += 1
      except p_llm_messages.FeedbackImpossibleError as err:
        self._log(f'BasePirelTask.run: WARNING task run failed due to "{str(err)}"')
        self._log('Trying one more time.')
        self.task_iteration_counter += 1

    self._log('BasePirelTask.run: FAIL task failed. Ending.')
    self.run_failed()

  def run_init(self) -> None:
    '''Invoked before starting the task. Can be overridden by subclasses'''

  def run_failed(self) -> None:
    '''Invoken when the task fails. Can be overridden by subclasses'''

  # TASK ITERATION
  def _run_task_once(self) -> Any:
    '''
    A single iteration of a task.
    RETURN refer to `BaseValidationResult` and its subclasses.

    NOTE prompts always ask for code blocks, thus we extract code blocks from raw response
    '''

    self._log(f'_run_task_once: initializing task iteration #{self.task_iteration_counter}')
    self.run_task_once_init()

    # reset state
    self._log('_run_task_once: resetting the state')
    self.chat_history.clear()
    self.code_blocks_history.clear()
    self.feedback_iteration_counter = 1

    # starting prompt and response
    self._log(f'_run_task_once: starting prompt and response')
    starting_messages = self._create_starting_messages()
    self.chat_history.extend(starting_messages)
    starting_raw_response = self._query_llm()
    self.chat_history.append(AIMessage(starting_raw_response))
    starting_code_blocks = self._extract_code_blocks(starting_raw_response)
    self.code_blocks_history.append(starting_code_blocks)

    # validate starting code blocks
    validation_result = self._validate_code_blocks()
    if validation_result.is_successful():
      self._log('_run_task_once: SUCCESS validation is successful. Returning the validation result')
      return validation_result.get_data()

    # FEEDBACK LOOP
    self._log('_run_task_once: First prompt and response are not valid. Starting the feedback loop')
    while self.does_require_feedback_iteration():

      self._log(f'_run_task_once: feedback loop (run #{self.task_iteration_counter}) (iteration #{self.feedback_iteration_counter})')
      self.run_task_once_feedback_init()

      # feedback prompt and response
      self._log('_run_task_once: generating a feedback message')
      feedback_message = self.get_feedback_message(validation_result)
      self.chat_history.append(feedback_message)
      feedback_raw_response = self._query_llm()
      self.chat_history.append(AIMessage(feedback_raw_response))
      feedback_code_blocks = self._extract_code_blocks(feedback_raw_response)
      self.code_blocks_history.append(feedback_code_blocks)

      # validate code blocks
      validation_result = self._validate_code_blocks()
      if validation_result.is_successful():
        self._log('_run_task_once: SUCCESS validation is successful. Returning the validation result')
        return validation_result.get_data()

      self._log('_run_task_once: WARNING feedback loop unsuccessful. trying one more time.')
      self.feedback_iteration_counter += 1
      self.run_task_once_feedback_failed()

    self._log(f'_run_task_once: FAIL task iteration failure #{self.task_iteration_counter}')
    raise BasePirelTask._TaskIterationFinishedError

  def run_task_once_init(self) -> None:
    '''Invoked before starting the task iteration. Can be overridden by subclasses'''

  def run_task_once_feedback_init(self) -> None:
    '''Invoked before starting feedback iteration. Can be overridden by subclasses'''

  def run_task_once_feedback_failed(self) -> None:
    '''Invoked at the end of feedback iteration. Can be overridden by subclasses'''

  # METHODS FOR INTERNAL USE
  def _create_starting_messages(self) -> List[BaseMessage]:
    '''Create a list of starting messages for initial query of a task'''
    self._log('creating starting messages')
    starting_messages = []
    starting_messages.append(self.get_system_message())
    starting_messages.extend(self.get_few_shot_messages())
    starting_messages.append(self.get_starting_prompt_message())
    return starting_messages

  def _query_llm(self) -> str:
    assert self.chat_history[-1].type == 'human', 'chat history must end with a human prompt'
    self._log_file(langchain_msgs_to_md(self.chat_history), f'llm-messages.md')
    raw_response = query_llm(self.chat_history, **self.model_params)
    self._log_file(raw_response, f'llm-raw-response.md')
    return raw_response

  def _extract_code_blocks(self, raw_response: str) -> List[str]:
    code_blocks = extract_code_blocks(raw_response)
    self._log_json(code_blocks, f'gen-code-blocks.json')
    logger.debug(f'generated code blocks:\n{json.dumps(code_blocks, indent=2)}')
    logger.debug(f'partial program:\n  {repr(self.template_dict["partial_program"])}')
    return code_blocks

  def _validate_code_blocks(self) -> p_llm_val.BaseValidationResult:
    self._log('validating the generated code blocks by p_llm_val module')
    validation_result = self.validate_code_blocks()
    self._log_json(validation_result.get_val_result(), f'val-result.json')
    return validation_result

  def _log_json(self, data: Union[list, dict], fname: str) -> None:
    p_utils.log_json_time(f'{self.subject.name}_{self.task_name}_{fname}', data)

  def _log_file(self, text: str, fname: str) -> None:
    p_utils.log_file_time(f'{self.subject.name}_{self.task_name}_{fname}', text)

  def _log(self, msg: str) -> None:
    logger.debug(f'{self.task_name}: {msg}')

  # HELPER METHODS
  def get_all_gen_code_blocks(self) -> List[str]:
    '''Return all previously generated code blocks'''
    all_code_blocks = []
    for code_blocks_history_elem in self.code_blocks_history:
      all_code_blocks.extend(code_blocks_history_elem)
    return all_code_blocks

  def log_args_as_json(self, fname: str, **kwargs) -> None:
    self._log_json(kwargs, fname)

  # ABSTRACT METHODS
  @abstractmethod
  def get_system_message(self) -> BaseMessage:
    '''Return system message for a task'''

  @abstractmethod
  def get_few_shot_messages(self) -> List[BaseMessage]:
    '''Return few shot messages (golden conversation) for a task'''

  @abstractmethod
  def get_starting_prompt_message(self) -> HumanMessage:
    '''Return the first prompt to start the chat'''

  @abstractmethod
  def get_feedback_message(self, validation_result: p_llm_val.BaseValidationResult) -> HumanMessage:
    '''
    Return a feedback message based on the generated code blocks and validation result.
    This method is generally invoked only when the previous response (or all previous responses) is not valid.
    '''

  @abstractmethod
  def validate_code_blocks(self) -> p_llm_val.BaseValidationResult:
    '''Validation is currently performed with `p_llm_val` module'''

  @abstractmethod
  def does_require_feedback_iteration(self) -> bool:
    '''Return True if need to run one more feedback-response iteration'''

  @abstractmethod
  def does_require_task_iteration(self) -> bool:
    '''Return True if need to run one more task iteration'''


# SIMPLIFY TEMPLATE
class SimplifyTemplateG(BasePirelTask):
  def __init__(self, task_name, template_dict):
    super().__init__(task_name, template_dict)
    self.temperature = 1.0

  def run_task_once_feedback_failed(self) -> None:
    self._log('increasing the model temperature')
    llm_temp = self.temperature + p_consts.GENERATION_TEMPERATURE_INCREMENT
    self.temperature = round(llm_temp, p_consts.GENERATION_TEMPERATURE_ROUND_DIGITS)
    self.model_params['temperature'] = self.temperature

  def get_system_message(self) -> BaseMessage:
    src_language = p_consts.LANG_DICT[self.template_dict['src_lang']]
    system_message = SystemMessagePromptTemplate.from_template(
      p_llm_templates.SimplifyTemplate.System.FILLIN_GENERIC
    ).format(
      language=src_language
    )
    return system_message

  def get_few_shot_messages(self) -> List[BaseMessage]:
    return []

  def get_starting_prompt_message(self) -> HumanMessage:
    src_language = p_consts.LANG_DICT[self.template_dict['src_lang']]
    template = self.template_dict['template_context_simplification']
    num_variants = p_consts.GENERATION_NUM_VARIANTS_IN_RESPONSE
    starting_prompt = HumanMessagePromptTemplate.from_template(
      p_llm_templates.SimplifyTemplate.Prompt.FILLIN_GENERIC
    ).format(
      language=src_language,
      template=template,
      num_variants=num_variants
    )
    return starting_prompt

  def get_feedback_message(self, validation_result: p_llm_val.SimplifyTemplateValidationResult) -> HumanMessage:
    self._log('initiating a feedback message factory')
    factory = p_llm_messages.SimplifyTemplateF(self.template_dict, self.subject, validation_result)
    feedback_message = factory.get_feedback_message()
    return feedback_message

  def validate_code_blocks(self) -> p_llm_val.SimplifyTemplateValidationResult:
    self._log('starting simplified template candidates validation')
    all_st_cands = self.get_all_gen_code_blocks()
    val_results_obj = p_llm_val.val_simplified_template_candidates(all_st_cands, self.template_dict, subject_name=self.subject.name)
    return val_results_obj

  def does_require_feedback_iteration(self) -> bool:
    return self.feedback_iteration_counter <= p_consts.TEMPLATE_SIMPLIFICATION_MAX_FEEDBACKS

  def does_require_task_iteration(self) -> bool:
    return self.task_iteration_counter <= p_consts.TEMPLATE_SIMPLIFICATION_MAX_RETRIES

  def run_failed(self) -> None:
    msg = f'Could not simplify the template. Reached retry limit. Check the logs.'
    self._log(f'ERROR {msg}')
    raise TemplateSimplificationRetryLimitError(msg)


# TRANSLATE SP1
class BaseTranslateSP1Task(BasePirelTask):
  '''
  Simple algorithm for translating SP1.
  `self.run` returns list of program pairs.
  '''

  def __init__(self, task_name: str, subject: p_subject.PirelSubject, template_dict: dict, sp1: str):
    super().__init__(task_name, subject, template_dict)
    self.sp1 = sp1
    self.log_args_as_json(
      'args_init.json', task_name=task_name, template_dict=template_dict, sp1=sp1
    )

  def get_system_message(self) -> BaseMessage:
    system_message = SystemMessagePromptTemplate.from_template(
      p_llm_templates.TranslateSP1.System.DIRECT_TRANS_2
    ).format(
      src_language = p_consts.LANG_DICT[self.template_dict['src_lang']],
      tar_language = p_consts.LANG_DICT[self.template_dict['tar_lang']],
    )
    return system_message

  def get_few_shot_messages(self) -> List[BaseMessage]:
    return []

  def get_starting_prompt_message(self) -> HumanMessage:
    starting_prompt = HumanMessagePromptTemplate.from_template(
      p_llm_templates.TranslateAny.Prompt.DIRECT_TRANS_WITH_REFERENCE
    ).format(
      src_language = p_consts.LANG_DICT[self.template_dict['src_lang']],
      tar_language = p_consts.LANG_DICT[self.template_dict['tar_lang']],
      program_to_translate = self.sp1,
      template_origin = self.template_dict['template_origin'],
      src_program = self.template_dict['src_program']
    )
    return starting_prompt

  def validate_code_blocks(self) -> p_llm_val.TranslateSP1ValidationResult:
    self._log('starting tp1 candidates validation')
    all_tp1_cands = self.get_all_gen_code_blocks()
    val_result_obj = p_llm_val.val_tp1_candidates(all_tp1_cands, self.sp1, self.template_dict, subject_name=self.subject.name)
    return val_result_obj

  def does_require_feedback_iteration(self) -> bool:
    return self.feedback_iteration_counter <= p_consts.TRANSLATION_SP1_MAX_FEEDBACKS

  def does_require_task_iteration(self) -> bool:
    return self.task_iteration_counter <= p_consts.TRANSLATION_SP1_MAX_RETRIES

  def run_failed(self) -> None:
    msg = f'Could not translate SP1. Reached retry limit. Check the logs.'
    self._log(f'ERROR {msg}')
    raise SP1TranslationRetryLimitError(msg)

  @classmethod
  def dispatch(self, subject: p_subject.PirelSubject, template_dict: dict, sp1: str) -> 'BaseTranslateSP1Task':
    '''
    Based on the values of the arguments provided, choose the right translator subclass
    '''
    logger.debug('~~~ BaseTranslateSP1Task.dispatch: starting')
    logger.debug(f'BaseTranslateSP1Task.dispatch: Translating SP1:\n{repr(sp1)}')

    if _is_context_empty(template_dict):
      logger.debug('BaseTranslateSP1Task.dispatch: Context is empty. Will use direct translation of SP1.')
      task_obj = SP1_DirectTransG('tr_sp1_dir_tr', subject, template_dict, sp1)

    else:
      logger.debug('BaseTranslateSP1Task.dispatch: Context is not empty. Will use partial translation of SP1.')
      task_obj = SP1_PartialProgramG('tr_sp1_par_pr', subject, template_dict, sp1)

    logger.debug(f'BaseTranslateSP1Task.dispatch: returning task object "{repr(task_obj)}"')
    return task_obj


class SP1_DirectTransG(BaseTranslateSP1Task):
  '''
  Ask for translation directly.
  '''
  def get_system_message(self) -> BaseMessage:
    src_language = p_consts.LANG_DICT[self.template_dict['src_lang']]
    tar_language = p_consts.LANG_DICT[self.template_dict['tar_lang']]
    system_message = SystemMessagePromptTemplate.from_template(
      p_llm_templates.TranslateSP1.System.DIRECT_TRANS
    ).format(
      src_language=src_language,
      tar_language=tar_language,
    )
    return system_message

  def get_feedback_message(self, validation_result: p_llm_val.TranslateSP1ValidationResult) -> HumanMessage:
    self._log('initiating a feedback message factory')
    factory = p_llm_messages.SP1_DirectTransF(self.template_dict, self.subject, validation_result)
    feedback_message = factory.get_feedback_message()
    return feedback_message


class SP1_PartialProgramG(BaseTranslateSP1Task):
  '''
  Translate a portion of a larger program.
  '''
  def get_starting_prompt_message(self) -> HumanMessage:
    src_lang = self.template_dict['src_lang']
    tar_lang = self.template_dict['tar_lang']
    problematic_node_path = self.template_dict['problematic_node_path']
    partial_program = self.template_dict['partial_program']

    src_snippet_to_translate = _extract_snippet(self.sp1, src_lang, problematic_node_path)

    starting_prompt = HumanMessagePromptTemplate.from_template(
      p_llm_templates.TranslateSP1.Prompt.PARTIAL_PROGRAM
    ).format(
      src_language = p_consts.LANG_DICT[src_lang],
      src_snippet_to_translate = src_snippet_to_translate,
      src_snippet_context = self.sp1,
      tar_language = p_consts.LANG_DICT[tar_lang],
      tar_partial_program = partial_program,
      variable_to_replace = p_consts.PAR_PROG_PROB_NODE_REPLACE
    )
    return starting_prompt

  def get_feedback_message(self, validation_result: p_llm_val.TranslateSP1ValidationResult) -> HumanMessage:
    self._log('initiating a feedback message factory')
    factory = p_llm_messages.SP1_PartialProgramF(self.template_dict, self.subject, validation_result)
    feedback_message = factory.get_feedback_message()
    return feedback_message


# TRANSLATE SP2
class BaseTranslateSP2Task(BasePirelTask):
  '''
  Simple algorithm for translating SP2.
  `self.run` returns list of program pairs.
  '''

  def __init__(self, task_name: str, subject: p_subject.PirelSubject, template_dict: dict, sp1_tp1_cand: dict, sp2: str):
    '''
    PARAM sp1_tp1_cand: (sp1_i, tp1_i_j)
    '''
    super().__init__(task_name, subject, template_dict)
    self.sp1 = sp1_tp1_cand['source']
    self.tp1_cand = sp1_tp1_cand['target']
    self.sp2 = sp2
    self.log_args_as_json(
      'args_init.json', task_name=task_name, template_dict=template_dict,
      sp1_tp1_cand=sp1_tp1_cand, sp2=sp2
    )

  def get_system_message(self) -> BaseMessage:
    return SystemMessage(p_llm_templates.TranslateAny.System.GENERIC)

  def get_few_shot_messages(self) -> List[BaseMessage]:
    return []

  def get_starting_prompt_message(self) -> HumanMessage:
    starting_prompt = HumanMessagePromptTemplate.from_template(
      p_llm_templates.TranslateAny.Prompt.DIRECT_TRANS
    ).format(
      src_language = p_consts.LANG_DICT[self.template_dict['src_lang']],
      tar_language = p_consts.LANG_DICT[self.template_dict['tar_lang']],
      program_to_translate = self.sp2
    )
    return starting_prompt

  def validate_code_blocks(self) -> p_llm_val.TranslateSP2ValidationResult:
    self._log('starting tp2 candidates validation')
    all_tp2_cands = self.get_all_gen_code_blocks()
    val_result_obj = p_llm_val.val_tp2_candidates(all_tp2_cands, self.sp1, self.sp2, self.tp1_cand, self.template_dict, subject_name=self.subject.name)
    return val_result_obj

  def does_require_feedback_iteration(self) -> bool:
    return self.feedback_iteration_counter <= p_consts.TRANSLATION_SP2_MAX_FEEDBACKS

  def does_require_task_iteration(self) -> bool:
    return self.task_iteration_counter <= p_consts.TRANSLATION_SP2_MAX_RETRIES

  def run_failed(self) -> None:
    msg = f'Could not translate SP2. Reached retry limit. Check the logs.'
    self._log(f'ERROR {msg}')
    raise SP2TranslationRetryLimitError(msg)

  @classmethod
  def dispatch(self, subject: p_subject.PirelSubject, template_dict: dict, sp1_tp1_cand: dict, sp2: str) -> 'BaseTranslateSP1Task':
    '''
    Based on the values of the arguments provided, choose the right subclass (translator)
    '''
    logger.debug('~~~ BaseTranslateSP2Task.dispatch: starting')
    logger.debug(f'BaseTranslateSP2Task.dispatch: Translating SP2:\n{repr(sp2)}')
    logger.debug(f'BaseTranslateSP2Task.dispatch: SP1-TP1-cand:\n{json.dumps(sp1_tp1_cand, indent=2)}')

    if _is_context_empty(template_dict):
      logger.debug('BaseTranslateSP2Task.dispatch: Context is empty. Will use direct translation of SP2 (similar to SP1).')
      task_obj = SP2_DirectTransG('tr_sp2_dir_tr', subject, template_dict, sp1_tp1_cand, sp2)

    else:
      logger.debug('BaseTranslateSP2Task.dispatch: Context is not empty. Will use partial translation of SP2 (similar to SP1).')
      task_obj = SP2_PartialProgramG('tr_sp2_par_pr', subject, template_dict, sp1_tp1_cand, sp2)

    logger.debug(f'BaseTranslateSP2Task.dispatch: returning task object "{repr(task_obj)}"')
    return task_obj


class SP2_DirectTransG(BaseTranslateSP2Task):
  '''
  Ask for translation directly, but provide a reference translation (sp1 -> tp1_cand)
  '''
  def get_starting_prompt_message(self) -> HumanMessage:
    src_lang = self.template_dict['src_lang']
    tar_lang = self.template_dict['tar_lang']

    starting_prompt = HumanMessagePromptTemplate.from_template(
      p_llm_templates.TranslateSP2.Prompt.DIRECT_TRANS_SIMILAR
    ).format(
      src_language=p_consts.LANG_DICT[src_lang],
      sp1=self.sp1,
      tar_language=p_consts.LANG_DICT[tar_lang],
      tp1_cand=self.tp1_cand,
      sp2=self.sp2
    )
    return starting_prompt

  def get_feedback_message(self, validation_result: p_llm_val.TranslateSP2ValidationResult) -> HumanMessage:
    self._log('initiating a feedback message factory')
    factory = p_llm_messages.SP2_DirectTransF(self.template_dict, self.subject, validation_result)
    feedback_message = factory.get_feedback_message()
    return feedback_message


class SP2_PartialProgramG(BaseTranslateSP2Task):
  '''
  Ask for translation of a portion of a larger program, provide a reference translation (sp1 -> tp1_cand)
  '''
  def get_starting_prompt_message(self) -> HumanMessage:
    src_lang = self.template_dict['src_lang']
    tar_lang = self.template_dict['tar_lang']
    problematic_node_path = self.template_dict['problematic_node_path']
    partial_program = self.template_dict['partial_program']

    src_snippet_to_translate = _extract_snippet(self.sp2, src_lang, problematic_node_path)

    starting_prompt = HumanMessagePromptTemplate.from_template(
      p_llm_templates.TranslateSP2.Prompt.PARTIAL_PROGRAM_SIMILAR
    ).format(
      src_language=p_consts.LANG_DICT[src_lang],
      snippet_to_translate_sp2=src_snippet_to_translate,
      snippet_context_sp2=self.sp2,
      tar_language=p_consts.LANG_DICT[tar_lang],
      partial_program=partial_program,
      variable_to_replace=p_consts.PAR_PROG_PROB_NODE_REPLACE,
      tp1_cand=self.tp1_cand,
      sp1=self.sp1,
    )
    return starting_prompt

  def get_feedback_message(self, validation_result: p_llm_val.TranslateSP2ValidationResult) -> HumanMessage:
    self._log('initiating a feedback message factory')
    factory = p_llm_messages.SP2_PartialProgramF(self.template_dict, self.subject, validation_result)
    feedback_message = factory.get_feedback_message()
    return feedback_message


# HELPER FUNCTIONS
def get_openai_credentials() -> Tuple[str, str]:
  assert p_consts.ENV_FILE.exists(), f'Create a "{p_consts.ENV_FILE.name}" file with necessary environment variables'
  env_dict = p_utils.read_json(p_consts.ENV_FILE)
  try:
    openai_api_key = env_dict['OPENAI_API_KEY']
    openai_organization = env_dict['OPENAI_ORGANIZATION']
    return openai_api_key, openai_organization
  except KeyError as err:
    msg = f'An environment variable "{err}" must be set.'
    logger.critical(msg)
    raise RuntimeError(msg) from err


def query_llm(messages: List[BaseMessage], **kwargs) -> str:
  api_key, org_id = get_openai_credentials()

  model_params = copy.deepcopy(p_consts.DEFAULT_MODEL_PARAMS)
  # overwrite the default model params, if `model_params` is provided
  if 'model_params' in kwargs:
    for param, val in kwargs['model_params'].items():
      model_params[param] = val

  logger.info(f'Making a query to LLM')
  logger.debug(f'Model parameters:\n{json.dumps(model_params, indent=2)}')

  chatgpt = ChatOpenAI(openai_api_key=api_key, openai_organization=org_id, **model_params)
  chat_result = chatgpt.invoke(messages)

  return chat_result.content


def extract_code_blocks(raw_response: str) -> List[str]:

  def _pre_process_raw_response(raw_response: str) -> str:
    lines = [line for line in raw_response.split('\n')]
    # 1. strip trailing whitespace characters at each line
    lines = [line.rstrip() for line in lines]
    # 2. strip leading whitespace characters at lines beginning with ```
    lines = [line.lstrip() if line.lstrip().startswith('```') else line for line in lines]
    return '\n'.join(lines)

  raw_response = _pre_process_raw_response(raw_response)
  code_block_re = re.compile(r'^```(\w+)?\n(.*?)```$', re.DOTALL | re.MULTILINE)
  matches = re.finditer(code_block_re, raw_response)
  code_blocks = [m.group(2).strip() for m in matches]
  logger.debug(f'Extracted {len(code_blocks)} code blocks from raw LLM response')
  return code_blocks


def langchain_msgs_to_md(messages: List[BaseMessage]) -> str:
  result_md = ''
  for msg in messages:
    result_md += f'# {msg.type}\n\n{msg.content}\n\n\n'
  return result_md.strip()


def _extract_snippet(program: str, lang: str, node_path: List[int]) -> str:
  '''
  Extract a snippet from `program` under `node_path`
  PARAM node_path: path to node of interest relative to the one and only child (context) under the root node
  '''
  program_ast_text, _ = d_ast_parse.parse_text_dbg(program, lang, keep_text=True)
  program_tree = pds.PirelTree(program_ast_text)

  root_node_children = program_tree.get_root_node().get_children()
  assert len(root_node_children) > 0, 'sanity check'
  if len(root_node_children) > 1:
    logger.warning(f'_extract_snippet: requested program\'s root node has multiple children (should be one)\n:{program}')

  context_node = root_node_children[0]
  problematic_node = context_node.get_child_by_path(node_path)
  snippet = problematic_node.get_text().strip()
  return snippet


def _is_context_empty(template_dict: dict) -> bool:
  ''''''
  # TODO template_dict['contexts'] is a list of contexts. Which one to consider?
  context = template_dict['contexts'][0]

  source_context = context['source_context']
  target_context = context['target_context']

  # source or parent context have a parent -> have context
  if len(source_context) > 1 or len(target_context) > 1:
    assert len(source_context) > 1, 'sanity check'
    assert len(target_context) > 1, 'sanity check'
    return False

  source_node_and_siblings = source_context[0]
  target_node_and_siblings = target_context[0]

  # source or parent context have a sibling -> have context
  if len(source_node_and_siblings) > 1 or len(target_node_and_siblings) > 1:
    assert len(source_node_and_siblings) > 1, 'sanity check'
    assert len(source_node_and_siblings) > 1, 'sanity check'
    return False

  assert source_node_and_siblings[0].split('.')[1] == template_dict['problematic_node_type'], 'sanity check'
  assert target_node_and_siblings[0] == 'unknown', 'sanity check'

  return True


# API
def simplify_template(template_dict: dict) -> dict:
  '''
  Simplify template and return it.
  NOTE writes to `template_dict`
  RETURN updated `template_dict`
  '''
  logger.info(f'~~~ Starting API call to p_llm_gen.simplify_template')

  # this is a necessary step to prepare a template for program simplification
  template_dict = p_generator.simplify_template_init(template_dict)

  # check if we need simplification step
  if len(template_dict['templatized_node_ids_context']) == 0:
    logger.debug('GOOD: We do not need template simplification')
    template_dict['template'] = template_dict['template_context_str_replace']
    template_dict['template_origin'] = template_dict['template_context_str_replace']
    return template_dict

  simplify_template = SimplifyTemplateG('simpl_templ', template_dict)
  simplification_dict = simplify_template.run()

  simplified_template = simplification_dict['simplified_template']
  simplified_template_origin = simplification_dict['simplified_template_origin']

  template_dict['template_origin_before_simplification'] = template_dict['template_origin']
  template_dict['template'] = simplified_template
  template_dict['template_origin'] = simplified_template_origin

  return template_dict


def get_translation_pairs_from_tsp(subject: p_subject.PirelSubject, tsp: Tuple[str, str], template_dict: dict) -> List[Tuple[dict, dict]]:
  '''
  RETURN non-empty list of all possible translation pairs obtained from a given `tsp`.
  NOTE raised errors propagate to the caller.
  '''
  logger.info(f'~~~ Starting API call to p_llm_gen.get_translation_pairs_from_tsp')
  logger.debug(f'Attempting to translate SP1 and SP2 to generate a translation pair:\n{json.dumps(tsp, indent=2)}')

  def _check_sp1_sp2_identical(sp1_tp1_cands: List[Dict[str, str]], sp2: str) -> Optional[List[Tuple[Dict[str, str], Dict[str, str]]]]:
    assert len(sp1_tp1_cands) > 0, 'sanity check'
    sp1 = sp1_tp1_cands[0]['source']
    assert all(map(lambda sp1_tp1_cand: sp1_tp1_cand['source'] == sp1, sp1_tp1_cands)), 'sanity check'
    if sp1 != sp2:
      return None
    logger.debug(f'SP1 and SP2 are identical. Just using the translation of SP1.')
    translation_pairs = []
    for sp1_tp1_cand in sp1_tp1_cands:
      sp1, tp1 = sp1_tp1_cand['source'], sp1_tp1_cand['target']
      translation_pairs.append(({'source': sp1, 'target': tp1}, {'source': sp2, 'target': tp1}))
    return translation_pairs

  sp1, sp2 = tsp

  # translate `sp1` to produce sp1_tp1_cands (a.k.a. program pairs)
  trans_sp1 = BaseTranslateSP1Task.dispatch(subject, template_dict, sp1)

  try:
    sp1_tp1_cands = trans_sp1.run()
  except SP1TranslationRetryLimitError as err:
    logger.warning(f'BAD: Reached a retry limit for SP1 translation:\n{str(err)}')
    raise NoTransPairsFromTSPError from err

  logger.debug(f'Generated {len(sp1_tp1_cands)} candidate translations for SP1:\n{json.dumps(sp1_tp1_cands, indent=2)}')

  # for each `sp1_tp1_cand` generate all possible `translation_pair` candidates
  all_translation_pairs = []
  for cand_idx, sp1_tp1_cand in enumerate(sp1_tp1_cands, start=1):
    logger.debug(f'Translating SP2 (SP1-TP1 cand {cand_idx}/{len(sp1_tp1_cands)})')

    # check if SP1 and SP2 are identical
    translation_pairs = _check_sp1_sp2_identical(sp1_tp1_cands, sp2)
    if translation_pairs is not None:
      all_translation_pairs.extend(translation_pairs)
      continue

    trans_sp2 = BaseTranslateSP2Task.dispatch(subject, template_dict, sp1_tp1_cand, sp2)

    try:
      translation_pair_cands = trans_sp2.run()
    except SP2TranslationRetryLimitError as err:
      logger.warning(f'BAD: Reached a retry limit for SP2 translation:\n{str(err)}')
      logger.debug(f'Will try with the next TP1 cands ({len(sp1_tp1_cands)-cand_idx} left)')
      continue

    all_translation_pairs.extend(translation_pair_cands)
    logger.debug(f'Generated {len(translation_pair_cands)} new translation pairs from (SP1-TP1 cand {cand_idx}/{len(sp1_tp1_cands)})')
    logger.debug(f'The number of all translation pairs so far is {len(all_translation_pairs)}')
    logger.debug(f'New translation pairs:\n{json.dumps(translation_pair_cands, indent=2)}')

  logger.debug(f'~~~ Finishing API call to p_llm_gen.get_translation_pairs_from_tsp')
  logger.debug(f'The number of all translation pairs is {len(all_translation_pairs)}:\n{json.dumps(all_translation_pairs, indent=2)}')

  if len(all_translation_pairs) == 0:
    msg = f'BAD: Could not generate any translation pairs from a program pair:\n{json.dumps(sp1_tp1_cands, indent=2)}'
    logger.warning(msg)
    raise NoTransPairsFromTSPError(msg)

  return all_translation_pairs


def is_tsp_syntactically_correct(tsp: Tuple[str, str], subject: p_subject.PirelSubject, template_dict: dict) -> bool:
  '''
  Check if a given `tsp` is syntactically correct using LLM.

  NOTE not using `BasePirelTask` because this is a simple check
  RAISE LLMResponseFormatError if LLM response is not in the expected format
  '''
  def _get_system_message(template_dict: dict) -> SystemMessage:
    src_language = p_consts.LANG_DICT[template_dict['src_lang']]
    system_message = SystemMessagePromptTemplate.from_template(
      p_llm_templates.CheckTSP.System.GENERIC
    ).format(
      src_language=src_language
    )
    return system_message

  def _get_prompt_message(tsp: Tuple[str, str], template_dict: dict) -> HumanMessage:
    sp1, sp2 = tsp
    src_lang = template_dict['src_lang']
    src_language = p_consts.LANG_DICT[src_lang]
    prompt_message = HumanMessagePromptTemplate.from_template(
      p_llm_templates.CheckTSP.Prompt.GENERIC
    ).format(
      src_language=src_language,
      src_lang=src_lang,
      sp1=sp1,
      sp2=sp2
    )
    return prompt_message

  def _get_messages(tsp: Tuple[str, str], template_dict: dict) -> List[BaseMessage]:
    return [_get_system_message(template_dict), _get_prompt_message(tsp, template_dict)]

  logger.debug(f'~~~ Starting API call to p_llm_gen.is_tsp_syntactically_correct')

  messages = _get_messages(tsp, template_dict)
  p_utils.log_file_time(f'{subject.name}_check_tsp_messages.md', langchain_msgs_to_md(messages))

  raw_response = query_llm(messages)
  p_utils.log_file_time(f'{subject.name}_check_tsp_raw_response.md', raw_response)

  code_blocks = extract_code_blocks(raw_response)
  p_utils.log_json_time(f'{subject.name}_check_tsp_code_blocks.json', code_blocks)

  if len(code_blocks) == 0:
    raise LLMResponseFormatError('No code blocks were generated')

  if len(code_blocks) > 1:
    raise LLMResponseFormatError('Multiple code blocks were generated')

  llm_resp_obj = json.loads(code_blocks[0])
  if 'snippet1' not in llm_resp_obj or 'snippet2' not in llm_resp_obj:
    raise LLMResponseFormatError('LLM response does not contain "snippet1" and "snippet2" keys')

  sp1_verdict = llm_resp_obj['snippet1']
  sp2_verdict = llm_resp_obj['snippet2']

  if sp1_verdict not in ['correct', 'incorrect']:
    raise LLMResponseFormatError('LLM response value for "snippet1" is not "correct" or "incorrect"')
  if sp2_verdict not in ['correct', 'incorrect']:
    raise LLMResponseFormatError('LLM response value for "snippet2" is not "correct" or "incorrect"')

  logger.debug(f'TSP: {json.dumps(tsp, indent=2)}')
  logger.debug(f'LLM response:\n{json.dumps(llm_resp_obj, indent=2)}')

  # both must be `correct` to be considered correct
  is_correct = sp1_verdict == 'correct' and sp2_verdict == 'correct'
  return is_correct


# TEST HARNESSES
def _test_translate_sp1():
  template_dict = p_utils.read_json('/code/repo-duoglot/backend/duoglotcore-server/pirel-logs/debug-11-broken-split/L0009/11-12-09-24-06.754595-L0009_SIMPLIFIED-TEMPLATE-p_llm_gen.json')
  sp1 = 'if id_puox:\n    secret_fun_4071()'
  trans_sp1 = BaseTranslateSP1Task('translate-sp1-basic', template_dict, sp1)
  j_program_pairs = trans_sp1.run()
  p_utils.write_json('temporary_test_translate_sp1.json', j_program_pairs)


def _test_translate_sp2():
  pass


def _test_get_translation_pairs_from_tsp():
  tsp = ("if id_puox:\n    secret_fun_4071()", "if 8860:\n    secret_fun_4071()")
  template_dict = p_utils.read_json('/code/repo-duoglot/backend/duoglotcore-server/pirel-logs/debug-11-broken-split/L0009/11-12-09-24-06.754595-L0009_SIMPLIFIED-TEMPLATE-p_llm_gen.json')

  translation_pairs = get_translation_pairs_from_tsp(tsp, template_dict)
  p_utils.write_json('temporary_test_get_translation_pairs_from_tsp.json', translation_pairs)


def _test_get_feedback_message_trans_sp1_partial():
  test_harness_config:dict = p_utils.read_json('temporary_test_get_feedback_message_trans_sp1_partial_config.json')

  template_dict = p_utils.read_json(test_harness_config['template_dict_fpath'])
  sp1 = test_harness_config['sp1']

  validation_result = p_utils.read_json(test_harness_config['validation_result_dict_fpath'])
  val_result_obj = p_llm_val.TranslateSP1ValidationResult(validation_result)

  trans_obj = SP1_PartialProgramG('test-trans-sp1-partial', template_dict, sp1)
  feedback_message = trans_obj.get_feedback_message(val_result_obj)
  feedback_message.pretty_print()


def _test_get_feedback_message_trans_sp2_partial():
  test_harness_config:dict = p_utils.read_json('temporary_test_get_feedback_message_trans_sp2_partial_config.json')

  template_dict = p_utils.read_json(test_harness_config['template_dict_fpath'])
  sp1_tp1_cand = test_harness_config['sp1_tp1_cand']
  sp2 = test_harness_config['sp2']

  validation_result = p_utils.read_json(test_harness_config['validation_result_dict_fpath'])
  val_result_obj = p_llm_val.TranslateSP2ValidationResult(validation_result)

  trans_obj = SP2_PartialProgramG('test-trans-sp2-partial', template_dict, sp1_tp1_cand, sp2)
  feedback_message = trans_obj.get_feedback_message(val_result_obj)
  feedback_message.pretty_print()


if __name__ == '__main__':
  # _test_translate_sp1()
  # _test_translate_sp2()
  # _test_get_translation_pairs_from_tsp()
  # _test_get_feedback_message_trans_sp1_partial()
  _test_get_feedback_message_trans_sp2_partial()
