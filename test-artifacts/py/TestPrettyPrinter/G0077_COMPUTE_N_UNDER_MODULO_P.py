def f_gold(n, p):
    if n >= p:
        return 0
    result = 1
    for i in range(1, n + 1):
        result = (result * i) % p
    return result