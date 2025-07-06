def test():
  "--- test function ---"
  param =[(98,),(9,),(18,),(38,),(84,),(8,),(39,),(6,),(60,),(47,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(a):
    retval_0 = 4 * a
    return retval_0
"-----------------"
test()
