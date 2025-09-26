from typing import List


class Config:
  benchmark_name: str = None
  src_lang: str = None
  tar_lang: str = None
  is_three_split: bool = None

  overriding_rulesets: List[str] = None

  max_concurrent_subjects: int = None
  reuse_translation_rules: bool = None

  sample_randomize: bool = None
  sample_size: int = None
  sample_start_idx: int = None
  sample_only: List[str] = None
  sample_exclude: List[str] = None

  is_email_report: bool = None

  sort_new_choices_in_reverse: bool = True


def load_configs(args):
  Config.benchmark_name = args.benchmark_name
  Config.src_lang = args.src_lang
  Config.tar_lang = args.tar_lang
  Config.is_three_split = args.is_three_split

  Config.overriding_rulesets = args.overriding_rulesets

  Config.max_concurrent_subjects = args.max_concurrent_subjects
  Config.reuse_translation_rules = args.reuse_translation_rules

  Config.sample_randomize = args.sample_randomize
  Config.sample_size = args.sample_size
  Config.sample_start_idx = args.sample_start_idx
  Config.sample_only = args.sample_only
  Config.sample_exclude = args.sample_exclude

  Config.is_email_report = args.is_email_report
