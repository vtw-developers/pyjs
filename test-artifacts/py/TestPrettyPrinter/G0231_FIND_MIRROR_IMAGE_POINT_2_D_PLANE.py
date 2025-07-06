def f_gold(a, b, c, x1, y1):
    temp = -2 * (a * x1 + b * y1 + c) / (a * a + b * b)
    x = temp * a + x1
    y = temp * b + y1
    return (x, y)