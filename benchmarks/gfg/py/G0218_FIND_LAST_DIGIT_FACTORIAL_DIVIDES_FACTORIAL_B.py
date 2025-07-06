def test():
  "--- test function ---"
  param =[(79, 84,),(61, 29,),(39, 77,),(39, 65,),(61, 78,),(86, 73,),(7, 92,),(86, 50,),(86, 63,),(11, 2,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(A, B):
    variable = 1
    if A == B:
        retval_0 = 1
        return retval_0
    elif (B - A) >= 5:
        retval_1 = 0
        return retval_1
    else:
        for i in range(A + 1, B + 1):
            variable = (variable * (i % 10)) % 10
        retval_2 = variable % 10
        return retval_2
"-----------------"
test()
