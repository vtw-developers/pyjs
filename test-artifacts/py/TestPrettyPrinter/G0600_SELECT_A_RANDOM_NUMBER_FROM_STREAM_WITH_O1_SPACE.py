def f_gold(x):
    res = 0
    count = 0
    count += 1
    if count == 1:
        res = x
    else:
        i = random.randrange(count)
        if i == count - 1:
            res = x
    return res