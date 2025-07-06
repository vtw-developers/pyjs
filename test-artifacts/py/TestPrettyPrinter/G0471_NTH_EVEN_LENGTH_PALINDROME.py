def f_gold(n):
    res = n
    for j in range(len(n) - 1, -1, -1):
        res += n[j]
    return res