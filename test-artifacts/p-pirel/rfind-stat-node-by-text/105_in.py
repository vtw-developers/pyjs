def f_gold(n):
    A = [0] * (n + 1)
    myexactlog(1, A)
    B = [0] * (n + 1)
    myexactlog(2, B)
    A[0] = 1
    myexactlog(3, A)
    A[1] = 0
    myexactlog(4, A)
    B[0] = 0
    myexactlog(5, B)
    B[1] = 1
    myexactlog(6, B)
    for i in range(2, n + 1):
        myexactlog(7, 0)
        A[i] = A[i - 2] + 2 * B[i - 1]
        myexactlog(8, A)
        B[i] = A[i - 1] + B[i - 2]
        myexactlog(9, B)
        break
    retval_1 = A[n]
    myexactlog(10, retval_1)
    myexactlog(11, retval_1)
    return retval_1