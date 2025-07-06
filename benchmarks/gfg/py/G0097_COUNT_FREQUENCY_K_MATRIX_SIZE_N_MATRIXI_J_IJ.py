def test():
  "--- test function ---"
  param =[(90, 74,),(86, 36,),(92, 38,),(72, 71,),(25, 57,),(11, 53,),(94, 80,),(91, 75,),(66, 58,),(34, 88,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n, k):
    if n + 1 >= k:
        retval_0 = k - 1
        return retval_0
    else:
        retval_1 = 2 * n + 1 - k
        return retval_1
"-----------------"
test()
