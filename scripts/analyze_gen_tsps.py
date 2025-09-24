from pathlib import Path
from itertools import chain
from typing import Dict, Tuple, List
import os
import p_consts
import p_utils
import p_data_structures as pds


def _get_type_ahu_ter_x_ident_lit_encoding(
  tree: pds.DuoGlotTree
) -> str:
  '''
  modified from p_llm_val.py
  '''
  def __rec_post_order(node: pds.DuoGlotNode):
    # base case (terminal node)
    if node.is_terminal():
      return node.get_type()
    # base case: non-terminal with a single terminal child
    if len(node.get_children()) == 1 and node.get_children()[0].is_terminal():
      return f'({node.get_type()} 0)'
    children_encoding = ''
    for child in node.get_children():
      children_encoding += __rec_post_order(child) + ' '
    children_encoding = children_encoding.strip()
    return f'({node.get_type()} {children_encoding})'
  encoding = __rec_post_order(tree.get_root_node())
  return encoding


def step1():
  '''
  grep from logs:
  paths = [
    ["G0010", "/root/pirel-shared-volume/logs-archive/debug-48/logs/pirel/9/20/3/35/15/201157-TSPs-generated.json"],
    ...
  ]
  '''
  paths = p_utils.read_json('apaths.json')
  enc_dict : Dict[str, List[Tuple[str, str, Path]]] = dict()
  for idx, (subject_name, fpath) in enumerate(paths, start=1):
    print(f'[{idx}/{len(paths)}] Processing {subject_name} - {fpath}')
    tsps = p_utils.read_json(fpath)
    snippets = chain.from_iterable(tsps)
    for snippet in snippets:
      tree = pds.DuoGlotTree.from_code_str(snippet, 'py')
      enc = _get_type_ahu_ter_x_ident_lit_encoding(tree)
      enc_dict.setdefault(enc, []).append((snippet, subject_name, fpath))

  # save
  p_utils.write_json('analyze_gen_tsps_step1.json', enc_dict)


def step2():
  '''
  manually inspect the output of step1, and identify some interesting encodings
  '''
  enc_dict : Dict[str, List[Tuple[str, str, Path]]] = p_utils.read_json('analyze_gen_tsps_step1.json')
  gfpath = Path('analyze_gen_tsps_step2_good.json')
  bfpath = Path('analyze_gen_tsps_step2_bad.json')
  gfpath.touch(exist_ok=True)
  bfpath.touch(exist_ok=True)
  good_enc_dict : Dict[str, List[Tuple[str, str, Path]]] = p_utils.read_json(gfpath)
  bad_enc_dict : Dict[str, List[Tuple[str, str, Path]]] = p_utils.read_json(bfpath)

  for idx, (enc, vals) in enumerate(enc_dict.items()):
    if enc in good_enc_dict or enc in bad_enc_dict:
      continue  # already processed
    os.system('clear')
    print(f'[{idx}/{len(enc_dict)}] Encoding: {enc[:30]}, Count: {len(vals)}\n\n\n\n\n')
    for snippet, subject_name, fpath in vals[:1]:  # show up to 5 examples
      print(f'{snippet}')
      # print('---')
    decision = input('\n\n\n\n\nIs this encoding good (g) or bad (b)? (g/b): ').strip().lower()
    if decision == 'g':
      good_enc_dict.setdefault(enc, []).append((snippet, subject_name, fpath))
    elif decision == 'b':
      bad_enc_dict.setdefault(enc, []).append((snippet, subject_name, fpath))

    # save
    p_utils.write_json('analyze_gen_tsps_step2_good.json', good_enc_dict)
    p_utils.write_json('analyze_gen_tsps_step2_bad.json', bad_enc_dict)


# step1()
step2()
