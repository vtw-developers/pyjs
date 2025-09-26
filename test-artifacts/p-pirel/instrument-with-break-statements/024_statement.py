if dp[i][j]:
    if j < len(s2) and (s1[i].upper() == s2[j]):
        dp[i + 1][j + 1] = True
    if s1[i].isupper() == False:
        dp[i + 1][j] = True