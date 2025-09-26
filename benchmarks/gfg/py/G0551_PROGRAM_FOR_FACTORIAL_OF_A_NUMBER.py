def test():
  "--- test function ---"
  param =[(2,),(3,),(4,),(5,),(6,),(7,),(8,),(9,),(10,),(11,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    retval_1 = 1 if (n == 1 or n == 0) else n * f_gold(n - 1)
    return retval_1
"-----------------"
test()
