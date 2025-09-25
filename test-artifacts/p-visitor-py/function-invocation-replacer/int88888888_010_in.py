import math
def f_gold(n):
    if n < 10:
        retval_1 = n * (n + 1) / 2
        return retval_1
    d = int(math.log10(n))
    a = [0] * (d + 1)
    a[0] = 0
    a[1] = 45
    for i in range(2, d + 1):
        a[i] = a[i - 1] * 10 + 45 * int(math.ceil(math.pow(10, i - 1)))
    p = int(math.ceil(math.pow(10, d)))
    msd = n // p
    retval_2 = int(msd * a[d] + (msd * (msd - 1) // 2) * p + msd * (1 + n % p) + f_gold(n % p))
    return retval_2