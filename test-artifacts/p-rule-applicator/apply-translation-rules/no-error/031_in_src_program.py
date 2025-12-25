def test():
  "--- test function ---"
  param = [('', 0, -1), ('x', 0, 0), ('1101010101111110', 0, 15)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(str_0, l, h):
    import sys
"-----------------"
test()