import asyncio
import unittest
from typing import Tuple

import d_ast_parse
import p_consts
import p_data_structures as pds
import p_grammar
import p_pirel
import p_utils


logger = p_utils.setup_logger(__name__)


class TestGetAlternativeStartingNodeTypes(unittest.TestCase):
  def setUp(self):
    self.fixtures_dir_path = p_consts.TEST_ARTIFACTS_DIR / 'p-grammar' / 'get-alternative-starting-node-types'
    self.maxDiff = None

  def load_fixture(self, test_id: str) -> dict:
    data = p_utils.read_json(self.fixtures_dir_path / f'{test_id}.json')
    return data

  def test_all(self):
    test_ids = sorted([p.stem for p in (self.fixtures_dir_path).glob('*.json')])
    for test_id in test_ids:
      with self.subTest(test_id=test_id):
        data = self.load_fixture(test_id)

        # prepare inputs
        src_code = data['src_code']
        node_path = data['node_path']
        src_lang = 'py'
        grammar = p_grammar.TreeSitterGrammar.from_dict(p_consts.GRAMMAR_DICT_READONLY[src_lang])
        tree = pds.DuoGlotTree.from_code_str(src_code, src_lang)
        assert len(tree.root_node.get_children()) == 1
        context_node = tree.root_node.get_children()[0]
        node = context_node.get_child_by_path(node_path)

        golden_return_dict = data['return_dict']
        return_dict = {
          'error_class': 'n/a',
          'error_msg': 'n/a',
        }

        try:
          alt_starting_nodes = p_grammar.get_alternative_starting_node_types(node, grammar)
          return_dict['alt_starting_nodes'] = [(node.get_id(), node.get_type(), alt_node_types) for node, alt_node_types in alt_starting_nodes]
        except Exception as e:
          return_dict['error_class'] = e.__class__.__name__
          return_dict['error_msg'] = str(e)

        eq, p, v1, v2 = p_utils.deep_json_diff(golden_return_dict, return_dict, coerce_types=True)
        self.assertTrue(eq, f'diff: {p}, {v1}, {v2}')


if __name__ == '__main__':
  unittest.main()
