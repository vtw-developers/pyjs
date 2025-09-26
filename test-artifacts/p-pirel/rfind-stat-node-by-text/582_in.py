def f_gold(a, b):
    if a == 0:
        myexactlog(1, 0)
        myexactlog(2, b)
        return b
    if b == 0:
        myexactlog(3, 1)
        myexactlog(4, a)
        return a
    k = 0
    myexactlog(5, k)
    while ((a | b) & 1) == 0:
        myexactlog(6, 0)
        a = a >> 1
        myexactlog(7, a)
        b = b >> 1
        myexactlog(8, b)
        k = k + 1
        myexactlog(9, k)
        break
    while (a & 1) == 0:
        myexactlog(10, 1)
        a = a >> 1
        myexactlog(11, a)
        break
    while b != 0:
        myexactlog(12, 3)
        while (b & 1) == 0:
            myexactlog(13, 2)
            b = b >> 1
            myexactlog(14, b)
            break
        if a > b:
            myexactlog(15, 2)
            temp = a
            myexactlog(16, temp)