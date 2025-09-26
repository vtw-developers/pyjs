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