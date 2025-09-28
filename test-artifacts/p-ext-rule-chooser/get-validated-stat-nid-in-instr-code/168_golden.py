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