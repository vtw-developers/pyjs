def f_gold(N, K):
    ans = 0
    y = N / K
    x = N % K
    ans = (K * (K - 1) / 2) * y + (x * (x + 1)) / 2
    return int(ans)