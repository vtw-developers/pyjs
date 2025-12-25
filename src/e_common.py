import asyncio
import csv
import random
import yaml
from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path

import p_consts
import p_learn_apply_rules
import p_rule_applicator as prapp
import p_rule_validator
import p_ruleset
import p_subject
import p_tree_log as ptlog
import p_utils


logger = p_utils.setup_logger(__name__, p_consts.EXPERIMENTS_DIR / 'e_common.log')


# UTILITIES
def generate_random_float_matrix(
  rows=4,
  cols=699,
  lower_bound=0.0,
  upper_bound=1.0
) -> List[List[float]]:
  '''
  Generate a 2D list of random float data for testing purposes.
  '''
  data = [
    [random.uniform(lower_bound, upper_bound) for _ in range(cols)]
    for _ in range(rows)
  ]
  return data


def normalize_path(path: Union[str, Path]) -> Path:
  '''
  PRE: path is either relative to ROOT_DIR or absolute.
  POST: path is absolute.
  '''
  if isinstance(path, str):
    path = Path(path)
  if not path.is_absolute():
    path = p_consts.ROOT_DIR / path
  return path.expanduser().resolve()


# OBTAINING PATHS TO THE FILES IN THE LOGS DIRECTORY
def _get_sbj_logged_path(
  subject_name: str,
  suffix: str,
  logs_dir: Path,
) -> Optional[Path]:
  '''
  Returns the path to "{subject_name}{suffix}" file in logs_dir.
  '''
  log_fpaths = list(logs_dir.glob(f'{subject_name}{suffix}'))
  if len(log_fpaths) == 0:
    return None
  assert len(log_fpaths) == 1, f'Multiple {subject_name}{suffix} files found in {logs_dir}'
  return log_fpaths[0]


def get_path_log(subject_name: str, logs_dir: Path) -> Optional[Path]:
  return _get_sbj_logged_path(subject_name, '.log', logs_dir)


def get_path_lea_rul(subject_name: str, logs_dir: Path) -> Optional[Path]:
  return _get_sbj_logged_path(subject_name, '_learned_rules.json', logs_dir)


def get_path_val_rul(subject_name: str, logs_dir: Path) -> Optional[Path]:
  return _get_sbj_logged_path(subject_name, '_validated_rules.json', logs_dir)


def get_path_lea_suc_yaml(subject_name: str, logs_dir: Path) -> Optional[Path]:
  return _get_sbj_logged_path(subject_name, '_tree_log_learn_phase_success.yaml', logs_dir)


def get_path_app_suc_yaml(subject_name: str, logs_dir: Path) -> Optional[Path]:
  return _get_sbj_logged_path(subject_name, '_tree_log_apply_phase_success.yaml', logs_dir)


def get_path_lea_fai_yaml(subject_name: str, logs_dir: Path) -> Optional[Path]:
  return _get_sbj_logged_path(subject_name, '_tree_log_learn_phase_fail.yaml', logs_dir)


def get_path_app_fai_yaml(subject_name: str, logs_dir: Path) -> Optional[Path]:
  return _get_sbj_logged_path(subject_name, '_tree_log_apply_phase_fail.yaml', logs_dir)


def get_path_yaml(subject_name: str, logs_dir: Path) -> Optional[Path]:
  '''
  Returns the path to the YAML log file from which the
  subject's hierarchical log data can be loaded.

  YAML log files are saved by p_learn_apply_rules incrementally.
  The default save location is p_consts.LEARN_RULES_LOGS_DIR.
  Check p_learn_apply_rules.py for details.

  Learn phase: (contains only learn phase logs)
  1. if success: {subject_name}_tree_log_learn_phase_success.yaml
  2. if    fail: {subject_name}_tree_log_learn_phase_fail.yaml

  Apply phase: (contains both learn and apply phase logs)
  1. if success: {subject_name}_tree_log_apply_phase_success.yaml
  2. if    fail: {subject_name}_tree_log_apply_phase_fail.yaml
  '''

  app_suc = get_path_app_suc_yaml(subject_name, logs_dir)
  app_fai = get_path_app_fai_yaml(subject_name, logs_dir)
  lea_suc = get_path_lea_suc_yaml(subject_name, logs_dir)
  lea_fai = get_path_lea_fai_yaml(subject_name, logs_dir)

  # Ensure exactly one of the two is not None (XOR logic)
  if app_suc is not None or app_fai is not None:
    assert (app_suc is None) != (app_fai is None), 'apply phase: success XOR fail expected'
    return app_suc if app_suc is not None else app_fai
  elif lea_suc is not None or lea_fai is not None:
    assert (lea_suc is None) != (lea_fai is None), 'learn phase: success XOR fail expected'
    return lea_suc if lea_suc is not None else lea_fai
  else:
    return None


# LOADING FILES FROM THE LOGS DIRECTORY
def load_subject_from_yaml(subject_log_fpath: Path) -> ptlog.Subject:
  '''
  Loads a YAML file containing the log data for a subject.
  '''
  assert subject_log_fpath is not None, 'subject_log_fpath should not be None'
  assert subject_log_fpath.exists(), f'subject_log_fpath does not exist: {subject_log_fpath}'
  assert subject_log_fpath.suffix == '.yaml', 'subject_log_fpath should be a .yaml file'
  yaml_text = p_utils.read_text(subject_log_fpath)
  yaml_obj = yaml.safe_load(yaml_text)
  lsubject = ptlog.Subject.from_dict(yaml_obj)
  return lsubject


def load_val_ruleset_serialized(subject_name: str, logs_dir: Path) -> dict:
  '''
  Returns the ruleset as a dict from the log dir.
  Serialized ruleset is saved by p_learn_apply_rules as
  {subject_name}_validated_rules.json and {subject_name}_learned_rules.json.
  '''
  path = get_path_val_rul(subject_name, logs_dir)
  assert path is not None, f'{subject_name}_validated_rules.json not found in {logs_dir}'
  ruleset_serialized = p_utils.read_json(path)
  return ruleset_serialized


def load_val_ruleset(subject_name: str, logs_dir: Path) -> p_ruleset.Ruleset:
  '''
  Returns the ruleset object from the log dir.
  Serialized ruleset is saved by p_learn_apply_rules as
  {subject_name}_validated_rules.json and {subject_name}_learned_rules.json.
  '''
  ruleset_serialized = load_val_ruleset_serialized(subject_name, logs_dir)
  ruleset = p_ruleset.Ruleset.from_dict(ruleset_serialized)
  return ruleset


def load_rulesets_union(
  subject_names: List[str],
  logs_dir: Path,
) -> p_ruleset.Ruleset:
  '''
  Returns a ruleset object that contains a UNION of all rulesets
  learned from the subjects in subject_names.
  PRE len(subject_names) > 0
  PRE application phase is successful for all subjects in subject_names
  '''
  assert len(subject_names) > 0, 'subject_names should not be empty'
  assert logs_dir.exists(), f'logs_dir does not exist: {logs_dir}'

  # bootstrap by loading the first subject's ruleset
  ruleset_serialized = load_val_ruleset_serialized(subject_names[0], logs_dir)
  ruleset = p_ruleset.Ruleset.from_dict(ruleset_serialized)

  for idx, subject_name in enumerate(subject_names[1:], start=2):
    subject_ruleset_serialized = load_val_ruleset_serialized(subject_name, logs_dir)
    subject_ruleset = p_ruleset.Ruleset.from_dict(subject_ruleset_serialized)
    ruleset.extend(subject_ruleset)  # NOTE expensive call

  return ruleset


def load_val_rulesets_union(
  benchmark_index: Dict[str, dict],
  shared_logs_dir: Path,
) -> p_ruleset.Ruleset:
  '''
  Returns a ruleset object that contains a UNION of all rulesets
  learned from the subjects scattered across multiple logs dirs.
  PRE application phase is successful for all subjects in subject_names
  '''
  assert len(benchmark_index) > 0, 'gfg_index should not be empty'
  for k, v in benchmark_index.items():
    assert v['success'] is True, f'subject {k} does not have success=True'
    assert v['logs_tag'] is not None, f'subject {k} does not have a logs_tag'
  assert shared_logs_dir.exists(), f'shared_logs_dir does not exist: {shared_logs_dir}'
  assert shared_logs_dir.is_dir(), f'shared_logs_dir is not a directory: {shared_logs_dir}'

  # bootstrap by loading the first subject's ruleset
  subject_names = sorted(benchmark_index.keys())
  s1_name = subject_names[0]
  s1_logs_dir = shared_logs_dir / benchmark_index[s1_name]['logs_tag'] / 'logs' / 'learn-rules'
  ruleset_serialized = load_val_ruleset_serialized(s1_name, s1_logs_dir)
  ruleset = p_ruleset.Ruleset.from_dict(ruleset_serialized)

  for idx, subject_name in enumerate(subject_names[1:], start=2):
    logger.debug(f'Loading ruleset for subject {idx}/{len(subject_names)}: {subject_name}')
    subject_logs_dir = shared_logs_dir / benchmark_index[subject_name]['logs_tag'] / 'logs' / 'learn-rules'
    subject_ruleset_serialized = load_val_ruleset_serialized(subject_name, subject_logs_dir)
    subject_ruleset = p_ruleset.Ruleset.from_dict(subject_ruleset_serialized)
    ruleset.extend(subject_ruleset)

  return ruleset


# OTHER LOADING
def get_subject_src_from_bench_dir(subject_name: str, benchmark_name: str) -> str:
  if benchmark_name == 'gfg':
    subject_fpaths = list(p_consts.GFG_BENCHMARK_DIR.glob(f'{subject_name}_*.py'))
    assert len(subject_fpaths) == 1, f'Expected exactly one file for subject {subject_name}'
    return p_utils.read_text(subject_fpaths[0])
  raise NotImplementedError(f'{benchmark_name} is not supported')


def load_subject_names(subject_names_fpath: Path) -> List[str]:
  '''
  Retrieves subject names from file.
  '''
  assert isinstance(subject_names_fpath, Path)
  assert subject_names_fpath.is_absolute()
  assert subject_names_fpath.exists()
  with open(subject_names_fpath, 'r') as f:
    subject_names = [line.strip() for line in f if line.strip()]
    return subject_names


def load_benchmark_index(
  bench_idx_fpath: Path,
  filter_value_success: list
) -> Dict[str, dict]:
  '''
  Loads the index CSV as a dict from a hard-coded path.
  An index is a table with the following headers:
  SUBJECT_NAME, SUCCESS, LOGS_TAG
  The index is a copy of Google Spreadsheet data exported as CSV.
  '''
  logger.debug(f'Loading benchmark index from {bench_idx_fpath}')

  assert bench_idx_fpath.exists(), f'Index file not found: {bench_idx_fpath}'
  assert bench_idx_fpath.is_file(), f'Index path is not a file: {bench_idx_fpath}'
  assert bench_idx_fpath.suffix == '.csv', 'Index file must be a CSV file'
  assert all(v in [True, False, None] for v in filter_value_success), 'filter_value_success must contain only True, False, or None'

  reader = csv.reader(open(bench_idx_fpath, 'r'))
  headers = next(reader)
  assert len(set(headers)) == len(headers), 'Duplicate column names in CSV file'
  assert headers[0] == 'SUBJECT_NAME', 'First column must be SUBJECT_NAME'
  assert headers[1] == 'SUCCESS', 'Second column must be SUCCESS'
  assert headers[2] == 'LOGS_TAG', 'Third column must be LOGS_TAG'

  data = dict()
  for row in reader:
    assert len(row) == len(headers), 'Row length does not match header length'
    assert row[0] != '', 'SUBJECT_NAME cannot be empty'
    assert row[1] in ['TRUE', 'FALSE', ''], 'SUCCESS must be TRUE, FALSE, or empty'

    subject_name = row[0]
    success = True if row[1] == 'TRUE' else False if row[1] == 'FALSE' else None
    logs_tag = row[2]
    if logs_tag == '':
      logs_tag = None

    # filtering
    if success not in filter_value_success:
      logger.debug(f'Skipping subject {subject_name} with success={success}')
      continue

    subject_dict = {'success': success, 'logs_tag': logs_tag}
    assert subject_name not in data, 'duplicate entry detected'
    data[subject_name] = subject_dict

  logger.debug(f'Loaded {len(data)} entries from benchmark index')
  return data


# OTHER API
def run_rule_app_single_gfg_own_rules(
  subject_name: str,
  logs_dir: Path
) -> Tuple[int, List[p_ruleset.TRuleBase], str]:
  '''
  Runs rule application for a specific GFG subject with rules
  that were learned and validated from the same subject.

  RETURN
  - time taken in msec
  - list of rules used
  - plausible target program
  '''
  src_program = get_subject_src_from_bench_dir(subject_name, 'gfg')
  subject = p_subject.PirelSubject('gfg', subject_name, src_program, 'py', 'js', True)
  ruleset = load_val_ruleset(subject_name, logs_dir)
  apply_subject = p_learn_apply_rules._create_subject_for_apply_phase(subject, ruleset)

  stms = p_utils.current_time_msec()
  tar_program_plausible, translate_dbg_history = \
    asyncio.run(prapp.apply_translation_rules(apply_subject))
  etms = p_utils.current_time_msec()

  used_rule_ids = p_rule_validator.get_used_translation_rule_ids(translate_dbg_history)
  # `if rid < len(ruleset.rules)` is needed because we append a rule to handle
  # log statements in _create_subject_for_apply_phase()
  used_rules = [ruleset.get_rule_by_idx(rid) for rid in used_rule_ids if rid < len(ruleset.rules)]
  return (etms - stms), used_rules, tar_program_plausible


# TEST HARNESSES
def _test_run_rule_app_single_gfg_own_rules():
  '''
  def run_rule_app_single_gfg_own_rules(
    subject_name: str,
    logs_dir: Path
  ) -> Tuple[int, List[p_ruleset.TRuleBase], str]:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_run_rule_app_single_gfg_own_rules.yaml'
  config = p_utils.read_yaml(config_fpath)

  subject_name = config['subject_name']
  logs_dir = Path(config['logs_dir'])

  rt, rules, tarprog = run_rule_app_single_gfg_own_rules(subject_name, logs_dir)
  print(f'Time taken: {rt} msec')
  print(f'Num rules used: {len(rules)}')
  for r in rules:
    print(f'  Rule: {r.to_rule_str()}')
  print(f'Plausible target program: {tarprog}')


if __name__ == '__main__':
  _test_run_rule_app_single_gfg_own_rules()
