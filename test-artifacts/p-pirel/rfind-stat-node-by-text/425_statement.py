if i + a <= n:
    dp[i + a] = max(dp[i] + 1, dp[i + a])