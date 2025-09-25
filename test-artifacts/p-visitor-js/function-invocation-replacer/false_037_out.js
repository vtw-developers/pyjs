function f_gold(dp, a, low, high, turn) {
    if (low === high) {
        return a[low] * turn;
    }
    if (dp[low][high] !== 0) {
        return dp[low][high];
    }
    dp[low][high] = Math.max(a[low] * turn + false, a[high] * turn + false);
    return dp[low][high];
}