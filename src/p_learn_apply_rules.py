import argparse
import asyncio
import random
from dataclasses import asdict
from pathlib import Path
from typing import List, Tuple

import p_consts
import p_pirel
import p_ruleset
import p_rule_applicator as prapp
import p_subject
import p_tree_log as ptlog
import p_utils
import p_visitor_py as pvpy


logger = p_utils.setup_logger(__name__)


# TaskGroup would cancel the remaining tasks in case one fails.
# With workaround <https://stackoverflow.com/questions/75250788>,
# SIGINT (Ctrl-C) has to be sent twice to stop the program though.
class ForgivingTaskGroup(asyncio.TaskGroup):
  _abort = lambda self: None


async def _mode_benchmark_subject_finish(
  lsubject: ptlog.Subject,
  lbenchmark: ptlog.Benchmark,
  lock: asyncio.Lock,
  shared_cnt_fin: List[int],
  conf: dict
) -> None:
  '''
  Called when a task for a subject finishes.
  '''

  lrule_learn_phase = lsubject.rule_learn_phase
  lrule_application_phase = lsubject.rule_application_phase

  async with lock:
    shared_cnt_fin[0] += 1

  # `L0001 1/20 7m11s: `
  subject = f'{lsubject.subject_name} {shared_cnt_fin[0]}/{lbenchmark.sample_size} '
  message = f'{lsubject.subject_name}:\n\n'

  if lrule_learn_phase.success is True:
    assert lrule_application_phase.success in [True, False], 'sanity check'
    if lrule_application_phase.success is True:
      subject = subject + f'L-YES, A-YES'
      message = message + lrule_application_phase.tar_main_code_plausible
    else:
      subject = subject + f'L-YES, A-NO'
      message = message + lrule_application_phase.reason
  else:
    subject = subject + f'L-NO'
    message = message + lrule_learn_phase.reason

  if conf.get('is_email_report', False):
    p_utils.email_safely(subject=subject, message=message)


def _create_src_program_for_apply_phase(
  main_subject: p_subject.PirelSubject
) -> str:
  '''
  RETURN the source program to be used in the application phase.
  '''
  if not main_subject.is_three_split:
    return pvpy.LogIndexerNo3Split.index_log_statements(
      pvpy.LogInserterNo3Split.insert_log_statements(
        main_subject.src_program))
  src_main_code = main_subject.get_src_main_code()
  src_main_code = pvpy.LogStatementInserter.insert_log_statements(src_main_code)
  src_main_code = pvpy.LogStatementsIndexer.index_log_statements(src_main_code)
  src_test_code = main_subject.get_src_test_code()
  src_test_call_code = main_subject.get_src_test_call_code()
  src_program = p_consts.TEST_SCRIPT_TEMPLATE.format(
    test_code=src_test_code, main_code=src_main_code, test_call_code=src_test_call_code)
  return src_program


def _create_subject_for_apply_phase(
  main_subject: p_subject.PirelSubject,
  current_ruleset: p_ruleset.Ruleset,
) -> p_subject.PirelSubject:
  '''
  Create a PirelSubject instance for the application phase.
  '''
  logger.debug('Creating subject for application phase')
  p_utils.log_json_time('args-_create_subject_for_apply_phase.json', locals())

  # all attributes of PirelSubject instance set explicitly
  benchmark_name = main_subject.benchmark_name
  name = main_subject.name
  src_program = _create_src_program_for_apply_phase(main_subject)
  src_lang = main_subject.src_lang
  tar_lang = main_subject.tar_lang
  is_three_split = main_subject.is_three_split
  translation_rules_main_code = \
    current_ruleset.to_str_ruleset() + '\n\n' + \
    p_utils.read_text(p_consts.LOG_STAT_RULE_FPATH)  # code is instrumented
  translation_rules_test_code = main_subject.translation_rules_test_code
  auto_backward = True
  choices = main_subject.choices
  readonly_choices_list = []

  # create a subject instance
  apply_phase_subject = p_subject.PirelSubject(
    benchmark_name, name, src_program, src_lang, tar_lang, is_three_split)
  apply_phase_subject.translation_rules_main_code = translation_rules_main_code
  apply_phase_subject.translation_rules_test_code = translation_rules_test_code
  apply_phase_subject.auto_backward = auto_backward
  apply_phase_subject.choices = choices
  apply_phase_subject.readonly_choices_list = readonly_choices_list

  # override readonly_choices_list with verified rules
  apply_phase_subject.readonly_choices_list = current_ruleset.get_choices_list_from_verified_rules(
    apply_phase_subject.get_src_main_code())

  return apply_phase_subject


async def learn_and_application_phases_on_subject(
  subject: p_subject.PirelSubject,
  starting_ruleset_str: str,
  lsubject: ptlog.Subject,
  lbenchmark: ptlog.Benchmark,
  semaphore: asyncio.Semaphore,
  lock: asyncio.Lock,
  shared_cnt_fin: List[int],
  conf: dict
):
  '''
  Wrapper function to run both rule learning and application phases.
  RETURN validated ruleset or None on failure.
  '''
  starting_ruleset = p_ruleset.Ruleset.from_starting_ruleset(starting_ruleset_str)

  # rule learning phase
  lrule_learn_phase = ptlog.RuleLearnPhase()
  lsubject.rule_learn_phase = lrule_learn_phase

  try:
    async with semaphore:
      logger.info('About to start rule learning phase')
      await p_pirel.learn_trans_rules_for_subject(
        subject, starting_ruleset, lrule_learn_phase)

    logger.info(f'SUCCESS Rule learning phase for "{subject.name}" succeeded.')
    lrule_learn_phase.success = True
    lrule_learn_phase.etms = p_utils.current_time_msec()
    p_utils.llog_text(f'{subject.name}_learned_rules.snart', starting_ruleset.to_str_ruleset())
    p_utils.llog_json(f'{subject.name}_learned_rules.json', starting_ruleset.to_dict())
    p_utils.llog_text(f'{subject.name}_src_main_code.py', subject.get_src_main_code())
    p_utils.llog_yaml(f'{subject.name}_tree_log_learn_phase_success.yaml', asdict(lsubject))

  except Exception as exc:
    logger.critical(f'FAIL Rule learning phase for "{subject.name}" failed.')
    logger.critical(p_utils.exception_to_str(exc))
    lrule_learn_phase.success = False
    lrule_learn_phase.reason = p_utils.exception_to_str(exc)
    lrule_learn_phase.etms = p_utils.current_time_msec()
    p_utils.llog_yaml(f'{subject.name}_tree_log_learn_phase_fail.yaml', asdict(lsubject))
    return await _mode_benchmark_subject_finish(lsubject, lbenchmark, lock, shared_cnt_fin, conf)

  # rule application phase
  lrule_application_phase = ptlog.RuleApplicationPhase()
  lsubject.rule_application_phase = lrule_application_phase
  lrule_application_phase.stms = p_utils.current_time_msec()
  try:
    async with semaphore:
      logger.info('About to start rule application phase')
      apply_subject = _create_subject_for_apply_phase(subject, starting_ruleset)
      tar_program_plausible, translate_dbg_history = \
        await prapp.apply_translation_rules(apply_subject)
      if subject.is_three_split:
        _, tar_main_code_plausible, _ = \
          tar_program_plausible.split(p_consts.TEST_MAIN_CALL_DELIMITER)
      else:
        tar_main_code_plausible = tar_program_plausible

    logger.info(f'SUCCESS Rule application phase for "{subject.name}" succeeded.')
    lrule_application_phase.tar_main_code_plausible = tar_main_code_plausible
    lrule_application_phase.success = True
    lrule_application_phase.etms = p_utils.current_time_msec()
    p_utils.llog_text(f'{subject.name}_validated_rules.snart', starting_ruleset.to_str_ruleset())
    p_utils.llog_json(f'{subject.name}_validated_rules.json', starting_ruleset.to_dict())
    p_utils.llog_text(f'{subject.name}_tar_main_code_plausible.{subject.tar_lang}', tar_main_code_plausible)
    p_utils.llog_yaml(f'{subject.name}_tree_log_apply_phase_success.yaml', asdict(lsubject))

  except Exception as exc:
    logger.critical(f'FAIL Rule application phase for "{subject.name}" failed.')
    logger.critical(p_utils.exception_to_str(exc))
    lrule_application_phase.success = False
    lrule_application_phase.reason = p_utils.exception_to_str(exc)
    lrule_application_phase.etms = p_utils.current_time_msec()
    p_utils.llog_yaml(f'{subject.name}_tree_log_apply_phase_fail.yaml', asdict(lsubject))
    return await _mode_benchmark_subject_finish(lsubject, lbenchmark, lock, shared_cnt_fin, conf)

  logger.info(f'SUCCESS Both learn and apply phases for "{subject.name}" succeeded.')
  await _mode_benchmark_subject_finish(lsubject, lbenchmark, lock, shared_cnt_fin, conf)


def _mode_benchmark_init(
  conf: dict
) -> Tuple[str, List[Tuple[str, str]], ptlog.Benchmark, List[p_subject.PirelSubject]]:

  def _load_benchmark_sample(conf: dict) -> List[Tuple[str, str]]:
    '''
    RETURN a sequence of (subject_name, src_program).
    `subject_name` is a five character prefix of the program in the dataset.
    `src_program` is contents of the program in the benchmark
    NOTE removes comments and docstrings from src_main_code.
    '''
    def _exclude(sample: List[Tuple[str, str]], exclude_list: List[str]) -> List[Tuple[str, str]]:
      return list(filter(lambda x: x[0] not in exclude_list, sample))

    benchmark_name = conf['benchmark_name']
    assert benchmark_name in p_consts.BENCHMARK_CONFIGS, \
      f'{benchmark_name=} not supported'

    benchmark_conf = p_consts.BENCHMARK_CONFIGS[benchmark_name]
    benchmark_dir = benchmark_conf['benchmark_dir']

    subject_fpaths : List[Path] = list(sorted(benchmark_dir.glob(f"*.{conf['src_lang']}")))
    dataset : List[Tuple[str, str]] = []

    # LOAD ALL SUBJECTS
    for subject_fpath in subject_fpaths:
      src_program = p_utils.read_text(subject_fpath)

      # NOTE remove comments, docstrings, and empty lines from main_code (not extensively tested)
      if conf['is_three_split']:
        src_test_code, src_main_code, src_test_call_code = src_program.split(p_consts.TEST_MAIN_CALL_DELIMITER)
        src_main_code = p_utils.remove_comments_and_docstrings_py(src_main_code)
        src_main_code = p_utils.remove_empty_lines(src_main_code)
        src_program = f'\n{p_consts.TEST_MAIN_CALL_DELIMITER}\n'.join([src_test_code, src_main_code, src_test_call_code])
      else:
        src_program = p_utils.remove_comments_and_docstrings_py(src_program)
        src_program = p_utils.remove_empty_lines(src_program)

      if conf['benchmark_name'] in ('gfg', 'leetcode'):
        subject_name = subject_fpath.stem[:5]
      else:
        subject_name = subject_fpath.stem
      dataset.append((subject_name, src_program))

    logger.debug(f'Loaded {len(dataset)} programs for translation rule learning phase.')

    # GO OVER THE SAMPLE LOADING OPTIONS
    # 1. `only` has the highest priority
    if len(conf['sample']['only']) > 0:
      sample = list(filter(lambda x: x[0] in conf['sample']['only'], dataset))
      return _exclude(sample, conf['sample']['exclude'])

    # 2. `is_random` has the second highest priority
    if conf['sample']['is_random']:
      dataset = _exclude(dataset, conf['sample']['exclude'])
      sample = sorted(random.sample(dataset, conf['sample']['size']))
      return sample

    # 3. slice the dataset
    start_idx = conf['sample']['start_idx']
    end_idx = start_idx + conf['sample']['size']
    sample = dataset[start_idx:end_idx]
    return _exclude(sample, conf['sample']['exclude'])

  def _load_starting_ruleset(conf: dict) -> str:
    '''
    RETURN the starting ruleset for the learning phase from
    the configuration file or the default starting ruleset.
    '''
    if conf.get('is_override_starting_ruleset', False):
      overriding_ruleset = ''
      for path_str in conf['overriding_ruleset_fpaths']:
        overriding_ruleset_fpath = p_consts.ROOT_DIR / path_str
        assert overriding_ruleset_fpath.exists(), f'Overriding ruleset file does not exist: {overriding_ruleset_fpath}'
        overriding_ruleset += p_utils.read_text(overriding_ruleset_fpath).strip() + '\n\n'
      return overriding_ruleset.strip()
    return p_utils.read_text(p_consts.STARTING_RULESET_FPATH)

  starting_ruleset_str = _load_starting_ruleset(conf)
  benchmark_sample = _load_benchmark_sample(conf)
  assert len(benchmark_sample) > 0, 'No subjects were loaded'

  lbenchmark = ptlog.Benchmark()
  lbenchmark.benchmark_name = conf['benchmark_name']
  lbenchmark.sample_size = len(benchmark_sample)

  subject_list = []
  for subject_idx, (subject_name, src_program) in enumerate(benchmark_sample, start=1):

    subject = p_subject.PirelSubject(
      benchmark_name=conf['benchmark_name'],
      name=subject_name,
      src_program=src_program,
      src_lang=conf['src_lang'],
      tar_lang=conf['tar_lang'],
      is_three_split=conf['is_three_split'],
    )

    lsubject = ptlog.Subject()
    lsubject.id = subject_idx
    lsubject.subject_name = subject.name
    lsubject.src_main_code = subject.get_src_main_code()

    subject_list.append(subject)
    lbenchmark.subjects.append(lsubject)

  return starting_ruleset_str, benchmark_sample, lbenchmark, subject_list


async def mode_benchmark(conf: dict) -> None:
  '''
  Run PiREL to learn and apply translation rules for a given benchmark.
  '''
  starting_ruleset_str, benchmark_sample, lbenchmark, subject_list = \
    _mode_benchmark_init(conf)

  num_concurrent_subjects = min(
    len(benchmark_sample), conf.get('max_concurrent_subjects', p_consts.MAX_CONCURRENT_SUBJECTS))
  logger.debug(f'Using a semaphore with {num_concurrent_subjects} concurrent subjects')
  semaphore = asyncio.Semaphore(num_concurrent_subjects)

  lock = asyncio.Lock()
  shared_cnt_fin = [0]

  async with ForgivingTaskGroup() as tg:
    for subject, lsubject in zip(subject_list, lbenchmark.subjects):
      coroutine = learn_and_application_phases_on_subject(
        subject, starting_ruleset_str, lsubject, lbenchmark,
        semaphore, lock, shared_cnt_fin, conf)
      tg.create_task(coroutine, name=subject.name)

  p_utils.llog_yaml(f'tree-log-{conf["benchmark_name"]}.yaml', asdict(lbenchmark))


async def mode_custom_deprecated(conf: dict) -> None:
  '''
  Run PiREL to learn translation rules for any program.
  '''

  logger.info('~~~ Starting mode_custom_deprecated()')

  subject = p_subject.PirelSubject.from_file_config(
    p_consts.PIREL_SUBJECT_CONFIGS_DIR / conf['pirel_subject_conf'])
  starting_ruleset = p_ruleset.Ruleset.from_starting_ruleset(
    subject.translation_rules_main_code)

  lsubject = ptlog.Subject()
  lsubject.id = 1
  lsubject.subject_name = subject.name
  lsubject.src_main_code = subject.get_src_main_code()
  lrule_learn_phase = ptlog.RuleLearnPhase()
  lsubject.rule_learn_phase = lrule_learn_phase

  try:
    await p_pirel.learn_trans_rules_for_subject(
      subject,
      starting_ruleset,
      lrule_learn_phase
    )

    lrule_learn_phase.success = True
    lrule_learn_phase.etms = p_utils.current_time_msec()
    logger.info(f'SUCCESS Translation of "{subject.name}" is successful.')
    logger.debug(f"Saving learned rules and target program in {p_consts.LEARN_RULES_LOGS_DIR}.")
    p_utils.llog_text(f'{subject.name}_learned_rules.snart', starting_ruleset.to_str_ruleset())
    p_utils.llog_json(f'{subject.name}_learned_rules.json', starting_ruleset.to_dict())
    p_utils.llog_text(f'{subject.name}_source_program.py', subject.get_src_main_code())

  except Exception as exc:
    msg = f'FAIL Failed to translate "{subject.name}"\n'
    msg += p_utils.exception_to_str(exc)
    lrule_learn_phase.success = False
    lrule_learn_phase.reason = msg
    lrule_learn_phase.etms = p_utils.current_time_msec()
    logger.error(msg)

  p_utils.llog_yaml(f'tree-log-custom-mode-{subject.name}.yaml', asdict(lsubject))


MODE_CALLBACKS = {
  'benchmark': mode_benchmark,
  'custom': mode_custom_deprecated,
}


def main():
  argparser = argparse.ArgumentParser()
  argparser.add_argument('conf_fname', type=str, help='Name of the configuration file')
  args = argparser.parse_args()

  conf_fname : str = args.conf_fname if args.conf_fname.endswith('.yaml') else args.conf_fname + '.yaml'
  conf_fpath = p_consts.LEARN_APPLY_RULES_CONFIGS_DIR / conf_fname
  assert conf_fpath.exists(), f'Configuration file does not exist: {conf_fpath}'

  conf = p_utils.read_yaml(conf_fpath)
  mode = conf['mode']
  assert mode in MODE_CALLBACKS, f'Invalid mode: {mode}. Must be one of {MODE_CALLBACKS}'
  assert f'mode_{mode}' in conf, f'"mode_{mode}" mode configuration is missing in "{conf_fpath}"'
  mode_conf = conf[f'mode_{mode}']

  try:
    asyncio.run(MODE_CALLBACKS[mode](mode_conf))
  except Exception as exc:
    p_utils.email_safely(subject='LEARNING PHASE SCRIPT ERROR', message=p_utils.exception_to_str(exc))
    raise


if __name__ == '__main__':
  main()
