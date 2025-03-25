mod = 1000000007
dp, pre = ([0] * (k + 1), [0] * (k + 2))
for i in range(1, n + 1):
    dp[0] = 1
    for j in range(1, k + 1):
        dp[j] = (pre[j + 1] - pre[max(0, j - i + 1)] + mod) % mod
    for j in range(1, k + 2):
        pre[j] = (pre[j - 1] + dp[j - 1]) % mod
return dp[k]