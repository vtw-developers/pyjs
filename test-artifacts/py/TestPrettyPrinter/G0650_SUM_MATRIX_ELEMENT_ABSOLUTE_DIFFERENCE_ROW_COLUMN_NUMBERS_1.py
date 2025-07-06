def f_gold(n):
    sum = 0
    for i in range(n):
        sum += i * (n - i)
    return 2 * sum