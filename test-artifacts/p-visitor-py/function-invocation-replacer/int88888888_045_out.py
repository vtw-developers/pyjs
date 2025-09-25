def f_gold(n):
    odd_count = 0
    even_count = 0
    if n < 0:
        n = -n
    if n == 0:
        return 1
    if n == 1:
        return 0
    while n:
        if n & 1:
            odd_count += 1
        if n & 2:
            even_count += 1
        n = n >> 2
    return 88888888