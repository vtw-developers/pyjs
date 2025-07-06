def test():
  "--- test function ---"
  param =[(96,),(85,),(54,),(14,),(47,),(11,),(49,),(99,),(28,),(82,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    if n == 0 or n == 9:
        retval_0 = True
        return retval_0
    if n < 9:
        retval_1 = False
        return retval_1
    retval_2 = f_gold((int)(n >> 3) - (int)(n & 7))
    return retval_2
"-----------------"
test()
