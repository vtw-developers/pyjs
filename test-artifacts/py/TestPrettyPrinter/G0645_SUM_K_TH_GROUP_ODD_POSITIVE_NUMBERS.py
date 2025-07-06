def f_gold(k):
    cur = int((k * (k - 1)) + 1)
    sum = 0
    while k:
        sum += cur
        cur += 2
        k = k - 1
    return sum