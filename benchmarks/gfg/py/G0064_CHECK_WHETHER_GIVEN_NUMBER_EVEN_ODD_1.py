def test():
  "--- test function ---"
  param =[(57,),(73,),(79,),(36,),(71,),(23,),(41,),(66,),(46,),(50,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    retval_0 = not (n & 1)
    return retval_0
"-----------------"
test()
