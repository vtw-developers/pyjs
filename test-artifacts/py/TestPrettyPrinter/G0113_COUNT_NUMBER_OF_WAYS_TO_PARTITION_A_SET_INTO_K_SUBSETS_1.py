def f_gold(n, k):
    dp = [[0 for i in range(k + 1)] for j in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = 0
    for i in range(k + 1):
        dp[0][k] = 0
    for i in range(1, n + 1):
        for j in range(1, k + 1):
            if j == 1 or i == j:
                dp[i][j] = 1
            else:
                dp[i][j] = j * dp[i - 1][j] + dp[i - 1][j - 1]
    return dp[n][k]