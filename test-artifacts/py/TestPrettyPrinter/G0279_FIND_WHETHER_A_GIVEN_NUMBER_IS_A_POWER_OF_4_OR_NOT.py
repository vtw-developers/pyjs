def f_gold(n):
    if n == 0:
        return False
    while n != 1:
        if n % 4 != 0:
            return False
        n = n // 4
    return True