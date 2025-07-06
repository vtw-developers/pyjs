def f_gold(n):
    while int(n / 100):
        last_digit = int(n % 10)
        n = int(n / 10)
        n += last_digit * 3
    return n % 29 == 0