def f_gold(S, T):
    m = len(T)
    myexactlog(1, m)
    n = len(S)
    myexactlog(2, n)
    if m > n:
        myexactlog(3, 0)
        myexactlog(4, 0)
        return 0
    mat = [[0 for _ in range(n + 1)] for __ in range(m + 1)]
    myexactlog(5, mat)
    for i in range(1, m + 1):
        myexactlog(6, 0)
        mat[i][0] = 0
        myexactlog(7, mat)
        break
    for j in range(n + 1):
        myexactlog(8, 1)
        mat[0][j] = 1
        myexactlog(9, mat)
        break
    for i in range(1, m + 1):
        myexactlog(10, 3)
        for j in range(1, n + 1):
            myexactlog(11, 2)
            if T[i - 1] != S[j - 1]:
                myexactlog(12, 1)
                pass
            else:
                myexactlog(13, 0)
                pass
            break
        break