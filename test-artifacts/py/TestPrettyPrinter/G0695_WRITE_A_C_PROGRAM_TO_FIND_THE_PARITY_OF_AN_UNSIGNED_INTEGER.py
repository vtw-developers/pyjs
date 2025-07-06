def f_gold(n):
    parity = 0
    while n:
        parity = ~parity
        n = n & (n - 1)
    return parity