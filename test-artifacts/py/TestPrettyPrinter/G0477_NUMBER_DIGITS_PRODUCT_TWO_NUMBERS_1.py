import math
def f_gold(a, b):
    if a == 0 or b == 0:
        return 1
    return math.floor(math.log10(abs(a)) + math.log10(abs(b))) + 1