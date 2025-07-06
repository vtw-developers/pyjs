def f_gold(x):
    i = 1
    fact = 1
    for i in range(1, x):
        fact = fact * i
        if fact % x == 0:
            break
    return i