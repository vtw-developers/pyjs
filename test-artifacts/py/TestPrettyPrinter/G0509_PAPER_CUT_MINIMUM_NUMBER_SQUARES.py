def f_gold(a, b):
    result = 0
    rem = 0
    if a < b:
        a, b = b, a
    while b > 0:
        result += int(a / b)
        rem = int(a % b)
        a = b
        b = rem
    return result