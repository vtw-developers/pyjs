import unittest
from pathlib import Path

import p_consts
import p_utils
import p_visitor_py


class TestParametrizableVariablesCollector(unittest.TestCase):
  def setUp(self):
    self.snippets_dir = p_consts.TEST_ARTIFACTS_DIR / 'p-visitor-py-test-only-body'
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

  def test_L0003(self):
    tree = self.load_tree_from('L0003')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0004(self):
    tree = self.load_tree_from('L0004')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums1', 'nums2'])

  def test_L0005(self):
    tree = self.load_tree_from('L0005')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0006(self):
    tree = self.load_tree_from('L0006')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'numRows'])

  def test_L0007(self):
    tree = self.load_tree_from('L0007')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['x'])

  def test_L0008(self):
    tree = self.load_tree_from('L0008')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0009(self):
    tree = self.load_tree_from('L0009')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['x'])

  def test_L0010(self):
    tree = self.load_tree_from('L0010')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'p'])

  def test_L0011(self):
    tree = self.load_tree_from('L0011')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['height'])

  def test_L0012(self):
    tree = self.load_tree_from('L0012')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num'])

  def test_L0013(self):
    tree = self.load_tree_from('L0013')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0014(self):
    tree = self.load_tree_from('L0014')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['strs'])

  def test_L0015(self):
    tree = self.load_tree_from('L0015')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0016(self):
    tree = self.load_tree_from('L0016')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'target'])

  def test_L0017(self):
    tree = self.load_tree_from('L0017')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['digits'])

  def test_L0018(self):
    tree = self.load_tree_from('L0018')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'target'])

  def test_L0020(self):
    tree = self.load_tree_from('L0020')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0022(self):
    tree = self.load_tree_from('L0022')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0026(self):
    tree = self.load_tree_from('L0026')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0027(self):
    tree = self.load_tree_from('L0027')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'val'])

  def test_L0028(self):
    tree = self.load_tree_from('L0028')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['haystack', 'needle'])

  def test_L0029(self):
    tree = self.load_tree_from('L0029')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['a', 'b'])

  def test_L0030(self):
    tree = self.load_tree_from('L0030')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'words'])

  def test_L0032(self):
    tree = self.load_tree_from('L0032')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0033(self):
    tree = self.load_tree_from('L0033')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'target'])

  def test_L0035(self):
    tree = self.load_tree_from('L0035')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'target'])

  def test_L0036(self):
    tree = self.load_tree_from('L0036')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['board'])

  def test_L0038(self):
    tree = self.load_tree_from('L0038')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0039(self):
    tree = self.load_tree_from('L0039')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['candidates', 'target'])

  def test_L0040(self):
    tree = self.load_tree_from('L0040')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['candidates', 'target'])

  def test_L0041(self):
    tree = self.load_tree_from('L0041')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0042(self):
    tree = self.load_tree_from('L0042')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['height'])

  def test_L0043(self):
    tree = self.load_tree_from('L0043')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num1', 'num2'])

  def test_L0045(self):
    tree = self.load_tree_from('L0045')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0046(self):
    tree = self.load_tree_from('L0046')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0047(self):
    tree = self.load_tree_from('L0047')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0048(self):
    tree = self.load_tree_from('L0048')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['matrix'])

  def test_L0049(self):
    tree = self.load_tree_from('L0049')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['strs'])

  def test_L0050(self):
    tree = self.load_tree_from('L0050')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['x', 'n'])

  def test_L0051(self):
    tree = self.load_tree_from('L0051')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0053(self):
    tree = self.load_tree_from('L0053')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0054(self):
    tree = self.load_tree_from('L0054')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['matrix'])

  def test_L0055(self):
    tree = self.load_tree_from('L0055')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0056(self):
    tree = self.load_tree_from('L0056')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['intervals'])

  def test_L0057(self):
    tree = self.load_tree_from('L0057')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['intervals', 'newInterval'])

  def test_L0058(self):
    tree = self.load_tree_from('L0058')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0059(self):
    tree = self.load_tree_from('L0059')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0062(self):
    tree = self.load_tree_from('L0062')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['m', 'n'])

  def test_L0063(self):
    tree = self.load_tree_from('L0063')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['obstacleGrid'])

  def test_L0064(self):
    tree = self.load_tree_from('L0064')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L0065(self):
    tree = self.load_tree_from('L0065')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0066(self):
    tree = self.load_tree_from('L0066')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['digits'])

  def test_L0067(self):
    tree = self.load_tree_from('L0067')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['a', 'b'])

  def test_L0068(self):
    tree = self.load_tree_from('L0068')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['words', 'maxWidth'])

  def test_L0069(self):
    tree = self.load_tree_from('L0069')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['x'])

  def test_L0070(self):
    tree = self.load_tree_from('L0070')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0071(self):
    tree = self.load_tree_from('L0071')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['path'])

  def test_L0072(self):
    tree = self.load_tree_from('L0072')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['word1', 'word2'])

  def test_L0073(self):
    tree = self.load_tree_from('L0073')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['matrix'])

  def test_L0074(self):
    tree = self.load_tree_from('L0074')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['matrix', 'target'])

  def test_L0075(self):
    tree = self.load_tree_from('L0075')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0076(self):
    tree = self.load_tree_from('L0076')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 't'])

  def test_L0077(self):
    tree = self.load_tree_from('L0077')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'k'])

  def test_L0078(self):
    tree = self.load_tree_from('L0078')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0079(self):
    tree = self.load_tree_from('L0079')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['board', 'word'])

  def test_L0080(self):
    tree = self.load_tree_from('L0080')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0081(self):
    tree = self.load_tree_from('L0081')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'target'])

  def test_L0084(self):
    tree = self.load_tree_from('L0084')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['heights'])

  def test_L0087(self):
    tree = self.load_tree_from('L0087')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s1', 's2'])

  def test_L0088(self):
    tree = self.load_tree_from('L0088')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums1', 'm', 'nums2', 'n'])

  def test_L0089(self):
    tree = self.load_tree_from('L0089')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0090(self):
    tree = self.load_tree_from('L0090')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0091(self):
    tree = self.load_tree_from('L0091')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0093(self):
    tree = self.load_tree_from('L0093')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0096(self):
    tree = self.load_tree_from('L0096')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0097(self):
    tree = self.load_tree_from('L0097')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s1', 's2', 's3'])

  def test_L0118(self):
    tree = self.load_tree_from('L0118')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['numRows'])

  def test_L0119(self):
    tree = self.load_tree_from('L0119')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['rowIndex'])

  def test_L0120(self):
    tree = self.load_tree_from('L0120')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['triangle'])

  def test_L0121(self):
    tree = self.load_tree_from('L0121')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['prices'])

  def test_L0122(self):
    tree = self.load_tree_from('L0122')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['prices'])

  def test_L0123(self):
    tree = self.load_tree_from('L0123')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['prices'])

  def test_L0126(self):
    tree = self.load_tree_from('L0126')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['beginWord', 'endWord', 'wordList'])

  def test_L0127(self):
    tree = self.load_tree_from('L0127')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['beginWord', 'endWord', 'wordList'])

  def test_L0128(self):
    tree = self.load_tree_from('L0128')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0130(self):
    tree = self.load_tree_from('L0130')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['board'])

  def test_L0131(self):
    tree = self.load_tree_from('L0131')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0132(self):
    tree = self.load_tree_from('L0132')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0136(self):
    tree = self.load_tree_from('L0136')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0137(self):
    tree = self.load_tree_from('L0137')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0139(self):
    tree = self.load_tree_from('L0139')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'wordDict'])

  def test_L0149(self):
    tree = self.load_tree_from('L0149')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['points'])

  def test_L0150(self):
    tree = self.load_tree_from('L0150')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['tokens'])

  def test_L0151(self):
    tree = self.load_tree_from('L0151')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0152(self):
    tree = self.load_tree_from('L0152')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0153(self):
    tree = self.load_tree_from('L0153')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0154(self):
    tree = self.load_tree_from('L0154')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0159(self):
    tree = self.load_tree_from('L0159')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0162(self):
    tree = self.load_tree_from('L0162')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])


if __name__ == '__main__':
  unittest.main()
