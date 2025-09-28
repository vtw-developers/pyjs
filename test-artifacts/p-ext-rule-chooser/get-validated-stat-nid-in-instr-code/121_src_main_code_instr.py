def f_gold(n, index, Sum, M, arr, dp):
    if index == n:
        myexactlog(1, 1)
        if (Sum % M) == 0:
            myexactlog(2, 0)
            myexactlog(3, True)
            return True
        myexactlog(4, False)
        return False
    if Sum in dp[index]:
        myexactlog(5, 2)
        retval_1 = dp[index][Sum]
        myexactlog(6, retval_1)
        myexactlog(7, retval_1)
        return retval_1
    placeAdd = f_gold(n, index + 1, Sum + arr[index], M, arr, dp)
    myexactlog(8, placeAdd)
    placeMinus = f_gold(n, index + 1, Sum - arr[index], M, arr, dp)
    myexactlog(9, placeMinus)
    res = placeAdd or placeMinus
    myexactlog(10, res)
    dp[index][Sum] = res
    myexactlog(11, dp)
    myexactlog(12, res)
    return res