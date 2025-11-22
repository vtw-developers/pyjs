def test():
    params = [63, 78, 13, 5, 34, 69, 63, 78, 80, 19]
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