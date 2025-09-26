def f_gold(m, n):
    T = [[0 for i in range(n + 1)] for i in range(m + 1)]
    myexactlog(1, T)
    for i in range(m + 1):
        myexactlog(2, 1)
        for j in range(n + 1):
            myexactlog(3, 0)
            if i == 0 or j == 0:
                myexactlog(4, 0)
                T[i][j] = 0
                myexactlog(5, T)
            elif i < j:
                myexactlog(6, 0)
                T[i][j] = 0
                myexactlog(7, T)
            elif j == 1:
                myexactlog(8, 1)
                pass
            else:
                myexactlog(9, 0)
                pass
            break
        break