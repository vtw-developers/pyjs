def f_gold(a, b):
    if a == 0:
        return b
    return f_gold(b % a, a)