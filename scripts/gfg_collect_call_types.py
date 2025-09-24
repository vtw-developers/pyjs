import p_consts
import p_utils
import p_visitor as pv
import p_visitor_py as pvpy
from typing import List


class CallFnTypeCollector(pv.Visitor):
  def __init__(self) -> None:
    super().__init__()
    self.pp = pvpy.PrettyPrinter(indent_with='    ')
    self.call_fn_types = []

  # VISIT METHODS
  def visit_CallNode(self, node: pvpy.CallNode) -> None:
    global CALL_FN_TYPES
    fn_str = self.pp.visit(node.function)
    CALL_FN_TYPES.add(fn_str)
    # CALL_FN_TYPES.add(node.function.__class__.__name__)

  @classmethod
  def collect_call_fn_types(cls, main_code: str) -> List[str]:
    src_parser = p_consts.PARSER_DICT['py']
    ts_tree = src_parser.parse(bytes(main_code, 'utf-8'))
    tree = pvpy.Tree.from_ts_tree(ts_tree)
    collector = cls()
    collector.visit(tree.root_node)
    return collector.call_fn_types


CALL_FN_TYPES = set()
benchmarks_subject_fpaths = list(p_consts.GFG_BENCHMARK_DIR.glob("G*.py"))
fout = open('adump.txt', 'w')

for i, fpath in enumerate(benchmarks_subject_fpaths, start=1):
  # print(f"Processing {i}/{len(benchmarks_subject_fpaths)}: {fpath.name}")
  code = p_utils.read_text(fpath)
  test, main, call = code.split(p_consts.TEST_MAIN_CALL_DELIMITER)

  collected = CallFnTypeCollector.collect_call_fn_types(main)
  fout.write(f"File: {fpath}\n")
  for elem in collected:
    fout.write(f"{elem}\n")

p_utils.write_json('asignatures_samples.json', list(CALL_FN_TYPES))

fout.close()
