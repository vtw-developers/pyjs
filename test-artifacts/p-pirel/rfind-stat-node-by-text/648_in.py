def f_gold(a, n):
    if n == 1:
        myexactlog(1, 0)
        retval_1 = a[0]
        myexactlog(2, retval_1)
        myexactlog(3, retval_1)
        return retval_1
    max_neg = -999999999999
    myexactlog(4, max_neg)
    count_neg = 0
    myexactlog(5, count_neg)
    count_zero = 0
    myexactlog(6, count_zero)
    prod = 1
    myexactlog(7, prod)
    for i in range(n):
        myexactlog(8, 0)
        if a[i] == 0:
            myexactlog(9, 1)
            pass
        break