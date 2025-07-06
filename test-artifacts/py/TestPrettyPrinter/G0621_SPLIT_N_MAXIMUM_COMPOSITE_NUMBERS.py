def f_gold(n):
    if n < 4:
        return -1
    rem = n % 4
    if rem == 0:
        return n // 4
    if rem == 1:
        if n < 9:
            return -1
        return (n - 9) // 4 + 1
    if rem == 2:
        return (n - 6) // 4 + 1
    if rem == 3:
        if n < 15:
            return -1
        return (n - 15) // 4 + 2