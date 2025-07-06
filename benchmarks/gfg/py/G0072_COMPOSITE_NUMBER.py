def test():
  "--- test function ---"
  param =[(62,),(13,),(29,),(72,),(30,),(20,),(10,),(47,),(91,),(52,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    if n <= 1:
        retval_0 = False
        return retval_0
    if n <= 3:
        retval_1 = False
        return retval_1
    if n % 2 == 0 or n % 3 == 0:
        retval_2 = True
        return retval_2
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            retval_3 = True
            return retval_3
        i = i + 6
    retval_4 = False
    return retval_4
"-----------------"
test()
