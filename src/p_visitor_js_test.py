import unittest
from typing import Tuple

import p_consts
import p_utils
import p_visitor_js as pvjs


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
        tree = pvjs.Tree.from_ts_tree(ts_tree)
        pp_code = pvjs.PrettyPrinter().visit(tree.root_node).strip()
        self.assertEqual(subject_code, pp_code)


class TestCommentsRemover(unittest.TestCase):
  def setUp(self):
    self.snippets_dir = p_consts.TEST_ARTIFACTS_DIR / 'p-visitor-js' / 'comments-remover'
    self.maxDiff = None

  def test_all(self):
    NUM_SNIPPETS = 5
    for i in range(1, NUM_SNIPPETS + 1):
      fpath = self.snippets_dir / f'snippet_{i:03d}_in.js'
      snippet = fpath.read_text().strip()
      with self.subTest(i=i):
        no_comments_code = pvjs.CommentsRemover.remove_comments(snippet)
        gold_fpath = self.snippets_dir / f'snippet_{i:03d}_out.js'
        gold_code = gold_fpath.read_text().strip()
        self.assertEqual(gold_code, no_comments_code)


class TestFunctionInvocationReplacer(unittest.TestCase):
  def setUp(self):
    self.fixtures_dir_path = p_consts.TEST_ARTIFACTS_DIR / 'p-visitor-js' / 'function-invocation-replacer'
    self.maxDiff = None

  def get_snippets(self, snippet_id: str) -> Tuple[str, str]:
    snippet = p_utils.read_text(self.fixtures_dir_path / f'{snippet_id}_in.js')
    gold = p_utils.read_text(self.fixtures_dir_path / f'{snippet_id}_out.js')
    return snippet, gold

  def test_all_int(self):
    NUM_TESTS = 47
    for i in range(1, NUM_TESTS + 1):
      snippet_id = f'int88888888_{i:03d}'
      with self.subTest(snippet_id=snippet_id):
        snippet, gold_snippet = self.get_snippets(snippet_id)
        replaced, replacement_done = pvjs.FunctionInvocationReplacer.replace_function_invocations(snippet, 'f_gold', 'f_gold', 88888888)
        self.assertTrue(replacement_done)
        self.assertEqual(replaced, gold_snippet)

  def test_all_false(self):
    NUM_TESTS = 47
    for i in range(1, NUM_TESTS + 1):
      snippet_id = f'false_{i:03d}'
      with self.subTest(snippet_id=snippet_id):
        snippet, gold_snippet = self.get_snippets(snippet_id)
        replaced, replacement_done = pvjs.FunctionInvocationReplacer.replace_function_invocations(snippet, 'f_gold', 'f_gold', False)
        self.assertTrue(replacement_done)
        self.assertEqual(replaced, gold_snippet)


if __name__ == '__main__':
  unittest.main()
