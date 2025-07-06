def f_gold(A, B, m, n):
    for i in range(n):
        for j in range(m):
            A[i][j] -= B[i][j]
    for i in range(1, n):
        for j in range(1, n):
            if A[i][j] - A[i][0] - A[0][j] + A[0][0] != 0:
                return -1
    result = 0
    for i in range(n):
        result += abs(A[i][0])
    for j in range(m):
        result += abs(A[0][j] - A[0][0])
    return result