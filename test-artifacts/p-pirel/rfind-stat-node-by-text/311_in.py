def f_gold(ar, n):
    res = 0
    myexactlog(1, res)
    ar.sort()
    myexactlog(2, ar)
    for i in range(0, n):
        myexactlog(3, 1)
        count = 1
        myexactlog(4, count)
        for i in range(n - 1):
            myexactlog(5, 0)
            if ar[i] == ar[i + 1]:
                myexactlog(6, 0)
                pass
            else:
                myexactlog(7, 0)
                pass
            break
        break