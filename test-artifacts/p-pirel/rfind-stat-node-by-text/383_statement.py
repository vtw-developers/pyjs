for cl in range(2, n + 1):
    myexactlog(5, 2)
    for i in range(n - cl + 1):
        myexactlog(6, 1)
        j = i + cl - 1
        myexactlog(7, j)
        if str_0[i] == str_0[j] and cl == 2:
            myexactlog(8, 0)
            L[i][j] = 2
            myexactlog(9, L)
        elif str_0[i] == str_0[j]:
            myexactlog(10, 0)
            pass
        else:
            myexactlog(11, 0)
            pass
        break
    break