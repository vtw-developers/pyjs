import random
import yaml
from typing import List, Optional, Union
from pathlib import Path

import p_consts
import p_ruleset
import p_tree_log as ptlog
import p_utils


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


def read_validated_rules(subject_name: str, logs_dir: Path) -> dict:
  '''
  Returns the ruleset as a dict from the log dir.
  Serialized ruleset is saved by p_learn_apply_rules as
  {subject_name}_validated_rules.json and {subject_name}_learned_rules.json.
  '''
  path = get_path_val_rul(subject_name, logs_dir)
  assert path is not None, f'{subject_name}_validated_rules.json not found in {logs_dir}'
  ruleset_serialized = p_utils.read_json(path)
  return ruleset_serialized


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
  ruleset_serialized = read_validated_rules(subject_names[0], logs_dir)
  ruleset = p_ruleset.Ruleset.from_dict(ruleset_serialized)

  for idx, subject_name in enumerate(subject_names[1:], start=2):
    subject_ruleset_serialized = read_validated_rules(subject_name, logs_dir)
    subject_ruleset = p_ruleset.Ruleset.from_dict(subject_ruleset_serialized)
    ruleset.extend(subject_ruleset)  # NOTE expensive call

  return ruleset


# OTHER LOADING
def get_subject_src_from_bench_dir(subject_name: str, benchmark_name: str) -> str:
  if benchmark_name == 'gfg':
    subject_fpaths = list(p_consts.GFG_BENCHMARK_DIR.glob(f'{subject_name}_*.py'))
    assert len(subject_fpaths) == 1, f'Expected exactly one file for subject {subject_name}'
    return p_utils.read_text(subject_fpaths[0])
  raise NotImplementedError(f'{benchmark_name} is not supported')
