# interface to pynguin test generation tool

import subprocess
import tempfile
from pathlib import Path
from typing import List

import p_consts
import p_utils


logger = p_utils.setup_logger(__name__)


def run_pynguin(f_gold_str: str) -> List[str]:
  '''
  RAISE pass all exceptions to the caller.
  '''
  logger.debug(f'Starting Pynguin to generate tests for:\n{f_gold_str}')
  pynguin = p_consts.BUILD_DIR / 'pynguin'

  # write the f_gold_str to a temporary file
  temp_f_gold_str_fpath = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
  temp_f_gold_str_fpath.write(f_gold_str)
  temp_f_gold_str_fpath.close()
  logger.debug(f'Writing "f_gold_str" into "{temp_f_gold_str_fpath.name}"')

  # create a temporary directory for the output
  temp_output_dir = tempfile.TemporaryDirectory()
  logger.debug(f'Creating temporary output directory to store Pynguin output: "{temp_output_dir.name}"')

  # run pynguin with the temporary file as input
  cmd = [str(pynguin), temp_f_gold_str_fpath.name, '--output-dir', temp_output_dir.name]

  try:
    process = subprocess.run(cmd, check=True, timeout=p_consts.PYNGUIN_TIMEOUT_SECONDS, capture_output=True)

    gen_test_fns_str = []
    for file in Path(temp_output_dir.name).iterdir():
      if file.name.endswith('.py'):
        gen_test_fns_str.append(file.read_text())
    return gen_test_fns_str

  # Pynguin timed out
  except subprocess.TimeoutExpired:
    logger.error(f'Pynguin timed out after {p_consts.PYNGUIN_TIMEOUT_SECONDS} seconds')
    raise

  # Pynguin ended with non-zero exit code
  except subprocess.CalledProcessError as e:
    logger.error(f'Pynguin failed with return code {e.returncode}')
    logger.error(f'Pynguin failed with error: {e.stderr.decode()}')
    raise

  # some other error occurred
  except Exception as e:
    logger.error(f'An unexpected error occurred: {e}')
    raise

  finally:
    temp_output_dir.cleanup()


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
