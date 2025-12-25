def test():
  "--- test function ---"
  param =[(85,),(86,),(3,),(35,),(59,),(38,),(33,),(15,),(75,),(74,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    if n < 3:
        myexactlog(1, 0)
        myexactlog(2, n)
        return n
    elif n >= 3 and n < 10:
        myexactlog(3, 0)
        myexactlog(4, n - 1)
        return n - 1
    po = 1
    myexactlog(5, po)
    while n // po > 9:
        myexactlog(6, 0)
        po = po * 10
        myexactlog(7, po)
    msd = n // po
    myexactlog(8, msd)
    if msd != 3:
        myexactlog(9, 1)
        myexactlog(10, f_gold(msd) * f_gold(po - 1) + f_gold(msd) + f_gold(n % po))
        return f_gold(msd) * f_gold(po - 1) + f_gold(msd) + f_gold(n % po)
    else:
        myexactlog(11, 0)
        myexactlog(12, f_gold(msd * po - 1))
        return f_gold(msd * po - 1)
"-----------------"
test()