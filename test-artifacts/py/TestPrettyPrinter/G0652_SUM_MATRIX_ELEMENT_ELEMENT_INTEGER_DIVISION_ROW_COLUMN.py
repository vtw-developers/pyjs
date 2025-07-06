def f_gold(N):
    ans = 0
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            ans += i // j
    return ans