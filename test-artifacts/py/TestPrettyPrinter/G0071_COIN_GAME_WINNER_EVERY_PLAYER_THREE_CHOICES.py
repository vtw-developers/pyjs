def f_gold(x, y, n):
    dp = [0 for i in range(n + 1)]
    dp[0] = False
    dp[1] = True
    for i in range(2, n + 1):
        if i - 1 >= 0 and not dp[i - 1]:
            dp[i] = True
        elif i - x >= 0 and not dp[i - x]:
            dp[i] = True
        elif i - y >= 0 and not dp[i - y]:
            dp[i] = True
        else:
            dp[i] = False
    return dp[n]