import math
def f_gold(n, k):
    while n % 2 == 0:
        k = k - 1
        n = n / 2
        if k == 0:
            return 2
    i = 3
    while i <= math.sqrt(n):
        while n % i == 0:
            if k == 1:
                return i
            k = k - 1
            n = n / i
        i = i + 2
    if n > 2 and k == 1:
        return n
    return -1