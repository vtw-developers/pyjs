def f_gold(x, y, n):
    dp = [0 for i in range(n + 1)]
    myexactlog(1, dp)
    dp[0] = False
    myexactlog(2, dp)
    dp[1] = True
    myexactlog(3, dp)
    for i in range(2, n + 1):
        myexactlog(4, 0)
        if i - 1 >= 0 and not dp[i - 1]:
            myexactlog(5, 0)
            pass
        elif i - x >= 0 and not dp[i - x]:
            myexactlog(6, 0)
            pass
        elif i - y >= 0 and not dp[i - y]:
            myexactlog(7, 1)
            pass
        else:
            myexactlog(8, 0)
            pass
        break