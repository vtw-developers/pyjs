def f_gold(n):
    dp = [0] * (n + 1)
    dp[0] = 0
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = max(dp[int(i / 2)] + dp[int(i / 3)] + dp[int(i / 4)], i)
    return dp[n]