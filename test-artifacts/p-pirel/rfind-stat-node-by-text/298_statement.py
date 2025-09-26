for i in range(n - 2, 0, -1):
    myexactlog(7, 0)
    if num[i] > num[right]:
        myexactlog(8, 0)
        rightMin[i] = right
        myexactlog(9, rightMin)
    else:
        myexactlog(10, 0)
        rightMin[i] = -1
        myexactlog(11, rightMin)
        right = i
        myexactlog(12, right)
    break