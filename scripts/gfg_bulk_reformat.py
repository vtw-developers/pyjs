import black

import p_consts
import p_utils


fpaths = list(p_consts.GFG_BENCHMARK_DIR.glob("G*.py"))
for fpath in fpaths:
  code = p_utils.read_text(fpath)
  test, main, call = code.split(p_consts.TEST_MAIN_CALL_DELIMITER)
  print(fpath)
  print(main)

  formatted_main = black.format_str(main, mode=black.Mode())
  print(formatted_main)

  formatted_code = f'{p_consts.TEST_MAIN_CALL_DELIMITER}'.join([test, f'\n{formatted_main}', call])
  p_utils.write_text(fpath, formatted_code)
