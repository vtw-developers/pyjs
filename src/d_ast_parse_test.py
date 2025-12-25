import unittest

import d_ast_parse
import p_consts


class TestGetRangeCursor(unittest.TestCase):
  def setUp(self):
    self.maxDiff = None

  def test_G0001(self):
    code = '''
def f_gold(x):
    m = 1
    while x & m:
        x = x ^ m
        m <<= 1
    x = x ^ m
    return x
'''.strip()
    orig_ast, _ = d_ast_parse.parse_text_dbg(code, 'py')

    # module
    with self.assertRaises(ValueError):
      d_ast_parse.get_range_cursor(orig_ast, 0)

    ast, start_idx, end_idx = d_ast_parse.get_range_cursor(orig_ast, 3)
    self.assertEqual(ast[1], 1)
    self.assertEqual(start_idx, 4)
    self.assertEqual(end_idx, 5)

    ast, start_idx, end_idx = d_ast_parse.get_range_cursor(orig_ast, 6)
    self.assertEqual(ast[1], 5)
    self.assertEqual(start_idx, 2)
    self.assertEqual(end_idx, 3)

    ast, start_idx, end_idx = d_ast_parse.get_range_cursor(orig_ast, 13)
    self.assertEqual(ast[1], 11)
    self.assertEqual(start_idx, 4)
    self.assertEqual(end_idx, 5)

    ast, start_idx, end_idx = d_ast_parse.get_range_cursor(orig_ast, 32)
    self.assertEqual(ast[1], 31)
    self.assertEqual(start_idx, 3)
    self.assertEqual(end_idx, 4)

    # large id
    with self.assertRaises(ValueError):
      d_ast_parse.get_range_cursor(orig_ast, 1111)

    # negative id
    with self.assertRaises(ValueError):
      d_ast_parse.get_range_cursor(orig_ast, -1)


class TestAreNodesEqual(unittest.TestCase):
  def setUp(self):
    self.maxDiff = None
    self.snippets_dir = p_consts.TEST_ARTIFACTS_DIR / 'd-ast-parse' / 'are-nodes-equal'

  def test_all(self):
    fixture_fpaths = sorted(self.snippets_dir.glob('*.py'))
    for fpath in fixture_fpaths:
      subject_name = fpath.stem[:5]
      with self.subTest(subject_name=subject_name):
        code = fpath.read_text()
        ast, _ = d_ast_parse.parse_text_dbg(code, 'py')
        self.assertTrue(d_ast_parse.are_nodes_equal(ast, ast))


if __name__ == '__main__':
  unittest.main()
