def f_gold(s1, s2):
    n = len(s1)
    myexactlog(1, n)
    m = len(s2)
    myexactlog(2, m)
    dp = [[False for i in range(m + 1)] for i in range(n + 1)]
    myexactlog(3, dp)
    dp[0][0] = True
    myexactlog(4, dp)
    for i in range(len(s1)):
        myexactlog(5, 0)
        pass
        break