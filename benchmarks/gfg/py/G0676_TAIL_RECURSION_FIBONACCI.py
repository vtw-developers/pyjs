def test():
  "--- test function ---"
  param =[(4, 43, 24,),(3, 48, 98,),(4, 21, 69,),(4, 79, 38,),(4, 38, 30,),(4, 26, 12,),(4, 10, 17,),(4, 37, 26,),(4, 91, 99,),(4, 3, 64,),(0,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n, a=0, b=1):
    if n == 0:
        return a
    if n == 1:
        return b
    retval_1 = f_gold(n - 1, b, a + b)
    return retval_1
"-----------------"
test()
