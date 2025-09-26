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
                    wstIdx = j
                    myexactlog(7, wstIdx)
                elif blockSize[wstIdx] < blockSize[j]:
                    myexactlog(8, 0)
                    wstIdx = j
                    myexactlog(9, wstIdx)
            break
        if wstIdx != -1:
            myexactlog(10, 2)
            allocation[i] = wstIdx
            myexactlog(11, allocation)
            blockSize[wstIdx] -= processSize[i]
            myexactlog(12, blockSize)