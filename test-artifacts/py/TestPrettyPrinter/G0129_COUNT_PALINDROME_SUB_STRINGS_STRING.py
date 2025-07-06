def f_gold(str, n):
    dp = [[0 for x in range(n)] for y in range(n)]
    P = [[False for x in range(n)] for y in range(n)]
    for i in range(n):
        P[i][i] = True
    for i in range(n - 1):
        if str[i] == str[i + 1]:
            P[i][i + 1] = True
            dp[i][i + 1] = 1
    for gap in range(2, n):
        for i in range(n - gap):
            j = gap + i
            if str[i] == str[j] and P[i + 1][j - 1]:
                P[i][j] = True
            if P[i][j] == True:
                dp[i][j] = dp[i][j - 1] + dp[i + 1][j] + 1 - dp[i + 1][j - 1]
            else:
                dp[i][j] = dp[i][j - 1] + dp[i + 1][j] - dp[i + 1][j - 1]
    return dp[0][n - 1]