def f_gold(n):
    DP = [0 for i in range(0, n + 1)]
    DP[0] = DP[1] = DP[2] = 1
    DP[3] = 2
    for i in range(4, n + 1):
        DP[i] = DP[i - 1] + DP[i - 3] + DP[i - 4]
    return DP[n]