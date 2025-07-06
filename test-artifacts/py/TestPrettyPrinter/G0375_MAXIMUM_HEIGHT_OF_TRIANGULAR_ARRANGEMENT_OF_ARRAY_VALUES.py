def f_gold(a, n):
    result = 1
    for i in range(1, n):
        y = (i * (i + 1)) / 2
        if y < n:
            result = i
        else:
            break
    return result