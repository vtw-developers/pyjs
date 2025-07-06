import math
def f_gold(n):
    nthElement = 19 + (n - 1) * 9
    outliersCount = int(math.log10(nthElement)) - 1
    nthElement += 9 * outliersCount
    return nthElement