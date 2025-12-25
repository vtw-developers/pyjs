import unittest
from typing import Tuple

import p_consts
import p_generator_lw
import p_utils


logger = p_utils.setup_logger(__name__)


class TestGenerateTspsLightweight(unittest.TestCase):
  def setUp(self):
    self.fixtures_dir = p_consts.TEST_ARTIFACTS_DIR / 'p-generator-lw' / 'generate-tsps-lightweight'
    self.maxDiff = None

  def load_fixture(self, subdir: str, test_id: str) -> Tuple[list, dict, dict]:
    data = p_utils.read_json(self.fixtures_dir / subdir / f'{test_id}.json')
    ref_tsps = data['tsps']
    template_dict = data['template_dict']
    ref_updated_template_dict = data['updated_template_dict']
    return ref_tsps, template_dict, ref_updated_template_dict

  def test_no_error(self):
    test_ids = sorted([f.stem for f in (self.fixtures_dir / 'no-error').glob('*.json')])
    for test_id in test_ids:
      with self.subTest(test_id=test_id):
        logger.debug(f'Running test {test_id}')
        ref_tsps, template_dict, ref_updated_template_dict = self.load_fixture('no-error', test_id)
        tsps, updated_template_dict = p_generator_lw.generate_tsps_lightweight(template_dict)
        eq, p, v1, v2 = p_utils.deep_json_diff(ref_tsps, tsps, coerce_types=True)
        self.assertTrue(eq, f'TSPs do not match for test {test_id}:\nPath: {p}\nValue1: {v1}\nValue2: {v2}')
        eq, p, v1, v2 = p_utils.deep_json_diff(ref_updated_template_dict, updated_template_dict, coerce_types=True)
        self.assertTrue(eq, f'Updated template dicts do not match for test {test_id}:\nPath: {p}\nValue1: {v1}\nValue2: {v2}')

  def test_assertion_error_cpnmbtsapn(self):
    test_ids = sorted([f.stem for f in (self.fixtures_dir / 'error-1').glob('*.json')])
    for test_id in test_ids:
      with self.subTest(test_id=test_id):
        logger.debug(f'Running test {test_id}')
        ref_tsps, template_dict, ref_updated_template_dict = self.load_fixture('error-1', test_id)
        with self.assertRaisesRegex(AssertionError, r'^cursor_prob_node must be the same as problematic_node'):
          tsps, updated_template_dict = p_generator_lw.generate_tsps_lightweight(template_dict)


if __name__ == '__main__':
  unittest.main()
