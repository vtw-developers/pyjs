def f_gold(n):
    C = [[0 for x in range(n + 1)] for y in range(n + 1)]
    myexactlog(1, C)
    for i in range(0, n + 1):
        myexactlog(2, 1)
        for j in range(0, min(i, n + 1)):
            myexactlog(3, 0)
            if j == 0 or j == i:
                myexactlog(4, 0)
                C[i][j] = 1
                myexactlog(5, C)
            else:
                myexactlog(6, 0)
                C[i][j] = C[i - 1][j - 1] + C[i - 1][j]
                myexactlog(7, C)
            break
        break
    sum_0 = 0
    myexactlog(8, sum_0)
    for i in range(0, n + 1):
        myexactlog(9, 2)
        pass
        break