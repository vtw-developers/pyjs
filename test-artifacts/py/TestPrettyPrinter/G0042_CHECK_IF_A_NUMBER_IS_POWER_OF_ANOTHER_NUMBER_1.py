import math
def f_gold(x, y):
    res1 = math.log(y) / math.log(x)
    res2 = math.log(y) / math.log(x)
    return 1 if (res1 == res2) else 0