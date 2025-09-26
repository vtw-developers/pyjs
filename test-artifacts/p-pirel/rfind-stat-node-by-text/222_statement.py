for i in range(1, N + 1):
    myexactlog(6, 0)
    if i % 2 == 0:
        myexactlog(7, 2)
        dp[i] = min(dp[i - 1] + insrt, dp[i // 2] + cpy)
        myexactlog(8, dp)
    else:
        myexactlog(9, 0)
        pass
    break