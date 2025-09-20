def test():
  "--- test function ---"
  param =[(46, 92,),(99, 87,),(30, 32,),(1, 86,),(26, 81,),(1, 49,),(27, 46,),(10, 52,),(26, 38,),(29, 80,)]
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
