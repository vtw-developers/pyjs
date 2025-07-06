import sys
def f_gold(A, B, m, n):
    A.sort()
    B.sort()
    a = 0
    b = 0
    result = sys.maxsize
    while a < m and b < n:
        if abs(A[a] - B[b]) < result:
            result = abs(A[a] - B[b])
        if A[a] < B[b]:
            a += 1
        else:
            b += 1
    return result