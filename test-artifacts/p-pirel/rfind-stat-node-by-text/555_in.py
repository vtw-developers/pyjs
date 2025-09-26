def f_gold(n):
    BT = [0] * (n + 1)
    myexactlog(1, BT)
    BT[0] = BT[1] = 1
    myexactlog(2, BT)
    for i in range(2, n + 1):
        myexactlog(3, 1)
        for j in range(i):
            myexactlog(4, 0)
            pass
            break