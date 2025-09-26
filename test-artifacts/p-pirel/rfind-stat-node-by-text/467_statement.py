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
        b[i - 1] = 0
        myexactlog(17, b)
    if a[i] == x:
        myexactlog(18, 4)
        continue
    y = a[i] + b[i]
    myexactlog(19, y)
    if i + 1 < n:
        myexactlog(20, 5)
        pass
    break