def test():
  "--- test function ---"
  param =[(2, 11,),(3, 10,),(4, 9,),(5, 8,),(6, 7,),(7, 6,),(8, 5,),(9, 4,),(10, 3,),(11, 2,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(k, n):
    f1 = 0
    f2 = 1
    f3 = f1 + f2
    i = 2
    while f3 % k != 0:
        f1 = f2
        f2 = f3
        f3 = f1 + f2
        i += 1
    retval_1 = n * i
    return retval_1
"-----------------"
test()
