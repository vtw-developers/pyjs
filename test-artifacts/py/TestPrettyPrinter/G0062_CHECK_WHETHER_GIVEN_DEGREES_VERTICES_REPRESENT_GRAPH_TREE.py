def f_gold(degree, n):
    deg_sum = sum(degree)
    if 2 * (n - 1) == deg_sum:
        return True
    else:
        return False