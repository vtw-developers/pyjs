def test():
  "--- test function ---"
  param =[(15,),(90,),(38,),(65,),(91,),(16,),(48,),(74,),(14,),(47,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    if n <= 1:
        retval_0 = False
        return retval_0
    if n <= 3:
        retval_1 = True
        return retval_1
    if n % 2 == 0 or n % 3 == 0:
        retval_2 = False
        return retval_2
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            retval_3 = False
            return retval_3
        i = i + 6
    retval_4 = True
    return retval_4
"-----------------"
test()
