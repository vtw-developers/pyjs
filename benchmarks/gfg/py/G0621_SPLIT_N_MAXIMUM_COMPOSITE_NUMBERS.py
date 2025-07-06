def test():
  "--- test function ---"
  param =[(55,),(35,),(24,),(75,),(5,),(7,),(50,),(28,),(67,),(59,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    if n < 4:
        retval_0 = -1
        return retval_0
    rem = n % 4
    if rem == 0:
        retval_1 = n // 4
        return retval_1
    if rem == 1:
        if n < 9:
            retval_2 = -1
            return retval_2
        retval_3 = (n - 9) // 4 + 1
        return retval_3
    if rem == 2:
        retval_4 = (n - 6) // 4 + 1
        return retval_4
    if rem == 3:
        if n < 15:
            retval_5 = -1
            return retval_5
        retval_6 = (n - 15) // 4 + 2
        return retval_6
"-----------------"
test()
