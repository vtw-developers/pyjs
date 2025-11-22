def test():
    params = [58, 92, 73, 52, 24, 14, 58, 11, 8, 52]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    count = 0
    while n != 0:
        count += n & 1
        n >>= 1
    return count
"-----------------"
test()