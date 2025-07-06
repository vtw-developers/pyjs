def f_gold(x1, y1, x2, y2, r1, r2):
    distSq = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)
    radSumSq = (r1 + r2) * (r1 + r2)
    if distSq == radSumSq:
        return 1
    elif distSq > radSumSq:
        return -1
    else:
        return 0