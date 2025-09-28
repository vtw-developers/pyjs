def f_gold(n, index, Sum, M, arr, dp):
    if index == n:
        myexactlog(1, 1)
        if (Sum % M) == 0:
            myexactlog(2, 0)
            pass