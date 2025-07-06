def test():
  "--- test function ---"
  param =[(45,),(16,),(15,),(91,),(82,),(18,),(31,),(6,),(93,),(35,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    if n == 0:
        retval_0 = False
        return retval_0
    while n != 1:
        if n % 4 != 0:
            retval_1 = False
            return retval_1
        n = n // 4
    retval_2 = True
    return retval_2
"-----------------"
test()
