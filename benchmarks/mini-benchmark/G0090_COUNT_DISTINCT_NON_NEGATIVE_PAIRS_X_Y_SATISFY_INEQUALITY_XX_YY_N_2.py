def test():
    params = [61, 45, 53, 4, 82, 86, 37, 48, 81, 50]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    res = 0
    x = 0
    while x * x < n:
        y = 0
        while x * x + y * y < n:
            res = res + 1
            y = y + 1
        x = x + 1
    return res
"-----------------"
test()