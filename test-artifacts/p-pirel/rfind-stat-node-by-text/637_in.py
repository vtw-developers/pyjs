def f_gold(n, m):
    dp = [[0 for x in range(m + 1)] for y in range(n + 1)]
    myexactlog(1, dp)
    for i in range(1, n + 1):
        myexactlog(2, 1)
        for j in range(0, m + 1):
            myexactlog(3, 0)
            if i > j:
                myexactlog(4, 0)
                pass
            break