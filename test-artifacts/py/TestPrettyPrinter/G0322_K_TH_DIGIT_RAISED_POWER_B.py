def f_gold(a, b, k):
    p = a ** b
    count = 0
    while p > 0 and count < k:
        rem = p % 10
        count = count + 1
        if count == k:
            return rem
        p = p / 10