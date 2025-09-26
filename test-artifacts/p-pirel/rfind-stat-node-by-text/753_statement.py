while ((a | b) & 1) == 0:
    myexactlog(6, 0)
    a = a >> 1
    myexactlog(7, a)
    b = b >> 1
    myexactlog(8, b)
    k = k + 1
    myexactlog(9, k)
    break