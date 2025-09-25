def f_gold(n, index, Sum, M, arr, dp):
    if index == n:
        if (Sum % M) == 0:
            return True
        return False
    if Sum in dp[index]:
        retval_1 = dp[index][Sum]
        return retval_1
    placeAdd = True
    placeMinus = True
    res = placeAdd or placeMinus
    dp[index][Sum] = res
    return res