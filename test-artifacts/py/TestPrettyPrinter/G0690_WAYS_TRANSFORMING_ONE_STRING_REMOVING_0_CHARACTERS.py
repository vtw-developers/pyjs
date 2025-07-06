def f_gold(a, b):
    n = len(a)
    m = len(b)
    if m == 0:
        return 1
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(i, n):
            if i == 0:
                if j == 0:
                    if a[j] == b[i]:
                        dp[i][j] = 1
                    else:
                        dp[i][j] = 0
                elif a[j] == b[i]:
                    dp[i][j] = dp[i][j - 1] + 1
                else:
                    dp[i][j] = dp[i][j - 1]
            else:
                if a[j] == b[i]:
                    dp[i][j] = dp[i][j - 1] + dp[i - 1][j - 1]
                else:
                    dp[i][j] = dp[i][j - 1]
    return dp[m - 1][n - 1]