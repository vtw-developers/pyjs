def f_gold(a, b):
    if a == b:
        myexactlog(1, 0)
        myexactlog(2, a)
        return a
    if a == 0:
        myexactlog(3, 1)
        myexactlog(4, b)
        return b
    if b == 0:
        myexactlog(5, 2)
        myexactlog(6, a)
        return a
    if (~a & 1) == 1:
        myexactlog(7, 4)
        if (b & 1) == 1:
            myexactlog(8, 3)
            retval_1 = f_gold(a >> 1, b)
            myexactlog(9, retval_1)
            myexactlog(10, retval_1)
            return retval_1
        else:
            pass