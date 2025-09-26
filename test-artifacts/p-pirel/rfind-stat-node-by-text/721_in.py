def f_gold(blockSize, m, processSize, n):
    allocation = [-1] * n
    myexactlog(1, allocation)
    for i in range(n):
        myexactlog(2, 1)
        wstIdx = -1
        myexactlog(3, wstIdx)
        for j in range(m):
            myexactlog(4, 0)
            if blockSize[j] >= processSize[i]:
                myexactlog(5, 1)
                if wstIdx == -1:
                    myexactlog(6, 0)
                    pass
                elif blockSize[wstIdx] < blockSize[j]:
                    myexactlog(7, 0)
                    pass