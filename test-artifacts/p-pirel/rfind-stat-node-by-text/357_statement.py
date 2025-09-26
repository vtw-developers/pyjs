for i in range(1, n - 1):
    myexactlog(9, 0)
    subtract = arr[i] - k
    myexactlog(10, subtract)
    add = arr[i] + k
    myexactlog(11, add)
    if subtract >= small or add <= big:
        myexactlog(12, 2)
        continue
    if big - subtract <= add - small:
        myexactlog(13, 3)
        pass
    else:
        myexactlog(14, 0)
        pass
    break