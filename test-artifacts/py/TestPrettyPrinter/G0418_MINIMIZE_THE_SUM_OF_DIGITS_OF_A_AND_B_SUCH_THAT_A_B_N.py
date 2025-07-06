def f_gold(n):
    sum = 0
    while n > 0:
        sum += n % 10
        n //= 10
    if sum == 1:
        return 10
    return sum