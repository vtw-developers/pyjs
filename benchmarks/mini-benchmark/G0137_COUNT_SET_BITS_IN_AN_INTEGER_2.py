def test():
    params = [32, 94, 33, 99, 17, 64, 80, 42, 12, 86]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    count = 0
    while n != 0:
        n &= n - 1
        count += 1
    return count
"-----------------"
test()