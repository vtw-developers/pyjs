def f_gold(n, index, modulo, M, arr, dp):
    modulo = ((modulo % M) + M) % M
    myexactlog(1, modulo)
    if index == n:
        myexactlog(2, 1)
        if modulo == 0:
            myexactlog(3, 0)
            myexactlog(4, 1)
            return 1
        myexactlog(5, 0)
        return 0
    if modulo in dp[index]:
        myexactlog(6, 2)
        retval_1 = dp[index][modulo]
        myexactlog(7, retval_1)
        myexactlog(8, retval_1)
        return retval_1
    placeAdd = f_gold(n, index + 1, modulo + arr[index], M, arr, dp)
    myexactlog(9, placeAdd)
    placeMinus = f_gold(n, index + 1, modulo - arr[index], M, arr, dp)
    myexactlog(10, placeMinus)
    res = bool(placeAdd or placeMinus)
    myexactlog(11, res)