def f_gold(n, k):
    if k <= 0:
        return n
    return n & ~(1 << (k - 1))