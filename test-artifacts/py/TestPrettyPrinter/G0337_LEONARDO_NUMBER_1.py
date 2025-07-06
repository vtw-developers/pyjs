def f_gold(n):
    dp = []
    dp.append(1)
    dp.append(1)
    for i in range(2, n + 1):
        dp.append(dp[i - 1] + dp[i - 2] + 1)
    return dp[n]