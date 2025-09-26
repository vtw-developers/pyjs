def f_gold(A, B, m, n):
    A.sort()
    myexactlog(1, A)
    B.sort()
    myexactlog(2, B)
    a = 0
    myexactlog(3, a)
    b = 0
    myexactlog(4, b)
    result = sys.maxsize
    myexactlog(5, result)
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
            b += 1
            myexactlog(12, b)
        break