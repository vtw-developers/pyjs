import math
def f_gold(C, l):
    if l >= C:
        return C
    eq_root = (math.sqrt(1 + 8 * (C - l)) - 1) / 2
    return math.ceil(eq_root) + l