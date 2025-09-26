def test():
  "--- test function ---"
  param =[(1, 44,),(6, 61,),(75, 20,),(51, 17,),(19, 25,),(82, 98,),(72, 21,),(48, 41,),(12, 17,),(41, 80,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
import math
def f_gold(a, b):
    retval_1 = math.floor((a + b) / 2)
    return retval_1
"-----------------"
test()
