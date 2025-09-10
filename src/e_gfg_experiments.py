import argparse
import asyncio
from typing import Optional, Tuple

import e_analyze_data
import p_consts
import p_learn_apply_rules
import p_rule_applicator as prapp
import p_subject
import p_utils


logger = p_utils.setup_logger(__name__)


_BENCHMARK_NAME = 'gfg'
_SRC_LANG = 'py'
_TAR_LANG = 'js'


def get_rule_application_duration_msec(
  apply_subject: p_subject.PirelSubject
) -> Tuple[int, Optional[str]]:
  '''
  Returns the time taken to apply rules to the subject in milliseconds,
  along with a boolean indicating if there was an error during application.
  '''
  try:
    start_time = p_utils.current_time_msec()
    tar_program_plausible = asyncio.run(prapp.apply_translation_rules(apply_subject))
  except Exception as err:
    logger.error(f'Error applying rules for subject {apply_subject.name}: {err}')
    return p_utils.current_time_msec() - start_time, str(err)

  return p_utils.current_time_msec() - start_time, None


def e01_rule_application_runtime_no_union(args):
  '''
  Measure the time it takes to translate a subject using only the rules
  learned from that subject (i.e., no union of rules from other subjects).
  Outputs a TSV file with columns:
  (NUM_RULES, DURATION_MSEC, ERROR_STR)

  NOTE NUM_RULES includes rules from starting ruleset.
  '''
  output_fpath = args.output_fpath or (p_consts.EXPERIMENTS_DIR / 'e01_rule_application_runtime_no_union.txt')
  output_fpath = e_analyze_data._normalize_path(output_fpath)
  fout = open(output_fpath, 'w')

  subject_names = e_analyze_data.get_subject_names(args)
  for idx, subject_name in enumerate(subject_names, start=1):
    logger.info(f'[{idx}/{len(subject_names)}] Processing subject: {subject_name}')

    src_program = e_analyze_data.get_subject_src_program(subject_name, _BENCHMARK_NAME)
    subject = p_subject.PirelSubject(
      benchmark_name=_BENCHMARK_NAME, name=subject_name, src_program=src_program,
      src_lang=_SRC_LANG, tar_lang=_TAR_LANG, is_three_split=True)
    ruleset = e_analyze_data.load_rulesets(
      [subject_name], e_analyze_data._normalize_path(args.logs_dir))
    apply_subject = p_learn_apply_rules._create_subject_for_apply_phase(subject, ruleset)
    duration_msec, error_str = get_rule_application_duration_msec(apply_subject)
    fout.write(f'{len(ruleset.rules)}\t{duration_msec}\t{error_str or ""}\n')

  fout.close()


def e02_rule_application_runtime_union(args):
  '''
  Measure the time it takes to translate a subject using the union of rules
  learned from that subject and other subjects.
  Outputs a TSV file with columns:
  (NUM_RULES, DURATION_MSEC, ERROR_STR)
  '''
  output_fpath = args.output_fpath or (p_consts.EXPERIMENTS_DIR / 'e02_rule_application_runtime_union.txt')
  output_fpath = e_analyze_data._normalize_path(output_fpath)
  fout = open(output_fpath, 'w')

  subject_names = e_analyze_data.get_subject_names(args)
  ruleset = e_analyze_data.load_rulesets(
    subject_names, e_analyze_data._normalize_path(args.logs_dir))

  for idx, subject_name in enumerate(subject_names, start=1):
    logger.info(f'[{idx}/{len(subject_names)}] Processing subject: {subject_name}')

    src_program = e_analyze_data.get_subject_src_program(subject_name, _BENCHMARK_NAME)
    subject = p_subject.PirelSubject(
      benchmark_name=_BENCHMARK_NAME, name=subject_name, src_program=src_program,
      src_lang=_SRC_LANG, tar_lang=_TAR_LANG, is_three_split=True)
    apply_subject = p_learn_apply_rules._create_subject_for_apply_phase(subject, ruleset)
    duration_msec, error_str = get_rule_application_duration_msec(apply_subject)
    fout.write(f'{len(ruleset.rules)}\t{duration_msec}\t{error_str or ""}\n')

  fout.close()


def get_args():
  parser = argparse.ArgumentParser(description='Run various experiments with data from PiREL.')
  parser.add_argument('--experiment', '-e',
                      help='ID of the experiment to run (int)',
                      type=int, required=True)
  parser.add_argument('--subject_names_fpath', '-s',
                      help='Path to a text file containing subject names, one per line',
                      required=False, default=(p_consts.EXPERIMENTS_DIR / 'subject-names.txt'))
  parser.add_argument('--output_fpath', '-o',
                      help='Path to output file.',
                      required=False)
  parser.add_argument('--logs_dir', '-l',
                      help='Path to directory containing PiREL logs.',
                      required=False, default=p_consts.LEARN_RULES_LOGS_DIR)
  return parser.parse_args()


def main():
  args = get_args()
  if args.experiment == 1:
    e01_rule_application_runtime_no_union(args)
  if args.experiment == 2:
    e02_rule_application_runtime_union(args)
  else:
    raise ValueError(f'Unknown experiment: {args.experiment}')


if __name__ == '__main__':
  main()
