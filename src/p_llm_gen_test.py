import json
import unittest
from typing import Tuple

import p_consts
import p_utils
import p_llm_gen


class TestExtractCodeBlocks(unittest.TestCase):
  def setUp(self):
    self.fixtures_dirpath = p_consts.TEST_ARTIFACTS_DIR / 'p-llm-gen' / 'extract-code-blocks'

  def load_fixture(self, fixture_id: str) -> Tuple[str, list]:
    raw_response = p_utils.read_text(self.fixtures_dirpath / f'response-{fixture_id}.md')
    gold = p_utils.read_json(self.fixtures_dirpath / f'response-{fixture_id}-gold.json')
    return raw_response, gold

  def test_simple_001(self):
    raw_response, gold = self.load_fixture('001')
    response = p_llm_gen.extract_code_blocks(raw_response)
    self.assertCountEqual(response, gold)

  def test_simple_002(self):
    raw_response, gold = self.load_fixture('002')
    response = p_llm_gen.extract_code_blocks(raw_response)
    self.assertCountEqual(response, gold)

  def test_simple_003(self):
    raw_response, gold = self.load_fixture('003')
    response = p_llm_gen.extract_code_blocks(raw_response)
    self.assertCountEqual(response, gold)

  def test_simple_004(self):
    raw_response, gold = self.load_fixture('004')
    response = p_llm_gen.extract_code_blocks(raw_response)
    self.assertCountEqual(response, gold)

  def test_simple_005(self):
    raw_response, gold = self.load_fixture('005')
    response = p_llm_gen.extract_code_blocks(raw_response)
    self.assertCountEqual(response, gold)

  def test_simple_006(self):
    raw_response, gold = self.load_fixture('006')
    response = p_llm_gen.extract_code_blocks(raw_response)
    self.assertCountEqual(response, gold)

  def test_simple_007(self):
    raw_response, gold = self.load_fixture('007')
    response = p_llm_gen.extract_code_blocks(raw_response)
    self.assertCountEqual(response, gold)

  def test_simple_008(self):
    raw_response, gold = self.load_fixture('008')
    response = p_llm_gen.extract_code_blocks(raw_response)
    self.assertCountEqual(response, gold)

  def test_simple_009(self):
    raw_response, gold = self.load_fixture('009')
    response = p_llm_gen.extract_code_blocks(raw_response)
    self.assertCountEqual(response, gold)

  def test_simple_010(self):
    raw_response, gold = self.load_fixture('010')
    response = p_llm_gen.extract_code_blocks(raw_response)
    self.assertCountEqual(response, gold)

  def test_simple_011(self):
    raw_response, gold = self.load_fixture('011')
    response = p_llm_gen.extract_code_blocks(raw_response)
    self.assertCountEqual(response, gold)

  def test_simple_012(self):
    raw_response, gold = self.load_fixture('012')
    response = p_llm_gen.extract_code_blocks(raw_response)
    self.assertCountEqual(response, gold)

  def test_simple_013(self):
    raw_response, gold = self.load_fixture('013')
    response = p_llm_gen.extract_code_blocks(raw_response)
    self.assertCountEqual(response, gold)

  def test_simple_014(self):
    raw_response, gold = self.load_fixture('014')
    response = p_llm_gen.extract_code_blocks(raw_response)
    self.assertCountEqual(response, gold)

  def test_simple_015(self):
    raw_response, gold = self.load_fixture('015')
    response = p_llm_gen.extract_code_blocks(raw_response)
    self.assertCountEqual(response, gold)

  def test_simple_016(self):
    raw_response, gold = self.load_fixture('016')
    response = p_llm_gen.extract_code_blocks(raw_response)
    self.assertCountEqual(response, gold)

  def test_simple_017(self):
    raw_response, gold = self.load_fixture('017')
    response = p_llm_gen.extract_code_blocks(raw_response)
    self.assertCountEqual(response, gold)


class TestGetTP2Offline(unittest.TestCase):
  def setUp(self):
    self.maxDiff = None
    self.fixtures_dir = p_consts.TEST_ARTIFACTS_DIR / 'p-llm-gen' / 'get-tp2-offline'

  def load_fixture(self, test_id: str) -> Tuple[str, str, str, str, dict]:
    fixture = p_utils.read_text(self.fixtures_dir / f'{test_id}.txt')
    sp1, tp1, sp2, gold_tp2, context_str = fixture.split(f'\n{p_consts.TEST_MAIN_CALL_DELIMITER}\n')
    return sp1, tp1, sp2, gold_tp2, json.loads(context_str)

  def test_all(self):
    test_ids = sorted(f.stem for f in self.fixtures_dir.glob('*.txt'))
    for test_id in test_ids:
      with self.subTest(test_id=test_id):
        sp1, tp1, sp2, gold_tp2, context = self.load_fixture(test_id)
        tp2 = p_llm_gen.get_tp2_offline(sp1, tp1, sp2, context)
        self.assertEqual(tp2, gold_tp2)


if __name__ == '__main__':
  unittest.main()
