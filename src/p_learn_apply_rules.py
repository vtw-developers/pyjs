import argparse
import random
from dataclasses import asdict
from pathlib import Path
from typing import List, Optional, Tuple

import d_grammar_expand
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
  lrule_learn_phase: ptlog.RuleLearnPhase
) -> Tuple[str, str]:
  '''
  RETURN Tuple of learned translation rules and translated program.
  RAISE All errors propagate to the caller.
  '''

  logger.info(f'Starting translation of "{subject.name}"')
  translation_rules = starting_ruleset
  p_utils.log_file_time(f'{subject.name}_starting-ruleset.snart', translation_rules)

  # This loop stops iff translation is successful or an error is raised.
  # Each iteration handles one problematic node at a time.
  iteration = 1
  while True:
    msg = f'~~~~ translation_iteration.id = {iteration}'
    logger.info(msg)
    print(msg)

    ltrans_iteration = ptlog.TransIteration(iteration)
    lrule_learn_phase.translation_iterations.append(ltrans_iteration)

    # PiREL attempts to translate the code. If there is a node that PiREL
    # cannot translate (a.k.a. problematic node), it will generate a
    # translation rule that translates the problematic node.
    try:
      logger.debug(f'Attempting to translate "{subject.name}" with the current ruleset')
      logger.debug(f'Number of translation rules in the ruleset: {translation_rules.count("match_expand")}')

      duoglot_result_dict = p_pirel.duoglot_translate_wrapper(
        subject.src_main_code,
        subject.src_lang,
        subject.tar_lang,
        translation_rules,
        subject.auto_backward,
        subject.choices,
        subject_name=subject.name,
      )

      ltrans_iteration.success = True

      logger.info('SUCCESS. Translation is successful. Returning the target program.')
      return translation_rules, duoglot_result_dict['tar_code']

    except d_grammar_expand.TranslationRuleNotFoundException as exc:
      logger.warning('FAIL. Translation failed. Attempting to learn translation rules for the problematic node.')
      templates_dict = exc.get_templates_dict()

      lprob_node = ptlog.ProbNode(templates_dict['problematic_node_id'], templates_dict['problematic_node_type'])
      ltrans_iteration.success = False
      ltrans_iteration.reason = f'''No translation rule for "{templates_dict['problematic_node_type']}"'''
      ltrans_iteration.problematic_node = lprob_node

      # ~~~ entering PiREL learning phase
      # NOTE all raised errors are sent to the caller. If there are no exceptions,
      # it means that there are translation rules to address the problematic node.
      trules_list = p_pirel.learn_trans_rules_for_prob_node(subject, translation_rules, templates_dict, lprob_node)

      logger.debug(f'PiREL has generated some translation rules to address the problematic node.')
      logger.debug(f'Number of translation rules: {len(trules_list)}')
      logger.debug(f'Prepending newly inferred translation rules to the existing ruleset')

      ltrans_iteration.success = True
      ltrans_iteration.reason = None

      # TODO do not add duplicate rules
      comment = f';;;; NEW RULE FROM PiREL (iteration {iteration}) (subject_name {subject.name})'
      for idx, translation_rule in enumerate(trules_list, start=1):
        translation_rules = f'{comment} (rule {idx})\n{translation_rule}\n\n\n' + translation_rules
        logger.debug(f'NEW RULE {idx}:\n{translation_rule}')

      p_utils.log_file_time(f'{subject.name}_updated-ruleset.snart', translation_rules)
      logger.debug(f'Ruleset has been updated with {len(trules_list)} translation rules.\n\n')
      iteration += 1


def learn_and_application_phases_on_subject(
  subject: p_subject.PirelSubject,
  starting_ruleset: str,
  lsubject: ptlog.Subject,
) -> Optional[str]:
  '''
  Run PiREL to learn and apply translation rules for a given subject.
  Save source program, learned translation rules, and a plausible target program.
  RAISE Nothing. Take care of all exceptions.
  RETURN None if rule learning phase or rule application phase fails, if both phases
  are successful, return the learned translation rules.
  '''

  # ~~~ RULE LEARNING PHASE
  logger.debug(f'~~~ Starting rule learning phase for "{subject.name}"')
  lrule_learn_phase = ptlog.RuleLearnPhase()
  lrule_learn_phase.start_time = p_utils.current_time_sec()
  lsubject.rule_learn_phase = lrule_learn_phase

  try:
    learned_trans_rules, tar_main_code = learn_phase_on_subject(subject, starting_ruleset, lrule_learn_phase)

    lrule_learn_phase.success = True
    lrule_learn_phase.end_time = p_utils.current_time_sec()
    logger.info(f'SUCCESS Translation of "{subject.name}" is successful.')
    logger.debug(f"Saving learned rules and target program in {p_consts.LEARN_RULES_LOGS_DIR}.")
    p_utils.llog_text(f'{subject.name}_learned_rules.snart', learned_trans_rules)
    p_utils.llog_text(f'{subject.name}_source_program.py', subject.src_main_code)

  except Exception as exc:
    msg = f'FAIL Failed to translate "{subject.name}"\n'
    msg += p_utils.exception_to_str(exc)
    logger.error(msg)

    lrule_learn_phase.success = False
    lrule_learn_phase.end_time = p_utils.current_time_sec()
    lrule_learn_phase.reason = str(exc)
    lsubject.success = False
    lsubject.reason = 'Translation rule learning phase failed'

    p_utils.llog_yaml_time(
      f'tree-log-01-learn-phase-exception-{subject.name}.yaml',
      asdict(lsubject),
      strs_as_lines=True,
      remove_null_vals=True,
      remove_empty_lists=True
    )

    logger.debug(f'Rule learning phase was not successful. Skipping rule application phase for "{subject.name}"')
    return None

  logger.debug(f'Rule learning phase for "{subject.name}" is complete')

  # ~~~ RULE APPLICATION PHASE
  '''NOTE runs only if 'learn rules' phase is successful
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

  logger.debug(f'Rule learning phase was successful. Starting rule application phase for "{subject.name}"')
  lrule_application_phase = ptlog.RuleApplicationPhase()
  lrule_application_phase.start_time = p_utils.current_time_sec()
  lsubject.rule_application_phase = lrule_application_phase

  try:
    subject.translation_rules_main_code = learned_trans_rules
    tar_program = p_rule_applicator.apply_translation_rules(subject)
    tar_test_code, tar_main_code, tar_test_call_code = tar_program.split(p_consts.TEST_MAIN_CALL_DELIMITER)

    logger.debug(f'Rule application phase for "{subject.name}" is successful.')
    logger.debug(f'Here is the source program:\n{subject.src_main_code}')
    logger.debug(f'Here is the target program:\n{tar_main_code}')

    p_utils.llog_text(f'{subject.name}_source_program.{subject.src_lang}', subject.src_main_code)
    p_utils.llog_text(f'{subject.name}_target_program.{subject.tar_lang}', tar_main_code)

    lrule_application_phase.success = True
    lrule_application_phase.end_time = p_utils.current_time_sec()
    lrule_application_phase.plausible_target_program = tar_main_code
    lsubject.success = True

    p_utils.llog_yaml_time(
      f'tree-log-03-rule-learn-and-apply-{subject.name}.yaml',
      asdict(lsubject),
      strs_as_lines=True,
      remove_null_vals=True,
      remove_empty_lists=True
    )
    logger.debug(f'Rule application phase for "{subject.name}" is complete')
    return learned_trans_rules

  except Exception as exc:
    msg = f'FAIL Failed to apply "{subject.name}"\n'
    msg += p_utils.exception_to_str(exc)
    logger.error(msg)

    lrule_application_phase.success = False
    lrule_application_phase.end_time = p_utils.current_time_sec()
    lrule_application_phase.reason = msg
    lsubject.success = False
    lsubject.reason = 'Translation rule application phase failed'

    p_utils.llog_yaml_time(
      f'tree-log-02-apply-phase-exception-{subject.name}.yaml',
      asdict(lsubject),
      strs_as_lines=True,
      remove_null_vals=True,
      remove_empty_lists=True
    )

    logger.debug(f'Rule learning phase was not successful.')
    return None


def learn_and_application_phases_benchmark_mode(conf: dict) -> None:
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

  logger.info('~~~ Starting `p_learn_apply_rules.learn_and_application_phases_benchmark_mode`')

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
    lsubject.id = subject_idx
    lbenchmark.subjects.append(lsubject)

    # ~~~ entry point for a single subject
    trans_rules = learn_and_application_phases_on_subject(subject, starting_ruleset, lsubject)

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

  p_utils.llog_yaml_time(
    f'tree-log-{conf["benchmark_name"]}.yaml',
    asdict(lbenchmark),
    strs_as_lines=True,
    remove_null_vals=True,
    remove_empty_lists=True
  )
  logger.info(f'~~~ Learning phase for all subjects is complete.')


def learn_and_application_phases_custom_mode(conf: dict) -> None:
  '''
  Run PiREL to learn and apply translation rules for any program.

  NOTE Right now, this function does not support rule application.
  Only the learning phase is completed.
  '''

  logger.info('~~~ Starting `p_learn_apply_rules.learn_and_application_phases_custom_mode`')

  subject = p_subject.PirelSubject.from_file_config(p_consts.PIREL_SUBJECT_CONFIGS_DIR / conf['pirel_subject_conf'])
  lsubject = ptlog.Subject(subject.name)
  lrule_learn_phase = ptlog.RuleLearnPhase()
  lsubject.rule_learn_phase = lrule_learn_phase

  try:
    learned_trans_rules, tar_main_code = learn_phase_on_subject(subject, subject.translation_rules_main_code, lrule_learn_phase)

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
  'benchmark': learn_and_application_phases_benchmark_mode,
  'custom': learn_and_application_phases_custom_mode,
}


if __name__ == '__main__':
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
