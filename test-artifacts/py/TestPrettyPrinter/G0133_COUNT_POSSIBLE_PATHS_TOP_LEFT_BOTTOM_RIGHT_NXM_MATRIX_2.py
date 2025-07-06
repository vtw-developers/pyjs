def f_gold(p, q):
    dp = [1 for i in range(q)]
    for i in range(p - 1):
        for j in range(1, q):
            dp[j] += dp[j - 1]
    return dp[q - 1]