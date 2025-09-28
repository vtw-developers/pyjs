def f_gold(x, y, n):
    dp = [0 for i in range(n + 1)]
    myexactlog(1, dp)
    dp[0] = False
    myexactlog(2, dp)
    dp[1] = True
    myexactlog(3, dp)
    for i in range(2, n + 1):
        myexactlog(4, 0)
        pass
        break