def f_gold(N, K):
    ans = 0
    for i in range(1, N + 1):
        ans += i % K
    return ans