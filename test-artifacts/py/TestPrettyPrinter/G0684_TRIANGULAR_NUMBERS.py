def f_gold(num):
    if num < 0:
        return False
    sum, n = 0, 1
    while sum <= num:
        sum = sum + n
        if sum == num:
            return True
        n += 1
    return False