def f_gold(n, k, x):
    dp = list()
    dp.append(0)
    dp.append(1)
    i = 2
    while i < n:
        dp.append((k - 2) * dp[i - 1] + (k - 1) * dp[i - 2])
        i = i + 1
    return (k - 1) * dp[n - 2] if x == 1 else dp[n - 1]