def test():
  "--- test function ---"
  param =[(76,),(26,),(45,),(35,),(34,),(22,),(3,),(25,),(22,),(78,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    retval_0 = (n * (n + 1) / 2) * (1 << (n - 1))
    return retval_0
"-----------------"
test()
