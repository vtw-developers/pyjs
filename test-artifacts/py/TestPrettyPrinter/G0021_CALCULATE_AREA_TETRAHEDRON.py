import math
def f_gold(side):
    volume = side ** 3 / (6 * math.sqrt(2))
    return round(volume, 2)