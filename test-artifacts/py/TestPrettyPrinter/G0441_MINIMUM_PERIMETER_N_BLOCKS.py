import math
def f_gold(n):
    l = math.sqrt(n)
    sq = l * l
    if sq == n:
        return l * 4
    else:
        row = n / l
        perimeter = 2 * (l + row)
        if n % l != 0:
            perimeter += 2
        return perimeter