import argparse
import random
from dataclasses import asdict
from pathlib import Path
from typing import List, Optional, Tuple

import p_consts
import p_pirel
import p_rule_applicator
import p_subject
import p_translators
import p_tree_log as ptlog
import p_utils


logger = p_utils.setup_logger(__name__)


def cleanup():
  '''
  Clear global caches.
  '''
  logger.info('Cleaning up global caches')
  p_translators._TRANSLATORS_CACHE.clear()


def learn_phase_on_subject(
  subject: p_subject.PirelSubject,
  starting_ruleset: str,
  lsubject: ptlog.Subject,
) -> Optional[str]:
  '''
  Run PiREL to learn translation rules for a given subject.
  '''
  logger.debug(f'~~~ Starting rule learning phase for "{subject.name}"')

  lrule_learn_phase = ptlog.RuleLearnPhase()
  lrule_learn_phase.start_time = p_utils.current_time_sec()
  lsubject.rule_learn_phase = lrule_learn_phase

  try:
    learned_trans_rules = p_pirel.learn_trans_rules_for_subject(subject, starting_ruleset, lrule_learn_phase)

    lrule_learn_phase.success = True
    lrule_learn_phase.end_time = p_utils.current_time_sec()

    logger.info(f'SUCCESS Successfully learned translation rules for "{subject.name}".')
    logger.debug(f"Saving learned rules and target program in {p_consts.LEARN_RULES_LOGS_DIR}.")

    p_utils.llog_text(f'{subject.name}_learned_rules.snart', learned_trans_rules)
    p_utils.llog_text(f'{subject.name}_source_program.py', subject.src_main_code)
    p_utils.llog_yaml_time(f'tree-log-learn-phase-success-{subject.name}.yaml', asdict(lsubject))

    return learned_trans_rules

  except Exception as exc:
    msg = f'FAIL Failed to learn translation rules for "{subject.name}" due to exception:\n'
    msg += p_utils.exception_to_str(exc)
    logger.error(msg)

    lrule_learn_phase.success = False
    lrule_learn_phase.end_time = p_utils.current_time_sec()
    lrule_learn_phase.reason = str(exc)

    lsubject.success = False
    lsubject.reason = 'Translation rule learning phase failed'

    p_utils.llog_yaml_time(f'tree-log-learn-phase-fail-{subject.name}.yaml', asdict(lsubject))

    return None


def application_phase_on_subject(
  subject: p_subject.PirelSubject,
  learned_trans_rules: str,
  lsubject: ptlog.Subject,
) -> Optional[str]:
  '''
  Run PiREL to apply translation rules for a given subject.
  '''

  p_utils.log_json_time(f'{subject.name}_args-application_phase_on_subject.json', locals())
  logger.debug(f'~~~ Starting rule application phase for "{subject.name}"')

  '''
  NOTE should run only if 'learn rules' phase was successful
  NOTE Rule application phase is run on the learned translation rules
  NOTE Rule Application Phase assumes that we have just enough
  translation rules to obtain "some" translation of the source code,
  i.e. there exists some combination of translation rules that
  that are enough to obtain the target code:
    - the translation is syntactically correct
      - since it is checked during rule learning phase
    - the translation may have compile errors
      - interpreter errors for scripting languages
        such as "var is not defined"
      - if there are compile errors, rule application phase
        will attempt to find another combination of translation rules
        that will not have compile errors
      - if there are still compile errors, the rule application phase
        raises `RuntimeError('No unique choices found')`
    - if there are no compile errors, there might still be semantic
      errors, i.e. the target code does not produce the expected output.
  '''

  lrule_application_phase = ptlog.RuleApplicationPhase()
  lrule_application_phase.start_time = p_utils.current_time_sec()
  lsubject.rule_application_phase = lrule_application_phase

  try:
    subject.translation_rules_main_code = learned_trans_rules
    tar_program, used_rule_ids_history = p_rule_applicator.apply_translation_rules(subject)
    tar_test_code, tar_main_code, tar_test_call_code = tar_program.split(p_consts.TEST_MAIN_CALL_DELIMITER)

    logger.debug(f'SUCCESS Rule application phase for "{subject.name}" is successful.')
    logger.debug(f'Here is the source program:\n{subject.src_main_code}')
    logger.debug(f'Here is the target program:\n{tar_main_code}')

    p_utils.llog_text(f'{subject.name}_source_program.{subject.src_lang}', subject.src_main_code)
    p_utils.llog_text(f'{subject.name}_target_program.{subject.tar_lang}', tar_main_code)

    lrule_application_phase.success = True
    lrule_application_phase.end_time = p_utils.current_time_sec()
    lrule_application_phase.plausible_target_program = tar_main_code
    lsubject.success = True

    p_utils.llog_yaml_time(f'tree-log-apply-phase-success-{subject.name}.yaml', asdict(lsubject))
    return learned_trans_rules

  except Exception as exc:
    msg = f'FAIL Failed to apply learned translation rules for "{subject.name}" due to exception:\n'
    msg += p_utils.exception_to_str(exc)
    logger.error(msg)

    lrule_application_phase.success = False
    lrule_application_phase.end_time = p_utils.current_time_sec()
    lrule_application_phase.reason = msg
    lsubject.success = False
    lsubject.reason = 'Translation rule application phase failed'

    p_utils.llog_yaml_time(f'tree-log-apply-phase-fail-{subject.name}.yaml', asdict(lsubject))
    return None


def mode_benchmark(conf: dict) -> None:
  '''
  Run PiREL to learn and apply translation rules for a given benchmark.
  '''

  def _load_benchmark_sample(conf: dict) -> List[Tuple[str, str]]:
    '''
    RETURN a sequence of (subject_name, src_program).
    `subject_name` is a five character prefix of the program in the dataset.
    `src_program` is contents of the program in the benchmark
    (includes test, main, test call code for leetcode).
    NOTE removes comments and docstrings from the main code.
    '''
    def _exclude(sample: List[Tuple[str, str]], exclude_list: List[str]) -> List[Tuple[str, str]]:
      return list(filter(lambda x: x[0] not in exclude_list, sample))

    benchmark_name = conf['benchmark_name']
    assert benchmark_name in ['leetcode', 'gfg'], f'benchmark "{benchmark_name}" not supported'

    benchmark_conf = p_consts.BENCHMARK_CONFIGS[benchmark_name]
    benchmark_dir = benchmark_conf['benchmark_dir']

    subject_fpaths : List[Path] = list(sorted(benchmark_dir.glob(f"*.{conf['src_lang']}")))
    dataset : List[Tuple[str, str]] = []

    # LOAD ALL SUBJECTS
    for subject_fpath in subject_fpaths:
      src_program = p_utils.read_text(subject_fpath)

      # NOTE remove comments, docstrings, and empty lines from main_code (not extensively tested)
      src_test_code, src_main_code, src_test_call_code = src_program.split(p_consts.TEST_MAIN_CALL_DELIMITER)
      src_main_code = p_utils.remove_comments_and_docstrings_py(src_main_code)
      src_main_code = p_utils.remove_empty_lines(src_main_code)
      src_program = f'\n{p_consts.TEST_MAIN_CALL_DELIMITER}\n'.join([src_test_code, src_main_code, src_test_call_code])

      # NOTE first five characters of the filename is the subject name for `leetcode` and `gfg`
      subject_name = subject_fpath.stem[:5]
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

  def _email_report(lsubject: ptlog.Subject, lbenchmark: ptlog.Benchmark) -> None:
    lrule_learn_phase = lsubject.rule_learn_phase
    lrule_application_phase = lsubject.rule_application_phase

    # `L0001 1/20 7m11s: `
    subject = f'{lsubject.subject_name} {lsubject.id}/{lbenchmark.sample_size} '
    subject += f'{lsubject.get_total_time()}: '
    message = f'{lsubject.subject_name}:\n\n'

    if lrule_learn_phase.success is True:
      assert lrule_application_phase.success in [True, False], 'Rule application phase must run if learn rules phase is successful'
      if lrule_application_phase.success is True:
        subject = subject + f'LEARN +, APPLY +'
        message = message + lrule_application_phase.plausible_target_program
      else:
        subject = subject + f'LEARN +, APPLY -'
        message = message + lrule_application_phase.reason
    else:
      subject = subject + f'LEARN -'
      message = message + lrule_learn_phase.reason

    p_utils.email_safely(subject=subject, message=message)

  def _load_starting_ruleset(conf: dict) -> str:
    '''
    RETURN the starting ruleset for the learning phase from
    the configuration file or the default starting ruleset.
    '''
    if conf.get('is_override_starting_ruleset', False):
      overriding_ruleset_fpath = p_consts.ROOT_DIR / conf['overriding_ruleset_fpath']
      assert overriding_ruleset_fpath.exists(), 'Starting ruleset file does not exist'
      return p_utils.read_text(overriding_ruleset_fpath)
    return p_utils.read_text(p_consts.STARTING_RULESET_FPATH)

  logger.info('~~~ Starting mode_benchmark()')

  starting_ruleset = _load_starting_ruleset(conf)
  benchmark_sample = _load_benchmark_sample(conf)
  assert len(benchmark_sample) > 0, 'No subjects were loaded'

  lbenchmark = ptlog.Benchmark(conf['benchmark_name'])
  lbenchmark.sample_size = len(benchmark_sample)

  for subject_idx, (subject_name, src_program) in enumerate(benchmark_sample, start=1):
    msg = f'Starting learning phase for {subject_idx}/{len(benchmark_sample)}-th program ({subject_name})'
    logger.debug(p_utils.header(subject_name) + msg)
    print(msg)

    subject = p_subject.PirelSubject(
      benchmark_name=conf['benchmark_name'],
      name=subject_name,
      src_program=src_program,
      src_lang=conf['src_lang'],
      tar_lang=conf['tar_lang'],
    )

    lsubject = ptlog.Subject(subject.name)
    lsubject.code_text = subject.src_main_code
    lsubject.id = subject_idx
    lbenchmark.subjects.append(lsubject)

    # ~~~ rule learning phase
    trans_rules = learn_phase_on_subject(subject, starting_ruleset, lsubject)
    if trans_rules is None:
      logger.debug(f'Rule learning phase for "{subject.name}" was not successful. Skipping rule application phase')
      continue

    # ~~~ rule application phase
    trans_rules = application_phase_on_subject(subject, trans_rules, lsubject)

    # update the starting ruleset for the next subject
    # by adding the learned rules if specified in the config
    if trans_rules is not None:
      assert isinstance(trans_rules, str), 'learned translation rules must be a string'
      if conf.get('is_reuse_trans_rules_across_subjects', False):
        starting_ruleset += trans_rules
        logger.info(f'Updated starting ruleset for the next subject with "{subject.name}" ruleset')

    if conf['is_email_report']:
      _email_report(lsubject, lbenchmark)
    logger.debug(p_utils.footer(subject_name))
    cleanup()

  p_utils.llog_yaml_time(f'tree-log-{conf["benchmark_name"]}.yaml', asdict(lbenchmark))
  logger.info(f'~~~ Learning phase for all subjects is complete.')


def mode_custom(conf: dict) -> None:
  '''
  Run PiREL to learn translation rules for any program.
  '''

  logger.info('~~~ Starting mode_custom()')

  subject = p_subject.PirelSubject.from_file_config(p_consts.PIREL_SUBJECT_CONFIGS_DIR / conf['pirel_subject_conf'])
  lsubject = ptlog.Subject(subject.name)
  lsubject.code_text = subject.src_main_code
  lrule_learn_phase = ptlog.RuleLearnPhase()
  lsubject.rule_learn_phase = lrule_learn_phase

  try:
    learned_trans_rules = p_pirel.learn_trans_rules_for_subject(
      subject,
      subject.translation_rules_main_code,
      lrule_learn_phase
    )

    lrule_learn_phase.success = True
    lsubject.success = True
    logger.info(f'SUCCESS Translation of "{subject.name}" is successful.')
    logger.debug(f"Saving learned rules and target program in {p_consts.LEARN_RULES_LOGS_DIR}.")
    p_utils.llog_text(f'{subject.name}_learned_rules.snart', learned_trans_rules)
    p_utils.llog_text(f'{subject.name}_source_program.py', subject.src_main_code)

  except Exception as exc:
    msg = f'FAIL Failed to translate "{subject.name}"\n'
    msg += p_utils.exception_to_str(exc)
    lrule_learn_phase.success = False
    lrule_learn_phase.reason = msg
    lsubject.success = False
    lsubject.reason = 'Translation rule learning phase failed'
    logger.error(msg)

  p_utils.llog_yaml_time(
    f'tree-log-custom-mode-{subject.name}.yaml',
    asdict(lsubject),
    strs_as_lines=True,
    remove_null_vals=True,
    remove_empty_lists=True
  )


MODE_CALLBACKS = {
  'benchmark': mode_benchmark,
  'custom': mode_custom,
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
    MODE_CALLBACKS[mode](mode_conf)
  except Exception as exc:
    p_utils.email_safely(subject='LEARNING PHASE SCRIPT ERROR', message=p_utils.exception_to_str(exc))
    raise


if __name__ == '__main__':
  main()
