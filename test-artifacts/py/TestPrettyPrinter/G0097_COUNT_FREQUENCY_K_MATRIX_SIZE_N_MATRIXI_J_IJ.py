def f_gold(n, k):
    if n + 1 >= k:
        return k - 1
    else:
        return 2 * n + 1 - k