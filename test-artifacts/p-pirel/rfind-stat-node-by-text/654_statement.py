if wstIdx != -1:
    myexactlog(10, 2)
    allocation[i] = wstIdx
    myexactlog(11, allocation)
    blockSize[wstIdx] -= processSize[i]
    myexactlog(12, blockSize)