import p_consts
import p_utils


logger = p_utils.setup_logger(__name__)


fpaths = sorted(p_consts.GFG_BENCHMARK_DIR.glob("G*.py"))
for fpath in fpaths:
  subject_name = fpath.stem[:5]  # e.g. G0001
  code = p_utils.read_text(fpath)
  test, main, call = code.split(p_consts.TEST_MAIN_CALL_DELIMITER)

  test_size = len(test)
  if test_size > 5000:
    logger.debug(f"{subject_name}: test_fn size={test_size}")
