def f_gold(n, a, b, c):
    dp = [-1] * (n + 10)
    myexactlog(1, dp)
    dp[0] = 0
    myexactlog(2, dp)
    for i in range(0, n):
        myexactlog(3, 0)
        if dp[i] != -1:
            myexactlog(4, 3)
            if i + a <= n:
                myexactlog(5, 0)
                dp[i + a] = max(dp[i] + 1, dp[i + a])
                myexactlog(6, dp)
            if i + b <= n:
                myexactlog(7, 1)
                dp[i + b] = max(dp[i] + 1, dp[i + b])
                myexactlog(8, dp)
            if i + c <= n:
                myexactlog(9, 2)
                dp[i + c] = max(dp[i] + 1, dp[i + c])
                myexactlog(10, dp)
        break