def f_gold(a, b):
    m = len(a)
    myexactlog(1, m)
    n = len(b)
    myexactlog(2, n)
    lookup = [[0] * (n + 1) for i in range(m + 1)]
    myexactlog(3, lookup)
    for i in range(n + 1):
        myexactlog(4, 0)
        lookup[0][i] = 0
        myexactlog(5, lookup)
        break
    for i in range(m + 1):
        myexactlog(6, 1)
        lookup[i][0] = 1
        myexactlog(7, lookup)
        break
    for i in range(1, m + 1):
        myexactlog(8, 3)
        for j in range(1, n + 1):
            myexactlog(9, 2)
            if a[i - 1] == b[j - 1]:
                myexactlog(10, 0)
                lookup[i][j] = lookup[i - 1][j - 1] + lookup[i - 1][j]
                myexactlog(11, lookup)
            else:
                myexactlog(12, 0)
                lookup[i][j] = lookup[i - 1][j]
                myexactlog(13, lookup)
            break
        break