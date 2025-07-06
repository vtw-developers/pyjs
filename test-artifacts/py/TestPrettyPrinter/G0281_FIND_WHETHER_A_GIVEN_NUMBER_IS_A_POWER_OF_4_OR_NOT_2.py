def f_gold(n):
    return n != 0 and ((n & (n - 1)) == 0) and not (n & 0xAAAAAAAA)