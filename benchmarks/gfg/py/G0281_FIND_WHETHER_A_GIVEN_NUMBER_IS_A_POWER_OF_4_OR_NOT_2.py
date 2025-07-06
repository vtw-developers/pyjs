def test():
  "--- test function ---"
  param =[(1,),(4,),(64,),(- 64,),(128,),(1024,),(97,),(86,),(14,),(99,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    retval_0 = n != 0 and ((n & (n - 1)) == 0) and not (n & 0xAAAAAAAA)
    return retval_0
"-----------------"
test()
