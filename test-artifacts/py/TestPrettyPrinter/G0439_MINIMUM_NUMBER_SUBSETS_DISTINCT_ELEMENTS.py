def f_gold(ar, n):
    res = 0
    ar.sort()
    for i in range(0, n):
        count = 1
        for i in range(n - 1):
            if ar[i] == ar[i + 1]:
                count += 1
            else:
                break
        res = max(res, count)
    return res