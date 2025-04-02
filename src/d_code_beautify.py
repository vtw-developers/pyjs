import d_consts
import d_utils
import jsbeautifier


def beautify(language, code_str):
  # return code_str
  ret_code = None
  if language == "js":
    if True:# (code_str.find("function test()") < 0 or code_str.find("\\x") < 0):
      ret_code = jsbeautifier.beautify(code_str)
    else:
      if d_consts.DEBUG_VERBOSE > 0: print("# beautify WARNING: unsupported javascript code.")
      ret_code = code_str
  else:
    if d_consts.DEBUG_VERBOSE > 0: print("# beautify WARNING: unsupported language " + language)
    ret_code = code_str
  mapping_list = d_utils.get_string_mapping_a(code_str, ret_code)
  return ret_code, mapping_list
