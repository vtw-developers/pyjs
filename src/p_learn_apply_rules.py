import argparse
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Union

import d_grammar_expand
import p_consts
import p_pirel
import p_subject
import p_utils
import p_rule_applicator


logger = p_utils.setup_logger(__name__)


@dataclass
class RuleLearningPhaseStats:
  success: bool = None
  start_time: int = None
  end_time: int = None
  translation_rules_main_code: str = None
  error_as_list: List[str] = None

@dataclass
class RuleApplicationPhaseStats:
  success: bool = None
  start_time: int = None
  end_time: int = None
  tar_main_code: str = None
  error_as_list: List[str] = None

@dataclass
class SubjectStats:
  benchmark_name: str
  subject_name: str
  src_main_code: str
  subject_idx: int
  sample_size: int
  start_time: int = None
  end_time: int = None
  stats_le: RuleLearningPhaseStats = None
  stats_app: RuleApplicationPhaseStats = None

  def get_total_time(self) -> str:
    assert self.start_time is not None and self.end_time is not None, 'Start and end times must be set'
    total_sec = self.end_time - self.start_time
    if total_sec < 60:
      return f'{total_sec}s'
    total_min, total_sec = divmod(total_sec, 60)
    total_hr, total_min = divmod(total_min, 60)
    if total_hr == 0:
      return f'{total_min}m {total_sec}s'
    return f'{total_hr}h{total_min}m{total_sec}s'


def rule_learning_phase_on_subject(subject: p_subject.PirelSubject, starting_ruleset: str) -> Tuple[str, str]:
  '''
  RETURN Tuple of learned translation rules and translated program.
  RAISE All errors propagate to the caller.
  '''

  logger.info(f'Starting translation of {subject.name}')
  translation_rules = starting_ruleset
  p_utils.log_file_time(f'{subject.name}_starting-ruleset.snart', translation_rules)

  # This loop stops iff translation is successful or an error is raised.
  # Each iteration handles one problematic node at a time.
  iteration = 1
  while True:
    logger.info(f'~~~~ Iteration #{iteration}')
    print(f'~~~~ Iteration #{iteration}')

    # PiREL attempts to translate the code. If there is a node that PiREL
    # cannot translate (a.k.a. problematic node), it will generate a
    # translation rule that translates the problematic node.
    try:
      duoglot_result_dict = p_pirel.duoglot_translate_wrapper(
        subject.src_main_code,
        subject.src_lang,
        subject.tar_lang,
        translation_rules,
        subject.auto_backward,
        subject.choices,
        subject_name=subject.name,
      )
      logger.info('SUCCESS. Translation is successful. Returning the target program.')
      return translation_rules, duoglot_result_dict['tar_code']

    except d_grammar_expand.TranslationRuleNotFoundException as exc:
      logger.warning('Translation failed. Attempting to learn translation rules for the problematic node.')
      templates_dict = exc.get_templates_dict()
      trules_list = p_pirel.learn_trans_rules_for_prob_node(subject, translation_rules, templates_dict)

      logger.debug(f'PiREL has generated some translation rules to address the problematic node.')
      logger.debug(f'Number of translation rules: {len(trules_list)}')
      logger.debug(f'Prepending newly inferred translation rules to the existing ruleset')

      # TODO do not add duplicate rules
      comment = f';;;; NEW RULE FROM PiREL (iteration {iteration}) (subject_name {subject.name})'
      for idx, translation_rule in enumerate(trules_list, start=1):
        translation_rules = f'{comment} (rule {idx})\n{translation_rule}\n\n\n' + translation_rules
        logger.debug(f'NEW RULE {idx}:\n{translation_rule}')

      p_utils.log_file_time(f'{subject.name}_updated-ruleset.snart', translation_rules)
      logger.debug(f'Ruleset has been updated with {len(trules_list)} translation rules.\n\n')
      iteration += 1


def learn_and_application_phases_on_subject(subject: p_subject.PirelSubject, starting_ruleset: str, **kwargs) -> SubjectStats:
  '''
  Run PiREL to learn and apply translation rules for a given subject.
  Save source program, learned translation rules, and a plausible target program.
  RAISE Nothing. Take care of all exceptions.
  RETURN a stats dictionary
  '''

  assert 'subject_idx' in kwargs
  assert 'sample_size' in kwargs

  stats_subj = SubjectStats(
    benchmark_name=subject.benchmark_name,
    subject_name=subject.name,
    src_main_code=subject.src_main_code,
    subject_idx=kwargs['subject_idx'],
    sample_size=kwargs['sample_size'],
  )

  # ~~~ RULE LEARNING PHASE
  logger.debug(f'~~~ Starting rule learning phase for "{subject.name}"')
  stats_le = RuleLearningPhaseStats()
  stats_le.start_time = p_utils.current_time_sec()
  stats_subj.stats_le = stats_le
  stats_subj.start_time = stats_le.start_time

  try:
    learned_trans_rules, tar_main_code = rule_learning_phase_on_subject(subject, starting_ruleset)

    logger.info(f'SUCCESS Translation of "{subject.name}" is successful.')
    logger.debug(f"Saving learned rules and target program in {p_consts.LEARN_RULES_LOGS_DIR}.")
    p_utils.llog_text(f'{subject.name}_learned_rules.snart', learned_trans_rules)
    p_utils.llog_text(f'{subject.name}_source_program.py', subject.src_main_code)

    stats_le.success = True
    stats_le.translation_rules_main_code = learned_trans_rules

  except Exception as exc:
    msg = f'FAIL Failed to translate "{subject.name}"\n'
    msg += p_utils.exception_to_str(exc)
    logger.error(msg)

    stats_le.success = False
    stats_le.error_as_list = msg.splitlines()  # so it looks better in json

  stats_le.end_time = p_utils.current_time_sec()
  logger.debug(f'Rule learning phase for "{subject.name}" is complete')

  # ~~~ RULE APPLICATION PHASE
  # NOTE runs only if 'learn rules' phase is successful
  logger.debug(f'~~~ Starting rule application phase for "{subject.name}"')
  stats_app = RuleApplicationPhaseStats()
  stats_subj.stats_app = stats_app
  stats_app.start_time = p_utils.current_time_sec()
  if not stats_le.success:
    logger.debug(f'Rule learning phase was not successful. Skipping rule application phase for "{subject.name}"')
    stats_subj.end_time = stats_app.start_time
    return stats_subj

  try:
    logger.debug(f'Rule learning phase was successful. Starting rule application phase for "{subject.name}"')
    # NOTE Rule application phase is run on the learned translation rules
    subject.translation_rules_main_code = learned_trans_rules
    tar_program = p_rule_applicator.apply_translation_rules(subject)
    tar_test_code, tar_main_code, tar_test_call_code = tar_program.split(p_consts.TEST_MAIN_CALL_DELIMITER)

    logger.debug(f'Rule application phase for "{subject.name}" is successful.')
    logger.debug(f'Here is the source program:\n{subject.src_main_code}')
    logger.debug(f'Here is the target program:\n{tar_main_code}')

    p_utils.llog_text(f'{subject.name}_source_program.py', subject.src_main_code)
    p_utils.llog_text(f'{subject.name}_target_program.py', tar_main_code)

    stats_app.success = True
    stats_app.tar_main_code = tar_main_code

  except Exception as exc:
    msg = f'FAIL Failed to apply "{subject.name}"\n'
    msg += p_utils.exception_to_str(exc)

    logger.error(msg)

    stats_app.success = False
    stats_app.error_as_list = msg.splitlines()  # so it looks better in json

  stats_app.end_time = p_utils.current_time_sec()
  stats_subj.end_time = stats_app.end_time
  logger.debug(f'Rule application phase for "{subject.name}" is complete')

  return stats_subj


def learn_and_application_phases_on_sample(conf_fpath: Path) -> None:
  '''
  Run PiREL to learn and apply translation rules for a given benchmark.
  '''

  def _load_benchmark_sample(conf: dict) -> List[Tuple[str, str]]:
    '''
    RETURN a sequence of (subject_name, src_program).
    `subject_name` is a five character prefix of the program in the dataset.
    `src_program` is contents of the program in the benchmark
    (includes test, main, test call code for leetcode).
    Origin of the dataset is located at `data/duoglot/tests/staleetcode/pysep`.

    NOTE removes comments and docstrings from the main code.
    '''
    def _exclude(sample: List[Tuple[str, str]], exclude_list: List[str]) -> List[Tuple[str, str]]:
      return list(filter(lambda x: x[0] not in exclude_list, sample))

    benchmark_name = conf['benchmark_name']
    assert benchmark_name in ['leetcode'], 'TODO add support for other benchmarks'

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

      # NOTE first five characters of the filename is the subject name for `leetcode`
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

  def _email_report(subject_name: str, learning_phase_stats: Dict[str, SubjectStats]) -> None:
    stats_subj = learning_phase_stats[subject_name]
    stats_le = stats_subj.stats_le
    stats_app = stats_subj.stats_app

    # `L0001 1/20 7m11s: `
    subject = f'{stats_subj.subject_name} {stats_subj.subject_idx}/{stats_subj.sample_size} '
    subject += f'{stats_subj.get_total_time()}: '
    message = f'{stats_subj.src_main_code}\n\n\n'

    assert stats_le.success in [True, False], 'Learn rules phase must have a result'
    assert stats_app.success in [True, False, None], 'sanity check'

    if stats_le.success is True:
      assert stats_app.success in [True, False], 'Rule application phase must run if learn rules phase is successful'
      if stats_app.success is True:
        subject = subject + f'LE(+) AP(+)'
        message = message + stats_app.tar_main_code
      else:
        subject = subject + f'LE(+) AP(-)'
        message = message + '\n'.join(stats_app.error_as_list)
    else:
      assert stats_app.success is None, 'Rule application phase must not run if learn rules phase fails'
      subject = subject + f'LE(-) AP(?)'
      message = message + '\n'.join(stats_le.error_as_list)

    p_utils.email_safely(subject=subject, message=message)

  def _load_starting_ruleset(conf: dict) -> str:
    '''
    RETURN the starting ruleset for the learning phase from
    the configuration file or the default starting ruleset.
    '''
    if conf.get('is_load_starting_ruleset', False):
      starting_ruleset_fpath = p_consts.ROOT_DIR / conf['starting_ruleset_fpath']
      assert starting_ruleset_fpath.exists(), 'Starting ruleset file does not exist'
      return p_utils.read_text(starting_ruleset_fpath)
    return p_utils.read_text(p_consts.STARTING_RULESET_FPATH)

  logger.info('~~~ Starting `p_learn_apply_rules.learning_phase_all_subjects`')

  conf = p_utils.read_yaml(conf_fpath)
  starting_ruleset = _load_starting_ruleset(conf)
  benchmark_sample = _load_benchmark_sample(conf)
  assert len(benchmark_sample) > 0, 'No subjects were loaded'

  stats_for_email = {}
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

    # ~~~ entry point for a single subject
    subject_stats = learn_and_application_phases_on_subject(
      subject,
      starting_ruleset,
      subject_idx=subject_idx,
      sample_size=len(benchmark_sample)
    )

    stats_for_email[subject_name] = subject_stats
    p_utils.llog_json_time(f'learning-phase-stats-{subject_name}.json', asdict(subject_stats))
    if conf['is_email_report']:
      _email_report(subject_name, stats_for_email)
    logger.debug(p_utils.footer(subject_name))

  logger.info(f'~~~ Learning phase for all subjects is complete.')


if __name__ == '__main__':
  argparser = argparse.ArgumentParser()
  argparser.add_argument('conf_fname', type=str, help='Name the configuration file (default=default.yaml)')
  args = argparser.parse_args()
  conf_fname : str = args.conf_fname if args.conf_fname.endswith('.yaml') else args.conf_fname + '.yaml'
  conf_fpath = p_consts.CONFIGS_DIR / conf_fname
  assert conf_fpath.exists(), f'Configuration file does not exist: {conf_fpath}'

  try:
    learn_and_application_phases_on_sample(conf_fpath)
  except Exception as exc:
    p_utils.email_safely(subject='LEARNING PHASE SCRIPT ERROR', message=p_utils.exception_to_str(exc))
    raise
