import math
def f_gold(n):
    res = 1
    while n % 2 == 0:
        n = n // 2
    for i in range(3, int(math.sqrt(n) + 1)):
        count = 0
        curr_sum = 1
        curr_term = 1
        while n % i == 0:
            count += 1
            n = n // i
            curr_term *= i
            curr_sum += curr_term
        res *= curr_sum
    if n >= 2:
        res *= 1 + n
    return res