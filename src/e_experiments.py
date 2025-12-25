import argparse
import asyncio
import os
from typing import Dict, List, Optional, Tuple

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
  (SUBJECT_NAME, NUM_RULES, DURATION_MSEC, ERROR_STR)

  NOTE NUM_RULES includes rules from starting ruleset.
  '''
  logger = p_utils.setup_logger(__name__, args.output_dir / 'e01.log')
  fout = open(args.output_dir / 'e01_table_gfg_rule_application_runtime_no_union.csv', 'w', newline='')
  writer = csv.writer(fout)
  writer.writerow(['SUBJECT_NAME', 'NUM_RULES', 'DURATION_MSEC', 'ERROR_STR'])

  subject_names = e_common.load_subject_names(args.subject_names_fpath)
  for idx, subject_name in enumerate(subject_names, start=1):
    logger.info(f'[{idx}/{len(subject_names)}] Processing subject: {subject_name}')

    src_program = e_common.get_subject_src_from_bench_dir(subject_name, 'gfg')
    subject = p_subject.PirelSubject('gfg', subject_name, src_program, 'py', 'js', True)
    ruleset = e_common.load_rulesets_union([subject_name], args.logs_dir)
    apply_subject = p_learn_apply_rules._create_subject_for_apply_phase(subject, ruleset)
    duration_msec, error_str = get_rule_application_duration_msec(apply_subject)
    writer.writerow([subject_name, len(ruleset.rules), duration_msec, error_str or ""])

  fout.close()


def e02_table_gfg_rule_application_runtime_union(args):
  '''
  Measure the time it takes to translate a subject using the union of rules
  learned from that subject and other subjects.
  Outputs a CSV file with columns:
  (SUBJECT_NAME, NUM_RULES, DURATION_MSEC, ERROR_STR)
  '''
  logger = p_utils.setup_logger(__name__, args.output_dir / 'e02.log')
  fout = open(args.output_dir / 'e02_table_gfg_rule_application_runtime_union.csv', 'w', newline='')
  writer = csv.writer(fout)
  writer.writerow(['SUBJECT_NAME', 'NUM_RULES', 'DURATION_MSEC', 'ERROR_STR'])

  subject_names = e_common.load_subject_names(args.subject_names_fpath)
  ruleset = e_common.load_rulesets_union(subject_names, args.logs_dir)
  logger.info(f'Loaded {len(ruleset.rules)} rules in total for union of rulesets.')
  p_utils.write_json(args.output_dir / 'ruleset-union.json', ruleset.to_dict())

  for idx, subject_name in enumerate(subject_names, start=1):
    logger.info(f'[{idx}/{len(subject_names)}] Processing subject: {subject_name}')

    src_program = e_common.get_subject_src_from_bench_dir(subject_name, 'gfg')
    subject = p_subject.PirelSubject(
      benchmark_name='gfg', name=subject_name, src_program=src_program,
      src_lang='py', tar_lang='js', is_three_split=True)
    apply_subject = p_learn_apply_rules._create_subject_for_apply_phase(subject, ruleset)
    duration_msec, error_str = get_rule_application_duration_msec(apply_subject)
    writer.writerow([subject_name, len(ruleset.rules), duration_msec, error_str or ""])

  fout.close()


def e03_rq1_gfg_subtree_trans_success_rate(args):
  '''
  Write a CSV file with columns:
  (SUBJECT_NAME, NUMERATOR, DENOMINATOR, ERROR_STR)

  where NUMERATOR is the number of subtrees that were successfully translated,
  DENOMINATOR is the total number of subtrees, and ERROR_STR is an error
  message if an error occurred during rule application (None otherwise).
  '''
  logger = p_utils.setup_logger(__name__, args.output_dir / 'e03.log')
  fout = open(args.output_dir / 'e03_rq1_gfg_subtree_trans_success_rate.csv', 'w', newline='')
  writer = csv.writer(fout)
  writer.writerow(['SUBJECT_NAME', 'NUMERATOR', 'DENOMINATOR', 'ERROR_STR'])

  subject_names = e_common.load_subject_names(args.subject_names_fpath)
  for idx, subject_name in enumerate(subject_names, start=1):
    logger.info(f'[{idx}/{len(subject_names)}] Processing subject: {subject_name}')

    src_program = e_common.get_subject_src_from_bench_dir(subject_name, 'gfg')
    subject = p_subject.PirelSubject('gfg', subject_name, src_program, 'py', 'js', True)
    ruleset = e_common.load_rulesets_union([subject_name], args.logs_dir)
    apply_subject = p_learn_apply_rules._create_subject_for_apply_phase(subject, ruleset)

    # need to add the rule since it's added at a str level in
    # p_learn_apply_rules._create_subject_for_apply_phase
    # and is used by get_rule_application_used_rules()
    ruleset.append_rule(p_ruleset.LogStatTRule(p_ruleset.LogStatTRule.parse_rule_str(
      p_utils.read_text(p_consts.LOG_STAT_RULE_FPATH))))

    try:
      used_rules = get_rule_application_used_rules(apply_subject, ruleset)
    except Exception as err:
      logger.error(f'Error applying rules for subject {apply_subject.name}: {err}')
      writer.writerow([subject_name, '', '', str(err)])
      continue

    numerator = len([r for r in used_rules
                 if isinstance(r, p_ruleset.StandardTRule)
                 or isinstance(r, p_ruleset.StatementOverfittedTRule)])
    denominator = len([r for r in used_rules
                   if isinstance(r, p_ruleset.StandardTRule)
                   or isinstance(r, p_ruleset.StatementOverfittedTRule)])
    writer.writerow([subject_name, numerator, denominator, ''])

  fout.close()


def e04_rq2_gfg_rule_extractability(args):
  '''
  Write a CSV file with columns:
  (SUBJECT_NAME, NUMERATOR, DENOMINATOR, ERROR_STR)

  where NUMERATOR is the number of subtrees for which rules are successfully extracted,
  DENOMINATOR is the number of subtrees PiREL attempts to translate, and ERROR_STR is an error
  message if an error occurred during rule application (None otherwise).
  '''
  logger = p_utils.setup_logger(__name__, args.output_dir / 'e04.log')
  fout = open(args.output_dir / 'e04_rq2_gfg_rule_extractability.csv', 'w', newline='')
  writer = csv.writer(fout)
  writer.writerow(['SUBJECT_NAME', 'NUMERATOR', 'DENOMINATOR', 'ERROR_STR'])

  subject_names = e_common.load_subject_names(args.subject_names_fpath)
  for idx, subject_name in enumerate(subject_names, start=1):
    logger.info(f'[{idx}/{len(subject_names)}] Processing subject: {subject_name}')

    src_program = e_common.get_subject_src_from_bench_dir(subject_name, 'gfg')
    subject = p_subject.PirelSubject('gfg', subject_name, src_program, 'py', 'js', True)
    ruleset = e_common.load_rulesets_union([subject_name], args.logs_dir)
    apply_subject = p_learn_apply_rules._create_subject_for_apply_phase(subject, ruleset)

    # need to add the rule since it's added at a str level in
    # p_learn_apply_rules._create_subject_for_apply_phase
    # and is used by get_rule_application_used_rules()
    ruleset.append_rule(p_ruleset.LogStatTRule(p_ruleset.LogStatTRule.parse_rule_str(
      p_utils.read_text(p_consts.LOG_STAT_RULE_FPATH))))

    try:
      used_rules = get_rule_application_used_rules(apply_subject, ruleset)
    except Exception as err:
      logger.error(f'Error applying rules for subject {apply_subject.name}: {err}')
      writer.writerow([subject_name, '', '', str(err)])
      continue

    numerator = len([r for r in used_rules
                 if isinstance(r, p_ruleset.StandardTRule)])
    denominator = len([r for r in used_rules
                   if isinstance(r, p_ruleset.StandardTRule)
                   or isinstance(r, p_ruleset.StatementOverfittedTRule)])
    writer.writerow([subject_name, numerator, denominator, ''])
  fout.close()


def e05_rq3_gfg_rule_reusability(args):
  '''
  Writes a CSV file with columns
  (COUNT, RULE_TYPE, RULE_STR)

  COUNT is the number of times a rule is used for translation.
  RULE_TYPE is the type of the rule (StandardTRule or StatementOverfittedTRule).
  RULE_STR is the string representation of the rule.
  '''
  sub_dir = f'{p_utils.current_time()}-e05-{args.tag}'
  args.output_dir = args.output_dir / sub_dir
  os.makedirs(args.output_dir, exist_ok=True)

  logger = p_utils.setup_logger(__name__, args.output_dir / 'e05.log')
  logger.info('Starting e05_rq3_gfg_rule_reusability...')

  logger.info(f'Loading benchmark index from {args.bench_idx_fpath}')
  gfg_index = e_common.load_benchmark_index(args.bench_idx_fpath, filter_value_success=[True])

  if args.serialized_ruleset_union_fpath:
    logger.info(f'Loading union of rulesets from cached {args.serialized_ruleset_union_fpath}')
    ruleset_serialized = p_utils.read_json(args.serialized_ruleset_union_fpath)
    ruleset = p_ruleset.Ruleset.from_dict(ruleset_serialized)
    logger.info(f'Loaded {len(ruleset.rules)} rules in total.')
  else:
    logger.info(f'Loading union of rulesets from {args.shared_logs_dir}')
    ruleset = e_common.load_val_rulesets_union(gfg_index, args.shared_logs_dir)
    p_utils.write_json(args.output_dir / 'ruleset-union.json', ruleset.to_dict())
    logger.info(f'Loaded {len(ruleset.rules)} rules in total.')

  logger.info('Checking sizes of matcher groups in the ruleset...')
  logger.info(f'MAX_NUM_ALTERNATIVE_EXPANSIONS = {p_consts.MAX_NUM_ALTERNATIVE_EXPANSIONS}')
  for matcher_sig, rules in ruleset.matcher_groups.items():
    if len(rules) > p_consts.MAX_NUM_ALTERNATIVE_EXPANSIONS:
      logger.error(
        f'Large matcher group with {len(rules)} rules. '
        f'Rule application may fail.')
    else:
      logger.debug(f'Matcher group has {len(rules)} rules')

  logger.info('Running rule application on all subjects to collect used rules...')
  all_used_rules: List[p_ruleset.TRuleBase] = []
  subject_names = sorted(gfg_index.keys())

  for idx, subject_name in enumerate(subject_names, start=1):
    src_program = e_common.get_subject_src_from_bench_dir(subject_name, 'gfg')
    subject = p_subject.PirelSubject('gfg', subject_name, src_program, 'py', 'js', True)
    apply_subject = p_learn_apply_rules._create_subject_for_apply_phase(subject, ruleset)

    # need to add the rule since it's added at a str level in
    # p_learn_apply_rules._create_subject_for_apply_phase
    # and is used by get_rule_application_used_rules()
    # NOTE code is instrumented for rule applicator to work
    ruleset.append_rule(p_ruleset.LogStatTRule(p_ruleset.LogStatTRule.parse_rule_str(
      p_utils.read_text(p_consts.LOG_STAT_RULE_FPATH))))

    stms = p_utils.current_time_msec()
    try:
      logger.info(f'[{idx}/{len(subject_names)}] Running rule application for {subject_name}')
      used_rules = get_rule_application_used_rules(apply_subject, ruleset)
      all_used_rules.extend(used_rules)
    except Exception as err:
      logger.error(f'Error applying rules for subject {subject_name}: {err}')
      continue
    finally:
      etms = p_utils.current_time_msec()
      logger.info(f'Rule application for {subject_name} took {(etms-stms)/1000} sec')

  all_used_rules = [r for r in all_used_rules
                if isinstance(r, p_ruleset.StandardTRule)
                or isinstance(r, p_ruleset.StatementOverfittedTRule)
                or isinstance(r, p_ruleset.StartingTRule)]

  logger.info(f'Used rules count: {len(all_used_rules)}')
  p_utils.write_json(args.output_dir / 'all-used-rules.json', [r.to_dict() for r in all_used_rules])

  logger.info('Counting unique rules used...')
  rule_counts : Dict[str, Tuple[int, str]] = dict()
  for rule in all_used_rules:
    rule_str = rule.to_rule_str()
    if rule_str in rule_counts:
      rule_counts[rule_str] = (rule_counts[rule_str][0] + 1, rule_counts[rule_str][1])
    else:
      rule_counts[rule_str] = (1, type(rule).__name__)
  logger.info(f'Counted {len(rule_counts)} unique rules used.')

  logger.info('Creating table for CSV output...')
  table : List[Tuple[int, str, str]] = []  # `count` first for sorting
  for rule_str, (count, rule_type) in rule_counts.items():
    table.append((count, rule_type, rule_str))
  # sort by count descending
  table.sort(reverse=True, key=lambda x: x[0])

  logger.info(f'Writing CSV output to {args.output_dir / "e05_rq3_gfg_rule_reusability.csv"}...')
  fout = open(args.output_dir / 'e05_rq3_gfg_rule_reusability.csv', 'w', newline='')
  writer = csv.writer(fout)
  writer.writerow(['COUNT', 'RULE_TYPE', 'RULE_STR'])
  for row in table:
    writer.writerow(row)
  fout.close()


def e06_check_ruleset_integrity(args):
  '''
  Check if the ruleset union contains all rules from individual rulesets.
  '''
  sub_dir = f'{p_utils.current_time()}-e06-{args.tag}'
  args.output_dir = args.output_dir / sub_dir
  os.makedirs(args.output_dir, exist_ok=True)

  logger = p_utils.setup_logger(__name__, args.output_dir / 'e06.log')
  logger.info('Starting e06_check_ruleset_integrity...')

  logger.info(f'Loading benchmark index from {args.bench_idx_fpath}')
  gfg_index = e_common.load_benchmark_index(args.bench_idx_fpath, filter_value_success=[True])

  if args.serialized_ruleset_union_fpath:
    logger.info(f'Loading union of rulesets from cached {args.serialized_ruleset_union_fpath}')
    ruleset_serialized = p_utils.read_json(args.serialized_ruleset_union_fpath)
    ruleset = p_ruleset.Ruleset.from_dict(ruleset_serialized)
    logger.info(f'Loaded {len(ruleset.rules)} rules in total.')
  else:
    logger.info(f'Loading union of rulesets from {args.shared_logs_dir}')
    ruleset = e_common.load_val_rulesets_union(gfg_index, args.shared_logs_dir)
    p_utils.write_json(args.output_dir / 'ruleset-union.json', ruleset.to_dict())
    logger.info(f'Loaded {len(ruleset.rules)} rules in total.')

  for subject_name in sorted(gfg_index.keys()):
    logger.info(f'Checking ruleset for subject {subject_name}...')
    subject_ruleset = e_common.load_val_ruleset(
      subject_name,
      args.shared_logs_dir / gfg_index[subject_name]['logs_tag'] / 'logs' / 'learn-rules'
    )
    missing_rules = []
    for rule in subject_ruleset.rules:
      if rule not in ruleset.rules:
        missing_rules.append(rule)
    if missing_rules:
      logger.error(f'Ruleset union is missing {len(missing_rules)} rules from subject {subject_name}:')
      for rule in missing_rules:
        logger.error(f'  Missing rule: {rule.to_rule_str()}')
    else:
      logger.info(f'All {len(subject_ruleset.rules)} rules from subject {subject_name} are present in the union.')


def e07_check_rule_app_reproducability(args):
  '''
  Check if rule application works without errors and produces
  the same results for subjects with their own validated rules.
  '''
  sub_dir = f'{p_utils.current_time()}-e07-{args.tag}'
  args.output_dir = args.output_dir / sub_dir
  os.makedirs(args.output_dir, exist_ok=True)

  logger = p_utils.setup_logger(__name__, args.output_dir / 'e07.log')
  logger.info('Starting e07_check_rule_app_reproducability...')

  logger.info(f'Loading benchmark index from {args.bench_idx_fpath}')
  gfg_index = e_common.load_benchmark_index(args.bench_idx_fpath, filter_value_success=[True])

  for idx, subject_name in enumerate(sorted(gfg_index.keys()), start=1):
    logger.info(f'[{idx}/{len(gfg_index)}] Processing subject: {subject_name}')
    logs_dir = args.shared_logs_dir / gfg_index[subject_name]['logs_tag'] / 'logs' / 'learn-rules'

    try:
      rt, rules, tarprog = e_common.run_rule_app_single_gfg_own_rules(subject_name, logs_dir)
      logger.info(f'Rule application for subject {subject_name} completed successfully.')
    except Exception as err:
      logger.error(f'Error occurred while processing subject {subject_name}: {err}')
      continue


def get_args():
  parser = argparse.ArgumentParser(description='Run various experiments with data from PiREL.')
  parser.add_argument('--experiment', metavar='N',
                      help='ID of the experiment to run (int)',
                      type=int, required=True)
  parser.add_argument('--bench_idx_fpath', metavar='PATH',
                      help='Path to a benchmark index file (CSV).',
                      required=True)
  parser.add_argument('--shared_logs_dir', metavar='PATH',
                      help='Path to directory containing all PiREL logs.',
                      required=True)
  parser.add_argument('--output_dir', metavar='PATH',
                      help='Path to output directory.',
                      required=False, default=e_consts.RESULTS_DIR)
  parser.add_argument('--tag', metavar='STR',
                      help='Tag to append to output directory name.',
                      required=False, type=str, default='')
  parser.add_argument('--serialized_ruleset_union_fpath', metavar='PATH',
                      help='Path to a JSON file containing the union of all rulesets. '
                           'If provided, this will be used instead of loading the rulesets '
                           'from shared_logs_dir.',
                      required=False, type=str, default='')
  parser.add_argument('--email_notify',
                      help='Whether to send a notification when the experiment is done.',
                      action='store_true', default=False)

  args = parser.parse_args()

  args.bench_idx_fpath = e_common.normalize_path(args.bench_idx_fpath)
  assert args.bench_idx_fpath.exists()
  assert args.bench_idx_fpath.suffix == '.csv'

  args.shared_logs_dir = e_common.normalize_path(args.shared_logs_dir)
  assert args.shared_logs_dir.exists()
  assert args.shared_logs_dir.is_dir()

  args.output_dir = e_common.normalize_path(args.output_dir)
  assert args.output_dir.exists()
  assert args.output_dir.is_dir()

  if args.tag.strip() == '':
    args.tag = args.bench_idx_fpath.stem
  args.tag = args.tag.strip().replace(' ', '_')

  if args.serialized_ruleset_union_fpath:
    args.serialized_ruleset_union_fpath = e_common.normalize_path(args.serialized_ruleset_union_fpath)
    assert args.serialized_ruleset_union_fpath.exists()
    assert args.serialized_ruleset_union_fpath.is_file()
    assert args.serialized_ruleset_union_fpath.suffix == '.json'

  return args


EXPERIMENTS = {
  1: e01_table_gfg_rule_application_runtime_no_union,
  2: e02_table_gfg_rule_application_runtime_union,
  3: e03_rq1_gfg_subtree_trans_success_rate,
  4: e04_rq2_gfg_rule_extractability,
  5: e05_rq3_gfg_rule_reusability,
  6: e06_check_ruleset_integrity,
  7: e07_check_rule_app_reproducability,
}


def main():
  args = get_args()
  assert args.experiment in EXPERIMENTS, f'Invalid experiment ID: {args.experiment}'
  EXPERIMENTS[args.experiment](args)
  if args.email_notify:
    p_utils.email_safely(f'Experiment {args.experiment} done')


if __name__ == '__main__':
  main()
