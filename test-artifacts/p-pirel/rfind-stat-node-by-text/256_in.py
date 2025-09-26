def f_gold(arr, n, k):
    if k > n:
        myexactlog(1, 0)
        retval_1 = -1
        myexactlog(2, retval_1)
        myexactlog(3, retval_1)
        return retval_1
    csum = [0] * n
    myexactlog(4, csum)
    csum[0] = arr[0]
    myexactlog(5, csum)
    for i in range(1, n):
        myexactlog(6, 0)
        csum[i] = csum[i - 1] + arr[i]
        myexactlog(7, csum)
        break
    max_sum = csum[k - 1]
    myexactlog(8, max_sum)
    max_end = k - 1
    myexactlog(9, max_end)
    for i in range(k, n):
        myexactlog(10, 1)
        curr_sum = csum[i] - csum[i - k]
        myexactlog(11, curr_sum)
        if curr_sum > max_sum:
            myexactlog(12, 1)
            max_sum = curr_sum
            myexactlog(13, max_sum)
            max_end = i
            myexactlog(14, max_end)
        break