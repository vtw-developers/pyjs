import p_consts
import p_utils


fpaths = list(p_consts.GFG_BENCHMARK_DIR.glob("G*.py"))
for fpath in fpaths:
  ref_fpath = p_consts.TEST_ARTIFACTS_DIR / 'py' / 'TestPrettyPrinter' / fpath.name
  ref_main_code = p_utils.read_text(ref_fpath)

  code = p_utils.read_text(fpath)
  test, main, call = code.split(p_consts.TEST_MAIN_CALL_DELIMITER)

  updated_code = p_consts.TEST_MAIN_CALL_DELIMITER.join([
      test,
      f'\n{ref_main_code}\n',
      call
  ])

  # print(updated_code)
  p_utils.write_text(fpath, updated_code)

  # input()
