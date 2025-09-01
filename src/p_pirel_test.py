import unittest

import p_data_structures as pds
import p_pirel


class TestAdaptRuleChoicesGetNewNid(unittest.TestCase):
  def setUp(self):
    pass

  def test_01(self):
    code = '''
def f_gold(s):
    myexactlog(1, (3 * math.sqrt(3) * (s * s)) / 2)
    return (3 * math.sqrt(3) * (s * s)) / 2
'''.strip()

    new_code = '''
return (3 * math.sqrt(3) * (s * s)) / 2
'''.strip()

    tree = pds.DuoGlotTree.from_code_str(code, 'py')
    new_tree = pds.DuoGlotTree.from_code_str(new_code, 'py')

    nid = 27
    new_id = p_pirel._adapt_rule_choices_get_new_nid(tree, nid, new_tree)
    self.assertEqual(new_id, 1)

    nid = 28
    new_id = p_pirel._adapt_rule_choices_get_new_nid(tree, nid, new_tree)
    self.assertEqual(new_id, 2)

    nid = 29
    new_id = p_pirel._adapt_rule_choices_get_new_nid(tree, nid, new_tree)
    self.assertEqual(new_id, 3)

    nid = 30
    new_id = p_pirel._adapt_rule_choices_get_new_nid(tree, nid, new_tree)
    self.assertEqual(new_id, 4)

    nid = 33
    new_id = p_pirel._adapt_rule_choices_get_new_nid(tree, nid, new_tree)
    self.assertEqual(new_id, 7)

  def test_expect_assertion_single_node_in_code(self):
    code = '''
def f_gold(s):
    duplicate = (3 * math.sqrt(3) * (s * s)) / 2
    myexactlog(1, (3 * math.sqrt(3) * (s * s)) / 2)
    return (3 * math.sqrt(3) * (s * s)) / 2
'''.strip()

    new_code = '''
return (3 * math.sqrt(3) * (s * s)) / 2
'''.strip()
    
    tree = pds.DuoGlotTree.from_code_str(code, 'py')
    new_tree = pds.DuoGlotTree.from_code_str(new_code, 'py')

    nid = 9  # `(3 * math.sqrt(3) * (s * s)) / 2`
    with self.assertRaises(AssertionError) as cm:
      p_pirel._adapt_rule_choices_get_new_nid(tree, nid, new_tree)
    self.assertEqual(str(cm.exception), 'support only one similar node in the tree')

  def test_expect_assertion_single_new_node(self):
    code = '''
def f_gold(s):
    myexactlog(1, (3 * math.sqrt(3) * (s * s)) / 2)
    return (3 * math.sqrt(3) * (s * s)) / 2
'''.strip()

    new_code = '''
duplicate = (3 * math.sqrt(3) * (s * s)) / 2
return (3 * math.sqrt(3) * (s * s)) / 2
'''.strip()
    
    tree = pds.DuoGlotTree.from_code_str(code, 'py')
    new_tree = pds.DuoGlotTree.from_code_str(new_code, 'py')

    nid = 28  # `(3 * math.sqrt(3) * (s * s)) / 2`
    with self.assertRaises(AssertionError) as cm:
      p_pirel._adapt_rule_choices_get_new_nid(tree, nid, new_tree)
    self.assertEqual(str(cm.exception), 'support only one similar node in the new_tree')


if __name__ == '__main__':
  unittest.main()
