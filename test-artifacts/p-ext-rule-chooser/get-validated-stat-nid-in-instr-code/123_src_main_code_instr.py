def f_gold(n, index, modulo, M, arr, dp):
    modulo = ((modulo % M) + M) % M
    myexactlog(1, modulo)
    if index == n:
        myexactlog(2, 0)
        pass