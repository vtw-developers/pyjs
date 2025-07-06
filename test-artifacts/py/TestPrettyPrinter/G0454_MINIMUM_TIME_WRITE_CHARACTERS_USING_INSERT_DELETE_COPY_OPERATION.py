def f_gold(N, insrt, remov, cpy):
    if N == 0:
        return 0
    if N == 1:
        return insrt
    dp = [0] * (N + 1)
    for i in range(1, N + 1):
        if i % 2 == 0:
            dp[i] = min(dp[i - 1] + insrt, dp[i // 2] + cpy)
        else:
            dp[i] = min(dp[i - 1] + insrt, dp[(i + 1) // 2] + cpy + remov)
    return dp[N]