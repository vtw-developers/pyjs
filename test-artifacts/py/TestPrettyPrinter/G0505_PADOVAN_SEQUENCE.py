def f_gold(n):
    pPrevPrev, pPrev, pCurr, pNext = 1, 1, 1, 1
    for i in range(3, n + 1):
        pNext = pPrevPrev + pPrev
        pPrevPrev = pPrev
        pPrev = pCurr
        pCurr = pNext
    return pNext