def f_gold(num):
    if num < 0:
        return f_gold(-num)
    if num == 0 or num == 7:
        return True
    if num < 10:
        return False
    return f_gold(num / 10 - 2 * (num - num / 10 * 10))