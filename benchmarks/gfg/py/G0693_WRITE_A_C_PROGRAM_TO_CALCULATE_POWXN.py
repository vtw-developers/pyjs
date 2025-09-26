def test():
  "--- test function ---"
  param =[(2, 11,),(3, 10,),(4, 9,),(5, 8,),(6, 7,),(7, 6,),(8, 5,),(9, 4,),(10, 3,),(11, 2,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(x, y):
    if y == 0:
        return 1
    elif int(y % 2) == 0:
        retval_1 = f_gold(x, int(y / 2)) * f_gold(x, int(y / 2))
        return retval_1
    else:
        retval_2 = x * f_gold(x, int(y / 2)) * f_gold(x, int(y / 2))
        return retval_2
"-----------------"
test()
