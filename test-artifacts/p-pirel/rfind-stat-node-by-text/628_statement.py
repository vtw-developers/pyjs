for i in range(4, n):
    myexactlog(18, 0)
    dp[i] = arr[i] + min(min(dp[i - 1], dp[i - 2]), min(dp[i - 3], dp[i - 4]))
    myexactlog(19, dp)
    break