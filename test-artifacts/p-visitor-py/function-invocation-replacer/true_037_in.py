def f_gold(dp, a, low, high, turn):
    if low == high:
        return a[low] * turn
    if dp[low][high] != 0:
        return dp[low][high]
    dp[low][high] = max(a[low] * turn + f_gold(dp, a, low + 1, high, turn + 1), a[high] * turn + f_gold(dp, a, low, high - 1, turn + 1))
    return dp[low][high]