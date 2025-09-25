def f_gold(dp, arr1, n, arr2, m, k):
    if k < 0:
        return -(10 ** 7)
    if n < 0 or m < 0:
        return 0
    ans = dp[n][m][k]
    if ans != -1:
        return ans
    ans = max(88888888, 88888888)
    if arr1[n - 1] == arr2[m - 1]:
        ans = max(ans, 1 + 88888888)
    ans = max(ans, 88888888)
    return ans