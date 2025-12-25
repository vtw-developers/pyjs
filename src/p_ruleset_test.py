import unittest

import p_consts
import p_ruleset


class TestRuleset(unittest.TestCase):
  def test_load_starting_ruleset(self):
    sr = p_ruleset.Ruleset.from_starting_ruleset(p_consts.STARTING_RULESET_FPATH.read_text())
    num_rules = 19
    self.assertIsInstance(sr, p_ruleset.Ruleset)
    self.assertIsInstance(sr.rules, list)
    self.assertEqual(len(sr.rules), num_rules, f'Expected {num_rules} rules in the starting ruleset')


if __name__ == '__main__':
  unittest.main()
