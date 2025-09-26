def f_gold(n):
    if n < 10:
        myexactlog(1, 0)
        retval_1 = n * (n + 1) / 2
        myexactlog(2, retval_1)
        myexactlog(3, retval_1)
        return retval_1
    d = int(math.log10(n))
    myexactlog(4, d)
    a = [0] * (d + 1)
    myexactlog(5, a)
    a[0] = 0
    myexactlog(6, a)
    a[1] = 45
    myexactlog(7, a)
    for i in range(2, d + 1):
        myexactlog(8, 0)
        a[i] = a[i - 1] * 10 + 45 * int(math.ceil(math.pow(10, i - 1)))
        myexactlog(9, a)
        break