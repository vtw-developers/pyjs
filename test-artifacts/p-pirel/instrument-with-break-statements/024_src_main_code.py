def f_gold(s1, s2):
    n = len(s1)
    m = len(s2)
    dp = [[False for i in range(m + 1)] for i in range(n + 1)]
    dp[0][0] = True
    for i in range(len(s1)):
        for j in range(len(s2) + 1):
            if dp[i][j]:
                if j < len(s2) and (s1[i].upper() == s2[j]):
                    dp[i + 1][j + 1] = True
                if s1[i].isupper() == False:
                    dp[i + 1][j] = True
    retval_1 = dp[n][m]
    return retval_1