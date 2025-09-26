def f_gold(arr1, arr2, m, n):
    i = 0
    myexactlog(1, i)
    j = 0
    myexactlog(2, j)
    if m < n:
        myexactlog(3, 0)
        myexactlog(4, 0)
        return 0
    arr1.sort()
    myexactlog(5, arr1)
    arr2.sort()
    myexactlog(6, arr2)
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
            i += 1
            myexactlog(12, i)
        else:
            myexactlog(13, 0)
            myexactlog(14, 0)
            return 0