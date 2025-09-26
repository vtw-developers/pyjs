for i in range(n):
    myexactlog(2, 0)
    j = 0
    myexactlog(3, j)
    while j < n:
        myexactlog(4, 0)
        if i != j and arr[j] == arr[i]:
            myexactlog(5, 0)
            break
        j += 1
        myexactlog(6, j)
        break
    if j == n:
        myexactlog(7, 1)
        dist_count += 1
        myexactlog(8, dist_count)
    if dist_count == k:
        myexactlog(9, 2)
        retval_1 = arr[i]
        myexactlog(10, retval_1)
        myexactlog(11, retval_1)
        return retval_1
    break