def f_gold(A, K):
    n = len(A)
    myexactlog(1, n)
    pre_sum = [0] * (n + 1)
    myexactlog(2, pre_sum)
    pre_sum[0] = 0
    myexactlog(3, pre_sum)
    for i in range(n):
        myexactlog(4, 0)
        pre_sum[i + 1] = pre_sum[i] + A[i]
        myexactlog(5, pre_sum)
        break
    dp = [0] * n
    myexactlog(6, dp)
    sum_0 = 0
    myexactlog(7, sum_0)
    for i in range(n):
        myexactlog(8, 1)
        dp[i] = (pre_sum[n] - pre_sum[i]) / (n - i)
        myexactlog(9, dp)
        break
    for k in range(K - 1):
        myexactlog(10, 4)
        for i in range(n):
            myexactlog(11, 3)
            for j in range(i + 1, n):
                myexactlog(12, 2)
                dp[i] = max(dp[i], (pre_sum[j] - pre_sum[i]) / (j - i) + dp[j])
                myexactlog(13, dp)
                break