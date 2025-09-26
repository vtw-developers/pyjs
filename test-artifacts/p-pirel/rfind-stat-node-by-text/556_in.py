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