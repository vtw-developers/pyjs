for i in range(n):
    myexactlog(13, 2)
    print(i + 1, "         ", processSize[i], end="     ")
    if allocation[i] != -1:
        myexactlog(14, 3)
        print(allocation[i] + 1)
    else:
        myexactlog(15, 0)
        pass
    break