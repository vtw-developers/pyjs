def test():
  "--- test function ---"
  param =[(1,),(2,),(4,),(5,),(6,),(7,),(3,),(8,),(9,),(10,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    retval_1 = (n * (n + 1) / 2) * (1 << (n - 1))
    return retval_1
"-----------------"
test()
