def test():
    params = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    pPrevPrev = 1
    pPrev = 1
    pCurr = 1
    pNext = 1
    for i in range(3, n + 1):
        pNext = pPrevPrev + pPrev
        pPrevPrev = pPrev
        pPrev = pCurr
        pCurr = pNext
    return pNext
"-----------------"
test()