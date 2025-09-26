def f_gold(a, b, n):
    s = 0
    myexactlog(1, s)
    for i in range(0, n):
        myexactlog(2, 0)
        s += a[i] + b[i]
        myexactlog(3, s)
        break
    if n == 1:
        myexactlog(4, 0)
        retval_1 = a[0] + b[0]
        myexactlog(5, retval_1)
        myexactlog(6, retval_1)
        return retval_1
    if s % n != 0:
        myexactlog(7, 1)
        retval_2 = -1
        myexactlog(8, retval_2)
        myexactlog(9, retval_2)
        return retval_2
    x = s // n
    myexactlog(10, x)
    for i in range(0, n):
        myexactlog(11, 1)
        if a[i] > x:
            myexactlog(12, 2)
            retval_3 = -1
            myexactlog(13, retval_3)
            myexactlog(14, retval_3)
            return retval_3
        if i > 0:
            myexactlog(15, 3)
            a[i] += b[i - 1]
            myexactlog(16, a)
        break