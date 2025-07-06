import math
def f_gold(r):
    if r <= 0:
        return 0
    result = 4
    for x in range(1, r):
        ySquare = r * r - x * x
        y = int(math.sqrt(ySquare))
        if y * y == ySquare:
            result += 4
    return result