import unittest
from typing import Tuple

import p_consts
import p_utils
import p_visitor as pvis
import p_visitor_py


class TestParametrizableVariablesCollector(unittest.TestCase):
  def setUp(self):
    self.snippets_dir = p_consts.TEST_ARTIFACTS_DIR / 'py' / 'TestParametrizableVariablesCollector'
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

  def test_identifier_in_keyword_argument(self):
    code = '''while i < j:
    print(id_wpyb, id_xafp=id_evw)
    break'''
    ts_tree = self.parser.parse(bytes(code, 'utf8'))
    tree = p_visitor_py.Tree.from_ts_tree(ts_tree)
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['i', 'j', 'id_wpyb', 'id_evw'])

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

  def test_L0165(self):
    tree = self.load_tree_from('L0165')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['version1', 'version2'])

  def test_L0166(self):
    tree = self.load_tree_from('L0166')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['numerator', 'denominator'])

  def test_L0167(self):
    tree = self.load_tree_from('L0167')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['numbers', 'target'])

  def test_L0168(self):
    tree = self.load_tree_from('L0168')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['columnNumber'])

  def test_L0169(self):
    tree = self.load_tree_from('L0169')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0171(self):
    tree = self.load_tree_from('L0171')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['columnTitle'])

  def test_L0172(self):
    tree = self.load_tree_from('L0172')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0179(self):
    tree = self.load_tree_from('L0179')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0186(self):
    tree = self.load_tree_from('L0186')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0187(self):
    tree = self.load_tree_from('L0187')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0188(self):
    tree = self.load_tree_from('L0188')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['k', 'prices'])

  def test_L0189(self):
    tree = self.load_tree_from('L0189')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L0198(self):
    tree = self.load_tree_from('L0198')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0200(self):
    tree = self.load_tree_from('L0200')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L0201(self):
    tree = self.load_tree_from('L0201')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['left', 'right'])

  def test_L0202(self):
    tree = self.load_tree_from('L0202')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0204(self):
    tree = self.load_tree_from('L0204')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0205(self):
    tree = self.load_tree_from('L0205')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 't'])

  def test_L0207(self):
    tree = self.load_tree_from('L0207')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['numCourses', 'prerequisites'])

  def test_L0210(self):
    tree = self.load_tree_from('L0210')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['numCourses', 'prerequisites'])

  def test_L0212(self):
    tree = self.load_tree_from('L0212')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['board', 'words'])

  def test_L0213(self):
    tree = self.load_tree_from('L0213')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0214(self):
    tree = self.load_tree_from('L0214')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0215(self):
    tree = self.load_tree_from('L0215')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L0216(self):
    tree = self.load_tree_from('L0216')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['k', 'n'])

  def test_L0217(self):
    tree = self.load_tree_from('L0217')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0219(self):
    tree = self.load_tree_from('L0219')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L0221(self):
    tree = self.load_tree_from('L0221')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['matrix'])

  def test_L0223(self):
    tree = self.load_tree_from('L0223')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['ax1', 'ay1', 'ax2', 'ay2', 'bx1', 'by1', 'bx2', 'by2'])

  def test_L0227(self):
    tree = self.load_tree_from('L0227')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0228(self):
    tree = self.load_tree_from('L0228')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0229(self):
    tree = self.load_tree_from('L0229')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0231(self):
    tree = self.load_tree_from('L0231')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0233(self):
    tree = self.load_tree_from('L0233')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0238(self):
    tree = self.load_tree_from('L0238')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0239(self):
    tree = self.load_tree_from('L0239')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L0240(self):
    tree = self.load_tree_from('L0240')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['matrix', 'target'])

  def test_L0241(self):
    tree = self.load_tree_from('L0241')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['expression'])

  def test_L0242(self):
    tree = self.load_tree_from('L0242')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 't'])

  def test_L0243(self):
    tree = self.load_tree_from('L0243')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['wordsDict', 'word1', 'word2'])

  def test_L0245(self):
    tree = self.load_tree_from('L0245')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['wordsDict', 'word1', 'word2'])

  def test_L0246(self):
    tree = self.load_tree_from('L0246')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num'])

  def test_L0247(self):
    tree = self.load_tree_from('L0247')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0249(self):
    tree = self.load_tree_from('L0249')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['strings'])

  def test_L0252(self):
    tree = self.load_tree_from('L0252')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['intervals'])

  def test_L0253(self):
    tree = self.load_tree_from('L0253')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['intervals'])

  def test_L0255(self):
    tree = self.load_tree_from('L0255')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['preorder'])

  def test_L0256(self):
    tree = self.load_tree_from('L0256')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['costs'])

  def test_L0258(self):
    tree = self.load_tree_from('L0258')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num'])

  def test_L0259(self):
    tree = self.load_tree_from('L0259')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'target'])

  def test_L0260(self):
    tree = self.load_tree_from('L0260')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0261(self):
    tree = self.load_tree_from('L0261')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'edges'])

  def test_L0263(self):
    tree = self.load_tree_from('L0263')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0264(self):
    tree = self.load_tree_from('L0264')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0266(self):
    tree = self.load_tree_from('L0266')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0268(self):
    tree = self.load_tree_from('L0268')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0269(self):
    tree = self.load_tree_from('L0269')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['words'])

  def test_L0273(self):
    tree = self.load_tree_from('L0273')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num'])

  def test_L0274(self):
    tree = self.load_tree_from('L0274')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['citations'])

  def test_L0275(self):
    tree = self.load_tree_from('L0275')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['citations'])

  def test_L0279(self):
    tree = self.load_tree_from('L0279')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0280(self):
    tree = self.load_tree_from('L0280')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0282(self):
    tree = self.load_tree_from('L0282')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num', 'target'])

  def test_L0283(self):
    tree = self.load_tree_from('L0283')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0286(self):
    tree = self.load_tree_from('L0286')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['rooms'])

  def test_L0287(self):
    tree = self.load_tree_from('L0287')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0289(self):
    tree = self.load_tree_from('L0289')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['board'])

  def test_L0290(self):
    tree = self.load_tree_from('L0290')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['pattern', 's'])

  def test_L0291(self):
    tree = self.load_tree_from('L0291')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['pattern', 's'])

  def test_L0292(self):
    tree = self.load_tree_from('L0292')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0293(self):
    tree = self.load_tree_from('L0293')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0299(self):
    tree = self.load_tree_from('L0299')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['secret', 'guess'])

  def test_L0301(self):
    tree = self.load_tree_from('L0301')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0302(self):
    tree = self.load_tree_from('L0302')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['image', 'x', 'y'])

  def test_L0305(self):
    tree = self.load_tree_from('L0305')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['m', 'n', 'positions'])

  def test_L0306(self):
    tree = self.load_tree_from('L0306')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num'])

  def test_L0309(self):
    tree = self.load_tree_from('L0309')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['prices'])

  def test_L0310(self):
    tree = self.load_tree_from('L0310')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'edges'])

  def test_L0311(self):
    tree = self.load_tree_from('L0311')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['mat1', 'mat2'])

  def test_L0312(self):
    tree = self.load_tree_from('L0312')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0317(self):
    tree = self.load_tree_from('L0317')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L0318(self):
    tree = self.load_tree_from('L0318')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['words'])

  def test_L0320(self):
    tree = self.load_tree_from('L0320')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['word'])

  def test_L0322(self):
    tree = self.load_tree_from('L0322')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['coins', 'amount'])

  def test_L0323(self):
    tree = self.load_tree_from('L0323')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'edges'])

  def test_L0324(self):
    tree = self.load_tree_from('L0324')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0325(self):
    tree = self.load_tree_from('L0325')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L0329(self):
    tree = self.load_tree_from('L0329')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['matrix'])

  def test_L0334(self):
    tree = self.load_tree_from('L0334')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0335(self):
    tree = self.load_tree_from('L0335')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['distance'])

  def test_L0338(self):
    tree = self.load_tree_from('L0338')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0342(self):
    tree = self.load_tree_from('L0342')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0343(self):
    tree = self.load_tree_from('L0343')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0344(self):
    tree = self.load_tree_from('L0344')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0345(self):
    tree = self.load_tree_from('L0345')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0347(self):
    tree = self.load_tree_from('L0347')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L0349(self):
    tree = self.load_tree_from('L0349')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums1', 'nums2'])

  def test_L0350(self):
    tree = self.load_tree_from('L0350')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums1', 'nums2'])

  def test_L0356(self):
    tree = self.load_tree_from('L0356')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['points'])

  def test_L0357(self):
    tree = self.load_tree_from('L0357')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0360(self):
    tree = self.load_tree_from('L0360')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'a', 'b', 'c'])

  def test_L0361(self):
    tree = self.load_tree_from('L0361')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L0365(self):
    tree = self.load_tree_from('L0365')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['jug1Capacity', 'jug2Capacity', 'targetCapacity'])

  def test_L0367(self):
    tree = self.load_tree_from('L0367')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num'])

  def test_L0368(self):
    tree = self.load_tree_from('L0368')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0370(self):
    tree = self.load_tree_from('L0370')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['length', 'updates'])

  def test_L0371(self):
    tree = self.load_tree_from('L0371')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['a', 'b'])

  def test_L0372(self):
    tree = self.load_tree_from('L0372')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['a', 'b'])

  def test_L0373(self):
    tree = self.load_tree_from('L0373')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums1', 'nums2', 'k'])

  def test_L0375(self):
    tree = self.load_tree_from('L0375')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0376(self):
    tree = self.load_tree_from('L0376')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0377(self):
    tree = self.load_tree_from('L0377')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'target'])

  def test_L0378(self):
    tree = self.load_tree_from('L0378')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['matrix', 'k'])

  def test_L0383(self):
    tree = self.load_tree_from('L0383')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['ransomNote', 'magazine'])

  def test_L0386(self):
    tree = self.load_tree_from('L0386')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0387(self):
    tree = self.load_tree_from('L0387')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0388(self):
    tree = self.load_tree_from('L0388')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['input'])

  def test_L0389(self):
    tree = self.load_tree_from('L0389')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 't'])

  def test_L0390(self):
    tree = self.load_tree_from('L0390')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0391(self):
    tree = self.load_tree_from('L0391')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['rectangles'])

  def test_L0392(self):
    tree = self.load_tree_from('L0392')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 't'])

  def test_L0393(self):
    tree = self.load_tree_from('L0393')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['data'])

  def test_L0394(self):
    tree = self.load_tree_from('L0394')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0395(self):
    tree = self.load_tree_from('L0395')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'k'])

  def test_L0396(self):
    tree = self.load_tree_from('L0396')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0397(self):
    tree = self.load_tree_from('L0397')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0399(self):
    tree = self.load_tree_from('L0399')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['equations', 'values', 'queries'])

  def test_L0400(self):
    tree = self.load_tree_from('L0400')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0401(self):
    tree = self.load_tree_from('L0401')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['turnedOn'])

  def test_L0403(self):
    tree = self.load_tree_from('L0403')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['stones'])

  def test_L0405(self):
    tree = self.load_tree_from('L0405')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num'])

  def test_L0406(self):
    tree = self.load_tree_from('L0406')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['people'])

  def test_L0407(self):
    tree = self.load_tree_from('L0407')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['heightMap'])

  def test_L0409(self):
    tree = self.load_tree_from('L0409')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0410(self):
    tree = self.load_tree_from('L0410')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'm'])

  def test_L0412(self):
    tree = self.load_tree_from('L0412')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0413(self):
    tree = self.load_tree_from('L0413')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0414(self):
    tree = self.load_tree_from('L0414')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0415(self):
    tree = self.load_tree_from('L0415')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num1', 'num2'])

  def test_L0416(self):
    tree = self.load_tree_from('L0416')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0417(self):
    tree = self.load_tree_from('L0417')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['heights'])

  def test_L0419(self):
    tree = self.load_tree_from('L0419')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['board'])

  def test_L0420(self):
    tree = self.load_tree_from('L0420')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['password'])

  def test_L0421(self):
    tree = self.load_tree_from('L0421')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0423(self):
    tree = self.load_tree_from('L0423')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0424(self):
    tree = self.load_tree_from('L0424')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'k'])

  def test_L0433(self):
    tree = self.load_tree_from('L0433')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['start', 'end', 'bank'])

  def test_L0434(self):
    tree = self.load_tree_from('L0434')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0435(self):
    tree = self.load_tree_from('L0435')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['intervals'])

  def test_L0438(self):
    tree = self.load_tree_from('L0438')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'p'])

  def test_L0440(self):
    tree = self.load_tree_from('L0440')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'k'])

  def test_L0441(self):
    tree = self.load_tree_from('L0441')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0442(self):
    tree = self.load_tree_from('L0442')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0443(self):
    tree = self.load_tree_from('L0443')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['chars'])

  def test_L0444(self):
    tree = self.load_tree_from('L0444')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['org', 'seqs'])

  def test_L0447(self):
    tree = self.load_tree_from('L0447')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['points'])

  def test_L0448(self):
    tree = self.load_tree_from('L0448')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0451(self):
    tree = self.load_tree_from('L0451')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0453(self):
    tree = self.load_tree_from('L0453')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0454(self):
    tree = self.load_tree_from('L0454')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums1', 'nums2', 'nums3', 'nums4'])

  def test_L0456(self):
    tree = self.load_tree_from('L0456')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0457(self):
    tree = self.load_tree_from('L0457')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0458(self):
    tree = self.load_tree_from('L0458')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['buckets', 'minutesToDie', 'minutesToTest'])

  def test_L0461(self):
    tree = self.load_tree_from('L0461')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['x', 'y'])

  def test_L0462(self):
    tree = self.load_tree_from('L0462')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0463(self):
    tree = self.load_tree_from('L0463')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L0464(self):
    tree = self.load_tree_from('L0464')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['maxChoosableInteger', 'desiredTotal'])

  def test_L0467(self):
    tree = self.load_tree_from('L0467')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['p'])

  def test_L0473(self):
    tree = self.load_tree_from('L0473')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['matchsticks'])

  def test_L0474(self):
    tree = self.load_tree_from('L0474')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['strs', 'm', 'n'])

  def test_L0475(self):
    tree = self.load_tree_from('L0475')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['houses', 'heaters'])

  def test_L0477(self):
    tree = self.load_tree_from('L0477')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0479(self):
    tree = self.load_tree_from('L0479')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0482(self):
    tree = self.load_tree_from('L0482')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'k'])

  def test_L0485(self):
    tree = self.load_tree_from('L0485')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0487(self):
    tree = self.load_tree_from('L0487')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0488(self):
    tree = self.load_tree_from('L0488')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['board', 'hand'])

  def test_L0490(self):
    tree = self.load_tree_from('L0490')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['maze', 'start', 'destination'])

  def test_L0491(self):
    tree = self.load_tree_from('L0491')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0492(self):
    tree = self.load_tree_from('L0492')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['area'])

  def test_L0494(self):
    tree = self.load_tree_from('L0494')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'target'])

  def test_L0495(self):
    tree = self.load_tree_from('L0495')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['timeSeries', 'duration'])

  def test_L0496(self):
    tree = self.load_tree_from('L0496')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums1', 'nums2'])

  def test_L0498(self):
    tree = self.load_tree_from('L0498')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['mat'])

  def test_L0499(self):
    tree = self.load_tree_from('L0499')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['maze', 'ball', 'hole'])

  def test_L0500(self):
    tree = self.load_tree_from('L0500')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['words'])

  def test_L0503(self):
    tree = self.load_tree_from('L0503')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0504(self):
    tree = self.load_tree_from('L0504')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num'])

  def test_L0505(self):
    tree = self.load_tree_from('L0505')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['maze', 'start', 'destination'])

  def test_L0506(self):
    tree = self.load_tree_from('L0506')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['score'])

  def test_L0507(self):
    tree = self.load_tree_from('L0507')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num'])

  def test_L0509(self):
    tree = self.load_tree_from('L0509')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0516(self):
    tree = self.load_tree_from('L0516')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0518(self):
    tree = self.load_tree_from('L0518')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['amount', 'coins'])

  def test_L0520(self):
    tree = self.load_tree_from('L0520')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['word'])

  def test_L0521(self):
    tree = self.load_tree_from('L0521')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['a', 'b'])

  def test_L0522(self):
    tree = self.load_tree_from('L0522')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['strs'])

  def test_L0523(self):
    tree = self.load_tree_from('L0523')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L0524(self):
    tree = self.load_tree_from('L0524')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'dictionary'])

  def test_L0525(self):
    tree = self.load_tree_from('L0525')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0526(self):
    tree = self.load_tree_from('L0526')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0531(self):
    tree = self.load_tree_from('L0531')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['picture'])

  def test_L0532(self):
    tree = self.load_tree_from('L0532')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L0533(self):
    tree = self.load_tree_from('L0533')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['picture', 'target'])

  def test_L0537(self):
    tree = self.load_tree_from('L0537')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num1', 'num2'])

  def test_L0539(self):
    tree = self.load_tree_from('L0539')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['timePoints'])

  def test_L0540(self):
    tree = self.load_tree_from('L0540')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0541(self):
    tree = self.load_tree_from('L0541')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'k'])

  def test_L0542(self):
    tree = self.load_tree_from('L0542')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['mat'])

  def test_L0544(self):
    tree = self.load_tree_from('L0544')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0547(self):
    tree = self.load_tree_from('L0547')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['isConnected'])

  def test_L0548(self):
    tree = self.load_tree_from('L0548')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0551(self):
    tree = self.load_tree_from('L0551')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0552(self):
    tree = self.load_tree_from('L0552')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0553(self):
    tree = self.load_tree_from('L0553')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0554(self):
    tree = self.load_tree_from('L0554')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['wall'])

  def test_L0557(self):
    tree = self.load_tree_from('L0557')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0560(self):
    tree = self.load_tree_from('L0560')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L0561(self):
    tree = self.load_tree_from('L0561')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0564(self):
    tree = self.load_tree_from('L0564')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0565(self):
    tree = self.load_tree_from('L0565')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0566(self):
    tree = self.load_tree_from('L0566')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'r', 'c'])

  def test_L0567(self):
    tree = self.load_tree_from('L0567')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s1', 's2'])

  def test_L0575(self):
    tree = self.load_tree_from('L0575')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['candyType'])

  def test_L0581(self):
    tree = self.load_tree_from('L0581')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0582(self):
    tree = self.load_tree_from('L0582')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['pid', 'ppid', 'kill'])

  def test_L0583(self):
    tree = self.load_tree_from('L0583')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['word1', 'word2'])

  def test_L0587(self):
    tree = self.load_tree_from('L0587')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['trees'])

  def test_L0591(self):
    tree = self.load_tree_from('L0591')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['code'])

  def test_L0594(self):
    tree = self.load_tree_from('L0594')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0598(self):
    tree = self.load_tree_from('L0598')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['m', 'n', 'ops'])

  def test_L0599(self):
    tree = self.load_tree_from('L0599')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['list1', 'list2'])

  def test_L0605(self):
    tree = self.load_tree_from('L0605')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['flowerBed', 'n'])

  def test_L0609(self):
    tree = self.load_tree_from('L0609')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['paths'])

  def test_L0628(self):
    tree = self.load_tree_from('L0628')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0629(self):
    tree = self.load_tree_from('L0629')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'k'])

  def test_L0630(self):
    tree = self.load_tree_from('L0630')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['courses'])

  def test_L0633(self):
    tree = self.load_tree_from('L0633')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['c'])

  def test_L0638(self):
    tree = self.load_tree_from('L0638')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['price', 'special', 'needs'])

  def test_L0639(self):
    tree = self.load_tree_from('L0639')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0643(self):
    tree = self.load_tree_from('L0643')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L0645(self):
    tree = self.load_tree_from('L0645')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0646(self):
    tree = self.load_tree_from('L0646')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['pairs'])

  def test_L0647(self):
    tree = self.load_tree_from('L0647')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0657(self):
    tree = self.load_tree_from('L0657')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['moves'])

  def test_L0658(self):
    tree = self.load_tree_from('L0658')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr', 'k', 'x'])

  def test_L0661(self):
    tree = self.load_tree_from('L0661')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['img'])

  def test_L0665(self):
    tree = self.load_tree_from('L0665')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0666(self):
    tree = self.load_tree_from('L0666')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0668(self):
    tree = self.load_tree_from('L0668')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['m', 'n', 'k'])

  def test_L0670(self):
    tree = self.load_tree_from('L0670')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num'])

  def test_L0673(self):
    tree = self.load_tree_from('L0673')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0674(self):
    tree = self.load_tree_from('L0674')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0675(self):
    tree = self.load_tree_from('L0675')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['forest'])

  def test_L0678(self):
    tree = self.load_tree_from('L0678')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0680(self):
    tree = self.load_tree_from('L0680')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0681(self):
    tree = self.load_tree_from('L0681')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['time'])

  def test_L0682(self):
    tree = self.load_tree_from('L0682')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['ops'])

  def test_L0684(self):
    tree = self.load_tree_from('L0684')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['edges'])

  def test_L0686(self):
    tree = self.load_tree_from('L0686')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['a', 'b'])

  def test_L0688(self):
    tree = self.load_tree_from('L0688')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'k', 'row', 'column'])

  def test_L0689(self):
    tree = self.load_tree_from('L0689')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L0691(self):
    tree = self.load_tree_from('L0691')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['stickers', 'target'])

  def test_L0692(self):
    tree = self.load_tree_from('L0692')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['words', 'k'])

  def test_L0693(self):
    tree = self.load_tree_from('L0693')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0694(self):
    tree = self.load_tree_from('L0694')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L0695(self):
    tree = self.load_tree_from('L0695')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L0696(self):
    tree = self.load_tree_from('L0696')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0697(self):
    tree = self.load_tree_from('L0697')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0698(self):
    tree = self.load_tree_from('L0698')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L0704(self):
    tree = self.load_tree_from('L0704')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'target'])

  def test_L0709(self):
    tree = self.load_tree_from('L0709')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0711(self):
    tree = self.load_tree_from('L0711')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L0712(self):
    tree = self.load_tree_from('L0712')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s1', 's2'])

  def test_L0713(self):
    tree = self.load_tree_from('L0713')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L0714(self):
    tree = self.load_tree_from('L0714')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['prices', 'fee'])

  def test_L0717(self):
    tree = self.load_tree_from('L0717')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['bits'])

  def test_L0718(self):
    tree = self.load_tree_from('L0718')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums1', 'nums2'])

  def test_L0720(self):
    tree = self.load_tree_from('L0720')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['words'])

  def test_L0721(self):
    tree = self.load_tree_from('L0721')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['accounts'])

  def test_L0723(self):
    tree = self.load_tree_from('L0723')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['board'])

  def test_L0724(self):
    tree = self.load_tree_from('L0724')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0728(self):
    tree = self.load_tree_from('L0728')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['left', 'right'])

  def test_L0730(self):
    tree = self.load_tree_from('L0730')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0733(self):
    tree = self.load_tree_from('L0733')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['image', 'sr', 'sc', 'newColor'])

  def test_L0734(self):
    tree = self.load_tree_from('L0734')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['sentence1', 'sentence2', 'similarPairs'])

  def test_L0735(self):
    tree = self.load_tree_from('L0735')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['asteroids'])

  def test_L0737(self):
    tree = self.load_tree_from('L0737')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['sentence1', 'sentence2', 'similarPairs'])

  def test_L0739(self):
    tree = self.load_tree_from('L0739')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['temperatures'])

  def test_L0740(self):
    tree = self.load_tree_from('L0740')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0741(self):
    tree = self.load_tree_from('L0741')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L0743(self):
    tree = self.load_tree_from('L0743')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['times', 'n', 'k'])

  def test_L0744(self):
    tree = self.load_tree_from('L0744')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['letters', 'target'])

  def test_L0746(self):
    tree = self.load_tree_from('L0746')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['cost'])

  def test_L0747(self):
    tree = self.load_tree_from('L0747')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0748(self):
    tree = self.load_tree_from('L0748')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['licensePlate', 'words'])

  def test_L0749(self):
    tree = self.load_tree_from('L0749')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['isInfected'])

  def test_L0752(self):
    tree = self.load_tree_from('L0752')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['deadends', 'target'])

  def test_L0760(self):
    tree = self.load_tree_from('L0760')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums1', 'nums2'])

  def test_L0763(self):
    tree = self.load_tree_from('L0763')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0765(self):
    tree = self.load_tree_from('L0765')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['row'])

  def test_L0766(self):
    tree = self.load_tree_from('L0766')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['matrix'])

  def test_L0767(self):
    tree = self.load_tree_from('L0767')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0768(self):
    tree = self.load_tree_from('L0768')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L0769(self):
    tree = self.load_tree_from('L0769')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L0771(self):
    tree = self.load_tree_from('L0771')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['jewels', 'stones'])

  def test_L0773(self):
    tree = self.load_tree_from('L0773')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['board'])

  def test_L0778(self):
    tree = self.load_tree_from('L0778')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L0779(self):
    tree = self.load_tree_from('L0779')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'k'])

  def test_L0780(self):
    tree = self.load_tree_from('L0780')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['sx', 'sy', 'tx', 'ty'])

  def test_L0781(self):
    tree = self.load_tree_from('L0781')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['answers'])

  def test_L0784(self):
    tree = self.load_tree_from('L0784')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0785(self):
    tree = self.load_tree_from('L0785')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['graph'])

  def test_L0786(self):
    tree = self.load_tree_from('L0786')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr', 'k'])

  def test_L0787(self):
    tree = self.load_tree_from('L0787')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'flights', 'src', 'dst', 'k'])

  def test_L0789(self):
    tree = self.load_tree_from('L0789')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['ghosts', 'target'])

  def test_L0792(self):
    tree = self.load_tree_from('L0792')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'words'])

  def test_L0794(self):
    tree = self.load_tree_from('L0794')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['board'])

  def test_L0796(self):
    tree = self.load_tree_from('L0796')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'goal'])

  def test_L0797(self):
    tree = self.load_tree_from('L0797')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['graph'])

  def test_L0798(self):
    tree = self.load_tree_from('L0798')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0800(self):
    tree = self.load_tree_from('L0800')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['color'])

  def test_L0802(self):
    tree = self.load_tree_from('L0802')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['graph'])

  def test_L0803(self):
    tree = self.load_tree_from('L0803')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid', 'hits'])

  def test_L0804(self):
    tree = self.load_tree_from('L0804')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['words'])

  def test_L0806(self):
    tree = self.load_tree_from('L0806')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['widths', 's'])

  def test_L0807(self):
    tree = self.load_tree_from('L0807')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L0811(self):
    tree = self.load_tree_from('L0811')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['cpdomains'])

  def test_L0812(self):
    tree = self.load_tree_from('L0812')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['points'])

  def test_L0816(self):
    tree = self.load_tree_from('L0816')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0819(self):
    tree = self.load_tree_from('L0819')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['paragraph', 'banned'])

  def test_L0821(self):
    tree = self.load_tree_from('L0821')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'c'])

  def test_L0822(self):
    tree = self.load_tree_from('L0822')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['fronts', 'backs'])

  def test_L0824(self):
    tree = self.load_tree_from('L0824')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['sentence'])

  def test_L0825(self):
    tree = self.load_tree_from('L0825')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['ages'])

  def test_L0826(self):
    tree = self.load_tree_from('L0826')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['difficulty', 'profit', 'worker'])

  def test_L0827(self):
    tree = self.load_tree_from('L0827')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L0829(self):
    tree = self.load_tree_from('L0829')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0832(self):
    tree = self.load_tree_from('L0832')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['A'])

  def test_L0838(self):
    tree = self.load_tree_from('L0838')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['dominoes'])

  def test_L0839(self):
    tree = self.load_tree_from('L0839')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['strs'])

  def test_L0841(self):
    tree = self.load_tree_from('L0841')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['rooms'])

  def test_L0844(self):
    tree = self.load_tree_from('L0844')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 't'])

  def test_L0845(self):
    tree = self.load_tree_from('L0845')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L0847(self):
    tree = self.load_tree_from('L0847')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['graph'])

  def test_L0848(self):
    tree = self.load_tree_from('L0848')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['S', 'shifts'])

  def test_L0851(self):
    tree = self.load_tree_from('L0851')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['richer', 'quiet'])

  def test_L0852(self):
    tree = self.load_tree_from('L0852')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L0853(self):
    tree = self.load_tree_from('L0853')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['target', 'position', 'speed'])

  def test_L0854(self):
    tree = self.load_tree_from('L0854')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s1', 's2'])

  def test_L0859(self):
    tree = self.load_tree_from('L0859')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'goal'])

  def test_L0860(self):
    tree = self.load_tree_from('L0860')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['bills'])

  def test_L0861(self):
    tree = self.load_tree_from('L0861')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L0862(self):
    tree = self.load_tree_from('L0862')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L0864(self):
    tree = self.load_tree_from('L0864')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L0867(self):
    tree = self.load_tree_from('L0867')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['matrix'])

  def test_L0868(self):
    tree = self.load_tree_from('L0868')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0869(self):
    tree = self.load_tree_from('L0869')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0873(self):
    tree = self.load_tree_from('L0873')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L0875(self):
    tree = self.load_tree_from('L0875')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['piles', 'h'])

  def test_L0881(self):
    tree = self.load_tree_from('L0881')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['people', 'limit'])

  def test_L0883(self):
    tree = self.load_tree_from('L0883')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L0884(self):
    tree = self.load_tree_from('L0884')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s1', 's2'])

  def test_L0885(self):
    tree = self.load_tree_from('L0885')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['rows', 'cols', 'rStart', 'cStart'])

  def test_L0886(self):
    tree = self.load_tree_from('L0886')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'dislikes'])

  def test_L0887(self):
    tree = self.load_tree_from('L0887')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['K', 'N'])

  def test_L0888(self):
    tree = self.load_tree_from('L0888')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['aliceSizes', 'bobSizes'])

  def test_L0890(self):
    tree = self.load_tree_from('L0890')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['words', 'pattern'])

  def test_L0893(self):
    tree = self.load_tree_from('L0893')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['words'])

  def test_L0896(self):
    tree = self.load_tree_from('L0896')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0898(self):
    tree = self.load_tree_from('L0898')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L0904(self):
    tree = self.load_tree_from('L0904')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['tree'])

  def test_L0905(self):
    tree = self.load_tree_from('L0905')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0907(self):
    tree = self.load_tree_from('L0907')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L0908(self):
    tree = self.load_tree_from('L0908')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L0909(self):
    tree = self.load_tree_from('L0909')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['board'])

  def test_L0912(self):
    tree = self.load_tree_from('L0912')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0914(self):
    tree = self.load_tree_from('L0914')
    self.param_collector.visit(tree.root_node)
    # self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['deck'])

  def test_L0915(self):
    tree = self.load_tree_from('L0915')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['A'])

  def test_L0917(self):
    tree = self.load_tree_from('L0917')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0918(self):
    tree = self.load_tree_from('L0918')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0921(self):
    tree = self.load_tree_from('L0921')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0922(self):
    tree = self.load_tree_from('L0922')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0924(self):
    tree = self.load_tree_from('L0924')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['graph', 'initial'])

  def test_L0925(self):
    tree = self.load_tree_from('L0925')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['name', 'typed'])

  def test_L0926(self):
    tree = self.load_tree_from('L0926')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0927(self):
    tree = self.load_tree_from('L0927')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L0928(self):
    tree = self.load_tree_from('L0928')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['graph', 'initial'])

  def test_L0929(self):
    tree = self.load_tree_from('L0929')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['emails'])

  def test_L0930(self):
    tree = self.load_tree_from('L0930')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'goal'])

  def test_L0931(self):
    tree = self.load_tree_from('L0931')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['matrix'])

  def test_L0932(self):
    tree = self.load_tree_from('L0932')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0934(self):
    tree = self.load_tree_from('L0934')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L0935(self):
    tree = self.load_tree_from('L0935')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L0937(self):
    tree = self.load_tree_from('L0937')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['logs'])

  def test_L0941(self):
    tree = self.load_tree_from('L0941')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L0942(self):
    tree = self.load_tree_from('L0942')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L0944(self):
    tree = self.load_tree_from('L0944')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['strs'])

  def test_L0946(self):
    tree = self.load_tree_from('L0946')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['pushed', 'popped'])

  def test_L0947(self):
    tree = self.load_tree_from('L0947')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['stones'])

  def test_L0953(self):
    tree = self.load_tree_from('L0953')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['words', 'order'])

  def test_L0954(self):
    tree = self.load_tree_from('L0954')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L0959(self):
    tree = self.load_tree_from('L0959')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L0960(self):
    tree = self.load_tree_from('L0960')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['strs'])

  def test_L0961(self):
    tree = self.load_tree_from('L0961')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0962(self):
    tree = self.load_tree_from('L0962')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0967(self):
    tree = self.load_tree_from('L0967')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'k'])

  def test_L0969(self):
    tree = self.load_tree_from('L0969')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L0970(self):
    tree = self.load_tree_from('L0970')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['x', 'y', 'bound'])

  def test_L0974(self):
    tree = self.load_tree_from('L0974')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L0977(self):
    tree = self.load_tree_from('L0977')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L0985(self):
    tree = self.load_tree_from('L0985')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'queries'])

  def test_L0986(self):
    tree = self.load_tree_from('L0986')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['firstList', 'secondList'])

  def test_L0989(self):
    tree = self.load_tree_from('L0989')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num', 'k'])

  def test_L0990(self):
    tree = self.load_tree_from('L0990')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['equations'])

  def test_L0994(self):
    tree = self.load_tree_from('L0994')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L0997(self):
    tree = self.load_tree_from('L0997')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'trust'])

  def test_L0999(self):
    tree = self.load_tree_from('L0999')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['board'])

  def test_L1001(self):
    tree = self.load_tree_from('L1001')
    self.param_collector.visit(tree.root_node)
    # removed `n` from the list of parametrizable identifiers
    # it is not used in the original function `f_gold`
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['lamps', 'queries'])

  def test_L1002(self):
    tree = self.load_tree_from('L1002')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['words'])

  def test_L1004(self):
    tree = self.load_tree_from('L1004')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L1005(self):
    tree = self.load_tree_from('L1005')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L1006(self):
    tree = self.load_tree_from('L1006')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['N'])

  def test_L1007(self):
    tree = self.load_tree_from('L1007')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['A', 'B'])

  def test_L1009(self):
    tree = self.load_tree_from('L1009')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L1011(self):
    tree = self.load_tree_from('L1011')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['weights', 'D'])

  def test_L1014(self):
    tree = self.load_tree_from('L1014')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['values'])

  def test_L1016(self):
    tree = self.load_tree_from('L1016')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'n'])

  def test_L1020(self):
    tree = self.load_tree_from('L1020')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L1021(self):
    tree = self.load_tree_from('L1021')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1027(self):
    tree = self.load_tree_from('L1027')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1029(self):
    tree = self.load_tree_from('L1029')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['costs'])

  def test_L1030(self):
    tree = self.load_tree_from('L1030')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['rows', 'cols', 'rCenter', 'cCenter'])

  def test_L1031(self):
    tree = self.load_tree_from('L1031')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'firstLen', 'secondLen'])

  def test_L1034(self):
    tree = self.load_tree_from('L1034')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid', 'row', 'col', 'color'])

  def test_L1035(self):
    tree = self.load_tree_from('L1035')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums1', 'nums2'])

  def test_L1037(self):
    tree = self.load_tree_from('L1037')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['points'])

  def test_L1041(self):
    tree = self.load_tree_from('L1041')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['instructions'])

  def test_L1042(self):
    tree = self.load_tree_from('L1042')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'paths'])

  def test_L1044(self):
    tree = self.load_tree_from('L1044')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1046(self):
    tree = self.load_tree_from('L1046')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['stones'])

  def test_L1047(self):
    tree = self.load_tree_from('L1047')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['S'])

  def test_L1048(self):
    tree = self.load_tree_from('L1048')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['words'])

  def test_L1049(self):
    tree = self.load_tree_from('L1049')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['stones'])

  def test_L1051(self):
    tree = self.load_tree_from('L1051')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['heights'])

  def test_L1052(self):
    tree = self.load_tree_from('L1052')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['customers', 'grumpy', 'minutes'])

  def test_L1061(self):
    tree = self.load_tree_from('L1061')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s1', 's2', 'baseStr'])

  def test_L1064(self):
    tree = self.load_tree_from('L1064')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L1072(self):
    tree = self.load_tree_from('L1072')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['matrix'])

  def test_L1078(self):
    tree = self.load_tree_from('L1078')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['text', 'first', 'second'])

  def test_L1079(self):
    tree = self.load_tree_from('L1079')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['tiles'])

  def test_L1085(self):
    tree = self.load_tree_from('L1085')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1087(self):
    tree = self.load_tree_from('L1087')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1089(self):
    tree = self.load_tree_from('L1089')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L1090(self):
    tree = self.load_tree_from('L1090')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['values', 'labels', 'numWanted', 'useLimit'])

  def test_L1091(self):
    tree = self.load_tree_from('L1091')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L1094(self):
    tree = self.load_tree_from('L1094')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['trips', 'capacity'])

  def test_L1099(self):
    tree = self.load_tree_from('L1099')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L1100(self):
    tree = self.load_tree_from('L1100')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'k'])

  def test_L1101(self):
    tree = self.load_tree_from('L1101')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['logs', 'n'])

  def test_L1102(self):
    tree = self.load_tree_from('L1102')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L1103(self):
    tree = self.load_tree_from('L1103')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['candies', 'num_people'])

  def test_L1105(self):
    tree = self.load_tree_from('L1105')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['books', 'shelfWidth'])

  def test_L1108(self):
    tree = self.load_tree_from('L1108')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['address'])

  def test_L1109(self):
    tree = self.load_tree_from('L1109')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['bookings', 'n'])

  def test_L1118(self):
    tree = self.load_tree_from('L1118')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['year', 'month'])

  def test_L1119(self):
    tree = self.load_tree_from('L1119')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1122(self):
    tree = self.load_tree_from('L1122')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr1', 'arr2'])

  def test_L1124(self):
    tree = self.load_tree_from('L1124')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['hours'])

  def test_L1128(self):
    tree = self.load_tree_from('L1128')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['dominoes'])

  def test_L1129(self):
    tree = self.load_tree_from('L1129')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'redEdges', 'blueEdges'])

  def test_L1133(self):
    tree = self.load_tree_from('L1133')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['A'])

  def test_L1134(self):
    tree = self.load_tree_from('L1134')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L1135(self):
    tree = self.load_tree_from('L1135')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'connections'])

  def test_L1137(self):
    tree = self.load_tree_from('L1137')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L1143(self):
    tree = self.load_tree_from('L1143')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['text1', 'text2'])

  def test_L1154(self):
    tree = self.load_tree_from('L1154')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['date'])

  def test_L1160(self):
    tree = self.load_tree_from('L1160')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['words', 'chars'])

  def test_L1162(self):
    tree = self.load_tree_from('L1162')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L1165(self):
    tree = self.load_tree_from('L1165')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['keyboard', 'word'])

  def test_L1167(self):
    tree = self.load_tree_from('L1167')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['sticks'])

  def test_L1168(self):
    tree = self.load_tree_from('L1168')
    self.param_collector.visit(tree.root_node)
    # `pipes` is a built-in module in Python
    # How can we tell that in this snippet it is not a module:
    # `pipes.append([0, i + 1, w])`
    # self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'wells', 'pipes'])

  def test_L1175(self):
    tree = self.load_tree_from('L1175')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L1180(self):
    tree = self.load_tree_from('L1180')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1181(self):
    tree = self.load_tree_from('L1181')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['phrases'])

  def test_L1182(self):
    tree = self.load_tree_from('L1182')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['colors', 'queries'])

  def test_L1185(self):
    tree = self.load_tree_from('L1185')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['day', 'month', 'year'])

  def test_L1189(self):
    tree = self.load_tree_from('L1189')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['text'])

  def test_L1190(self):
    tree = self.load_tree_from('L1190')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1197(self):
    tree = self.load_tree_from('L1197')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['x', 'y'])

  def test_L1198(self):
    tree = self.load_tree_from('L1198')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['mat'])

  def test_L1202(self):
    tree = self.load_tree_from('L1202')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'pairs'])

  def test_L1207(self):
    tree = self.load_tree_from('L1207')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L1208(self):
    tree = self.load_tree_from('L1208')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 't', 'maxCost'])

  def test_L1210(self):
    tree = self.load_tree_from('L1210')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L1213(self):
    tree = self.load_tree_from('L1213')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr1', 'arr2', 'arr3'])

  def test_L1217(self):
    tree = self.load_tree_from('L1217')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['position'])

  def test_L1218(self):
    tree = self.load_tree_from('L1218')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr', 'difference'])

  def test_L1219(self):
    tree = self.load_tree_from('L1219')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L1220(self):
    tree = self.load_tree_from('L1220')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L1221(self):
    tree = self.load_tree_from('L1221')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1222(self):
    tree = self.load_tree_from('L1222')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['queens', 'king'])

  def test_L1228(self):
    tree = self.load_tree_from('L1228')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L1230(self):
    tree = self.load_tree_from('L1230')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['prob', 'target'])

  def test_L1234(self):
    tree = self.load_tree_from('L1234')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1239(self):
    tree = self.load_tree_from('L1239')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L1243(self):
    tree = self.load_tree_from('L1243')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L1245(self):
    tree = self.load_tree_from('L1245')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['edges'])

  def test_L1252(self):
    tree = self.load_tree_from('L1252')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['m', 'n', 'indices'])

  def test_L1254(self):
    tree = self.load_tree_from('L1254')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L1257(self):
    tree = self.load_tree_from('L1257')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['regions', 'region1', 'region2'])

  def test_L1258(self):
    tree = self.load_tree_from('L1258')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['synonyms', 'text'])

  def test_L1260(self):
    tree = self.load_tree_from('L1260')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid', 'k'])

  def test_L1266(self):
    tree = self.load_tree_from('L1266')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['points'])

  def test_L1267(self):
    tree = self.load_tree_from('L1267')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L1273(self):
    tree = self.load_tree_from('L1273')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nodes', 'parent', 'value'])

  def test_L1275(self):
    tree = self.load_tree_from('L1275')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['moves'])

  def test_L1277(self):
    tree = self.load_tree_from('L1277')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['matrix'])

  def test_L1281(self):
    tree = self.load_tree_from('L1281')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L1282(self):
    tree = self.load_tree_from('L1282')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['groupSizes'])

  def test_L1283(self):
    tree = self.load_tree_from('L1283')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'threshold'])

  def test_L1284(self):
    tree = self.load_tree_from('L1284')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['mat'])

  def test_L1287(self):
    tree = self.load_tree_from('L1287')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L1288(self):
    tree = self.load_tree_from('L1288')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['intervals'])

  def test_L1292(self):
    tree = self.load_tree_from('L1292')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['mat', 'threshold'])

  def test_L1293(self):
    tree = self.load_tree_from('L1293')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid', 'k'])

  def test_L1295(self):
    tree = self.load_tree_from('L1295')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1298(self):
    tree = self.load_tree_from('L1298')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['status', 'candies', 'keys', 'containedBoxes', 'initialBoxes'])

  def test_L1299(self):
    tree = self.load_tree_from('L1299')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L1304(self):
    tree = self.load_tree_from('L1304')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L1306(self):
    tree = self.load_tree_from('L1306')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr', 'start'])

  def test_L1309(self):
    tree = self.load_tree_from('L1309')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1310(self):
    tree = self.load_tree_from('L1310')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr', 'queries'])

  def test_L1311(self):
    tree = self.load_tree_from('L1311')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['watchedVideos', 'friends', 'id', 'level'])

  def test_L1313(self):
    tree = self.load_tree_from('L1313')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1314(self):
    tree = self.load_tree_from('L1314')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['mat', 'k'])

  def test_L1316(self):
    tree = self.load_tree_from('L1316')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['text'])

  def test_L1318(self):
    tree = self.load_tree_from('L1318')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['a', 'b', 'c'])

  def test_L1319(self):
    tree = self.load_tree_from('L1319')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'connections'])

  def test_L1323(self):
    tree = self.load_tree_from('L1323')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num'])

  def test_L1324(self):
    tree = self.load_tree_from('L1324')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1329(self):
    tree = self.load_tree_from('L1329')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['mat'])

  def test_L1332(self):
    tree = self.load_tree_from('L1332')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1338(self):
    tree = self.load_tree_from('L1338')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L1342(self):
    tree = self.load_tree_from('L1342')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num'])

  def test_L1345(self):
    tree = self.load_tree_from('L1345')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L1346(self):
    tree = self.load_tree_from('L1346')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L1347(self):
    tree = self.load_tree_from('L1347')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 't'])

  def test_L1351(self):
    tree = self.load_tree_from('L1351')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L1361(self):
    tree = self.load_tree_from('L1361')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'leftChild', 'rightChild'])

  def test_L1365(self):
    tree = self.load_tree_from('L1365')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1366(self):
    tree = self.load_tree_from('L1366')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['votes'])

  def test_L1368(self):
    tree = self.load_tree_from('L1368')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L1370(self):
    tree = self.load_tree_from('L1370')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1371(self):
    tree = self.load_tree_from('L1371')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1374(self):
    tree = self.load_tree_from('L1374')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L1376(self):
    tree = self.load_tree_from('L1376')
    self.param_collector.visit(tree.root_node)
    # removed `n` from the list of parametrizable identifiers
    # it is not used in the original function `f_gold`
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['headID', 'manager', 'informTime'])

  def test_L1377(self):
    tree = self.load_tree_from('L1377')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'edges', 't', 'target'])

  def test_L1380(self):
    tree = self.load_tree_from('L1380')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['matrix'])

  def test_L1383(self):
    tree = self.load_tree_from('L1383')
    self.param_collector.visit(tree.root_node)
    # removed `n` from the list of parametrizable identifiers
    # it is not used in the original function `f_gold`
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['speed', 'efficiency', 'k'])

  def test_L1385(self):
    tree = self.load_tree_from('L1385')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr1', 'arr2', 'd'])

  def test_L1386(self):
    tree = self.load_tree_from('L1386')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'reservedSeats'])

  def test_L1389(self):
    tree = self.load_tree_from('L1389')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'index'])

  def test_L1391(self):
    tree = self.load_tree_from('L1391')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L1392(self):
    tree = self.load_tree_from('L1392')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1394(self):
    tree = self.load_tree_from('L1394')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L1395(self):
    tree = self.load_tree_from('L1395')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['rating'])

  def test_L1400(self):
    tree = self.load_tree_from('L1400')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'k'])

  def test_L1404(self):
    tree = self.load_tree_from('L1404')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1405(self):
    tree = self.load_tree_from('L1405')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['a', 'b', 'c'])

  def test_L1409(self):
    tree = self.load_tree_from('L1409')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['queries', 'm'])

  def test_L1413(self):
    tree = self.load_tree_from('L1413')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1414(self):
    tree = self.load_tree_from('L1414')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['k'])

  def test_L1418(self):
    tree = self.load_tree_from('L1418')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['orders'])

  def test_L1419(self):
    tree = self.load_tree_from('L1419')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['croakOfFrogs'])

  def test_L1423(self):
    tree = self.load_tree_from('L1423')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['cardPoints', 'k'])

  def test_L1425(self):
    tree = self.load_tree_from('L1425')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L1426(self):
    tree = self.load_tree_from('L1426')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L1431(self):
    tree = self.load_tree_from('L1431')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['candies', 'extraCandies'])

  def test_L1434(self):
    tree = self.load_tree_from('L1434')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['hats'])

  def test_L1436(self):
    tree = self.load_tree_from('L1436')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['paths'])

  def test_L1441(self):
    tree = self.load_tree_from('L1441')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['target', 'n'])

  def test_L1442(self):
    tree = self.load_tree_from('L1442')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L1443(self):
    tree = self.load_tree_from('L1443')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'edges', 'hasApple'])

  def test_L1446(self):
    tree = self.load_tree_from('L1446')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1447(self):
    tree = self.load_tree_from('L1447')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L1450(self):
    tree = self.load_tree_from('L1450')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['startTime', 'endTime', 'queryTime'])

  def test_L1455(self):
    tree = self.load_tree_from('L1455')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['sentence', 'searchWord'])

  def test_L1460(self):
    tree = self.load_tree_from('L1460')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['target', 'arr'])

  def test_L1461(self):
    tree = self.load_tree_from('L1461')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'k'])

  def test_L1462(self):
    tree = self.load_tree_from('L1462')
    self.param_collector.visit(tree.root_node)
    # removed `numCourses` from the list of parametrizable identifiers
    # it is not used in the original function `f_gold`
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['prerequisites', 'queries'])

  def test_L1463(self):
    tree = self.load_tree_from('L1463')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L1464(self):
    tree = self.load_tree_from('L1464')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1466(self):
    tree = self.load_tree_from('L1466')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'connections'])

  def test_L1470(self):
    tree = self.load_tree_from('L1470')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'n'])

  def test_L1471(self):
    tree = self.load_tree_from('L1471')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr', 'k'])

  def test_L1475(self):
    tree = self.load_tree_from('L1475')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['prices'])

  def test_L1480(self):
    tree = self.load_tree_from('L1480')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1481(self):
    tree = self.load_tree_from('L1481')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr', 'k'])

  def test_L1482(self):
    tree = self.load_tree_from('L1482')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['bloomDay', 'm', 'k'])

  def test_L1486(self):
    tree = self.load_tree_from('L1486')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'start'])

  def test_L1496(self):
    tree = self.load_tree_from('L1496')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['path'])

  def test_L1497(self):
    tree = self.load_tree_from('L1497')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr', 'k'])

  def test_L1499(self):
    tree = self.load_tree_from('L1499')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['points', 'k'])

  def test_L1502(self):
    tree = self.load_tree_from('L1502')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L1503(self):
    tree = self.load_tree_from('L1503')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'left', 'right'])

  def test_L1507(self):
    tree = self.load_tree_from('L1507')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['date'])

  def test_L1508(self):
    tree = self.load_tree_from('L1508')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'n', 'left', 'right'])

  def test_L1512(self):
    tree = self.load_tree_from('L1512')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1514(self):
    tree = self.load_tree_from('L1514')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'edges', 'succProb', 'start', 'end'])

  def test_L1518(self):
    tree = self.load_tree_from('L1518')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['numBottles', 'numExchange'])

  def test_L1523(self):
    tree = self.load_tree_from('L1523')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['low', 'high'])

  def test_L1524(self):
    tree = self.load_tree_from('L1524')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L1528(self):
    tree = self.load_tree_from('L1528')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'indices'])

  def test_L1534(self):
    tree = self.load_tree_from('L1534')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr', 'a', 'b', 'c'])

  def test_L1539(self):
    tree = self.load_tree_from('L1539')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr', 'k'])

  def test_L1546(self):
    tree = self.load_tree_from('L1546')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'target'])

  def test_L1551(self):
    tree = self.load_tree_from('L1551')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L1552(self):
    tree = self.load_tree_from('L1552')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['position', 'm'])

  def test_L1554(self):
    tree = self.load_tree_from('L1554')
    self.param_collector.visit(tree.root_node)
    # self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['dict'])

  def test_L1557(self):
    tree = self.load_tree_from('L1557')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'edges'])

  def test_L1559(self):
    tree = self.load_tree_from('L1559')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L1561(self):
    tree = self.load_tree_from('L1561')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['piles'])

  def test_L1567(self):
    tree = self.load_tree_from('L1567')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1572(self):
    tree = self.load_tree_from('L1572')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['mat'])

  def test_L1576(self):
    tree = self.load_tree_from('L1576')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1584(self):
    tree = self.load_tree_from('L1584')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['points'])

  def test_L1588(self):
    tree = self.load_tree_from('L1588')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L1589(self):
    tree = self.load_tree_from('L1589')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'requests'])

  def test_L1605(self):
    tree = self.load_tree_from('L1605')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['rowSum', 'colSum'])

  def test_L1614(self):
    tree = self.load_tree_from('L1614')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1619(self):
    tree = self.load_tree_from('L1619')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L1625(self):
    tree = self.load_tree_from('L1625')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'a', 'b'])

  def test_L1626(self):
    tree = self.load_tree_from('L1626')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['scores', 'ages'])

  def test_L1629(self):
    tree = self.load_tree_from('L1629')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['releaseTimes', 'keysPressed'])

  def test_L1630(self):
    tree = self.load_tree_from('L1630')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'l', 'r'])

  def test_L1631(self):
    tree = self.load_tree_from('L1631')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['heights'])

  def test_L1636(self):
    tree = self.load_tree_from('L1636')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1640(self):
    tree = self.load_tree_from('L1640')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr', 'pieces'])

  def test_L1641(self):
    tree = self.load_tree_from('L1641')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L1646(self):
    tree = self.load_tree_from('L1646')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L1647(self):
    tree = self.load_tree_from('L1647')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1652(self):
    tree = self.load_tree_from('L1652')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['code', 'k'])

  def test_L1654(self):
    tree = self.load_tree_from('L1654')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['forbidden', 'a', 'b', 'x'])

  def test_L1658(self):
    tree = self.load_tree_from('L1658')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'x'])

  def test_L1662(self):
    tree = self.load_tree_from('L1662')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['word1', 'word2'])

  def test_L1672(self):
    tree = self.load_tree_from('L1672')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['accounts'])

  def test_L1678(self):
    tree = self.load_tree_from('L1678')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['command'])

  def test_L1679(self):
    tree = self.load_tree_from('L1679')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L1684(self):
    tree = self.load_tree_from('L1684')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['allowed', 'words'])

  def test_L1685(self):
    tree = self.load_tree_from('L1685')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1688(self):
    tree = self.load_tree_from('L1688')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L1689(self):
    tree = self.load_tree_from('L1689')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L1691(self):
    tree = self.load_tree_from('L1691')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['cuboids'])

  def test_L1697(self):
    tree = self.load_tree_from('L1697')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'edgeList', 'queries'])

  def test_L1700(self):
    tree = self.load_tree_from('L1700')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['students', 'sandwiches'])

  def test_L1701(self):
    tree = self.load_tree_from('L1701')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['customers'])

  def test_L1704(self):
    tree = self.load_tree_from('L1704')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1705(self):
    tree = self.load_tree_from('L1705')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['apples', 'days'])

  def test_L1706(self):
    tree = self.load_tree_from('L1706')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L1711(self):
    tree = self.load_tree_from('L1711')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['deliciousness'])

  def test_L1712(self):
    tree = self.load_tree_from('L1712')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1716(self):
    tree = self.load_tree_from('L1716')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L1717(self):
    tree = self.load_tree_from('L1717')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'x', 'y'])

  def test_L1718(self):
    tree = self.load_tree_from('L1718')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L1719(self):
    tree = self.load_tree_from('L1719')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['pairs'])

  def test_L1720(self):
    tree = self.load_tree_from('L1720')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['encoded', 'first'])

  def test_L1722(self):
    tree = self.load_tree_from('L1722')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['source', 'target', 'allowedSwaps'])

  def test_L1723(self):
    tree = self.load_tree_from('L1723')
    self.param_collector.visit(tree.root_node)
    # from math import inf
    # ans = inf
    # self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['jobs', 'k'])

  def test_L1725(self):
    tree = self.load_tree_from('L1725')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['rectangles'])

  def test_L1730(self):
    tree = self.load_tree_from('L1730')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L1732(self):
    tree = self.load_tree_from('L1732')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['gain'])

  def test_L1734(self):
    tree = self.load_tree_from('L1734')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['encoded'])

  def test_L1736(self):
    tree = self.load_tree_from('L1736')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['time'])

  def test_L1742(self):
    tree = self.load_tree_from('L1742')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['lowLimit', 'highLimit'])

  def test_L1743(self):
    tree = self.load_tree_from('L1743')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['adjacentPairs'])

  def test_L1748(self):
    tree = self.load_tree_from('L1748')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1758(self):
    tree = self.load_tree_from('L1758')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1760(self):
    tree = self.load_tree_from('L1760')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'maxOperations'])

  def test_L1763(self):
    tree = self.load_tree_from('L1763')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1765(self):
    tree = self.load_tree_from('L1765')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['isWater'])

  def test_L1768(self):
    tree = self.load_tree_from('L1768')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['word1', 'word2'])

  def test_L1769(self):
    tree = self.load_tree_from('L1769')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['boxes'])

  def test_L1772(self):
    tree = self.load_tree_from('L1772')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['features', 'responses'])

  def test_L1773(self):
    tree = self.load_tree_from('L1773')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['items', 'ruleKey', 'ruleValue'])

  def test_L1775(self):
    tree = self.load_tree_from('L1775')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums1', 'nums2'])

  def test_L1781(self):
    tree = self.load_tree_from('L1781')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1790(self):
    tree = self.load_tree_from('L1790')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s1', 's2'])

  def test_L1791(self):
    tree = self.load_tree_from('L1791')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['edges'])

  def test_L1796(self):
    tree = self.load_tree_from('L1796')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1798(self):
    tree = self.load_tree_from('L1798')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['coins'])

  def test_L1800(self):
    tree = self.load_tree_from('L1800')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1805(self):
    tree = self.load_tree_from('L1805')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['word'])

  def test_L1807(self):
    tree = self.load_tree_from('L1807')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'knowledge'])

  def test_L1812(self):
    tree = self.load_tree_from('L1812')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['coordinates'])

  def test_L1813(self):
    tree = self.load_tree_from('L1813')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['sentence1', 'sentence2'])

  def test_L1816(self):
    tree = self.load_tree_from('L1816')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'k'])

  def test_L1817(self):
    tree = self.load_tree_from('L1817')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['logs', 'k'])

  def test_L1822(self):
    tree = self.load_tree_from('L1822')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1823(self):
    tree = self.load_tree_from('L1823')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'k'])

  def test_L1826(self):
    tree = self.load_tree_from('L1826')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['sensor1', 'sensor2'])

  def test_L1827(self):
    tree = self.load_tree_from('L1827')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1828(self):
    tree = self.load_tree_from('L1828')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['points', 'queries'])

  def test_L1829(self):
    tree = self.load_tree_from('L1829')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'maximumBit'])

  def test_L1832(self):
    tree = self.load_tree_from('L1832')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['sentence'])

  def test_L1833(self):
    tree = self.load_tree_from('L1833')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['costs', 'coins'])

  def test_L1837(self):
    tree = self.load_tree_from('L1837')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'k'])

  def test_L1838(self):
    tree = self.load_tree_from('L1838')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L1844(self):
    tree = self.load_tree_from('L1844')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1848(self):
    tree = self.load_tree_from('L1848')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'target', 'start'])

  def test_L1854(self):
    tree = self.load_tree_from('L1854')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['logs'])

  def test_L1855(self):
    tree = self.load_tree_from('L1855')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums1', 'nums2'])

  def test_L1856(self):
    tree = self.load_tree_from('L1856')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1859(self):
    tree = self.load_tree_from('L1859')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1860(self):
    tree = self.load_tree_from('L1860')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['memory1', 'memory2'])

  def test_L1861(self):
    tree = self.load_tree_from('L1861')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['box'])

  def test_L1864(self):
    tree = self.load_tree_from('L1864')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1869(self):
    tree = self.load_tree_from('L1869')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1870(self):
    tree = self.load_tree_from('L1870')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['dist', 'hour'])

  def test_L1871(self):
    tree = self.load_tree_from('L1871')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'minJump', 'maxJump'])

  def test_L1872(self):
    tree = self.load_tree_from('L1872')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['stones'])

  def test_L1874(self):
    tree = self.load_tree_from('L1874')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums1', 'nums2'])

  def test_L1876(self):
    tree = self.load_tree_from('L1876')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1877(self):
    tree = self.load_tree_from('L1877')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1880(self):
    tree = self.load_tree_from('L1880')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['firstWord', 'secondWord', 'targetWord'])

  def test_L1881(self):
    tree = self.load_tree_from('L1881')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'x'])

  def test_L1882(self):
    tree = self.load_tree_from('L1882')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['servers', 'tasks'])

  def test_L1883(self):
    tree = self.load_tree_from('L1883')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['dist', 'speed', 'hoursBefore'])

  def test_L1886(self):
    tree = self.load_tree_from('L1886')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['mat', 'target'])

  def test_L1887(self):
    tree = self.load_tree_from('L1887')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1888(self):
    tree = self.load_tree_from('L1888')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1891(self):
    tree = self.load_tree_from('L1891')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['ribbons', 'k'])

  def test_L1893(self):
    tree = self.load_tree_from('L1893')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['ranges', 'left', 'right'])

  def test_L1895(self):
    tree = self.load_tree_from('L1895')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L1897(self):
    tree = self.load_tree_from('L1897')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['words'])

  def test_L1898(self):
    tree = self.load_tree_from('L1898')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'p', 'removable'])

  def test_L1899(self):
    tree = self.load_tree_from('L1899')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['triplets', 'target'])

  def test_L1903(self):
    tree = self.load_tree_from('L1903')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num'])

  def test_L1904(self):
    tree = self.load_tree_from('L1904')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['startTime', 'finishTime'])

  def test_L1905(self):
    tree = self.load_tree_from('L1905')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid1', 'grid2'])

  def test_L1906(self):
    tree = self.load_tree_from('L1906')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'queries'])

  def test_L1909(self):
    tree = self.load_tree_from('L1909')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1913(self):
    tree = self.load_tree_from('L1913')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1914(self):
    tree = self.load_tree_from('L1914')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid', 'k'])

  def test_L1915(self):
    tree = self.load_tree_from('L1915')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['word'])

  def test_L1920(self):
    tree = self.load_tree_from('L1920')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1921(self):
    tree = self.load_tree_from('L1921')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['dist', 'speed'])

  def test_L1922(self):
    tree = self.load_tree_from('L1922')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L1923(self):
    tree = self.load_tree_from('L1923')
    self.param_collector.visit(tree.root_node)
    # removed `n` from the list of parametrizable identifiers
    # it is not used in the original function `f_gold`
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['paths'])

  def test_L1925(self):
    tree = self.load_tree_from('L1925')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L1926(self):
    tree = self.load_tree_from('L1926')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['maze', 'entrance'])

  def test_L1929(self):
    tree = self.load_tree_from('L1929')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1930(self):
    tree = self.load_tree_from('L1930')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1935(self):
    tree = self.load_tree_from('L1935')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['text', 'brokenLetters'])

  def test_L1936(self):
    tree = self.load_tree_from('L1936')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['rungs', 'dist'])

  def test_L1941(self):
    tree = self.load_tree_from('L1941')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1942(self):
    tree = self.load_tree_from('L1942')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['times', 'targetFriend'])

  def test_L1943(self):
    tree = self.load_tree_from('L1943')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['segments'])

  def test_L1944(self):
    tree = self.load_tree_from('L1944')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['heights'])

  def test_L1945(self):
    tree = self.load_tree_from('L1945')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'k'])

  def test_L1946(self):
    tree = self.load_tree_from('L1946')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num', 'change'])

  def test_L1952(self):
    tree = self.load_tree_from('L1952')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L1953(self):
    tree = self.load_tree_from('L1953')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['milestones'])

  def test_L1957(self):
    tree = self.load_tree_from('L1957')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1958(self):
    tree = self.load_tree_from('L1958')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['board', 'rMove', 'cMove', 'color'])

  def test_L1959(self):
    tree = self.load_tree_from('L1959')
    self.param_collector.visit(tree.root_node)
    # uses inf
    # self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L1961(self):
    tree = self.load_tree_from('L1961')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'words'])

  def test_L1962(self):
    tree = self.load_tree_from('L1962')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['piles', 'k'])

  def test_L1963(self):
    tree = self.load_tree_from('L1963')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L1967(self):
    tree = self.load_tree_from('L1967')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['patterns', 'word'])

  def test_L1968(self):
    tree = self.load_tree_from('L1968')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1970(self):
    tree = self.load_tree_from('L1970')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['row', 'col', 'cells'])

  def test_L1971(self):
    tree = self.load_tree_from('L1971')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'edges', 'source', 'destination'])

  def test_L1974(self):
    tree = self.load_tree_from('L1974')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['word'])

  def test_L1976(self):
    tree = self.load_tree_from('L1976')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'roads'])

  def test_L1979(self):
    tree = self.load_tree_from('L1979')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1980(self):
    tree = self.load_tree_from('L1980')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1984(self):
    tree = self.load_tree_from('L1984')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L1991(self):
    tree = self.load_tree_from('L1991')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1992(self):
    tree = self.load_tree_from('L1992')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['land'])

  def test_L1994(self):
    tree = self.load_tree_from('L1994')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1995(self):
    tree = self.load_tree_from('L1995')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L1996(self):
    tree = self.load_tree_from('L1996')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['properties'])

  def test_L1998(self):
    tree = self.load_tree_from('L1998')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2000(self):
    tree = self.load_tree_from('L2000')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['word', 'ch'])

  def test_L2006(self):
    tree = self.load_tree_from('L2006')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L2007(self):
    tree = self.load_tree_from('L2007')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['changed'])

  def test_L2011(self):
    tree = self.load_tree_from('L2011')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['operations'])

  def test_L2012(self):
    tree = self.load_tree_from('L2012')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2016(self):
    tree = self.load_tree_from('L2016')
    self.param_collector.visit(tree.root_node)
    # uses inf
    # self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2017(self):
    tree = self.load_tree_from('L2017')
    self.param_collector.visit(tree.root_node)
    # uses inf
    # self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L2021(self):
    tree = self.load_tree_from('L2021')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['lights'])

  def test_L2022(self):
    tree = self.load_tree_from('L2022')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['original', 'm', 'n'])

  def test_L2023(self):
    tree = self.load_tree_from('L2023')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'target'])

  def test_L2024(self):
    tree = self.load_tree_from('L2024')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['answerKey', 'k'])

  def test_L2028(self):
    tree = self.load_tree_from('L2028')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['rolls', 'mean', 'n'])

  def test_L2029(self):
    tree = self.load_tree_from('L2029')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['stones'])

  def test_L2032(self):
    tree = self.load_tree_from('L2032')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums1', 'nums2', 'nums3'])

  def test_L2033(self):
    tree = self.load_tree_from('L2033')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid', 'x'])

  def test_L2035(self):
    tree = self.load_tree_from('L2035')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2037(self):
    tree = self.load_tree_from('L2037')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['seats', 'students'])

  def test_L2038(self):
    tree = self.load_tree_from('L2038')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['colors'])

  def test_L2039(self):
    tree = self.load_tree_from('L2039')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['edges', 'patience'])

  def test_L2042(self):
    tree = self.load_tree_from('L2042')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L2044(self):
    tree = self.load_tree_from('L2044')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2045(self):
    tree = self.load_tree_from('L2045')
    self.param_collector.visit(tree.root_node)
    # uses time as variable
    # self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'edges', 'time', 'change'])

  def test_L2047(self):
    tree = self.load_tree_from('L2047')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['sentence'])

  def test_L2048(self):
    tree = self.load_tree_from('L2048')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L2049(self):
    tree = self.load_tree_from('L2049')
    self.param_collector.visit(tree.root_node)
    # uses inf
    # self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['parents'])

  def test_L2052(self):
    tree = self.load_tree_from('L2052')
    self.param_collector.visit(tree.root_node)
    # uses inf
    # self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['sentence', 'k'])

  def test_L2053(self):
    tree = self.load_tree_from('L2053')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr', 'k'])

  def test_L2055(self):
    tree = self.load_tree_from('L2055')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'queries'])

  def test_L2057(self):
    tree = self.load_tree_from('L2057')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2059(self):
    tree = self.load_tree_from('L2059')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'start', 'goal'])

  def test_L2063(self):
    tree = self.load_tree_from('L2063')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['word'])

  def test_L2064(self):
    tree = self.load_tree_from('L2064')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'quantities'])

  def test_L2067(self):
    tree = self.load_tree_from('L2067')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'count'])

  def test_L2068(self):
    tree = self.load_tree_from('L2068')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['word1', 'word2'])

  def test_L2073(self):
    tree = self.load_tree_from('L2073')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['tickets', 'k'])

  def test_L2075(self):
    tree = self.load_tree_from('L2075')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['encodedText', 'rows'])

  def test_L2076(self):
    tree = self.load_tree_from('L2076')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'restrictions', 'requests'])

  def test_L2078(self):
    tree = self.load_tree_from('L2078')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['colors'])

  def test_L2079(self):
    tree = self.load_tree_from('L2079')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['plants', 'capacity'])

  def test_L2083(self):
    tree = self.load_tree_from('L2083')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L2085(self):
    tree = self.load_tree_from('L2085')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['words1', 'words2'])

  def test_L2089(self):
    tree = self.load_tree_from('L2089')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'target'])

  def test_L2090(self):
    tree = self.load_tree_from('L2090')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L2091(self):
    tree = self.load_tree_from('L2091')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2092(self):
    tree = self.load_tree_from('L2092')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'meetings', 'firstPerson'])

  def test_L2094(self):
    tree = self.load_tree_from('L2094')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['digits'])

  def test_L2099(self):
    tree = self.load_tree_from('L2099')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L2100(self):
    tree = self.load_tree_from('L2100')
    self.param_collector.visit(tree.root_node)
    # uses time as variable
    # self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['security', 'time'])

  def test_L2101(self):
    tree = self.load_tree_from('L2101')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['bombs'])

  def test_L2103(self):
    tree = self.load_tree_from('L2103')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['rings'])

  def test_L2104(self):
    tree = self.load_tree_from('L2104')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2105(self):
    tree = self.load_tree_from('L2105')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['plants', 'capacityA', 'capacityB'])

  def test_L2106(self):
    tree = self.load_tree_from('L2106')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['fruits', 'startPos', 'k'])

  def test_L2108(self):
    tree = self.load_tree_from('L2108')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['words'])

  def test_L2109(self):
    tree = self.load_tree_from('L2109')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'spaces'])

  def test_L2110(self):
    tree = self.load_tree_from('L2110')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['prices'])

  def test_L2114(self):
    tree = self.load_tree_from('L2114')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['sentences'])

  def test_L2119(self):
    tree = self.load_tree_from('L2119')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num'])

  def test_L2120(self):
    tree = self.load_tree_from('L2120')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'startPos', 's'])

  def test_L2121(self):
    tree = self.load_tree_from('L2121')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['arr'])

  def test_L2122(self):
    tree = self.load_tree_from('L2122')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2125(self):
    tree = self.load_tree_from('L2125')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['bank'])

  def test_L2132(self):
    tree = self.load_tree_from('L2132')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid', 'stampHeight', 'stampWidth'])

  def test_L2133(self):
    tree = self.load_tree_from('L2133')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['matrix'])

  def test_L2134(self):
    tree = self.load_tree_from('L2134')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2135(self):
    tree = self.load_tree_from('L2135')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['startWords', 'targetWords'])

  def test_L2136(self):
    tree = self.load_tree_from('L2136')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['plantTime', 'growTime'])

  def test_L2138(self):
    tree = self.load_tree_from('L2138')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'k', 'fill'])

  def test_L2139(self):
    tree = self.load_tree_from('L2139')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['target', 'maxDoubles'])

  def test_L2140(self):
    tree = self.load_tree_from('L2140')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['questions'])

  def test_L2144(self):
    tree = self.load_tree_from('L2144')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['cost'])

  def test_L2145(self):
    tree = self.load_tree_from('L2145')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['differences', 'lower', 'upper'])

  def test_L2146(self):
    tree = self.load_tree_from('L2146')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid', 'pricing', 'start', 'k'])

  def test_L2148(self):
    tree = self.load_tree_from('L2148')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2149(self):
    tree = self.load_tree_from('L2149')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2150(self):
    tree = self.load_tree_from('L2150')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2151(self):
    tree = self.load_tree_from('L2151')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['statements'])

  def test_L2154(self):
    tree = self.load_tree_from('L2154')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'original'])

  def test_L2155(self):
    tree = self.load_tree_from('L2155')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2157(self):
    tree = self.load_tree_from('L2157')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['words'])

  def test_L2160(self):
    tree = self.load_tree_from('L2160')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num'])

  def test_L2161(self):
    tree = self.load_tree_from('L2161')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'pivot'])

  def test_L2162(self):
    tree = self.load_tree_from('L2162')
    self.param_collector.visit(tree.root_node)
    # uses inf
    # self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['startAt', 'moveCost', 'pushCost', 'targetSeconds'])

  def test_L2164(self):
    tree = self.load_tree_from('L2164')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2165(self):
    tree = self.load_tree_from('L2165')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num'])

  def test_L2167(self):
    tree = self.load_tree_from('L2167')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L2168(self):
    tree = self.load_tree_from('L2168')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L2169(self):
    tree = self.load_tree_from('L2169')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num1', 'num2'])

  def test_L2170(self):
    tree = self.load_tree_from('L2170')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2171(self):
    tree = self.load_tree_from('L2171')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['beans'])

  def test_L2174(self):
    tree = self.load_tree_from('L2174')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L2176(self):
    tree = self.load_tree_from('L2176')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L2177(self):
    tree = self.load_tree_from('L2177')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num'])

  def test_L2178(self):
    tree = self.load_tree_from('L2178')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['finalSum'])

  def test_L2180(self):
    tree = self.load_tree_from('L2180')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num'])

  def test_L2182(self):
    tree = self.load_tree_from('L2182')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'repeatLimit'])

  def test_L2185(self):
    tree = self.load_tree_from('L2185')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['words', 'pref'])

  def test_L2186(self):
    tree = self.load_tree_from('L2186')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 't'])

  def test_L2190(self):
    tree = self.load_tree_from('L2190')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'key'])

  def test_L2191(self):
    tree = self.load_tree_from('L2191')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['mapping', 'nums'])

  def test_L2192(self):
    tree = self.load_tree_from('L2192')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'edges'])

  def test_L2193(self):
    tree = self.load_tree_from('L2193')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L2194(self):
    tree = self.load_tree_from('L2194')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L2198(self):
    tree = self.load_tree_from('L2198')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2200(self):
    tree = self.load_tree_from('L2200')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'key', 'k'])

  def test_L2201(self):
    tree = self.load_tree_from('L2201')
    self.param_collector.visit(tree.root_node)
    # removed `n` from the list of parametrizable identifiers
    # it is not used in the original function `f_gold`
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['artifacts', 'dig'])

  def test_L2202(self):
    tree = self.load_tree_from('L2202')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L2203(self):
    tree = self.load_tree_from('L2203')
    self.param_collector.visit(tree.root_node)
    # uses inf
    # self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'edges', 'src1', 'src2', 'dest'])

  def test_L2206(self):
    tree = self.load_tree_from('L2206')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2207(self):
    tree = self.load_tree_from('L2207')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['text', 'pattern'])

  def test_L2208(self):
    tree = self.load_tree_from('L2208')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2210(self):
    tree = self.load_tree_from('L2210')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2211(self):
    tree = self.load_tree_from('L2211')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['directions'])

  def test_L2212(self):
    tree = self.load_tree_from('L2212')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['numArrows', 'aliceArrows'])

  def test_L2214(self):
    tree = self.load_tree_from('L2214')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['damage', 'armor'])

  def test_L2215(self):
    tree = self.load_tree_from('L2215')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums1', 'nums2'])

  def test_L2216(self):
    tree = self.load_tree_from('L2216')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2217(self):
    tree = self.load_tree_from('L2217')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['queries', 'intLength'])

  def test_L2218(self):
    tree = self.load_tree_from('L2218')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['piles', 'k'])

  def test_L2219(self):
    tree = self.load_tree_from('L2219')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2220(self):
    tree = self.load_tree_from('L2220')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['start', 'goal'])

  def test_L2221(self):
    tree = self.load_tree_from('L2221')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2224(self):
    tree = self.load_tree_from('L2224')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['current', 'correct'])

  def test_L2225(self):
    tree = self.load_tree_from('L2225')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['matches'])

  def test_L2226(self):
    tree = self.load_tree_from('L2226')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['candies', 'k'])

  def test_L2229(self):
    tree = self.load_tree_from('L2229')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2235(self):
    tree = self.load_tree_from('L2235')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num1', 'num2'])

  def test_L2237(self):
    tree = self.load_tree_from('L2237')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'lights', 'requirement'])

  def test_L2239(self):
    tree = self.load_tree_from('L2239')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2240(self):
    tree = self.load_tree_from('L2240')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['total', 'cost1', 'cost2'])

  def test_L2243(self):
    tree = self.load_tree_from('L2243')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'k'])

  def test_L2244(self):
    tree = self.load_tree_from('L2244')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['tasks'])

  def test_L2248(self):
    tree = self.load_tree_from('L2248')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2249(self):
    tree = self.load_tree_from('L2249')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['circles'])

  def test_L2255(self):
    tree = self.load_tree_from('L2255')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['words', 's'])

  def test_L2256(self):
    tree = self.load_tree_from('L2256')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2257(self):
    tree = self.load_tree_from('L2257')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['m', 'n', 'guards', 'walls'])

  def test_L2258(self):
    tree = self.load_tree_from('L2258')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L2259(self):
    tree = self.load_tree_from('L2259')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['number', 'digit'])

  def test_L2260(self):
    tree = self.load_tree_from('L2260')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['cards'])

  def test_L2261(self):
    tree = self.load_tree_from('L2261')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k', 'p'])

  def test_L2262(self):
    tree = self.load_tree_from('L2262')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L2264(self):
    tree = self.load_tree_from('L2264')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num'])

  def test_L2267(self):
    tree = self.load_tree_from('L2267')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L2268(self):
    tree = self.load_tree_from('L2268')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L2269(self):
    tree = self.load_tree_from('L2269')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num', 'k'])

  def test_L2270(self):
    tree = self.load_tree_from('L2270')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2273(self):
    tree = self.load_tree_from('L2273')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['words'])

  def test_L2274(self):
    tree = self.load_tree_from('L2274')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['bottom', 'top', 'special'])

  def test_L2275(self):
    tree = self.load_tree_from('L2275')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['candidates'])

  def test_L2278(self):
    tree = self.load_tree_from('L2278')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'letter'])

  def test_L2279(self):
    tree = self.load_tree_from('L2279')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['capacity', 'rocks', 'additionalRocks'])

  def test_L2281(self):
    tree = self.load_tree_from('L2281')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['strength'])

  def test_L2283(self):
    tree = self.load_tree_from('L2283')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num'])

  def test_L2284(self):
    tree = self.load_tree_from('L2284')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['messages', 'senders'])

  def test_L2285(self):
    tree = self.load_tree_from('L2285')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'roads'])

  def test_L2287(self):
    tree = self.load_tree_from('L2287')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'target'])

  def test_L2288(self):
    tree = self.load_tree_from('L2288')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['sentence', 'discount'])

  def test_L2289(self):
    tree = self.load_tree_from('L2289')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2290(self):
    tree = self.load_tree_from('L2290')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L2291(self):
    tree = self.load_tree_from('L2291')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['present', 'future', 'budget'])

  def test_L2293(self):
    tree = self.load_tree_from('L2293')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2295(self):
    tree = self.load_tree_from('L2295')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'operations'])

  def test_L2299(self):
    tree = self.load_tree_from('L2299')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['password'])

  def test_L2301(self):
    tree = self.load_tree_from('L2301')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'sub', 'mappings'])

  def test_L2302(self):
    tree = self.load_tree_from('L2302')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'k'])

  def test_L2303(self):
    tree = self.load_tree_from('L2303')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['brackets', 'income'])

  def test_L2304(self):
    tree = self.load_tree_from('L2304')
    self.param_collector.visit(tree.root_node)
    # uses inf
    # self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid', 'moveCost'])

  def test_L2305(self):
    tree = self.load_tree_from('L2305')
    self.param_collector.visit(tree.root_node)
    # uses inf
    # self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['cookies', 'k'])

  def test_L2306(self):
    tree = self.load_tree_from('L2306')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['ideas'])

  def test_L2309(self):
    tree = self.load_tree_from('L2309')
    self.param_collector.visit(tree.root_node)
    # uses ascii_uppercase after import
    # self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L2310(self):
    tree = self.load_tree_from('L2310')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['num', 'k'])

  def test_L2311(self):
    tree = self.load_tree_from('L2311')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s', 'k'])

  def test_L2312(self):
    tree = self.load_tree_from('L2312')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['m', 'n', 'prices'])

  def test_L2315(self):
    tree = self.load_tree_from('L2315')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['s'])

  def test_L2316(self):
    tree = self.load_tree_from('L2316')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n', 'edges'])

  def test_L2317(self):
    tree = self.load_tree_from('L2317')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums'])

  def test_L2318(self):
    tree = self.load_tree_from('L2318')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L2319(self):
    tree = self.load_tree_from('L2319')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['grid'])

  def test_L2320(self):
    tree = self.load_tree_from('L2320')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['n'])

  def test_L2321(self):
    tree = self.load_tree_from('L2321')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums1', 'nums2'])

  def test_L2322(self):
    tree = self.load_tree_from('L2322')
    self.param_collector.visit(tree.root_node)
    # uses inf
    # self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['nums', 'edges'])

  def test_L2323(self):
    tree = self.load_tree_from('L2323')
    self.param_collector.visit(tree.root_node)
    self.assertCountEqual(self.param_collector.get_parametrizable_identifiers(), ['jobs', 'workers'])


class TestPrettyPrinter(unittest.TestCase):
  def setUp(self):
    self.snippets_dir = p_consts.TEST_ARTIFACTS_DIR / 'py' / 'TestPrettyPrinter'
    self.src_lang = 'py'
    self.parser = p_consts.PARSER_DICT[self.src_lang]
    self.pp = p_visitor_py.PrettyPrinter(indent_with='    ')
    self.maxDiff = None

  def load_test_subject(self, subject_name: str) -> Tuple[str, p_visitor_py.Tree]:
    for fpath in self.snippets_dir.iterdir():
      if fpath.name.startswith(subject_name):
        snippet_text = p_utils.read_text(fpath).strip()
        ts_tree = self.parser.parse(bytes(snippet_text, 'utf8'))
        tree = p_visitor_py.Tree.from_ts_tree(ts_tree)
        return snippet_text, tree
    raise FileNotFoundError(f"No file starting with '{subject_name}' found in {self.snippets_dir}")

  def test_L0001(self):
    gold_code, tree = self.load_test_subject('L0001')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0003(self):
    gold_code, tree = self.load_test_subject('L0003')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0004(self):
    gold_code, tree = self.load_test_subject('L0004')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0005(self):
    gold_code, tree = self.load_test_subject('L0005')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0006(self):
    gold_code, tree = self.load_test_subject('L0006')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0007(self):
    gold_code, tree = self.load_test_subject('L0007')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0008(self):
    gold_code, tree = self.load_test_subject('L0008')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0009(self):
    gold_code, tree = self.load_test_subject('L0009')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L00010(self):
    gold_code, tree = self.load_test_subject('L0010')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L00011(self):
    gold_code, tree = self.load_test_subject('L0011')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0012(self):
    gold_code, tree = self.load_test_subject('L0012')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0013(self):
    gold_code, tree = self.load_test_subject('L0013')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0014(self):
    gold_code, tree = self.load_test_subject('L0014')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0015(self):
    gold_code, tree = self.load_test_subject('L0015')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0016(self):
    gold_code, tree = self.load_test_subject('L0016')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0017(self):
    gold_code, tree = self.load_test_subject('L0017')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0018(self):
    gold_code, tree = self.load_test_subject('L0018')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0020(self):
    gold_code, tree = self.load_test_subject('L0020')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0022(self):
    gold_code, tree = self.load_test_subject('L0022')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0026(self):
    gold_code, tree = self.load_test_subject('L0026')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0027(self):
    gold_code, tree = self.load_test_subject('L0027')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0028(self):
    gold_code, tree = self.load_test_subject('L0028')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0029(self):
    gold_code, tree = self.load_test_subject('L0029')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0030(self):
    gold_code, tree = self.load_test_subject('L0030')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0032(self):
    gold_code, tree = self.load_test_subject('L0032')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0033(self):
    gold_code, tree = self.load_test_subject('L0033')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0035(self):
    gold_code, tree = self.load_test_subject('L0035')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0036(self):
    gold_code, tree = self.load_test_subject('L0036')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0038(self):
    gold_code, tree = self.load_test_subject('L0038')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0039(self):
    gold_code, tree = self.load_test_subject('L0039')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0040(self):
    gold_code, tree = self.load_test_subject('L0040')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0041(self):
    gold_code, tree = self.load_test_subject('L0041')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0042(self):
    gold_code, tree = self.load_test_subject('L0042')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0043(self):
    gold_code, tree = self.load_test_subject('L0043')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0045(self):
    gold_code, tree = self.load_test_subject('L0045')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0046(self):
    gold_code, tree = self.load_test_subject('L0046')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0047(self):
    gold_code, tree = self.load_test_subject('L0047')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0048(self):
    gold_code, tree = self.load_test_subject('L0048')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0049(self):
    gold_code, tree = self.load_test_subject('L0049')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0050(self):
    gold_code, tree = self.load_test_subject('L0050')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0051(self):
    gold_code, tree = self.load_test_subject('L0051')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0053(self):
    gold_code, tree = self.load_test_subject('L0053')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0054(self):
    gold_code, tree = self.load_test_subject('L0054')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0055(self):
    gold_code, tree = self.load_test_subject('L0055')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0056(self):
    gold_code, tree = self.load_test_subject('L0056')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0057(self):
    gold_code, tree = self.load_test_subject('L0057')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0058(self):
    gold_code, tree = self.load_test_subject('L0058')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0059(self):
    gold_code, tree = self.load_test_subject('L0059')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0062(self):
    gold_code, tree = self.load_test_subject('L0062')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0063(self):
    gold_code, tree = self.load_test_subject('L0063')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0064(self):
    gold_code, tree = self.load_test_subject('L0064')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0065(self):
    gold_code, tree = self.load_test_subject('L0065')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0066(self):
    gold_code, tree = self.load_test_subject('L0066')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0067(self):
    gold_code, tree = self.load_test_subject('L0067')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0068(self):
    gold_code, tree = self.load_test_subject('L0068')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0069(self):
    gold_code, tree = self.load_test_subject('L0069')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0070(self):
    gold_code, tree = self.load_test_subject('L0070')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0071(self):
    gold_code, tree = self.load_test_subject('L0071')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0072(self):
    gold_code, tree = self.load_test_subject('L0072')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0073(self):
    gold_code, tree = self.load_test_subject('L0073')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0074(self):
    gold_code, tree = self.load_test_subject('L0074')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0075(self):
    gold_code, tree = self.load_test_subject('L0075')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0076(self):
    gold_code, tree = self.load_test_subject('L0076')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0077(self):
    gold_code, tree = self.load_test_subject('L0077')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0078(self):
    gold_code, tree = self.load_test_subject('L0078')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0079(self):
    gold_code, tree = self.load_test_subject('L0079')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0080(self):
    gold_code, tree = self.load_test_subject('L0080')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0081(self):
    gold_code, tree = self.load_test_subject('L0081')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0084(self):
    gold_code, tree = self.load_test_subject('L0084')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0087(self):
    gold_code, tree = self.load_test_subject('L0087')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0088(self):
    gold_code, tree = self.load_test_subject('L0088')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0089(self):
    gold_code, tree = self.load_test_subject('L0089')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0090(self):
    gold_code, tree = self.load_test_subject('L0090')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0091(self):
    gold_code, tree = self.load_test_subject('L0091')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0093(self):
    gold_code, tree = self.load_test_subject('L0093')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0096(self):
    gold_code, tree = self.load_test_subject('L0096')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0097(self):
    gold_code, tree = self.load_test_subject('L0097')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0118(self):
    gold_code, tree = self.load_test_subject('L0118')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0119(self):
    gold_code, tree = self.load_test_subject('L0119')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0120(self):
    gold_code, tree = self.load_test_subject('L0120')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0121(self):
    gold_code, tree = self.load_test_subject('L0121')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0122(self):
    gold_code, tree = self.load_test_subject('L0122')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0123(self):
    gold_code, tree = self.load_test_subject('L0123')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0126(self):
    gold_code, tree = self.load_test_subject('L0126')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0127(self):
    gold_code, tree = self.load_test_subject('L0127')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0128(self):
    gold_code, tree = self.load_test_subject('L0128')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0130(self):
    gold_code, tree = self.load_test_subject('L0130')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0131(self):
    gold_code, tree = self.load_test_subject('L0131')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0132(self):
    gold_code, tree = self.load_test_subject('L0132')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0136(self):
    gold_code, tree = self.load_test_subject('L0136')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0137(self):
    gold_code, tree = self.load_test_subject('L0137')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0139(self):
    gold_code, tree = self.load_test_subject('L0139')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0149(self):
    gold_code, tree = self.load_test_subject('L0149')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0150(self):
    gold_code, tree = self.load_test_subject('L0150')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0151(self):
    gold_code, tree = self.load_test_subject('L0151')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0152(self):
    gold_code, tree = self.load_test_subject('L0152')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0153(self):
    gold_code, tree = self.load_test_subject('L0153')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0154(self):
    gold_code, tree = self.load_test_subject('L0154')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0159(self):
    gold_code, tree = self.load_test_subject('L0159')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0162(self):
    gold_code, tree = self.load_test_subject('L0162')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0165(self):
    gold_code, tree = self.load_test_subject('L0165')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0166(self):
    gold_code, tree = self.load_test_subject('L0166')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0167(self):
    gold_code, tree = self.load_test_subject('L0167')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0168(self):
    gold_code, tree = self.load_test_subject('L0168')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0169(self):
    gold_code, tree = self.load_test_subject('L0169')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0171(self):
    gold_code, tree = self.load_test_subject('L0171')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0172(self):
    gold_code, tree = self.load_test_subject('L0172')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0179(self):
    gold_code, tree = self.load_test_subject('L0179')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0186(self):
    gold_code, tree = self.load_test_subject('L0186')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0187(self):
    gold_code, tree = self.load_test_subject('L0187')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0188(self):
    gold_code, tree = self.load_test_subject('L0188')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0189(self):
    gold_code, tree = self.load_test_subject('L0189')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0198(self):
    gold_code, tree = self.load_test_subject('L0198')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0200(self):
    gold_code, tree = self.load_test_subject('L0200')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0201(self):
    gold_code, tree = self.load_test_subject('L0201')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0202(self):
    gold_code, tree = self.load_test_subject('L0202')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0204(self):
    gold_code, tree = self.load_test_subject('L0204')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0205(self):
    gold_code, tree = self.load_test_subject('L0205')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0207(self):
    gold_code, tree = self.load_test_subject('L0207')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0210(self):
    gold_code, tree = self.load_test_subject('L0210')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0212(self):
    gold_code, tree = self.load_test_subject('L0212')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0213(self):
    gold_code, tree = self.load_test_subject('L0213')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0214(self):
    gold_code, tree = self.load_test_subject('L0214')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0215(self):
    gold_code, tree = self.load_test_subject('L0215')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0216(self):
    gold_code, tree = self.load_test_subject('L0216')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0217(self):
    gold_code, tree = self.load_test_subject('L0217')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0219(self):
    gold_code, tree = self.load_test_subject('L0219')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0221(self):
    gold_code, tree = self.load_test_subject('L0221')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0223(self):
    gold_code, tree = self.load_test_subject('L0223')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0227(self):
    gold_code, tree = self.load_test_subject('L0227')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0228(self):
    gold_code, tree = self.load_test_subject('L0228')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0229(self):
    gold_code, tree = self.load_test_subject('L0229')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0231(self):
    gold_code, tree = self.load_test_subject('L0231')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0233(self):
    gold_code, tree = self.load_test_subject('L0233')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0238(self):
    gold_code, tree = self.load_test_subject('L0238')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0239(self):
    gold_code, tree = self.load_test_subject('L0239')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0240(self):
    gold_code, tree = self.load_test_subject('L0240')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0241(self):
    gold_code, tree = self.load_test_subject('L0241')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0242(self):
    gold_code, tree = self.load_test_subject('L0242')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0243(self):
    gold_code, tree = self.load_test_subject('L0243')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0245(self):
    gold_code, tree = self.load_test_subject('L0245')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0246(self):
    gold_code, tree = self.load_test_subject('L0246')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0247(self):
    gold_code, tree = self.load_test_subject('L0247')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0249(self):
    gold_code, tree = self.load_test_subject('L0249')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0252(self):
    gold_code, tree = self.load_test_subject('L0252')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0253(self):
    gold_code, tree = self.load_test_subject('L0253')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0255(self):
    gold_code, tree = self.load_test_subject('L0255')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0256(self):
    gold_code, tree = self.load_test_subject('L0256')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0258(self):
    gold_code, tree = self.load_test_subject('L0258')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0259(self):
    gold_code, tree = self.load_test_subject('L0259')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0260(self):
    gold_code, tree = self.load_test_subject('L0260')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0261(self):
    gold_code, tree = self.load_test_subject('L0261')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0263(self):
    gold_code, tree = self.load_test_subject('L0263')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0264(self):
    gold_code, tree = self.load_test_subject('L0264')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0266(self):
    gold_code, tree = self.load_test_subject('L0266')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0268(self):
    gold_code, tree = self.load_test_subject('L0268')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0269(self):
    gold_code, tree = self.load_test_subject('L0269')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0273(self):
    gold_code, tree = self.load_test_subject('L0273')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0274(self):
    gold_code, tree = self.load_test_subject('L0274')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0275(self):
    gold_code, tree = self.load_test_subject('L0275')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0279(self):
    gold_code, tree = self.load_test_subject('L0279')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0280(self):
    gold_code, tree = self.load_test_subject('L0280')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0282(self):
    gold_code, tree = self.load_test_subject('L0282')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0283(self):
    gold_code, tree = self.load_test_subject('L0283')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0286(self):
    gold_code, tree = self.load_test_subject('L0286')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0287(self):
    gold_code, tree = self.load_test_subject('L0287')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0289(self):
    gold_code, tree = self.load_test_subject('L0289')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0290(self):
    gold_code, tree = self.load_test_subject('L0290')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0291(self):
    gold_code, tree = self.load_test_subject('L0291')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0292(self):
    gold_code, tree = self.load_test_subject('L0292')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0293(self):
    gold_code, tree = self.load_test_subject('L0293')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0299(self):
    gold_code, tree = self.load_test_subject('L0299')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0301(self):
    gold_code, tree = self.load_test_subject('L0301')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0302(self):
    gold_code, tree = self.load_test_subject('L0302')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0305(self):
    gold_code, tree = self.load_test_subject('L0305')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0306(self):
    gold_code, tree = self.load_test_subject('L0306')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0309(self):
    gold_code, tree = self.load_test_subject('L0309')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0310(self):
    gold_code, tree = self.load_test_subject('L0310')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0311(self):
    gold_code, tree = self.load_test_subject('L0311')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0312(self):
    gold_code, tree = self.load_test_subject('L0312')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0317(self):
    gold_code, tree = self.load_test_subject('L0317')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0318(self):
    gold_code, tree = self.load_test_subject('L0318')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0320(self):
    gold_code, tree = self.load_test_subject('L0320')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0322(self):
    gold_code, tree = self.load_test_subject('L0322')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0323(self):
    gold_code, tree = self.load_test_subject('L0323')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0324(self):
    gold_code, tree = self.load_test_subject('L0324')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0325(self):
    gold_code, tree = self.load_test_subject('L0325')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0329(self):
    gold_code, tree = self.load_test_subject('L0329')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0334(self):
    gold_code, tree = self.load_test_subject('L0334')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0335(self):
    gold_code, tree = self.load_test_subject('L0335')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0338(self):
    gold_code, tree = self.load_test_subject('L0338')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0342(self):
    gold_code, tree = self.load_test_subject('L0342')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0343(self):
    gold_code, tree = self.load_test_subject('L0343')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0344(self):
    gold_code, tree = self.load_test_subject('L0344')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0345(self):
    gold_code, tree = self.load_test_subject('L0345')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0347(self):
    gold_code, tree = self.load_test_subject('L0347')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0349(self):
    gold_code, tree = self.load_test_subject('L0349')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0350(self):
    gold_code, tree = self.load_test_subject('L0350')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0356(self):
    gold_code, tree = self.load_test_subject('L0356')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0357(self):
    gold_code, tree = self.load_test_subject('L0357')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0360(self):
    gold_code, tree = self.load_test_subject('L0360')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0361(self):
    gold_code, tree = self.load_test_subject('L0361')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0365(self):
    gold_code, tree = self.load_test_subject('L0365')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0367(self):
    gold_code, tree = self.load_test_subject('L0367')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0368(self):
    gold_code, tree = self.load_test_subject('L0368')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0370(self):
    gold_code, tree = self.load_test_subject('L0370')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0371(self):
    gold_code, tree = self.load_test_subject('L0371')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0372(self):
    gold_code, tree = self.load_test_subject('L0372')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0373(self):
    gold_code, tree = self.load_test_subject('L0373')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0375(self):
    gold_code, tree = self.load_test_subject('L0375')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0376(self):
    gold_code, tree = self.load_test_subject('L0376')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0377(self):
    gold_code, tree = self.load_test_subject('L0377')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0378(self):
    gold_code, tree = self.load_test_subject('L0378')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0383(self):
    gold_code, tree = self.load_test_subject('L0383')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0386(self):
    gold_code, tree = self.load_test_subject('L0386')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0387(self):
    gold_code, tree = self.load_test_subject('L0387')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0388(self):
    gold_code, tree = self.load_test_subject('L0388')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0389(self):
    gold_code, tree = self.load_test_subject('L0389')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0390(self):
    gold_code, tree = self.load_test_subject('L0390')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0391(self):
    gold_code, tree = self.load_test_subject('L0391')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0392(self):
    gold_code, tree = self.load_test_subject('L0392')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0393(self):
    gold_code, tree = self.load_test_subject('L0393')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0394(self):
    gold_code, tree = self.load_test_subject('L0394')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0395(self):
    gold_code, tree = self.load_test_subject('L0395')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0396(self):
    gold_code, tree = self.load_test_subject('L0396')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0397(self):
    gold_code, tree = self.load_test_subject('L0397')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0399(self):
    gold_code, tree = self.load_test_subject('L0399')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0400(self):
    gold_code, tree = self.load_test_subject('L0400')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0401(self):
    gold_code, tree = self.load_test_subject('L0401')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0403(self):
    gold_code, tree = self.load_test_subject('L0403')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0405(self):
    gold_code, tree = self.load_test_subject('L0405')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0406(self):
    gold_code, tree = self.load_test_subject('L0406')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0407(self):
    gold_code, tree = self.load_test_subject('L0407')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0409(self):
    gold_code, tree = self.load_test_subject('L0409')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0410(self):
    gold_code, tree = self.load_test_subject('L0410')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0412(self):
    gold_code, tree = self.load_test_subject('L0412')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0413(self):
    gold_code, tree = self.load_test_subject('L0413')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0414(self):
    gold_code, tree = self.load_test_subject('L0414')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0415(self):
    gold_code, tree = self.load_test_subject('L0415')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0416(self):
    gold_code, tree = self.load_test_subject('L0416')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0417(self):
    gold_code, tree = self.load_test_subject('L0417')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0419(self):
    gold_code, tree = self.load_test_subject('L0419')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0420(self):
    gold_code, tree = self.load_test_subject('L0420')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0421(self):
    gold_code, tree = self.load_test_subject('L0421')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0423(self):
    gold_code, tree = self.load_test_subject('L0423')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0424(self):
    gold_code, tree = self.load_test_subject('L0424')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0433(self):
    gold_code, tree = self.load_test_subject('L0433')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0434(self):
    gold_code, tree = self.load_test_subject('L0434')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0435(self):
    gold_code, tree = self.load_test_subject('L0435')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0438(self):
    gold_code, tree = self.load_test_subject('L0438')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0440(self):
    gold_code, tree = self.load_test_subject('L0440')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0441(self):
    gold_code, tree = self.load_test_subject('L0441')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0442(self):
    gold_code, tree = self.load_test_subject('L0442')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0443(self):
    gold_code, tree = self.load_test_subject('L0443')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0444(self):
    gold_code, tree = self.load_test_subject('L0444')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0447(self):
    gold_code, tree = self.load_test_subject('L0447')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0448(self):
    gold_code, tree = self.load_test_subject('L0448')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0451(self):
    gold_code, tree = self.load_test_subject('L0451')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0453(self):
    gold_code, tree = self.load_test_subject('L0453')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0454(self):
    gold_code, tree = self.load_test_subject('L0454')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0456(self):
    gold_code, tree = self.load_test_subject('L0456')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0457(self):
    gold_code, tree = self.load_test_subject('L0457')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0458(self):
    gold_code, tree = self.load_test_subject('L0458')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0461(self):
    gold_code, tree = self.load_test_subject('L0461')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0462(self):
    gold_code, tree = self.load_test_subject('L0462')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0463(self):
    gold_code, tree = self.load_test_subject('L0463')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0464(self):
    gold_code, tree = self.load_test_subject('L0464')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0467(self):
    gold_code, tree = self.load_test_subject('L0467')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0473(self):
    gold_code, tree = self.load_test_subject('L0473')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0474(self):
    gold_code, tree = self.load_test_subject('L0474')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0475(self):
    gold_code, tree = self.load_test_subject('L0475')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0477(self):
    gold_code, tree = self.load_test_subject('L0477')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0479(self):
    gold_code, tree = self.load_test_subject('L0479')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0482(self):
    gold_code, tree = self.load_test_subject('L0482')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0485(self):
    gold_code, tree = self.load_test_subject('L0485')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0487(self):
    gold_code, tree = self.load_test_subject('L0487')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0488(self):
    gold_code, tree = self.load_test_subject('L0488')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0490(self):
    gold_code, tree = self.load_test_subject('L0490')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0491(self):
    gold_code, tree = self.load_test_subject('L0491')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0492(self):
    gold_code, tree = self.load_test_subject('L0492')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0494(self):
    gold_code, tree = self.load_test_subject('L0494')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0495(self):
    gold_code, tree = self.load_test_subject('L0495')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0496(self):
    gold_code, tree = self.load_test_subject('L0496')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0498(self):
    gold_code, tree = self.load_test_subject('L0498')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0499(self):
    gold_code, tree = self.load_test_subject('L0499')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0500(self):
    gold_code, tree = self.load_test_subject('L0500')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0503(self):
    gold_code, tree = self.load_test_subject('L0503')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0504(self):
    gold_code, tree = self.load_test_subject('L0504')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0505(self):
    gold_code, tree = self.load_test_subject('L0505')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0506(self):
    gold_code, tree = self.load_test_subject('L0506')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0507(self):
    gold_code, tree = self.load_test_subject('L0507')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0509(self):
    gold_code, tree = self.load_test_subject('L0509')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0516(self):
    gold_code, tree = self.load_test_subject('L0516')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0518(self):
    gold_code, tree = self.load_test_subject('L0518')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0520(self):
    gold_code, tree = self.load_test_subject('L0520')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0521(self):
    gold_code, tree = self.load_test_subject('L0521')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0522(self):
    gold_code, tree = self.load_test_subject('L0522')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0523(self):
    gold_code, tree = self.load_test_subject('L0523')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0524(self):
    gold_code, tree = self.load_test_subject('L0524')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0525(self):
    gold_code, tree = self.load_test_subject('L0525')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0526(self):
    gold_code, tree = self.load_test_subject('L0526')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0531(self):
    gold_code, tree = self.load_test_subject('L0531')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0532(self):
    gold_code, tree = self.load_test_subject('L0532')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0533(self):
    gold_code, tree = self.load_test_subject('L0533')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0537(self):
    gold_code, tree = self.load_test_subject('L0537')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0539(self):
    gold_code, tree = self.load_test_subject('L0539')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0540(self):
    gold_code, tree = self.load_test_subject('L0540')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0541(self):
    gold_code, tree = self.load_test_subject('L0541')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0542(self):
    gold_code, tree = self.load_test_subject('L0542')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0544(self):
    gold_code, tree = self.load_test_subject('L0544')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0547(self):
    gold_code, tree = self.load_test_subject('L0547')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0548(self):
    gold_code, tree = self.load_test_subject('L0548')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0551(self):
    gold_code, tree = self.load_test_subject('L0551')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0552(self):
    gold_code, tree = self.load_test_subject('L0552')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0553(self):
    gold_code, tree = self.load_test_subject('L0553')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0554(self):
    gold_code, tree = self.load_test_subject('L0554')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0557(self):
    gold_code, tree = self.load_test_subject('L0557')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0560(self):
    gold_code, tree = self.load_test_subject('L0560')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0561(self):
    gold_code, tree = self.load_test_subject('L0561')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0564(self):
    gold_code, tree = self.load_test_subject('L0564')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0565(self):
    gold_code, tree = self.load_test_subject('L0565')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0566(self):
    gold_code, tree = self.load_test_subject('L0566')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0567(self):
    gold_code, tree = self.load_test_subject('L0567')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0575(self):
    gold_code, tree = self.load_test_subject('L0575')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0581(self):
    gold_code, tree = self.load_test_subject('L0581')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0582(self):
    gold_code, tree = self.load_test_subject('L0582')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0583(self):
    gold_code, tree = self.load_test_subject('L0583')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0587(self):
    gold_code, tree = self.load_test_subject('L0587')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0591(self):
    gold_code, tree = self.load_test_subject('L0591')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0594(self):
    gold_code, tree = self.load_test_subject('L0594')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0598(self):
    gold_code, tree = self.load_test_subject('L0598')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0599(self):
    gold_code, tree = self.load_test_subject('L0599')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0605(self):
    gold_code, tree = self.load_test_subject('L0605')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0609(self):
    gold_code, tree = self.load_test_subject('L0609')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0628(self):
    gold_code, tree = self.load_test_subject('L0628')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0629(self):
    gold_code, tree = self.load_test_subject('L0629')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0630(self):
    gold_code, tree = self.load_test_subject('L0630')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0633(self):
    gold_code, tree = self.load_test_subject('L0633')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0638(self):
    gold_code, tree = self.load_test_subject('L0638')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0639(self):
    gold_code, tree = self.load_test_subject('L0639')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0643(self):
    gold_code, tree = self.load_test_subject('L0643')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0645(self):
    gold_code, tree = self.load_test_subject('L0645')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0646(self):
    gold_code, tree = self.load_test_subject('L0646')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0647(self):
    gold_code, tree = self.load_test_subject('L0647')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0657(self):
    gold_code, tree = self.load_test_subject('L0657')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0658(self):
    gold_code, tree = self.load_test_subject('L0658')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0661(self):
    gold_code, tree = self.load_test_subject('L0661')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0665(self):
    gold_code, tree = self.load_test_subject('L0665')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0666(self):
    gold_code, tree = self.load_test_subject('L0666')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0668(self):
    gold_code, tree = self.load_test_subject('L0668')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0670(self):
    gold_code, tree = self.load_test_subject('L0670')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0673(self):
    gold_code, tree = self.load_test_subject('L0673')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0674(self):
    gold_code, tree = self.load_test_subject('L0674')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0675(self):
    gold_code, tree = self.load_test_subject('L0675')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0678(self):
    gold_code, tree = self.load_test_subject('L0678')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0680(self):
    gold_code, tree = self.load_test_subject('L0680')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0681(self):
    gold_code, tree = self.load_test_subject('L0681')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0682(self):
    gold_code, tree = self.load_test_subject('L0682')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0684(self):
    gold_code, tree = self.load_test_subject('L0684')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0686(self):
    gold_code, tree = self.load_test_subject('L0686')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0688(self):
    gold_code, tree = self.load_test_subject('L0688')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0689(self):
    gold_code, tree = self.load_test_subject('L0689')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0691(self):
    gold_code, tree = self.load_test_subject('L0691')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0692(self):
    gold_code, tree = self.load_test_subject('L0692')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0693(self):
    gold_code, tree = self.load_test_subject('L0693')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0694(self):
    gold_code, tree = self.load_test_subject('L0694')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0695(self):
    gold_code, tree = self.load_test_subject('L0695')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0696(self):
    gold_code, tree = self.load_test_subject('L0696')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0697(self):
    gold_code, tree = self.load_test_subject('L0697')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0698(self):
    gold_code, tree = self.load_test_subject('L0698')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0704(self):
    gold_code, tree = self.load_test_subject('L0704')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0709(self):
    gold_code, tree = self.load_test_subject('L0709')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0711(self):
    gold_code, tree = self.load_test_subject('L0711')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0712(self):
    gold_code, tree = self.load_test_subject('L0712')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0713(self):
    gold_code, tree = self.load_test_subject('L0713')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0714(self):
    gold_code, tree = self.load_test_subject('L0714')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0717(self):
    gold_code, tree = self.load_test_subject('L0717')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0718(self):
    gold_code, tree = self.load_test_subject('L0718')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0720(self):
    gold_code, tree = self.load_test_subject('L0720')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0721(self):
    gold_code, tree = self.load_test_subject('L0721')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0723(self):
    gold_code, tree = self.load_test_subject('L0723')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0724(self):
    gold_code, tree = self.load_test_subject('L0724')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0728(self):
    gold_code, tree = self.load_test_subject('L0728')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0730(self):
    gold_code, tree = self.load_test_subject('L0730')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0733(self):
    gold_code, tree = self.load_test_subject('L0733')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0734(self):
    gold_code, tree = self.load_test_subject('L0734')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0735(self):
    gold_code, tree = self.load_test_subject('L0735')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0737(self):
    gold_code, tree = self.load_test_subject('L0737')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0739(self):
    gold_code, tree = self.load_test_subject('L0739')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0740(self):
    gold_code, tree = self.load_test_subject('L0740')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0741(self):
    gold_code, tree = self.load_test_subject('L0741')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0743(self):
    gold_code, tree = self.load_test_subject('L0743')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0744(self):
    gold_code, tree = self.load_test_subject('L0744')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0746(self):
    gold_code, tree = self.load_test_subject('L0746')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0747(self):
    gold_code, tree = self.load_test_subject('L0747')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0748(self):
    gold_code, tree = self.load_test_subject('L0748')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0749(self):
    gold_code, tree = self.load_test_subject('L0749')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0752(self):
    gold_code, tree = self.load_test_subject('L0752')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0760(self):
    gold_code, tree = self.load_test_subject('L0760')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0763(self):
    gold_code, tree = self.load_test_subject('L0763')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0765(self):
    gold_code, tree = self.load_test_subject('L0765')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0766(self):
    gold_code, tree = self.load_test_subject('L0766')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0767(self):
    gold_code, tree = self.load_test_subject('L0767')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0768(self):
    gold_code, tree = self.load_test_subject('L0768')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0769(self):
    gold_code, tree = self.load_test_subject('L0769')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0771(self):
    gold_code, tree = self.load_test_subject('L0771')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0773(self):
    gold_code, tree = self.load_test_subject('L0773')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0778(self):
    gold_code, tree = self.load_test_subject('L0778')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0779(self):
    gold_code, tree = self.load_test_subject('L0779')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0780(self):
    gold_code, tree = self.load_test_subject('L0780')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0781(self):
    gold_code, tree = self.load_test_subject('L0781')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0784(self):
    gold_code, tree = self.load_test_subject('L0784')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0785(self):
    gold_code, tree = self.load_test_subject('L0785')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0786(self):
    gold_code, tree = self.load_test_subject('L0786')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0787(self):
    gold_code, tree = self.load_test_subject('L0787')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0789(self):
    gold_code, tree = self.load_test_subject('L0789')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0792(self):
    gold_code, tree = self.load_test_subject('L0792')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0794(self):
    gold_code, tree = self.load_test_subject('L0794')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0796(self):
    gold_code, tree = self.load_test_subject('L0796')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0797(self):
    gold_code, tree = self.load_test_subject('L0797')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0798(self):
    gold_code, tree = self.load_test_subject('L0798')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0800(self):
    gold_code, tree = self.load_test_subject('L0800')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0802(self):
    gold_code, tree = self.load_test_subject('L0802')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0803(self):
    gold_code, tree = self.load_test_subject('L0803')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0804(self):
    gold_code, tree = self.load_test_subject('L0804')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0806(self):
    gold_code, tree = self.load_test_subject('L0806')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0807(self):
    gold_code, tree = self.load_test_subject('L0807')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0811(self):
    gold_code, tree = self.load_test_subject('L0811')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0812(self):
    gold_code, tree = self.load_test_subject('L0812')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0816(self):
    gold_code, tree = self.load_test_subject('L0816')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0819(self):
    gold_code, tree = self.load_test_subject('L0819')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0821(self):
    gold_code, tree = self.load_test_subject('L0821')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0822(self):
    gold_code, tree = self.load_test_subject('L0822')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0824(self):
    gold_code, tree = self.load_test_subject('L0824')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0825(self):
    gold_code, tree = self.load_test_subject('L0825')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0826(self):
    gold_code, tree = self.load_test_subject('L0826')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0827(self):
    gold_code, tree = self.load_test_subject('L0827')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0829(self):
    gold_code, tree = self.load_test_subject('L0829')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0832(self):
    gold_code, tree = self.load_test_subject('L0832')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0838(self):
    gold_code, tree = self.load_test_subject('L0838')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0839(self):
    gold_code, tree = self.load_test_subject('L0839')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0841(self):
    gold_code, tree = self.load_test_subject('L0841')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0844(self):
    gold_code, tree = self.load_test_subject('L0844')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0845(self):
    gold_code, tree = self.load_test_subject('L0845')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0847(self):
    gold_code, tree = self.load_test_subject('L0847')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0848(self):
    gold_code, tree = self.load_test_subject('L0848')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0851(self):
    gold_code, tree = self.load_test_subject('L0851')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0852(self):
    gold_code, tree = self.load_test_subject('L0852')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0853(self):
    gold_code, tree = self.load_test_subject('L0853')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0854(self):
    gold_code, tree = self.load_test_subject('L0854')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0859(self):
    gold_code, tree = self.load_test_subject('L0859')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0860(self):
    gold_code, tree = self.load_test_subject('L0860')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0861(self):
    gold_code, tree = self.load_test_subject('L0861')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0862(self):
    gold_code, tree = self.load_test_subject('L0862')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0864(self):
    gold_code, tree = self.load_test_subject('L0864')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0867(self):
    gold_code, tree = self.load_test_subject('L0867')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0868(self):
    gold_code, tree = self.load_test_subject('L0868')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0869(self):
    gold_code, tree = self.load_test_subject('L0869')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0873(self):
    gold_code, tree = self.load_test_subject('L0873')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0875(self):
    gold_code, tree = self.load_test_subject('L0875')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0881(self):
    gold_code, tree = self.load_test_subject('L0881')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0883(self):
    gold_code, tree = self.load_test_subject('L0883')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0884(self):
    gold_code, tree = self.load_test_subject('L0884')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0885(self):
    gold_code, tree = self.load_test_subject('L0885')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0886(self):
    gold_code, tree = self.load_test_subject('L0886')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0887(self):
    gold_code, tree = self.load_test_subject('L0887')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0888(self):
    gold_code, tree = self.load_test_subject('L0888')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0890(self):
    gold_code, tree = self.load_test_subject('L0890')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0893(self):
    gold_code, tree = self.load_test_subject('L0893')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0896(self):
    gold_code, tree = self.load_test_subject('L0896')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0898(self):
    gold_code, tree = self.load_test_subject('L0898')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0904(self):
    gold_code, tree = self.load_test_subject('L0904')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0905(self):
    gold_code, tree = self.load_test_subject('L0905')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0907(self):
    gold_code, tree = self.load_test_subject('L0907')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0908(self):
    gold_code, tree = self.load_test_subject('L0908')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0909(self):
    gold_code, tree = self.load_test_subject('L0909')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0912(self):
    gold_code, tree = self.load_test_subject('L0912')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0914(self):
    gold_code, tree = self.load_test_subject('L0914')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0915(self):
    gold_code, tree = self.load_test_subject('L0915')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0917(self):
    gold_code, tree = self.load_test_subject('L0917')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0918(self):
    gold_code, tree = self.load_test_subject('L0918')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0921(self):
    gold_code, tree = self.load_test_subject('L0921')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0922(self):
    gold_code, tree = self.load_test_subject('L0922')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0924(self):
    gold_code, tree = self.load_test_subject('L0924')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0925(self):
    gold_code, tree = self.load_test_subject('L0925')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0926(self):
    gold_code, tree = self.load_test_subject('L0926')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0927(self):
    gold_code, tree = self.load_test_subject('L0927')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0928(self):
    gold_code, tree = self.load_test_subject('L0928')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0929(self):
    gold_code, tree = self.load_test_subject('L0929')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0930(self):
    gold_code, tree = self.load_test_subject('L0930')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0931(self):
    gold_code, tree = self.load_test_subject('L0931')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0932(self):
    gold_code, tree = self.load_test_subject('L0932')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0934(self):
    gold_code, tree = self.load_test_subject('L0934')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0935(self):
    gold_code, tree = self.load_test_subject('L0935')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0937(self):
    gold_code, tree = self.load_test_subject('L0937')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0941(self):
    gold_code, tree = self.load_test_subject('L0941')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0942(self):
    gold_code, tree = self.load_test_subject('L0942')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0944(self):
    gold_code, tree = self.load_test_subject('L0944')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0946(self):
    gold_code, tree = self.load_test_subject('L0946')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0947(self):
    gold_code, tree = self.load_test_subject('L0947')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0953(self):
    gold_code, tree = self.load_test_subject('L0953')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0954(self):
    gold_code, tree = self.load_test_subject('L0954')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0959(self):
    gold_code, tree = self.load_test_subject('L0959')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0960(self):
    gold_code, tree = self.load_test_subject('L0960')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0961(self):
    gold_code, tree = self.load_test_subject('L0961')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0962(self):
    gold_code, tree = self.load_test_subject('L0962')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0967(self):
    gold_code, tree = self.load_test_subject('L0967')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0969(self):
    gold_code, tree = self.load_test_subject('L0969')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0970(self):
    gold_code, tree = self.load_test_subject('L0970')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0974(self):
    gold_code, tree = self.load_test_subject('L0974')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0977(self):
    gold_code, tree = self.load_test_subject('L0977')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0985(self):
    gold_code, tree = self.load_test_subject('L0985')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0986(self):
    '''
    exclude this test case due to a bug in tree-sitter
    the current version of tree-sitter we are using
    cannot parse the program correctly (has ERROR)
    '''
    # gold_code, tree = self.load_test_subject('L0986')
    # pp_code = self.pp.visit(tree.root_node).strip()
    # self.assertEqual(pp_code, gold_code)

  def test_L0989(self):
    gold_code, tree = self.load_test_subject('L0989')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0990(self):
    gold_code, tree = self.load_test_subject('L0990')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0994(self):
    gold_code, tree = self.load_test_subject('L0994')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0997(self):
    gold_code, tree = self.load_test_subject('L0997')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L0999(self):
    gold_code, tree = self.load_test_subject('L0999')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1001(self):
    gold_code, tree = self.load_test_subject('L1001')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1002(self):
    gold_code, tree = self.load_test_subject('L1002')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1004(self):
    gold_code, tree = self.load_test_subject('L1004')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1005(self):
    gold_code, tree = self.load_test_subject('L1005')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1006(self):
    gold_code, tree = self.load_test_subject('L1006')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1007(self):
    gold_code, tree = self.load_test_subject('L1007')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1009(self):
    gold_code, tree = self.load_test_subject('L1009')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1011(self):
    gold_code, tree = self.load_test_subject('L1011')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1014(self):
    gold_code, tree = self.load_test_subject('L1014')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1016(self):
    gold_code, tree = self.load_test_subject('L1016')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1020(self):
    gold_code, tree = self.load_test_subject('L1020')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1021(self):
    gold_code, tree = self.load_test_subject('L1021')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1027(self):
    gold_code, tree = self.load_test_subject('L1027')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1029(self):
    gold_code, tree = self.load_test_subject('L1029')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1030(self):
    gold_code, tree = self.load_test_subject('L1030')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1031(self):
    gold_code, tree = self.load_test_subject('L1031')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1034(self):
    gold_code, tree = self.load_test_subject('L1034')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1035(self):
    gold_code, tree = self.load_test_subject('L1035')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1037(self):
    gold_code, tree = self.load_test_subject('L1037')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1041(self):
    gold_code, tree = self.load_test_subject('L1041')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1042(self):
    gold_code, tree = self.load_test_subject('L1042')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1044(self):
    gold_code, tree = self.load_test_subject('L1044')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1046(self):
    gold_code, tree = self.load_test_subject('L1046')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1047(self):
    gold_code, tree = self.load_test_subject('L1047')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1048(self):
    gold_code, tree = self.load_test_subject('L1048')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1049(self):
    gold_code, tree = self.load_test_subject('L1049')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1051(self):
    gold_code, tree = self.load_test_subject('L1051')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1052(self):
    gold_code, tree = self.load_test_subject('L1052')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1061(self):
    gold_code, tree = self.load_test_subject('L1061')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1064(self):
    gold_code, tree = self.load_test_subject('L1064')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1072(self):
    gold_code, tree = self.load_test_subject('L1072')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1078(self):
    gold_code, tree = self.load_test_subject('L1078')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1079(self):
    gold_code, tree = self.load_test_subject('L1079')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1085(self):
    gold_code, tree = self.load_test_subject('L1085')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1087(self):
    gold_code, tree = self.load_test_subject('L1087')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1089(self):
    gold_code, tree = self.load_test_subject('L1089')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1090(self):
    gold_code, tree = self.load_test_subject('L1090')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1091(self):
    gold_code, tree = self.load_test_subject('L1091')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1094(self):
    gold_code, tree = self.load_test_subject('L1094')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1099(self):
    gold_code, tree = self.load_test_subject('L1099')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1100(self):
    gold_code, tree = self.load_test_subject('L1100')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1101(self):
    gold_code, tree = self.load_test_subject('L1101')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1102(self):
    gold_code, tree = self.load_test_subject('L1102')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1103(self):
    gold_code, tree = self.load_test_subject('L1103')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1105(self):
    gold_code, tree = self.load_test_subject('L1105')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1108(self):
    gold_code, tree = self.load_test_subject('L1108')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1109(self):
    gold_code, tree = self.load_test_subject('L1109')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1118(self):
    gold_code, tree = self.load_test_subject('L1118')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1119(self):
    gold_code, tree = self.load_test_subject('L1119')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1122(self):
    gold_code, tree = self.load_test_subject('L1122')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1124(self):
    gold_code, tree = self.load_test_subject('L1124')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1128(self):
    gold_code, tree = self.load_test_subject('L1128')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1129(self):
    gold_code, tree = self.load_test_subject('L1129')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1133(self):
    gold_code, tree = self.load_test_subject('L1133')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1134(self):
    gold_code, tree = self.load_test_subject('L1134')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1135(self):
    gold_code, tree = self.load_test_subject('L1135')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1137(self):
    gold_code, tree = self.load_test_subject('L1137')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1143(self):
    gold_code, tree = self.load_test_subject('L1143')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1154(self):
    gold_code, tree = self.load_test_subject('L1154')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1160(self):
    gold_code, tree = self.load_test_subject('L1160')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1162(self):
    gold_code, tree = self.load_test_subject('L1162')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1165(self):
    gold_code, tree = self.load_test_subject('L1165')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1167(self):
    gold_code, tree = self.load_test_subject('L1167')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1168(self):
    gold_code, tree = self.load_test_subject('L1168')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1175(self):
    gold_code, tree = self.load_test_subject('L1175')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1180(self):
    gold_code, tree = self.load_test_subject('L1180')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1181(self):
    gold_code, tree = self.load_test_subject('L1181')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1182(self):
    gold_code, tree = self.load_test_subject('L1182')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1185(self):
    gold_code, tree = self.load_test_subject('L1185')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1189(self):
    gold_code, tree = self.load_test_subject('L1189')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1190(self):
    gold_code, tree = self.load_test_subject('L1190')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1197(self):
    gold_code, tree = self.load_test_subject('L1197')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1198(self):
    gold_code, tree = self.load_test_subject('L1198')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1202(self):
    gold_code, tree = self.load_test_subject('L1202')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1207(self):
    gold_code, tree = self.load_test_subject('L1207')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1208(self):
    gold_code, tree = self.load_test_subject('L1208')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1210(self):
    gold_code, tree = self.load_test_subject('L1210')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1213(self):
    gold_code, tree = self.load_test_subject('L1213')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1217(self):
    gold_code, tree = self.load_test_subject('L1217')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1218(self):
    gold_code, tree = self.load_test_subject('L1218')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1219(self):
    gold_code, tree = self.load_test_subject('L1219')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1220(self):
    gold_code, tree = self.load_test_subject('L1220')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1221(self):
    gold_code, tree = self.load_test_subject('L1221')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1222(self):
    gold_code, tree = self.load_test_subject('L1222')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1228(self):
    gold_code, tree = self.load_test_subject('L1228')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1230(self):
    gold_code, tree = self.load_test_subject('L1230')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1234(self):
    gold_code, tree = self.load_test_subject('L1234')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1239(self):
    gold_code, tree = self.load_test_subject('L1239')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1243(self):
    gold_code, tree = self.load_test_subject('L1243')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1245(self):
    gold_code, tree = self.load_test_subject('L1245')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1252(self):
    gold_code, tree = self.load_test_subject('L1252')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1254(self):
    gold_code, tree = self.load_test_subject('L1254')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1257(self):
    gold_code, tree = self.load_test_subject('L1257')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1258(self):
    gold_code, tree = self.load_test_subject('L1258')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1260(self):
    gold_code, tree = self.load_test_subject('L1260')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1266(self):
    gold_code, tree = self.load_test_subject('L1266')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1267(self):
    gold_code, tree = self.load_test_subject('L1267')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1273(self):
    gold_code, tree = self.load_test_subject('L1273')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1275(self):
    gold_code, tree = self.load_test_subject('L1275')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1277(self):
    gold_code, tree = self.load_test_subject('L1277')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1281(self):
    gold_code, tree = self.load_test_subject('L1281')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1282(self):
    gold_code, tree = self.load_test_subject('L1282')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1283(self):
    gold_code, tree = self.load_test_subject('L1283')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1284(self):
    gold_code, tree = self.load_test_subject('L1284')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1287(self):
    gold_code, tree = self.load_test_subject('L1287')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1288(self):
    gold_code, tree = self.load_test_subject('L1288')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1292(self):
    gold_code, tree = self.load_test_subject('L1292')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1293(self):
    gold_code, tree = self.load_test_subject('L1293')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1295(self):
    gold_code, tree = self.load_test_subject('L1295')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1298(self):
    gold_code, tree = self.load_test_subject('L1298')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1299(self):
    gold_code, tree = self.load_test_subject('L1299')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1304(self):
    gold_code, tree = self.load_test_subject('L1304')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1306(self):
    gold_code, tree = self.load_test_subject('L1306')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1309(self):
    gold_code, tree = self.load_test_subject('L1309')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1310(self):
    gold_code, tree = self.load_test_subject('L1310')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1311(self):
    gold_code, tree = self.load_test_subject('L1311')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1313(self):
    gold_code, tree = self.load_test_subject('L1313')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1314(self):
    gold_code, tree = self.load_test_subject('L1314')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1316(self):
    gold_code, tree = self.load_test_subject('L1316')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1318(self):
    gold_code, tree = self.load_test_subject('L1318')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1319(self):
    gold_code, tree = self.load_test_subject('L1319')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1323(self):
    gold_code, tree = self.load_test_subject('L1323')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1324(self):
    gold_code, tree = self.load_test_subject('L1324')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1329(self):
    gold_code, tree = self.load_test_subject('L1329')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1332(self):
    gold_code, tree = self.load_test_subject('L1332')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1338(self):
    gold_code, tree = self.load_test_subject('L1338')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1342(self):
    gold_code, tree = self.load_test_subject('L1342')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1345(self):
    gold_code, tree = self.load_test_subject('L1345')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1346(self):
    gold_code, tree = self.load_test_subject('L1346')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1347(self):
    gold_code, tree = self.load_test_subject('L1347')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1351(self):
    gold_code, tree = self.load_test_subject('L1351')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1361(self):
    gold_code, tree = self.load_test_subject('L1361')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1365(self):
    gold_code, tree = self.load_test_subject('L1365')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1366(self):
    gold_code, tree = self.load_test_subject('L1366')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1368(self):
    gold_code, tree = self.load_test_subject('L1368')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1370(self):
    gold_code, tree = self.load_test_subject('L1370')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1371(self):
    gold_code, tree = self.load_test_subject('L1371')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1374(self):
    gold_code, tree = self.load_test_subject('L1374')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1376(self):
    gold_code, tree = self.load_test_subject('L1376')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1377(self):
    gold_code, tree = self.load_test_subject('L1377')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1380(self):
    gold_code, tree = self.load_test_subject('L1380')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1383(self):
    gold_code, tree = self.load_test_subject('L1383')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1385(self):
    gold_code, tree = self.load_test_subject('L1385')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1386(self):
    gold_code, tree = self.load_test_subject('L1386')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1389(self):
    gold_code, tree = self.load_test_subject('L1389')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1391(self):
    gold_code, tree = self.load_test_subject('L1391')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1392(self):
    gold_code, tree = self.load_test_subject('L1392')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1394(self):
    gold_code, tree = self.load_test_subject('L1394')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1395(self):
    gold_code, tree = self.load_test_subject('L1395')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1400(self):
    gold_code, tree = self.load_test_subject('L1400')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1404(self):
    gold_code, tree = self.load_test_subject('L1404')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1405(self):
    gold_code, tree = self.load_test_subject('L1405')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1409(self):
    gold_code, tree = self.load_test_subject('L1409')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1413(self):
    gold_code, tree = self.load_test_subject('L1413')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1414(self):
    gold_code, tree = self.load_test_subject('L1414')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1418(self):
    gold_code, tree = self.load_test_subject('L1418')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1419(self):
    gold_code, tree = self.load_test_subject('L1419')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1423(self):
    gold_code, tree = self.load_test_subject('L1423')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1425(self):
    gold_code, tree = self.load_test_subject('L1425')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1426(self):
    gold_code, tree = self.load_test_subject('L1426')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1431(self):
    gold_code, tree = self.load_test_subject('L1431')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1434(self):
    gold_code, tree = self.load_test_subject('L1434')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1436(self):
    gold_code, tree = self.load_test_subject('L1436')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1441(self):
    gold_code, tree = self.load_test_subject('L1441')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1442(self):
    gold_code, tree = self.load_test_subject('L1442')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1443(self):
    gold_code, tree = self.load_test_subject('L1443')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1446(self):
    gold_code, tree = self.load_test_subject('L1446')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1447(self):
    gold_code, tree = self.load_test_subject('L1447')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1450(self):
    gold_code, tree = self.load_test_subject('L1450')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1455(self):
    gold_code, tree = self.load_test_subject('L1455')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1460(self):
    gold_code, tree = self.load_test_subject('L1460')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1461(self):
    gold_code, tree = self.load_test_subject('L1461')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1462(self):
    gold_code, tree = self.load_test_subject('L1462')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1463(self):
    gold_code, tree = self.load_test_subject('L1463')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1464(self):
    gold_code, tree = self.load_test_subject('L1464')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1466(self):
    gold_code, tree = self.load_test_subject('L1466')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1470(self):
    gold_code, tree = self.load_test_subject('L1470')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1471(self):
    gold_code, tree = self.load_test_subject('L1471')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1475(self):
    gold_code, tree = self.load_test_subject('L1475')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1480(self):
    gold_code, tree = self.load_test_subject('L1480')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1481(self):
    gold_code, tree = self.load_test_subject('L1481')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1482(self):
    gold_code, tree = self.load_test_subject('L1482')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1486(self):
    gold_code, tree = self.load_test_subject('L1486')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1496(self):
    gold_code, tree = self.load_test_subject('L1496')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1497(self):
    gold_code, tree = self.load_test_subject('L1497')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1499(self):
    gold_code, tree = self.load_test_subject('L1499')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1502(self):
    gold_code, tree = self.load_test_subject('L1502')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1503(self):
    gold_code, tree = self.load_test_subject('L1503')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1507(self):
    gold_code, tree = self.load_test_subject('L1507')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1508(self):
    gold_code, tree = self.load_test_subject('L1508')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1512(self):
    gold_code, tree = self.load_test_subject('L1512')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1514(self):
    gold_code, tree = self.load_test_subject('L1514')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1518(self):
    gold_code, tree = self.load_test_subject('L1518')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1523(self):
    gold_code, tree = self.load_test_subject('L1523')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1524(self):
    gold_code, tree = self.load_test_subject('L1524')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1528(self):
    gold_code, tree = self.load_test_subject('L1528')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1534(self):
    gold_code, tree = self.load_test_subject('L1534')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1539(self):
    gold_code, tree = self.load_test_subject('L1539')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1546(self):
    gold_code, tree = self.load_test_subject('L1546')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1551(self):
    gold_code, tree = self.load_test_subject('L1551')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1552(self):
    gold_code, tree = self.load_test_subject('L1552')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1554(self):
    gold_code, tree = self.load_test_subject('L1554')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1557(self):
    gold_code, tree = self.load_test_subject('L1557')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1559(self):
    gold_code, tree = self.load_test_subject('L1559')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1561(self):
    gold_code, tree = self.load_test_subject('L1561')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1567(self):
    gold_code, tree = self.load_test_subject('L1567')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1572(self):
    gold_code, tree = self.load_test_subject('L1572')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1576(self):
    gold_code, tree = self.load_test_subject('L1576')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1584(self):
    gold_code, tree = self.load_test_subject('L1584')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1588(self):
    gold_code, tree = self.load_test_subject('L1588')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1589(self):
    gold_code, tree = self.load_test_subject('L1589')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1605(self):
    gold_code, tree = self.load_test_subject('L1605')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1614(self):
    gold_code, tree = self.load_test_subject('L1614')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1619(self):
    gold_code, tree = self.load_test_subject('L1619')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1625(self):
    gold_code, tree = self.load_test_subject('L1625')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1626(self):
    gold_code, tree = self.load_test_subject('L1626')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1629(self):
    gold_code, tree = self.load_test_subject('L1629')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1630(self):
    gold_code, tree = self.load_test_subject('L1630')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1631(self):
    gold_code, tree = self.load_test_subject('L1631')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1636(self):
    gold_code, tree = self.load_test_subject('L1636')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1640(self):
    gold_code, tree = self.load_test_subject('L1640')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1641(self):
    gold_code, tree = self.load_test_subject('L1641')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1646(self):
    gold_code, tree = self.load_test_subject('L1646')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1647(self):
    gold_code, tree = self.load_test_subject('L1647')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1652(self):
    gold_code, tree = self.load_test_subject('L1652')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1654(self):
    gold_code, tree = self.load_test_subject('L1654')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1658(self):
    gold_code, tree = self.load_test_subject('L1658')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1662(self):
    gold_code, tree = self.load_test_subject('L1662')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1672(self):
    gold_code, tree = self.load_test_subject('L1672')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1678(self):
    gold_code, tree = self.load_test_subject('L1678')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1679(self):
    gold_code, tree = self.load_test_subject('L1679')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1684(self):
    gold_code, tree = self.load_test_subject('L1684')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1685(self):
    gold_code, tree = self.load_test_subject('L1685')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1688(self):
    gold_code, tree = self.load_test_subject('L1688')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1689(self):
    gold_code, tree = self.load_test_subject('L1689')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1691(self):
    gold_code, tree = self.load_test_subject('L1691')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1697(self):
    gold_code, tree = self.load_test_subject('L1697')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1700(self):
    gold_code, tree = self.load_test_subject('L1700')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1701(self):
    gold_code, tree = self.load_test_subject('L1701')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1704(self):
    gold_code, tree = self.load_test_subject('L1704')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1705(self):
    gold_code, tree = self.load_test_subject('L1705')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1706(self):
    gold_code, tree = self.load_test_subject('L1706')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1711(self):
    gold_code, tree = self.load_test_subject('L1711')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1712(self):
    gold_code, tree = self.load_test_subject('L1712')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1716(self):
    gold_code, tree = self.load_test_subject('L1716')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1717(self):
    gold_code, tree = self.load_test_subject('L1717')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1718(self):
    gold_code, tree = self.load_test_subject('L1718')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1719(self):
    gold_code, tree = self.load_test_subject('L1719')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1720(self):
    gold_code, tree = self.load_test_subject('L1720')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1722(self):
    gold_code, tree = self.load_test_subject('L1722')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1723(self):
    gold_code, tree = self.load_test_subject('L1723')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1725(self):
    gold_code, tree = self.load_test_subject('L1725')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1730(self):
    gold_code, tree = self.load_test_subject('L1730')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1732(self):
    gold_code, tree = self.load_test_subject('L1732')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1734(self):
    gold_code, tree = self.load_test_subject('L1734')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1736(self):
    gold_code, tree = self.load_test_subject('L1736')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1742(self):
    gold_code, tree = self.load_test_subject('L1742')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1743(self):
    gold_code, tree = self.load_test_subject('L1743')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1748(self):
    gold_code, tree = self.load_test_subject('L1748')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1758(self):
    gold_code, tree = self.load_test_subject('L1758')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1760(self):
    gold_code, tree = self.load_test_subject('L1760')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1763(self):
    gold_code, tree = self.load_test_subject('L1763')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1765(self):
    gold_code, tree = self.load_test_subject('L1765')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1768(self):
    gold_code, tree = self.load_test_subject('L1768')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1769(self):
    gold_code, tree = self.load_test_subject('L1769')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1772(self):
    gold_code, tree = self.load_test_subject('L1772')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1773(self):
    gold_code, tree = self.load_test_subject('L1773')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1775(self):
    gold_code, tree = self.load_test_subject('L1775')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1781(self):
    gold_code, tree = self.load_test_subject('L1781')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1790(self):
    gold_code, tree = self.load_test_subject('L1790')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1791(self):
    gold_code, tree = self.load_test_subject('L1791')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1796(self):
    gold_code, tree = self.load_test_subject('L1796')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1798(self):
    gold_code, tree = self.load_test_subject('L1798')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1800(self):
    gold_code, tree = self.load_test_subject('L1800')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1805(self):
    gold_code, tree = self.load_test_subject('L1805')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1807(self):
    gold_code, tree = self.load_test_subject('L1807')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1812(self):
    gold_code, tree = self.load_test_subject('L1812')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1813(self):
    gold_code, tree = self.load_test_subject('L1813')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1816(self):
    gold_code, tree = self.load_test_subject('L1816')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1817(self):
    gold_code, tree = self.load_test_subject('L1817')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1822(self):
    gold_code, tree = self.load_test_subject('L1822')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1823(self):
    gold_code, tree = self.load_test_subject('L1823')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1826(self):
    gold_code, tree = self.load_test_subject('L1826')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1827(self):
    gold_code, tree = self.load_test_subject('L1827')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1828(self):
    gold_code, tree = self.load_test_subject('L1828')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1829(self):
    gold_code, tree = self.load_test_subject('L1829')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1832(self):
    gold_code, tree = self.load_test_subject('L1832')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1833(self):
    gold_code, tree = self.load_test_subject('L1833')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1837(self):
    gold_code, tree = self.load_test_subject('L1837')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1838(self):
    gold_code, tree = self.load_test_subject('L1838')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1844(self):
    gold_code, tree = self.load_test_subject('L1844')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1848(self):
    gold_code, tree = self.load_test_subject('L1848')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1854(self):
    gold_code, tree = self.load_test_subject('L1854')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1855(self):
    gold_code, tree = self.load_test_subject('L1855')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1856(self):
    gold_code, tree = self.load_test_subject('L1856')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1859(self):
    gold_code, tree = self.load_test_subject('L1859')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1860(self):
    gold_code, tree = self.load_test_subject('L1860')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1861(self):
    gold_code, tree = self.load_test_subject('L1861')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1864(self):
    gold_code, tree = self.load_test_subject('L1864')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1869(self):
    gold_code, tree = self.load_test_subject('L1869')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1870(self):
    gold_code, tree = self.load_test_subject('L1870')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1871(self):
    gold_code, tree = self.load_test_subject('L1871')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1872(self):
    gold_code, tree = self.load_test_subject('L1872')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1874(self):
    gold_code, tree = self.load_test_subject('L1874')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1876(self):
    gold_code, tree = self.load_test_subject('L1876')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1877(self):
    gold_code, tree = self.load_test_subject('L1877')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1880(self):
    gold_code, tree = self.load_test_subject('L1880')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1881(self):
    gold_code, tree = self.load_test_subject('L1881')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1882(self):
    gold_code, tree = self.load_test_subject('L1882')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1883(self):
    gold_code, tree = self.load_test_subject('L1883')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1886(self):
    gold_code, tree = self.load_test_subject('L1886')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1887(self):
    gold_code, tree = self.load_test_subject('L1887')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1888(self):
    gold_code, tree = self.load_test_subject('L1888')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1891(self):
    gold_code, tree = self.load_test_subject('L1891')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1893(self):
    gold_code, tree = self.load_test_subject('L1893')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1895(self):
    gold_code, tree = self.load_test_subject('L1895')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1897(self):
    gold_code, tree = self.load_test_subject('L1897')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1898(self):
    gold_code, tree = self.load_test_subject('L1898')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1899(self):
    gold_code, tree = self.load_test_subject('L1899')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1903(self):
    gold_code, tree = self.load_test_subject('L1903')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1904(self):
    gold_code, tree = self.load_test_subject('L1904')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1905(self):
    gold_code, tree = self.load_test_subject('L1905')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1906(self):
    gold_code, tree = self.load_test_subject('L1906')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1909(self):
    gold_code, tree = self.load_test_subject('L1909')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1913(self):
    gold_code, tree = self.load_test_subject('L1913')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1914(self):
    gold_code, tree = self.load_test_subject('L1914')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1915(self):
    gold_code, tree = self.load_test_subject('L1915')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1920(self):
    gold_code, tree = self.load_test_subject('L1920')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1921(self):
    gold_code, tree = self.load_test_subject('L1921')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1922(self):
    gold_code, tree = self.load_test_subject('L1922')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1923(self):
    gold_code, tree = self.load_test_subject('L1923')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1925(self):
    gold_code, tree = self.load_test_subject('L1925')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1926(self):
    gold_code, tree = self.load_test_subject('L1926')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1929(self):
    gold_code, tree = self.load_test_subject('L1929')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1930(self):
    gold_code, tree = self.load_test_subject('L1930')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1935(self):
    gold_code, tree = self.load_test_subject('L1935')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1936(self):
    gold_code, tree = self.load_test_subject('L1936')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1941(self):
    gold_code, tree = self.load_test_subject('L1941')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1942(self):
    gold_code, tree = self.load_test_subject('L1942')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1943(self):
    gold_code, tree = self.load_test_subject('L1943')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1944(self):
    gold_code, tree = self.load_test_subject('L1944')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1945(self):
    gold_code, tree = self.load_test_subject('L1945')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1946(self):
    gold_code, tree = self.load_test_subject('L1946')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1952(self):
    gold_code, tree = self.load_test_subject('L1952')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1953(self):
    gold_code, tree = self.load_test_subject('L1953')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1957(self):
    gold_code, tree = self.load_test_subject('L1957')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1958(self):
    gold_code, tree = self.load_test_subject('L1958')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1959(self):
    gold_code, tree = self.load_test_subject('L1959')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1961(self):
    gold_code, tree = self.load_test_subject('L1961')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1962(self):
    gold_code, tree = self.load_test_subject('L1962')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1963(self):
    gold_code, tree = self.load_test_subject('L1963')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1967(self):
    gold_code, tree = self.load_test_subject('L1967')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1968(self):
    gold_code, tree = self.load_test_subject('L1968')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1970(self):
    gold_code, tree = self.load_test_subject('L1970')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1971(self):
    gold_code, tree = self.load_test_subject('L1971')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1974(self):
    gold_code, tree = self.load_test_subject('L1974')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1976(self):
    gold_code, tree = self.load_test_subject('L1976')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1979(self):
    gold_code, tree = self.load_test_subject('L1979')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1980(self):
    gold_code, tree = self.load_test_subject('L1980')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1984(self):
    gold_code, tree = self.load_test_subject('L1984')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1991(self):
    gold_code, tree = self.load_test_subject('L1991')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1992(self):
    gold_code, tree = self.load_test_subject('L1992')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1994(self):
    gold_code, tree = self.load_test_subject('L1994')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1995(self):
    gold_code, tree = self.load_test_subject('L1995')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1996(self):
    gold_code, tree = self.load_test_subject('L1996')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L1998(self):
    gold_code, tree = self.load_test_subject('L1998')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2000(self):
    gold_code, tree = self.load_test_subject('L2000')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2006(self):
    gold_code, tree = self.load_test_subject('L2006')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2007(self):
    gold_code, tree = self.load_test_subject('L2007')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2011(self):
    gold_code, tree = self.load_test_subject('L2011')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2012(self):
    gold_code, tree = self.load_test_subject('L2012')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2016(self):
    gold_code, tree = self.load_test_subject('L2016')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2017(self):
    gold_code, tree = self.load_test_subject('L2017')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2021(self):
    gold_code, tree = self.load_test_subject('L2021')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2022(self):
    gold_code, tree = self.load_test_subject('L2022')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2023(self):
    gold_code, tree = self.load_test_subject('L2023')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2024(self):
    gold_code, tree = self.load_test_subject('L2024')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2028(self):
    gold_code, tree = self.load_test_subject('L2028')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2029(self):
    gold_code, tree = self.load_test_subject('L2029')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2032(self):
    gold_code, tree = self.load_test_subject('L2032')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2033(self):
    gold_code, tree = self.load_test_subject('L2033')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2035(self):
    gold_code, tree = self.load_test_subject('L2035')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2037(self):
    gold_code, tree = self.load_test_subject('L2037')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2038(self):
    gold_code, tree = self.load_test_subject('L2038')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2039(self):
    gold_code, tree = self.load_test_subject('L2039')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2042(self):
    gold_code, tree = self.load_test_subject('L2042')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2044(self):
    gold_code, tree = self.load_test_subject('L2044')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2045(self):
    gold_code, tree = self.load_test_subject('L2045')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2047(self):
    gold_code, tree = self.load_test_subject('L2047')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2048(self):
    gold_code, tree = self.load_test_subject('L2048')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2049(self):
    gold_code, tree = self.load_test_subject('L2049')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2052(self):
    gold_code, tree = self.load_test_subject('L2052')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2053(self):
    gold_code, tree = self.load_test_subject('L2053')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2055(self):
    gold_code, tree = self.load_test_subject('L2055')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2057(self):
    gold_code, tree = self.load_test_subject('L2057')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2059(self):
    gold_code, tree = self.load_test_subject('L2059')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2063(self):
    gold_code, tree = self.load_test_subject('L2063')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2064(self):
    gold_code, tree = self.load_test_subject('L2064')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2067(self):
    gold_code, tree = self.load_test_subject('L2067')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2068(self):
    gold_code, tree = self.load_test_subject('L2068')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2073(self):
    gold_code, tree = self.load_test_subject('L2073')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2075(self):
    gold_code, tree = self.load_test_subject('L2075')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2076(self):
    gold_code, tree = self.load_test_subject('L2076')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2078(self):
    gold_code, tree = self.load_test_subject('L2078')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2079(self):
    gold_code, tree = self.load_test_subject('L2079')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2083(self):
    gold_code, tree = self.load_test_subject('L2083')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2085(self):
    gold_code, tree = self.load_test_subject('L2085')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2089(self):
    gold_code, tree = self.load_test_subject('L2089')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2090(self):
    gold_code, tree = self.load_test_subject('L2090')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2091(self):
    gold_code, tree = self.load_test_subject('L2091')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2092(self):
    gold_code, tree = self.load_test_subject('L2092')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2094(self):
    gold_code, tree = self.load_test_subject('L2094')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2099(self):
    gold_code, tree = self.load_test_subject('L2099')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2100(self):
    gold_code, tree = self.load_test_subject('L2100')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2101(self):
    gold_code, tree = self.load_test_subject('L2101')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2103(self):
    gold_code, tree = self.load_test_subject('L2103')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2104(self):
    gold_code, tree = self.load_test_subject('L2104')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2105(self):
    gold_code, tree = self.load_test_subject('L2105')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2106(self):
    gold_code, tree = self.load_test_subject('L2106')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2108(self):
    gold_code, tree = self.load_test_subject('L2108')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2109(self):
    gold_code, tree = self.load_test_subject('L2109')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2110(self):
    gold_code, tree = self.load_test_subject('L2110')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2114(self):
    gold_code, tree = self.load_test_subject('L2114')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2119(self):
    gold_code, tree = self.load_test_subject('L2119')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2120(self):
    gold_code, tree = self.load_test_subject('L2120')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2121(self):
    gold_code, tree = self.load_test_subject('L2121')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2122(self):
    gold_code, tree = self.load_test_subject('L2122')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2125(self):
    gold_code, tree = self.load_test_subject('L2125')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2132(self):
    gold_code, tree = self.load_test_subject('L2132')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2133(self):
    gold_code, tree = self.load_test_subject('L2133')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2134(self):
    gold_code, tree = self.load_test_subject('L2134')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2135(self):
    gold_code, tree = self.load_test_subject('L2135')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2136(self):
    gold_code, tree = self.load_test_subject('L2136')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2138(self):
    gold_code, tree = self.load_test_subject('L2138')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2139(self):
    gold_code, tree = self.load_test_subject('L2139')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2140(self):
    gold_code, tree = self.load_test_subject('L2140')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2144(self):
    gold_code, tree = self.load_test_subject('L2144')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2145(self):
    gold_code, tree = self.load_test_subject('L2145')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2146(self):
    gold_code, tree = self.load_test_subject('L2146')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2148(self):
    gold_code, tree = self.load_test_subject('L2148')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2149(self):
    gold_code, tree = self.load_test_subject('L2149')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2150(self):
    gold_code, tree = self.load_test_subject('L2150')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2151(self):
    gold_code, tree = self.load_test_subject('L2151')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2154(self):
    gold_code, tree = self.load_test_subject('L2154')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2155(self):
    gold_code, tree = self.load_test_subject('L2155')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2157(self):
    gold_code, tree = self.load_test_subject('L2157')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2160(self):
    gold_code, tree = self.load_test_subject('L2160')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2161(self):
    gold_code, tree = self.load_test_subject('L2161')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2162(self):
    gold_code, tree = self.load_test_subject('L2162')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2164(self):
    gold_code, tree = self.load_test_subject('L2164')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2165(self):
    gold_code, tree = self.load_test_subject('L2165')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2167(self):
    gold_code, tree = self.load_test_subject('L2167')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2168(self):
    gold_code, tree = self.load_test_subject('L2168')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2169(self):
    gold_code, tree = self.load_test_subject('L2169')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2170(self):
    gold_code, tree = self.load_test_subject('L2170')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2171(self):
    gold_code, tree = self.load_test_subject('L2171')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2174(self):
    gold_code, tree = self.load_test_subject('L2174')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2176(self):
    gold_code, tree = self.load_test_subject('L2176')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2177(self):
    gold_code, tree = self.load_test_subject('L2177')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2178(self):
    gold_code, tree = self.load_test_subject('L2178')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2180(self):
    gold_code, tree = self.load_test_subject('L2180')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2182(self):
    gold_code, tree = self.load_test_subject('L2182')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2185(self):
    gold_code, tree = self.load_test_subject('L2185')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2186(self):
    gold_code, tree = self.load_test_subject('L2186')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2190(self):
    gold_code, tree = self.load_test_subject('L2190')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2191(self):
    gold_code, tree = self.load_test_subject('L2191')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2192(self):
    gold_code, tree = self.load_test_subject('L2192')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2193(self):
    gold_code, tree = self.load_test_subject('L2193')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2194(self):
    gold_code, tree = self.load_test_subject('L2194')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2198(self):
    gold_code, tree = self.load_test_subject('L2198')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2200(self):
    gold_code, tree = self.load_test_subject('L2200')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2201(self):
    gold_code, tree = self.load_test_subject('L2201')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2202(self):
    gold_code, tree = self.load_test_subject('L2202')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2203(self):
    gold_code, tree = self.load_test_subject('L2203')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2206(self):
    gold_code, tree = self.load_test_subject('L2206')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2207(self):
    gold_code, tree = self.load_test_subject('L2207')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2208(self):
    gold_code, tree = self.load_test_subject('L2208')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2210(self):
    gold_code, tree = self.load_test_subject('L2210')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2211(self):
    gold_code, tree = self.load_test_subject('L2211')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2212(self):
    gold_code, tree = self.load_test_subject('L2212')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2214(self):
    gold_code, tree = self.load_test_subject('L2214')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2215(self):
    gold_code, tree = self.load_test_subject('L2215')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2216(self):
    gold_code, tree = self.load_test_subject('L2216')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2217(self):
    gold_code, tree = self.load_test_subject('L2217')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2218(self):
    gold_code, tree = self.load_test_subject('L2218')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2219(self):
    gold_code, tree = self.load_test_subject('L2219')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2220(self):
    gold_code, tree = self.load_test_subject('L2220')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2221(self):
    gold_code, tree = self.load_test_subject('L2221')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2224(self):
    gold_code, tree = self.load_test_subject('L2224')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2225(self):
    gold_code, tree = self.load_test_subject('L2225')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2226(self):
    gold_code, tree = self.load_test_subject('L2226')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2229(self):
    gold_code, tree = self.load_test_subject('L2229')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2235(self):
    gold_code, tree = self.load_test_subject('L2235')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2237(self):
    gold_code, tree = self.load_test_subject('L2237')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2239(self):
    gold_code, tree = self.load_test_subject('L2239')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2240(self):
    gold_code, tree = self.load_test_subject('L2240')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2243(self):
    gold_code, tree = self.load_test_subject('L2243')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2244(self):
    gold_code, tree = self.load_test_subject('L2244')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2248(self):
    gold_code, tree = self.load_test_subject('L2248')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2249(self):
    gold_code, tree = self.load_test_subject('L2249')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2255(self):
    gold_code, tree = self.load_test_subject('L2255')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2256(self):
    gold_code, tree = self.load_test_subject('L2256')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2257(self):
    gold_code, tree = self.load_test_subject('L2257')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2258(self):
    gold_code, tree = self.load_test_subject('L2258')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2259(self):
    gold_code, tree = self.load_test_subject('L2259')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2260(self):
    gold_code, tree = self.load_test_subject('L2260')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2261(self):
    gold_code, tree = self.load_test_subject('L2261')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2262(self):
    gold_code, tree = self.load_test_subject('L2262')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2264(self):
    gold_code, tree = self.load_test_subject('L2264')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2267(self):
    gold_code, tree = self.load_test_subject('L2267')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2268(self):
    gold_code, tree = self.load_test_subject('L2268')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2269(self):
    gold_code, tree = self.load_test_subject('L2269')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2270(self):
    gold_code, tree = self.load_test_subject('L2270')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2273(self):
    gold_code, tree = self.load_test_subject('L2273')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2274(self):
    gold_code, tree = self.load_test_subject('L2274')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2275(self):
    gold_code, tree = self.load_test_subject('L2275')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2278(self):
    gold_code, tree = self.load_test_subject('L2278')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2279(self):
    gold_code, tree = self.load_test_subject('L2279')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2281(self):
    gold_code, tree = self.load_test_subject('L2281')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2283(self):
    gold_code, tree = self.load_test_subject('L2283')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2284(self):
    gold_code, tree = self.load_test_subject('L2284')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2285(self):
    gold_code, tree = self.load_test_subject('L2285')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2287(self):
    gold_code, tree = self.load_test_subject('L2287')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2288(self):
    gold_code, tree = self.load_test_subject('L2288')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2289(self):
    gold_code, tree = self.load_test_subject('L2289')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2290(self):
    gold_code, tree = self.load_test_subject('L2290')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2291(self):
    gold_code, tree = self.load_test_subject('L2291')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2293(self):
    gold_code, tree = self.load_test_subject('L2293')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2295(self):
    gold_code, tree = self.load_test_subject('L2295')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2299(self):
    gold_code, tree = self.load_test_subject('L2299')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2301(self):
    gold_code, tree = self.load_test_subject('L2301')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2302(self):
    gold_code, tree = self.load_test_subject('L2302')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2303(self):
    gold_code, tree = self.load_test_subject('L2303')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2304(self):
    gold_code, tree = self.load_test_subject('L2304')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2305(self):
    gold_code, tree = self.load_test_subject('L2305')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2306(self):
    gold_code, tree = self.load_test_subject('L2306')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2309(self):
    gold_code, tree = self.load_test_subject('L2309')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2310(self):
    gold_code, tree = self.load_test_subject('L2310')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2311(self):
    gold_code, tree = self.load_test_subject('L2311')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2312(self):
    gold_code, tree = self.load_test_subject('L2312')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2315(self):
    gold_code, tree = self.load_test_subject('L2315')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2316(self):
    gold_code, tree = self.load_test_subject('L2316')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2317(self):
    gold_code, tree = self.load_test_subject('L2317')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2318(self):
    gold_code, tree = self.load_test_subject('L2318')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2319(self):
    gold_code, tree = self.load_test_subject('L2319')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2320(self):
    gold_code, tree = self.load_test_subject('L2320')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2321(self):
    gold_code, tree = self.load_test_subject('L2321')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2322(self):
    gold_code, tree = self.load_test_subject('L2322')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_L2323(self):
    gold_code, tree = self.load_test_subject('L2323')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)


class TestLogStatementInserter(unittest.TestCase):
  def setUp(self):
    self.maxDiff = None
    self.src_lang = 'py'
    self.snippets_dir = p_consts.TEST_ARTIFACTS_DIR / 'py' / 'TestLogStatementInserter'
    self.parser = p_consts.PARSER_DICT[self.src_lang]

  def to_tree(self, snippet: str) -> p_visitor_py.Tree:
    ts_tree = self.parser.parse(bytes(snippet, 'utf-8'))
    tree = p_visitor_py.Tree.from_ts_tree(ts_tree)
    assert tree.root_node is not None
    assert tree.root_node.node_type == 'module'
    return tree

  def test_insert_log_statements_L0001(self):
    tree = self.to_tree(p_utils.read_text(self.snippets_dir / 'L0001_input.py'))
    inserter = p_visitor_py.LogStatementInserter(function_name='f_gold')
    inserter.visit(tree.root_node)
    pp_code = p_visitor_py.PrettyPrinter(indent_with='    ').visit(tree.root_node).strip()
    gold_code = p_utils.read_text(self.snippets_dir / 'L0001_output.py')
    self.assertEqual(pp_code, gold_code)


class TestAssignedIdentifierExtractor(unittest.TestCase):
  def setUp(self):
    self.src_lang = 'py'
    self.parser = p_consts.PARSER_DICT[self.src_lang]
    self.maxDiff = None

  def get_ast(self, snippet) -> pvis.AbstractNode:
    ts_tree = self.parser.parse(bytes(snippet, 'utf-8'))
    tree = p_visitor_py.Tree.from_ts_tree(ts_tree)
    assert tree.root_node is not None
    assert tree.root_node.node_type == 'module'
    assert len(tree.root_node.children) == 1, 'snippet must contain a single statement'
    return tree.root_node.children[0]

  def extract_assigned_identifiers(self, snippet):
    ast = self.get_ast(snippet)
    extractor = p_visitor_py.AssignedIdentifierExtractor()
    extractor.visit(ast)
    return extractor.get_assigned_identifiers()

  def test_single_assignment(self):
    # Test a simple assignment
    snippet = 'x = 10'
    assigned_identifiers = self.extract_assigned_identifiers(snippet)
    self.assertCountEqual(assigned_identifiers, ['x'])

    snippet = 'num = 10'
    assigned_identifiers = self.extract_assigned_identifiers(snippet)
    self.assertCountEqual(assigned_identifiers, ['num'])

  def test_subscript_assignment(self):
    # Test subscript assignment
    snippet = 'arr[0] = 10'
    assigned_identifiers = self.extract_assigned_identifiers(snippet)
    self.assertCountEqual(assigned_identifiers, ['arr'])


if __name__ == '__main__':
  unittest.main()
