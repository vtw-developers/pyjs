import p_consts
import p_utils
import p_visitor as pv
import p_visitor_py as pvpy
from typing import List


class AssignmentsCollector(pv.Visitor):
  def __init__(self) -> None:
    super().__init__()
    self.pp = pvpy.PrettyPrinter(indent_with='    ')
    self.assignments = []

  # VISIT METHODS
  def visit_AssignmentNode(self, node: pvpy.AssignmentNode) -> None:
    global ASSIGNMENTS
    assignment_signature = self.get_signature(node)
    if assignment_signature in ASSIGNMENTS:
      return
    ASSIGNMENTS.add(assignment_signature)
    unparsed = self.pp.visit(node)
    self.assignments.append(unparsed)
  
  def visit_AugmentedAssignmentNode(self, node: pvpy.AugmentedAssignmentNode) -> None:
    global ASSIGNMENTS
    assignment_signature = self.get_signature(node)
    if assignment_signature in ASSIGNMENTS:
      return
    ASSIGNMENTS.add(assignment_signature)
    unparsed = self.pp.visit(node)
    self.assignments.append(unparsed)

  def get_signature(self, node: pv.AbstractNode) -> str:
    '''
    Get the signature of the node.
    '''
    types = []
    def _rec_visit(node: pv.AbstractNode) -> str:
      nonlocal types
      if isinstance(node, pv.TerminalNode):
        types.append('term')
        return
      types.append(node.node_type)
      for child in node.get_children():
        _rec_visit(child)
    _rec_visit(node)
    return ' '.join(types)

  @classmethod
  def collect_assignments(cls, main_code: str) -> List[str]:
    src_parser = p_consts.PARSER_DICT['py']
    ts_tree = src_parser.parse(bytes(main_code, 'utf-8'))
    tree = pvpy.Tree.from_ts_tree(ts_tree)
    collector = cls()
    collector.visit(tree.root_node)
    return collector.assignments


ASSIGNMENTS = set()
benchmarks_subject_fpaths = list(p_consts.GFG_BENCHMARK_DIR.glob("G*.py"))
fout = open('adump.txt', 'w')

for i, fpath in enumerate(benchmarks_subject_fpaths, start=1):
  print(f"Processing {i}/{len(benchmarks_subject_fpaths)}: {fpath.name}")
  code = p_utils.read_text(fpath)
  test, main, call = code.split(p_consts.TEST_MAIN_CALL_DELIMITER)

  collected = AssignmentsCollector.collect_assignments(main)
  # fout.write(f"File: {fpath}\n")
  for elem in collected:
    fout.write(f"{elem}\n")

p_utils.write_json('asignatures_samples.json', list(ASSIGNMENTS))

fout.close()
