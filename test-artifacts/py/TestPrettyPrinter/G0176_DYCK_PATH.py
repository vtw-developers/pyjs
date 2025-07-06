def f_gold(n):
    res = 1
    for i in range(0, n):
        res *= 2 * n - i
        res /= i + 1
    return res / (n + 1)