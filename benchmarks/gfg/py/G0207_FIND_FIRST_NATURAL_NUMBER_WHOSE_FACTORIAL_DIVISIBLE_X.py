def test():
  "--- test function ---"
  param =[(6,),(4,),(5,),(9,),(7,),(2,),(1,),(3,),(8,),(10,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(x):
    i = 1
    fact = 1
    for i in range(1, x):
        fact = fact * i
        if fact % x == 0:
            break
    return i
"-----------------"
test()
