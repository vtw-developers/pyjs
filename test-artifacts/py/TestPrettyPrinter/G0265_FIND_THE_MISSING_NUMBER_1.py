def f_gold(a, n):
    i, total = 0, 1
    for i in range(2, n + 2):
        total += i
        total -= a[i - 2]
    return total