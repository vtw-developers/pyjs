def test():
  "--- test function ---"
  param =[(44,),(9,),(19,),(10,),(78,),(94,),(70,),(81,),(81,),(49,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    myexactlog(1, range(0, n + 1))
"-----------------"
test()