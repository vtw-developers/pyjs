def test():
    params = [63, 64, 85, 36, 20, 63, 42, 19, 62, 97]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    parity = 0
    while n != 0:
        parity = ~parity
        n = n & (n - 1)
    return parity
"-----------------"
test()