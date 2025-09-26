def f_gold(n):
    ar = [0] * 10
    while n > 0:
        digit = n % 10
        if ar[digit]:
            return 0
        ar[digit] = 1
        n = n // 10