def f_gold(n, k, x):
    dp = list()
    myexactlog(1, dp)
    dp.append(0)
    myexactlog(2, dp)
    dp.append(1)
    myexactlog(3, dp)
    i = 2
    myexactlog(4, i)
    while i < n:
        myexactlog(5, 0)
        dp.append((k - 2) * dp[i - 1] + (k - 1) * dp[i - 2])
        myexactlog(6, dp)
        i = i + 1
        myexactlog(7, i)