def f_gold(n, a, b, c):
    dp = [-1] * (n + 10)
    dp[0] = 0
    for i in range(0, n):
        if dp[i] != -1:
            if i + a <= n:
                dp[i + a] = max(dp[i] + 1, dp[i + a])