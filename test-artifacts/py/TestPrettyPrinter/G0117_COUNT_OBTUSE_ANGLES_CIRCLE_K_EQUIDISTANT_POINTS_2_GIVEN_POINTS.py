def f_gold(a, b, k):
    c1 = (b - a) - 1
    c2 = (k - b) + (a - 1)
    if c1 == c2:
        return 0
    return min(c1, c2)