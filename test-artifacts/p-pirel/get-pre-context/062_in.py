def f_gold(num):
    if num // 10 == 0:
        return True
    while num // 10 != 0:
        digit1 = num % 10
        digit2 = (num // 10) % 10
        if abs(digit2 - digit1) > 1:
            return False
        num = num // 10
    return True