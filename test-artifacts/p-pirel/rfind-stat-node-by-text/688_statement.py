for j in range(i):
    myexactlog(6, 1)
    if arr[i] > arr[j] and (i - j) <= (arr[i] - arr[j]):
        myexactlog(7, 0)
        LIS[i] = max(LIS[i], LIS[j] + 1)
        myexactlog(8, LIS)
    break