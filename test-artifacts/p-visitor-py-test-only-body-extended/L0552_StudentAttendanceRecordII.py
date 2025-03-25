mod = int(1000000000.0 + 7)
dp = [[[0, 0, 0], [0, 0, 0]] for _ in range(n)]
dp[0][0][0] = dp[0][0][1] = dp[0][1][0] = 1
for i in range(1, n):
    dp[i][1][0] = (dp[i - 1][0][0] + dp[i - 1][0][1] + dp[i - 1][0][2]) % mod
    dp[i][0][1] = dp[i - 1][0][0]
    dp[i][0][2] = dp[i - 1][0][1]
    dp[i][1][1] = dp[i - 1][1][0]
    dp[i][1][2] = dp[i - 1][1][1]
    dp[i][0][0] = (dp[i - 1][0][0] + dp[i - 1][0][1] + dp[i - 1][0][2]) % mod
    dp[i][1][0] = (dp[i][1][0] + dp[i - 1][1][0] + dp[i - 1][1][1] + dp[i - 1][1][2]) % mod
ans = 0
for j in range(2):
    for k in range(3):
        ans = (ans + dp[n - 1][j][k]) % mod
return ans