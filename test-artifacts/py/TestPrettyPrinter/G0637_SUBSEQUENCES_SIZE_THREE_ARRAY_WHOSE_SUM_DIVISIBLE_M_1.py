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
                ans = ans + (h[i] * (h[i] - 1) * h[rem] / 2)
            elif i == rem:
                ans = ans + h[i] * (h[i] - 1) * h[j] / 2
            elif rem == j:
                ans = ans + h[j] * (h[j] - 1) * h[i] / 2
            else:
                ans = ans + h[i] * h[j] * h[rem]
        return ans