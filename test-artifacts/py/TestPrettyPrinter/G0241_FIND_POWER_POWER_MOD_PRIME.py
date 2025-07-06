def f_gold(A, B, C, M):
    res = pow(B, C, M - 1)
    ans = pow(A, res, M)
    return ans