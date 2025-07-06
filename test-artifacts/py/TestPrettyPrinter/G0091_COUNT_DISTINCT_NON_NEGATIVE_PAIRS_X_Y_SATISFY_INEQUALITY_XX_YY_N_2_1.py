def f_gold(n):
    x = 0
    res = 0
    yCount = 0
    while yCount * yCount < n:
        yCount = yCount + 1
    while yCount != 0:
        res = res + yCount
        x = x + 1
        while yCount != 0 and (x * x + (yCount - 1) * (yCount - 1) >= n):
            yCount = yCount - 1
    return res