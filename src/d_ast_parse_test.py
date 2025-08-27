import unittest

import d_ast_parse


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


if __name__ == '__main__':
  unittest.main()
