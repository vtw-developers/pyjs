def test():
    params = [60, 20, 33, 34, 68, 79, 20, 41, 36, 17]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    n -= 1
    n |= n >> 1
    n |= n >> 2
    n |= n >> 4
    n |= n >> 8
    n |= n >> 16
    n += 1
    return n
"-----------------"
test()