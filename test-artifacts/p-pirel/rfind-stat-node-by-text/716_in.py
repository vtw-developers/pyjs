def f_gold(n, a, b, c):
    dp = [-1] * (n + 10)
    myexactlog(1, dp)
    dp[0] = 0
    myexactlog(2, dp)
    for i in range(0, n):
        myexactlog(3, 0)
        if dp[i] != -1:
            myexactlog(4, 1)
            if i + a <= n:
                myexactlog(5, 0)
                pass
        break