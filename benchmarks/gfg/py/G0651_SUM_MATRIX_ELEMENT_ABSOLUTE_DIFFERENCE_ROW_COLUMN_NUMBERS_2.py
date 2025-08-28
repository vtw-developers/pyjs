def test():
  "--- test function ---"
  param =[(12,),(89,),(76,),(2,),(81,),(11,),(26,),(35,),(16,),(66,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    n -= 1
    sum_0 = 0
    sum_0 += (n * (n + 1)) / 2
    sum_0 += (n * (n + 1) * (2 * n + 1)) / 6
    return int(sum_0)
"-----------------"
test()
