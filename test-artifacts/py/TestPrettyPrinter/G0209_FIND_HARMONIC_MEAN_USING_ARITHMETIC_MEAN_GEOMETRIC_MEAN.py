import math
def f_gold(a, b):
    AM = (a + b) / 2
    GM = math.sqrt(a * b)
    HM = (GM * GM) / AM
    return HM