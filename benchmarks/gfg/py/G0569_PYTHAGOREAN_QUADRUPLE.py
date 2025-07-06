def test():
  "--- test function ---"
  param =[(1, 1, 1, 3,),(3, 2, 5, 38,),(0, 0, 0, 0,),(- 1, - 1, - 1, 1,),(82, 79, 6, 59,),(14, 57, 35, 29,),(6, 96, 45, 75,),(13, 7, 3, 63,),(96, 65, 72, 93,),(70, 33, 6, 2,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(a, b, c, d):
    sum = a * a + b * b + c * c
    if d * d == sum:
        retval_0 = True
        return retval_0
    else:
        retval_1 = False
        return retval_1
"-----------------"
test()
