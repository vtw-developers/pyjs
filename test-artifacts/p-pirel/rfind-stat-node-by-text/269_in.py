def f_gold(m, n):
    T = [[0 for i in range(n + 1)] for i in range(m + 1)]
    myexactlog(1, T)
    for i in range(m + 1):
        myexactlog(2, 1)
        for j in range(n + 1):
            myexactlog(3, 0)
            if i == 0 or j == 0:
                myexactlog(4, 0)
                pass
            elif i < j:
                myexactlog(5, 0)
                pass
            elif j == 1:
                myexactlog(6, 1)
                pass
            else:
                myexactlog(7, 0)
                pass