while a < m and b < n:
    myexactlog(6, 0)
    if abs(A[a] - B[b]) < result:
        myexactlog(7, 0)
        result = abs(A[a] - B[b])
        myexactlog(8, result)
    if A[a] < B[b]:
        myexactlog(9, 1)
        pass
    else:
        myexactlog(10, 0)
        pass
    break