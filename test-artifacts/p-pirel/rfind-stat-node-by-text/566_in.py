def f_gold(a, n):
    if n == 1:
        myexactlog(1, 0)
        retval_1 = a[0]
        myexactlog(2, retval_1)
        myexactlog(3, retval_1)
        return retval_1
    max_neg = float("-inf")
    myexactlog(4, max_neg)
    min_pos = float("inf")
    myexactlog(5, min_pos)
    count_neg = 0
    myexactlog(6, count_neg)
    count_zero = 0
    myexactlog(7, count_zero)
    prod = 1
    myexactlog(8, prod)
    for i in range(0, n):
        myexactlog(9, 0)
        pass
        break