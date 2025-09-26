for i in range(2, n + 1):
    myexactlog(4, 0)
    dp[0][i] = dp[0][i - 1] + dp[1][i - 1]
    myexactlog(5, dp)
    dp[1][i] = dp[0][i - 1] * 2 + dp[1][i - 1]
    myexactlog(6, dp)
    break