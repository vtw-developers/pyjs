def test():
  "--- test function ---"
  param =[(85,),(86,),(3,),(35,),(59,),(38,),(33,),(15,),(75,),(74,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    if n < 3:
        return n
    elif n >= 3 and n < 10:
        retval_0 = n - 1
        return retval_0
    po = 1
    while n / po > 9:
        po = po * 10
    msd = n / po
    if msd != 3:
        retval_1 = f_gold(msd) * f_gold(po - 1) + f_gold(msd) + f_gold(n % po)
        return retval_1
    else:
        retval_2 = f_gold(msd * po - 1)
        return retval_2
"-----------------"
test()
