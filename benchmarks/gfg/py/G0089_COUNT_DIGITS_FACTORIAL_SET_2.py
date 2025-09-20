def test():
  "--- test function ---"
  param =[(56,),(92,),(52,),(96,),(96,),(63,),(51,),(79,),(70,),(9,),(-4,),(1,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
import math
def f_gold(n):
    if n < 0:
        return 0
    if n <= 1:
        return 1
    x = n * math.log10(n / math.e) + math.log10(2 * math.pi * n) / 2.0
    retval_1 = math.floor(x) + 1
    return retval_1
"-----------------"
test()
