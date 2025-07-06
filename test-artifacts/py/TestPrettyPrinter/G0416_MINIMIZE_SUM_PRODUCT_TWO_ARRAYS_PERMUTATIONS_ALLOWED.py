def f_gold(A, B, n):
    sorted(A)
    sorted(B)
    result = 0
    for i in range(n):
        result += A[i] * B[n - i - 1]
    return result