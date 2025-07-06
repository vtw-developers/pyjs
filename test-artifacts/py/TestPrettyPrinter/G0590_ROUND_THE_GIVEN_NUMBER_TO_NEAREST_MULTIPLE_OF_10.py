def f_gold(n):
    a = (n // 10) * 10
    b = a + 10
    return b if n - a > b - n else a