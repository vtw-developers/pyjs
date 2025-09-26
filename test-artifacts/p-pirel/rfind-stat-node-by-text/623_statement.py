for j in range(i + 1, n):
    myexactlog(12, 2)
    dp[i] = max(dp[i], (pre_sum[j] - pre_sum[i]) / (j - i) + dp[j])
    myexactlog(13, dp)
    break