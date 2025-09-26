for i in range(n - 1, -1, -1):
    myexactlog(2, 2)
    for j in range(0, n):
        myexactlog(3, 1)
        if i == j:
            myexactlog(4, 0)
            continue
        for k in range(j + 1, n):
            myexactlog(5, 0)
            if i == k:
                myexactlog(6, 1)
                pass
            break
        break
    break