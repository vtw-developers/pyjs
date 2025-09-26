import p_consts
import p_utils
import p_visitor as pv
import p_visitor_py as pvpy
from typing import List


class RecCallFnTypeCollector(pv.Visitor):
  def __init__(self, subject_name: str) -> None:
    super().__init__()
    self.pp = pvpy.PrettyPrinter(indent_with='    ')
    self.rec_call_fn_types = []
    self.subject_name = subject_name

  # VISIT METHODS
  def visit_CallNode(self, node: pvpy.CallNode) -> None:
    global REC_CALL_FN_TYPES
    if not isinstance(node.function, pvpy.IdentifierNode):
      return
    if node.function.val() != 'f_gold':
      return
    rec_fn_str = self.pp.visit(node)
    # REC_CALL_FN_TYPES.append((self.subject_name, rec_fn_str))
    REC_CALL_FN_TYPES.setdefault(self.subject_name, []).append(rec_fn_str)

  @classmethod
  def collect_rec_call_fn_types(cls, main_code: str, subject_name: str) -> List[str]:
    src_parser = p_consts.PARSER_DICT['py']
    ts_tree = src_parser.parse(bytes(main_code, 'utf-8'))
    tree = pvpy.Tree.from_ts_tree(ts_tree)
    collector = cls(subject_name)
    collector.visit(tree.root_node)
    return collector.rec_call_fn_types


REC_CALL_FN_TYPES = dict()
benchmarks_subject_fpaths = list(p_consts.GFG_BENCHMARK_DIR.glob("G*.py"))
fout = open('adump.txt', 'w')

for i, fpath in enumerate(benchmarks_subject_fpaths, start=1):
  # print(f"Processing {i}/{len(benchmarks_subject_fpaths)}: {fpath.name}")
  subject_name = fpath.stem[:5]
  code = p_utils.read_text(fpath)
  test, main, call = code.split(p_consts.TEST_MAIN_CALL_DELIMITER)

  collected = RecCallFnTypeCollector.collect_rec_call_fn_types(main, subject_name)
  fout.write(f"File: {fpath}\n")
  for elem in collected:
    fout.write(f"{elem}\n")

p_utils.write_json('asignatures_samples.json', REC_CALL_FN_TYPES)

fout.close()
