import p_consts
import p_utils


fpaths = list(p_consts.GFG_BENCHMARK_DIR.glob("G*.py"))
for fpath in fpaths:
  code = p_utils.read_text(fpath)
  test, main, call = code.split(p_consts.TEST_MAIN_CALL_DELIMITER)
  print(fpath)
  print(main)

  dst_dir = p_consts.TEST_ARTIFACTS_DIR / 'py' / 'TestPrettyPrinter'
  p_utils.write_text(dst_dir / fpath.name, main.strip())
