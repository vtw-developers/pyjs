def f_gold(n):
    dp = [[0] * (n + 1) for i in range(2)]
    myexactlog(1, dp)
    dp[0][1] = 1
    myexactlog(2, dp)
    dp[1][1] = 2
    myexactlog(3, dp)
    for i in range(2, n + 1):
        myexactlog(4, 0)
        dp[0][i] = dp[0][i - 1] + dp[1][i - 1]
        myexactlog(5, dp)
        dp[1][i] = dp[0][i - 1] * 2 + dp[1][i - 1]
        myexactlog(6, dp)
        break