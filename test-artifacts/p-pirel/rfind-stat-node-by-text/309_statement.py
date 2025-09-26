for i in range(1, n + 1):
    myexactlog(2, 1)
    for j in range(0, m + 1):
        myexactlog(3, 0)
        if i > j:
            myexactlog(4, 1)
            if j == 0:
                myexactlog(5, 0)
                pass
            else:
                myexactlog(6, 0)
                pass
        break
    break