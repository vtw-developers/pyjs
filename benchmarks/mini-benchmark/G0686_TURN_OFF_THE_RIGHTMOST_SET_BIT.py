def test():
    params = [9, 54, 60, 32, 41, 64, 4, 51, 57, 92]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    return n & (n - 1)
"-----------------"
test()