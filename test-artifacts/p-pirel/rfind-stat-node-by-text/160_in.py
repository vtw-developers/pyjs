def f_gold(arr, n):
    dp = [0] * n
    myexactlog(1, dp)
    if n == 1:
        myexactlog(2, 0)
        retval_1 = arr[0]
        myexactlog(3, retval_1)
        myexactlog(4, retval_1)
        return retval_1
    if n == 2:
        myexactlog(5, 1)
        retval_2 = min(arr[0], arr[1])
        myexactlog(6, retval_2)
        myexactlog(7, retval_2)
        return retval_2
    if n == 3:
        myexactlog(8, 2)
        retval_3 = min(arr[0], min(arr[1], arr[2]))
        myexactlog(9, retval_3)
        myexactlog(10, retval_3)
        return retval_3
    if n == 4:
        myexactlog(11, 3)
        retval_4 = min(min(arr[0], arr[1]), min(arr[2], arr[3]))
        myexactlog(12, retval_4)
        myexactlog(13, retval_4)
        return retval_4
    dp[0] = arr[0]
    myexactlog(14, dp)
    dp[1] = arr[1]
    myexactlog(15, dp)
    dp[2] = arr[2]
    myexactlog(16, dp)
    dp[3] = arr[3]
    myexactlog(17, dp)
    for i in range(4, n):
        myexactlog(18, 0)
        dp[i] = arr[i] + min(min(dp[i - 1], dp[i - 2]), min(dp[i - 3], dp[i - 4]))