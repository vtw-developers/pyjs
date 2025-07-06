def f_gold(n):
    S = 0
    for i in range(1, n + 1):
        S += i * i - (i - 1) * (i - 1)
    return S