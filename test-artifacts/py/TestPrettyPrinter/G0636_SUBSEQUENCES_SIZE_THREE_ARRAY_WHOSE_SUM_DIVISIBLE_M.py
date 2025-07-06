def f_gold(A, N, M):
    sum = 0
    ans = 0
    for i in range(0, N):
        for j in range(i + 1, N):
            for k in range(j + 1, N):
                sum = A[i] + A[j] + A[k]
                if sum % M == 0:
                    ans = ans + 1
    return ans