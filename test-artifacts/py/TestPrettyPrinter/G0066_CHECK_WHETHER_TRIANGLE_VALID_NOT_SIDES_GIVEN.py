def f_gold(a, b, c):
    if (a + b <= c) or (a + c <= b) or (b + c <= a):
        return False
    else:
        return True