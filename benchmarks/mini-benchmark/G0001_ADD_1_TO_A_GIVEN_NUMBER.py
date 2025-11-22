def test():
    params = [96, 66, 67, 13, 75, 78, 1, 83, 27, 65]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(x):
    m = 1
    while x & m != 0:
        x = x ^ m
        m <<= 1
    x = x ^ m
    return x
"-----------------"
test()