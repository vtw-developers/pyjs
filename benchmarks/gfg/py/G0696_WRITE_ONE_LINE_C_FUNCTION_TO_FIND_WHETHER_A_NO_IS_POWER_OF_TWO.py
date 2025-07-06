def test():
  "--- test function ---"
  param =[(1,),(2,),(8,),(1024,),(24,),(7,),(46,),(61,),(73,),(66,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    if n == 0:
        retval_0 = False
        return retval_0
    while n != 1:
        if n % 2 != 0:
            retval_1 = False
            return retval_1
        n = n // 2
    retval_2 = True
    return retval_2
"-----------------"
test()
