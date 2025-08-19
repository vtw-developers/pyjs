import p_consts
import p_utils
import p_visitor as pv
import p_visitor_py as pvpy
from typing import List, Tuple


class AssignmentStatementsExtractor(pv.Visitor):
  def __init__(self) -> None:
    super().__init__()
    self.assignment_statements : List[str] = []
    self.pp = pvpy.PrettyPrinter(indent_with='    ')

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

  # VISIT METHODS
  def visit_ExpressionStatementNode(self, node: pvpy.ExpressionStatementNode) -> None:
    children = node.get_children()
    if len(children) != 1:
      return
    child = children[0]
    if not isinstance(child, pvpy.AssignmentNode):
      return
    assignment_stat = self.pp.visit(child)
    self.assignment_statements.append(assignment_stat)
    signature = self.get_signature(node)
    if signature not in SIGNATURES_SAMPLES:
      SIGNATURES_SAMPLES[signature] = assignment_stat

  @classmethod
  def get_assignment_statements(cls, main_code: str) -> List[str]:
    src_parser = p_consts.PARSER_DICT['py']
    ts_tree = src_parser.parse(bytes(main_code, 'utf-8'))
    tree = pvpy.Tree.from_ts_tree(ts_tree)
    extractor = cls()
    extractor.visit(tree.root_node)
    return extractor.assignment_statements


SIGNATURES_SAMPLES = {}
benchmarks_subject_fpaths = list(p_consts.GFG_BENCHMARK_DIR.glob("G*.py"))
fout = open('dump.txt', 'w')

for i, fpath in enumerate(benchmarks_subject_fpaths, start=1):
  print(f"Processing {i}/{len(benchmarks_subject_fpaths)}: {fpath.name}")
  code = p_utils.read_text(fpath)
  test, main, call = code.split(p_consts.TEST_MAIN_CALL_DELIMITER)

  assignment_statements = AssignmentStatementsExtractor.get_assignment_statements(main)
  fout.write(f"File: {fpath}\n")
  for assign_stat in assignment_statements:
    fout.write(f"{assign_stat}\n")

p_utils.write_json('signatures_samples.json', SIGNATURES_SAMPLES)

fout.close()
