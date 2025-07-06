def f_gold(n):
    dp = [[0 for j in range(27)] for i in range(n + 1)]
    for i in range(0, 26):
        dp[1][i] = 1
    for i in range(2, n + 1):
        for j in range(0, 26):
            if j == 0:
                dp[i][j] = dp[i - 1][j + 1]
            else:
                dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j + 1]
    sum = 0
    for i in range(0, 26):
        sum = sum + dp[n][i]
    return sum