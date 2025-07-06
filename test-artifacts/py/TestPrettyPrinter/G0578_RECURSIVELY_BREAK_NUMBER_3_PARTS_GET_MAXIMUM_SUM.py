def f_gold(n):
    if n == 0 or n == 1:
        return n
    return max((f_gold(n // 2) + f_gold(n // 3) + f_gold(n // 4)), n)