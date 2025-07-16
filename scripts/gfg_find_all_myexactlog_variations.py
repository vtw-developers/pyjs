import p_consts
import p_utils
import p_visitor as pv
import p_visitor_py as pvpy
from typing import List, Tuple


class LogStatementsExtractor(pv.Visitor):
  def __init__(self) -> None:
    super().__init__()
    self.log_statements : List[str] = []
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
  def visit_CallNode(self, node: pvpy.CallNode) -> None:
    '''
    Check if the call node is a log statement.
    If it is, add it to the list of log statements.
    '''
    global SIGNATURES_SAMPLES
    if not isinstance(node.function, pvpy.IdentifierNode):
      return
    if node.function.val() != 'myexactlog':
      return
    log_statement = self.pp.visit(node)
    self.log_statements.append(log_statement)
    signature = self.get_signature(node.arguments)
    if signature not in SIGNATURES_SAMPLES:
      SIGNATURES_SAMPLES[signature] = log_statement

  @classmethod
  def get_log_statements(cls, main_code: str) -> List[str]:
    src_parser = p_consts.PARSER_DICT['py']
    ts_tree = src_parser.parse(bytes(main_code, 'utf-8'))
    tree = pvpy.Tree.from_ts_tree(ts_tree)
    checker = cls()
    checker.visit(tree.root_node)
    return checker.log_statements


SIGNATURES_SAMPLES = {}
benchmarks_subject_fpaths = list(p_consts.GFG_BENCHMARK_DIR.glob("G*.py"))
fout = open('dump.txt', 'w')

for i, fpath in enumerate(benchmarks_subject_fpaths, start=1):
  print(f"Processing {i}/{len(benchmarks_subject_fpaths)}: {fpath.name}")
  code = p_utils.read_text(fpath)
  test, main, call = code.split(p_consts.TEST_MAIN_CALL_DELIMITER)

  main = pvpy.LogStatementInserter.insert_log_statements(main)
  main = pvpy.LogStatementsIndexer.index_log_statements(main)

  log_statements = LogStatementsExtractor.get_log_statements(main)
  fout.write(f"File: {fpath}\n")
  for log_statement in log_statements:
    fout.write(f"{log_statement}\n")

p_utils.write_json('signatures_samples.json', SIGNATURES_SAMPLES)

fout.close()
