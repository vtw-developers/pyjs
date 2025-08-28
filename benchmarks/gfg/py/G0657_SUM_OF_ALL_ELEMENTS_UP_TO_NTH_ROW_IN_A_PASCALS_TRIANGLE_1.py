def test():
  "--- test function ---"
  param =[(53,),(3,),(28,),(44,),(84,),(83,),(46,),(3,),(16,),(89,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    sum_0 = 0
    sum_0 = 1 << n
    return sum_0 - 1
"-----------------"
test()
