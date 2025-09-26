def f_gold(n, m):
    count = []
    myexactlog(1, count)
    for i in range(n + 2):
        myexactlog(2, 0)
        count.append(0)
        myexactlog(3, count)
        break
    count[0] = 0
    myexactlog(4, count)
    for i in range(1, n + 1):
        myexactlog(5, 1)
        if i > m:
            myexactlog(6, 0)
            count[i] = count[i - 1] + count[i - m]
        elif i < m:
            pass
        else:
            pass