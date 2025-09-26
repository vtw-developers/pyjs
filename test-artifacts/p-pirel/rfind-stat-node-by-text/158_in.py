def f_gold(arr1, arr2, m, n, k):
    sorted1 = [0] * (m + n)
    myexactlog(1, sorted1)
    i = 0
    myexactlog(2, i)
    j = 0
    myexactlog(3, j)
    d = 0
    myexactlog(4, d)
    while i < m and j < n:
        myexactlog(5, 0)
        if arr1[i] < arr2[j]:
            myexactlog(6, 0)
            sorted1[d] = arr1[i]
            myexactlog(7, sorted1)
            i += 1
            myexactlog(8, i)
        else:
            myexactlog(9, 0)
            sorted1[d] = arr2[j]
            myexactlog(10, sorted1)
            j += 1
            myexactlog(11, j)
        d += 1
        myexactlog(12, d)
        break
    while i < m:
        myexactlog(13, 1)
        sorted1[d] = arr1[i]
        myexactlog(14, sorted1)
        d += 1
        myexactlog(15, d)
        i += 1
        myexactlog(16, i)
        break
    while j < n:
        myexactlog(17, 2)
        sorted1[d] = arr2[j]