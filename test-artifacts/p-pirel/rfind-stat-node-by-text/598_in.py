def f_gold(cost, N):
    dp = [[0 for i in range(N + 1)] for j in range(N + 1)]
    myexactlog(1, dp)
    dp[0][0] = cost[0][0]
    myexactlog(2, dp)
    for i in range(1, N):
        myexactlog(3, 0)
        pass
        break