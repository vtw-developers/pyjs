def f_gold(x, y):
    if y == 0:
        return 0
    if y > 0:
        return x + f_gold(x, y - 1)
    if y < 0:
        return -f_gold(x, -y)