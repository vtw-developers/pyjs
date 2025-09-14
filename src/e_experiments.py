import argparse
import asyncio
import os
from typing import List, Optional, Tuple

import e_common
import e_consts
import p_consts
import p_learn_apply_rules
import p_ruleset
import p_rule_applicator as prapp
import p_rule_validator
import p_subject
import p_utils
import csv


def get_rule_application_duration_msec(
  apply_subject: p_subject.PirelSubject
) -> Tuple[int, Optional[str]]:
  '''
  Returns the time taken to apply rules to the subject in milliseconds,
  along with a error string if an exception occurred (None otherwise).
  NOTE Refer to p_learn_apply_rules for what apply_subject should be.
  '''
  try:
    start_time = p_utils.current_time_msec()
    tar_program_plausible, translate_dbg_history = \
      asyncio.run(prapp.apply_translation_rules(apply_subject))
  except Exception as err:
    return p_utils.current_time_msec() - start_time, str(err)
  return p_utils.current_time_msec() - start_time, None


def get_rule_application_used_rules(
  apply_subject: p_subject.PirelSubject,
  ruleset: p_ruleset.Ruleset
) -> List[p_ruleset.TRuleBase]:
  '''
  Returns the set of rule IDs that were actually used during rule application.
  NOTE Refer to p_learn_apply_rules for what apply_subject should be.
  NOTE ruleset actually is already part of apply_subject, but in a str form.
       We need it in obj form.
  RETURN List of rules (p_ruleset.TRuleBase) that were used during application.
  '''
  tar_program_plausible, translate_dbg_history = \
    asyncio.run(prapp.apply_translation_rules(apply_subject))
  used_rule_ids = p_rule_validator.get_used_translation_rule_ids(translate_dbg_history)
  used_rules = [ruleset.get_rule_by_idx(rid) for rid in used_rule_ids]
  return used_rules


def e01_table_gfg_rule_application_runtime_no_union(args):
  '''
  Measure the time it takes to translate a subject using only the rules
  learned from that subject (i.e., no union of rules from other subjects).
  Outputs a CSV file with columns:
  (NUM_RULES, DURATION_MSEC, ERROR_STR)

  NOTE NUM_RULES includes rules from starting ruleset.
  '''
  logger = p_utils.setup_logger(__name__, args.output_dir / 'e01.log')
  fout = open(args.output_dir / 'e01_table_gfg_rule_application_runtime_no_union.csv', 'w', newline='')
  writer = csv.writer(fout)
  writer.writerow(['NUM_RULES', 'DURATION_MSEC', 'ERROR_STR'])

  subject_names = e_common.load_subject_names(args.subject_names_fpath)
  for idx, subject_name in enumerate(subject_names, start=1):
    logger.info(f'[{idx}/{len(subject_names)}] Processing subject: {subject_name}')

    src_program = e_common.get_subject_src_from_bench_dir(subject_name, 'gfg')
    subject = p_subject.PirelSubject('gfg', subject_name, src_program, 'py', 'js', True)
    ruleset = e_common.load_rulesets_union([subject_name], args.logs_dir)
    apply_subject = p_learn_apply_rules._create_subject_for_apply_phase(subject, ruleset)
    duration_msec, error_str = get_rule_application_duration_msec(apply_subject)
    writer.writerow([len(ruleset.rules), duration_msec, error_str or ""])
  fout.close()

def e02_table_gfg_rule_application_runtime_union(args):
  '''
  Measure the time it takes to translate a subject using the union of rules
  learned from that subject and other subjects.
  Outputs a CSV file with columns:
  (NUM_RULES, DURATION_MSEC, ERROR_STR)
  '''
  logger = p_utils.setup_logger(__name__, args.output_dir / 'e02.log')
  fout = open(args.output_dir / 'e02_table_gfg_rule_application_runtime_union.csv', 'w', newline='')
  writer = csv.writer(fout)
  writer.writerow(['NUM_RULES', 'DURATION_MSEC', 'ERROR_STR'])

  subject_names = e_common.load_subject_names(args.subject_names_fpath)
  ruleset = e_common.load_rulesets_union(subject_names, args.logs_dir)

  for idx, subject_name in enumerate(subject_names, start=1):
    logger.info(f'[{idx}/{len(subject_names)}] Processing subject: {subject_name}')

    src_program = e_common.get_subject_src_from_bench_dir(subject_name, 'gfg')
    subject = p_subject.PirelSubject(
      benchmark_name='gfg', name=subject_name, src_program=src_program,
      src_lang='py', tar_lang='js', is_three_split=True)
    apply_subject = p_learn_apply_rules._create_subject_for_apply_phase(subject, ruleset)
    duration_msec, error_str = get_rule_application_duration_msec(apply_subject)
    writer.writerow([len(ruleset.rules), duration_msec, error_str or ""])
  fout.close()


def e03_rq1_gfg_subtree_trans_success_rate(args):
  '''
  Write a CSV file with columns:
  (NUMERATOR, DENOMINATOR, ERROR_STR)

  where NUMERATOR is the number of subtrees that were successfully translated,
  DENOMINATOR is the total number of subtrees, and ERROR_STR is an error
  message if an error occurred during rule application (None otherwise).
  '''
  logger = p_utils.setup_logger(__name__, args.output_dir / 'e03.log')
  fout = open(args.output_dir / 'e03_rq1_gfg_subtree_trans_success_rate.csv', 'w', newline='')
  writer = csv.writer(fout)
  writer.writerow(['NUMERATOR', 'DENOMINATOR', 'ERROR_STR'])

  subject_names = e_common.load_subject_names(args.subject_names_fpath)
  for idx, subject_name in enumerate(subject_names, start=1):
    logger.info(f'[{idx}/{len(subject_names)}] Processing subject: {subject_name}')

    src_program = e_common.get_subject_src_from_bench_dir(subject_name, 'gfg')
    subject = p_subject.PirelSubject('gfg', subject_name, src_program, 'py', 'js', True)
    ruleset = e_common.load_rulesets_union([subject_name], args.logs_dir)
    apply_subject = p_learn_apply_rules._create_subject_for_apply_phase(subject, ruleset)

    # need to add the rule since it's added at a str level in
    # p_learn_apply_rules._create_subject_for_apply_phase
    ruleset.append_rule(p_ruleset.LogStatTRule(p_ruleset.LogStatTRule.parse_rule_str(
      p_utils.read_text(p_consts.LOG_STAT_RULE_FPATH))))

    try:
      used_rules = get_rule_application_used_rules(apply_subject, ruleset)
    except Exception as err:
      logger.error(f'Error applying rules for subject {apply_subject.name}: {err}')
      writer.writerow(['', '', str(err)])
      continue

    numerator = len([r for r in used_rules
                 if isinstance(r, p_ruleset.StandardTRule)
                 or isinstance(r, p_ruleset.StatementOverfittedTRule)])
    denominator = len([r for r in used_rules
                   if isinstance(r, p_ruleset.StandardTRule)
                   or isinstance(r, p_ruleset.StatementOverfittedTRule)])
    writer.writerow([numerator, denominator, ''])
  fout.close()


def e04_rq2_gfg_rule_extractability(args):
  '''
  Write a CSV file with columns:
  (NUMERATOR, DENOMINATOR, ERROR_STR)

  where NUMERATOR is the number of subtrees for which rules are successfully extracted,
  DENOMINATOR is the number of subtrees PiREL attempts to translate, and ERROR_STR is an error
  message if an error occurred during rule application (None otherwise).
  '''
  logger = p_utils.setup_logger(__name__, args.output_dir / 'e04.log')
  fout = open(args.output_dir / 'e04_rq2_gfg_rule_extractability.csv', 'w', newline='')
  writer = csv.writer(fout)
  writer.writerow(['NUMERATOR', 'DENOMINATOR', 'ERROR_STR'])

  subject_names = e_common.load_subject_names(args.subject_names_fpath)
  for idx, subject_name in enumerate(subject_names, start=1):
    logger.info(f'[{idx}/{len(subject_names)}] Processing subject: {subject_name}')

    src_program = e_common.get_subject_src_from_bench_dir(subject_name, 'gfg')
    subject = p_subject.PirelSubject('gfg', subject_name, src_program, 'py', 'js', True)
    ruleset = e_common.load_rulesets_union([subject_name], args.logs_dir)
    apply_subject = p_learn_apply_rules._create_subject_for_apply_phase(subject, ruleset)

    # need to add the rule since it's added at a str level in
    # p_learn_apply_rules._create_subject_for_apply_phase
    ruleset.append_rule(p_ruleset.LogStatTRule(p_ruleset.LogStatTRule.parse_rule_str(
      p_utils.read_text(p_consts.LOG_STAT_RULE_FPATH))))

    try:
      used_rules = get_rule_application_used_rules(apply_subject, ruleset)
    except Exception as err:
      logger.error(f'Error applying rules for subject {apply_subject.name}: {err}')
      writer.writerow(['', '', str(err)])
      continue

    numerator = len([r for r in used_rules
                 if isinstance(r, p_ruleset.StandardTRule)])
    denominator = len([r for r in used_rules
                   if isinstance(r, p_ruleset.StandardTRule)
                   or isinstance(r, p_ruleset.StatementOverfittedTRule)])
    writer.writerow([numerator, denominator, ''])
  fout.close()


def get_args():
  parser = argparse.ArgumentParser(description='Run various experiments with data from PiREL.')
  parser.add_argument('--experiment', '-e',
                      help='ID of the experiment to run (int)',
                      type=int, required=True)
  parser.add_argument('--subject_names_fpath', '-s',
                      help='Path to a text file containing subject names, one per line',
                      required=False, default=(p_consts.EXPERIMENTS_DIR / 'subject-names.txt'))
  parser.add_argument('--logs_dir', '-l',
                      help='Path to directory containing PiREL logs.',
                      # required=False, default=p_consts.LEARN_RULES_LOGS_DIR)
                      required=False, default='/root/pirel-shared-volume/logs-archive/debug-46/logs/learn-rules')
  parser.add_argument('--output_dir', '-o',
                      help='Path to output directory.',
                      required=False, default=e_consts.RESULTS_DIR)
  parser.add_argument('--tag', '-t',
                      help='Tag to append to output directory name.',
                      required=False, type=str, default='')
  return parser.parse_args()


def main():
  args = get_args()

  if args.subject_names_fpath:
    args.subject_names_fpath = e_common.normalize_path(args.subject_names_fpath)
  if args.logs_dir:
    args.logs_dir = e_common.normalize_path(args.logs_dir)
  if args.output_dir:
    args.output_dir = e_common.normalize_path(args.output_dir)

  args.tag = args.tag.strip().replace(' ', '_')
  args.tag = f'-{args.tag}' if args.tag else ''
  args.output_dir = args.output_dir / f'{p_utils.current_time()}{args.tag}'
  os.makedirs(args.output_dir, exist_ok=True)

  if args.experiment == 1:
    e01_table_gfg_rule_application_runtime_no_union(args)
  elif args.experiment == 2:
    e02_table_gfg_rule_application_runtime_union(args)
  elif args.experiment == 3:
    e03_rq1_gfg_subtree_trans_success_rate(args)
  elif args.experiment == 4:
    e04_rq2_gfg_rule_extractability(args)
  else:
    raise ValueError(f'Unknown experiment: {args.experiment}')


if __name__ == '__main__':
  main()
