import unittest
from pathlib import Path

import p_consts
import p_utils
import p_visitor_py


class TestParametrizableVariablesCollector(unittest.TestCase):
  def setUp(self):
    self.snippets_dir = p_consts.TEST_ARTIFACTS_DIR / 'p-visitor-py-test'
    self.src_lang = 'py'
    self.parser = p_consts.PARSER_DICT[self.src_lang]
    self.param_collector = p_visitor_py.ParametrizableVariablesCollector()

  def load_tree_from(self, subject_name: str) -> p_visitor_py.Tree:
    for fpath in self.snippets_dir.iterdir():
      if fpath.name.startswith(subject_name):
        snippet_text = p_utils.read_text(fpath)
        ts_tree = self.parser.parse(bytes(snippet_text, 'utf8'))
        tree = p_visitor_py.Tree.from_ts_tree(ts_tree)
        return tree
    raise FileNotFoundError(f"No file starting with '{subject_name}' found in {self.snippets_dir}")

  def test_L0001(self):
    tree = self.load_tree_from('L0001')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'target'])


if __name__ == '__main__':
  unittest.main()
