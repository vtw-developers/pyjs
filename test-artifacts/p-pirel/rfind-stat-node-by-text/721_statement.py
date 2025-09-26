if blockSize[j] >= processSize[i]:
    myexactlog(5, 1)
    if wstIdx == -1:
        myexactlog(6, 0)
        pass
    elif blockSize[wstIdx] < blockSize[j]:
        myexactlog(7, 0)
        pass