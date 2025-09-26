while a < m and b < n:
    myexactlog(6, 0)
    if abs(A[a] - B[b]) < result:
        myexactlog(7, 0)
        result = abs(A[a] - B[b])
        myexactlog(8, result)
    if A[a] < B[b]:
        myexactlog(9, 1)
        a += 1
        myexactlog(10, a)
    else:
        myexactlog(11, 0)
        pass
    break