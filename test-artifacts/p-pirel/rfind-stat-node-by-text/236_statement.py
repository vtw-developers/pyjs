if res > n / 2:
    myexactlog(17, 2)
    retval_1 = n // 2
    myexactlog(18, retval_1)
    myexactlog(19, retval_1)
    return retval_1
else:
    myexactlog(20, 2)
    myexactlog(21, res)
    return res