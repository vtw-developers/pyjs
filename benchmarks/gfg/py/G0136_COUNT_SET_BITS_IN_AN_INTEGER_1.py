def test():
  "--- test function ---"
  param =[(43,),(94,),(72,),(86,),(42,),(33,),(8,),(74,),(29,),(34,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    if n == 0:
        retval_0 = 0
        return retval_0
    else:
        retval_1 = (n & 1) + f_gold(n >> 1)
        return retval_1
"-----------------"
test()
