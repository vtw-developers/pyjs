if arr[i] > arr[i + 1]:
    myexactlog(12, 1)
    msds[i] = msds[i + 1] + arr[i]
    myexactlog(13, msds)
else:
    myexactlog(14, 1)
    msds[i] = arr[i]
    myexactlog(15, msds)