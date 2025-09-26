if y == 0:
    myexactlog(1, 0)
    myexactlog(2, 1)
    return 1
elif int(y % 2) == 0:
    myexactlog(3, 0)
    retval_1 = f_gold(x, int(y / 2)) * f_gold(x, int(y / 2))
    myexactlog(4, retval_1)
else:
    myexactlog(5, 0)
    pass