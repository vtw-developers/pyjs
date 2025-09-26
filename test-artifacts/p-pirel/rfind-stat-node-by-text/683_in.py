def f_gold(n):
    dp = [[0 for i in range(n + 1)] for i in range(10)]
    myexactlog(1, dp)
    for i in range(10):
        myexactlog(2, 0)
        dp[i][1] = 1
        myexactlog(3, dp)
        break
    for digit in range(10):
        myexactlog(4, 2)
        for len_0 in range(2, n + 1):
            myexactlog(5, 1)
            pass
            break
        break