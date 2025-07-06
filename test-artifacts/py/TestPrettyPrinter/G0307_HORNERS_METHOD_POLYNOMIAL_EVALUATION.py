def f_gold(poly, n, x):
    result = poly[0]
    for i in range(1, n):
        result = result * x + poly[i]
    return result