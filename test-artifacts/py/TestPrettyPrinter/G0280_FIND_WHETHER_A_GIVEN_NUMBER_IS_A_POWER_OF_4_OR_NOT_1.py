def f_gold(n):
    count = 0
    if n and (not (n & (n - 1))):
        while n > 1:
            n >>= 1
            count += 1
        if count % 2 == 0:
            return True
        else:
            return False