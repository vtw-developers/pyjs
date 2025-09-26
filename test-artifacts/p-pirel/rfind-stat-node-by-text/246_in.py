def f_gold(k, n):
    f1 = 0
    myexactlog(1, f1)
    f2 = 1
    myexactlog(2, f2)
    f3 = f1 + f2
    myexactlog(3, f3)
    i = 2
    myexactlog(4, i)
    while f3 % k != 0:
        myexactlog(5, 0)
        f1 = f2
        myexactlog(6, f1)
        f2 = f3
        myexactlog(7, f2)
        f3 = f1 + f2
        myexactlog(8, f3)
        i += 1
        myexactlog(9, i)
        break