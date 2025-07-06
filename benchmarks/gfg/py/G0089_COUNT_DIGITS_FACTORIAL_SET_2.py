def test():
  "--- test function ---"
  param =[(56,),(92,),(52,),(96,),(96,),(63,),(51,),(79,),(70,),(9,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
import math
def f_gold(n):
    if n < 0:
        retval_0 = 0
        return retval_0
    if n <= 1:
        retval_1 = 1
        return retval_1
    x = n * math.log10(n / math.e) + math.log10(2 * math.pi * n) / 2.0
    retval_2 = math.floor(x) + 1
    return retval_2
"-----------------"
test()
