def test():
  "--- test function ---"
  param =[(37,),(39,),(73,),(8,),(28,),(66,),(20,),(36,),(6,),(51,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    if n <= 1:
        retval_0 = False
        return retval_0
    for i in range(2, n):
        if n % i == 0:
            retval_1 = False
            return retval_1
    retval_2 = True
    return retval_2
"-----------------"
test()
