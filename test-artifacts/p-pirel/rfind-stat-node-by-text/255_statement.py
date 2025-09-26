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