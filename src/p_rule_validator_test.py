import json
import unittest

import p_consts
import p_rule_validator as prval


class TestProcessUsedRuleIds(unittest.TestCase):
  def to_string(self, obj) -> str:
    return json.dumps(obj)

  def test_simple_001(self):
    used_rule_ids_history = [
      [9, 10, 11, 12, 13, 6, 14, 1, 14, 11],
      [9, 10, 11, 12, 13, 7, 14, 1, 14, 11]
    ]
    gold = [
      [
        {
          'idx': 5,
          'old_rule_id': 6,
          'new_rule_id': 7,
        }
      ]
    ]
    res = prval.process_used_rule_ids_history_deprecated(used_rule_ids_history)
    self.assertEqual(len(used_rule_ids_history), len(res) + 1, 'result is one less than input')
    self.assertEqual(self.to_string(gold), self.to_string(res))

  def test_simple_002(self):
    used_rule_ids_history = [
      [12, 13, 14, 15, 16, 9, 17, 1, 17, 14, 9, 17, 1, 17, 14, 8, 17, 1, 17, 17, 6, 17, 1, 17, 14, 4],
      [12, 13, 14, 15, 16, 10, 17, 1, 17, 14, 9, 17, 1, 17, 14, 8, 17, 1, 17, 17, 6, 17, 1, 17, 14, 4]
    ]
    gold = [
      [
        {
          'idx': 5,
          'old_rule_id': 9,
          'new_rule_id': 10,
        }
      ]
    ]
    res = prval.process_used_rule_ids_history_deprecated(used_rule_ids_history)
    self.assertEqual(len(used_rule_ids_history), len(res) + 1, 'result is one less than input')
    self.assertEqual(self.to_string(gold), self.to_string(res))

  def test_simple_003(self):
    used_rule_ids_history = [
      [24, 25, 26, 27, 26, 26, 28, 21, 29, 1, 29, 26, 21, 29, 1, 29, 26, 20, 29, 1, 29, 29, 18, 29, 1, 29, 26, 4, 17, 1, 29, 29, 21, 16, 12, 10, 6, 29, 1, 29, 26, 1, 29, 29, 23],
      [24, 25, 26, 27, 26, 26, 28, 22, 29, 1, 29, 26, 21, 29, 1, 29, 26, 20, 29, 1, 29, 29, 18, 29, 1, 29, 26, 4, 17, 1, 29, 29, 21, 16, 12, 10, 6, 29, 1, 29, 26, 1, 29, 29, 23],
      [24, 25, 26, 27, 26, 26, 28, 22, 29, 1, 29, 26, 21, 29, 1, 29, 26, 20, 29, 1, 29, 29, 18, 29, 1, 29, 26, 4, 17, 1, 29, 29, 22, 16, 12, 10, 6, 29, 1, 29, 26, 1, 29, 29, 23]
    ]
    gold = [
      [
        {
          'idx': 7,
          'old_rule_id': 21,
          'new_rule_id': 22,
        }
      ],
      [
        {
          'idx': 32,
          'old_rule_id': 21,
          'new_rule_id': 22,
        }
      ]
    ]
    res = prval.process_used_rule_ids_history_deprecated(used_rule_ids_history)
    self.assertEqual(len(used_rule_ids_history), len(res) + 1, 'result is one less than input')
    self.assertEqual(self.to_string(gold), self.to_string(res))

  def test_simple_004(self):
    used_rule_ids_history = [
      [29, 30, 31, 32, 31, 31, 31, 31, 33, 26, 34, 1, 34, 31, 26, 34, 1, 34, 31, 25, 34, 1, 34, 34, 23, 34, 1, 34, 31, 4, 22, 1, 34, 34, 26, 21, 17, 15, 11, 34, 1, 34, 31, 10, 7, 1, 34, 34, 28, 6, 7, 1, 34, 34, 28, 1, 34, 34, 28, 1, 34, 34, 28],
      [29, 30, 31, 32, 31, 31, 31, 31, 33, 27, 34, 1, 34, 31, 26, 34, 1, 34, 31, 25, 34, 1, 34, 34, 23, 34, 1, 34, 31, 4, 22, 1, 34, 34, 26, 21, 17, 15, 11, 34, 1, 34, 31, 10, 7, 1, 34, 34, 28, 6, 7, 1, 34, 34, 28, 1, 34, 34, 28, 1, 34, 34, 28],
      [29, 30, 31, 32, 31, 31, 31, 31, 33, 27, 34, 1, 34, 31, 26, 34, 1, 34, 31, 25, 34, 1, 34, 34, 23, 34, 1, 34, 31, 4, 22, 1, 34, 34, 27, 21, 17, 15, 11, 34, 1, 34, 31, 10, 7, 1, 34, 34, 28, 6, 7, 1, 34, 34, 28, 1, 34, 34, 28, 1, 34, 34, 28],
      [29, 30, 31, 32, 31, 31, 31, 31, 33, 27, 34, 1, 34, 31, 26, 34, 1, 34, 31, 25, 34, 1, 34, 34, 23, 34, 1, 34, 31, 4, 22, 1, 34, 34, 27, 21, 17, 15, 11, 34, 1, 34, 31, 10, 8, 1, 34, 34, 28, 6, 7, 1, 34, 34, 28, 1, 34, 34, 28, 1, 34, 34, 28],
      [29, 30, 31, 32, 31, 31, 31, 31, 33, 27, 34, 1, 34, 31, 26, 34, 1, 34, 31, 25, 34, 1, 34, 34, 23, 34, 1, 34, 31, 4, 22, 1, 34, 34, 27, 21, 17, 15, 11, 34, 1, 34, 31, 10, 8, 1, 34, 34, 28, 6, 8, 1, 34, 34, 28, 1, 34, 34, 28, 1, 34, 34, 28]
    ]
    gold = [
      [
        {
          'idx': 9,
          'old_rule_id': 26,
          'new_rule_id': 27,
        }
      ],
      [
        {
          'idx': 34,
          'old_rule_id': 26,
          'new_rule_id': 27,
        }
      ],
      [
        {
          'idx': 44,
          'old_rule_id': 7,
          'new_rule_id': 8,
        }
      ],
      [
        {
          'idx': 50,
          'old_rule_id': 7,
          'new_rule_id': 8,
        }
      ]
    ]
    res = prval.process_used_rule_ids_history_deprecated(used_rule_ids_history)
    self.assertEqual(len(used_rule_ids_history), len(res) + 1, 'result is one less than input')
    self.assertEqual(self.to_string(gold), self.to_string(res))

  def test_simple_005(self):
    used_rule_ids_history = [
      [0, 1, 2, 3, 4],
      [0, 2, 2, 3, 4],
      [0, 3, 2, 3, 4],
      [0, 1, 4, 3, 4],
      [0, 1, 2, 5, 4],
      [0, 1, 2, 6, 6],
      [0, 1, 2, 6, 6],
      [7, 7, 7, 7, 7]
    ]
    gold = [
      [
        {
          'idx': 1,
          'old_rule_id': 1,
          'new_rule_id': 2,
        }
      ],
      [
        {
          'idx': 1,
          'old_rule_id': 2,
          'new_rule_id': 3,
        }
      ],
      [
        {
          'idx': 1,
          'old_rule_id': 3,
          'new_rule_id': 1,
        },
        {
          'idx': 2,
          'old_rule_id': 2,
          'new_rule_id': 4,
        }
      ],
      [
        {
          'idx': 2,
          'old_rule_id': 4,
          'new_rule_id': 2,
        },
        {
          'idx': 3,
          'old_rule_id': 3,
          'new_rule_id': 5,
        }
      ],
      [
        {
          'idx': 3,
          'old_rule_id': 5,
          'new_rule_id': 6,
        },
        {
          'idx': 4,
          'old_rule_id': 4,
          'new_rule_id': 6,
        }
      ],
      [],
      [
        {
          'idx': 0,
          'old_rule_id': 0,
          'new_rule_id': 7,
        },
        {
          'idx': 1,
          'old_rule_id': 1,
          'new_rule_id': 7,
        },
        {
          'idx': 2,
          'old_rule_id': 2,
          'new_rule_id': 7,
        },
        {
          'idx': 3,
          'old_rule_id': 6,
          'new_rule_id': 7,
        },
        {
          'idx': 4,
          'old_rule_id': 6,
          'new_rule_id': 7,
        }
      ]
    ]
    res = prval.process_used_rule_ids_history_deprecated(used_rule_ids_history)
    self.assertEqual(len(used_rule_ids_history), len(res) + 1, 'result is one less than input')
    self.assertEqual(self.to_string(gold), self.to_string(res))

  def test_empty_001(self):
    used_rule_ids_history = [
      [9, 10, 11, 12, 13, 6, 14, 1, 14, 11],
    ]
    gold = []
    res = prval.process_used_rule_ids_history_deprecated(used_rule_ids_history)
    self.assertEqual(len(used_rule_ids_history), len(res) + 1, 'result is one less than input')
    self.assertEqual(self.to_string(gold), self.to_string(res))


if __name__ == '__main__':
  unittest.main()
