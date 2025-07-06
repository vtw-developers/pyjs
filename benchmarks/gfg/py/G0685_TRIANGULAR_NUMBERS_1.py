def test():
  "--- test function ---"
  param =[(1,),(3,),(6,),(10,),(55,),(48,),(63,),(72,),(16,),(85,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
import math
def f_gold(num):
    if num < 0:
        retval_0 = False
        return retval_0
    c = -2 * num
    b, a = 1, 1
    d = (b * b) - (4 * a * c)
    if d < 0:
        retval_1 = False
        return retval_1
    root1 = (-b + math.sqrt(d)) / (2 * a)
    root2 = (-b - math.sqrt(d)) / (2 * a)
    if root1 > 0 and math.floor(root1) == root1:
        retval_2 = True
        return retval_2
    if root2 > 0 and math.floor(root2) == root2:
        retval_3 = True
        return retval_3
    retval_4 = False
    return retval_4
"-----------------"
test()
