import asyncio
import json
import p_consts
import p_utils
import p_ruleset
import p_ext_rule_chooser


def _test_get_proposed_choices_compile_error():
  '''
  def get_proposed_choices_compile_error(
    tar_program_instr: str,
    tar_main_code: str,
    tar_error_dict: dict,
    choices_list_history: list,
    map_to_exid: Dict[int, List[dict]],
    translate_dbg_history: List[dict],
    verified_choice_options: List[Tuple[Tuple[int, int, int], List[int]]] = [],
    raise_on_missing_vrf_rule: bool = False,
  ) -> dict:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_get_proposed_choices_compile_error_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  tar_program_instr = args_dict['tar_program_instr']
  tar_main_code = args_dict['tar_main_code']
  tar_error_dict = args_dict['tar_error_dict']
  choices_list_history = args_dict['choices_list_history']
  for choices_list in choices_list_history:
    for i in range(len(choices_list)):
      elem = choices_list[i]
      choices_list[i] = tuple(elem[0]), elem[1]
  map_to_exid = args_dict['map_to_exid']
  map_to_exid = {int(k): v for k, v in map_to_exid.items()}  # ensure keys are int
  translate_dbg_history = args_dict['translate_dbg_history']
  for elem in translate_dbg_history:
    elem['range_info'] = tuple(elem['range_info']) if elem['range_info'] is not None else None
  verified_choice_options = args_dict['verified_choice_options']
  verified_choice_options = [(tuple(a[0]), a[1]) for a in verified_choice_options]
  raise_on_missing_vrf_rule = args_dict['raise_on_missing_vrf_rule']

  new_choices = p_ext_rule_chooser.get_proposed_choices_compile_error(
    tar_program_instr,
    tar_main_code,
    tar_error_dict,
    choices_list_history,
    map_to_exid,
    translate_dbg_history,
    verified_choice_options,
    raise_on_missing_vrf_rule,
  )
  print(f'New choices: {json.dumps(new_choices, indent=2)}')
  p_utils.write_tmp_json('new_choices.json', new_choices)


def _test_get_proposed_choices_semantic_error():
  '''
  def get_proposed_choices_semantic_error(
    tar_program_instr: str,
    tar_main_code: str,
    error_lines: dict,
    choices_list_history: list,
    map_to_exid: Dict[int, List[dict]],
    translate_dbg_history: List[dict],
    verified_choice_options: List[Tuple[Tuple[int, int, int], List[int]]] = [],
    raise_on_missing_vrf_rule: bool = False,
  ) -> dict:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_get_proposed_choices_semantic_error_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  tar_program_instr = args_dict['tar_program_instr']
  tar_main_code = args_dict['tar_main_code']
  error_lines = args_dict['error_lines']
  error_lines = {int(k): v for k, v in error_lines.items()}  # ensure keys are int
  choices_list_history = args_dict['choices_list_history']
  for choices_list in choices_list_history:
    for i in range(len(choices_list)):
      elem = choices_list[i]
      choices_list[i] = tuple(elem[0]), elem[1]
  map_to_exid = args_dict['map_to_exid']
  map_to_exid = {int(k): v for k, v in map_to_exid.items()}  # ensure keys are int
  translate_dbg_history = args_dict['translate_dbg_history']
  for elem in translate_dbg_history:
    elem['range_info'] = tuple(elem['range_info']) if elem['range_info'] is not None else None
  verified_choice_options = args_dict['verified_choice_options']
  verified_choice_options = [(tuple(a[0]), a[1]) for a in verified_choice_options]
  raise_on_missing_vrf_rule = args_dict['raise_on_missing_vrf_rule']

  new_choices = p_ext_rule_chooser.get_proposed_choices_semantic_error(
    tar_program_instr,
    tar_main_code,
    error_lines,
    choices_list_history,
    map_to_exid,
    translate_dbg_history,
    verified_choice_options,
    raise_on_missing_vrf_rule
  )
  print(f'New choices: {json.dumps(new_choices, indent=2)}')
  p_utils.write_tmp_json('new_choices.json', new_choices)


def _test_stat_node_validate_exprs():
  '''
  async def stat_node_validate_exprs(
    src_main_code: str,
    src_test_code: str,
    translation_rules_test_code: str,
    ruleset: p_ruleset.Ruleset,
    simple_ntext: str,
    subject_name: str
  ) -> list:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_stat_node_validate_exprs_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  src_main_code = args_dict['src_main_code']
  src_test_code = args_dict['src_test_code']
  translation_rules_test_code = args_dict['translation_rules_test_code']
  ruleset = p_ruleset.Ruleset.from_dict(args_dict['ruleset'])
  simple_ntext = args_dict['simple_ntext']
  subject_name = args_dict['subject_name']

  asyncio.run(p_ext_rule_chooser.stat_node_validate_exprs(
    src_main_code,
    src_test_code,
    translation_rules_test_code,
    ruleset,
    simple_ntext,
    subject_name
  ))
  verified_choice_options = ruleset.get_choice_options_from_verified_rules(src_main_code)

  print(f'Readonly choices list: {json.dumps(verified_choice_options, indent=2)}')


if __name__ == '__main__':
  # _test_get_proposed_choices_compile_error()
  # _test_get_proposed_choices_semantic_error()
  _test_stat_node_validate_exprs()
