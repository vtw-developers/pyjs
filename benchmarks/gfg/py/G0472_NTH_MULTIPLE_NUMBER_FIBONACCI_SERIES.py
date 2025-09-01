def test():
  "--- test function ---"
  param =[(50, 60,),(52, 45,),(42, 17,),(2, 68,),(37, 43,),(48, 46,),(31, 4,),(9, 64,),(78, 14,),(64, 80,)]
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
    return n * i
"-----------------"
test()
