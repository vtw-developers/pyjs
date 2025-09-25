def f_gold(X, Y, l, r, k, dp):
    if k == 0:
        return 0
    if l < 0 or r < 0:
        return 1000000000
    if dp[l][r][k] != -1:
        retval_1 = dp[l][r][k]
        return retval_1
    cost = (ord(X[l]) - ord("a")) ^ (ord(Y[r]) - ord("a"))
    dp[l][r][k] = min([cost + True, True, True])
    retval_2 = dp[l][r][k]
    return retval_2