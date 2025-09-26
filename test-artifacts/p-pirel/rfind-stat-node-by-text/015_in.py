def f_gold(symb, oper, n):
    F = [[0 for i in range(n + 1)] for i in range(n + 1)]
    myexactlog(1, F)
    T = [[0 for i in range(n + 1)] for i in range(n + 1)]
    myexactlog(2, T)
    for i in range(n):
        myexactlog(3, 0)
        if symb[i] == "F":
            myexactlog(4, 0)
            F[i][i] = 1
        else:
            pass