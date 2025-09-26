def f_gold(cost, N):
    dp = [[0 for i in range(N + 1)] for j in range(N + 1)]
    myexactlog(1, dp)
    dp[0][0] = cost[0][0]
    myexactlog(2, dp)
    for i in range(1, N):
        myexactlog(3, 0)
        dp[i][0] = dp[i - 1][0] + cost[i][0]
        myexactlog(4, dp)
        break
    for j in range(1, N):
        myexactlog(5, 1)
        dp[0][j] = dp[0][j - 1] + cost[0][j]
        myexactlog(6, dp)
        break
    for i in range(1, N):
        myexactlog(7, 3)
        for j in range(1, N):
            myexactlog(8, 2)
            pass
            break
        break