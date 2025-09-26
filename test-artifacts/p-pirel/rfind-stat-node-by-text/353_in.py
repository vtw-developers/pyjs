def f_gold(str_0):
    n = len(str_0)
    myexactlog(1, n)
    L = [[0 for x in range(n)] for x in range(n)]
    myexactlog(2, L)
    for i in range(n):
        myexactlog(3, 0)
        L[i][i] = 1
        myexactlog(4, L)
        break
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
                L[i][j] = L[i + 1][j - 1] + 2
                myexactlog(11, L)
            else:
                myexactlog(12, 0)
                pass
            break