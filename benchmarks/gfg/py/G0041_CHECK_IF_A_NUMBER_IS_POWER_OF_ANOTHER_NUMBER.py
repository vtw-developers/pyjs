def test():
  "--- test function ---"
  param =[(57, 1,),(3, 9,),(10, 101,),(10, 10000,),(6, 46656,),(2, 2048,),(1, 40,),(20, 79,),(96, 98,),(25, 5,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(x, y):
    if x == 1:
        retval_0 = y == 1
        return retval_0
    pow = 1
    while pow < y:
        pow = pow * x
    retval_1 = pow == y
    return retval_1
"-----------------"
test()
