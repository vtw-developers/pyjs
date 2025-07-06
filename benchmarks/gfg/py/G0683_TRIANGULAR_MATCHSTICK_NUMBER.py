def test():
  "--- test function ---"
  param =[(6,),(25,),(15,),(30,),(17,),(80,),(27,),(13,),(12,),(67,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(x):
    retval_0 = (3 * x * (x + 1)) / 2
    return retval_0
"-----------------"
test()
