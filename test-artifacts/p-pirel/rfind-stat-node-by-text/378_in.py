def f_gold(blockSize, m, processSize, n):
    allocation = [-1] * n
    myexactlog(1, allocation)
    for i in range(n):
        myexactlog(2, 1)
        bestIdx = -1
        myexactlog(3, bestIdx)
        for j in range(m):
            myexactlog(4, 0)
            if blockSize[j] >= processSize[i]:
                myexactlog(5, 1)
                if bestIdx == -1:
                    myexactlog(6, 0)
                    bestIdx = j
                    myexactlog(7, bestIdx)
                elif blockSize[bestIdx] > blockSize[j]:
                    myexactlog(8, 0)
                    bestIdx = j
                    myexactlog(9, bestIdx)
            break
        break