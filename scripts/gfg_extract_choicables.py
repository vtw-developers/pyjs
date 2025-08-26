import p_consts
import p_utils
import p_visitor as pv
import p_visitor_py as pvpy
from typing import List, Tuple


class ChoicablesExtractor(pv.Visitor):
  def __init__(self) -> None:
    super().__init__()
    self.choicables : List[str] = []
    self.pp = pvpy.PrettyPrinter(indent_with='    ')
  
  def add_choicable(self, node: pv.AbstractNode) -> None:
    global SIGNATURES_SAMPLES
    choicable_signature = self.get_signature(node)
    if choicable_signature in SIGNATURES_SAMPLES:
      return
    SIGNATURES_SAMPLES.append(choicable_signature)
    self.choicables.append(self.pp.visit(node))
    
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
  def visit_AssignmentNode(self, node: pv.AbstractNode) -> None:
    self.add_choicable(node)

  def visit_AugmentedAssignmentNode(self, node: pvpy.AugmentedAssignmentNode) -> None:
    self.add_choicable(node)
  
  def visit_WhileStatementNode(self, node: pvpy.WhileStatementNode) -> None:
    self.add_choicable(node.condition)
    self.visit(node.body)

  def visit_IfStatementNode(self, node: pvpy.IfStatementNode) -> None:
    self.add_choicable(node.condition)
    self.visit(node.consequence)
    for alt in node.alternatives:
      self.visit(alt)

  def visit_ElifClauseNode(self, node: pvpy.ElifClauseNode) -> None:
    self.add_choicable(node.condition)

  @classmethod
  def get_choicables_str(cls, main_code: str) -> List[str]:
    src_parser = p_consts.PARSER_DICT['py']
    ts_tree = src_parser.parse(bytes(main_code, 'utf-8'))
    tree = pvpy.Tree.from_ts_tree(ts_tree)
    extractor = cls()
    extractor.visit(tree.root_node)
    return extractor.choicables


SIGNATURES_SAMPLES = []
benchmarks_subject_fpaths = list(p_consts.GFG_BENCHMARK_DIR.glob("G*.py"))
fout = open('a_dump.txt', 'w')

for i, fpath in enumerate(benchmarks_subject_fpaths, start=1):
  print(f"Processing {i}/{len(benchmarks_subject_fpaths)}: {fpath.name}")
  code = p_utils.read_text(fpath)
  test, main, call = code.split(p_consts.TEST_MAIN_CALL_DELIMITER)

  choicables_str = ChoicablesExtractor.get_choicables_str(main)
  fout.write(f"File: {fpath}\n")
  for choicable in choicables_str:
    fout.write(f"{choicable}\n")

p_utils.write_json('a_signatures_samples.json', SIGNATURES_SAMPLES)

fout.close()
