def f_gold(n):
    position = 1
    m = 1
    while not (n & m):
        m = m << 1
        position += 1
    return position