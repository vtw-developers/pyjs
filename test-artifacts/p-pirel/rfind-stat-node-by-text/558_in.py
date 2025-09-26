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
        myexactlog(5, 1)
        pass
        break