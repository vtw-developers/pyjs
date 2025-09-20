def test():
  "--- test function ---"
  param =[(20,),(95,),(39,),(21,),(94,),(79,),(56,),(62,),(23,),(3,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
import math
def f_gold(n):
    fibo = 2.078087 * math.log(n) + 1.672276
    retval_1 = round(fibo)
    return retval_1
"-----------------"
test()
