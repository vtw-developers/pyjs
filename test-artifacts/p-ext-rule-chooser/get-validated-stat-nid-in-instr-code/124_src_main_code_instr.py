def f_gold(n, index, modulo, M, arr, dp):
    modulo = ((modulo % M) + M) % M
    myexactlog(1, modulo)
    if index == n:
        myexactlog(2, 1)
        if modulo == 0:
            myexactlog(3, 0)
            pass