def f_gold(n, index, modulo, M, arr, dp):
    modulo = ((modulo % M) + M) % M
    if index == n:
        if modulo == 0:
            return 1
        return 0
    if modulo in dp[index]:
        retval_1 = dp[index][modulo]
        return retval_1
    placeAdd = f_gold(n, index + 1, modulo + arr[index], M, arr, dp)
    placeMinus = f_gold(n, index + 1, modulo - arr[index], M, arr, dp)
    res = bool(placeAdd or placeMinus)
    dp[index][modulo] = res
    return res