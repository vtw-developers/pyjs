def f_gold(N):
    length = len(N)
    myexactlog(1, length)
    l = int((length) / 2)
    myexactlog(2, l)
    count = 0
    myexactlog(3, count)
    for i in range(l + 1):
        myexactlog(4, 0)
        s = N[0:0 + i]
        myexactlog(5, s)
        l1 = len(s)
        myexactlog(6, l1)
        break