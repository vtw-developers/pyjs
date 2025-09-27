import re

import p_consts
import p_utils


RE_FOR = r'for (\w+) in range'
ASSIGNMENT_TEMPLATES = [
  '{var} = ',
  '{var} = {var} + ',
  '{var} += ',
  '{var} = {var} -',
  '{var} -= ',
  '{var} = {var} *',
  '{var} *= ',
  '{var} = {var} /',
  '{var} /= ',
  '{var} = {var} //',
  '{var} //= ',
  '{var} = {var} %',
  '{var} %= ',
  '{var} = {var} **',
  '{var} **= ',
  '{var} = {var} &',
  '{var} &= ',
  '{var} = {var} |',
  '{var} |= ',
  '{var} = {var} ^',
  '{var} ^= ',
  '{var} = {var} <<',
  '{var} <<= ',
  '{var} = {var} >>',
  '{var} >>= ',
]


benchmarks_subject_fpaths = list(p_consts.GFG_BENCHMARK_DIR.glob("G*.py"))

for i, fpath in enumerate(benchmarks_subject_fpaths, start=1):
  print(f"Processing {i}/{len(benchmarks_subject_fpaths)}: {fpath}")
  code = p_utils.read_text(fpath)
  test, main, call = code.split(p_consts.TEST_MAIN_CALL_DELIMITER)

  loop_vars = re.findall(RE_FOR, main)
  if len(loop_vars) == 0:
    print("No loop variables found, skipping...")
    continue

  print(f"Loop variables found: {loop_vars}")

  flag_usage_found = False
  for var in loop_vars:
    for template in ASSIGNMENT_TEMPLATES:
      pattern = template.format(var=var)
      if pattern in main:
        print(f"Found assignment to loop variable '{var}': {pattern}")
        flag_usage_found = True

  if not flag_usage_found:
    print("No assignments to loop variables found.")
  else:
    print("Assignments to loop variables found.")
    input('Press Enter to continue...')
