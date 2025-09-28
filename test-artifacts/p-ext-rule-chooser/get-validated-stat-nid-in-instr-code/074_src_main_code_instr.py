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
        myexactlog(5, 1)
        for j in range(len(s2) + 1):
            myexactlog(6, 0)
            if dp[i][j]:
                myexactlog(7, 2)
                if j < len(s2) and (s1[i].upper() == s2[j]):
                    myexactlog(8, 0)
                    dp[i + 1][j + 1] = True
                    myexactlog(9, dp)
                if s1[i].isupper() == False:
                    myexactlog(10, 1)
                    pass
            break
        break