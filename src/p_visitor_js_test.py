import unittest
from typing import Tuple

import p_consts
import p_utils
import p_visitor_js


class TestPrettyPrinter(unittest.TestCase):
  def setUp(self):
    self.snippets_dir = p_consts.TEST_ARTIFACTS_DIR / 'leetcode-javascript' / 'solutions'
    self.src_lang = 'js'
    self.parser = p_consts.PARSER_DICT[self.src_lang]
    self.pp = p_visitor_js.PrettyPrinter()
    self.maxDiff = None

  def load_test_subject(self, subject_name: str) -> Tuple[str, p_visitor_js.Tree]:
    for fpath in self.snippets_dir.iterdir():
      if fpath.name.startswith(subject_name):
        snippet_text = p_utils.read_text(fpath).strip()
        ts_tree = self.parser.parse(bytes(snippet_text, 'utf8'))
        tree = p_visitor_js.Tree.from_ts_tree(ts_tree)
        return snippet_text, tree
    raise FileNotFoundError(f"No file starting with '{subject_name}' found in {self.snippets_dir}")

  def test_0001(self):
    gold_code, tree = self.load_test_subject('0001')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0002(self):
    gold_code, tree = self.load_test_subject('0002')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0003(self):
    gold_code, tree = self.load_test_subject('0003')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0004(self):
    gold_code, tree = self.load_test_subject('0004')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0005(self):
    gold_code, tree = self.load_test_subject('0005')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0006(self):
    gold_code, tree = self.load_test_subject('0006')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0007(self):
    gold_code, tree = self.load_test_subject('0007')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0008(self):
    gold_code, tree = self.load_test_subject('0008')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0009(self):
    gold_code, tree = self.load_test_subject('0009')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0010(self):
    gold_code, tree = self.load_test_subject('0010')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0011(self):
    gold_code, tree = self.load_test_subject('0011')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0012(self):
    gold_code, tree = self.load_test_subject('0012')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0013(self):
    gold_code, tree = self.load_test_subject('0013')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0014(self):
    gold_code, tree = self.load_test_subject('0014')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0015(self):
    gold_code, tree = self.load_test_subject('0015')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0016(self):
    gold_code, tree = self.load_test_subject('0016')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0017(self):
    gold_code, tree = self.load_test_subject('0017')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0018(self):
    gold_code, tree = self.load_test_subject('0018')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0019(self):
    gold_code, tree = self.load_test_subject('0019')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0020(self):
    gold_code, tree = self.load_test_subject('0020')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0021(self):
    gold_code, tree = self.load_test_subject('0021')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0022(self):
    gold_code, tree = self.load_test_subject('0022')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0023(self):
    gold_code, tree = self.load_test_subject('0023')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0024(self):
    gold_code, tree = self.load_test_subject('0024')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0025(self):
    gold_code, tree = self.load_test_subject('0025')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0026(self):
    gold_code, tree = self.load_test_subject('0026')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0027(self):
    gold_code, tree = self.load_test_subject('0027')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0028(self):
    gold_code, tree = self.load_test_subject('0028')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0029(self):
    gold_code, tree = self.load_test_subject('0029')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0030(self):
    gold_code, tree = self.load_test_subject('0030')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0031(self):
    gold_code, tree = self.load_test_subject('0031')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0032(self):
    gold_code, tree = self.load_test_subject('0032')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0033(self):
    gold_code, tree = self.load_test_subject('0033')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0034(self):
    gold_code, tree = self.load_test_subject('0034')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0035(self):
    gold_code, tree = self.load_test_subject('0035')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0036(self):
    gold_code, tree = self.load_test_subject('0036')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0037(self):
    gold_code, tree = self.load_test_subject('0037')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0038(self):
    gold_code, tree = self.load_test_subject('0038')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0039(self):
    gold_code, tree = self.load_test_subject('0039')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0040(self):
    gold_code, tree = self.load_test_subject('0040')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0041(self):
    gold_code, tree = self.load_test_subject('0041')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0042(self):
    gold_code, tree = self.load_test_subject('0042')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0043(self):
    gold_code, tree = self.load_test_subject('0043')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0044(self):
    gold_code, tree = self.load_test_subject('0044')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0045(self):
    gold_code, tree = self.load_test_subject('0045')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0046(self):
    gold_code, tree = self.load_test_subject('0046')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0047(self):
    gold_code, tree = self.load_test_subject('0047')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0048(self):
    gold_code, tree = self.load_test_subject('0048')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0049(self):
    gold_code, tree = self.load_test_subject('0049')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0050(self):
    gold_code, tree = self.load_test_subject('0050')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0051(self):
    gold_code, tree = self.load_test_subject('0051')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0052(self):
    gold_code, tree = self.load_test_subject('0052')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0053(self):
    gold_code, tree = self.load_test_subject('0053')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0054(self):
    gold_code, tree = self.load_test_subject('0054')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0055(self):
    gold_code, tree = self.load_test_subject('0055')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0056(self):
    gold_code, tree = self.load_test_subject('0056')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0057(self):
    gold_code, tree = self.load_test_subject('0057')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0058(self):
    gold_code, tree = self.load_test_subject('0058')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0059(self):
    gold_code, tree = self.load_test_subject('0059')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0060(self):
    gold_code, tree = self.load_test_subject('0060')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0061(self):
    gold_code, tree = self.load_test_subject('0061')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0062(self):
    gold_code, tree = self.load_test_subject('0062')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0063(self):
    gold_code, tree = self.load_test_subject('0063')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0064(self):
    gold_code, tree = self.load_test_subject('0064')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0065(self):
    gold_code, tree = self.load_test_subject('0065')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0066(self):
    gold_code, tree = self.load_test_subject('0066')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0067(self):
    gold_code, tree = self.load_test_subject('0067')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0068(self):
    gold_code, tree = self.load_test_subject('0068')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0069(self):
    gold_code, tree = self.load_test_subject('0069')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0070(self):
    gold_code, tree = self.load_test_subject('0070')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0071(self):
    gold_code, tree = self.load_test_subject('0071')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0072(self):
    gold_code, tree = self.load_test_subject('0072')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0073(self):
    gold_code, tree = self.load_test_subject('0073')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0074(self):
    gold_code, tree = self.load_test_subject('0074')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0075(self):
    gold_code, tree = self.load_test_subject('0075')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0076(self):
    gold_code, tree = self.load_test_subject('0076')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0077(self):
    gold_code, tree = self.load_test_subject('0077')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0078(self):
    gold_code, tree = self.load_test_subject('0078')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0079(self):
    gold_code, tree = self.load_test_subject('0079')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0080(self):
    gold_code, tree = self.load_test_subject('0080')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0081(self):
    gold_code, tree = self.load_test_subject('0081')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0082(self):
    gold_code, tree = self.load_test_subject('0082')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0083(self):
    gold_code, tree = self.load_test_subject('0083')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0084(self):
    gold_code, tree = self.load_test_subject('0084')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0085(self):
    gold_code, tree = self.load_test_subject('0085')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0086(self):
    gold_code, tree = self.load_test_subject('0086')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0087(self):
    gold_code, tree = self.load_test_subject('0087')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0088(self):
    gold_code, tree = self.load_test_subject('0088')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0089(self):
    gold_code, tree = self.load_test_subject('0089')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0090(self):
    gold_code, tree = self.load_test_subject('0090')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0091(self):
    gold_code, tree = self.load_test_subject('0091')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0092(self):
    gold_code, tree = self.load_test_subject('0092')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0093(self):
    gold_code, tree = self.load_test_subject('0093')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0094(self):
    gold_code, tree = self.load_test_subject('0094')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0095(self):
    gold_code, tree = self.load_test_subject('0095')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0096(self):
    gold_code, tree = self.load_test_subject('0096')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0097(self):
    gold_code, tree = self.load_test_subject('0097')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0098(self):
    gold_code, tree = self.load_test_subject('0098')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0099(self):
    gold_code, tree = self.load_test_subject('0099')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0100(self):
    gold_code, tree = self.load_test_subject('0100')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0101(self):
    gold_code, tree = self.load_test_subject('0101')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0102(self):
    gold_code, tree = self.load_test_subject('0102')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0103(self):
    gold_code, tree = self.load_test_subject('0103')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0104(self):
    gold_code, tree = self.load_test_subject('0104')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0105(self):
    gold_code, tree = self.load_test_subject('0105')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0106(self):
    gold_code, tree = self.load_test_subject('0106')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0107(self):
    gold_code, tree = self.load_test_subject('0107')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0108(self):
    gold_code, tree = self.load_test_subject('0108')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0109(self):
    gold_code, tree = self.load_test_subject('0109')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0110(self):
    gold_code, tree = self.load_test_subject('0110')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0111(self):
    gold_code, tree = self.load_test_subject('0111')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0112(self):
    gold_code, tree = self.load_test_subject('0112')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0113(self):
    gold_code, tree = self.load_test_subject('0113')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0114(self):
    gold_code, tree = self.load_test_subject('0114')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0115(self):
    gold_code, tree = self.load_test_subject('0115')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0116(self):
    gold_code, tree = self.load_test_subject('0116')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0117(self):
    gold_code, tree = self.load_test_subject('0117')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0118(self):
    gold_code, tree = self.load_test_subject('0118')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0119(self):
    gold_code, tree = self.load_test_subject('0119')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0120(self):
    gold_code, tree = self.load_test_subject('0120')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0121(self):
    gold_code, tree = self.load_test_subject('0121')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0122(self):
    gold_code, tree = self.load_test_subject('0122')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0123(self):
    gold_code, tree = self.load_test_subject('0123')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0124(self):
    gold_code, tree = self.load_test_subject('0124')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0125(self):
    gold_code, tree = self.load_test_subject('0125')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0126(self):
    gold_code, tree = self.load_test_subject('0126')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0127(self):
    gold_code, tree = self.load_test_subject('0127')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0128(self):
    gold_code, tree = self.load_test_subject('0128')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0129(self):
    gold_code, tree = self.load_test_subject('0129')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0130(self):
    gold_code, tree = self.load_test_subject('0130')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0131(self):
    gold_code, tree = self.load_test_subject('0131')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0132(self):
    gold_code, tree = self.load_test_subject('0132')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0133(self):
    gold_code, tree = self.load_test_subject('0133')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0134(self):
    gold_code, tree = self.load_test_subject('0134')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0135(self):
    gold_code, tree = self.load_test_subject('0135')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0136(self):
    gold_code, tree = self.load_test_subject('0136')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0137(self):
    gold_code, tree = self.load_test_subject('0137')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0138(self):
    gold_code, tree = self.load_test_subject('0138')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0139(self):
    gold_code, tree = self.load_test_subject('0139')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0140(self):
    gold_code, tree = self.load_test_subject('0140')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0141(self):
    gold_code, tree = self.load_test_subject('0141')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0142(self):
    gold_code, tree = self.load_test_subject('0142')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0143(self):
    gold_code, tree = self.load_test_subject('0143')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0144(self):
    gold_code, tree = self.load_test_subject('0144')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0145(self):
    gold_code, tree = self.load_test_subject('0145')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0146(self):
    gold_code, tree = self.load_test_subject('0146')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0147(self):
    gold_code, tree = self.load_test_subject('0147')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0148(self):
    gold_code, tree = self.load_test_subject('0148')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0149(self):
    gold_code, tree = self.load_test_subject('0149')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0150(self):
    gold_code, tree = self.load_test_subject('0150')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0151(self):
    gold_code, tree = self.load_test_subject('0151')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0152(self):
    gold_code, tree = self.load_test_subject('0152')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0153(self):
    gold_code, tree = self.load_test_subject('0153')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0154(self):
    gold_code, tree = self.load_test_subject('0154')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0155(self):
    gold_code, tree = self.load_test_subject('0155')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0160(self):
    gold_code, tree = self.load_test_subject('0160')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0162(self):
    gold_code, tree = self.load_test_subject('0162')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0164(self):
    gold_code, tree = self.load_test_subject('0164')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0165(self):
    gold_code, tree = self.load_test_subject('0165')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0166(self):
    gold_code, tree = self.load_test_subject('0166')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0167(self):
    gold_code, tree = self.load_test_subject('0167')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0168(self):
    gold_code, tree = self.load_test_subject('0168')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0169(self):
    gold_code, tree = self.load_test_subject('0169')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0171(self):
    gold_code, tree = self.load_test_subject('0171')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0172(self):
    gold_code, tree = self.load_test_subject('0172')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0173(self):
    gold_code, tree = self.load_test_subject('0173')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0174(self):
    gold_code, tree = self.load_test_subject('0174')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0179(self):
    gold_code, tree = self.load_test_subject('0179')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0187(self):
    gold_code, tree = self.load_test_subject('0187')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0188(self):
    gold_code, tree = self.load_test_subject('0188')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0189(self):
    gold_code, tree = self.load_test_subject('0189')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0190(self):
    gold_code, tree = self.load_test_subject('0190')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0191(self):
    gold_code, tree = self.load_test_subject('0191')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0198(self):
    gold_code, tree = self.load_test_subject('0198')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0199(self):
    gold_code, tree = self.load_test_subject('0199')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0200(self):
    gold_code, tree = self.load_test_subject('0200')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0201(self):
    gold_code, tree = self.load_test_subject('0201')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0202(self):
    gold_code, tree = self.load_test_subject('0202')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0203(self):
    gold_code, tree = self.load_test_subject('0203')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0204(self):
    gold_code, tree = self.load_test_subject('0204')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0205(self):
    gold_code, tree = self.load_test_subject('0205')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0206(self):
    gold_code, tree = self.load_test_subject('0206')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0207(self):
    gold_code, tree = self.load_test_subject('0207')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0208(self):
    gold_code, tree = self.load_test_subject('0208')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0209(self):
    gold_code, tree = self.load_test_subject('0209')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0210(self):
    gold_code, tree = self.load_test_subject('0210')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0211(self):
    gold_code, tree = self.load_test_subject('0211')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0212(self):
    gold_code, tree = self.load_test_subject('0212')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0213(self):
    gold_code, tree = self.load_test_subject('0213')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0214(self):
    gold_code, tree = self.load_test_subject('0214')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0215(self):
    gold_code, tree = self.load_test_subject('0215')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0216(self):
    gold_code, tree = self.load_test_subject('0216')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0217(self):
    gold_code, tree = self.load_test_subject('0217')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0218(self):
    gold_code, tree = self.load_test_subject('0218')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0219(self):
    gold_code, tree = self.load_test_subject('0219')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0220(self):
    gold_code, tree = self.load_test_subject('0220')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0221(self):
    gold_code, tree = self.load_test_subject('0221')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0222(self):
    gold_code, tree = self.load_test_subject('0222')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0223(self):
    gold_code, tree = self.load_test_subject('0223')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0224(self):
    gold_code, tree = self.load_test_subject('0224')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0225(self):
    gold_code, tree = self.load_test_subject('0225')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0226(self):
    gold_code, tree = self.load_test_subject('0226')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0227(self):
    gold_code, tree = self.load_test_subject('0227')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0228(self):
    gold_code, tree = self.load_test_subject('0228')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0229(self):
    gold_code, tree = self.load_test_subject('0229')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0230(self):
    gold_code, tree = self.load_test_subject('0230')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0231(self):
    gold_code, tree = self.load_test_subject('0231')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0232(self):
    gold_code, tree = self.load_test_subject('0232')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0233(self):
    gold_code, tree = self.load_test_subject('0233')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0234(self):
    gold_code, tree = self.load_test_subject('0234')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0235(self):
    gold_code, tree = self.load_test_subject('0235')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0236(self):
    gold_code, tree = self.load_test_subject('0236')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0237(self):
    gold_code, tree = self.load_test_subject('0237')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0238(self):
    gold_code, tree = self.load_test_subject('0238')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0239(self):
    gold_code, tree = self.load_test_subject('0239')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0240(self):
    gold_code, tree = self.load_test_subject('0240')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0241(self):
    gold_code, tree = self.load_test_subject('0241')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0242(self):
    gold_code, tree = self.load_test_subject('0242')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0257(self):
    gold_code, tree = self.load_test_subject('0257')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0258(self):
    gold_code, tree = self.load_test_subject('0258')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0260(self):
    gold_code, tree = self.load_test_subject('0260')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0263(self):
    gold_code, tree = self.load_test_subject('0263')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0264(self):
    gold_code, tree = self.load_test_subject('0264')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0268(self):
    gold_code, tree = self.load_test_subject('0268')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0273(self):
    gold_code, tree = self.load_test_subject('0273')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0274(self):
    gold_code, tree = self.load_test_subject('0274')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0275(self):
    gold_code, tree = self.load_test_subject('0275')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0278(self):
    gold_code, tree = self.load_test_subject('0278')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0279(self):
    gold_code, tree = self.load_test_subject('0279')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0282(self):
    gold_code, tree = self.load_test_subject('0282')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0283(self):
    gold_code, tree = self.load_test_subject('0283')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0284(self):
    gold_code, tree = self.load_test_subject('0284')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0287(self):
    gold_code, tree = self.load_test_subject('0287')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0289(self):
    gold_code, tree = self.load_test_subject('0289')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0290(self):
    gold_code, tree = self.load_test_subject('0290')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0292(self):
    gold_code, tree = self.load_test_subject('0292')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0295(self):
    gold_code, tree = self.load_test_subject('0295')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0297(self):
    gold_code, tree = self.load_test_subject('0297')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0299(self):
    gold_code, tree = self.load_test_subject('0299')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0300(self):
    gold_code, tree = self.load_test_subject('0300')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0301(self):
    gold_code, tree = self.load_test_subject('0301')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0303(self):
    gold_code, tree = self.load_test_subject('0303')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0304(self):
    gold_code, tree = self.load_test_subject('0304')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0306(self):
    gold_code, tree = self.load_test_subject('0306')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0307(self):
    gold_code, tree = self.load_test_subject('0307')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0309(self):
    gold_code, tree = self.load_test_subject('0309')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0310(self):
    gold_code, tree = self.load_test_subject('0310')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0312(self):
    gold_code, tree = self.load_test_subject('0312')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0313(self):
    gold_code, tree = self.load_test_subject('0313')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0315(self):
    gold_code, tree = self.load_test_subject('0315')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0316(self):
    gold_code, tree = self.load_test_subject('0316')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0318(self):
    gold_code, tree = self.load_test_subject('0318')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0319(self):
    gold_code, tree = self.load_test_subject('0319')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0321(self):
    gold_code, tree = self.load_test_subject('0321')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0322(self):
    gold_code, tree = self.load_test_subject('0322')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0324(self):
    gold_code, tree = self.load_test_subject('0324')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0326(self):
    gold_code, tree = self.load_test_subject('0326')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0327(self):
    gold_code, tree = self.load_test_subject('0327')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0328(self):
    gold_code, tree = self.load_test_subject('0328')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0329(self):
    gold_code, tree = self.load_test_subject('0329')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0330(self):
    gold_code, tree = self.load_test_subject('0330')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0331(self):
    gold_code, tree = self.load_test_subject('0331')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0332(self):
    gold_code, tree = self.load_test_subject('0332')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0334(self):
    gold_code, tree = self.load_test_subject('0334')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0335(self):
    gold_code, tree = self.load_test_subject('0335')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0336(self):
    gold_code, tree = self.load_test_subject('0336')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0337(self):
    gold_code, tree = self.load_test_subject('0337')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0338(self):
    gold_code, tree = self.load_test_subject('0338')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0341(self):
    gold_code, tree = self.load_test_subject('0341')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0342(self):
    gold_code, tree = self.load_test_subject('0342')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0343(self):
    gold_code, tree = self.load_test_subject('0343')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0344(self):
    gold_code, tree = self.load_test_subject('0344')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0345(self):
    gold_code, tree = self.load_test_subject('0345')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0347(self):
    gold_code, tree = self.load_test_subject('0347')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0349(self):
    gold_code, tree = self.load_test_subject('0349')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0350(self):
    gold_code, tree = self.load_test_subject('0350')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0352(self):
    gold_code, tree = self.load_test_subject('0352')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0354(self):
    gold_code, tree = self.load_test_subject('0354')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0355(self):
    gold_code, tree = self.load_test_subject('0355')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0357(self):
    gold_code, tree = self.load_test_subject('0357')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0363(self):
    gold_code, tree = self.load_test_subject('0363')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0365(self):
    gold_code, tree = self.load_test_subject('0365')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0367(self):
    gold_code, tree = self.load_test_subject('0367')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0368(self):
    gold_code, tree = self.load_test_subject('0368')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0371(self):
    gold_code, tree = self.load_test_subject('0371')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0372(self):
    gold_code, tree = self.load_test_subject('0372')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0373(self):
    gold_code, tree = self.load_test_subject('0373')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0374(self):
    gold_code, tree = self.load_test_subject('0374')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0375(self):
    gold_code, tree = self.load_test_subject('0375')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0376(self):
    gold_code, tree = self.load_test_subject('0376')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0377(self):
    gold_code, tree = self.load_test_subject('0377')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0378(self):
    gold_code, tree = self.load_test_subject('0378')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0380(self):
    gold_code, tree = self.load_test_subject('0380')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0381(self):
    gold_code, tree = self.load_test_subject('0381')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0382(self):
    gold_code, tree = self.load_test_subject('0382')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0383(self):
    gold_code, tree = self.load_test_subject('0383')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0384(self):
    gold_code, tree = self.load_test_subject('0384')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0385(self):
    gold_code, tree = self.load_test_subject('0385')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0386(self):
    gold_code, tree = self.load_test_subject('0386')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0387(self):
    gold_code, tree = self.load_test_subject('0387')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0388(self):
    gold_code, tree = self.load_test_subject('0388')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0389(self):
    gold_code, tree = self.load_test_subject('0389')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0390(self):
    gold_code, tree = self.load_test_subject('0390')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0391(self):
    gold_code, tree = self.load_test_subject('0391')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0392(self):
    gold_code, tree = self.load_test_subject('0392')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0393(self):
    gold_code, tree = self.load_test_subject('0393')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0394(self):
    gold_code, tree = self.load_test_subject('0394')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0395(self):
    gold_code, tree = self.load_test_subject('0395')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0396(self):
    gold_code, tree = self.load_test_subject('0396')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0397(self):
    gold_code, tree = self.load_test_subject('0397')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0398(self):
    gold_code, tree = self.load_test_subject('0398')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0399(self):
    gold_code, tree = self.load_test_subject('0399')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0400(self):
    gold_code, tree = self.load_test_subject('0400')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0401(self):
    gold_code, tree = self.load_test_subject('0401')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0402(self):
    gold_code, tree = self.load_test_subject('0402')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0403(self):
    gold_code, tree = self.load_test_subject('0403')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0404(self):
    gold_code, tree = self.load_test_subject('0404')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0405(self):
    gold_code, tree = self.load_test_subject('0405')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0406(self):
    gold_code, tree = self.load_test_subject('0406')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0407(self):
    gold_code, tree = self.load_test_subject('0407')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0409(self):
    gold_code, tree = self.load_test_subject('0409')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0410(self):
    gold_code, tree = self.load_test_subject('0410')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0412(self):
    gold_code, tree = self.load_test_subject('0412')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0413(self):
    gold_code, tree = self.load_test_subject('0413')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0414(self):
    gold_code, tree = self.load_test_subject('0414')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0415(self):
    gold_code, tree = self.load_test_subject('0415')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0416(self):
    gold_code, tree = self.load_test_subject('0416')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0417(self):
    gold_code, tree = self.load_test_subject('0417')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0419(self):
    gold_code, tree = self.load_test_subject('0419')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0420(self):
    gold_code, tree = self.load_test_subject('0420')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0421(self):
    gold_code, tree = self.load_test_subject('0421')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0423(self):
    gold_code, tree = self.load_test_subject('0423')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0424(self):
    gold_code, tree = self.load_test_subject('0424')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0427(self):
    gold_code, tree = self.load_test_subject('0427')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0429(self):
    gold_code, tree = self.load_test_subject('0429')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0430(self):
    gold_code, tree = self.load_test_subject('0430')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0432(self):
    gold_code, tree = self.load_test_subject('0432')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0433(self):
    gold_code, tree = self.load_test_subject('0433')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0434(self):
    gold_code, tree = self.load_test_subject('0434')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0435(self):
    gold_code, tree = self.load_test_subject('0435')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0436(self):
    gold_code, tree = self.load_test_subject('0436')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0437(self):
    gold_code, tree = self.load_test_subject('0437')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0438(self):
    gold_code, tree = self.load_test_subject('0438')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0440(self):
    gold_code, tree = self.load_test_subject('0440')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0441(self):
    gold_code, tree = self.load_test_subject('0441')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0442(self):
    gold_code, tree = self.load_test_subject('0442')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0443(self):
    gold_code, tree = self.load_test_subject('0443')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0445(self):
    gold_code, tree = self.load_test_subject('0445')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0446(self):
    gold_code, tree = self.load_test_subject('0446')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0447(self):
    gold_code, tree = self.load_test_subject('0447')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0448(self):
    gold_code, tree = self.load_test_subject('0448')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0449(self):
    gold_code, tree = self.load_test_subject('0449')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0450(self):
    gold_code, tree = self.load_test_subject('0450')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0451(self):
    gold_code, tree = self.load_test_subject('0451')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0452(self):
    gold_code, tree = self.load_test_subject('0452')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0453(self):
    gold_code, tree = self.load_test_subject('0453')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0454(self):
    gold_code, tree = self.load_test_subject('0454')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0455(self):
    gold_code, tree = self.load_test_subject('0455')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0456(self):
    gold_code, tree = self.load_test_subject('0456')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0457(self):
    gold_code, tree = self.load_test_subject('0457')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0458(self):
    gold_code, tree = self.load_test_subject('0458')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0459(self):
    gold_code, tree = self.load_test_subject('0459')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0460(self):
    gold_code, tree = self.load_test_subject('0460')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0461(self):
    gold_code, tree = self.load_test_subject('0461')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0462(self):
    gold_code, tree = self.load_test_subject('0462')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0463(self):
    gold_code, tree = self.load_test_subject('0463')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0464(self):
    gold_code, tree = self.load_test_subject('0464')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0466(self):
    gold_code, tree = self.load_test_subject('0466')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0467(self):
    gold_code, tree = self.load_test_subject('0467')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0468(self):
    gold_code, tree = self.load_test_subject('0468')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0470(self):
    gold_code, tree = self.load_test_subject('0470')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0472(self):
    gold_code, tree = self.load_test_subject('0472')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0473(self):
    gold_code, tree = self.load_test_subject('0473')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0474(self):
    gold_code, tree = self.load_test_subject('0474')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0475(self):
    gold_code, tree = self.load_test_subject('0475')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0476(self):
    gold_code, tree = self.load_test_subject('0476')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0477(self):
    gold_code, tree = self.load_test_subject('0477')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0478(self):
    gold_code, tree = self.load_test_subject('0478')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0479(self):
    gold_code, tree = self.load_test_subject('0479')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0480(self):
    gold_code, tree = self.load_test_subject('0480')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0481(self):
    gold_code, tree = self.load_test_subject('0481')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0482(self):
    gold_code, tree = self.load_test_subject('0482')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0483(self):
    gold_code, tree = self.load_test_subject('0483')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0485(self):
    gold_code, tree = self.load_test_subject('0485')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0486(self):
    gold_code, tree = self.load_test_subject('0486')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0488(self):
    gold_code, tree = self.load_test_subject('0488')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0491(self):
    gold_code, tree = self.load_test_subject('0491')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0492(self):
    gold_code, tree = self.load_test_subject('0492')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0493(self):
    gold_code, tree = self.load_test_subject('0493')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0494(self):
    gold_code, tree = self.load_test_subject('0494')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0495(self):
    gold_code, tree = self.load_test_subject('0495')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0496(self):
    gold_code, tree = self.load_test_subject('0496')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0497(self):
    gold_code, tree = self.load_test_subject('0497')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0498(self):
    gold_code, tree = self.load_test_subject('0498')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0500(self):
    gold_code, tree = self.load_test_subject('0500')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0501(self):
    gold_code, tree = self.load_test_subject('0501')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0502(self):
    gold_code, tree = self.load_test_subject('0502')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0503(self):
    gold_code, tree = self.load_test_subject('0503')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0504(self):
    gold_code, tree = self.load_test_subject('0504')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0506(self):
    gold_code, tree = self.load_test_subject('0506')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0507(self):
    gold_code, tree = self.load_test_subject('0507')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0508(self):
    gold_code, tree = self.load_test_subject('0508')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0509(self):
    gold_code, tree = self.load_test_subject('0509')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0513(self):
    gold_code, tree = self.load_test_subject('0513')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0514(self):
    gold_code, tree = self.load_test_subject('0514')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0515(self):
    gold_code, tree = self.load_test_subject('0515')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0516(self):
    gold_code, tree = self.load_test_subject('0516')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0517(self):
    gold_code, tree = self.load_test_subject('0517')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0518(self):
    gold_code, tree = self.load_test_subject('0518')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0519(self):
    gold_code, tree = self.load_test_subject('0519')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0520(self):
    gold_code, tree = self.load_test_subject('0520')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0521(self):
    gold_code, tree = self.load_test_subject('0521')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0522(self):
    gold_code, tree = self.load_test_subject('0522')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0523(self):
    gold_code, tree = self.load_test_subject('0523')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0524(self):
    gold_code, tree = self.load_test_subject('0524')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0525(self):
    gold_code, tree = self.load_test_subject('0525')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0526(self):
    gold_code, tree = self.load_test_subject('0526')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0528(self):
    gold_code, tree = self.load_test_subject('0528')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0529(self):
    gold_code, tree = self.load_test_subject('0529')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0530(self):
    gold_code, tree = self.load_test_subject('0530')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0532(self):
    gold_code, tree = self.load_test_subject('0532')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0537(self):
    gold_code, tree = self.load_test_subject('0537')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0538(self):
    gold_code, tree = self.load_test_subject('0538')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0539(self):
    gold_code, tree = self.load_test_subject('0539')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0540(self):
    gold_code, tree = self.load_test_subject('0540')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0541(self):
    gold_code, tree = self.load_test_subject('0541')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0542(self):
    gold_code, tree = self.load_test_subject('0542')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0543(self):
    gold_code, tree = self.load_test_subject('0543')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0546(self):
    gold_code, tree = self.load_test_subject('0546')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0547(self):
    gold_code, tree = self.load_test_subject('0547')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0551(self):
    gold_code, tree = self.load_test_subject('0551')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0552(self):
    gold_code, tree = self.load_test_subject('0552')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0553(self):
    gold_code, tree = self.load_test_subject('0553')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0554(self):
    gold_code, tree = self.load_test_subject('0554')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0556(self):
    gold_code, tree = self.load_test_subject('0556')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0557(self):
    gold_code, tree = self.load_test_subject('0557')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0558(self):
    gold_code, tree = self.load_test_subject('0558')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0559(self):
    gold_code, tree = self.load_test_subject('0559')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0560(self):
    gold_code, tree = self.load_test_subject('0560')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0563(self):
    gold_code, tree = self.load_test_subject('0563')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0564(self):
    gold_code, tree = self.load_test_subject('0564')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0565(self):
    gold_code, tree = self.load_test_subject('0565')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0566(self):
    gold_code, tree = self.load_test_subject('0566')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0567(self):
    gold_code, tree = self.load_test_subject('0567')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0572(self):
    gold_code, tree = self.load_test_subject('0572')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0575(self):
    gold_code, tree = self.load_test_subject('0575')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0576(self):
    gold_code, tree = self.load_test_subject('0576')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0581(self):
    gold_code, tree = self.load_test_subject('0581')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0583(self):
    gold_code, tree = self.load_test_subject('0583')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0587(self):
    gold_code, tree = self.load_test_subject('0587')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0589(self):
    gold_code, tree = self.load_test_subject('0589')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0590(self):
    gold_code, tree = self.load_test_subject('0590')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0591(self):
    gold_code, tree = self.load_test_subject('0591')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0592(self):
    gold_code, tree = self.load_test_subject('0592')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0593(self):
    gold_code, tree = self.load_test_subject('0593')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0594(self):
    gold_code, tree = self.load_test_subject('0594')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0598(self):
    gold_code, tree = self.load_test_subject('0598')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0599(self):
    gold_code, tree = self.load_test_subject('0599')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0600(self):
    gold_code, tree = self.load_test_subject('0600')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0605(self):
    gold_code, tree = self.load_test_subject('0605')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0606(self):
    gold_code, tree = self.load_test_subject('0606')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0609(self):
    gold_code, tree = self.load_test_subject('0609')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0611(self):
    gold_code, tree = self.load_test_subject('0611')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0617(self):
    gold_code, tree = self.load_test_subject('0617')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0621(self):
    gold_code, tree = self.load_test_subject('0621')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0622(self):
    gold_code, tree = self.load_test_subject('0622')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0623(self):
    gold_code, tree = self.load_test_subject('0623')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0624(self):
    gold_code, tree = self.load_test_subject('0624')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0628(self):
    gold_code, tree = self.load_test_subject('0628')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0629(self):
    gold_code, tree = self.load_test_subject('0629')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0630(self):
    gold_code, tree = self.load_test_subject('0630')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0632(self):
    gold_code, tree = self.load_test_subject('0632')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0633(self):
    gold_code, tree = self.load_test_subject('0633')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0636(self):
    gold_code, tree = self.load_test_subject('0636')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0637(self):
    gold_code, tree = self.load_test_subject('0637')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0638(self):
    gold_code, tree = self.load_test_subject('0638')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0639(self):
    gold_code, tree = self.load_test_subject('0639')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0640(self):
    gold_code, tree = self.load_test_subject('0640')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0641(self):
    gold_code, tree = self.load_test_subject('0641')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0643(self):
    gold_code, tree = self.load_test_subject('0643')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0645(self):
    gold_code, tree = self.load_test_subject('0645')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0646(self):
    gold_code, tree = self.load_test_subject('0646')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0647(self):
    gold_code, tree = self.load_test_subject('0647')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0648(self):
    gold_code, tree = self.load_test_subject('0648')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0649(self):
    gold_code, tree = self.load_test_subject('0649')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0650(self):
    gold_code, tree = self.load_test_subject('0650')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0652(self):
    gold_code, tree = self.load_test_subject('0652')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0653(self):
    gold_code, tree = self.load_test_subject('0653')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0654(self):
    gold_code, tree = self.load_test_subject('0654')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0655(self):
    gold_code, tree = self.load_test_subject('0655')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0657(self):
    gold_code, tree = self.load_test_subject('0657')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0658(self):
    gold_code, tree = self.load_test_subject('0658')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0659(self):
    gold_code, tree = self.load_test_subject('0659')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0661(self):
    gold_code, tree = self.load_test_subject('0661')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0662(self):
    gold_code, tree = self.load_test_subject('0662')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0664(self):
    gold_code, tree = self.load_test_subject('0664')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0665(self):
    gold_code, tree = self.load_test_subject('0665')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0667(self):
    gold_code, tree = self.load_test_subject('0667')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0668(self):
    gold_code, tree = self.load_test_subject('0668')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0669(self):
    gold_code, tree = self.load_test_subject('0669')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0670(self):
    gold_code, tree = self.load_test_subject('0670')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0671(self):
    gold_code, tree = self.load_test_subject('0671')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0672(self):
    gold_code, tree = self.load_test_subject('0672')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0673(self):
    gold_code, tree = self.load_test_subject('0673')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0674(self):
    gold_code, tree = self.load_test_subject('0674')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0675(self):
    gold_code, tree = self.load_test_subject('0675')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0676(self):
    gold_code, tree = self.load_test_subject('0676')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0677(self):
    gold_code, tree = self.load_test_subject('0677')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0678(self):
    gold_code, tree = self.load_test_subject('0678')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0679(self):
    gold_code, tree = self.load_test_subject('0679')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0680(self):
    gold_code, tree = self.load_test_subject('0680')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0682(self):
    gold_code, tree = self.load_test_subject('0682')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0684(self):
    gold_code, tree = self.load_test_subject('0684')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0685(self):
    gold_code, tree = self.load_test_subject('0685')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0686(self):
    gold_code, tree = self.load_test_subject('0686')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0687(self):
    gold_code, tree = self.load_test_subject('0687')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0688(self):
    gold_code, tree = self.load_test_subject('0688')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0689(self):
    gold_code, tree = self.load_test_subject('0689')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0690(self):
    gold_code, tree = self.load_test_subject('0690')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0691(self):
    gold_code, tree = self.load_test_subject('0691')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0692(self):
    gold_code, tree = self.load_test_subject('0692')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0693(self):
    gold_code, tree = self.load_test_subject('0693')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0695(self):
    gold_code, tree = self.load_test_subject('0695')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0696(self):
    gold_code, tree = self.load_test_subject('0696')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0697(self):
    gold_code, tree = self.load_test_subject('0697')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0698(self):
    gold_code, tree = self.load_test_subject('0698')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0699(self):
    gold_code, tree = self.load_test_subject('0699')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0700(self):
    gold_code, tree = self.load_test_subject('0700')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0701(self):
    gold_code, tree = self.load_test_subject('0701')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0703(self):
    gold_code, tree = self.load_test_subject('0703')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0704(self):
    gold_code, tree = self.load_test_subject('0704')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0705(self):
    gold_code, tree = self.load_test_subject('0705')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0706(self):
    gold_code, tree = self.load_test_subject('0706')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0707(self):
    gold_code, tree = self.load_test_subject('0707')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0710(self):
    gold_code, tree = self.load_test_subject('0710')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0712(self):
    gold_code, tree = self.load_test_subject('0712')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0713(self):
    gold_code, tree = self.load_test_subject('0713')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0714(self):
    gold_code, tree = self.load_test_subject('0714')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0715(self):
    gold_code, tree = self.load_test_subject('0715')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0717(self):
    gold_code, tree = self.load_test_subject('0717')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0718(self):
    gold_code, tree = self.load_test_subject('0718')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0719(self):
    gold_code, tree = self.load_test_subject('0719')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0720(self):
    gold_code, tree = self.load_test_subject('0720')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0721(self):
    gold_code, tree = self.load_test_subject('0721')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0722(self):
    gold_code, tree = self.load_test_subject('0722')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0724(self):
    gold_code, tree = self.load_test_subject('0724')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0725(self):
    gold_code, tree = self.load_test_subject('0725')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0726(self):
    gold_code, tree = self.load_test_subject('0726')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0728(self):
    gold_code, tree = self.load_test_subject('0728')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0729(self):
    gold_code, tree = self.load_test_subject('0729')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0730(self):
    gold_code, tree = self.load_test_subject('0730')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0731(self):
    gold_code, tree = self.load_test_subject('0731')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0732(self):
    gold_code, tree = self.load_test_subject('0732')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0733(self):
    gold_code, tree = self.load_test_subject('0733')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0735(self):
    gold_code, tree = self.load_test_subject('0735')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0736(self):
    gold_code, tree = self.load_test_subject('0736')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0738(self):
    gold_code, tree = self.load_test_subject('0738')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0739(self):
    gold_code, tree = self.load_test_subject('0739')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0740(self):
    gold_code, tree = self.load_test_subject('0740')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0741(self):
    gold_code, tree = self.load_test_subject('0741')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0743(self):
    gold_code, tree = self.load_test_subject('0743')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0744(self):
    gold_code, tree = self.load_test_subject('0744')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0745(self):
    gold_code, tree = self.load_test_subject('0745')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0746(self):
    gold_code, tree = self.load_test_subject('0746')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0747(self):
    gold_code, tree = self.load_test_subject('0747')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0748(self):
    gold_code, tree = self.load_test_subject('0748')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0749(self):
    gold_code, tree = self.load_test_subject('0749')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0752(self):
    gold_code, tree = self.load_test_subject('0752')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0753(self):
    gold_code, tree = self.load_test_subject('0753')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0754(self):
    gold_code, tree = self.load_test_subject('0754')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0756(self):
    gold_code, tree = self.load_test_subject('0756')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0757(self):
    gold_code, tree = self.load_test_subject('0757')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0761(self):
    gold_code, tree = self.load_test_subject('0761')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0762(self):
    gold_code, tree = self.load_test_subject('0762')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0763(self):
    gold_code, tree = self.load_test_subject('0763')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0764(self):
    gold_code, tree = self.load_test_subject('0764')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0765(self):
    gold_code, tree = self.load_test_subject('0765')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0766(self):
    gold_code, tree = self.load_test_subject('0766')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0767(self):
    gold_code, tree = self.load_test_subject('0767')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0768(self):
    gold_code, tree = self.load_test_subject('0768')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0769(self):
    gold_code, tree = self.load_test_subject('0769')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0770(self):
    gold_code, tree = self.load_test_subject('0770')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0773(self):
    gold_code, tree = self.load_test_subject('0773')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0775(self):
    gold_code, tree = self.load_test_subject('0775')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0777(self):
    gold_code, tree = self.load_test_subject('0777')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0778(self):
    gold_code, tree = self.load_test_subject('0778')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0779(self):
    gold_code, tree = self.load_test_subject('0779')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0780(self):
    gold_code, tree = self.load_test_subject('0780')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0781(self):
    gold_code, tree = self.load_test_subject('0781')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0782(self):
    gold_code, tree = self.load_test_subject('0782')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0783(self):
    gold_code, tree = self.load_test_subject('0783')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0784(self):
    gold_code, tree = self.load_test_subject('0784')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0785(self):
    gold_code, tree = self.load_test_subject('0785')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0786(self):
    gold_code, tree = self.load_test_subject('0786')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0787(self):
    gold_code, tree = self.load_test_subject('0787')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0788(self):
    gold_code, tree = self.load_test_subject('0788')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0789(self):
    gold_code, tree = self.load_test_subject('0789')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0790(self):
    gold_code, tree = self.load_test_subject('0790')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0791(self):
    gold_code, tree = self.load_test_subject('0791')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0792(self):
    gold_code, tree = self.load_test_subject('0792')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0793(self):
    gold_code, tree = self.load_test_subject('0793')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0794(self):
    gold_code, tree = self.load_test_subject('0794')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0795(self):
    gold_code, tree = self.load_test_subject('0795')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0796(self):
    gold_code, tree = self.load_test_subject('0796')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0797(self):
    gold_code, tree = self.load_test_subject('0797')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0798(self):
    gold_code, tree = self.load_test_subject('0798')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0799(self):
    gold_code, tree = self.load_test_subject('0799')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0801(self):
    gold_code, tree = self.load_test_subject('0801')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0802(self):
    gold_code, tree = self.load_test_subject('0802')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0803(self):
    gold_code, tree = self.load_test_subject('0803')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0804(self):
    gold_code, tree = self.load_test_subject('0804')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0805(self):
    gold_code, tree = self.load_test_subject('0805')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0806(self):
    gold_code, tree = self.load_test_subject('0806')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0808(self):
    gold_code, tree = self.load_test_subject('0808')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0809(self):
    gold_code, tree = self.load_test_subject('0809')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0810(self):
    gold_code, tree = self.load_test_subject('0810')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0811(self):
    gold_code, tree = self.load_test_subject('0811')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0812(self):
    gold_code, tree = self.load_test_subject('0812')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0813(self):
    gold_code, tree = self.load_test_subject('0813')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0814(self):
    gold_code, tree = self.load_test_subject('0814')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0815(self):
    gold_code, tree = self.load_test_subject('0815')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0816(self):
    gold_code, tree = self.load_test_subject('0816')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0817(self):
    gold_code, tree = self.load_test_subject('0817')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0818(self):
    gold_code, tree = self.load_test_subject('0818')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0819(self):
    gold_code, tree = self.load_test_subject('0819')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0820(self):
    gold_code, tree = self.load_test_subject('0820')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0821(self):
    gold_code, tree = self.load_test_subject('0821')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0822(self):
    gold_code, tree = self.load_test_subject('0822')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0823(self):
    gold_code, tree = self.load_test_subject('0823')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0824(self):
    gold_code, tree = self.load_test_subject('0824')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0825(self):
    gold_code, tree = self.load_test_subject('0825')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0826(self):
    gold_code, tree = self.load_test_subject('0826')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0827(self):
    gold_code, tree = self.load_test_subject('0827')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0828(self):
    gold_code, tree = self.load_test_subject('0828')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0829(self):
    gold_code, tree = self.load_test_subject('0829')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0830(self):
    gold_code, tree = self.load_test_subject('0830')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0831(self):
    gold_code, tree = self.load_test_subject('0831')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0833(self):
    gold_code, tree = self.load_test_subject('0833')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0834(self):
    gold_code, tree = self.load_test_subject('0834')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0835(self):
    gold_code, tree = self.load_test_subject('0835')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0836(self):
    gold_code, tree = self.load_test_subject('0836')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0837(self):
    gold_code, tree = self.load_test_subject('0837')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0838(self):
    gold_code, tree = self.load_test_subject('0838')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0839(self):
    gold_code, tree = self.load_test_subject('0839')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0840(self):
    gold_code, tree = self.load_test_subject('0840')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0841(self):
    gold_code, tree = self.load_test_subject('0841')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0842(self):
    gold_code, tree = self.load_test_subject('0842')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0843(self):
    gold_code, tree = self.load_test_subject('0843')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0844(self):
    gold_code, tree = self.load_test_subject('0844')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0845(self):
    gold_code, tree = self.load_test_subject('0845')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0846(self):
    gold_code, tree = self.load_test_subject('0846')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0847(self):
    gold_code, tree = self.load_test_subject('0847')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0848(self):
    gold_code, tree = self.load_test_subject('0848')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0849(self):
    gold_code, tree = self.load_test_subject('0849')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0850(self):
    gold_code, tree = self.load_test_subject('0850')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0851(self):
    gold_code, tree = self.load_test_subject('0851')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0852(self):
    gold_code, tree = self.load_test_subject('0852')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0853(self):
    gold_code, tree = self.load_test_subject('0853')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0854(self):
    gold_code, tree = self.load_test_subject('0854')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0855(self):
    gold_code, tree = self.load_test_subject('0855')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0856(self):
    gold_code, tree = self.load_test_subject('0856')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0857(self):
    gold_code, tree = self.load_test_subject('0857')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0858(self):
    gold_code, tree = self.load_test_subject('0858')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0859(self):
    gold_code, tree = self.load_test_subject('0859')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0860(self):
    gold_code, tree = self.load_test_subject('0860')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0861(self):
    gold_code, tree = self.load_test_subject('0861')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0862(self):
    gold_code, tree = self.load_test_subject('0862')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0863(self):
    gold_code, tree = self.load_test_subject('0863')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0864(self):
    gold_code, tree = self.load_test_subject('0864')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0865(self):
    gold_code, tree = self.load_test_subject('0865')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0866(self):
    gold_code, tree = self.load_test_subject('0866')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0867(self):
    gold_code, tree = self.load_test_subject('0867')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0868(self):
    gold_code, tree = self.load_test_subject('0868')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0869(self):
    gold_code, tree = self.load_test_subject('0869')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0870(self):
    gold_code, tree = self.load_test_subject('0870')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0871(self):
    gold_code, tree = self.load_test_subject('0871')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0872(self):
    gold_code, tree = self.load_test_subject('0872')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0873(self):
    gold_code, tree = self.load_test_subject('0873')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0874(self):
    gold_code, tree = self.load_test_subject('0874')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0875(self):
    gold_code, tree = self.load_test_subject('0875')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0876(self):
    gold_code, tree = self.load_test_subject('0876')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0877(self):
    gold_code, tree = self.load_test_subject('0877')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0878(self):
    gold_code, tree = self.load_test_subject('0878')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0879(self):
    gold_code, tree = self.load_test_subject('0879')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0880(self):
    gold_code, tree = self.load_test_subject('0880')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0881(self):
    gold_code, tree = self.load_test_subject('0881')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0882(self):
    gold_code, tree = self.load_test_subject('0882')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0883(self):
    gold_code, tree = self.load_test_subject('0883')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0884(self):
    gold_code, tree = self.load_test_subject('0884')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0885(self):
    gold_code, tree = self.load_test_subject('0885')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0886(self):
    gold_code, tree = self.load_test_subject('0886')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0887(self):
    gold_code, tree = self.load_test_subject('0887')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0888(self):
    gold_code, tree = self.load_test_subject('0888')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0889(self):
    gold_code, tree = self.load_test_subject('0889')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0890(self):
    gold_code, tree = self.load_test_subject('0890')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0891(self):
    gold_code, tree = self.load_test_subject('0891')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0892(self):
    gold_code, tree = self.load_test_subject('0892')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0893(self):
    gold_code, tree = self.load_test_subject('0893')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0894(self):
    gold_code, tree = self.load_test_subject('0894')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0895(self):
    gold_code, tree = self.load_test_subject('0895')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0896(self):
    gold_code, tree = self.load_test_subject('0896')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0897(self):
    gold_code, tree = self.load_test_subject('0897')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0898(self):
    gold_code, tree = self.load_test_subject('0898')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0899(self):
    gold_code, tree = self.load_test_subject('0899')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0900(self):
    gold_code, tree = self.load_test_subject('0900')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0901(self):
    gold_code, tree = self.load_test_subject('0901')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0902(self):
    gold_code, tree = self.load_test_subject('0902')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0903(self):
    gold_code, tree = self.load_test_subject('0903')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0904(self):
    gold_code, tree = self.load_test_subject('0904')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0905(self):
    gold_code, tree = self.load_test_subject('0905')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0906(self):
    gold_code, tree = self.load_test_subject('0906')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0907(self):
    gold_code, tree = self.load_test_subject('0907')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0908(self):
    gold_code, tree = self.load_test_subject('0908')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0909(self):
    gold_code, tree = self.load_test_subject('0909')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0910(self):
    gold_code, tree = self.load_test_subject('0910')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0911(self):
    gold_code, tree = self.load_test_subject('0911')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0912(self):
    gold_code, tree = self.load_test_subject('0912')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0913(self):
    gold_code, tree = self.load_test_subject('0913')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0914(self):
    gold_code, tree = self.load_test_subject('0914')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0915(self):
    gold_code, tree = self.load_test_subject('0915')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0916(self):
    gold_code, tree = self.load_test_subject('0916')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0918(self):
    gold_code, tree = self.load_test_subject('0918')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0919(self):
    gold_code, tree = self.load_test_subject('0919')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0920(self):
    gold_code, tree = self.load_test_subject('0920')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0921(self):
    gold_code, tree = self.load_test_subject('0921')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0922(self):
    gold_code, tree = self.load_test_subject('0922')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0923(self):
    gold_code, tree = self.load_test_subject('0923')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0924(self):
    gold_code, tree = self.load_test_subject('0924')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0925(self):
    gold_code, tree = self.load_test_subject('0925')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0926(self):
    gold_code, tree = self.load_test_subject('0926')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0927(self):
    gold_code, tree = self.load_test_subject('0927')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0928(self):
    gold_code, tree = self.load_test_subject('0928')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0929(self):
    gold_code, tree = self.load_test_subject('0929')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0930(self):
    gold_code, tree = self.load_test_subject('0930')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0931(self):
    gold_code, tree = self.load_test_subject('0931')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0932(self):
    gold_code, tree = self.load_test_subject('0932')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0933(self):
    gold_code, tree = self.load_test_subject('0933')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0934(self):
    gold_code, tree = self.load_test_subject('0934')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0935(self):
    gold_code, tree = self.load_test_subject('0935')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0936(self):
    gold_code, tree = self.load_test_subject('0936')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0937(self):
    gold_code, tree = self.load_test_subject('0937')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0938(self):
    gold_code, tree = self.load_test_subject('0938')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0939(self):
    gold_code, tree = self.load_test_subject('0939')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0940(self):
    gold_code, tree = self.load_test_subject('0940')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0941(self):
    gold_code, tree = self.load_test_subject('0941')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0942(self):
    gold_code, tree = self.load_test_subject('0942')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0943(self):
    gold_code, tree = self.load_test_subject('0943')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0944(self):
    gold_code, tree = self.load_test_subject('0944')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0945(self):
    gold_code, tree = self.load_test_subject('0945')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0966(self):
    gold_code, tree = self.load_test_subject('0966')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0970(self):
    gold_code, tree = self.load_test_subject('0970')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0976(self):
    gold_code, tree = self.load_test_subject('0976')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0977(self):
    gold_code, tree = self.load_test_subject('0977')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0985(self):
    gold_code, tree = self.load_test_subject('0985')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0989(self):
    gold_code, tree = self.load_test_subject('0989')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0994(self):
    gold_code, tree = self.load_test_subject('0994')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_0997(self):
    gold_code, tree = self.load_test_subject('0997')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1002(self):
    gold_code, tree = self.load_test_subject('1002')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1004(self):
    gold_code, tree = self.load_test_subject('1004')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1005(self):
    gold_code, tree = self.load_test_subject('1005')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1009(self):
    gold_code, tree = self.load_test_subject('1009')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1010(self):
    gold_code, tree = self.load_test_subject('1010')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1022(self):
    gold_code, tree = self.load_test_subject('1022')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1023(self):
    gold_code, tree = self.load_test_subject('1023')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1028(self):
    gold_code, tree = self.load_test_subject('1028')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1037(self):
    gold_code, tree = self.load_test_subject('1037')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1038(self):
    gold_code, tree = self.load_test_subject('1038')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1041(self):
    gold_code, tree = self.load_test_subject('1041')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1047(self):
    gold_code, tree = self.load_test_subject('1047')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1051(self):
    gold_code, tree = self.load_test_subject('1051')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1071(self):
    gold_code, tree = self.load_test_subject('1071')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1079(self):
    gold_code, tree = self.load_test_subject('1079')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1081(self):
    gold_code, tree = self.load_test_subject('1081')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1092(self):
    gold_code, tree = self.load_test_subject('1092')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1103(self):
    gold_code, tree = self.load_test_subject('1103')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1108(self):
    gold_code, tree = self.load_test_subject('1108')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1122(self):
    gold_code, tree = self.load_test_subject('1122')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1123(self):
    gold_code, tree = self.load_test_subject('1123')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1137(self):
    gold_code, tree = self.load_test_subject('1137')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1143(self):
    gold_code, tree = self.load_test_subject('1143')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1161(self):
    gold_code, tree = self.load_test_subject('1161')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1189(self):
    gold_code, tree = self.load_test_subject('1189')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1200(self):
    gold_code, tree = self.load_test_subject('1200')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1206(self):
    gold_code, tree = self.load_test_subject('1206')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1207(self):
    gold_code, tree = self.load_test_subject('1207')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1208(self):
    gold_code, tree = self.load_test_subject('1208')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1217(self):
    gold_code, tree = self.load_test_subject('1217')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1232(self):
    gold_code, tree = self.load_test_subject('1232')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1233(self):
    gold_code, tree = self.load_test_subject('1233')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1249(self):
    gold_code, tree = self.load_test_subject('1249')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1252(self):
    gold_code, tree = self.load_test_subject('1252')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1261(self):
    gold_code, tree = self.load_test_subject('1261')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1267(self):
    gold_code, tree = self.load_test_subject('1267')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1268(self):
    gold_code, tree = self.load_test_subject('1268')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1287(self):
    gold_code, tree = self.load_test_subject('1287')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1290(self):
    gold_code, tree = self.load_test_subject('1290')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1291(self):
    gold_code, tree = self.load_test_subject('1291')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1292(self):
    gold_code, tree = self.load_test_subject('1292')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1295(self):
    gold_code, tree = self.load_test_subject('1295')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1296(self):
    gold_code, tree = self.load_test_subject('1296')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1297(self):
    gold_code, tree = self.load_test_subject('1297')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1304(self):
    gold_code, tree = self.load_test_subject('1304')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1309(self):
    gold_code, tree = self.load_test_subject('1309')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1313(self):
    gold_code, tree = self.load_test_subject('1313')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1317(self):
    gold_code, tree = self.load_test_subject('1317')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1318(self):
    gold_code, tree = self.load_test_subject('1318')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1319(self):
    gold_code, tree = self.load_test_subject('1319')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1323(self):
    gold_code, tree = self.load_test_subject('1323')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1324(self):
    gold_code, tree = self.load_test_subject('1324')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1331(self):
    gold_code, tree = self.load_test_subject('1331')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1332(self):
    gold_code, tree = self.load_test_subject('1332')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1333(self):
    gold_code, tree = self.load_test_subject('1333')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1342(self):
    gold_code, tree = self.load_test_subject('1342')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1351(self):
    gold_code, tree = self.load_test_subject('1351')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1352(self):
    gold_code, tree = self.load_test_subject('1352')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1356(self):
    gold_code, tree = self.load_test_subject('1356')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1358(self):
    gold_code, tree = self.load_test_subject('1358')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1360(self):
    gold_code, tree = self.load_test_subject('1360')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1365(self):
    gold_code, tree = self.load_test_subject('1365')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1366(self):
    gold_code, tree = self.load_test_subject('1366')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1368(self):
    gold_code, tree = self.load_test_subject('1368')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1372(self):
    gold_code, tree = self.load_test_subject('1372')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1374(self):
    gold_code, tree = self.load_test_subject('1374')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1380(self):
    gold_code, tree = self.load_test_subject('1380')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1389(self):
    gold_code, tree = self.load_test_subject('1389')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1400(self):
    gold_code, tree = self.load_test_subject('1400')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1402(self):
    gold_code, tree = self.load_test_subject('1402')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1408(self):
    gold_code, tree = self.load_test_subject('1408')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1410(self):
    gold_code, tree = self.load_test_subject('1410')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1415(self):
    gold_code, tree = self.load_test_subject('1415')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1431(self):
    gold_code, tree = self.load_test_subject('1431')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1436(self):
    gold_code, tree = self.load_test_subject('1436')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1437(self):
    gold_code, tree = self.load_test_subject('1437')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1443(self):
    gold_code, tree = self.load_test_subject('1443')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1446(self):
    gold_code, tree = self.load_test_subject('1446')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1447(self):
    gold_code, tree = self.load_test_subject('1447')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1448(self):
    gold_code, tree = self.load_test_subject('1448')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1450(self):
    gold_code, tree = self.load_test_subject('1450')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1451(self):
    gold_code, tree = self.load_test_subject('1451')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1455(self):
    gold_code, tree = self.load_test_subject('1455')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1456(self):
    gold_code, tree = self.load_test_subject('1456')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1460(self):
    gold_code, tree = self.load_test_subject('1460')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1462(self):
    gold_code, tree = self.load_test_subject('1462')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1464(self):
    gold_code, tree = self.load_test_subject('1464')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1466(self):
    gold_code, tree = self.load_test_subject('1466')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1470(self):
    gold_code, tree = self.load_test_subject('1470')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1472(self):
    gold_code, tree = self.load_test_subject('1472')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1475(self):
    gold_code, tree = self.load_test_subject('1475')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1480(self):
    gold_code, tree = self.load_test_subject('1480')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1481(self):
    gold_code, tree = self.load_test_subject('1481')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1486(self):
    gold_code, tree = self.load_test_subject('1486')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1491(self):
    gold_code, tree = self.load_test_subject('1491')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1492(self):
    gold_code, tree = self.load_test_subject('1492')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1493(self):
    gold_code, tree = self.load_test_subject('1493')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1496(self):
    gold_code, tree = self.load_test_subject('1496')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1502(self):
    gold_code, tree = self.load_test_subject('1502')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1507(self):
    gold_code, tree = self.load_test_subject('1507')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1512(self):
    gold_code, tree = self.load_test_subject('1512')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1519(self):
    gold_code, tree = self.load_test_subject('1519')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1524(self):
    gold_code, tree = self.load_test_subject('1524')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1528(self):
    gold_code, tree = self.load_test_subject('1528')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1535(self):
    gold_code, tree = self.load_test_subject('1535')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1550(self):
    gold_code, tree = self.load_test_subject('1550')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1551(self):
    gold_code, tree = self.load_test_subject('1551')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1566(self):
    gold_code, tree = self.load_test_subject('1566')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1576(self):
    gold_code, tree = self.load_test_subject('1576')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1598(self):
    gold_code, tree = self.load_test_subject('1598')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1657(self):
    gold_code, tree = self.load_test_subject('1657')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1668(self):
    gold_code, tree = self.load_test_subject('1668')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1669(self):
    gold_code, tree = self.load_test_subject('1669')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1672(self):
    gold_code, tree = self.load_test_subject('1672')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1679(self):
    gold_code, tree = self.load_test_subject('1679')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1716(self):
    gold_code, tree = self.load_test_subject('1716')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1718(self):
    gold_code, tree = self.load_test_subject('1718')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1726(self):
    gold_code, tree = self.load_test_subject('1726')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1732(self):
    gold_code, tree = self.load_test_subject('1732')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1748(self):
    gold_code, tree = self.load_test_subject('1748')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1749(self):
    gold_code, tree = self.load_test_subject('1749')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1752(self):
    gold_code, tree = self.load_test_subject('1752')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1764(self):
    gold_code, tree = self.load_test_subject('1764')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1765(self):
    gold_code, tree = self.load_test_subject('1765')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1768(self):
    gold_code, tree = self.load_test_subject('1768')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1769(self):
    gold_code, tree = self.load_test_subject('1769')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1780(self):
    gold_code, tree = self.load_test_subject('1780')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1790(self):
    gold_code, tree = self.load_test_subject('1790')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1791(self):
    gold_code, tree = self.load_test_subject('1791')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1800(self):
    gold_code, tree = self.load_test_subject('1800')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1812(self):
    gold_code, tree = self.load_test_subject('1812')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1817(self):
    gold_code, tree = self.load_test_subject('1817')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1832(self):
    gold_code, tree = self.load_test_subject('1832')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1833(self):
    gold_code, tree = self.load_test_subject('1833')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1880(self):
    gold_code, tree = self.load_test_subject('1880')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1886(self):
    gold_code, tree = self.load_test_subject('1886')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1910(self):
    gold_code, tree = self.load_test_subject('1910')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1920(self):
    gold_code, tree = self.load_test_subject('1920')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1926(self):
    gold_code, tree = self.load_test_subject('1926')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1929(self):
    gold_code, tree = self.load_test_subject('1929')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1930(self):
    gold_code, tree = self.load_test_subject('1930')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1935(self):
    gold_code, tree = self.load_test_subject('1935')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1976(self):
    gold_code, tree = self.load_test_subject('1976')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1980(self):
    gold_code, tree = self.load_test_subject('1980')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1985(self):
    gold_code, tree = self.load_test_subject('1985')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_1996(self):
    gold_code, tree = self.load_test_subject('1996')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2000(self):
    gold_code, tree = self.load_test_subject('2000')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2011(self):
    gold_code, tree = self.load_test_subject('2011')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2016(self):
    gold_code, tree = self.load_test_subject('2016')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2017(self):
    gold_code, tree = self.load_test_subject('2017')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2027(self):
    gold_code, tree = self.load_test_subject('2027')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2033(self):
    gold_code, tree = self.load_test_subject('2033')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2037(self):
    gold_code, tree = self.load_test_subject('2037')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2047(self):
    gold_code, tree = self.load_test_subject('2047')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2053(self):
    gold_code, tree = self.load_test_subject('2053')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2085(self):
    gold_code, tree = self.load_test_subject('2085')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2095(self):
    gold_code, tree = self.load_test_subject('2095')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2099(self):
    gold_code, tree = self.load_test_subject('2099')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2114(self):
    gold_code, tree = self.load_test_subject('2114')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2115(self):
    gold_code, tree = self.load_test_subject('2115')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2116(self):
    gold_code, tree = self.load_test_subject('2116')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2127(self):
    gold_code, tree = self.load_test_subject('2127')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2129(self):
    gold_code, tree = self.load_test_subject('2129')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2130(self):
    gold_code, tree = self.load_test_subject('2130')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2154(self):
    gold_code, tree = self.load_test_subject('2154')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2161(self):
    gold_code, tree = self.load_test_subject('2161')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2185(self):
    gold_code, tree = self.load_test_subject('2185')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2206(self):
    gold_code, tree = self.load_test_subject('2206')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2215(self):
    gold_code, tree = self.load_test_subject('2215')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2226(self):
    gold_code, tree = self.load_test_subject('2226')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2235(self):
    gold_code, tree = self.load_test_subject('2235')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2244(self):
    gold_code, tree = self.load_test_subject('2244')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2270(self):
    gold_code, tree = self.load_test_subject('2270')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2300(self):
    gold_code, tree = self.load_test_subject('2300')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2336(self):
    gold_code, tree = self.load_test_subject('2336')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2342(self):
    gold_code, tree = self.load_test_subject('2342')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2349(self):
    gold_code, tree = self.load_test_subject('2349')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2352(self):
    gold_code, tree = self.load_test_subject('2352')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2364(self):
    gold_code, tree = self.load_test_subject('2364')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2375(self):
    gold_code, tree = self.load_test_subject('2375')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2379(self):
    gold_code, tree = self.load_test_subject('2379')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2381(self):
    gold_code, tree = self.load_test_subject('2381')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2390(self):
    gold_code, tree = self.load_test_subject('2390')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2396(self):
    gold_code, tree = self.load_test_subject('2396')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2401(self):
    gold_code, tree = self.load_test_subject('2401')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2413(self):
    gold_code, tree = self.load_test_subject('2413')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2425(self):
    gold_code, tree = self.load_test_subject('2425')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2427(self):
    gold_code, tree = self.load_test_subject('2427')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2429(self):
    gold_code, tree = self.load_test_subject('2429')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2460(self):
    gold_code, tree = self.load_test_subject('2460')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2462(self):
    gold_code, tree = self.load_test_subject('2462')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2467(self):
    gold_code, tree = self.load_test_subject('2467')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2469(self):
    gold_code, tree = self.load_test_subject('2469')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2482(self):
    gold_code, tree = self.load_test_subject('2482')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2490(self):
    gold_code, tree = self.load_test_subject('2490')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2493(self):
    gold_code, tree = self.load_test_subject('2493')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2523(self):
    gold_code, tree = self.load_test_subject('2523')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2529(self):
    gold_code, tree = self.load_test_subject('2529')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2535(self):
    gold_code, tree = self.load_test_subject('2535')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2542(self):
    gold_code, tree = self.load_test_subject('2542')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2559(self):
    gold_code, tree = self.load_test_subject('2559')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2560(self):
    gold_code, tree = self.load_test_subject('2560')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2570(self):
    gold_code, tree = self.load_test_subject('2570')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2579(self):
    gold_code, tree = self.load_test_subject('2579')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2594(self):
    gold_code, tree = self.load_test_subject('2594')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2618(self):
    gold_code, tree = self.load_test_subject('2618')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2619(self):
    gold_code, tree = self.load_test_subject('2619')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2620(self):
    gold_code, tree = self.load_test_subject('2620')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2621(self):
    gold_code, tree = self.load_test_subject('2621')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2622(self):
    gold_code, tree = self.load_test_subject('2622')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2623(self):
    gold_code, tree = self.load_test_subject('2623')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2625(self):
    gold_code, tree = self.load_test_subject('2625')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2626(self):
    gold_code, tree = self.load_test_subject('2626')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2627(self):
    gold_code, tree = self.load_test_subject('2627')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2629(self):
    gold_code, tree = self.load_test_subject('2629')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2630(self):
    gold_code, tree = self.load_test_subject('2630')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2631(self):
    gold_code, tree = self.load_test_subject('2631')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2634(self):
    gold_code, tree = self.load_test_subject('2634')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2635(self):
    gold_code, tree = self.load_test_subject('2635')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2637(self):
    gold_code, tree = self.load_test_subject('2637')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2648(self):
    gold_code, tree = self.load_test_subject('2648')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2649(self):
    gold_code, tree = self.load_test_subject('2649')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2650(self):
    gold_code, tree = self.load_test_subject('2650')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2657(self):
    gold_code, tree = self.load_test_subject('2657')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2658(self):
    gold_code, tree = self.load_test_subject('2658')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2661(self):
    gold_code, tree = self.load_test_subject('2661')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2665(self):
    gold_code, tree = self.load_test_subject('2665')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2666(self):
    gold_code, tree = self.load_test_subject('2666')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2667(self):
    gold_code, tree = self.load_test_subject('2667')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2677(self):
    gold_code, tree = self.load_test_subject('2677')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2683(self):
    gold_code, tree = self.load_test_subject('2683')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2685(self):
    gold_code, tree = self.load_test_subject('2685')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2693(self):
    gold_code, tree = self.load_test_subject('2693')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2694(self):
    gold_code, tree = self.load_test_subject('2694')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2695(self):
    gold_code, tree = self.load_test_subject('2695')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2698(self):
    gold_code, tree = self.load_test_subject('2698')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2703(self):
    gold_code, tree = self.load_test_subject('2703')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2704(self):
    gold_code, tree = self.load_test_subject('2704')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2705(self):
    gold_code, tree = self.load_test_subject('2705')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2715(self):
    gold_code, tree = self.load_test_subject('2715')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2721(self):
    gold_code, tree = self.load_test_subject('2721')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2722(self):
    gold_code, tree = self.load_test_subject('2722')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2723(self):
    gold_code, tree = self.load_test_subject('2723')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2724(self):
    gold_code, tree = self.load_test_subject('2724')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2725(self):
    gold_code, tree = self.load_test_subject('2725')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2726(self):
    gold_code, tree = self.load_test_subject('2726')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2727(self):
    gold_code, tree = self.load_test_subject('2727')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2780(self):
    gold_code, tree = self.load_test_subject('2780')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2948(self):
    gold_code, tree = self.load_test_subject('2948')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_2965(self):
    gold_code, tree = self.load_test_subject('2965')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_3042(self):
    gold_code, tree = self.load_test_subject('3042')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_3066(self):
    gold_code, tree = self.load_test_subject('3066')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_3105(self):
    gold_code, tree = self.load_test_subject('3105')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_3108(self):
    gold_code, tree = self.load_test_subject('3108')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_3110(self):
    gold_code, tree = self.load_test_subject('3110')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_3151(self):
    gold_code, tree = self.load_test_subject('3151')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_3160(self):
    gold_code, tree = self.load_test_subject('3160')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_3169(self):
    gold_code, tree = self.load_test_subject('3169')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_3174(self):
    gold_code, tree = self.load_test_subject('3174')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_3191(self):
    gold_code, tree = self.load_test_subject('3191')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_3208(self):
    gold_code, tree = self.load_test_subject('3208')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_3223(self):
    gold_code, tree = self.load_test_subject('3223')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_3306(self):
    gold_code, tree = self.load_test_subject('3306')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_3356(self):
    gold_code, tree = self.load_test_subject('3356')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_3392(self):
    gold_code, tree = self.load_test_subject('3392')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_3394(self):
    gold_code, tree = self.load_test_subject('3394')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_3396(self):
    gold_code, tree = self.load_test_subject('3396')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_3397(self):
    gold_code, tree = self.load_test_subject('3397')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_3402(self):
    gold_code, tree = self.load_test_subject('3402')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_3452(self):
    gold_code, tree = self.load_test_subject('3452')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_3461(self):
    gold_code, tree = self.load_test_subject('3461')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_3462(self):
    gold_code, tree = self.load_test_subject('3462')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)

  def test_3463(self):
    gold_code, tree = self.load_test_subject('3463')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)


if __name__ == '__main__':
  unittest.main()
