def f_gold(n, r, b, g):
    fact = [0 for i in range(n + 1)]
    fact[0] = 1
    for i in range(1, n + 1, 1):
        fact[i] = fact[i - 1] * i