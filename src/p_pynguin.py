# interface to pynguin test generation tool

import subprocess
import tempfile
from pathlib import Path
from typing import List

import p_consts


def run_pynguin(f_gold_str: str) -> List[str]:
  pynguin = p_consts.BUILD_DIR / 'pynguin'

  # write the f_gold_str to a temporary file
  temp_f_gold_str_fpath = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
  temp_f_gold_str_fpath.write(f_gold_str)
  temp_f_gold_str_fpath.close()

  # create a temporary directory for the output
  temp_output_dir = tempfile.TemporaryDirectory()

  # run pynguin with the temporary file as input
  cmd = [str(pynguin), temp_f_gold_str_fpath.name, '--output-dir', temp_output_dir.name]
  process = subprocess.run(cmd, check=True)

  if process.returncode != 0:
    raise RuntimeError('Pynguin failed to run')

  gen_test_fns_str = []
  for file in Path(temp_output_dir.name).iterdir():
    if file.name.endswith('.py'):
      gen_test_fns_str.append(file.read_text())

  temp_output_dir.cleanup()
  return gen_test_fns_str


if __name__ == '__main__':
  input_file = '''# triangle example from
# https://pynguin.readthedocs.io/en/latest/user/quickstart.html#a-simple-example
def f_gold(x: int, y: int, z: int) -> str:
    if x == y == z:
        return "Equilateral triangle"
    if x in {y, z} or y == z:
        return "Isosceles triangle"
    return "Scalene triangle"'''
  result_files = run_pynguin(input_file)
  for result_file in result_files:
    print(f'Generated test file:\n{result_file}')
