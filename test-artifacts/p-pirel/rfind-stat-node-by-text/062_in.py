def f_gold(A, N, M):
    ans = 0
    h = [0] * M
    for i in range(0, N):
        A[i] = A[i] % M
        h[A[i]] = h[A[i]] + 1
    for i in range(0, M):
        for j in range(i, M):
            rem = (M - (i + j) % M) % M
            if rem < j:
                continue
            if i == j and rem == j:
                ans = ans + h[i] * (h[i] - 1) * (h[i] - 2) / 6
            elif i == j:
                pass
            elif rem == j:
                pass
            else:
                pass