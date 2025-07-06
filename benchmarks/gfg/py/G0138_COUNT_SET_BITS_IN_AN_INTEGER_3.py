def test():
  "--- test function ---"
  param =[(6,),(58,),(90,),(69,),(15,),(54,),(60,),(51,),(46,),(91,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    if n == 0:
        retval_0 = 0
        return retval_0
    else:
        retval_1 = 1 + f_gold(n & (n - 1))
        return retval_1
"-----------------"
test()
