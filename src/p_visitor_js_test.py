import unittest

import p_consts
import p_visitor_js


class TestPrettyPrinter(unittest.TestCase):
  def setUp(self):
    self.snippets_dir = p_consts.TEST_ARTIFACTS_DIR / 'js' / 'leetcode-javascript' / 'solutions'
    self.parser = p_consts.PARSER_DICT['js']
    self.maxDiff = None

  def test_all(self):
    for fpath in sorted(self.snippets_dir.glob('*.js')):
      subject_name = fpath.stem[:4]
      # tree-sitter version we are using cannot parse it correctly
      if subject_name == '0833':
        continue
      subject_code = fpath.read_text().strip()
      with self.subTest(subject_name=subject_name):
        ts_tree = self.parser.parse(bytes(subject_code, 'utf8'))
        tree = p_visitor_js.Tree.from_ts_tree(ts_tree)
        pp_code = p_visitor_js.PrettyPrinter().visit(tree.root_node).strip()
        self.assertEqual(subject_code, pp_code)


class TestCommentsRemover(unittest.TestCase):
  def setUp(self):
    self.snippets_dir = p_consts.TEST_ARTIFACTS_DIR / 'p-visitor-js' / 'comments-remover'
    self.maxDiff = None

  def test_all(self):
    NUM_SNIPPETS = 4
    for i in range(1, NUM_SNIPPETS + 1):
      fpath = self.snippets_dir / f'snippet_{i:03d}_in.js'
      snippet = fpath.read_text().strip()
      with self.subTest(i=i):
        no_comments_code = p_visitor_js.CommentsRemover.remove_comments(snippet)
        gold_fpath = self.snippets_dir / f'snippet_{i:03d}_out.js'
        gold_code = gold_fpath.read_text().strip()
        self.assertEqual(gold_code, no_comments_code)


if __name__ == '__main__':
  unittest.main()
