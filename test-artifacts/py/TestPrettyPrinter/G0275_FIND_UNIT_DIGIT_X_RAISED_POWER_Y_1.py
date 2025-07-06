import math
def f_gold(x, y):
    x = x % 10
    if y != 0:
        y = y % 4 + 4
    return ((int)(math.pow(x, y))) % 10