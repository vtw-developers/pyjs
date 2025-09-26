def f_gold(arr, n):
    dp = [0] * n
    myexactlog(1, dp)
    if n == 1:
        myexactlog(2, 0)
        retval_1 = arr[0]
        myexactlog(3, retval_1)
        myexactlog(4, retval_1)
        return retval_1
    if n == 2:
        myexactlog(5, 1)
        retval_2 = min(arr[0], arr[1])
        myexactlog(6, retval_2)
        myexactlog(7, retval_2)
        return retval_2
    if n == 3:
        myexactlog(8, 2)
        retval_3 = min(arr[0], min(arr[1], arr[2]))
        myexactlog(9, retval_3)
        myexactlog(10, retval_3)
        return retval_3
    if n == 4:
        myexactlog(11, 3)
        pass