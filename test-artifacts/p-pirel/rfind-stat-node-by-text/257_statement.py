for k in range(K - 1):
    myexactlog(10, 4)
    for i in range(n):
        myexactlog(11, 3)
        for j in range(i + 1, n):
            myexactlog(12, 2)
            dp[i] = max(dp[i], (pre_sum[j] - pre_sum[i]) / (j - i) + dp[j])
            myexactlog(13, dp)
            break
        break
    break