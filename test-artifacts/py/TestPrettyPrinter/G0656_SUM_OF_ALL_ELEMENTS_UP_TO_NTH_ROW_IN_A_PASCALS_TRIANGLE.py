def f_gold(n):
    sum = 0
    for row in range(n):
        sum = sum + (1 << row)
    return sum