def f_gold(n):
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count