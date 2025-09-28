import asyncio
import p_consts
import p_pirel
import p_utils
import p_visitor as pv
import p_visitor_py as pvpy
from typing import List


def step1():
  STAT_TYPES = set()
  benchmarks_subject_fpaths = list(p_consts.GFG_BENCHMARK_DIR.glob("G*.py"))

  for i, fpath in enumerate(benchmarks_subject_fpaths, start=1):
    print(f"Processing {i}/{len(benchmarks_subject_fpaths)}: {fpath.name}")
    code = p_utils.read_text(fpath)
    test, main, call = code.split(p_consts.TEST_MAIN_CALL_DELIMITER)

    stat_nodes = asyncio.run(p_pirel._get_statement_nodes(main, 'py', True))
    for stat_node in stat_nodes:
      STAT_TYPES.add(stat_node.get_ts_node_type())

  p_utils.write_json('acollected.json', list(STAT_TYPES))


def step2():
  benchmarks_subject_fpaths = list(p_consts.GFG_BENCHMARK_DIR.glob("G*.py"))
  fout = open('astatements.log', 'w')

  for i, fpath in enumerate(benchmarks_subject_fpaths, start=1):
    print(f"Processing {i}/{len(benchmarks_subject_fpaths)}: {fpath.name}")
    code = p_utils.read_text(fpath)
    test, main, call = code.split(p_consts.TEST_MAIN_CALL_DELIMITER)

    stat_nodes = asyncio.run(p_pirel._get_statement_nodes(main, 'py', True))
    flag_found = False
    for stat_node in stat_nodes:
      if stat_node.get_ts_node_type() == 'import_from_statement':
        flag_found = True
    
    if flag_found:
      fout.write(str(fpath))
      fout.write('\n')
  
  fout.close()

step1()
# step2()