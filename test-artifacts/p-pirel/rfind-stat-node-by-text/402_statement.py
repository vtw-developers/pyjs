while i > 0 and j > 0:
    myexactlog(12, 0)
    if dp[i][j] == dp[i - 1][j - 1] + 1:
        myexactlog(13, 1)
        res += str_0[i - 1]
        myexactlog(14, res)
        i -= 1
        myexactlog(15, i)
        j -= 1
        myexactlog(16, j)
    elif dp[i][j] == dp[i - 1][j] and (dp[i][j] != dp[i][j - 1] or i % 2):
        myexactlog(17, 0)
        i -= 1
        myexactlog(18, i)
    else:
        myexactlog(19, 1)
        j -= 1
        myexactlog(20, j)
    break