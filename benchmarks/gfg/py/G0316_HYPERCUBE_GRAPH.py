def test():
  "--- test function ---"
  param =[(2,),(3,),(4,),(5,),(6,),(7,),(8,),(9,),(10,),(11,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    if n == 1:
        return 2
    retval_1 = 2 * f_gold(n - 1)
    return retval_1
"-----------------"
test()
