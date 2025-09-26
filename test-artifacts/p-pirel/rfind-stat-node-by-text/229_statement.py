for j in range(i + 1, n):
    myexactlog(9, 1)
    if templeHeight[j] < templeHeight[j - 1]:
        myexactlog(10, 1)
        right += 1
        myexactlog(11, right)
    else:
        myexactlog(12, 1)
        pass
    break