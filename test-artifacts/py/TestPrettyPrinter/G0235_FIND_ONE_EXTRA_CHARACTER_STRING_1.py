def f_gold(strA, strB):
    res = 0
    for i in range(0, len(strA)):
        res = res ^ (ord)(strA[i])
    for i in range(0, len(strB)):
        res = res ^ (ord)(strB[i])
    return (chr)(res)