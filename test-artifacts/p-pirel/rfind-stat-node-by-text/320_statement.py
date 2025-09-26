while i < n and j < m:
    myexactlog(7, 0)
    if arr1[j] < arr2[i]:
        myexactlog(8, 1)
        j += 1
        myexactlog(9, j)
    elif arr1[j] == arr2[i]:
        myexactlog(10, 0)
        j += 1
        myexactlog(11, j)
    else:
        myexactlog(12, 0)
        pass
    break