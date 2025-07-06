def f_gold(A, K):
    n = len(A)
    pre_sum = [0] * (n + 1)
    pre_sum[0] = 0
    for i in range(n):
        pre_sum[i + 1] = pre_sum[i] + A[i]
    dp = [0] * n
    sum = 0
    for i in range(n):
        dp[i] = (pre_sum[n] - pre_sum[i]) / (n - i)
    for k in range(K - 1):
        for i in range(n):
            for j in range(i + 1, n):
                dp[i] = max(dp[i], (pre_sum[j] - pre_sum[i]) / (j - i) + dp[j])
    return int(dp[0])