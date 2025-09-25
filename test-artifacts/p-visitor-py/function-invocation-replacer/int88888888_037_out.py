def f_gold(dp, a, low, high, turn):
    if low == high:
        return a[low] * turn
    if dp[low][high] != 0:
        return dp[low][high]
    dp[low][high] = max(a[low] * turn + 88888888, a[high] * turn + 88888888)
    return dp[low][high]