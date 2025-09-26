'''
This script was used for analyzing 
_create_src_main_code_for_val() and get_pre_context() in p_pirel.py.
It helped to test new functions _instrument_with_break_statements()
and _rfind_statement_nid_by_text() in p_pirel.py.
'''


import random

import p_consts
import p_pirel
import p_utils
import p_visitor_py as pvpy


logger = p_utils.setup_logger(__name__)


def get_num_lines(text: str) -> int:
  return len(text.splitlines())


def find_text_in_text(statement: str, src_main_code: str) -> int:
  lines = src_main_code.splitlines()
  statement_lines = statement.splitlines()
  lines = [line.strip() for line in lines]
  statement_lines = [line.strip() for line in statement_lines]
  for i in range(len(lines) - len(statement_lines) + 1):
    if lines[i:i + len(statement_lines)] == statement_lines:
      return i + 1

  print(statement)
  print('---')
  print(src_main_code)
  raise ValueError(f'Cannot find statement in src_main_code')


def step_1_gather_stats() -> dict:
  global PATHS
  stats = dict()
  for idx, path in enumerate(PATHS):
    print(f'Processing {idx+1}/{len(PATHS)}: {path}')
    args_dict = p_utils.read_json(path)
    src_main_code = args_dict['src_main_code']
    lang = args_dict['lang']
    is_three_split = args_dict['is_three_split']
    stat_nid = args_dict['stat_nid']

    _tree = pvpy.Tree.from_str(src_main_code)
    _nid_node_map = _tree.root_node.get_nid_node_map()
    stat_node = _nid_node_map[stat_nid]

    pp = pvpy.PrettyPrinter(indent_with='    ')
    pp.visit(stat_node)

    statement = '\n'.join(pp.lines)
    pre_context = p_pirel.get_pre_context(src_main_code, lang, is_three_split, stat_nid, [])
    src_main_code_val = p_pirel._create_src_main_code_for_val(
      src_main_code, pre_context, statement, is_three_split)

    nl_statement = get_num_lines(statement)
    nl_src_main_code = get_num_lines(src_main_code_val)
    idx_statement_in_src_main_code = find_text_in_text(statement, src_main_code_val)

    stats.setdefault(nl_statement, {}).setdefault(nl_src_main_code, {}).setdefault(
      idx_statement_in_src_main_code, []).append(
        (src_main_code_val, statement)
      )

  return stats


def step_2_work_with_stats(stats: dict):
  save_dir = p_consts.TEST_ARTIFACTS_DIR / 'p-pirel' / 'rfind-stat-node-by-text'
  counter = 2
  nl_statements = sorted(stats.keys())
  for nl_statement in nl_statements:
    nl_src_main_codes = sorted(stats[nl_statement].keys())
    for nl_src_main_code in nl_src_main_codes:
      idx_statement_in_src_main_codes = sorted(stats[nl_statement][nl_src_main_code].keys())
      for idx_statement_in_src_main_code in idx_statement_in_src_main_codes:
        entries = stats[nl_statement][nl_src_main_code][idx_statement_in_src_main_code]
        entries = [tuple(entry) for entry in entries]
        entries = list(set(entries))
        entry = random.choice(entries)
        src_main_code_val, statement = entry

        fid = f'{counter:03}'
        p_utils.write_text(save_dir / f'{fid}_in.py', src_main_code_val)
        p_utils.write_text(save_dir / f'{fid}_statement.py', statement)
        counter += 1

        # print(nl_statement, nl_src_main_code, idx_statement_in_src_main_code)
        # print('---')
        # print(src_main_code_val)
        # print('---')
        # print(statement)
        # print('---')
        # input()

        continue


PATHS = p_utils.read_text('apaths.txt').splitlines()

# stats = step_1_gather_stats()
# p_utils.write_json('astats.json', stats)

# stats = p_utils.read_json('astats.json')
# step_2_work_with_stats(stats)
