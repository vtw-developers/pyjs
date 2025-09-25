def f_gold(n, index, Sum, M, arr, dp):
    if index == n:
        if (Sum % M) == 0:
            return True
        return False
    if Sum in dp[index]:
        retval_1 = dp[index][Sum]
        return retval_1
    placeAdd = f_gold(n, index + 1, Sum + arr[index], M, arr, dp)
    placeMinus = f_gold(n, index + 1, Sum - arr[index], M, arr, dp)
    res = placeAdd or placeMinus
    dp[index][Sum] = res
    return res