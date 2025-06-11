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


if __name__ == '__main__':
  unittest.main()
