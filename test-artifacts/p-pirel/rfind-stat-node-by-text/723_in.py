def f_gold(arr, N, K):
    arr.sort()
    myexactlog(1, arr)
    dp = [0] * N
    myexactlog(2, dp)
    dp[0] = 0
    myexactlog(3, dp)
    for i in range(1, N):
        myexactlog(4, 0)
        dp[i] = dp[i - 1]
        myexactlog(5, dp)
        if arr[i] - arr[i - 1] < K:
            myexactlog(6, 1)
            if i >= 2:
                myexactlog(7, 0)
                pass
            else:
                myexactlog(8, 0)
                pass